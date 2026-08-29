# Agent Skill Coach 设计

## 目标

在 `product-grill` 维护全部可复用的角色 Base Skill、Skill Coach 方法和回归案例。Multica 只保存部署副本和 Agent↔Skill 绑定，不作为 canonical source。

## 核心闭环

```text
Issue / Run / PR / Human feedback
→ Skill Coach 收集直接证据
→ 归因到一个角色和一个 canonical Skill
→ 生成最小 Skill patch
→ failure replay + holdout replay
→ Skill PR
→ Product Owner Human Gate
→ merge 后同步 Multica
→ read-back + SHA-256 验证
```

## 组件

### Canonical Skill repository

当前 `product-grill` 仓库的 `skills/` 是唯一 Skill 源：

- 产品定义：`product-grill`
- 阶段设计：`product-stage-design`
- PRD：`prd-grill`
- 产品合同审查：`product-contract-gate`
- 技术设计：`tech-design-grill`
- QA 验收合同：`stage-acceptance-test-design`
- Test Contract Review：`test-contract-adversarial-review`
- Developer：`design-driven-python-development`
- Code Review：`code-review-grill`
- Skill 改进：`agent-skill-coach`

### Agent Skill Coach

Coach 是独立 Agent。它读取完整 Issue、直接外部状态、Agent 使用的 Skill 版本及 Product Owner 最终决定，只修改 `product-grill` 中一个明确归因的 Skill。它不能修改产品代码、替代产品决策、直接同步 live Skill、合并 PR 或批准自己的改动。

### Base Skill 绑定

| Agent | Base / Workflow Skills |
|---|---|
| Goal OS - Project Lead | `product-grill`, `product-stage-design`, `product-contract-gate`, `goal-os-project-routing-protocol`, `goal-os-spec-driven-flow` |
| Goal OS - PRD Writer | `prd-grill`, `product-contract-gate` |
| Goal OS - Product Reviewer | `product-contract-gate` |
| Varys - Arch | `tech-design-grill` |
| Samwell - QA | `stage-acceptance-test-design` |
| Tywin - Dev | `design-driven-python-development` |
| Brienne - CR | `test-contract-adversarial-review`, `code-review-grill` |
| Skill Coach | `agent-skill-coach` |

Project workflow Skill 仍可存在于 Goal OS 配置中，但专业方法全部从 `product-grill` 同步。

## 改进门槛

Coach 只有在以下证据之一成立时才提出 patch：

- Product Owner 明确给出可复用纠正；
- direct source 推翻 Agent 结论；
- 可复现失败证明 Base Skill 缺少关键 invariant；
- 两个独立 Issue 出现同一模式。

Agent 自评、单次偶发故障、未决产品判断和 Issue 私有事实不能进入 Skill。

## Eval

每个 Coach 输出必须包含：

1. failure replay：原错误在新 Skill 下不再发生；
2. holdout replay：相邻历史案例不退化；
3. attribution check：问题确实属于目标 Skill；
4. scope check：一次只修改一个 Skill；
5. safety check：不削弱 Human Gate、角色分离或直接来源权威。

## 同步协议

```text
canonical SKILL.md
→ validate/package
→ Multica import overwrite 或 update
→ 设置 Agent skill IDs
→ live agent get / skill get
→ exact content + SHA-256 比对
```

同步前更新 Agent instruction snapshot；live update 后必须回读。创建或更新 Skill 不等于 Agent 已采用，只有绑定与回读都通过才算完成。

## 安全边界

- Skill PR 仍需 Product Owner 批准后才能 merge/deploy；
- Coach 不自动修改 live Multica；
- Coach 不自动 merge；
- Coach 不把 Review finding 自动升级成产品或 threat-model 决策；
- 删除 Skill、Agent、branch、worktree 或 stash 需要单独授权。
