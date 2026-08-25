import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class FrameworkCompilationContractTests(unittest.TestCase):
    def test_contract_is_bundled_and_routed(self):
        contract = SKILL_ROOT / "references" / "research-framework-compilation-contract.md"
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertTrue(contract.is_file())
        self.assertIn("research-framework-compilation-contract.md", skill_text)

    def test_contract_separates_evidence_and_explanation_frameworks(self):
        text = (
            SKILL_ROOT / "references" / "research-framework-compilation-contract.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Evidence Framework", text)
        self.assertIn("Explanation Framework", text)
        self.assertIn("Framework Vn", text)
        self.assertIn("Relative MECE", text)

    def test_contract_has_all_structural_change_events(self):
        text = (
            SKILL_ROOT / "references" / "research-framework-compilation-contract.md"
        ).read_text(encoding="utf-8")

        for event in (
            "Add",
            "Split",
            "Merge",
            "Reorder",
            "Reframe",
            "Remove",
            "Challenge",
            "No structural change",
        ):
            self.assertIn(f"`{event}`", text)

    def test_framework_eval_matrix_covers_regression_transfer_and_negative(self):
        evals = json.loads((SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in evals["evals"]}

        expected = {
            "framework-compilation-skill-evaluation-industry-regression": "behavior-regression",
            "framework-compilation-transfer-user-activation-diagnosis": "transfer",
            "framework-compilation-preserves-user-provided-structure": "negative",
            "framework-compilation-reframes-after-evidence": "behavior-regression",
        }
        for case_id, case_type in expected.items():
            self.assertIn(case_id, cases)
            self.assertEqual(cases[case_id]["type"], case_type)

    def test_framework_grader_is_bundled(self):
        grader = (
            SKILL_ROOT
            / "evals"
            / "graders"
            / "research-framework-compilation-rubric.md"
        )
        self.assertTrue(grader.is_file())
        text = grader.read_text(encoding="utf-8")
        self.assertIn("User structure boundary", text)
        self.assertIn("Artifact projection", text)


if __name__ == "__main__":
    unittest.main()
