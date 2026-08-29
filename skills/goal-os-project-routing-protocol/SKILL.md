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
