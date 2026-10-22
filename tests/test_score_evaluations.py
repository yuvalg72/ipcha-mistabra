"""Offline evaluation scorer regression tests; fixture is synthetic, not a benchmark."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from score_evaluations import EvaluationError, score, validate  # noqa: E402


class EvaluationScorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "examples/evaluation-ledger.synthetic.json")
                              .read_text(encoding="utf-8"))

    def test_synthetic_fixture_is_not_claimed_as_benchmark_proof(self):
        report = score(self.data)
        self.assertEqual(report["dataset_kind"], "synthetic_example")
        self.assertFalse(report["benchmark_proof"])
        self.assertEqual(report["cases"], 2)
        self.assertEqual(report["baseline"]["material_issue_recall"], 0.0)
        self.assertEqual(report["skill"]["material_issue_recall"], 1.0)
        self.assertEqual(report["baseline"]["false_objections_per_case"], 0.5)
        self.assertEqual(report["skill"]["false_objections_per_case"], 0.0)

    def test_no_gold_positive_items_is_well_defined(self):
        one = copy.deepcopy(self.data)
        one["cases"] = [one["cases"][1]]
        r = score(one)
        self.assertIsNone(r["skill"]["material_issue_recall"])
        self.assertIsNone(r["skill"]["material_issue_precision"])
        self.assertIsNone(r["skill_minus_baseline"]["material_issue_recall"])

    def test_malformed_record_fails_validation(self):
        bad_values = [
            ("dataset_kind", []),
            ("cases", []),
        ]
        for key, value in bad_values:
            with self.subTest(key=key):
                altered = copy.deepcopy(self.data)
                altered[key] = value
                with self.assertRaises(EvaluationError):
                    validate(altered)

        paths = [
            (("cases", 0, "gold_issue_ids"), [1]),
            (("cases", 0, "acceptable_verdicts"), []),
            (("cases", 0, "baseline", "issue_ids"), [[]]),
            (("cases", 0, "baseline", "unsupported_claims"), True),
            (("cases", 0, "baseline", "source_fidelity"), "5"),
            (("cases", 0, "baseline", "decision_quality"), 9),
            (("cases", 0, "skill", "verdict"), []),
        ]
        for path, value in paths:
            with self.subTest(path=path):
                data = copy.deepcopy(self.data)
                target = data
                for element in path[:-1]:
                    target = target[element]
                target[path[-1]] = value
                with self.assertRaises(EvaluationError):
                    validate(data)

    def test_duplicate_detected_issue_ids_rejected(self):
        data = copy.deepcopy(self.data)
        data["cases"][0]["skill"]["issue_ids"] = ["x", "x"]
        with self.assertRaisesRegex(EvaluationError, "duplicate"):
            validate(data)


if __name__ == "__main__":
    unittest.main()
