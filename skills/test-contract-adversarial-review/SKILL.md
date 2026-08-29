---
name: test-contract-adversarial-review
description: Independently review a QA-authored acceptance-test contract before implementation without rewriting the tests. Use when a reviewer must prove approved design obligations are covered, trace each QA claim through executable tests and production boundaries, check whole-contract consistency, run narrow adversarial probes, and return APPROVED, REQUEST_CHANGES, or BLOCKED for a human test-suite gate.
---

# Test Contract Adversarial Review

## Purpose

Review whether a QA-authored acceptance contract can distinguish the approved behavior from plausible false implementations. This is a reviewer workflow, not a second test-authoring workflow.

The QA owner's claim ledger, baseline failures, mutation results, and positive evidence are review inputs. None is self-authenticating.

## Boundary

Keep the review independent and read-only:

- Do not write or redesign the acceptance contract, executable tests, fixtures, production code, or approved requirements.
- Do not invent new product semantics, acceptance conditions, or implementation choices.
- Do not merely repeat the QA owner's checklist or rerun every QA command.
- Use reviewer probes only to test a material claim already made by QA.
- Route test-contract defects to the QA owner; route missing or contradictory product/design authority to the accountable lead.

## Required Inputs

Require all of the following for one exact candidate revision:

- approved product/stage requirements with stable IDs;
- approved technical design and accepted architecture decisions;
- complete Stage Test Suite or equivalent acceptance contract;
- complete executable acceptance tests, fixtures, gates, and helpers;
- authoritative base and exact current candidate revision;
- QA Claim Ledger;
- baseline RED, negative-control, mutation, or bypass evidence;
- exact non-interactive commands and machine results.

Return `BLOCKED` when authority, provenance, revision identity, executable inputs, or access is insufficient for a trustworthy review.

## QA Claim Ledger Contract

Treat each claim as an author assertion to verify, not an approval token. Each material claim should provide:

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

Missing fields are findings only when they prevent traceability or verification. Do not reject harmless formatting differences.

## Review Method

### 1. Lock the candidate

Record the approved input revisions, authoritative base, exact candidate revision, worktree identity, and changed files. Review the complete candidate and complete base-to-current diff, including added, modified, renamed, and deleted files.

A dirty worktree, unresolved revision, mismatched HEAD, stale evidence, or partial diff is `BLOCKED`.

### 2. Direction A — Design to QA Claims

Independently enumerate the approved obligations that acceptance must prove:

- mandatory user-visible requirements;
- critical design and architecture obligations;
- security, permission, trust, and side-effect boundaries;
- failure, blocked, retry, resume, migration, or compatibility behavior;
- evidence and provenance obligations needed to reject fabricated completion.

Map each obligation to QA Claim IDs:

```text
approved obligation -> QA claim IDs -> COVERED | MISSING | BLOCKED
```

This direction prevents an author from omitting an important obligation and then presenting a complete-looking claim list.

Do not create a new acceptance condition. Every obligation must cite approved authority.

### 3. Direction B — QA Claim to Implementation

For every material claim, verify:

1. **Purpose alignment** — `intended_purpose` matches the cited approved authority and does not weaken or extend it.
2. **Implementation alignment** — trace:

```text
Claim
-> Test ID
-> fixture/input
-> executable entrypoint
-> production boundary and actual code path
-> assertion/oracle
-> machine result and artifact
```

3. **Falsification strength** — the negative oracle rejects absence, mutation, substitution, bypass, fixture echo, stale artifact, or fabricated evidence for the intended reason.
4. **Evidence provenance** — the evidence belongs to the exact candidate and current run; reported fields are recomputed or corroborated where material.

A test name, docstring, author explanation, green exit code, test count, status label, or evidence-shaped file cannot substitute for this trace.

### 4. Whole-contract consistency

Review the Stage Test Suite, executable tests, fixtures, helpers, gate CLI, evidence semantics, and affected production boundaries as one contract. Check whether:

- claims contradict, duplicate, shadow, or bypass one another;
- normal-success tests can accidentally pass through blocked/skip/unavailable branches;
- a local fix weakens unrelated approved behavior, compatibility, or failure semantics;
- collection, skip, xfail, deselection, timeout, and test-discovery rules preserve mandatory coverage;
- shared fixtures or helpers silently decide unapproved product meaning;
- the contract remains implementation-permissive while outcome-precise;
- ownership and test-change boundaries remain intact.

A point fix passing its named regression is insufficient if the complete contract becomes less trustworthy.

### 5. Reviewer probes

Run the smallest practical independent probe for material claims involving:

- trust roots or evidence provenance;
- authorization or side-effect boundaries;
- fabricated completion or stale artifacts;
- high-impact bypasses;
- a negative control whose observed result is ambiguous.

A probe may be a code-path trace, recomputation, controlled input variation, or deletion/mutation/replacement/bypass experiment. Record the exact command or procedure and observed result.

The probe validates the QA owner's stated purpose. It must not become a reviewer-authored replacement acceptance test or add product semantics.

### 6. Findings and ownership

Every blocking finding includes:

- severity: `Critical` or `Important`;
- exact file, line, claim, requirement, or artifact location;
- violated approved obligation or review invariant;
- observable failure and impact;
- evidence;
- required correction condition;
- owner: QA contract owner, product/design owner, or accountable lead.

Minor findings may accompany approval when they do not weaken contract trustworthiness.

## Output

Produce these four artifacts in the review report.

### A. Design-to-QA coverage matrix

| Approved Obligation | Authority | QA Claim IDs | Status | Evidence / Finding |
|---|---|---|---|---|
| ... | ... | ... | COVERED / MISSING / BLOCKED | ... |

### B. QA-Claim-to-implementation matrix

| Claim ID | Purpose Alignment | Implementation Alignment | Falsification Strength | Global Consistency | Reviewer Probe | Verdict |
|---|---|---|---|---|---|---|
| ... | PASS / FAIL / BLOCKED | PASS / FAIL / BLOCKED | PASS / FAIL / BLOCKED | PASS / FAIL / BLOCKED | command + observed result / Not Required | PASS / FAIL / BLOCKED |

### C. Whole-contract findings

List validated Critical, Important, and Minor findings with owner and correction condition. Use `None` when a severity has no findings.

### D. Revision-bound verdict

Return exactly one:

- `APPROVED` — every critical approved obligation is covered; all material claims align with approved authority and actual executable behavior; material falsification controls discriminate; no unresolved Critical or Important whole-contract finding remains.
- `REQUEST_CHANGES` — the acceptance contract, tests, fixtures, helpers, gates, or evidence contain a validated Critical or Important defect owned by QA.
- `BLOCKED` — missing/contradictory approved authority, inaccessible inputs, candidate mismatch, dirty state, or untrustworthy provenance prevents a valid review.

State the exact reviewed candidate revision. Approval means only that this revision may enter the human test-suite gate; it does not approve human decisions or authorize implementation.

## Anti-Patterns

- Rewriting the QA owner's acceptance conditions and calling that independent review.
- Reviewing only claims QA chose to list, without deriving coverage from approved design.
- Trusting a claim ledger because it is structured.
- Treating an external file path as a trust boundary when QA can write the same path.
- Running the full QA suite and calling duplicated execution independent review.
- Designing holdouts that add requirements not present in approved authority.
- Approving a local correction without checking the complete contract and affected regression surface.
- Treating a previous approval as valid after the candidate revision changes.
