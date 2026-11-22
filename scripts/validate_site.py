#!/usr/bin/env python3
"""Static quality gates for the sixteen-module Linear Algebra course."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_PATHS = sorted((ROOT / "content").glob("[0-9][0-9]-*/index.html"))
EXPECTED_ARTICLES = 16

class MathAudit(HTMLParser):
    ARITY = {"mfrac": 2, "msub": 2, "msup": 2, "msubsup": 3,
             "munder": 2, "mover": 2, "munderover": 3}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.inside_math, self.errors, self.math_count = [], False, [], 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "math":
            self.math_count += 1
            self.inside_math = True
            if not attrs.get("aria-label") and not attrs.get("aria-labelledby"):
                self.errors.append("MathML without accessible description")
            if attrs.get("display") == "block":
                if not any(t == "div" and ("data-math-scroll" in a or "math-scroll" in a.get("class", "").split()) for t, _, a in self.stack):
                    self.errors.append("Display MathML outside a keyboard-scrollable region")
        if not self.inside_math:
            self.stack.append((tag, 0 if tag in self.ARITY else None, attrs))
            return
        if self.stack and self.stack[-1][0] in self.ARITY:
            parent_tag, count, parent_attrs = self.stack[-1]
            self.stack[-1] = (parent_tag, count + 1, parent_attrs)
        self.stack.append((tag, 0 if tag in self.ARITY else None, attrs))
    def handle_endtag(self, tag):
        if tag == "math": self.inside_math = False
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
        self.h1 = self.h2 = self.figures = self.figcaptions = self.demos = 0
        self.links, self.images, self.external_assets, self.errors = [], [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "div" and a.get("data-demo"): self.demos += 1
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "img":
            if not a.get("alt"): self.errors.append("Image missing alt text")
            if a.get("src"): self.images.append(a["src"])
        if tag == "script" and a.get("src", "").startswith(("http://", "https://")):
            self.external_assets.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet" and a.get("href", "").startswith(("http://", "https://")):
            self.external_assets.append(a["href"])

def audit_page(path: Path, kind="article"):
    source = path.read_text(encoding="utf-8")
    page, math = PageAudit(), MathAudit()
    page.feed(source); math.feed(source)
    errors = list(page.errors) + list(math.errors)
    if page.h1 != 1: errors.append(f"Expected exactly one h1, found {page.h1}")
    if kind == "article":
        is_second_batch = int(path.parent.name[:2]) >= 9
        if is_second_batch:
            if page.h2 < 8: errors.append(f"Expected at least eight h2 sections, found {page.h2}")
            if math.math_count < 8: errors.append(f"Expected at least eight MathML expressions, found {math.math_count}")
            if page.figures < 8 or page.figcaptions < 8: errors.append("Article needs at least eight figures with captions")
        else:
            if page.h2 < 5: errors.append(f"Expected at least five h2 sections, found {page.h2}")
            if math.math_count < 4: errors.append(f"Expected at least four MathML expressions, found {math.math_count}")
            if page.figures < 1 or page.figcaptions < 1: errors.append("Article needs a figure and caption")
        if page.demos < 1: errors.append("Article needs one meaningful interactive demo")
    elif kind == "lab":
        if page.h2 < 2 or math.math_count < 1 or page.figures < 1 or page.demos < 1:
            errors.append("Lab needs headings, MathML, a figure and an interactive input")
    for href in page.links + page.images:
        if href.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")): continue
        clean = href.split("#", 1)[0].split("?", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"Broken local link/asset: {href}")
    if page.external_assets: errors.append("External CSS/JS dependency: " + ", ".join(page.external_assets))
    return {"path": str(path.relative_to(ROOT)), "h2": page.h2, "mathml": math.math_count,
            "figures": page.figures, "demos": page.demos, "errors": errors}

def main():
    failures = []
    home = ROOT / "index.html"
    if not home.exists():
        failures.append({"path":"index.html","errors":["Missing homepage"]})
    else:
        r = audit_page(home, "home")
        if r["errors"]: failures.append(r)
        print(f"{'PASS' if not r['errors'] else 'FAIL'} index.html | homepage")
    if len(ARTICLE_PATHS) != EXPECTED_ARTICLES:
        failures.append({"path":"content","errors":[f"Expected {EXPECTED_ARTICLES} articles, found {len(ARTICLE_PATHS)}"]})
    for path in ARTICLE_PATHS:
        r = audit_page(path, "article")
        evidence_path = path.parent / "evidence.json"
        if not evidence_path.exists():
            r["errors"].append("Missing evidence.json")
        else:
            try:
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
                claims = evidence.get("evidence", [])
                if len(claims) < 3: r["errors"].append("evidence.json needs at least three claim/source entries")
                if any(x.get("status") not in ("verified","derived") for x in claims):
                    r["errors"].append("evidence.json contains an unsupported status")
            except (ValueError, OSError) as exc:
                r["errors"].append(f"Invalid evidence.json: {exc}")
        print(f"{'PASS' if not r['errors'] else 'FAIL'} {r['path']} | h2={r['h2']} math={r['mathml']} figures={r['figures']} demos={r['demos']}")
        if r["errors"]:
            for error in r["errors"]: print("  -", error)
            failures.append(r)
    lab = ROOT / "lab" / "index.html"
    if not lab.exists():
        failures.append({"path":"lab/index.html","errors":["Missing Matrix Computation Lab"]})
    else:
        r = audit_page(lab, "lab")
        print(f"{'PASS' if not r['errors'] else 'FAIL'} lab/index.html | matrix lab")
        if r["errors"]:
            for error in r["errors"]: print("  -", error)
            failures.append(r)
    diagrams = sorted((ROOT / "assets" / "diagrams").glob("*.svg"))
    if len(diagrams) < 72:
        failures.append({"path":"assets/diagrams","errors":[f"Expected at least 72 SVGs, found {len(diagrams)}"]})
    for svg_path in diagrams:
        try:
            root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
            ns = "{http://www.w3.org/2000/svg}"
            if not root.tag.endswith("svg"): raise ValueError("root is not svg")
            if not root.attrib.get("viewBox"): raise ValueError("missing viewBox")
            if root.find(ns+"title") is None or root.find(ns+"desc") is None:
                raise ValueError("missing SVG title or desc")
        except (ET.ParseError, ValueError) as exc:
            failures.append({"path":str(svg_path.relative_to(ROOT)),"errors":[f"Invalid accessible SVG: {exc}"]})
    if failures:
        print(f"\nFAILED: {len(failures)} page/asset audit(s)")
        return 1
    print(f"\nPASS: homepage, {len(ARTICLE_PATHS)} articles, matrix lab and {len(diagrams)} SVG assets checked")
    return 0

if __name__ == "__main__":
    sys.exit(main())
