---
name: product-stage-design
description: Grill the user to plan and prioritize product stages. Clarifies why stages are divided this way, what each stage validates, stage dependencies, and risks. Requires product.md as input. Outputs product-stages.md—a roadmap that guides stage-by-stage PRD writing.
---

# Background

Stage planning is not feature listing. It's a **hypothesis validation strategy**.

Each stage should test core assumptions, reduce risk, or build toward the long-term vision defined in product.md. Stage division reflects strategy: do we learn fast (MVP-first) or build capability (foundation-first)?

A "decision tree" for stage planning includes: **why divide stages this way**, **what each stage proves**, **dependencies between stages**, **key assumptions per stage**, and **major risks**.

When product uncertainty is still high, prefer **1+N planning**:
- lock Stage 1 in full detail
- keep later stages as placeholders with trigger conditions
- refine later stages only after Stage 1 is validated

# Requirement

## Input (Required)

- `product.md` (settled product definition)

If input is missing, stop grilling and ask the user to provide/confirm the input first.

Interview the user until shared understanding of Stage Planning is reached. Assume product.md is already settled. Map as **decision tree**: main branches include:

- **stage division rationale** — why this many stages? what's the dividing principle? (learn fast vs. build foundation vs. de-risk)
- **stage sequence** — why this order? which can run in parallel?
- **planning mode** — full upfront roadmap vs. 1+N (Stage 1 locked + later placeholders)
- **stage goals** — what does each stage accomplish? what does it prove or unblock?
- **stage scope** — what's in vs. out of each stage? why?
- **key assumptions per stage** — what must be true? what do we validate?
- **dependencies** — does stage B wait for stage A? why?
- **stage risks** — what could go wrong in each stage?
- **stage success criteria** — how do we know each stage succeeded? (gates to next stage)
- **open questions** — what still needs deciding?

Work **one question at a time**. The **frontier** is every decision whose prerequisites are settled. Identify the next frontier question, ask it with recommended answer, and wait for user confirmation before moving on.

Each question should be formatted:

```
❓ **Q1** - **<question title>**: <question body>

Choices:
- A) <option A>
- B) <option B>
- C) <option C, if needed>

➡️ **Recommended**: <one recommended option and why>
```

After user answers, briefly reflect what was locked and what it unlocks next. Do not batch multiple frontier questions in one turn.
Default to multiple-choice with recommendation. Use open freeform only when options cannot be meaningfully pre-defined.

Finding **facts** is your job (research competitors' roadmaps, check dependencies, examine product.md). Never ask the user for facts you could research yourself. When a frontier question requires an environment fact (filesystem, tools, runtime state), dispatch a sub-agent to fetch it. Do not block the whole round: treat that branch as unsettled and continue asking other frontier questions whose prerequisites are already settled. Finding **decisions** is theirs.

The session ends when the frontier is empty. Do not write stage-level PRDs (prd-grill) until stages are planned and user confirms.

# Output

Once shared understanding is reached, produce:

```md
# Product Stage Planning

## I. Stage Division Strategy

### Rationale
<why divide into stages this way? what's the core principle (learn fast, de-risk, build foundation)?
what assumptions are we testing stage-by-stage?>

### Stage Sequence
<in what order? any parallelization?>

## II. Stage Roadmap

| Stage | Name | Primary Goal | Key Assumptions to Validate | Success Criteria | Dependencies | Estimated Duration |
|-------|------|--------------|----------------------------|------------------|--------------|-------------------|
| 1 | <name> | <what does this stage achieve?> | <what must be true?> | <how do we know it worked?> | <blocks/waits for?> | <estimate> |
| 2 | ... | ... | ... | ... | ... | ... |

If using **1+N mode**, Stage 2+ may be placeholders with trigger conditions and TBD details.

## III. Stage Details

### Stage 1: <Name>
- **Goal**: <specific target for this stage>
- **Key Assumptions**: <what are we betting on>
- **Major Unknowns**: <what might go wrong>
- **Unblocks**: <what does success enable>
- **Risks**: <what's most likely to derail this>

### Stage 2: <Name>
[same structure]

If placeholder:
- **Trigger Condition**: <what must be true before this stage is detailed>
- **Current Definition**: Placeholder (to be refined after prior stage validation)

...

## IV. Readiness Assessment

- **Clarity**: Strong / Medium / Weak
- **Stage Dependencies Clear**: Yes / No
- **Ready for PRD Writing**: Yes / No, because <one sentence>

### Open Questions
<what still needs deciding before stage PRDs?>
```

If shared understanding NOT reached:

```md
# Shared Understanding Reached: No

**Unresolved Branch**: <which stage planning decision is still open?>

**Why It Matters**: <why does this matter for roadmap?>

**Next Step**: <what needs to be clarified?>
```

Then continue grilling.

# Core Principles

1. **Stages test assumptions, not just build features** — each stage should answer a core question
2. **Rationale is more important than the schedule** — understand WHY before discussing when
3. **Dependencies are explicit** — spell out what each stage waits for or enables
4. **One question at a time, with options** — each question should include 2-4 choices and one recommendation
5. **Risks are surfaced** — what could derail each stage?
6. **Success is measurable** — each stage has a gate to the next

# Anti-Patterns

1. Stages are just "1-2-3-4" with no rationale → "Why these splits? What's each stage proving?"
2. All features in stage 1, nothing in stage 2 → "What's left to validate?"
3. Stages are identical (no learning between them) → "What does each stage teach us?"
4. Dependencies ignored → "Which stages wait for which?"
5. No risks per stage → "What's the biggest threat to each stage?"
6. Success criteria too vague → "How will we actually know if this stage succeeded?"

# Session Complete When

- [ ] Stage division rationale is clear
- [ ] Stage sequence and ordering is justified
- [ ] Each stage has a clear goal
- [ ] Key assumptions per stage are identified
- [ ] Dependencies between stages are explicit
- [ ] Success criteria for each stage are measurable
- [ ] Major risks per stage are surfaced
- [ ] User confirms: "This roadmap makes sense. I'm ready for stage PRDs."
- [ ] No major uncertainties in the plan remain
