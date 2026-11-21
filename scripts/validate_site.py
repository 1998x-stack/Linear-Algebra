#!/usr/bin/env python3
"""Static quality gates for the Linear Algebra teaching site (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = [
    "content/01-vectors/index.html",
    "content/02-linear-transformations/index.html",
    "content/03-linear-systems/index.html",
    "content/04-vector-spaces/index.html",
    "content/05-determinants/index.html",
    "content/06-eigenvalues/index.html",
    "content/07-least-squares/index.html",
    "content/08-svd/index.html",
]

class MathAudit(HTMLParser):
    """Check accessible MathML and direct-child arity for structural operators."""
    ARITY = {"mfrac": 2, "msub": 2, "msup": 2, "msubsup": 3,
             "munder": 2, "mover": 2, "munderover": 3}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.inside_math = False
        self.errors = []
        self.math_count = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "math":
            self.math_count += 1
            self.inside_math = True
            if not attrs.get("aria-label") and not attrs.get("aria-labelledby"):
                self.errors.append("MathML without accessible description")
            if attrs.get("display") == "block":
                if not any(t == "div" and ("data-math-scroll" in a or "math-scroll" in a.get("class", "").split()) for t, a in self.stack):
                    self.errors.append("Display MathML outside a keyboard-scrollable region")
        if not self.inside_math:
            self.stack.append((tag, attrs))
            return
        if self.stack and self.stack[-1][0] in self.ARITY:
            parent_tag, parent_count, parent_attrs = self.stack[-1]
            self.stack[-1] = (parent_tag, parent_count + 1, parent_attrs)
        self.stack.append((tag, 0 if tag in self.ARITY else None, attrs))
    def handle_endtag(self, tag):
        if tag == "math":
            self.inside_math = False
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                frame = self.stack[i]
                if tag in self.ARITY and frame[1] != self.ARITY[tag]:
                    self.errors.append(f"{tag} must have {self.ARITY[tag]} direct element children; found {frame[1]}")
                self.stack = self.stack[:i]
                break

class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.h1 = 0
        self.h2 = 0
        self.figures = 0
        self.figcaptions = 0
        self.links = []
        self.images = []
        self.external_assets = []
        self.demos = 0
        self.errors = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "div" and attrs.get("data-demo"): self.demos += 1
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "img":
            if not attrs.get("alt"): self.errors.append("Image missing alt text")
            if attrs.get("src"): self.images.append(attrs["src"])
        if tag == "script" and attrs.get("src", "").startswith(("http://", "https://")):
            self.external_assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href", "").startswith(("http://", "https://")):
            self.external_assets.append(attrs["href"])
        if tag not in ("meta", "link", "img", "input", "br", "hr", "source"):
            self.stack.append((tag, attrs))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break

def audit_page(path: Path, is_home=False):
    source = path.read_text(encoding="utf-8")
    page = PageAudit()
    page.feed(source)
    math = MathAudit()
    math.feed(source)
    errors = list(page.errors) + list(math.errors)
    if page.h1 != 1: errors.append(f"Expected exactly one h1, found {page.h1}")
    if not is_home:
        if page.h2 < 5: errors.append(f"Expected at least five h2 sections, found {page.h2}")
        if math.math_count < 4: errors.append(f"Expected at least four MathML expressions, found {math.math_count}")
        if page.figures < 1 or page.figcaptions < 1: errors.append("Article needs a figure and caption")
        if page.demos < 1: errors.append("Article needs a meaningful interactive demo")
    if page.external_assets: errors.append("External CSS/JS dependency: " + ", ".join(page.external_assets))
    for href in page.links + page.images:
        if href.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")): continue
        clean = href.split("#", 1)[0].split("?", 1)[0]
        if not clean: continue
        target = (path.parent / clean).resolve()
        if not target.exists(): errors.append(f"Broken local link/asset: {href}")
    return {"path": str(path.relative_to(ROOT)), "h2": page.h2, "mathml": math.math_count,
            "figures": page.figures, "demos": page.demos, "errors": errors}

def main():
    failures = []
    home = ROOT / "index.html"
    if not home.exists():
        failures.append({"path": "index.html", "errors": ["Missing homepage"]})
    else:
        result = audit_page(home, is_home=True)
        print(f"{'PASS' if not result['errors'] else 'FAIL'} {result['path']} | homepage")
        for error in result["errors"]: print("  -", error)
        if result["errors"]: failures.append(result)
    for relative in ARTICLES:
        path = ROOT / relative
        if not path.exists():
            failures.append({"path": relative, "errors": ["Missing required page"]})
            continue
        result = audit_page(path)
        print(f"{'PASS' if not result['errors'] else 'FAIL'} {result['path']} | h2={result['h2']} math={result['mathml']} figures={result['figures']} demos={result['demos']}")
        for error in result["errors"]: print("  -", error)
        if result["errors"]: failures.append(result)
    diagrams = sorted((ROOT / "assets/diagrams").glob("*.svg"))
    if len(diagrams) < 8:
        failures.append({"path": "assets/diagrams", "errors": [f"Expected at least 8 SVGs, found {len(diagrams)}"]})
    for svg in diagrams:
        data = svg.read_text(encoding="utf-8")
        for token in ('viewBox=', '<title', '<desc', 'xmlns="http://www.w3.org/2000/svg"'):
            if token not in data:
                failures.append({"path": str(svg.relative_to(ROOT)), "errors": [f"SVG missing {token}"]})
    if failures:
        print(f"\nFAILED: {len(failures)} page/asset audit(s)")
        return 1
    print(f"\nPASS: 1 homepage, {len(ARTICLES)} articles and {len(diagrams)} SVG assets checked")
    return 0

if __name__ == "__main__":
    sys.exit(main())
