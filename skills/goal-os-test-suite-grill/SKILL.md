---
name: goal-os-test-suite-grill
description: Legacy Goal OS test-suite Skill; migrate to stage-acceptance-test-design.
---

# Goal OS Test Suite Grill — Deprecated

This Skill is retained only as a migration marker. It must not be assigned to new Agents or used as the acceptance-test authority.

Use instead:

- `$stage-acceptance-test-design` for Samwell's QA-owned Stage Test Suite and executable acceptance Oracle;
- `$test-contract-adversarial-review` for Brienne's independent Test Suite contract review;
- `$goal-os-spec-driven-flow` for ownership, Human Gate and routing order.

If invoked directly, return `BLOCKED_LEGACY_SKILL` and request migration to the current Skills. Do not interview the Product Owner, create skipped placeholder acceptance tests, let Project Lead issue a content-review verdict, or let Developer modify the QA Oracle.
