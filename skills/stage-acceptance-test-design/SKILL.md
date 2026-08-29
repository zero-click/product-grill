---
name: stage-acceptance-test-design
description: Design a stage's independent acceptance-test contract after requirements and technical design are approved and before implementation begins. Supports interactive clarification and headless draft generation when the user wants a complete acceptance specification and runnable black-box tests produced first for later review. Use when acceptance criteria must stay separate from developer tests, implementation claims need artifact-backed verification, or tests need anti-cheating controls before coding starts.
---

# Stage Acceptance Test Design

## Background

Developer tests prove that production code satisfies checks chosen during implementation. They do not prove that those checks represent the approved requirement, reject fake implementations, or inspect the real user-visible result.

This skill creates an independent acceptance lifecycle:

```text
approved requirements
-> approved technical design
-> acceptance-test contract and executable black-box tests
-> stakeholder approval
-> implementation
-> independent acceptance execution
-> acceptance decision
```

The acceptance contract is derived from approved requirements. It cannot add behavior, relax requirements, or become a competing source of truth.

For AI-generated implementation, the acceptance contract also acts as an executable objective function. A clear prose requirement is not protected unless the suite can distinguish the required behavior from plausible shortcuts, fabricated evidence, and superficially green completion.

## Requirement

Design and, when the repository is available, create the acceptance-test contract and runnable acceptance tests for one implementation stage.

Use the target project's existing names, paths, framework, and conventions. If the project already defines where specifications or acceptance tests live, follow that. Otherwise use clear defaults:

```text
specs/stage-N-acceptance-tests.md
tests/acceptance/stage_N/
```

Required inputs:

- approved requirements for the stage, with stable requirement IDs;
- approved technical design or an equivalent implementation approach;
- the production entrypoint or public boundary to exercise;
- the current codebase and test/runtime configuration, or an explicit greenfield baseline;
- any explicit non-goals, prohibited outcomes, permissions, side-effect limits, or external dependency constraints.

Stop and route backward when:

- requirements are missing, unapproved, contradictory, or lack stable IDs;
- the technical design is missing, unapproved, or exposes no observable way to verify a requirement;
- a proposed test would decide new behavior instead of verifying approved behavior;
- the runtime, entrypoint, or required dependency is inaccessible.

Finding repository/runtime facts is your job. Do not ask the user for facts you can inspect.

## Operating Modes

Use **Interactive Mode** unless the user asks for headless, batch, autonomous, draft-first, "no questions", or "just produce the doc".

In **Interactive Mode**, ask unresolved requirement, approval, or risk decisions one at a time with 2-4 choices and one recommendation.

In **Headless Mode**, do not stop to ask questions. Read the requirement and design sources, inspect the codebase/test runtime, choose the most defensible acceptance strategy, and produce the acceptance contract plus runnable tests or concrete test stubs in one pass. When a decision truly needs human confirmation, write it into the output under `Human Review Required` with:

- the decision that needs confirmation;
- the recommended answer;
- 2-4 alternatives and trade-offs;
- the downstream impact if the recommendation is wrong;
- whether execution is still possible before confirmation.

Mark uncertain assumptions inline as `Assumption` or `Needs Review`. Headless output is a reviewable draft until the approver accepts the contract.

## Ownership Model

Keep acceptance ownership independent from implementation:

| Role | Owns | Must Not Do |
|---|---|---|
| Acceptance Owner | Test contract, executable acceptance tests, fixtures, independent execution, acceptance verdict | Modify production code to make tests pass; approve their own interpretation of unclear requirements |
| Approver | Requirement meaning, coverage approval, accepted-test changes | Delegate acceptance meaning to the implementer |
| Implementer | Production code and developer-owned unit/integration tests | Weaken, delete, skip, special-case, or silently modify approved acceptance tests |
| Test Contract Reviewer | Independent coverage, claim-to-implementation alignment, whole-contract consistency, and material probes | Rewrite the acceptance contract or treat the author's claims as proof |
| Code Reviewer | Implementation quality and checks for test bypass or tampering | Treat acceptance pass as a substitute for code review |

The implementer may read and run acceptance tests. If a test is wrong or impossible, they submit a test change request. The acceptance owner evaluates it, and the approver accepts or rejects any substantive change before the approved suite changes.

## Process

### 1. Establish the acceptance baseline

Before asking questions:

1. Read the canonical requirement and design documents.
2. Inventory every in-scope required behavior and explicit prohibited outcome.
3. Inspect the production boundary, runtime/tool availability, fixtures, existing tests, and CI commands.
4. Identify observable outputs, state transitions, errors, external effects, and final artifacts.
5. Separate requirement facts from implementation choices.

Do not ask the user for facts you can discover from the repository or runtime.

### 2. Define acceptance properties before examples

For each requirement, state the externally observable property that must hold. Prefer properties over implementation-shaped assertions.

Bad:

```text
The workflow must call StepA, then StepB, then StepC.
```

Good:

```text
The public entrypoint produces the required artifact from valid input, and missing required capabilities result in an honest blocked/failure state rather than fabricated completion.
```

A test may assert an exact value only when the approved requirement requires that value. Do not hard-code a class, module, database table, prompt, internal step order, or agent count merely because the current design uses it.

For every mandatory property, define both:

- a **positive oracle** that proves the required observable outcome; and
- a **falsification oracle** that proves the suite rejects absence, substitution, mutation, bypass, or fabrication of the claimed capability.

Be precise about observable truth and permissive about implementation. The falsification oracle may perturb a component or boundary named by the approved design when that perturbation is necessary to prove causal contribution; it must not require one arbitrary internal implementation.

### 3. Build requirement traceability

Every in-scope requirement must map through this chain:

```text
requirement ID
-> acceptance property
-> test ID
-> executable test path and command
-> runtime evidence
-> final artifact or observable outcome
```

Use explicit statuses for uncovered requirements:

- `COVERED` - executable acceptance coverage exists;
- `HUMAN_EVALUATION` - judgment is necessary and evaluator/evidence are named;
- `BLOCKED` - an executable seam or dependency is missing;
- `NOT_APPLICABLE` - approved rationale is present.

Never silently omit a requirement.

Also maintain a machine-readable or consistently structured **QA Claim Ledger** for reviewer handoff. Each material claim states what the acceptance owner believes the contract proves and where that proof is implemented:

```yaml
claim_id: TC-...
approved_source:
  - <requirement/design/ADR locator>
intended_purpose: <what the test is meant to prove>
implementation:
  test_ids: [AT-...]
  test_files: [path/to/test]
  production_boundary: <public entrypoint or named boundary>
expected_positive: <observable result that must pass>
expected_negative: <wrong behavior that must fail>
command: <exact non-interactive command>
evidence: <artifact or machine-result location>
```

The ledger is an author claim and navigation aid. It cannot prove coverage, test behavior, or approval by itself.

### 4. Design the minimum sufficient scenario set

Cover these classes where applicable:

1. Normal outcome - the production entrypoint produces the required user-visible result.
2. Blocked or missing capability - unavailable tools, permissions, dependencies, or inputs cause an honest blocked/failure state.
3. Risk boundary - prohibited, unauthorized, paid, destructive, or externally published behavior does not occur.
4. Outcome evidence - completion requires the real artifact/content/state, not only logs or labels.
5. State consistency - step states and top-level terminal state cannot contradict each other.
6. Boundary and recovery - limits, invalid input, retry/resume, idempotency, and partial failure follow the requirement/design.
7. Metamorphic behavior - meaningful input or constraint changes produce corresponding output changes.
8. Repeatability - isolated repeated runs do not pass because of stale artifacts or shared state.
9. Holdout coverage - when template or keyword hard-coding is a material risk, keep representative cases outside developer-visible fixtures or generate them at run time.

Do not add a category just to fill a template. Each included test must trace to a requirement, explicit risk, or design invariant.

### 5. Define negative controls

For every mandatory acceptance property, answer:

```text
What clearly wrong implementation could still pass this test?
```

List concrete negative controls. At minimum, consider:

- unconditional success responses;
- process invocation without the required result;
- fake or stale artifact from a previous run;
- capability declaration without a reachable tool, permission, or runtime;
- echoing fixture data or a precomputed expected result;
- empty, placeholder, malformed, or unverifiable output;
- skipped, deselected, quarantined, or expected-failure tests counted as pass;
- top-level success while required work is pending or failed;
- code paths that detect acceptance fixtures and special-case them.

When a requirement claims that a capability or component contributes to an outcome, also consider:

- **deletion/disable control** - remove or disable the claimed capability and require honest failure or blocking;
- **mutation control** - alter the capability or its output and require the final outcome to fail validation or change correspondingly;
- **bypass control** - prevent the intended capability path while leaving a convenient host/framework shortcut available, and require the shortcut not to satisfy acceptance;
- **provenance recomputation** - independently recalculate hashes, derived values, invocation relationships, or artifact lineage instead of trusting reported evidence fields;
- **fresh holdout/metamorphic control** - vary material inputs or constraints using a case that is not encoded as a production template, fixed expected-value table, or developer-visible special case.

A negative control is valid only if the acceptance suite rejects it for the intended reason.

### 6. Write executable tests before implementation

Create tests using the project's existing acceptance-test framework. If no convention exists, place them under:

```text
tests/acceptance/stage_N/
```

Rules:

- exercise the production entrypoint or approved public boundary;
- isolate each run in a new temporary workspace or state store;
- construct or copy fixtures explicitly;
- assert artifacts and external behavior, not private implementation details;
- verify provenance when stale or prebuilt artifacts are possible;
- verify prohibited side effects by observing the relevant boundary;
- fail on unexpected `skip`, `xfail`, deselection, timeout suppression, or missing test collection;
- emit useful failure evidence without leaking secrets;
- avoid network dependence unless approved requirements make a live external source part of acceptance;
- when live dependencies are required, distinguish dependency failure (`BLOCKED`) from implementation failure (`REQUEST_CHANGES`).

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

Before approval and before production implementation:

1. Run the suite against the current baseline, an intentionally incomplete seam, or controlled mutants.
2. Exercise the named cheating implementations through dependency injection, test doubles, fixture variants, or temporary mutations without committing them to production.
3. Record which test rejects each mutant and why.
4. Restore the baseline and verify the working tree.

At least the critical negative controls must produce the expected failures. A suite that only demonstrates green results has not established that its assertions discriminate correct from fake behavior.

If any materially wrong implementation or controlled mutant still passes, treat the acceptance contract itself as defective. Correct and reapprove the oracle before using it to judge the implementation; do not preserve a green verdict and merely add a future test.

Do not require all tests to be red when the repository already contains valid behavior. In that case, mutation or negative-control evidence supplies the discrimination proof.

### 8. Independent review and approval gate

Before stakeholder approval, an independent Test Contract Reviewer reviews the exact candidate revision without rewriting it. The reviewer derives approved obligations independently, checks Design-to-Claim coverage, traces every material Claim through executable tests and actual production boundaries, checks whole-contract consistency, and uses narrow reviewer probes where trust, permission, provenance, fabricated completion, or high-impact bypass claims need corroboration.

The reviewer returns `APPROVED`, `REQUEST_CHANGES`, or `BLOCKED`. Reviewer `APPROVED` means only that the exact Test Contract revision may enter the stakeholder/human approval gate.

The approver then reviews the contract, reviewer evidence, and executable-test mapping before implementation begins. Approval requires:

- every in-scope requirement is covered or explicitly dispositioned;
- tests assert approved behavior rather than convenient implementation choices;
- passing tests would provide evidence of the promised outcome;
- named cheating implementations are rejected;
- required evidence and final artifacts are inspectable;
- missing capabilities lead to `BLOCKED`, not fabricated success;
- commands are executable in the target repository;
- ownership and test-change boundaries are explicit.

Record the approval status and the immutable test-contract revision/hash. After approval, substantive changes require a test change request.

### 9. Implementation and independent execution

After approval:

```text
approved acceptance suite
-> implementer writes production code and developer tests
-> implementer runs acceptance suite without changing it
-> independent acceptance owner reruns the approved suite
-> verdict
```

If implementation reveals a requirement ambiguity, do not adapt the test informally. Route the ambiguity to the approver and update the requirement source first if approved meaning changes.

The independent run must:

1. start from a clean checkout/workspace;
2. verify the approved contract revision/hash;
3. run the full documented acceptance command;
4. check collection counts and confirm no mandatory test was skipped, deselected, quarantined, or converted to expected failure;
5. inspect required final artifacts/evidence;
6. confirm provenance belongs to this run and prohibited side effects did not occur;
7. execute the approved causal deletion/mutation/bypass controls where causal contribution is material;
8. execute at least one fresh holdout or metamorphic case when hard-coding, fixture echoing, or template overfitting is a material risk;
9. invalidate the suite and route it for correction if a known-false implementation can still pass;
10. issue exactly one verdict:
   - `PASS` - all mandatory properties and artifacts are verified;
   - `REQUEST_CHANGES` - implementation behavior violates an approved requirement;
   - `BLOCKED` - an external dependency or approved test seam prevents a valid verdict.

`PASS` does not authorize merge by itself. Code review and the project's merge gate remain separate.

## Output

Write an acceptance-test contract with this structure, adapting file names to the project:

```md
# Stage N Acceptance Test Suite: <Stage Name>

## 1. Authority and Lifecycle
- Requirement Source(s): ...
- Technical Design Source: ...
- Acceptance Owner: ...
- Approver: ...
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
| Requirement ID | Required Behavior | Acceptance Property | Test IDs | Evidence / Artifact | Status |
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
- Executable Test: `...`
- Command: `...`

## 5. Negative-Control and Mutation Matrix
| Mutant / Cheating Implementation | Tests That Must Fail | Expected Failure Reason | Baseline Evidence |
|---|---|---|---|

## 6. Executable Test Mapping
| Test ID | Test File / Case | Command | Mandatory | Requirement IDs |
|---|---|---|---|---|

## 7. QA Claim Ledger
```yaml
- claim_id: TC-...
  approved_source: [...]
  intended_purpose: ...
  implementation:
    test_ids: [...]
    test_files: [...]
    production_boundary: ...
  expected_positive: ...
  expected_negative: ...
  command: ...
  evidence: ...
```

## 8. Runtime Evidence and Artifact Inspection
- Evidence locations: ...
- Fresh-run provenance method: ...
- Artifact inspection rules: ...
- Prohibited-side-effect observation: ...

## 9. Independent Test Contract Review
- Reviewed Candidate Revision: ...
- Design-to-QA Coverage Matrix: ...
- QA-Claim-to-Implementation Matrix: ...
- Whole-Contract Findings: ...
- Reviewer Probe Evidence: ...
- Reviewer Verdict: APPROVED | REQUEST_CHANGES | BLOCKED

## 10. Human Approval
- Coverage: Complete | Incomplete
- Requirement fidelity: Pass | Request Changes
- Anti-cheating discrimination: Pass | Request Changes
- Executability: Pass | Blocked
- Decision: Approved | Request Changes | Blocked
- Approver / Date / Contract Hash: ...

## 11. Human Review Required
| Decision | Recommendation | Alternatives | Impact If Wrong | Can Execute Before Confirmation? |
|---|---|---|---|---|
| <decision needing human confirmation> | <recommended answer> | <2-4 options> | <what changes downstream?> | Yes / No |

## 12. Test Change Requests
| TCR ID | Reason | Requirement Impact | Acceptance Owner Decision | Approver Decision | New Hash |
|---|---|---|---|---|---|
```

Also create or specify the runnable acceptance tests and the exact non-interactive command to execute them.

## Completion Gate

This skill is complete only when:

- the test contract and executable acceptance tests both exist, or a specific blocker explains why they cannot;
- every in-scope requirement is covered or explicitly dispositioned;
- each mandatory test maps to a requirement and exact command;
- the QA Claim Ledger maps every material claim to approved authority, executable tests, production boundary, positive/negative behavior, command, and evidence;
- critical negative controls are proven to fail against controlled bad behavior;
- test collection and skip/deselection policies are enforced;
- the exact candidate revision and all review inputs are ready for independent Test Contract Review;
- Interactive Mode: unresolved requirement or risk decisions are either settled by the approver or listed in `Human Review Required`;
- Headless Mode: all decisions requiring confirmation are listed in `Human Review Required`;
- ownership and test change request rules are recorded;
- the suite can be rerun independently from a clean workspace.

At this point the acceptance owner may declare `READY_FOR_TEST_CONTRACT_REVIEW`, not stakeholder approval. The stage becomes acceptance-ready only after the independent reviewer approves the exact revision and the stakeholder/human gate records approval.

If any condition is missing, report `BLOCKED` with the exact missing decision, seam, dependency, or artifact. Do not label the stage acceptance-ready.

## Common Pitfalls

1. Testing status labels instead of outcomes - `completed` is not evidence; inspect the promised artifact/state.
2. Encoding the current implementation as the oracle - test approved properties, not a fixed internal structure.
3. Letting the acceptance owner write production code - it destroys independence; route implementation failures to the implementer.
4. Letting the implementer edit accepted tests - use an approved test change request.
5. All-green pre-implementation suite - prove discrimination with baseline failures or controlled mutants.
6. Silent skips/deselection - collection count and mandatory-test execution are part of acceptance.
7. Fixture echoing - vary inputs, use metamorphic/holdout cases, and verify result provenance.
8. Stale artifact acceptance - isolate runs and verify artifact timestamps/run IDs/content provenance.
9. Live dependency confusion - distinguish `BLOCKED` external dependency from `REQUEST_CHANGES` implementation failure.
10. Acceptance pass replacing code review - approved behavior and implementation quality remain separate gates.
11. Evidence-shape acceptance - a file, status, invocation record, or signed claim is not proof unless its content and causal provenance are independently checked.
12. Retrofitting after a false PASS - when a cheating implementation passes, reopen and correct the acceptance contract first; do not keep the old PASS while treating the missing oracle as optional future coverage.
