#!/usr/bin/env python3
"""Static quality gates for the Linear Algebra teaching site (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import re
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

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.h1 = 0
        self.h2 = 0
        self.math = 0
        self.figures = 0
        self.figcaptions = 0
        self.svg = 0
        self.svg_title = 0
        self.svg_desc = 0
        self.errors = []
        self.links = []
        self.images = []
        self.external_assets = []
        self.demos = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "svg":
            self.svg += 1
            self.svg_title = 0
            self.svg_desc = 0
        if tag == "title" and any(x[0] == "svg" for x in self.stack): self.svg_title += 1
        if tag == "desc" and any(x[0] == "svg" for x in self.stack): self.svg_desc += 1
        if tag == "math":
            self.math += 1
            if not attrs.get("aria-label") and not attrs.get("aria-labelledby"):
                self.errors.append("MathML without aria-label/aria-labelledby")
            if attrs.get("display") == "block":
                if not any(t == "div" and ("data-math-scroll" in a or "math-scroll" in a.get("class", "").split()) for t, a in self.stack):
                    self.errors.append("Display MathML outside keyboard-scrollable region")
            if any(t == "svg" for t, _ in self.stack):
                self.errors.append("MathML nested inside SVG")
        if tag == "mfrac":
            self.stack.append((tag, attrs))
            return
        if tag == "div" and attrs.get("data-demo"): self.demos += 1
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag in ("img", "script", "link"):
            src = attrs.get("src") if tag != "link" else attrs.get("href")
            if tag == "img":
                if not attrs.get("alt"): self.errors.append("Image missing alt text")
                if src: self.images.append(src)
            if tag == "script" and src and src.startswith(("http://", "https://")):
                self.external_assets.append(src)
            if tag == "link" and attrs.get("rel") == "stylesheet" and src and src.startswith(("http://", "https://")):
                self.external_assets.append(src)
        if tag not in ("meta", "link", "img", "input", "br", "hr", "source", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "stop", "use"):
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "mfrac":
            for i in range(len(self.stack)-1, -1, -1):
                if self.stack[i][0] == "mfrac":
                    # Count element children is tracked by parser depth in a separate static scan below.
                    self.stack.pop(i)
                    break
            return
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if data.strip(): self.text.append(data.strip())

def audit(path: Path):
    source = path.read_text(encoding="utf-8")
    p = Audit()
    p.feed(source)
    errors = list(p.errors)
    if p.h1 != 1: errors.append(f"Expected exactly one h1, found {p.h1}")
    if path.parent != ROOT and p.h2 < 5: errors.append(f"Expected at least five h2 sections, found {p.h2}")
    if path.parent != ROOT and p.math < 4: errors.append(f"Expected at least four MathML expressions, found {p.math}")
    if path.parent != ROOT and (p.figures < 1 or "<figcaption" not in source): errors.append("Article needs a figure and caption")
    if path.parent != ROOT and p.demos < 1: errors.append("Article needs a meaningful interactive demo")
    if p.external_assets: errors.append("External CSS/JS dependency: " + ", ".join(p.external_assets))
    if re.search(r"<svg[\s\S]*?<math[\s\S]*?</svg>", source, re.I): errors.append("MathML appears inside SVG")
    if re.search(r"<mfrac\b[^>]*>(?:(?!</mfrac>).)*</mfrac>", source, re.S):
        for m in re.finditer(r"<mfrac\b[^>]*>(.*?)</mfrac>", source, re.S):
            children = re.findall(r"<(?:mi|mn|mo|mrow|mfrac|msub|msup|msubsup|mtext|msqrt|mtable)\b", m.group(1))
            if len(children) != 2: errors.append(f"mfrac must have exactly two element children (found {len(children)})")
    for href in p.links + p.images:
        if href.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")): continue
        clean = href.split("#", 1)[0].split("?", 1)[0]
        if not clean: continue
        target = (path.parent / clean).resolve()
        if not target.exists(): errors.append(f"Broken local link/asset: {href}")
    return {"path": str(path.relative_to(ROOT)), "h1": p.h1, "h2": p.h2, "mathml": p.math,
            "figures": p.figures, "demos": p.demos, "errors": errors}

def main():
    files = [ROOT / x for x in ARTICLES]\n    home = ROOT / "index.html"\n    if not home.exists(): failures = [{"path": "index.html", "errors": ["Missing homepage"]}]\n    else:\n        home_source = home.read_text(encoding="utf-8")\n        if home_source.count("<h1") != 1: failures = [{"path": "index.html", "errors": ["Homepage must have exactly one h1"]}]\n        else: failures = []
    failures = []
    for path in files:
        if not path.exists():
            failures.append({"path": str(path), "errors": ["Missing required page"]})
            continue
        result = audit(path)
        print(f"{'PASS' if not result['errors'] else 'FAIL'} {result['path']} | h2={result['h2']} math={result['mathml']} figures={result['figures']} demos={result['demos']}")
        for error in result["errors"]:
            print("  -", error)
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
    print(f"\nPASS: {len(files)} pages and {len(diagrams)} SVG assets checked")
    return 0

if __name__ == "__main__":
    sys.exit(main())
