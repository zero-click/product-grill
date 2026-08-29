---
name: goal-os-spec-driven-flow
description: Define Goal OS stage ownership, evidence order, Gates, and rerouting.
---

# Goal OS Spec-Driven Delivery Flow

Use this Skill with `~/code/goal-os/dev-config/multica-routing.yaml`. The routing file is authoritative when stage wording differs. Approved specs remain authoritative for product meaning.

## Active roles

- **Project Lead** — Product Definition, Stage Design, state machine, Human Gates, notification, merge routing and closeout.
- **PRD Writer** — Stage PRD.
- **Product Reviewer** — independent Product/Stage/PRD contract review.
- **Varys** — architecture and Stage Technical Design.
- **Samwell** — QA-owned Stage Test Suite, executable acceptance tests, independent acceptance and regression.
- **Tywin** — production implementation and developer-owned unit/integration TDD.
- **Brienne** — independent architecture review, Stage Test Suite contract review and white-box PR/code/security review.

Legacy helper roles are outside the active delivery chain unless the Product Owner explicitly reactivates them.

## Canonical flow

1. Product Definition — Project Lead using `$product-grill`.
2. Stage Design — Project Lead using `$product-stage-design`.
3. Stage PRD — PRD Writer using `$prd-grill` and `$product-contract-gate` author evidence.
4. Product Review — Product Reviewer using `$product-contract-gate` independently.
5. Product Owner Product Gate — Project Lead pauses after its independent Gate Probe.
6. Stage Technical Design — Varys using `$tech-design-grill`.
7. Architecture Review — Brienne independently reviews the full design contract.
8. Product Owner Design Gate — Project Lead pauses.
9. Stage Test Suite and executable acceptance tests — Samwell using `$stage-acceptance-test-design`; baseline/negative proof is included where applicable.
10. Stage Test Suite Review — Brienne using `$test-contract-adversarial-review`, independent of Samwell.
11. Product Owner Stage Test Suite Gate — Project Lead pauses after Brienne approval; Project Lead does not issue a second content-review verdict.
12. TDD implementation — Tywin using `$design-driven-python-development`, without modifying the approved QA contract.
13. Developer quality Gate — Tywin records exact candidate revision and developer-owned evidence.
14. Independent QA acceptance — Samwell against the approved Test Suite and current candidate.
15. PR/code/security review — Brienne using `$code-review-grill` after QA PASS.
16. Review changes — Tywin → developer quality → Samwell regression → Brienne re-review.
17. Product Owner PR/Merge Gate — Project Lead pauses on exact approved HEAD.
18. Merge and closeout — Project Lead verifies merged artifact, final states and notification.

## Authority chain

```text
product.md
→ product-stages.md
→ stage-N-prd.md
→ stage-N-technical-design.md
→ stage-N-test-suite.md + tests/acceptance/stage_N/
→ implementation
```

The Stage Test Suite derives a verification contract from approved requirements; it cannot redefine product meaning. Production code implements the contract; it does not own the acceptance Oracle.

## Separation of duties

- Samwell owns acceptance design and verdict; Tywin may read/run it but cannot create, weaken, rewrite, delete, bypass or special-case the approved QA Oracle.
- Brienne reviews the Stage Test Suite independently; it must not rewrite Samwell's tests or provide Samwell's verdict.
- QA PASS and Brienne code review are independent. QA PASS must precede code review.
- Any review-driven implementation change invalidates the old QA PASS and Brienne approval; rerun developer quality, QA regression and Brienne review on the new exact revision.
- Project Lead validates routing state, revision alignment and Gate evidence; it does not reproduce specialist content review.

## Handoff rules

Use a new comment containing one verified `mention://agent/<uuid>` execution Owner. Do not hard-code Agent UUIDs; resolve the current live ID. Plain `@name`, prose, metadata, edited comments and “ready for next” are not dispatch.

Successful handoffs contain only artifact/PR locator, exact revision, verdict/status and the one next Owner. `REQUEST_CHANGES` may additionally list concrete defects with artifact locations. `BLOCKED` may additionally state the blocker and required decision.

## Evidence and Gate rules

- Fresh requirement-level evidence is required; process execution, exit code, self-report or green CI is never outcome evidence by itself.
- Scenario A success, Scenario B missing capability and Scenario C risk boundary require distinct causal Oracles. A success path cannot pass through Block, Skip, Unavailable or `missing_capability`.
- Every acceptance property needs a known-cheating negative control and executable mapping.
- Human Gate approval binds to an exact immutable revision. Changed specs, tests or code invalidate downstream approvals that depended on the old revision.
- No merge without current-head QA PASS, current-head Brienne approval and explicit Product Owner approval.
- Completion, blocker and user-decision states require out-of-band notification plus `notification sent` evidence.
