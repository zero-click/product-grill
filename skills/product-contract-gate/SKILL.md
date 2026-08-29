---
name: product-contract-gate
description: Goal OS shared method for Product/Stage/PRD contract evidence, independent review, and Project Lead Product Gate probing.
---

# Product Contract Gate

Use this skill whenever a Goal OS Product Definition, Stage Design, or Stage PRD is authored, reviewed, or advanced to Product Owner Product Gate.

This is an evidence method, not a new canonical product spec. The canonical chain remains:

```text
specs/product.md -> specs/product-stages.md -> specs/stage-N-prd.md
```

## Evidence Format

Use fenced YAML blocks as the primary parser-friendly format in Multica comments. Human prose may introduce or explain the YAML, but the YAML is the evidence the validator reads.

Canonical issue evidence should use `specs/product.md`, `specs/product-stages.md`, and `specs/stage-N-prd.md` in read-order fields. Synthetic validator fixtures may keep those files at fixture root as `product.md`, `product-stages.md`, and `stage-2-prd.md`; the validator normalizes those fixture-root paths to the canonical contract shape.

## Author Contract

Product, Stage, and PRD authors submit:

```yaml
decision_preservation_ledger:
  verdict: READY_FOR_REVIEW # or BLOCKED
  rows:
    - decision_source: "issue comment or canonical section"
      preserved_semantic: "product meaning that must remain true"
      forbidden_opposite_or_weakened_interpretation: "what the docs must make impossible"
      canonical_landing: "canonical path/section, or MISSING"
      unresolved_gap: "NONE, or the remaining conflict/missing landing"
      owner_to_close: "NONE, or correct owner"
```

Rules:

- Product Owner decisions cannot be reframed as safer compromises, conditional permission, or future options without an explicit new decision.
- `unresolved_gap` other than `NONE` blocks review-ready routing.
- PRD Writer finding Product Definition or Stage Design conflict must return `BLOCKED` to Project Lead, not reinterpret it downstream.

## Reviewer Contract

Product Reviewer submits an independently authored matrix:

```yaml
product_contract_consistency_matrix:
  reviewer_verdict: APPROVED # or REQUEST_CHANGES / BLOCKED
  rows:
    - row_id: authority_status_consistency
      document_references: ["specs/product.md", "specs/product-stages.md"]
      conclusion: "reviewer judgment"
      counterexample: "plausible wrong interpretation or why none applies"
      verdict: PASS # PASS / FAIL / NOT_APPLICABLE
      owner_if_fail: "NONE, or correct owner"
```

Mandatory `row_id` values:

- `authority_status_consistency`
- `product_to_stage_to_prd_scope_consistency`
- `lifecycle_state_determinism`
- `requirement_priority_to_mandatory_entry_exit_consistency`
- `default_permission_to_risk_boundary_to_user_flow_consistency`
- `non_goal_to_supported_flow_consistency`
- `open_decisions_to_claimed_readiness_consistency`
- `language_reviewability_convention`
- `strongest_counterexample`

Rules:

- Every row needs references, conclusion, counterexample, verdict, and owner_if_fail.
- Any mandatory `FAIL`, missing row, empty reference, or unresolved evidence makes `APPROVED` invalid.
- The strongest counterexample row must state the most plausible wrong implementation or product interpretation still at risk, and how the documents exclude it.
- File lists, Requirement ID counts, "reviewed", "consistent", and "no blocker found" are not substitutes.

## Project Lead Contract

Before Product Owner Product Gate, Project Lead submits:

```yaml
project_lead_gate_probe:
  authority_preflight:
    issue: "ZER-..."
    worktree: "persistent issue worktree"
    branch: "branch"
    head: "current HEAD"
    status: "clean or dirty with explanation"
    required_files: ["specs/product.md", "specs/product-stages.md", "specs/stage-N-prd.md"]
    read_order: ["specs/product.md", "specs/product-stages.md", "specs/stage-N-prd.md"]
  ledger_probe:
    selected_row: "ledger row reference"
    canonical_reference: "canonical section checked"
    forbidden_opposite_still_allowed: false
    conclusion: "independent judgment"
  cross_document_invariant_probe:
    invariant: "invariant checked"
    document_references: ["specs/product.md", "specs/stage-N-prd.md"]
    conclusion: "independent judgment"
  reviewer_matrix_integrity:
    mandatory_rows_complete: true
    references_non_empty: true
    verdict_matches_evidence: true
    conclusion: "integrity judgment"
  strongest_remaining_counterargument: "strongest remaining risk, or why closed"
  gate_decision: ADVANCE # ADVANCE / REJECT_REVIEW_VERDICT / BLOCKED
```

Rules:

- Reviewer `APPROVED` is input only.
- Missing probe evidence or reviewer verdict/evidence mismatch requires `REJECT_REVIEW_VERDICT`.
- Product/process decision needed requires `BLOCKED`.
- Product Owner Product Gate packet is allowed only after `gate_decision: ADVANCE`.
- Old approvals are stale after this gate change; re-review paused issues with a new matrix and new Gate Probe.
