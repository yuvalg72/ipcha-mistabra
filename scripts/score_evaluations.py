#!/usr/bin/env python3
"""Score blinded, expert-adjudicated paired responses; NEVER run a model or certify quality.

This offline scorer accepts a finalized JSON annotation ledger. It measures only
what human reviewers recorded, not objective model correctness by itself.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VERDICTS = frozenset({"PROCEED", "REVISE", "RETHINK", "STOP"})
KIND = frozenset({"synthetic_example", "human_adjudicated"})


class EvaluationError(ValueError):
    """Invalid human evaluation ledger."""


def check(test: bool, message: str) -> None:
    if not test:
        raise EvaluationError(message)


def ids(value: Any, where: str, allow_empty: bool = True) -> set[str]:
    check(isinstance(value, list), f"{where} must be an array")
    check(allow_empty or bool(value), f"{where} may not be empty")
    check(all(isinstance(x, str) and bool(x.strip()) for x in value),
          f"{where} must contain nonempty string identifiers")
    check(len(value) == len(set(value)), f"{where} has duplicate identifiers")
    return set(value)


def validate(data: Any) -> list[dict[str, Any]]:
    check(isinstance(data, dict), "evaluation ledger must be an object")
    check(type(data.get("schema_version")) is int and data["schema_version"] == 1,
          "schema_version must be integer 1")
    check(isinstance(data.get("dataset_kind"), str) and data["dataset_kind"] in KIND,
          "dataset_kind must be synthetic_example or human_adjudicated")
    cases = data.get("cases")
    check(isinstance(cases, list) and bool(cases), "cases must be a nonempty list")
    found: set[str] = set()
    for i, item in enumerate(cases):
        at = f"cases[{i}]"
        check(isinstance(item, dict), f"{at} must be an object")
        case_id = item.get("id")
        check(isinstance(case_id, str) and bool(case_id.strip()), f"{at}.id missing")
        check(case_id not in found, f"duplicate case id {case_id}")
        found.add(case_id)
        check(isinstance(item.get("segment"), str) and bool(item["segment"].strip()),
              f"{at}.segment must be nonempty")
        ids(item.get("gold_issue_ids"), at + ".gold_issue_ids")
        acceptable = ids(item.get("acceptable_verdicts"), at + ".acceptable_verdicts",
                         allow_empty=False)
        check(acceptable <= VERDICTS, f"{at}.acceptable_verdicts invalid")
        for run in ("baseline", "skill"):
            item_run = item.get(run)
            rp = at + "." + run
            check(isinstance(item_run, dict), rp + " must be an object")
            ids(item_run.get("issue_ids"), rp + ".issue_ids")
            check(isinstance(item_run.get("verdict"), str) and
                  item_run["verdict"] in VERDICTS, rp + ".verdict invalid")
            n = item_run.get("unsupported_claims")
            check(type(n) is int and n >= 0, rp + ".unsupported_claims must be int >= 0")
            for score in ("source_fidelity", "actionability", "decision_quality"):
                n = item_run.get(score)
                check(type(n) is int and 1 <= n <= 5,
                      f"{rp}.{score} must be an integer 1..5")
    return cases


def summarize(cases: list[dict[str, Any]], run: str) -> dict[str, float | int | None]:
    count, tp, fp, fn, correct = len(cases), 0, 0, 0, 0
    unsupported = source_fidelity = actionability = decision_quality = 0
    for item in cases:
        gold = set(item["gold_issue_ids"])
        result = item[run]
        actual = set(result["issue_ids"])
        tp += len(actual & gold)
        fp += len(actual - gold)
        fn += len(gold - actual)
        correct += int(result["verdict"] in item["acceptable_verdicts"])
        unsupported += result["unsupported_claims"]
        source_fidelity += result["source_fidelity"]
        actionability += result["actionability"]
        decision_quality += result["decision_quality"]
    return {
        "cases": count,
        "material_issue_precision": round(tp / (tp + fp), 4) if tp + fp else None,
        "material_issue_recall": round(tp / (tp + fn), 4) if tp + fn else None,
        "false_objections_per_case": round(fp / count, 4),
        "acceptable_verdict_rate": round(correct / count, 4),
        "unsupported_claims_per_case": round(unsupported / count, 4),
        "source_fidelity_mean_1_to_5": round(source_fidelity / count, 4),
        "actionability_mean_1_to_5": round(actionability / count, 4),
        "decision_quality_mean_1_to_5": round(decision_quality / count, 4),
    }


def score(data: Any) -> dict[str, Any]:
    cases = validate(data)
    baseline, skill = summarize(cases, "baseline"), summarize(cases, "skill")
    keys = [key for key in baseline if key != "cases"]
    by_segment: dict[str, dict[str, Any]] = {}
    for segment in sorted({c["segment"] for c in cases}):
        subset = [c for c in cases if c["segment"] == segment]
        by_segment[segment] = {"baseline": summarize(subset, "baseline"),
                               "skill": summarize(subset, "skill")}
    return {
        "dataset_kind": data["dataset_kind"],
        "cases": len(cases),
        "measures_are": "human_annotations_not_independent_validation",
        "benchmark_proof": False,
        "baseline": baseline,
        "skill": skill,
        "skill_minus_baseline": {key: round(skill[key] - baseline[key], 4)
                                 if skill[key] is not None and baseline[key] is not None
                                 else None for key in keys},
        "by_segment": by_segment,
        "caveats": [
            "Synthetic example scores are NOT evidence of improvement."
            if data["dataset_kind"] == "synthetic_example" else
            "Human annotations require blind adjudication, controlled model settings, and uncertainty intervals before claims of improvement.",
            "Issue-id labels and numeric quality scores were provided by reviewers, not inferred or verified by this scorer.",
            "Precision and recall use the adjudicated issue list as reference, not an objective oracle.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="Human-scored baseline/skill cases")
    args = parser.parse_args(argv)
    try:
        with args.ledger.open(encoding="utf-8") as source:
            data = json.load(source)
        print(json.dumps(score(data), ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, EvaluationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
