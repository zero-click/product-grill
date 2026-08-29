---
name: goal-os-codex-command-surface
description: Map Goal OS stages to verified Codex command surfaces.
---

# Goal OS Codex Command Surface

Use this Skill to select an installed Codex/ECC/BMAD/Superpowers command for each Goal OS stage. The command must exist on the selected runtime; do not assume a Claude slash command is available when the Agent runtime is Codex.

## Product / PRD

- `ecc-plan-prd`
- `ecc-prp-prd`
- `bmad-create-prd`
- `bmad-validate-prd`

## Architecture / Specification

- `ecc-prp-plan`
- `bmad-create-architecture`
- `bmad-check-implementation-readiness`

## Development / TDD

- `ecc-feature-dev`
- `ecc-prp-implement`
- `tdd-workflow`
- `test-driven-development`
- `writing-plans`
- `executing-plans`

## Verification / Review

- `ecc-quality-gate`
- `ecc-code-review`
- `ecc-review-pr`
- `verification-loop`
- `verification-before-completion`
- `requesting-code-review`
- `security-review`

## Discovery

Expected locations:

- ECC Codex prompts: `~/.codex/prompts/ecc-*.md`
- BMAD prompt shims: `~/.codex/prompts/bmad-*.md`
- Codex Skills: `~/.codex/skills/`
- Agent Skills: `~/.agents/skills/`

Resolve the installed command at runtime. If the required command or file is missing, return `BLOCKED` with the exact missing command/path; do not invent an equivalent workflow or claim it ran.
