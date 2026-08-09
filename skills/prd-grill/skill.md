---
name: prd-grill
description: Grill the user to design a single stage's detailed PRD. Clarifies user flows, features, technical decisions, quality standards, and acceptance criteria. Requires product.md and product-stages.md as input. Outputs stage-{n}-prd.md—a specification that guides development for one stage.
---

# Background

Stage PRD design is a **detailed execution specification**, not philosophy.

A stage PRD must answer: **what is the user flow**, **what features are built**, **what are the technical decisions**, **what's the quality bar**, **how do we validate**, and **what are the risks**. This specification must be clear enough for developers and QA to work autonomously.

A "decision tree" for stage PRD includes: **user flows**, **feature scope and priority**, **technical architecture**, **quality standards**, **validation strategy**, and **edge cases/risks**.

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
- **technical architecture** — how is this built? why this tech stack / design? constraints?
- **data model** — what data structures, entities, APIs are needed?
- **quality and non-functional requirements** — performance, reliability, security, compliance
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

The session ends when the frontier is empty. Do not start development until PRD is confirmed and user is ready.

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
| Feature | User Story | Acceptance Criteria | Priority | Technical Notes |
|---------|------------|-------------------|----------|-----------------|
| <name> | As <user>, I want <action> so that <benefit> | <how do we verify it works?> | P0/P1/P2 | <tech decisions> |

### Features Explicitly NOT in This Stage
<what's deferred? why?>

## IV. Technical Design

### Architecture / Tech Stack
<how is this built? key tech decisions and why>

### Data Model
<core entities, relationships, APIs needed>

### System Interfaces
<how does this stage connect to external systems or other stages?>

### Constraints and Non-Functional Requirements
- Performance: <e.g., response time < 500ms>
- Reliability: <uptime, error handling>
- Security: <auth, data privacy, compliance>
- Scalability: <concurrent users, data volume>

## V. Quality and Acceptance

### Definition of Done
<what must be true for a feature to be considered complete?>
- Code review passed
- Tests pass (unit / integration / E2E)
- Documentation updated
- Performance benchmarks met
- etc.

### Acceptance Criteria (per feature)
<from feature table above; reference it>

### Testing Strategy
- Unit test coverage: <target %?>
- Integration tests: <what scenarios?>
- E2E tests: <user journeys to test?>
- Manual testing: <what requires manual QA?>

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
<what still needs deciding before dev starts?>

## VII. Rollout and Validation

### Rollout Strategy
<how do we deploy this? canary, full, phased?>

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

**Why It Matters**: <why is this blocking development?>

**Next Step**: <what needs to be clarified or decided?>
```

Then continue grilling.

# Core Principles

1. **PRD is a specification, not a suggestion** — developers should not have to guess
2. **User flows are the spine** — everything else hangs off how users actually use it
3. **Acceptance criteria are testable** — if you can't test it, it's not done
4. **Trade-offs are explicit** — why this feature and not that one? why this tech and not that?
5. **Risks are named** — what could go wrong? what's the mitigation?
6. **One question at a time, with options** — clarity over speed

# Anti-Patterns

1. Features listed without user flows → "Who uses this? What's the actual task?"
2. "Nice to have" unclear → "Which features are P0 MVP vs. P2 future?"
3. Acceptance criteria too vague → "How do you test 'fast'? Be specific."
4. Technical decisions without reasoning → "Why this database? What were the alternatives?"
5. No edge cases → "What if the user does X? Does the system handle it?"
6. Dependencies ignored → "What external blockers exist?"
7. No rollout plan → "How do we deploy this safely?"

# Session Complete When

- [ ] Stage objective is clear and measurable
- [ ] Primary user for this stage is defined
- [ ] Core user flows are step-by-step documented
- [ ] Feature list is prioritized and scoped
- [ ] Deferred features are explicitly listed
- [ ] Technical architecture is decided
- [ ] Data model is clear
- [ ] Non-functional requirements are specified
- [ ] Definition of done is explicit
- [ ] Acceptance criteria per feature are testable
- [ ] Edge cases and error handling are documented
- [ ] Major risks are identified
- [ ] External dependencies are mapped
- [ ] Rollout and validation plan is ready
- [ ] User confirms: "Devs can start building now."
- [ ] No major ambiguity remains
