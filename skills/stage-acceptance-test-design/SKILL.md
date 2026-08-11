---
name: stage-acceptance-test-design
description: Design and own a stage's independent product acceptance lifecycle after PRD and technical-design approval and before implementation. Converts stable PRD requirement IDs into an approved specs/stage-N-test-suite.md plus runnable QA-owned tests under tests/acceptance/stage_N/. Use when acceptance must be separated from developer tests, when a QA agent needs to write black-box tests before coding, or when implementation claims must be checked against real artifacts and anti-cheating controls.
---

# Stage Acceptance Test Design

## Background

TDD proves that production code satisfies tests chosen by the developer. It does not prove that those tests represent the approved product requirement, reject convenient fake implementations, or inspect the real outcome.

This Skill creates an independent acceptance lifecycle:

```text
approved PRD
→ approved technical design
→ QA test contract and executable acceptance tests
→ Product Lead approval
→ implementation
→ independent QA execution
→ acceptance decision
```

The test contract is derived from the PRD. It cannot add product requirements, relax them, or become a competing source of truth.

## When to Use

Use this Skill when:

- an approved stage is ready to define acceptance before implementation;
- a QA agent must own black-box product tests independently of the developer;
- developer-written tests could encode a weak or implementation-shaped definition of success;
- a stage needs traceability from requirement to executable test and final artifact;
- implementation is complete and QA must independently issue `PASS`, `REQUEST_CHANGES`, or `BLOCKED`.

Do not use it to:

- discover the product or stage roadmap;
- write or reinterpret product requirements;
- choose architecture before technical-design approval;
- replace developer unit/integration tests or code review;
- manufacture a passing result when required runtime capabilities are unavailable.

## Required Inputs and Gate

Required inputs:

- `product.md` — settled product definition;
- `product-stages.md` — settled stage plan;
- `stage-N-prd.md` — approved PRD with stable requirement IDs;
- `stage-N-technical-design.md` — approved technical design;
- the current codebase and test/runtime configuration, or an explicit greenfield baseline;
- the production entrypoint or a documented target entrypoint that will exist in this stage.

Stop and route backward when:

- the PRD is missing, unapproved, contradictory, or lacks stable requirement IDs → return to `prd-grill`;
- the technical design is missing, unapproved, or cannot expose a requirement through an observable seam → return to `tech-design-grill`;
- a proposed test would decide new product behavior → record the product decision and return it to Product Lead/PRD;
- the current implementation or runtime is inaccessible → report the limitation instead of inventing executable tests.

## Ownership and Decision Rights

| Role | Owns | Must Not Do |
|---|---|---|
| QA | Test contract, executable acceptance tests, fixtures, independent execution, acceptance verdict | Modify production code to make tests pass; approve own product interpretation |
| Product Lead | Requirement coverage, product meaning, test-contract approval, Test Change Request approval | Delegate acceptance meaning to the developer |
| Developer | Production code and developer-owned unit/integration tests | Weaken, delete, skip, special-case, or silently modify approved acceptance tests |
| Code Reviewer | Implementation quality and checks for test bypass/tampering | Treat QA pass as a substitute for code review |

The developer may read and run acceptance tests. If a test is wrong or impossible, the developer submits a Test Change Request; QA evaluates it and Product Lead approves or rejects it before any accepted-test change.

## Outputs

Produce both:

```text
specs/stage-N-test-suite.md
tests/acceptance/stage_N/
```

A Markdown contract without runnable tests is incomplete. Runnable tests without an approved requirement mapping are developer tests, not independent acceptance tests.

Use the target project's existing acceptance-test framework and conventions. Do not impose Python or another stack when the project already has a test harness. Every executable test must have one exact command that QA can run non-interactively.

## Process

### 1. Establish the acceptance baseline

Before asking questions:

1. Read the canonical product documents in order.
2. Inventory every in-scope P0/P1 PRD requirement ID and every explicit prohibited outcome.
3. Inspect the production boundary, runtime/tool availability, fixtures, existing tests, and CI commands.
4. Identify observable outputs, state transitions, errors, external effects, and final artifacts.
5. Separate product facts from implementation choices.

Finding repository/runtime facts is QA's job. Ask the user only for unresolved product or risk decisions, one at a time, with 2–4 choices and one recommendation.

### 2. Define acceptance properties before examples

For each requirement, state the externally observable property that must hold. Prefer properties over fixed implementation choices.

Bad:

```text
The workflow must contain strategy_agent then notification_agent.
```

Good:

```text
Every required capability is covered by an executable, authorized agent/tool path;
if any required capability is unavailable, the stage blocks rather than claiming completion.
```

A test may assert an exact value only when the PRD itself requires that value. Do not hard-code a particular DAG, class, module, database, prompt wording, or agent count merely because the current design uses it.

### 3. Build requirement traceability

Every in-scope requirement must map through this chain:

```text
PRD requirement ID
→ acceptance property
→ test ID
→ executable test path and command
→ runtime evidence
→ final artifact or observable outcome
```

Use explicit statuses for uncovered requirements:

- `COVERED`
- `HUMAN_EVALUATION` — judgment is necessary and evaluator/evidence are named;
- `BLOCKED` — an executable seam or dependency is missing;
- `NOT_APPLICABLE` — Product Lead-approved rationale is present.

Never silently omit a requirement.

### 4. Design the minimum sufficient scenario set

Cover these classes where applicable:

1. **Normal outcome** — the production entrypoint produces the required user-visible result.
2. **Blocked or missing capability** — missing agent, tool, permission, dependency, or input causes an honest blocked/failure state.
3. **Risk boundary** — prohibited, unauthorized, paid, destructive, or externally published behavior does not occur.
4. **Outcome evidence** — completion requires the real artifact/content/state, not only process logs or labels.
5. **State consistency** — step states and top-level terminal state cannot contradict each other.
6. **Boundary and recovery** — limits, invalid input, retry/resume, idempotency, and partial failure follow the PRD/design.
7. **Metamorphic behavior** — meaningful input/constraint changes cause the corresponding capability, workflow, or result change.
8. **Repeatability** — repeated isolated runs do not pass because of stale artifacts or shared state.
9. **Holdout coverage** — when keyword/template hard-coding is a material risk, keep representative cases outside the developer-visible fixture set or generate them at run time.

Do not add a category just to fill a template. Each included test must trace to a requirement, explicit risk, or design invariant.

### 5. Define negative controls and cheating implementations

For every mandatory acceptance property, answer:

> What clearly wrong implementation could still pass this test?

List concrete negative controls. At minimum, consider:

- fixed workflow/DAG regardless of goal semantics;
- unconditional `completed`/`passed` responses;
- process invocation, agent call, or Skill load without target result;
- fake or stale artifact from a previous run;
- capability declaration without the required tool, permission, or reachable runtime;
- echoing fixture data or a precomputed expected result;
- empty, placeholder, malformed, or unverifiable output;
- skipped, deselected, quarantined, or expected-failure tests counted as pass;
- top-level success while required steps are pending/failed;
- developer code paths that detect acceptance fixtures and special-case them.

A negative control is valid only if the acceptance suite rejects it for the intended reason.

### 6. Write the executable tests before implementation

Create tests under:

```text
tests/acceptance/stage_N/
```

Rules:

- exercise the production entrypoint or approved public boundary;
- isolate each run in a new temporary workspace/state store;
- construct or copy fixtures explicitly;
- assert artifacts and external behavior, not private implementation details;
- verify provenance when stale/prebuilt artifacts are possible;
- verify prohibited side effects by observing the relevant boundary;
- fail on unexpected `skip`, `xfail`, deselection, timeout suppression, or missing test collection;
- emit useful failure evidence without leaking secrets;
- avoid network dependence unless the PRD/design explicitly makes a live external source part of acceptance;
- when live dependencies are required, distinguish dependency failure (`BLOCKED`) from product failure (`REQUEST_CHANGES`).

Each test entry must name:

- test ID and requirement IDs;
- Given / When / Then;
- exact executable path;
- exact non-interactive command;
- expected evidence and artifact;
- negative control(s);
- isolation/provenance strategy;
- mandatory vs. advisory status.

### 7. Prove that the suite can fail

Before Product Lead approval and before production implementation:

1. Run the suite against the current baseline, an intentionally incomplete seam, or controlled mutants.
2. Exercise the named cheating implementations through dependency injection, test doubles, fixture variants, or temporary mutations without committing them to production.
3. Record which test rejects each mutant and why.
4. Restore the baseline and verify the working tree.

At least the critical negative controls must produce the expected failures. A suite that only demonstrates green results has not established that its assertions discriminate correct from fake behavior.

Do not require all tests to be red when the repository already contains valid behavior. In that case, mutation/negative-control evidence supplies the discrimination proof.

### 8. Product Lead review gate

Product Lead reviews the contract and executable-test mapping before implementation begins. Approval requires:

- every in-scope requirement is covered or explicitly dispositioned;
- tests assert product meaning rather than convenient implementation choices;
- passing tests would provide evidence of the promised outcome;
- named cheating implementations are rejected;
- required evidence and final artifacts are inspectable;
- missing capabilities lead to `BLOCKED`, not fabricated success;
- commands are executable in the target repository;
- QA ownership and the Test Change Request boundary are explicit.

Record the approval status and the immutable test-contract revision/hash. After approval, substantive changes require a Test Change Request.

### 9. Developer implementation loop

After approval:

```text
QA-owned acceptance suite approved
→ Developer writes production code and developer tests
→ Developer runs acceptance suite without changing it
→ failures route to Developer
```

If implementation reveals a product ambiguity, do not adapt the test informally. Route to Product Lead and update the PRD first if product meaning changes.

### 10. Independent QA execution

After implementation and after every code-review change that could affect behavior:

1. QA starts from a clean checkout/workspace.
2. QA verifies the approved contract revision/hash.
3. QA runs the full documented acceptance command.
4. QA checks collection counts and confirms no mandatory test was skipped, deselected, quarantined, or converted to expected failure.
5. QA opens and inspects required final artifacts/evidence.
6. QA confirms provenance belongs to this run and prohibited side effects did not occur.
7. QA issues exactly one verdict:
   - `PASS` — all mandatory properties and artifacts are verified;
   - `REQUEST_CHANGES` — implementation behavior violates an approved requirement;
   - `BLOCKED` — an external dependency or approved test seam prevents a valid verdict.

`PASS` does not authorize merge by itself. Code review and the project's human merge gate remain separate.

## Test Contract Output Template

Write `specs/stage-N-test-suite.md` with this structure:

```md
# Stage N Acceptance Test Suite: <Stage Name>

## 1. Authority and Lifecycle
- Product: `product.md`
- Stage Plan: `product-stages.md`
- PRD: `stage-N-prd.md` (revision/hash: ...)
- Technical Design: `stage-N-technical-design.md` (revision/hash: ...)
- QA Owner: ...
- Product Lead Reviewer: ...
- Status: Draft | Approved | Superseded
- Approved Contract Revision/Hash: ...
- Production Entrypoint: ...
- Full Acceptance Command: `...`

## 2. Scope and Acceptance Rule
- In scope: ...
- Out of scope: ...
- Mandatory pass rule: ...
- Skip/deselection rule: mandatory tests may not be skipped or omitted
- Verdicts: PASS | REQUEST_CHANGES | BLOCKED

## 3. Requirement Coverage Matrix
| PRD ID | Required Product Behavior | Acceptance Property | Test IDs | Evidence / Artifact | Status |
|---|---|---|---|---|---|

## 4. Acceptance Scenarios
### AT-SN-001: <Name>
- Requirement: ...
- Class: Normal | Blocked | Risk | Evidence | State | Boundary | Metamorphic | Repeatability | Holdout
- Priority: Mandatory | Advisory
- Given: ...
- When: ...
- Then: ...
- Required Evidence / Artifact: ...
- Negative Controls That Must Fail: ...
- Isolation / Provenance: ...
- Executable Test: `tests/acceptance/stage_N/...`
- Command: `...`

## 5. Negative-Control and Mutation Matrix
| Mutant / Cheating Implementation | Tests That Must Fail | Expected Failure Reason | Baseline Evidence |
|---|---|---|---|

## 6. Executable Test Mapping
| Test ID | Test File / Case | Command | Mandatory | Requirement IDs |
|---|---|---|---|---|

## 7. Runtime Evidence and Artifact Inspection
- Evidence locations: ...
- Fresh-run provenance method: ...
- Artifact inspection rules: ...
- Prohibited-side-effect observation: ...

## 8. Product Lead Approval
- Coverage: Complete | Incomplete
- Product fidelity: Pass | Request Changes
- Anti-cheating discrimination: Pass | Request Changes
- Executability: Pass | Blocked
- Decision: Approved | Request Changes | Blocked
- Reviewer / Date / Contract Hash: ...

## 9. Test Change Requests
| TCR ID | Reason | Requirement Impact | QA Decision | Product Lead Decision | New Hash |
|---|---|---|---|---|---|
```

## Completion Gate

This Skill is complete only when:

- both the test contract and executable acceptance tests exist;
- every in-scope PRD requirement is covered or explicitly dispositioned;
- each mandatory test maps to a requirement and exact command;
- critical negative controls are proven to fail against controlled bad behavior;
- test collection and skip/deselection policies are enforced;
- Product Lead has approved the contract revision/hash;
- QA ownership and Test Change Request rules are recorded;
- the suite can be rerun independently from a clean workspace.

If any condition is missing, report `Shared Understanding Reached: No` or `BLOCKED` with the exact missing decision, seam, dependency, or artifact. Do not label the stage acceptance-ready.

## Common Pitfalls

1. **Testing status labels instead of outcomes** — `completed` is not evidence; inspect the promised artifact/state.
2. **Encoding the current implementation as the oracle** — test PRD properties, not a fixed DAG or module structure.
3. **Letting QA write production code** — it destroys independence; route implementation failures to the developer.
4. **Letting the developer edit accepted tests** — use a Product Lead-approved Test Change Request.
5. **All-green pre-implementation suite** — prove discrimination with baseline failures or controlled mutants.
6. **Silent skips/deselection** — collection count and mandatory-test execution are part of acceptance.
7. **Fixture echoing** — vary inputs, use metamorphic/holdout cases, and verify result provenance.
8. **Stale artifact acceptance** — isolate runs and verify artifact timestamps/run IDs/content provenance.
9. **Live dependency confusion** — distinguish `BLOCKED` external dependency from `REQUEST_CHANGES` product failure.
10. **QA pass replacing code review** — product behavior and implementation quality remain separate gates.
