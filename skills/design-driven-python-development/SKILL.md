---
name: design-driven-python-development
description: Implement approved Python features and fixes from a technical design and immutable acceptance contract using modular boundaries, developer-owned pytest TDD, repository-defined quality gates, and revision-bound evidence. Use for non-trivial Python implementation after design and test-contract approval; do not use to invent requirements, redesign architecture, author acceptance tests, or perform independent review.
metadata:
  origin: ECC-derived
  upstream_repository: affaan-m/everything-claude-code
  upstream_commit: 656d4b5746413e4e78f9c62cb34d686515931f4f
  upstream_sources:
    python-patterns: 103e0130dac33a49d26705fc5a2df804980fcab6a0138d65bc7f370a987d49f6
    python-testing: b9f7a158dae3b6c06c9c75ffe84e27a1edc86092d2afdcb39e96fc2569902eb7
    hexagonal-architecture: 1579f70e4cd5a2dde39d29a2055d18b39f06b063a308d3b43a498900c99495b7
---

# Design-Driven Python Development

## Purpose

Turn an approved product contract, technical design, and acceptance contract into the smallest correct Python implementation. Preserve the approved module ownership and dependency direction while proving each production change with developer-owned tests.

This is an implementation method. It does not authorize product, architecture, acceptance, review, merge, or release decisions.

## Authority Order

Use this order when sources disagree:

1. current human instruction and explicit approvals;
2. repository agent/contributor contract;
3. approved requirements or PRD;
4. approved technical design and accepted architecture decisions;
5. approved acceptance contract and executable acceptance tests;
6. existing production behavior that remains in scope;
7. this generic method.

Stop with `BLOCKED` rather than choosing the easiest interpretation. Generic Python advice never overrides approved design or established repository conventions.

## Preconditions

Before editing production code, verify:

- the exact approved requirement, design, and acceptance revisions or hashes;
- the authoritative branch/worktree and current candidate revision;
- the in-scope behavior, non-goals, module responsibilities, and prohibited outcomes;
- the repository's actual Python version, package layout, test runner, and quality commands;
- that the acceptance suite is readable and not developer-owned.

If the design leaves module ownership, public contracts, persistence, security boundaries, migration behavior, or error semantics undecided, route the gap to the responsible owner. Do not resolve it through implementation convenience.

## Design-to-Implementation Map

Maintain this map during the task. It may live in the issue evidence artifact rather than a new repository document.

| Requirement | Design Component | Python Module / Boundary | Developer Test | Acceptance Coverage | Status |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | RED / GREEN / BLOCKED |

The map prevents three common failures:

- implementing behavior that has no approved requirement;
- satisfying a weak developer proxy instead of the accepted outcome;
- collapsing or bypassing a boundary defined by the technical design.

## Modular Python Contract

### Preserve approved boundaries

- Organize code around cohesive responsibilities and the current repository structure; do not force a generic `src/` layout or broad package migration.
- Keep domain/application logic independent from filesystem, network, runtime, storage, framework, and vendor details when the approved design establishes that separation.
- Express external capabilities through the design's ports or stable interfaces. In Python, prefer a small `Protocol` or callable contract when structural typing improves substitution and testing.
- Implement concrete I/O and infrastructure behavior in adapters at the edge.
- Keep dependency wiring explicit in the approved composition root; avoid hidden service locators, import-time setup, and mutable global registries.
- Do not create an abstraction for every function. Add a boundary only when required by the design, an external side effect, independent substitution, or a demonstrated maintenance need.

### Keep modules coherent

Each changed module should have one explainable responsibility, a stable public surface, and dependencies appropriate to its layer. Split responsibilities when unrelated reasons to change are mixed; do not split mechanically by line count.

Prevent:

- circular imports;
- core modules importing adapters or recipe/project-specific implementations;
- adapters calling each other around the application boundary;
- public contracts depending on private implementation types;
- convenience helpers becoming a second source of domain truth;
- unrelated refactors disguised as modularization.

### Use Python deliberately

- Follow the repository's supported Python version and formatting conventions.
- Type public functions, boundary objects, and non-obvious internal contracts. Avoid `Any` when a meaningful type is practical.
- Use `Protocol` for capability contracts, `dataclass` for internal value objects where appropriate, and Pydantic or equivalent validation at approved serialization/input boundaries—not as an automatic domain model.
- Prefer explicit dataflow and dependency injection over hidden globals or import-time side effects.
- Catch specific exceptions, preserve causes with exception chaining, and translate infrastructure errors at the correct boundary.
- Use context managers for resources and `pathlib` for path operations where compatible with repository conventions.
- Avoid mutable default arguments, bare `except`, wildcard imports, silent failure, magic success values, and speculative performance tricks.

## Developer-Owned TDD

Acceptance tests are an immutable external oracle. The developer writes unit and integration tests for implementation behavior but does not rewrite the acceptance contract.

For each smallest behavior slice:

1. **RED** — write or update one focused developer-owned test derived from an approved requirement and design component.
2. Run the exact target and prove it fails for the intended missing or incorrect behavior—not syntax, setup, dependency, or unrelated failures.
3. **GREEN** — write the smallest production change that makes that target pass without weakening the assertion or bypassing the intended production boundary.
4. Rerun the same target and record non-empty GREEN output.
5. **REFACTOR** — improve names, duplication, boundaries, and dependency direction only while tests remain green.
6. Run affected unit/integration tests before starting the next slice.

Tests should verify behavior at the narrowest meaningful public boundary. Prefer real domain/application code and simple fakes for outbound ports. Use mocks only for genuine external boundaries or interaction semantics; a mock invocation is not proof of a user-visible outcome.

For bug fixes, first reproduce the defect with a failing test, then add a positive control and the relevant boundary/regression case. Fix the causal invariant rather than hard-coding the reported fixture, path, string, or attack.

## Acceptance and Anti-Cheating Boundary

The developer may run the approved acceptance suite but must not:

- edit, weaken, delete, skip, deselect, quarantine, or special-case it;
- detect acceptance fixtures, IDs, prompts, filenames, or known expected values in production code;
- replace real execution with fixed output, fixture echo, stale artifact reuse, fabricated evidence, or status-only success;
- change the test contract to match the implementation;
- treat a local acceptance pass as independent QA approval.

If an acceptance test appears wrong or impossible, stop and submit a test-contract change request with evidence. Continue only after the accountable owner approves a new exact revision.

## Verification

Discover commands from repository configuration and the approved acceptance contract. Do not invent command surfaces or require tools that are not configured.

Run, in order:

1. the focused RED/GREEN target for each behavior slice;
2. affected unit and integration tests;
3. configured format, lint, type, security, and architecture checks relevant to changed code;
4. the approved acceptance slice or full suite required for developer handoff;
5. the broader affected regression surface after all code changes;
6. `git diff --check`, complete base-to-current diff inspection, and repository status/provenance checks.

A command is evidence only when its current non-empty output, exit status, candidate revision, and test count or result are recorded. Do not claim unrun checks passed.

Before handoff, verify the complete change did not alter unrelated behavior, architecture ownership, compatibility, security boundaries, migration semantics, or approved acceptance files.

## Handoff Evidence

Provide a compact artifact containing:

- approved requirement/design/test-contract revisions;
- exact base and candidate revision;
- Design-to-Implementation Map;
- RED and GREEN commands with observed results;
- repository quality and regression commands with non-empty results;
- acceptance command/result clearly labelled as developer-run, not independent QA;
- changed production modules and developer-owned tests;
- known risks, blockers, or unrun checks.

The handoff verdict is `READY_FOR_INDEPENDENT_QA`, `BLOCKED`, or `INCOMPLETE`. It is never self-approval, merge approval, or acceptance approval.

## Completion Gate

Implementation is ready for independent QA only when:

- every changed behavior traces to approved authority, a design component, production code, and developer-owned tests;
- every new production behavior has valid RED then GREEN evidence;
- module responsibilities and dependency direction match the approved design;
- configured quality checks and affected regression tests pass with fresh evidence;
- approved acceptance files are unchanged unless an approved test-contract revision explicitly changed them;
- the complete diff and affected call paths were reviewed;
- exact candidate provenance and remaining risks are recorded.

Otherwise report the precise blocker or missing evidence without weakening the contract.
