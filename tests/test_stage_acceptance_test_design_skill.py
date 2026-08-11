from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "stage-acceptance-test-design" / "SKILL.md"


class StageAcceptanceTestDesignSkillTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATH.read_text(encoding="utf-8")

    def assertContainsAll(self, values):
        for value in values:
            with self.subTest(value=value):
                self.assertIn(value, self.content)

    def test_has_valid_frontmatter_and_trigger_description(self):
        self.assertTrue(self.content.startswith("---\n"))
        match = re.match(r"---\n(.*?)\n---\n", self.content, re.DOTALL)
        if match is None:
            self.fail("SKILL.md frontmatter is missing or malformed")
        frontmatter = match.group(1)
        self.assertIn("name: stage-acceptance-test-design", frontmatter)
        description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
        if description is None:
            self.fail("SKILL.md description is missing")
        description_text = description.group(1)
        self.assertLessEqual(len(description_text), 1024)
        self.assertIn("before implementation", description_text)
        self.assertIn("runnable QA-owned tests", description_text)

    def test_requires_canonical_inputs_and_exact_outputs(self):
        self.assertContainsAll(
            [
                "`product.md`",
                "`product-stages.md`",
                "`stage-N-prd.md`",
                "`stage-N-technical-design.md`",
                "specs/stage-N-test-suite.md",
                "tests/acceptance/stage_N/",
            ]
        )

    def test_separates_qa_product_developer_and_reviewer_rights(self):
        self.assertContainsAll(
            [
                "QA | Test contract",
                "Product Lead | Requirement coverage",
                "Developer | Production code",
                "Code Reviewer | Implementation quality",
                "Test Change Request",
                "The developer may read and run acceptance tests",
            ]
        )
        self.assertIn(
            "The developer may read and run acceptance tests.", self.content
        )
        self.assertIn(
            "the developer submits a Test Change Request", self.content
        )

    def test_requires_requirement_to_artifact_traceability(self):
        self.assertContainsAll(
            [
                "PRD requirement ID",
                "→ acceptance property",
                "→ test ID",
                "→ executable test path and command",
                "→ runtime evidence",
                "→ final artifact or observable outcome",
                "Never silently omit a requirement.",
            ]
        )

    def test_requires_executable_black_box_tests_and_exact_commands(self):
        self.assertContainsAll(
            [
                "exercise the production entrypoint or approved public boundary",
                "assert artifacts and external behavior, not private implementation details",
                "exact executable path",
                "exact non-interactive command",
                "Full Acceptance Command",
                "A Markdown contract without runnable tests is incomplete.",
            ]
        )

    def test_rejects_known_cheating_implementations(self):
        self.assertContainsAll(
            [
                "fixed workflow/DAG regardless of goal semantics",
                "unconditional `completed`/`passed` responses",
                "process invocation, agent call, or Skill load without target result",
                "fake or stale artifact from a previous run",
                "capability declaration without the required tool",
                "echoing fixture data or a precomputed expected result",
                "top-level success while required steps are pending/failed",
                "special-case them",
            ]
        )

    def test_requires_red_or_mutation_proof_before_approval(self):
        self.assertContainsAll(
            [
                "Prove that the suite can fail",
                "controlled mutants",
                "which test rejects each mutant and why",
                "critical negative controls must produce the expected failures",
                "mutation/negative-control evidence",
            ]
        )

    def test_covers_product_outcome_and_robustness_scenarios(self):
        self.assertContainsAll(
            [
                "Normal outcome",
                "Blocked or missing capability",
                "Risk boundary",
                "Outcome evidence",
                "State consistency",
                "Metamorphic behavior",
                "Repeatability",
                "Holdout coverage",
            ]
        )

    def test_forbids_skip_or_deselection_as_pass(self):
        self.assertContainsAll(
            [
                "fail on unexpected `skip`, `xfail`, deselection",
                "confirms no mandatory test was skipped, deselected, quarantined",
                "mandatory tests may not be skipped or omitted",
            ]
        )

    def test_requires_product_lead_approval_and_independent_qa_verdict(self):
        self.assertContainsAll(
            [
                "Product Lead reviews the contract",
                "Record the approval status and the immutable test-contract revision/hash",
                "QA starts from a clean checkout/workspace",
                "`PASS`",
                "`REQUEST_CHANGES`",
                "`BLOCKED`",
                "does not authorize merge by itself",
            ]
        )

    def test_contract_template_contains_mandatory_sections(self):
        self.assertContainsAll(
            [
                "## 1. Authority and Lifecycle",
                "## 3. Requirement Coverage Matrix",
                "## 4. Acceptance Scenarios",
                "## 5. Negative-Control and Mutation Matrix",
                "## 6. Executable Test Mapping",
                "## 7. Runtime Evidence and Artifact Inspection",
                "## 8. Product Lead Approval",
                "## 9. Test Change Requests",
            ]
        )


if __name__ == "__main__":
    unittest.main()
