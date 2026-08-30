---
name: mode-routing-guide
description: Research mode routing guide for research-topic-compiler
---

# Research Mode Routing Guide

Use this file when `SKILL.md` identifies a mode but the run needs detailed trigger or execution rules.

## Lightweight Concept Lens Mode

### Trigger Signals

- 用户说“概念解读”“概念源流”“概念透镜”“语义演化”“行业演进看板”。
- 用户要 PM 技术评审提问脚本、反模式诊断、概念债务识别或供应商/方案评估问题。
- 用户不需要完整 Obsidian Research Project，但需要带来源的结构化理解和可操作判断。
- 用户要求生成本地 HTML 决策看板、Tailwind + Alpine.js 看板或可验证的概念演进 dashboard。

### Working Rules

- 先追溯概念源流：提出背景、原始问题、原始用户、原始用途、主要语义漂移和当前误用。
- 再归纳范式阶段：从证据中推导 3-6 个阶段，不强套固定四阶段，也不把简单时间线当结构。
- 每个阶段必须写清用户需求、底层矛盾、成熟解法、PM 视角操作逻辑、证据依据和 1-2 个评审问题。
- 输出默认是聊天内 PM 决策看板；只有用户明确要文件或 HTML dashboard 时才生成本地 `dashboard.html`。
- 生成 HTML dashboard 前读取 `concept-lens-output-contract.md`、`concept-lens-html-dashboard-template.md` 和 `concept-lens-design-quality.md`。
- 冷启动或事实敏感主题先读取 `concept-lens-source-and-factuality.md` 并浏览验证；用到历史来源时区分证据和模型推断。
- 生成 HTML 后运行 `python3 scripts/validate_html_artifact.py <path-to-dashboard.html>`，并在可用时做浏览器视觉检查。

## General Research Dashboard Output

This is an output artifact route for `Normal Research` and `Application`, not a new research mode.

### Trigger Signals

- 用户明确要求一般专题研究或应用研究的 HTML、网页看板、可视化研究报告。
- 研究结果需要同时服务领导、产品、研发、设计或运营，并把结论、证据、置信度和行动放在同一个扫描面。
- 用户已有带来源的 Markdown/Research Project，要求转换为 Dashboard；若现有证据已覆盖目标，不要为了转换格式重新扩源。

### Working Rules

- 选择 `research-dashboard-html`，读取 `research-dashboard-output-contract.md`。
- Normal Research/Application 先完成适用的迭代循环，并通过 `research-dashboard-output-contract.md` 的 renderable research state 门禁；唯一终态本身不够。不要让页面生成替代 FRAME、Evidence、Framework Change 或 saturation gate。
- 保留引用、置信度、矛盾、residual Gaps、residual risks 和终态；压缩展示不能把弱证据升级为确定结论。
- 输出 `dashboard.html` 与 `summary.md`，运行 `python3 scripts/validate_html_artifact.py <path-to-dashboard.html>`，并做桌面/移动端浏览器检查。
- 普通聊天、Markdown-only、L1/L2 快答和 UI mockup 请求不自动生成 HTML。用户要求最终选一个时仍转交 `decision-research`。

## Learning Report HTML Output

This is the reader-facing artifact route for a Learning Pack or a single-reader Normal Research/Application run. It is not a new research mode.

### Trigger Signals

- 用户说“让我系统学会”“逐步理解”“深入解释”“不要蜻蜓点水”“观点要鲜明”。
- 用户要把行业/技术演进讲清楚，再对比自己的现状，最后落到可执行改进。
- 用户要 `learning report HTML`、学习型 HTML、长文式报告或可连续阅读的研究产物，而不是研究过程看板。

### Working Rules

- 选择 `learning-report-html`，读取 `editorial-projection-gate.md` 与 `learning-report-output-contract.md`。
- 先完成适用的 Research Framework 和终态门禁，再执行 Editorial Projection Gate；不得让 HTML 写作替代研究循环。
- 以一个主要读者为中心，按“论点 -> 机制 -> 对照 -> 边界 -> 当前状态 -> 行动”编译连续叙事；具体顺序由 Framework Vn 决定。
- 证据默认放脚注、文末或折叠审计附录；影响结论的反例和不确定性留在正文。
- 用一张精确比较表和 1-3 个有语义的视觉关系帮助理解；不要把每节做成卡片或展示研究状态。
- 生成 `report.html` 与 `summary.md`，运行 `python3 scripts/validate_html_artifact.py <path-to-report.html>`，并完成桌面/平板/390x844 检查。
- UI-only 请求继续交给 `frontend-design`；多角色扫描和证据审计继续使用 `research-dashboard-html`。

## Learning Pack Mode

### Trigger Signals

- 用户说“陌生领域”“系统学习”“学习路线”“教程式理解”。
- 用户说“不要只给证据卡片”“不要太表面”。
- 用户说“像 Agent-Learning-Hub，但轻一点”。
- 用户希望建立一个主题的长期认知框架。

### Working Rules

Learning Pack 默认写进 `05_研究报告`、`03_阶段结论`、`07_行业案例对照` 和 `08_最佳实践与应用模板`。

不要默认新增 `10-12` 文件。只有满足任一条件时，才建议新增：

- 用户明确要求独立学习包。
- 主题复杂度达到 `L4/L5` 且内容过长。
- 研究项目要复用给他人学习。
- `05_研究报告` 过长影响阅读。

可新增文件：

- `10_学习路线.md`
- `11_概念地图.md`
- `12_实践任务.md`

## Application Mode

### Trigger Signals

- 用户问“对我有什么用”“对我们业务有什么用”。
- 用户问“怎么落地”“怎么做成方案 / PRD / Workflow / Skill / Eval”。
- 用户需要把研究结论变成具体工作产物。

### High-Stakes Applied Business Research

When the research will inform product strategy, commercialization, packaging, go-to-market, workflow/platform design, enterprise adoption, implementation, or other high-cost decisions, treat Application Mode as a decision-support run rather than a generic summary.

- Read `applied-business-research-contract.md`.
- Default to `L4`.
- Required outputs: decision context, evidence coverage, transfer reasoning, judgment matrix, staged recommendation, risks, and open validations.

### Required Outputs

至少转成一种：

- 判断：是否值得做、边界在哪里、风险是什么、何时不适合。
- 方案：模块拆解、路线图、资源投入、关键取舍。
- 模板：PRD 片段、Workflow 表、Eval 指标、接口草案、SOP、风险矩阵。
- 任务：最小实践、验证动作、下一步调研、团队分工。

## Product Candidate Research

Use `product-decision-mode.md` for the detailed candidate backlog workflow.

### Trigger Signals

- 用户说“帮我做竞品分析”“先找一批候选方案”“建立候选池”“后续继续补”。
- 用户说“这个方向值不值得做”“市场上有没有类似的”“我该怎么定位”。
- 用户描述的是一个需要在多个候选项之间做决定的场景，但当前目标是先形成候选池。
- 用户目标是形成 PRD 输入、技术选型报告、Go/No-Go 决策输入或产品路线图输入。
- 调研后的预期产物是 Candidate Backlog 和 handoff，而非单一最终结论。

### Ownership Rule

This mode may output Top candidates or a ranked candidate table. Treat those outputs as decision inputs.

If the user asks for “选一个”“给我最终推荐”“为什么排除其他方案”“基于这个 Candidate Backlog 下结论”， hand off to `decision-research`.

## Radar Mode

Radar Mode details live in `research-radar-loop-contract.md`.

Do not create Codex automations unless the user explicitly asks to create, schedule, or enable one.
