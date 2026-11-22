#!/usr/bin/env python3
"""Responsive, offline and interaction smoke tests for all course pages."""
from pathlib import Path
import json
import subprocess
import sys
import time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE="http://127.0.0.1:8765"
PAGES=[
("home","/index.html"),
("01-vectors","/content/01-vectors/index.html"),
("02-transformations","/content/02-linear-transformations/index.html"),
("03-systems","/content/03-linear-systems/index.html"),
("04-spaces","/content/04-vector-spaces/index.html"),
("05-determinants","/content/05-determinants/index.html"),
("06-eigenvalues","/content/06-eigenvalues/index.html"),
("07-least-squares","/content/07-least-squares/index.html"),
("08-svd","/content/08-svd/index.html"),
("09-lu","/content/09-lu-decomposition/index.html"),
("10-qr","/content/10-qr-decomposition/index.html"),
("11-orthogonal","/content/11-orthogonal-matrices/index.html"),
("12-symmetric","/content/12-symmetric-matrices/index.html"),
("13-positive-definite","/content/13-positive-definite-quadratic-forms/index.html"),
("14-spectral","/content/14-spectral-theorem/index.html"),
("15-pca","/content/15-principal-component-analysis/index.html"),
("16-image-svd","/content/16-image-compression/index.html"),
("matrix-lab","/lab/index.html")]

def main():
    out=ROOT/"reports"/"browser";out.mkdir(parents=True,exist_ok=True)
    server=subprocess.Popen([sys.executable,"-m","http.server","8765","--bind","127.0.0.1"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(1);report={"viewports":[],"interactions":[],"errors":[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for width,height,label in [(1440,1000,"desktop"),(768,1024,"tablet"),(390,844,"mobile"),(360,800,"mobile-small")]:
                for slug,route in PAGES:
                    page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
                    errors=[];page.on("pageerror",lambda exc:errors.append(str(exc)))
                    page.goto(BASE+route,wait_until="networkidle")
                    page.evaluate("() => document.fonts.ready.then(() => true)")
                    metrics=page.evaluate("""() => ({width:innerWidth,documentWidth:document.documentElement.scrollWidth,
                      math:Array.from(document.querySelectorAll('math')).map(x=>({ns:x.namespaceURI,w:x.getBoundingClientRect().width,h:x.getBoundingClientRect().height})),
                      images:Array.from(document.images).map(x=>({src:x.getAttribute('src'),ok:x.complete&&x.naturalWidth>0}))})""")
                    local=[]
                    if metrics["documentWidth"]>metrics["width"]+1:local.append(f"horizontal overflow {metrics['documentWidth']} > {metrics['width']}")
                    for i,m in enumerate(metrics["math"]):
                        if m["ns"]!="http://www.w3.org/1998/Math/MathML":local.append(f"MathML {i+1} wrong namespace {m['ns']}")
                        if m["w"]<=0 or m["h"]<=0:local.append(f"MathML {i+1} has zero geometry")
                    for im in metrics["images"]:
                        if not im["ok"]:local.append("image failed: "+str(im["src"]))
                    local.extend("page error: "+e for e in errors)
                    report["viewports"].append({"page":slug,"viewport":label,"width":width,"mathml_count":len(metrics["math"]),"image_count":len(metrics["images"]),"errors":local})
                    report["errors"].extend(f"{slug} {label}: {e}" for e in local)
                    if label in ("desktop","mobile"):page.screenshot(path=str(out/f"{slug}-{label}.png"),full_page=True,animations="disabled")
                    page.close()
            checks=[
              ("01-vectors","/content/01-vectors/index.html","input[name=a]","1.5","[data-output=combo]","3.50"),
              ("02-transformations","/content/02-linear-transformations/index.html","input[name=shear]","1.0","[data-output=matrix]","1.00"),
              ("03-systems","/content/03-linear-systems/index.html","[data-step-next]",None,"[data-step-count]","2 / 3"),
              ("04-spaces","/content/04-vector-spaces/index.html","input[name=dependent]",None,"[data-output=rank]","rank = 1"),
              ("05-determinants","/content/05-determinants/index.html","input[name=scale]","-1.0","[data-output=det]","-1.00"),
              ("06-eigenvalues","/content/06-eigenvalues/index.html","input[name=lambda]","2.0","[data-output=eigen]","2.0 v"),
              ("07-least-squares","/content/07-least-squares/index.html","input[name=c]","0.5","[data-output=projection]","0.50"),
              ("08-svd","/content/08-svd/index.html","input[name=sigma]","0.25","[data-output=svd]","0.25"),
              ("09-lu","/content/09-lu-decomposition/index.html","input[name=b1]","6","[data-output=lu-result]","1.75"),
              ("10-qr","/content/10-qr-decomposition/index.html","input[name=b1]","3","[data-output=qr-result]","2.333"),
              ("11-orthogonal","/content/11-orthogonal-matrices/index.html","input[name=angle]","60","[data-output=orth-result]","5.00"),
              ("12-symmetric","/content/12-symmetric-matrices/index.html","input[name=offdiag]","1.5","[data-output=sym-result]","3.5"),
              ("13-positive-definite","/content/13-positive-definite-quadratic-forms/index.html","input[name=cross]","3.5","[data-output=pd-result]","不是正定"),
              ("14-spectral","/content/14-spectral-theorem/index.html","input[name=power]","2","[data-output=spectral-result]","[[5, 4], [4, 5]]"),
              ("15-pca","/content/15-principal-component-analysis/index.html","input[name=components]","2","[data-output=pca-result]","100%"),
              ("16-image-svd","/content/16-image-compression/index.html","input[name=rank]","2","[data-output=image-result]","40.00")]
            for slug,route,control,value,output,expected in checks:
                page=browser.new_page(viewport={"width":1280,"height":900});page.goto(BASE+route,wait_until="networkidle")
                if slug=="11-orthogonal":
                    page.locator(control).evaluate("(el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));}",value)
                    page.locator('input[name=reflect]').check()
                elif slug=="03-systems":page.locator(control).click()
                elif slug=="04-spaces":page.locator(control).check()
                else:page.locator(control).evaluate("(el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));}",value)
                actual=page.locator(output).inner_text();passed=expected in actual
                report["interactions"].append({"page":slug,"expected":expected,"actual":actual,"passed":passed})
                if not passed:report["errors"].append(f"{slug} expected {expected!r}, got {actual!r}")
                page.close()
            page=browser.new_page(viewport={"width":1280,"height":900});page.goto(BASE+"/lab/index.html",wait_until="networkidle");page.locator("#run-lab").click()
            actual=page.locator("#lab-result").inner_text()
            passed=all(x in actual for x in ("LU · partial pivoting","QR · Modified Gram–Schmidt","Cholesky","SVD"))
            report["interactions"].append({"page":"matrix-lab","expected":"LU, QR, Cholesky and SVD report","actual":actual[:500],"passed":passed})
            if not passed:report["errors"].append("matrix lab did not produce all expected report sections")
            page.close();browser.close()
    finally:
        server.terminate();server.wait(timeout=5)
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"viewport_checks":len(report["viewports"]),"interaction_checks":len(report["interactions"]),"errors":report["errors"]},ensure_ascii=False,indent=2))
    return 1 if report["errors"] else 0

if __name__=="__main__":sys.exit(main())
