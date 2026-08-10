---
name: prd-grill
description: Grill the user to define a single stage's product requirements. Clarifies user flows, product behavior, feature scope, quality outcomes, acceptance criteria, edge cases, and risks. Requires product.md and product-stages.md as input. Outputs stage-{n}-prd.md as the approved product input to technical design. Use this for stage PRDs; do not use it to choose architecture, tech stack, modules, database schemas, or implementation tasks.
---

# Background

Stage PRD design is a **detailed product specification**, not philosophy and not technical design.

A stage PRD must answer: **what is the user flow**, **what product behavior is required**, **what is in scope**, **what is the quality bar**, **how the result is accepted**, and **what are the risks**. It must be precise enough for product, engineering, and QA to share one behavioral contract while leaving implementation choices to a separate technical design.

A "decision tree" for stage PRD includes: **user flows**, **feature scope and priority**, **observable product behavior**, **product-level artifacts and states**, **quality outcomes**, **acceptance strategy**, and **edge cases/risks**.

# Requirement

## Input (Required)

- `product.md` (settled product definition)
- `product-stages.md` (settled stage plan, including target stage)

If input is missing, stop grilling and ask the user to provide/confirm the input first.

Interview the user until shared understanding of this stage's detailed design is reached. Assume product.md and product-stages.md are settled. Map as **decision tree**: main branches include:

- **stage goal and success criteria** — what is this stage achieving? how do we measure success?
- **target user for this stage** — who is the primary user (may be narrower than product.md)
- **user flows** — step-by-step: how does the user accomplish key tasks in this stage?
- **feature list and priority** — what features are built? what's MVP vs. nice-to-have?
- **product contract** — what artifacts, user-visible states, ownership rules, and observable system behaviors must exist?
- **quality and non-functional outcomes** — what performance, reliability, security, privacy, or compliance outcomes must users receive?
- **acceptance criteria** — how do we know this feature is done? definition of done?
- **edge cases and error handling** — what goes wrong? how do we handle it?
- **dependencies and risks** — what external blockers? what could derail this?
- **open questions** — what still needs deciding before dev?

Work **one question at a time**. The **frontier** is every decision whose prerequisites are settled. Identify the next frontier question, ask it with recommended answer, and wait for user confirmation before moving on.

Each question should be formatted:

```
❓ **Q1** - **<question title>**: <question body, including choices if applicable>

Choices:
- A) <option A>
- B) <option B>
- C) <option C, if needed>

➡️ **Recommended**: <one recommended option and why>
```

After user answers, briefly reflect what was locked and what it unlocks next. Do not batch multiple frontier questions in one turn.
Default to multiple-choice with recommendation. Use open freeform only when options cannot be meaningfully pre-defined.

Finding **facts** is your job (examine product.md, review product-stages.md, research similar products). Never ask the user for facts you could research yourself. When a frontier question requires an environment fact (filesystem, tools, runtime state), dispatch a sub-agent to fetch it. Do not block the whole round: treat that branch as unsettled and continue asking other frontier questions whose prerequisites are already settled. Finding **decisions** is theirs.

The session ends when every material product branch is settled or explicitly marked for validation. Do not start technical design until the PRD is confirmed.

# Output

Once shared understanding is reached, produce:

```md
# Stage {N} PRD: <Stage Name>

## I. Stage Objective

### What We're Building
<one sentence: what is the user-visible output of this stage?>

### Success Criteria for This Stage
<measurable definition of success; should align with product-stages.md gate>

### Key Assumptions We're Testing
<from product-stages.md; what must be true for this to work?>

## II. Target User and Flows

### Primary User Persona (for this stage)
<who is the main user for this stage? may be narrower than product.md>

### Core User Flows
<step-by-step flows for primary tasks:>

**Flow 1: <Task Name>**
1. User does X
2. System does Y
3. ...

**Flow 2: <Task Name>**
[same structure]

## III. Feature Specification

### Feature List (MVP scope for this stage)
| ID | Feature | User Story | Acceptance Criteria | Priority | Product Rules |
|----|---------|------------|---------------------|----------|---------------|
| FR-01 | <name> | As <user>, I want <action> so that <benefit> | <observable evidence that it works> | P0/P1/P2 | <required behavior or invariant> |

### Features Explicitly NOT in This Stage
<what's deferred? why?>

## IV. Product Contract

### Core Artifacts and Ownership
<what product objects or artifacts exist, who creates/reads/updates them, and which one is the source of truth?>

### User-Visible States and Transitions
<what states can users observe, what events move between them, and what outcomes are terminal or blocked?>

### External Behavior and Constraints
<what must callers or users be able to do or observe? Define product behavior, not API paths, database tables, modules, or framework choices.>

### Non-Functional Outcomes
- Performance: <user-visible threshold and measurement condition>
- Reliability: <required recovery or availability outcome>
- Security and privacy: <required product boundary and prohibited outcome>
- Scale: <expected usage envelope only when material to acceptance>

## V. Quality and Acceptance

### Definition of Done
<what product evidence must exist for this stage to be accepted?>
- Every P0 requirement has observable acceptance evidence
- Required normal, blocked, and boundary scenarios pass
- Non-functional outcomes are measured where specified
- No unresolved product decision blocks technical design

### Acceptance Criteria (per feature)
<from feature table above; reference it>

### Acceptance Strategy
- Automated acceptance scenarios: <which externally observable behaviors?>
- End-to-end journeys: <which user flows?>
- Human evaluation: <what requires judgment and by whom?>
- Evidence: <what report, result, or artifact proves acceptance?>

### Edge Cases and Error Handling
<what goes wrong? how should system respond?>
- User input validation: <constraints>
- System failures: <recovery strategy>
- Concurrent operations: <race conditions?>
- Boundary conditions: <limits?>

## VI. Risks and Unknowns

### Major Risks for This Stage
<what's most likely to go wrong?>

### External Dependencies
<what must exist or be true outside this stage?>

### Open Questions
<what still needs deciding before PRD approval or technical design?>

## VII. Stage Validation

### Validation Plan
<how will this stage be validated with target users or representative scenarios? Define exposure and evidence needs as product constraints; leave deployment mechanisms to technical design.>

### Validation Checklist
<how do we confirm success at launch?>
- [ ] All acceptance criteria met
- [ ] Performance benchmarks passed
- [ ] No critical bugs
- [ ] Stage success metric achieved
- [ ] User feedback positive
- [ ] Ready for next stage

### Sign-Off
- Product: _____ Date: _____
- Tech Lead: _____ Date: _____
- QA Lead: _____ Date: _____
```

If shared understanding NOT reached:

```md
# Shared Understanding Reached: No

**Unresolved Branch**: <which PRD decision is still open?>

**Why It Matters**: <why is this blocking PRD approval or technical design?>

**Next Step**: <what needs to be clarified or decided?>
```

Then continue grilling.

# Core Principles

1. **PRD is a product specification, not a suggestion** — engineering should not have to guess required behavior
2. **User flows are the spine** — everything else hangs off how users actually use it
3. **Acceptance criteria are testable** — if you can't test it, it's not done
4. **Product trade-offs are explicit** — why this behavior and not the alternative? what is deferred?
5. **Risks are named** — what could go wrong? what's the mitigation?
6. **One question at a time, with options** — clarity over speed

# Anti-Patterns

1. Features listed without user flows → "Who uses this? What's the actual task?"
2. "Nice to have" unclear → "Which features are P0 MVP vs. P2 future?"
3. Acceptance criteria too vague → "How do you test 'fast'? Be specific."
4. Implementation choices embedded in PRD → move architecture, database, modules, and API implementation into technical design
5. No edge cases → "What if the user does X? Does the system handle it?"
6. Dependencies ignored → "What external blockers exist?"
7. No stage validation plan → "What evidence will show the stage succeeded with its target user?"

# Session Complete When

- [ ] Stage objective is clear and measurable
- [ ] Primary user for this stage is defined
- [ ] Core user flows are step-by-step documented
- [ ] Feature list is prioritized and scoped
- [ ] Deferred features are explicitly listed
- [ ] Core product artifacts, ownership, and user-visible states are clear
- [ ] Non-functional requirements are specified
- [ ] Definition of done is explicit
- [ ] Acceptance criteria per feature are testable
- [ ] Edge cases and error handling are documented
- [ ] Major risks are identified
- [ ] External dependencies are mapped
- [ ] Stage validation plan is ready
- [ ] User confirms: "The product requirements are approved. We can start technical design."
- [ ] No major ambiguity remains
