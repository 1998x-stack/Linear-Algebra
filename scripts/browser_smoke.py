#!/usr/bin/env python3
"""Responsive, offline and interaction smoke tests for the published HTML course."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8765"
PAGES = [
    ("home", "/index.html"),
    ("01-vectors", "/content/01-vectors/index.html"),
    ("02-transformations", "/content/02-linear-transformations/index.html"),
    ("03-systems", "/content/03-linear-systems/index.html"),
    ("04-spaces", "/content/04-vector-spaces/index.html"),
    ("05-determinants", "/content/05-determinants/index.html"),
    ("06-eigenvalues", "/content/06-eigenvalues/index.html"),
    ("07-least-squares", "/content/07-least-squares/index.html"),
    ("08-svd", "/content/08-svd/index.html"),
]

def main():
    out = ROOT / "reports" / "browser"
    out.mkdir(parents=True, exist_ok=True)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    report = {"viewports": [], "interactions": [], "errors": []}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for width, height, label in [(1440, 1000, "desktop"), (390, 844, "mobile"), (360, 800, "mobile-small")]:
                for slug, route in PAGES:
                    page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
                    page_errors = []
                    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                    page.goto(BASE + route, wait_until="networkidle")
                    page.evaluate("() => document.fonts.ready")
                    metrics = page.evaluate("""() => ({
                      width: window.innerWidth,
                      documentWidth: document.documentElement.scrollWidth,
                      math: Array.from(document.querySelectorAll('math')).map(x => ({
                        ns: x.namespaceURI,
                        width: x.getBoundingClientRect().width,
                        height: x.getBoundingClientRect().height
                      })),
                      images: Array.from(document.images).map(x => ({
                        src: x.getAttribute('src'),
                        ok: x.complete && x.naturalWidth > 0
                      }))
                    })""")
                    errors = []
                    if metrics["documentWidth"] > metrics["width"] + 1:
                        errors.append(f"horizontal overflow {metrics['documentWidth']} > {metrics['width']}")
                    for i, item in enumerate(metrics["math"]):
                        if item["ns"] != "http://www.w3.org/1998/Math/MathML":
                            errors.append(f"MathML {i+1} has wrong namespace: {item['ns']}")
                        if item["width"] <= 0 or item["height"] <= 0:
                            errors.append(f"MathML {i+1} has zero geometry")
                    for item in metrics["images"]:
                        if not item["ok"]:
                            errors.append(f"image failed to load: {item['src']}")
                    if page_errors:
                        errors.extend("page error: " + x for x in page_errors)
                    report["viewports"].append({
                        "page": slug, "viewport": label, "width": width,
                        "mathml_count": len(metrics["math"]), "image_count": len(metrics["images"]),
                        "errors": errors
                    })
                    if errors:
                        report["errors"].extend(f"{slug} {label}: {e}" for e in errors)
                    if label in ("desktop", "mobile"):
                        page.screenshot(path=str(out / f"{slug}-{label}.png"), full_page=True, animations="disabled")
                    page.close()
            # Exercise one real control on every module.
            checks = [
                ("01-vectors", "/content/01-vectors/index.html",
                 "input[name=a]", "1.5", "[data-output=combo]", "5.50"),
                ("02-transformations", "/content/02-linear-transformations/index.html",
                 "input[name=shear]", "1.0", "[data-output=matrix]", "1.00"),
                ("03-systems", "/content/03-linear-systems/index.html",
                 "[data-step-next]", None, "[data-step-count]", "2 / 3"),
                ("04-spaces", "/content/04-vector-spaces/index.html",
                 "input[name=dependent]", None, "[data-output=rank]", "rank = 1"),
                ("05-determinants", "/content/05-determinants/index.html",
                 "input[name=scale]", "-1.0", "[data-output=det]", "-1.00"),
                ("06-eigenvalues", "/content/06-eigenvalues/index.html",
                 "input[name=lambda]", "2.0", "[data-output=eigen]", "2.0 v"),
                ("07-least-squares", "/content/07-least-squares/index.html",
                 "input[name=c]", "0.5", "[data-output=projection]", "0.50"),
                ("08-svd", "/content/08-svd/index.html",
                 "input[name=sigma]", "0.25", "[data-output=svd]", "0.25"),
            ]
            for slug, route, control, value, output, expected in checks:
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(BASE + route, wait_until="networkidle")
                if slug == "03-systems":
                    page.locator(control).click()
                elif slug == "04-spaces":
                    page.locator(control).check()
                else:
                    page.locator(control).evaluate(
                        "(el, value) => { el.value = value; el.dispatchEvent(new Event('input', {bubbles:true})); }",
                        value
                    )
                actual = page.locator(output).inner_text()
                ok = expected in actual
                report["interactions"].append({"page": slug, "expected": expected, "actual": actual, "passed": ok})
                if not ok:
                    report["errors"].append(f"{slug} interaction expected {expected!r}, got {actual!r}")
                page.close()
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"viewport_checks": len(report["viewports"]), "interaction_checks": len(report["interactions"]),
                      "errors": report["errors"]}, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
