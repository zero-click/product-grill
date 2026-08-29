# Role to Base Skill Map

Use this map to attribute Goal OS delivery feedback. Workflow Skills may coexist, but the Coach modifies a professional Base Skill only when the failure belongs to that role's reusable method.

| Role | Canonical Base Skill | Coach may improve | Must not absorb |
|---|---|---|---|
| Project Lead | `product-grill`, `product-stage-design`; shared `product-contract-gate` | product framing, stage strategy, Gate evidence probe | Multica dispatch mechanics, specialist methods |
| PRD Writer | `prd-grill`; shared `product-contract-gate` | user flow, product behavior, requirement clarity, author decision ledger | architecture, test implementation, routing |
| Product Reviewer | `product-contract-gate` | independent cross-document review, contradiction and decision-preservation checks | authoring the product contract, Human approval |
| Architecture Owner | `tech-design-grill` | component responsibility, boundaries, trade-offs, migration, failure semantics | product meaning, QA Oracle, production code |
| QA / Acceptance Owner | `stage-acceptance-test-design` | causal Oracle, negative controls, holdouts, provenance, independent verdict | production implementation, white-box code review |
| Test Contract Reviewer | `test-contract-adversarial-review` | independent claim tracing, mutation/probe design, whole-contract review | rewriting QA tests, adding product semantics |
| Developer | `design-driven-python-development` | design-driven implementation, developer TDD, anti-hardcoding, revision evidence | acceptance tests, product/design decisions, merge |
| Code Reviewer | `code-review-grill` | complete diff/call-path/security/migration/test-integrity review | production edits, Human merge approval |
| Skill Coach | `agent-skill-coach` | evidence attribution, minimal Skill patch, replay design | live deployment, self-approval, product decisions |

## Selection rule

When one episode exposes several failures, select the earliest causal professional-method gap only if it is independently evidenced. Create separate candidate changes for independent downstream failures. Never patch three role Skills in one PR simply because all three participated in the same Issue.
