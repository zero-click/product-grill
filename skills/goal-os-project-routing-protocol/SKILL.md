---
name: goal-os-project-routing-protocol
description: Route Goal OS owners, callbacks, Human Gates, and notifications.
---

# Goal OS Multica Routing Protocol

Use only for Goal OS Project Lead routing. The authoritative workflow is `~/code/goal-os/dev-config/multica-routing.yaml`; this Skill defines transport and handoff behavior without duplicating stage semantics.

Normal professional stages are handed directly from the current Specialist to the canonical next Owner. Project Lead handles initial dispatch, Human Gate continuation, exception callbacks, merge routing and closeout; it is not a mandatory relay for every handoff.

## Dispatch

1. Resolve the current workflow step and canonical next Owner from the authoritative routing file.
2. Activate one execution Owner only.
3. Use a new, verified `mention://agent/<uuid>` comment. Plain `@name`, prose, metadata or editing an old comment is not dispatch.
4. A successful handoff contains only the artifact or PR URL, exact revision, status/verdict and the one next Owner mention.
5. Update `pipeline_status`, `waiting_on`, `waiting_on_agent_id` and `return_to_agent_id`; metadata records state but never substitutes for the mention.
6. Read back the newest comment and verify that it contains the intended Agent URI.

Do not hard-code Agent UUIDs in this Skill. Resolve current IDs from live workspace state.

## Callback

After a callback, perform exactly one action:

- evidence and exact revision satisfy the workflow Gate: route the canonical next Owner;
- professional artifact is deficient: `REQUEST_CHANGES` to the responsible Owner;
- external condition or required evidence is missing: `BLOCKED` with the condition needed to resume;
- Human Gate reached: stop automatic routing, notify the designated Product Owner and wait for explicit approval;
- workflow complete: run merge/closeout and notification steps.

A status summary without a valid next Owner or Human Gate pause is not a handoff.

## Verdict and Notification

- Specialist verdicts are routing inputs, not independent proof. Verify that the verdict binds to the current immutable candidate and required evidence.
- Product, Design, Stage Test Suite and PR/Merge Gates require a Human pause.
- Done, blocked, user-decision and Human Gate states require the configured out-of-band notification plus an auditable `notification sent` record.
- Only the designated Product Owner may approve a Human Gate or waive a mandatory standard.

Agent-to-Agent handoffs and Human Gate notifications are different interfaces. Keep the canonical Specialist handoff compact, but make every Human-facing notification decision-ready:

```text
结论：<能否推进；一句人话原因>
影响：<当前风险或被阻塞的结果>
需要你决定：<一个真正属于产品语义、范围、风险接受或权威的决定；无需决定则明确写“无需你操作”>

审查对象：<artifact / PR URL>
Revision：<exact immutable revision>
专业审查：<verdict + one-sentence rationale>
关键证据：<minimal reproducible evidence or link>
下一步：<owner + action after the decision>
```

Human-facing notifications use the designated stakeholder's established working language. For a Chinese stakeholder, conclusions, explanations, impact, and requested decisions are Chinese; preserve exact commands, paths, hashes, schema fields, API names, quoted errors, and machine verdicts.

Do not forward an untranslated Specialist report, one-line verdict, matrix, protocol dump, or implementation-option menu as the Human Gate packet. The Project Lead must explain the practical meaning in plain language, recommend the professional default, and ask the Human only when product meaning, scope, risk acceptance, or authority is genuinely unsettled. Internal implementation choices remain with the accountable Specialist.
