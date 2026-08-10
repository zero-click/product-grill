---
name: tech-design-grill
description: Grill the user to turn an approved stage PRD into an implementable technical design grounded in the real codebase when one exists, or in an explicit greenfield baseline. Clarifies current and target architecture, component responsibilities, interfaces, data and state design, security boundaries, migration, code impact, testing, and requirement traceability. Requires product.md, product-stages.md, and stage-{n}-prd.md. Outputs stage-{n}-tech-design.md. Use after PRD approval and before implementation planning or coding.
---

# Background

Technical design translates an approved product contract into an implementable system design. It answers **how the approved requirements will be realized** without silently changing what the product is supposed to do.

A valid design must be grounded in both:

1. the canonical product chain: `product.md → product-stages.md → stage-{n}-prd.md`;
2. the actual codebase, when one exists: current modules, contracts, persistence, runtime behavior, tests, and migration constraints; otherwise an explicitly declared greenfield baseline.

Do not treat an older technical document as authoritative merely because it is more detailed. If the user has declared a newer product document canonical, record conflicts with old documents as migration work.

# Requirement

## Inputs (Required)

- `product.md` — settled product definition
- `product-stages.md` — settled stage plan
- `stage-{n}-prd.md` — approved product requirements for the target stage
- the current codebase and relevant runtime/configuration files, if they exist
- project mode: existing system or greenfield

If one of the three product documents is missing or not approved, stop and return to the appropriate product skill. For an existing system, if the codebase is inaccessible, state that limitation rather than inventing current architecture. For a greenfield project, explicitly record that no current implementation exists.

## First: establish the source of truth

Before asking design questions:

1. Read the three canonical product documents.
2. Inspect the actual codebase and tests, or explicitly establish a greenfield baseline when no implementation exists.
3. Identify old or replaced designs that may create migration debt.
4. Build a requirement inventory from stable PRD IDs.
5. Separate facts from decisions:
   - codebase and environment facts are your responsibility to investigate;
   - architectural trade-offs and compatibility policy are user decisions.

## Design decision tree

Interview the user until shared understanding of the technical design is reached. Main branches include:

- **current architecture** — what exists now and where are the relevant boundaries, or what is explicitly absent in greenfield mode?
- **target architecture** — what components and responsibilities are needed?
- **requirement mapping** — how does each PRD requirement map to components and tests?
- **interfaces and contracts** — what calls what, with which inputs, outputs, and failures?
- **data and state** — what is persisted, what is derived, and who owns each mutable field?
- **security and trust boundaries** — which actors and channels are trusted to perform which actions?
- **migration and compatibility** — how do existing data, contracts, configuration, and callers move forward?
- **failure and recovery** — how does the system fail safely, retry, resume, or block?
- **testing and verification** — what proves the design and PRD are implemented correctly?
- **code impact** — which modules are added, changed, deleted, or explicitly left alone?

Work **one unresolved architectural decision at a time**. Do factual codebase investigation in parallel where useful, but do not batch multiple user decisions into one question.

Format each decision question as:

```text
❓ **Q{n} — <decision title>**: <decision and why it matters>

Choices:
- A) <option A and main trade-off>
- B) <option B and main trade-off>
- C) <option C, if material>

➡️ **Recommended**: <one option, grounded in the PRD and current codebase>
```

After the user answers, briefly record what was locked and what it unlocks next.

## Product boundary protection

Technical design may choose implementation mechanisms, but it must not silently:

- add a new user-facing product concept;
- create a second source of truth;
- weaken an acceptance criterion;
- change a user-visible state or workflow;
- introduce a new product artifact merely to fit the current code;
- restore behavior from a replaced legacy design.

If implementation analysis exposes an unresolved product question, stop that branch and route the decision back to `prd-grill`. Update the PRD first, then resume technical design.

# Output

Once shared understanding is reached, produce:

```md
# Stage {N} Technical Design: <Stage Name>

## 1. Scope and Requirement Mapping

### Canonical Inputs
- Product: `product.md`
- Stage plan: `product-stages.md`
- PRD: `stage-{n}-prd.md`

### In Scope / Out of Scope
<technical scope and explicit exclusions>

### Requirement Traceability
| PRD ID | Required Behavior | Component(s) | Interface / State | Verification |
|--------|-------------------|--------------|-------------------|--------------|
| FR-01 | <behavior> | <component> | <contract> | <test/evidence> |

## 2. Current Architecture

### Relevant Components
<what exists today and which responsibilities they own>

### Current Constraints and Debt
<legacy contracts, coupling, migration constraints, replaced documents>

## 3. Target Architecture

### Architecture Overview
<diagram and explanation>

### Component Responsibilities
| Component | Responsibility | Inputs | Outputs | Must Not Own |
|-----------|----------------|--------|---------|--------------|

### Key Decisions and Alternatives
| Decision | Chosen Option | Alternatives | Rationale | Trade-Off |
|----------|---------------|--------------|-----------|-----------|

## 4. Contracts, Data, and State

### Interfaces
<per-interface inputs, outputs, errors, idempotency, and caller>

### Data and Persistence
<entities or schemas, ownership, mutability, indexes, retention>

### State Machine
<states, transitions, actor/event, reject conditions>

### Failure and Recovery
<failure modes, retries, resume rules, blocked states, operator action>

## 5. Security and Trust Boundaries

<actors, authentication, authorization, secrets, prohibited flows, channel separation>

For systems with multiple actors, authentication channels, or shared mutable resources, include explicit actor/auth, ownership, field ownership, and state-transition tables.

## 6. Migration and Compatibility

### Migration Path
<how existing schemas, files, APIs, configuration, or users move to the target>

### Compatibility Policy
<backward compatibility, versioning, deprecation, rollback>

### Documentation and Reference Migration
<README, workflow, agent instructions, examples, and old designs that must be updated or marked legacy>

## 7. Code Impact

| Path / Module | Add / Change / Delete | Responsibility Change | PRD IDs |
|---------------|-----------------------|-----------------------|---------|

<identify obsolete components that should be removed rather than preserved by default>

## 8. Testing and Verification

### Test Strategy
- Unit: <logic and invariants>
- Integration: <component and persistence boundaries>
- End-to-end: <PRD user flows and blocked scenarios>
- Migration: <old-to-new and rollback cases>
- Security: <authorization and prohibited actions>

### Architecture Conformance
<how boundaries, dependencies, and forbidden ownership are checked>

### Completion Evidence
<commands, reports, and traceability evidence required before implementation is considered complete>

## 9. Risks and Open Decisions

| Risk / Decision | Impact | Mitigation / Owner | Blocking? |
|-----------------|--------|--------------------|-----------|

## 10. Architecture Review

- **Requirement Coverage**: Complete / Incomplete
- **Architecture Coherence**: Pass / Request Changes
- **Migration Safety**: Pass / Request Changes
- **Testability**: Pass / Request Changes
- **Ready for Implementation Planning**: Yes / No, because <one sentence>
```

If shared understanding is not reached, output:

```md
# Technical Design Ready: No

**Unresolved Decision**: <decision>

**Why It Matters**: <impact on architecture, migration, or verification>

**Required Next Step**: <investigation or user decision>
```

Then continue grilling.

# Core Principles

1. **PRD defines what; technical design defines how** — never hide product changes inside architecture.
2. **Inspect before designing** — current code and tests are facts, not assumptions; in greenfield mode, explicitly record their absence.
3. **One source of truth** — derive from the canonical product chain and record legacy drift separately.
4. **Trace every requirement** — each PRD ID maps to components and verification evidence.
5. **Migration is part of design** — a target architecture without a safe path from current state is incomplete.
6. **Failure paths are first-class** — blocked, retry, recovery, and rollback behavior must be explicit.
7. **Delete obsolete layers deliberately** — do not preserve accidental abstractions merely for compatibility.
8. **One decision at a time** — give alternatives and a grounded recommendation.

# Anti-Patterns

1. Rewriting the PRD inside the design instead of referencing requirement IDs.
2. Designing from an old architecture document without inspecting current code.
3. Choosing modules or schemas before current and target ownership are clear.
4. Adding adapters, registries, bindings, or packages without a demonstrated responsibility.
5. Saying “backward compatible” without defining versioning, migration, and rollback.
6. Listing tests without mapping them to PRD behavior and failure boundaries.
7. Treating passing unit tests as evidence of architecture or product conformance.
8. Starting implementation while architecture review still has blocking decisions.

# Session Complete When

- [ ] Canonical product inputs are confirmed
- [ ] Current architecture is grounded in inspected code, or greenfield mode is explicitly established
- [ ] Every P0 PRD requirement maps to a component and verification method
- [ ] Target component responsibilities and ownership are unambiguous
- [ ] Interfaces, data, state, and failure behavior are specified
- [ ] Security and trust boundaries are explicit where relevant
- [ ] Migration, compatibility, and rollback are defined
- [ ] Code impact includes additions, changes, and deletions
- [ ] Test strategy covers normal, blocked, boundary, and migration scenarios
- [ ] No technical decision silently changes the approved product contract
- [ ] User confirms: "The technical design is approved. We can plan implementation."
