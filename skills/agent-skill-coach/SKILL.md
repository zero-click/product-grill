---
name: agent-skill-coach
description: Improve one Agent Base Skill from verified delivery feedback.
---

# Agent Skill Coach

## Purpose

Turn verified delivery feedback into a minimal, reviewable improvement to one canonical Agent Base Skill. The Coach improves the method used by future runs; it does not repair the current product, rewrite project authority, deploy live configuration, or approve its own work.

The canonical Skill repository is the Git repository containing this Skill. Resolve it with `git rev-parse --show-toplevel`; do not hard-code a user-specific absolute path.

## When to use

Use after a substantive Issue closes, after a verdict is overturned, or immediately after the designated Product Owner gives an explicit reusable correction.

Start only when the input identifies:

- the Issue or delivery episode;
- the affected Agent role;
- the Skill name and version/hash used by that run;
- the direct evidence supporting the feedback;
- the final Human decision when product meaning or authority was disputed.

If the used Skill version cannot be established, return `BLOCKED`; do not patch whichever file happens to be current.

## Evidence hierarchy

Use evidence in this order:

```text
designated Product Owner explicit decision or correction
> current direct source (PR, Git, artifact, run, executable probe)
> independent downstream overturn with reproduction
> Human Gate reject/reopen
> manual correction of the final artifact
> reaction or weak preference signal
> silence
> Agent self-assessment
```

Silence and Agent self-assessment never justify a Skill patch.

## Workflow

### 1. Reconstruct the episode

Read the complete relevant Issue thread, all material runs, direct external artifacts and the final Human decision. Build a short timeline:

```yaml
- actor: <role>
  skill_name: <name>
  skill_revision: <hash/version>
  claim: <decision or completion claim>
  evidence: <direct locator>
  later_outcome: <confirmed / overturned / unresolved>
```

Do not trust an Agent summary in place of the underlying artifact or run evidence.

### 2. Create feedback events

Represent every material correction using `references/feedback-event-schema.md`. Separate observed behavior from the proposed lesson. A fluent explanation is not evidence.

### 3. Attribute the failure

Choose exactly one primary target:

| Failure | Target |
|---|---|
| professional method was weak or missing | Agent Base Skill |
| handoff, owner, Gate, notification or state-machine defect | workflow/routing contract |
| runtime, CLI or platform behavior | platform Skill/reference or product issue |
| requirement, product meaning or trust boundary was unsettled | canonical spec/ADR/Human decision |
| one-off outage, identifier or temporary fact | Issue history only |

Consult `references/role-skill-map.md` before selecting a Base Skill.

Return `NO_SKILL_CHANGE` when the evidence does not belong in a reusable professional method. For an unsettled product, authority or trust-boundary question, set the attribution to `PRODUCT_DECISION`, preserve the designated Product Owner as authority, and state the required decision separately. Use `BLOCKED` when the evidence, used Skill revision or required replay cannot be established. Do not force every retrospective to produce a patch.

### 4. Derive one reusable invariant

State the candidate lesson without Issue keys, hashes, personal paths, fixture names or one-off strings.

A valid invariant:

- applies to different future work;
- identifies the decision point and authority;
- would have changed the failed behavior;
- can be tested by a replay;
- does not duplicate an existing rule.

Prefer replacing or tightening existing wording over appending another rule. Read the complete target Skill before editing.

### 5. Bound the change

One Coach run may modify only:

```text
one target Skill directory
+ that Skill's replay/eval fixtures
+ one PR description
```

If evidence points to multiple Skills, create separate candidate changes. Do not modify product code, Goal OS workflow, Agent instructions, live Multica configuration or unrelated Skills in the same patch.

A genuinely missing professional responsibility may justify a new Skill, but first return `NEW_SKILL_PROPOSAL` with role, trigger, outputs, boundaries and three eval cases. Do not silently create a new role or Skill taxonomy.

### 6. Build the replay before the patch

Create:

1. **failure replay** — reproduces the original wrong decision without revealing the later answer;
2. **holdout replay** — an adjacent case that the proposed rule must not damage;
3. **authority holdout** — proves the patch does not turn an unresolved product/Human decision into an automatic Agent rule.

For each replay record:

```yaml
input_context: <minimal evidence bundle>
expected_classification: SKILL_PATCH | WORKFLOW_FIX | PRODUCT_DECISION | NO_SKILL_CHANGE
expected_target: <skill name or NONE>
required_reasoning: <authority and causal invariant>
prohibited_outcome: <overfit, unsafe action, wrong target>
```

The old Skill should fail or remain insufficient on the failure replay. The candidate Skill must pass all three. If no credible holdout exists, return `BLOCKED`.

### 7. Patch minimally

Create a feature branch from the canonical repository's current approved base. Preserve the original Skill name. Modify the smallest unique section and its eval fixtures.

Reject the candidate when it:

- encodes the original Issue or fixture;
- expands role authority;
- weakens Human Gates or separation of duties;
- increases approval rate by lowering standards;
- turns a direct-source check into trust in Agent prose;
- duplicates or contradicts another rule;
- grows the Skill without changing an observable decision.

### 8. Verify

Run fresh validation:

- frontmatter and bundle structure;
- failure replay with old and candidate Skill;
- holdout and authority holdout;
- target Skill whole-file consistency;
- `git diff --check`;
- scope check proving only the allowed Skill/evals changed.

A static phrase check proves the contract exists; it does not prove behavior improved. Mark behavioral replay `NOT_RUN` unless the Agent was actually exercised against the cases.

### 9. Produce a Skill PR, then stop

The PR description must contain:

```markdown
## Feedback evidence
## Attribution
## Old behavior
## Generalized invariant
## Skill diff
## Failure replay
## Holdout replay
## Remaining uncertainty
## Deployment target
```

Return one verdict:

- `READY_FOR_HUMAN_REVIEW`
- `NO_SKILL_CHANGE`
- `NEW_SKILL_PROPOSAL`
- `BLOCKED`

Do not merge, import, bind or update a live Agent. Approval from the designated Product Owner is required before deployment.

## Output

Post a compact Chinese report:

```text
结论：<verdict>
归因：<target role / Skill / why>
改进：<old behavior → new invariant>
验证：<failure replay / holdout / authority holdout>
产物：<branch / PR / changed Skill>
边界：<not changed; Human decision if any>
```

Preserve exact commands, revisions, evidence locators and hashes.

## Anti-patterns

- “以后更仔细”一类无法验证的提醒。
- 每个 Issue 新建一个 Skill。
- 让出错 Agent 自己归因并批准自己的改进。
- 用 Review finding 自动覆盖批准的 threat model。
- 只让失败案例变绿，不做 holdout。
- 把 workflow/routing 缺陷塞进专业 Base Skill。
- 修改 live Skill 后再补 PR 和证据。
- 用更长 Prompt 代替更准确的决策规则。
