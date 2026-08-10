---
name: tech-design-grill
description: Grill an approved stage PRD into an implementable technical design. Use after PRD approval and before implementation planning or coding. Requires product.md, product-stages.md, and stage-{n}-prd.md; inspect the existing codebase when present or establish greenfield mode. Outputs stage-{n}-tech-design.md with architecture, contracts, state, security, migration, code impact, testing, and requirement traceability.
---

# Background

Technical design defines **how** to implement an approved product contract without silently changing **what** the product must do.

Ground decisions in:

1. `product.md → product-stages.md → stage-{n}-prd.md`;
2. the current code and tests, or an explicit greenfield baseline.

Treat replaced designs as migration context, not as the source of truth.

# Inputs

Required:

- settled `product.md`
- settled `product-stages.md`
- approved `stage-{n}-prd.md`
- project mode: existing system or greenfield
- current codebase and runtime/configuration files, when they exist

If a product document is missing or unapproved, return to the appropriate product skill. If an existing codebase is inaccessible, state the limitation rather than inventing architecture.

# Process

Before asking design questions:

1. Read the canonical product documents.
2. Inventory stable PRD requirement IDs.
3. Inspect relevant code, contracts, persistence, configuration, and tests; in greenfield mode, record that no current implementation exists.
4. Identify legacy designs and compatibility constraints.

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

Ask **one unresolved user decision at a time**. Give 2-4 meaningful options, their main trade-offs, and one grounded recommendation. Investigate codebase and environment facts yourself; do not ask the user for facts you can inspect.

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

## 10. Review
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
- the user approves the design for implementation planning.
