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
        const x = 90 + c * 210, y = 210 - c * 105;
        setLine(root.querySelector("#projection-vector"), 90, 210, x, y);
        setLine(root.querySelector("#projection-residual"), x, y, 250, 45);
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
        if (second) second.setAttribute("transform", isDependent ? "translate(0 0) scale(2 2)" : "rotate(-35 170 155)");
        setText(root, "[data-output=rank]", isDependent ? "相关：张成空间是一条直线，rank = 1" : "无关：张成空间是整个平面，rank = 2");
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
