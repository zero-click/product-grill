# Product Grill

Product Grill is a small Codex/agent skill pack for turning vague product ideas into implementation-ready work. It keeps product definition, stage planning, PRD writing, technical design, acceptance testing, and code review as separate, reviewable steps.

## Skills

- `product-grill`: clarify a product idea and produce `product.md`.
- `product-stage-design`: plan product stages and produce `product-stages.md`.
- `prd-grill`: define one stage's product requirements and produce `stage-{n}-prd.md`.
- `tech-design-grill`: convert an approved PRD into `stage-{n}-tech-design.md`.
- `stage-acceptance-test-design`: define independent acceptance criteria and black-box tests.
- `test-contract-adversarial-review`: independently review QA claims, executable tests, and whole-contract consistency before the human test-suite gate.
- `design-driven-python-development`: implement approved Python designs with modular boundaries, developer-owned TDD, and immutable acceptance tests.
- `code-review-grill`: review a PR against approved requirements, design, tests, and evidence.
- `product-contract-gate`: preserve product decisions and independently review Product/Stage/PRD contract evidence.
- `agent-skill-coach`: turn verified delivery feedback into a replay-tested candidate improvement to one Base Skill.

Goal OS workflow/runtime Skills are also canonical here:

- `goal-os-spec-driven-flow`: stage ownership, evidence order, Human Gates, and rerouting.
- `goal-os-project-routing-protocol`: Multica dispatch, callback, handoff, and notification transport.
- `goal-os-codex-command-surface`: runtime command discovery by delivery stage.
- `goal-os-test-suite-grill`: deprecated migration marker; use the current QA and review Skills instead.

## Workflow

```text
product.md
-> product-stages.md
-> stage-{n}-prd.md
-> stage-{n}-tech-design.md
-> acceptance test contract
-> independent test-contract review
-> human test-suite gate
-> design-driven Python implementation
-> independent code review
```

## Usage

Copy or install the `skills/` directory into an agent environment that supports Codex-style skills. Then call the relevant skill by name, for example:

```text
Use product-grill to help me define this product idea.
Use prd-grill to draft the Stage 1 PRD.
Use code-review-grill to review this PR.
```

Each skill supports an interactive mode and a headless draft mode when you ask for a complete document first.

---

# Product Grill（中文）

Product Grill 是一个轻量的 Codex/Agent 技能包，用来把模糊的产品想法推进到可实现、可验收、可审查的工作项。它把产品定义、阶段规划、PRD、技术设计、验收测试和代码审查拆成独立步骤，减少隐含假设。

## 技能

- `product-grill`：澄清产品想法，生成 `product.md`。
- `product-stage-design`：规划产品阶段，生成 `product-stages.md`。
- `prd-grill`：定义单个阶段的产品需求，生成 `stage-{n}-prd.md`。
- `tech-design-grill`：把已批准的 PRD 转成技术设计，生成 `stage-{n}-tech-design.md`。
- `stage-acceptance-test-design`：设计独立验收标准和黑盒验收测试。
- `test-contract-adversarial-review`：在人工 Test Suite Gate 前独立审查 QA Claim、可执行测试和完整合同的一致性。
- `design-driven-python-development`：按批准的技术设计，以模块化边界和 Developer TDD 实现 Python 代码，不改写 QA 验收测试。
- `code-review-grill`：基于需求、设计、测试和证据审查 PR。
- `product-contract-gate`：保留产品决定并独立审查 Product/Stage/PRD 合同证据。
- `agent-skill-coach`：把已验证的交付反馈转成一个 Base Skill 的 replay-tested 候选改进。

Goal OS 的 workflow/runtime Skill 也以本仓库为 canonical source：

- `goal-os-spec-driven-flow`：阶段 Owner、证据顺序、Human Gate 和回退路径。
- `goal-os-project-routing-protocol`：Multica 派单、回调、交接与通知协议。
- `goal-os-codex-command-surface`：按交付阶段核验 runtime command surface。
- `goal-os-test-suite-grill`：只保留为迁移标记；新流程使用当前 QA 与 Review Skill。

## 流程

```text
product.md
-> product-stages.md
-> stage-{n}-prd.md
-> stage-{n}-tech-design.md
-> 验收测试契约
-> 独立 Test Contract Review
-> 人工 Test Suite Gate
-> Design-driven Python 实现
-> 独立代码审查
```

## 使用

将 `skills/` 目录复制或安装到支持 Codex 风格 skills 的 agent 环境中，然后按名称调用需要的技能，例如：

```text
Use product-grill to help me define this product idea.
Use prd-grill to draft the Stage 1 PRD.
Use code-review-grill to review this PR.
```

每个技能都支持交互模式；如果你要求先生成完整草稿，也支持 headless draft 模式。
