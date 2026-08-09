---
name: product-grill
description: Grill the user until a vague product idea becomes a clear, documented Product Definition. Clarifies target user, core problem, product model, core assumptions, long-term vision, and boundaries. Outputs product.md—the high-level product specification that guides stage design and team execution.
---

# Background

Product definition clarification is a **dependency-driven process**.

A valid product model depends on foundational decisions: **target user**, **core problem**, **why now**, **core model/architecture**, **key assumptions**, **long-term vision**, and **safety boundaries**. Hidden assumptions must surface. If these are unsettled, do not jump to stage planning or PRD writing.

A "decision tree" is the structure for product definition dependency management. Each decision unlocks downstream decisions. Ask only questions whose prerequisites are already settled.

# Requirement

Interview the user until shared understanding of the Product Definition is reached. Map this as a **decision tree**: the root is the proposed product, and main branches typically include:

- **target user** — who benefits? why them specifically?
- **core problem** — what specific pain point or opportunity?
- **why now** — why is this the right time?
- **core model** — how does the product fundamentally work? what's the architecture?
- **key assumptions** — what must be true for this to work?
- **core decisions** — why this approach and not the alternative?
- **long-term vision** — where does this product go in 3-5 years?
- **non-goals and boundaries** — what explicitly will NOT be done? safety limits?
- **key dependencies** — what must exist or be true?
- **open questions** — what's still uncertain?

Work **one question at a time**. The **frontier** is every decision whose prerequisites are settled—questions you can ask NOW. Identify the next frontier question, ask it with your recommended answer, wait for user confirmation before moving to the next question.

Each question should be formatted:

```
❓ **Q{n}** - **<question title>**: <question body>

Choices:
- A) <option A>
- B) <option B>
- C) <option C, if needed>

➡️ **Recommended**: <one recommended option and why>
```

After user answers, reflect briefly on what it unlocks, then ask the next question. Do not batch multiple frontier questions into one turn.
Default to multiple-choice with recommendation. Use open freeform only when options cannot be meaningfully pre-defined.

Finding **facts** is your job (research examples, examine context, look up precedents). Never ask the user for facts you could research yourself. When a frontier question requires an environment fact (filesystem, tools, runtime state), dispatch a sub-agent to fetch it. Do not block the whole round: treat that branch as unsettled and continue asking other frontier questions whose prerequisites are already settled. Finding **decisions** is theirs.

If the product bundles multiple distinct products or contradicts itself, say so directly and propose splitting.

The session ends when the frontier is empty: every material branch visited, nothing important left implicit. Do not move to product-stage-design until the user confirms shared understanding.

# Output

Once shared understanding is reached, produce:

```md
# Product Definition Document

## I. Product Identity

### One-Sentence Definition
<what is this product in one clear sentence?>

### Target User
<who is this for? why this user and not others?>

### Core Problem
<what specific pain point or opportunity does this solve?>

### Why Now
<why is this the right time to build this?>

## II. Product Model

### Core Model / Architecture
<how does this product fundamentally work? what's the key mechanism?>
<include diagram if helpful>

### Key Concepts and Definitions
<what are the core terms/components users and team need to understand?>

### Core Assumptions (待验证 if uncertain)
<what must be true for this product to work? mark assumptions that are uncertain>

### Core Decisions and Trade-Offs
<why did we choose this design over the alternative? what trade-offs did we make?>

## III. Vision and Boundaries

### Long-Term Vision
<where does this product go in 3-5 years? what's the mature state?>

### Non-Goals (explicitly NOT in this product)
<what will we deliberately NOT do?>

### Safety Boundaries (hard limits)
<what can the product never do? what's off-limits?>

## IV. Success and Risk

### North Star Metric (long-term)
<the single most important measure of success>

### Key Dependencies
<what must be true? what could block this?>

### Major Risks
<what's most likely to go wrong? what big unknowns exist?>

### Open Questions
<what do we still need to decide or validate?>

## V. Readiness Assessment

- **Clarity**: Strong / Medium / Weak
- **Major Uncertainties**: <what's still unclear and needs stage design to validate?>
- **Ready for Stage Planning**: Yes / No, because <one sentence>
```

If shared understanding has NOT been reached, output:

```md
# Shared Understanding Reached: No

**Unresolved Branch**: <which decision tree branch is still open?>

**Why It Matters**: <why can't we proceed?>

**Next Step**: <what needs to be clarified?>
```

Then continue grilling.

# Core Principles

1. **One question at a time** — focus and clarity
2. **Give 2-4 options + one recommendation** — improve decision quality and speed
3. **Facts are your responsibility** — never ask the user for things you could research
4. **Core model is the heart** — spend time here; it defines everything downstream
5. **Assumptions must be explicit** — especially for new/risky products
6. **Core decisions need reasoning** — "why not the alternative?" surfaces critical thinking
7. **Mark uncertainties** — don't pretend everything is settled

# Anti-Patterns

1. Product too vague: "Better AI tool" → "What specifically? How different from existing?"
2. Bundled products: "AI assistant + scheduling + analytics" → "Which is the core problem?"
3. Assumptions hidden: "Of course users will do X" → "Why are we sure?"
4. No trade-offs: "We'll have everything" → "What trade-offs define the design?"
5. Unclear model: Can't explain the product in a flow diagram → model not clear enough
6. Wishful vision: "We'll be #1" → "What does success concretely look like?"
7. No boundaries: "Everything is in scope" → "What won't we do?"

# Session Complete When

- [ ] Target user is specific and justified
- [ ] Core problem is clearly stated
- [ ] Why now is explained
- [ ] Core model/architecture is understandable
- [ ] Key assumptions are explicit (with uncertainty flags)
- [ ] Core decisions and trade-offs are documented
- [ ] Long-term vision is concrete
- [ ] Non-goals are explicitly listed
- [ ] Safety boundaries are stated
- [ ] Key dependencies are identified
- [ ] Major risks are surfaced
- [ ] North star metric is defined
- [ ] User confirms: "This is our product. I'm ready to plan stages."
- [ ] No major ambiguity remains
