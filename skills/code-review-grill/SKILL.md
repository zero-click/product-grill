---
name: code-review-grill
description: Perform an independent, read-only review of the current pull-request HEAD against approved requirements, technical design, test contract, and runtime evidence. Use before merge when a reviewer must find correctness, security, architecture, migration, test-integrity, or evidence gaps and return an evidence-backed APPROVED, REQUEST_CHANGES, or BLOCKED verdict.
---

# Code Review Grill

Adapted from ECC's `requesting-code-review` / `code-reviewer.md`. This version is for an already-independent reviewer: do not dispatch another reviewer and do not modify the candidate branch.

## Purpose

Review the implementation at the **current PR HEAD**, not the author's narrative. Determine whether the code is safe to merge against the approved product contract and evidence.

QA PASS proves approved acceptance behavior. It does not replace code review, security review, architecture review, migration review, or test-integrity review.

## Required Inputs

- PR URL, base revision, and current PR HEAD;
- approved product definition, stage plan, and Stage PRD;
- approved technical design;
- approved Stage Test Suite and immutable revision/hash;
- current-head independent QA verdict and evidence;
- repository-defined quality, test, migration, and release configuration.

If the current PR HEAD cannot be verified, canonical inputs are missing, or evidence belongs to another revision, return `BLOCKED`. Do not infer freshness from labels or self-reports.

## Review Boundary

The review is read-only.

- Do not edit production code, tests, specifications, branch state, index, or PR HEAD.
- Inspect with read-only repository and PR commands.
- If another revision must be examined, use a separate temporary checkout/worktree; never move the review checkout's HEAD.
- Use repository-defined commands and the approved Stage Test Suite. Do not invent a parallel quality command surface.
- Run targeted checks when they materially test a finding. Do not rerun Samwell's full acceptance suite merely to imitate independent QA.

## Review Process

### 1. Lock review provenance

Record:

- PR URL;
- base revision;
- reviewed HEAD;
- current remote PR HEAD;
- approved Test Suite revision/hash;
- QA evidence HEAD.

All current-head values must agree before issuing `APPROVED`.

### 2. Read the contract before the diff

Read in authority order:

```text
product.md
→ product-stages.md
→ stage-N-prd.md
→ stage-N-technical-design.md
→ approved stage-N-test-suite.md
```

Build a short review checklist from in-scope Requirement IDs, non-goals, safety boundaries, architecture decisions, migration obligations, and prohibited outcomes.

### 3. Inspect the complete change

Review the complete base-to-current-HEAD diff and relevant surrounding code. Check:

- implementation matches Requirement IDs and user-visible behavior;
- deviations from approved design are explicit and justified;
- responsibilities, dependency direction, Ports/Adapters boundaries, and source-of-truth ownership remain coherent;
- failure, retry, resume, idempotency, concurrency, and blocked behavior are honest;
- authentication, authorization, input validation, secrets, sensitive data, and external side effects respect the approved boundary;
- schema/configuration changes include compatibility, migration, rollback, and operational handling where applicable;
- code is understandable, minimally scoped, and does not retain replaced paths without a justified compatibility requirement.

Do not flag style preferences unless they create a concrete maintenance or correctness risk.

### 4. Review tests and anti-bypass integrity

Check that:

- developer tests cover changed logic and integration boundaries;
- tests verify behavior rather than only mocks or process invocation;
- approved acceptance files and revision/hash were not weakened, skipped, deleted, special-cased, or silently changed;
- production code does not detect fixtures, test IDs, prompts, or known cases to manufacture a pass;
- QA evidence contains real outcome artifacts and belongs to the reviewed HEAD;
- a green label, empty log, or exit code without inspectable evidence is not treated as proof.

If the approved acceptance contract itself appears wrong, classify that separately from an implementation defect. Do not ask the developer to silently change QA-owned tests.

### 5. Validate material findings

Before reporting a blocking finding:

- cite exact `file:line` or artifact/evidence location;
- state the violated Requirement ID, design rule, risk boundary, or test-integrity rule;
- explain the concrete failure mode and impact;
- use a targeted check or code-path trace when practical;
- identify the correct fix owner: implementation, architecture, QA contract, or product decision.

## Severity

- **Critical** — security breach, data loss/corruption, unauthorized/destructive behavior, fabricated success, or core requirement failure. Must fix.
- **Important** — correctness, architecture, migration, reliability, test-integrity, or material requirement gap. Must fix before merge.
- **Minor** — concrete maintainability or documentation issue that does not block safe merge. Advisory unless repository policy says otherwise.

Do not inflate severity. A specific, well-evidenced Important finding is more useful than a vague Critical label.

## Verdict Rules

Return exactly one verdict:

- `APPROVED` — no unresolved Critical or Important findings; provenance and required evidence are current and complete.
- `REQUEST_CHANGES` — at least one validated Critical or Important finding exists.
- `BLOCKED` — a trustworthy review cannot be completed because required inputs, access, current-head provenance, or mandatory evidence are unavailable.

Minor findings alone may accompany `APPROVED`. QA PASS never forces approval.

## Output Format

The human-facing review is part of the review contract, not optional presentation polish.

- Use the stakeholder's established working language; for a Chinese team, headings, conclusions, explanations, impact, and next actions are in Chinese.
- Preserve exact commands, paths, hashes, schema fields, API/class/function names, enums, quoted errors, and machine verdicts such as `APPROVED`, `REQUEST_CHANGES`, and `BLOCKED`.
- The first screen must answer in plain language: **能不能合并、最严重风险是什么、谁下一步做什么**. A one-line verdict, hash dump, matrix, or untranslated review transcript is invalid even when technically correct.
- Explain each technical finding once in human terms, then attach the exact evidence locator. Put detailed matrices and long command output after the decision summary or in linked evidence.
- Do not turn implementation details into a menu for the stakeholder. Recommend the professional correction; ask for a Human decision only when approved product meaning, risk tolerance, or authority is genuinely unsettled.

```markdown
结论：`APPROVED | REQUEST_CHANGES | BLOCKED`。<一句人话说明能否合并以及原因>
最严重风险：<一个最重要的风险；无阻塞项时明确写“未发现阻塞风险”>
下一步：<owner + required action；Human 无需行动时明确说明>

# PR 审查

## 审查上下文
- PR: <URL>
- Base: <revision>
- Reviewed HEAD: <revision>
- Remote PR HEAD: <revision>
- QA Evidence HEAD: <revision>
- Approved Test Contract: <revision/hash>

## 做得好的地方
- <specific evidence-backed strength>

## Findings

### Critical
1. **<title>**
   - 证据：`<file:line or artifact>`
   - 违反合同：`<Requirement ID / design rule / risk boundary>`
   - 实际失败与影响：<what fails and why it matters>
   - 修复 Owner：<implementation | architecture | QA contract | product>
   - 通过条件：<clear condition for resolution>

### Important
<same structure or `None`>

### Minor
<same structure or `None`>

## 合同与测试完整性
- Requirement alignment: PASS | FAIL | BLOCKED
- Architecture alignment: PASS | FAIL | BLOCKED
- Security and risk boundary: PASS | FAIL | BLOCKED
- Migration/compatibility: PASS | FAIL | NOT_APPLICABLE | BLOCKED
- Acceptance-test integrity: PASS | FAIL | BLOCKED
- Current-head evidence: PASS | FAIL | BLOCKED

## Verdict
`APPROVED | REQUEST_CHANGES | BLOCKED`

## 判断依据
<concise evidence-based rationale in the stakeholder's working language>
```

## Anti-Patterns

- Reviewing only the PR description or changed filenames.
- Treating Samwell PASS as proof of code quality.
- Approving a stale HEAD or mismatched QA packet.
- Rewriting code while acting as the independent reviewer.
- Asking Tywin to alter QA-owned acceptance tests without a test-change decision.
- Reporting vague findings without location, violated contract, impact, and fix owner.
- Returning only an English verdict, revision, matrix, or raw transcript when the stakeholder's working language and decision needs are known.
- Blocking on personal taste, speculative scale, or unapproved future requirements.
