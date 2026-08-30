---
name: tech-design-grill
description: Convert an approved stage PRD into an implementable technical design. Supports interactive grilling one question at a time and headless draft generation when the user wants a complete stage-{n}-tech-design.md produced first for later review. Use after PRD approval and before implementation planning or coding. Inspect the existing codebase when present or establish greenfield mode.
---

# Background

Technical design defines **how** to implement an approved product contract without silently changing **what** the product must do.

Ground decisions in:

1. `product.md → product-stages.md → stage-{n}-prd.md`;
2. the current canonical technical design and accepted ADRs, when revising an existing design;
3. the current code and tests, or an explicit greenfield baseline.

Treat replaced designs as migration context, not as the source of truth.

Technical Design is a durable architecture and decision document, not an Issue, PR, incident, review-finding, or Gate history. Treat delivery artifacts as evidence to reconcile against design authority, not as authority by themselves.

# Inputs

Required:

- settled `product.md`
- settled `product-stages.md`
- approved `stage-{n}-prd.md`
- project mode: existing system or greenfield
- current canonical technical design and relevant accepted ADRs, when revising an existing design
- current codebase and runtime/configuration files, when they exist

If a product document is missing or unapproved, return to the appropriate product skill. If an existing codebase is inaccessible, state the limitation rather than inventing architecture.

# Process

Before asking design questions:

1. Read the canonical product documents.
2. When revising an existing design, read the complete current canonical technical design and all relevant accepted ADRs before editing. Reconcile each proposed change as accepted, proposed, contradicted, or obsolete; do not infer ADR acceptance from implementation, review, or Gate status.
3. Inventory stable PRD requirement IDs.
4. Inspect relevant code, contracts, persistence, configuration, and tests; in greenfield mode, record that no current implementation exists.
5. Identify legacy designs and compatibility constraints.

Integrate accepted, durable changes into the existing authoritative sections for architecture, responsibilities, contracts, data, state, security, migration, and testing. Update or remove contradictions across the whole document instead of appending a chronological problem list. If implementation evidence conflicts with the canonical design or an accepted ADR, preserve the accepted decision and put the unresolved proposal in `Human Review Required` with its impact and required authority.

Then resolve this decision tree:

- current and target architecture
- requirement-to-component mapping
- component responsibilities and ownership
- interfaces, data, and state transitions
- security and trust boundaries
- failure, retry, resume, and blocked behavior
- migration, compatibility, and rollback
- code additions, changes, and deletions
- testing and completion evidence

## Operating Modes

Use **Interactive Mode** unless the user asks for headless, batch, autonomous, draft-first, "no questions", or "just produce the doc".

In **Interactive Mode**, ask one unresolved user decision at a time. Give 2-4 meaningful options, their main trade-offs, and one grounded recommendation. Investigate codebase and environment facts yourself; do not ask the user for facts you can inspect.

Use:

```text
❓ **Q{n} — <decision>**: <why it matters>

Choices:
- A) <option and trade-off>
- B) <option and trade-off>
- C) <option and trade-off, if material>

➡️ **Recommended**: <option and rationale>
```

After each answer, state what is locked and continue to the next unblocked decision.

In **Headless Mode**, do not stop to ask design questions. Read the approved product inputs, inspect the codebase or record greenfield assumptions, choose the most defensible technical design, and produce a complete `stage-{n}-tech-design.md` draft in one pass. When a decision truly needs human confirmation, write it into the output under `Human Review Required` with:

- the decision that needs confirmation;
- the recommended answer;
- 2-4 alternatives and trade-offs;
- the downstream impact if the recommendation is wrong.

Mark uncertain assumptions inline as `Assumption` or `Needs Review`. Headless output is a reviewable draft, not final approval.

## Human-facing handoff

Write Issue, PR, Gate, and delivery handoff comments to Human in concise Chinese, using plain language and leading with the conclusion. Keep the design document itself in the project's established language. Use this shape:

```text
结论：<是否可进入下一步，以及最重要的原因>
改动：<已全文复核并整合/保持的长期架构、职责、契约、数据、状态、安全、迁移和测试章节；说明清理了哪些矛盾>
依据：<canonical inputs / accepted ADR / direct implementation evidence>
待确认：<需要 Human 或产品权威决定的事项；没有则写“无”>
```

This handoff block is mandatory for every delivered draft or revision, including greenfield output. When the response contains the design artifact itself, append a separate handoff block after the artifact; do not assume the document title, body, or `Human Review Required` section substitutes for the Human-facing comment. For a revision, the `改动` line must report the whole-document reconciliation result across every affected authoritative section, including sections intentionally preserved and contradictions removed or routed for authority; a point-fix list is insufficient.

Do not make the Human reconstruct the conclusion from a design body or Agent activity log.

## Protect the product boundary

Technical design must not silently:

- add user-facing concepts or artifacts;
- create a second source of truth;
- weaken acceptance criteria;
- change user-visible behavior, states, or workflows;
- revive replaced behavior merely to fit current code.

If implementation analysis exposes a product decision, return that branch to `prd-grill`, update the PRD, then resume.

# Output

Produce:

```md
# Stage {N} Technical Design: <Stage Name>

## 1. Scope and Traceability

### Canonical Inputs
<product, stage plan, and PRD paths>

### In Scope / Out of Scope
<technical scope and exclusions>

| PRD ID | Required Behavior | Components | Contract / State | Verification |
|--------|-------------------|------------|------------------|--------------|

## 2. Current Baseline
<existing architecture and constraints, or explicit greenfield state>

## 3. Target Architecture
<architecture diagram and explanation>

| Component | Responsibility | Inputs | Outputs | Must Not Own |
|-----------|----------------|--------|---------|--------------|

### Decisions
| Decision | Choice | Alternatives | Rationale | Trade-Off |
|----------|--------|--------------|-----------|-----------|

## 4. Contracts, Data, and State

### Interfaces
<inputs, outputs, errors, idempotency, and callers>

### Data and Persistence
<schemas, ownership, mutability, indexes, and retention>

### State and Recovery
<transitions, rejected actions, retries, resume, and blocked behavior>

## 5. Security and Trust Boundaries
<actors, authentication, authorization, secrets, ownership, and prohibited flows>

## 6. Migration and Compatibility
<migration, versioning, deprecation, rollback, and documentation updates>

## 7. Code Impact
| Path / Module | Add / Change / Delete | Responsibility Change | PRD IDs |
|---------------|-----------------------|-----------------------|---------|

## 8. Testing and Evidence
- Unit: <logic and invariants>
- Integration: <boundaries and persistence>
- End-to-end: <PRD flows and blocked cases>
- Migration: <forward and rollback>
- Security: <authorization and prohibited actions>
- Completion evidence: <commands, reports, and artifacts>

## 9. Risks and Open Decisions
| Risk / Decision | Impact | Mitigation / Owner | Blocking? |
|-----------------|--------|--------------------|-----------|

## 10. Human Review Required
| Decision | Recommendation | Alternatives | Impact If Wrong |
|----------|----------------|--------------|-----------------|
| <decision needing human confirmation> | <recommended answer> | <2-4 options> | <what changes downstream?> |

## 11. Review
- **Requirement Coverage**: Complete / Incomplete
- **Architecture Coherence**: Pass / Request Changes
- **Migration Safety**: Pass / Request Changes / Not Applicable
- **Testability**: Pass / Request Changes
- **Ready for Implementation Planning**: Yes / No, because <reason>
```

# Completion Gate

Finish only when:

- every P0 PRD requirement maps to components and verification;
- responsibilities, contracts, state, and failure behavior are unambiguous;
- security boundaries are explicit where relevant;
- migration and rollback are defined or marked not applicable for greenfield;
- code impact and testing cover normal, blocked, boundary, and migration cases;
- no technical decision changes the approved product contract;
- Interactive Mode: the user approves the design for implementation planning;
- Headless Mode: approval and any unresolved design decisions are listed in `Human Review Required`.
