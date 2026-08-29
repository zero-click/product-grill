# Feedback Event Schema

每个事件描述一个可核验的“原判断 → 后续结果”，不直接等同于 Skill 教训。

```yaml
feedback_event:
  issue:
    key: <issue key>
    url: <direct URL>
  actor:
    role: <agent role>
    run_id: <run ID>
    skill_name: <base skill>
    skill_revision: <version or SHA-256>
  original_claim:
    verdict: <claim/verdict>
    artifact_revision: <HEAD/hash/version>
    evidence_locator: <comment/artifact/run message>
  outcome:
    status: CONFIRMED | OVERTURNED | PARTIAL | UNRESOLVED
    decided_by: PRODUCT_OWNER | DIRECT_SOURCE | DOWNSTREAM_AGENT | NONE
    evidence_locator: <direct source>
  observed_gap: <what the original method failed to do>
  impact: <wrong gate / escaped defect / false blocker / rework / idle issue>
  candidate_attribution:
    class: BASE_SKILL | WORKFLOW | PLATFORM | PRODUCT_DECISION | ONE_OFF
    target: <skill/workflow/component or NONE>
    confidence: CONFIRMED | PROBABLE | UNRESOLVED
  candidate_invariant: <general rule without issue-specific identifiers>
```

## Validity rules

- `skill_revision` and `artifact_revision` are mandatory for verdict-related feedback.
- `OVERTURNED` requires a direct evidence locator; a later opinion alone is insufficient.
- `UNRESOLVED` cannot produce a Skill patch.
- `PRODUCT_DECISION` must preserve the Human decision as authority, not convert it into a professional rule before settlement.
- Raw events stay in Issue/PR history or eval fixtures; only generalized invariants enter `SKILL.md`.
