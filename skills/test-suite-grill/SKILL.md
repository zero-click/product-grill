---
name: test-suite-grill
description: Grill an approved Stage PRD and Technical Design into a QA-owned acceptance test suite. Use after technical design approval and before implementation. Requires product.md, product-stages.md, stage-{n}-prd.md, and stage-{n}-technical-design.md. Outputs stage-{n}-test-suite.md plus a tests/acceptance/stage_N/ directory. The QA agent owns the acceptance contract; Product Lead reviews and approves; the developer agent cannot weaken or rewrite approved acceptance tests.
---

# Background

A stage acceptance test suite is a **verification contract**, not an implementation plan and not a restatement of the PRD.

It answers: **how do we prove the system actually does what the PRD requires?**

A test suite must be precise enough for QA, developer, and reviewer to share one verification standard — while leaving implementation choices to the already-approved technical design.

A "decision tree" for test suite design includes: **requirement coverage matrix**, **black-box acceptance properties**, **negative controls and anti-cheating tests**, **deterministic vs live evidence layers**, and **scenario independence**.

# Requirement

## Input (Required)

- `product.md` (settled product definition)
- `product-stages.md` (settled stage plan, including target stage)
- `stage-{n}-prd.md` (approved Stage PRD)
- `stage-{n}-technical-design.md` (approved Stage technical design)

If input is missing, stop grilling and ask the user to provide/confirm the input first.

Interview the user until shared understanding of the test suite is reached. Assume all four canonical inputs are settled. Map as **decision tree**: main branches include:

- **requirement coverage matrix** — which PRD requirements need mandatory acceptance tests? what evidence proves each?
- **black-box acceptance properties** — for each mandatory requirement, what externally observable behavior must be true for PASS?
- **negative controls and anti-cheating** — what known cheating or shortcut implementations must fail? (e.g., fixed DAG, fixed `completed` JSON, process evidence without artifact, mock masquerading as real runtime, `missing_capability` return path used to satisfy a success scenario)
- **deterministic vs live evidence** — which tests use controlled local data and are CI-stable? which tests require real external interaction and should run as pre-merge or stage-gate evidence?
- **scenario independence** — are Scenario A (success), B (missing capability), C (risk boundary) tested as separate, independent tests? a success test must not be satisfiable by a `missing_capability` return
- **outcome evidence requirements** — what final artifacts, outputs, or observable system state must exist for PASS? process evidence (CLI ran, agent invoked, test green) is necessary but not sufficient
- **executable test mapping** — each acceptance test maps to a concrete test file and command

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

Finding **facts** is your job (examine PRD, technical design, codebase inventory, existing tests). Never ask the user for facts you could research yourself. When a frontier question requires an environment fact (filesystem, tools, runtime state), dispatch a sub-agent to fetch it. Do not block the whole round: treat that branch as unsettled and continue asking other frontier questions whose prerequisites are already settled. Finding **decisions** is theirs.

The session ends when every mandatory requirement has a mapped acceptance test, every anti-cheating concern is addressed, scenarios are independent, and the coverage matrix is complete. Do not start implementation until the test suite is approved by Product Lead.

# Output

Once shared understanding is reached, produce two deliverables:

## 1. `specs/stage-{n}-test-suite.md`

```md
# Stage {N} Acceptance Test Suite

## 1. Authority and Scope

- Product Goal:
- Stage Definition:
- PRD:
- Technical Design:
- QA Owner:
- Reviewer:
- Status: Draft | Approved | Superseded

## 2. Requirement Coverage Matrix

| Requirement ID | Acceptance Test ID | Scenario | Evidence Type | Negative Control | Status |
|----------------|-------------------|----------|---------------|-----------------|--------|
| FR-SN-01 | AT-SN-001 | A (success) | Artifact + Runtime | Fixed output | |
| FR-SN-02 | AT-SN-002 | B (missing) | Block report | Fake completed | |
| ... | ... | ... | ... | ... | |

## 3. Scenario A — Success (Capabilities Available)

### AT-SN-001: <test name>

**Requirement:** FR-SN-...

**Given**
- <preconditions>

**When**
- <action>

**Then**
- <observable outcome>
- <artifact exists>
- <evidence recorded>

**Required Evidence**
- <specific artifact field, URL, content, or state>

**Known Cheating Implementations That Must Fail**
- <fixed DAG>
- <fixed `completed` JSON>
- <process evidence without artifact>
- <mock masquerading as real runtime>
- <`missing_capability` return path satisfying this test>

## 4. Scenario B — Missing Capability

### AT-SN-0XX: <test name>

**Requirement:** FR-SN-...

**Given**
- <required capability removed>

**When**
- <action>

**Then**
- `status: blocked`, `reason: missing_capability`
- No Goalfile generated
- No agent invoked

**Must NOT be satisfiable by**: generating a valid Goalfile or completing First Run

## 5. Scenario C — Risk Boundary

### AT-SN-0XX: <test name>

**Requirement:** FR-SN-...

**Given**
- <risky action requested>

**When**
- <action>

**Then**
- `status: blocked`, `reason: risk_boundary`
- Blocked before invocation or generation

## 6. Anti-Cheating and Negative Controls

### AT-SN-0XX: <test name>

**Given** <known cheating implementation>

**When** <run acceptance test>

**Then** MUST FAIL

## 7. Outcome Evidence Requirements

<What final artifacts, outputs, or system state must exist for any PASS verdict? Process evidence is necessary but not sufficient.>

## 8. Reliability and Repeatability

<Deterministic tests use controlled local data. Live tests use real external sources. Specify which is which and their stability expectations.>

## 9. Executable Test Mapping

| Test ID | Test File | Command |
|---------|-----------|---------|
| AT-SN-001 | `tests/acceptance/stage_N/test_....py` | `uv run pytest ...` |
| ... | ... | ... |

## 10. Stage Acceptance Rule

- All Mandatory acceptance tests must PASS.
- `missing_capability` or `skip` does not satisfy a Scenario A test.
- Scenario A, B, C must be independent tests; a Scenario A test must not be satisfiable by a Block return path.
- Process evidence (CLI ran, agent invoked, CI green) is necessary but not sufficient.
- Outcome Evidence (final artifact exists, content matches success criteria) is required for PASS.
- QA independently runs the acceptance suite after implementation.
- Developer agent must not weaken, rewrite, or delete approved acceptance tests.
- Disputed test changes route through QA and Product Lead.
- Product Lead reviews and approves this suite before implementation.
```

## 2. `tests/acceptance/stage_N/` directory scaffolding

If the project repo exists, create the directory and placeholder test files mapping to each `AT-SN-*` ID:

```
tests/acceptance/stage_N/
├── __init__.py
├── test_scenario_a_success.py
├── test_scenario_b_missing_capability.py
├── test_scenario_c_risk_boundary.py
└── test_anti_cheating.py
```

Each placeholder should contain:
- The test function with docstring referencing its AT-SN ID
- `pytest.skip("acceptance tests not yet implemented — pending QA suite")`
- A comment block with the Given/When/Then from the test suite

If shared understanding NOT reached:

```md
# Shared Understanding Reached: No

**Unresolved Branch**: <which test suite decision is still open?>

**Why It Matters**: <why is this blocking test suite approval?>

**Next Step**: <what needs to be clarified or decided?>
```

Then continue grilling.

# Core Principles

1. **Test suite is a verification contract, not implementation guidance** — it tells you how to prove the system works, not how to build it
2. **Scenarios are independent** — Scenario A success must not be satisfiable by a missing-capability block or a process-only evidence path
3. **Outcome evidence > process evidence** — green tests and invoked agents are necessary but not sufficient; the final artifact must match the success criteria
4. **Anti-cheating is mandatory** — for every acceptance test, identify what cheating implementations would also pass, and ensure they fail
5. **QA owns the contract** — the developer agent reads and implements against the test suite, but cannot weaken or rewrite approved acceptance tests
6. **One question at a time, with options** — clarity over speed

# Anti-Patterns

1. Success test with a `missing_capability` return path → "Does this test actually prove the goal was achieved?"
2. Process evidence accepted as outcome evidence → "The CLI ran and the agent was invoked, but did the artifact get produced?"
3. Developer-authored acceptance tests → "Who owns the test oracle?"
4. No negative controls → "What cheating implementation also passes this test?"
5. Scenarios entangled → "Can Scenario A be satisfied by Scenario B's behavior?"
6. Fixed-output assertions masquerading as property tests → "Does this test verify an implementation choice or a product property?"
7. Test suite restates PRD instead of defining verification → "How exactly do we test this requirement?"

# Session Complete When

- [ ] Every mandatory PRD requirement has a mapped acceptance test
- [ ] Requirement coverage matrix is complete
- [ ] Scenario A, B, C are independent tests
- [ ] Scenario A success is not satisfiable by `missing_capability` or process-only evidence
- [ ] Every acceptance test has at least one anti-cheating negative control
- [ ] Outcome evidence requirements are specified for each test
- [ ] Deterministic vs live evidence layers are classified
- [ ] Executable test mapping is concrete
- [ ] Product Lead review and approval recorded
- [ ] User confirms: "The acceptance test suite is approved. We can start implementation."
- [ ] No major ambiguity in verification standard remains
