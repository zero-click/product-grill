# Agent Skill Coach Implementation Plan

> **For Hermes:** Execute task-by-task and verify repository and live Multica states separately.

**Goal:** Add a canonical Agent Coach Skill and complete Goal OS Agent↔Base Skill bindings from the `product-grill` repository.

**Architecture:** `product-grill` owns reusable Skill source and eval cases. Multica owns deployed copies and assignments. Goal OS Agent instructions explicitly load assigned Skills; Coach may create Skill PRs but never merge or deploy them.

**Tech Stack:** Markdown Skills, JSON eval fixtures, Multica CLI, SHA-256 read-back verification.

---

### Task 1: Canonicalize the shared Product Contract Gate

**Files:**
- Create: `skills/product-contract-gate/SKILL.md`

**Steps:**
1. Export the current live Multica Skill content.
2. Write the exact content under `product-grill/skills/`.
3. Validate frontmatter and compare source/live SHA-256.

### Task 2: Create Agent Skill Coach

**Files:**
- Create: `skills/agent-skill-coach/SKILL.md`
- Create: `skills/agent-skill-coach/references/feedback-event-schema.md`
- Create: `skills/agent-skill-coach/references/role-skill-map.md`
- Create: `skills/agent-skill-coach/evals/evals.json`
- Create: `agents/skill-coach/instructions.md`

**Steps:**
1. Define evidence intake and direct-source hierarchy.
2. Define attribution among Skill, workflow, product decision and one-off issue state.
3. Require one-Skill minimal patch, failure replay and holdout replay.
4. Block live sync, merge and self-approval.
5. Add deterministic eval fixtures covering correct attribution and unsafe overreach.

### Task 3: Update canonical inventory

**Files:**
- Modify: `README.md`
- Create: `config/goal-os-skill-bindings.json`

**Steps:**
1. List all canonical Skills including Coach and Product Contract Gate.
2. Record name-based Agent bindings without personal IDs.
3. Validate JSON and Skill references.

### Task 4: Update Goal OS instruction snapshots

**Files:**
- Modify: `goal-os/dev-config/agents/goal-os-project-lead/instructions.md`
- Modify: `goal-os/dev-config/agents/goal-os-prd-writer/instructions.md`
- Modify: `goal-os/dev-config/agents/goal-os-product-reviewer/instructions.md`

**Steps:**
1. Replace filesystem-only Skill use with explicit `$skill-name` loading.
2. Add `BLOCKED` behavior when an assigned Skill is unavailable.
3. Preserve role boundaries, routing and Human Gates.
4. Diff-check all three complete instructions.

### Task 5: Validate and package

**Steps:**
1. Run Skill structural validation for every canonical Skill.
2. Run Coach eval assertions.
3. Package new/missing Skills.
4. Compute canonical SHA-256 values.

### Task 6: Sync Multica

**Steps:**
1. Import/update `product-grill`, `product-stage-design`, `prd-grill`, `product-contract-gate`, and `agent-skill-coach`.
2. Create `Skill Coach` on the online Codex runtime with one-task concurrency.
3. Set exact Skill assignments for Project Lead, PRD Writer, Product Reviewer and Coach while preserving required existing workflow Skills.
4. Sync the three updated Agent instructions.

### Task 7: Verify live state

**Steps:**
1. Read back every changed Skill and compare content SHA-256 with canonical source.
2. Read back every changed Agent instruction and compare with snapshot.
3. Verify exact Agent↔Skill assignments.
4. Confirm no unexpected Agent or Skill assignment changed.
5. Report repository state separately from live Multica state.
