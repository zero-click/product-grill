# Stage Acceptance Test Design Implementation Plan

> **For Hermes:** Execute this plan task-by-task and verify every artifact before completion.

**Goal:** Add an independent lifecycle Skill that turns an approved stage PRD and technical design into a Product Lead-approved test contract plus executable QA-owned acceptance tests.

**Architecture:** Add a peer Skill named `stage-acceptance-test-design`. The Skill owns the lifecycle from requirement traceability and anti-cheating controls through executable tests, baseline mutation checks, Product Lead approval, independent QA execution, and controlled test-change requests. Repository tests inspect the Skill as a contract so its mandatory ownership, outputs, gates, and anti-cheating rules cannot silently regress.

**Tech Stack:** Markdown Skill, Python standard-library `unittest`, Git.

---

### Task 1: Add the lifecycle Skill

**Files:**
- Create: `skills/stage-acceptance-test-design/SKILL.md`

**Steps:**
1. Define exact inputs and lifecycle position after approved technical design and before implementation.
2. Define outputs `specs/stage-N-test-suite.md` and `tests/acceptance/stage_N/`.
3. Define PRD → test ID → executable test → evidence → artifact traceability.
4. Require normal, blocked/missing-capability, risk-boundary, outcome-evidence, anti-cheating, metamorphic, and repeatability coverage where applicable.
5. Require baseline/mutation proof that tests reject known cheating implementations before development.
6. Separate QA ownership, Product Lead approval, Developer implementation, and Code Reviewer bypass review.
7. Define post-implementation independent execution and Test Change Request flow.

### Task 2: Add executable contract regression tests

**Files:**
- Create: `tests/test_stage_acceptance_test_design_skill.py`

**Steps:**
1. Verify frontmatter and peer naming/output conventions.
2. Verify required inputs, outputs, lifecycle gates, and role separation.
3. Verify anti-cheating, negative-control, artifact, holdout/metamorphic, and no-skip requirements.
4. Verify the Skill demands runnable commands and implementation-neutral black-box assertions.

### Task 3: Verify and review

**Steps:**
1. Run `python3 -m unittest discover -s tests -v` and require zero failures.
2. Run a frontmatter parse and file-size validation using Python.
3. Inspect `git diff --check` and `git diff` against the approved scope.
4. Independently review whether a fixed DAG, fixed `completed`, invocation-only evidence, or weakened/skipped assertions could still satisfy the Skill.
5. Commit locally; do not push without Woosley approval.
