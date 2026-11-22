(() => {
  "use strict";
  const byId = (id) => document.getElementById(id);
  const valueOf = (root, name, fallback) => {
    const node = root.querySelector('[name="' + name + '"]');
    return node ? Number(node.value) : fallback;
  };
  const setText = (root, selector, value) => {
    const node = root.querySelector(selector);
    if (node) node.textContent = value;
  };
  const setLine = (node, x1, y1, x2, y2) => {
    if (!node) return;
    node.setAttribute("x1", x1); node.setAttribute("y1", y1);
    node.setAttribute("x2", x2); node.setAttribute("y2", y2);
  };

  document.querySelectorAll("[data-demo]").forEach((root) => {
    const kind = root.dataset.demo;
    const update = () => {
      if (kind === "linear-combination") {
        const a = valueOf(root, "a", 1), b = valueOf(root, "b", 1);
        const x = 180 + 38 * (a + 2 * b), y = 165 - 38 * (2 * a + b);
        setLine(root.querySelector("#combo-result"), 180, 165, x, y);
        const point = root.querySelector("#combo-point");
        if (point) { point.setAttribute("cx", x); point.setAttribute("cy", y); }
        setText(root, "[data-output=combo]", "(" + (a + 2*b).toFixed(2) + ", " + (2*a + b).toFixed(2) + ")");
        setText(root, "[data-output=coeff]", a.toFixed(1) + "u + " + b.toFixed(1) + "v");
      }
      if (kind === "matrix") {
        const s = valueOf(root, "shear", .5);
        const grid = root.querySelector("#matrix-grid");
        if (grid) grid.setAttribute("transform", "matrix(1 0 " + (-s).toFixed(3) + " 1 0 0)");
        setText(root, "[data-output=matrix]", "A = [[1, " + s.toFixed(2) + "], [0, 1]]");
        setText(root, "[data-output=det]", "det(A) = 1");
      }
      if (kind === "determinant") {
        const s = valueOf(root, "scale", 1);
        const poly = root.querySelector("#det-shape");
        if (poly) {
          const x0=185,y0=165,dx=68*s,dy=64;
          poly.setAttribute("points", x0+","+y0+" "+(x0+dx)+","+y0+" "+(x0+dx)+","+(y0-dy)+" "+x0+","+(y0-dy));
        }
        setText(root, "[data-output=det]", "det(A) = " + s.toFixed(2) + "；有向面积 = " + s.toFixed(2));
      }
      if (kind === "eigen") {
        const lambda = valueOf(root, "lambda", 3);
        const endX = 170 + 38 * lambda, endY = 155 - 38 * lambda;
        setLine(root.querySelector("#eigen-after"), 170, 155, endX, endY);
        setText(root, "[data-output=eigen]", "A v = " + lambda.toFixed(1) + " v（方向保持不变）");
      }
      if (kind === "projection") {
        const c = valueOf(root, "c", 1);
        const x = 90 + c * 80, y = 210 - c * 80;
        setLine(root.querySelector("#projection-vector"), 90, 210, x, y);
        setLine(root.querySelector("#projection-residual"), x, y, 250, 210);
        setText(root, "[data-output=projection]", "投影系数 c = " + c.toFixed(2));
      }
      if (kind === "svd") {
        const sigma = valueOf(root, "sigma", 1);
        const ellipse = root.querySelector("#svd-ellipse");
        if (ellipse) ellipse.setAttribute("ry", (54 * sigma).toFixed(1));
        setText(root, "[data-output=svd]", "σ₁ = 3，σ₂ = " + sigma.toFixed(2));
      }
      if (kind === "rank") {
        const dependent = root.querySelector('[name="dependent"]');
        const isDependent = dependent ? dependent.checked : false;
        const second = root.querySelector("#rank-second");
        if (second) second.setAttribute("d", isDependent ? "M170 155L260 85" : "M170 155L95 85");
        setText(root, "[data-output=rank]", isDependent ? "相关：张成空间是一条直线，rank = 1" : "无关：张成空间是整个平面，rank = 2");
      }
      if (kind === "lu") {
        const b1 = valueOf(root, "b1", 5);
        const x1 = (3*b1 - 11) / 4, x2 = (b1 - 3) / 2, x3 = 7 - b1;
        setText(root, "[data-output=b1]", String(b1));
        setText(root, "[data-output=lu-result]", "x = (" + [x1,x2,x3].map(v=>v.toFixed(2)).join(", ") + ")");
        setText(root, "[data-output=lu-steps]", "固定 L、U；前代 y = (" + [b1,-2-2*b1,7-b1].map(v=>v.toFixed(2)).join(", ") + ")，再回代");
      }
      if (kind === "qr") {
        const b1 = valueOf(root, "b1", 1);
        const x2 = (b1 - 2) / 3, x1 = (b1 + 2 - x2) / 2;
        setText(root, "[data-output=qr-b1]", String(b1));
        setText(root, "[data-output=qr-result]", "x = (" + x1.toFixed(3) + ", " + x2.toFixed(3) + ")");
        setText(root, "[data-output=qr-check]", "Aᵀr = (0, 0)；残差与列空间正交");
      }
      if (kind === "orthogonal") {
        const angle = valueOf(root, "angle", 30);
        const reflect = !!root.querySelector('[name="reflect"]')?.checked;
        const rad = angle * Math.PI / 180;
        const x = 90 * Math.cos(rad), y = 90 * Math.sin(rad) * (reflect ? -1 : 1);
        const line = root.querySelector("#orthogonal-vector");
        if (line) { line.setAttribute("x2", 180+x); line.setAttribute("y2", 160-y); }
        setText(root, "[data-output=angle]", angle + "°");
        setText(root, "[data-output=orth-result]", "‖Qv‖ = 5.00；det(Q) = " + (reflect ? "−1" : "+1"));
      }
      if (kind === "symmetric") {
        const c = valueOf(root, "offdiag", 1);
        setText(root, "[data-output=sym-c]", c.toFixed(1));
        setText(root, "[data-output=sym-result]", "λ₁ = " + (2+c).toFixed(1) + "，λ₂ = " + (2-c).toFixed(1) + "；特征方向仍正交");
      }
      if (kind === "positive-definite") {
        const c = valueOf(root, "cross", 2);
        const det = 12 - c*c;
        setText(root, "[data-output=pd-c]", c.toFixed(2));
        setText(root, "[data-output=pd-result]", "det(A) = " + det.toFixed(2) + "；" + (det > 1e-9 ? "正定" : (Math.abs(det) <= 1e-9 ? "半正定边界" : "不是正定（不定）")));
      }
      if (kind === "spectral") {
        const n = valueOf(root, "power", 2);
        const p = Math.pow(3,n), a = (p+1)/2, b = (p-1)/2;
        setText(root, "[data-output=power]", String(n));
        setText(root, "[data-output=spectral-result]", "A" + (n===2?"²":"^"+n) + " = [[" + a + ", " + b + "], [" + b + ", " + a + "]]");
      }
      if (kind === "pca") {
        const k = valueOf(root, "components", 1);
        setText(root, "[data-output=pca-k]", String(k));
        setText(root, "[data-output=pca-result]", "解释方差 " + (k===1?"80%":"100%") + "；平方重建误差 " + (k===1?"2.00":"0.00"));
      }
      if (kind === "image-svd") {
        const rank = valueOf(root, "rank", 1);
        const parity = (n) => { let p=0; while(n){p^=1;n&=n-1;} return p ? -1 : 1; };
        root.querySelectorAll("[data-pixel]").forEach(cell => {
          const r=Number(cell.dataset.r), c=Number(cell.dataset.c);
          let value=148;
          if(rank>=2) value += 10*parity(r&1)*parity(c&1);
          if(rank>=3) value += 5*parity(r&2)*parity(c&2);
          const g=Math.max(0,Math.min(255,Math.round(value)));
          cell.setAttribute("fill", "rgb("+g+","+g+","+g+")");
        });
        const error = rank===1 ? Math.sqrt(80*80+40*40) : (rank===2 ? 40 : 0);
        const storage = (17*rank/64*100).toFixed(1);
        setText(root, "[data-output=image-rank]", String(rank));
        setText(root, "[data-output=image-result]", "Frobenius 误差 " + error.toFixed(2) + "；存储 " + storage + "%");
      }
    };
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", update));
    update();
  });

  document.querySelectorAll("[data-stepper]").forEach((root) => {
    const panels = Array.from(root.querySelectorAll("[data-step]"));
    let current = 0;
    const render = () => {
      panels.forEach((panel, i) => { panel.hidden = i !== current; });
      setText(root, "[data-step-count]", "步骤 " + (current + 1) + " / " + panels.length);
      const prev = root.querySelector("[data-step-prev]");
      const next = root.querySelector("[data-step-next]");
      if (prev) prev.disabled = current === 0;
      if (next) next.disabled = current === panels.length - 1;
    };
    root.querySelector("[data-step-prev]")?.addEventListener("click", () => { current = Math.max(0, current - 1); render(); });
    root.querySelector("[data-step-next]")?.addEventListener("click", () => { current = Math.min(panels.length - 1, current + 1); render(); });
    render();
  });
})();
