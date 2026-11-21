# Linear Algebra · 线性代数可视化课程

一个从几何直觉走向严谨数学的中文线性代数学习站。课程采用渐进式图解、可交互实验、完整推导与可复核例题，让每个矩阵公式都能对应到空间中的真实变化。

**在线阅读：** https://1998x-stack.github.io/Linear-Algebra/

## 学习路线

| 模块 | 主题 | 关键问题 |
|---|---|---|
| [01 向量与线性组合](content/01-vectors/) | 向量、线性组合、张成、基 | 哪些点可以由给定向量组合得到？ |
| [02 矩阵与线性变换](content/02-linear-transformations/) | 矩阵、基向量、复合变换 | 矩阵如何改变整个空间？ |
| [03 线性方程组与高斯消元](content/03-linear-systems/) | 消元、主元、解的结构 | 方程组为什么可能有唯一解、无解或无穷多解？ |
| [04 向量空间、秩与维数](content/04-vector-spaces/) | 子空间、线性无关、基、四个基本子空间 | 一个矩阵揭示了哪些空间关系？ |
| [05 行列式与体积](content/05-determinants/) | 面积缩放、方向、可逆性 | 行列式为什么能检测信息是否被压扁？ |
| [06 特征值与特征向量](content/06-eigenvalues/) | 不变方向、特征多项式、对角化 | 哪些方向在变换下保持不变？ |
| [07 正交投影与最小二乘](content/07-least-squares/) | 内积、投影、Gram–Schmidt、最小二乘 | 如何找到离数据最近的可行解？ |
| [08 奇异值分解与低秩近似](content/08-svd/) | SVD、奇异值、压缩、PCA 联系 | 如何把任意线性变换拆成旋转与伸缩？ |

## 如何学习

1. 先阅读每篇开头的问题，不急着背公式。
2. 观察图示，确认箭头、坐标、矩阵列和空间对象之间的对应关系。
3. 操作交互实验，预测结果后再改变参数。
4. 跟随逐步推导，检查每一步的条件和维度。
5. 完成例题与自测；用反例检查自己是否理解了适用边界。
6. 按页面底部的先修链接继续学习。

## 内容工程原则

- **数学正确性优先。** 每个公式都解释符号、维度、前提和结论；教学例子与一般定理明确区分。
- **图形不是装饰。** 每幅 SVG 都有标题、描述、图注和可检查的数学含义。
- **交互是渐进增强。** 没有 JavaScript 时，静态图、公式和结论仍然完整。
- **公式采用 MathML。** 不用 Unicode 拼凑分式、矩阵或上下标；公式有无障碍描述，并为窄屏提供横向滚动区域。
- **结论交叉验证。** 关键结果同时用代数计算、几何解释或数值代入检查。
- **引用可追溯。** 课程结构参考 MIT 18.06，基础概念参考 Hefferon 教材；视觉教学方法参考 3Blue1Brown 的线性代数专题。所有文章、推导和插图独立编写，不复制原作内容或素材。

## 仓库结构

```text
.
├── index.html                 # 课程首页与知识导航
├── README.md
├── AGENTS.md                  # 内容生产、数学审校和发布约束
├── assets/
│   ├── css/site.css           # 全站响应式设计系统
│   ├── js/site.js             # 无依赖交互增强
│   └── diagrams/              # 独立 SVG 图示
├── content/
│   ├── 01-vectors/index.html
│   ├── 02-linear-transformations/index.html
│   ├── 03-linear-systems/index.html
│   ├── 04-vector-spaces/index.html
│   ├── 05-determinants/index.html
│   ├── 06-eigenvalues/index.html
│   ├── 07-least-squares/index.html
│   └── 08-svd/index.html
├── references/reading-map.md  # 内容与权威课程/教材对应关系
├── scripts/validate_site.py  # 页面、公式、图示和链接静态校验
├── tests/test_site.py        # 课程结构回归测试
└── .github/workflows/pages.yml
```

## 本地预览与验证

页面为静态 HTML，不需要 Node、构建框架或 CDN：

```bash
python3 -m http.server 8000
# 浏览 http://localhost:8000

python3 scripts/validate_site.py
python3 -m unittest discover -s tests -v
python3 -m pip install -r requirements-dev.txt
python3 -m playwright install chromium
python3 scripts/browser_smoke.py
```

建议在 Chromium、Firefox、Safari 中检查数学排版；至少检查 1440px、768px、390px 和 360px 视口。CI 还会用 Playwright/Chromium 检查桌面、390px/360px 手机视口、MathML 命名空间与几何、图片加载和八个交互控件，并保存截图报告。该自动化检查不等同于人工审阅所有浏览器的视觉细节。

## 参考资料

1. Gilbert Strang, MIT OpenCourseWare, [18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/). 课程覆盖消元、四个基本子空间、正交投影、行列式和特征值等主题。
2. Jim Hefferon, [Linear Algebra](https://hefferon.net/linearalgebra/). 免费本科教材，包含线性方程组、向量空间、线性映射、行列式和特征值。
3. 3Blue1Brown, [Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra). 作为视觉教学方法参考；本项目独立绘制图形并独立撰写讲解。
4. Kenji Hiranabe, [The Art of Linear Algebra](https://github.com/kenjihiranabe/The-Art-of-Linear-Algebra). 以矩阵分解为主线的图解参考。\n5. Fabio Furini, [Linear Algebra lecture notes and computation lab](https://fabiofurini.github.io/linear-algebra/). 逐步计算与精确算术交互实验参考。\n6. NIST Digital Library of Mathematical Functions, [About MathML](https://dlmf.nist.gov/help/mathml). MathML 与浏览器数学呈现说明。

## 发布

GitHub Actions 在推送到 `main` 后运行结构验证并发布 GitHub Pages。部署工作流使用 `actions/configure-pages`、`actions/upload-pages-artifact` 和 `actions/deploy-pages`。只有在远端部署运行成功并检查页面 URL 后，才将网站标记为已发布。
