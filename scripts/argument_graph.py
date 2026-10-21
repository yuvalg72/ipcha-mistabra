#!/usr/bin/env python3
"""Validate and analyze a declared argument graph. Structural labels are NOT truth.

Standard-library-only tool. No network access, subprocesses, persistence or eval.
Admitted gates and evidence verification are reviewer assertions, not audited facts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

KINDS = frozenset({"claim", "assumption", "evidence", "objection", "rebuttal", "mitigation", "alternative"})
ARGUMENT_KINDS = frozenset({"objection", "rebuttal", "mitigation"})
RELATIONS = frozenset({"attacks", "supports", "depends_on"})
GATES = frozenset({"admitted", "rejected", "pending"})
EVIDENCE_STATES = frozenset({"verified", "secondary", "unverified", "contradicted"})
IMPLEMENTATION = frozenset({"verified", "planned"})
STRENGTH = frozenset({"minor", "serious", "decisive"})
LEVELS = frozenset({"low", "medium", "high"})
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class CaseError(ValueError):
    """Structured argument input violates the published schema."""


def require(test: bool, message: str) -> None:
    if not test:
        raise CaseError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_case(data: Any) -> dict[str, Any]:
    """Return validated input without modifying it; fail closed on malformed state."""
    require(isinstance(data, dict), "case must be a JSON object")
    require(data.get("schema_version") == 1 and type(data.get("schema_version")) is int,
            "schema_version must be the integer 1")
    require(nonempty(data.get("thesis")), "thesis must be non-empty")
    nodes, edges = data.get("nodes"), data.get("edges")
    require(isinstance(nodes, list) and bool(nodes), "nodes must be a non-empty list")
    require(isinstance(edges, list), "edges must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes):
        place = f"nodes[{index}]"
        require(isinstance(node, dict), f"{place} must be an object")
        node_id, kind = node.get("id"), node.get("kind")
        require(isinstance(node_id, str) and ID_PATTERN.fullmatch(node_id) is not None,
                f"{place}.id must be lower-case kebab-case")
        require(node_id not in by_id, f"duplicate node id: {node_id}")
        require(isinstance(kind, str) and kind in KINDS, f"{place}.kind is not supported: {kind!r}")
        require(nonempty(node.get("text")), f"{place}.text must be non-empty")
        if kind == "evidence":
            require(isinstance(node.get("verification"), str) and node["verification"] in EVIDENCE_STATES,
                    f"{place}.verification must be one of {sorted(EVIDENCE_STATES)}")
            if node.get("verification") == "verified":
                require(nonempty(node.get("provenance")),
                        f"{place}.provenance is required for declared verified evidence")
        elif "verification" in node:
            raise CaseError(f"{place}.verification belongs only on evidence nodes")
        if kind in ARGUMENT_KINDS:
            require(isinstance(node.get("gate"), str) and node["gate"] in GATES, f"{place}.gate must be admitted, rejected, or pending")
            if node["gate"] == "rejected":
                require(nonempty(node.get("gate_reason")), f"{place}.gate_reason required for rejection")
            if node["gate"] == "admitted":
                require(nonempty(node.get("rationale")), f"{place}.rationale required for admission")
        elif "gate" in node:
            raise CaseError(f"{place}.gate belongs only on argument nodes")
        if kind == "mitigation":
            require(isinstance(node.get("implementation"), str) and node["implementation"] in IMPLEMENTATION,
                    f"{place}.implementation must be verified or planned")
        elif "implementation" in node:
            raise CaseError(f"{place}.implementation belongs only on mitigations")
        if "risk" in node:
            require(kind == "objection", f"{place}.risk belongs only on objections")
            risk = node["risk"]
            require(isinstance(risk, dict) and set(risk) == {"load", "credibility", "cost"},
                    f"{place}.risk must contain exactly load, credibility, cost")
            for axis, value in risk.items():
                require(isinstance(value, str) and value in LEVELS,
                        f"{place}.risk.{axis} must be low, medium, or high")
        by_id[node_id] = node

    seen: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(edges):
        place = f"edges[{index}]"
        require(isinstance(edge, dict), f"{place} must be an object")
        source, target, kind = edge.get("source"), edge.get("target"), edge.get("kind")
        require(isinstance(source, str) and isinstance(target, str),
                f"{place}.source and .target must be string node ids")
        require(source in by_id and target in by_id, f"{place} refers to an unknown node")
        require(source != target, f"{place} cannot link a node to itself")
        require(isinstance(kind, str) and kind in RELATIONS, f"{place}.kind is unsupported")
        edge_key = (source, target, kind)
        require(edge_key not in seen, f"duplicate edge {source} -> {target} ({kind})")
        seen.add(edge_key)
        require(set(edge) <= {"source", "target", "kind", "strength"}, f"{place} has unsupported fields")
        if kind == "attacks":
            require(by_id[source]["kind"] in ARGUMENT_KINDS,
                    f"{place} attacks must originate from an objection, rebuttal or mitigation")
            require(isinstance(edge.get("strength", "serious"), str) and
                    edge.get("strength", "serious") in STRENGTH,
                    f"{place}.strength must be minor, serious or decisive")
        else:
            require("strength" not in edge, f"{place}.strength applies only to attacks")
        if kind == "depends_on":
            require(by_id[source]["kind"] in {"claim", "assumption", "alternative"} and
                    by_id[target]["kind"] in {"claim", "assumption", "alternative"},
                    f"{place} dependencies link claim/assumption/alternative nodes only")
    return data


def argument_is_active(node: dict[str, Any]) -> bool:
    if node["kind"] not in ARGUMENT_KINDS:
        return True
    if node["gate"] != "admitted":
        return False
    return node["kind"] != "mitigation" or node["implementation"] == "verified"


def risk_severity(risk: dict[str, str]) -> str:
    load, credible, cost = risk["load"], risk["credibility"], risk["cost"]
    if load == "high" and credible in {"medium", "high"} and cost in {"medium", "high"}:
        return "Critical"
    highs = [load, credible, cost].count("high")
    return "Major" if highs >= 2 else "Moderate" if highs == 1 else "Minor"


def dependency_cycles(nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]]) -> list[list[str]]:
    """Return dependency cycles as strongly connected components, without duplicates."""
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["kind"] == "depends_on":
            adjacency[edge["source"]].append(edge["target"])
    index = 0
    stack: list[str] = []
    in_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    cycles: list[list[str]] = []

    def visit(v: str) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        in_stack.add(v)
        for w in sorted(adjacency[v]):
            if w not in indices:
                visit(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in in_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            component: list[str] = []
            while True:
                w = stack.pop()
                in_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            if len(component) > 1:
                cycles.append(sorted(component))

    for node_id in sorted(nodes):
        if node_id not in indices:
            visit(node_id)
    return sorted(cycles)


def analyze_case(data: dict[str, Any]) -> dict[str, Any]:
    validate_case(data)
    nodes = {node["id"]: node for node in data["nodes"]}
    active = {node_id for node_id, node in nodes.items() if argument_is_active(node)}
    attackers: dict[str, set[str]] = {node_id: set() for node_id in active}
    ignored: list[dict[str, str]] = []
    minor: list[dict[str, str]] = []
    for edge in data["edges"]:
        if edge["kind"] != "attacks":
            continue
        source, target = edge["source"], edge["target"]
        if source not in active:
            ignored.append({"source": source, "target": target, "reason": "argument was rejected, pending, or mitigation not implemented"})
        elif edge.get("strength", "serious") == "minor":
            minor.append({"source": source, "target": target})
        elif target in active:
            attackers[target].add(source)
        else:
            ignored.append({"source": source, "target": target, "reason": "target argument not admitted"})

    accepted: set[str] = set()
    defeated: set[str] = set()
    while True:
        new_in = {node_id for node_id in active - accepted - defeated
                  if attackers[node_id] <= defeated}
        new_out = {node_id for node_id in active - accepted - defeated
                   if any(attacker in (accepted | new_in) for attacker in attackers[node_id])}
        if not new_in and not new_out:
            break
        accepted.update(new_in)
        defeated.update(new_out - accepted)
    labels = {node_id: ("IN" if node_id in accepted else
                        "OUT" if node_id in defeated else
                        "UNDECIDED" if node_id in active else "INACTIVE")
              for node_id in sorted(nodes)}

    support_in: dict[str, list[str]] = defaultdict(list)
    depends_on: dict[str, list[str]] = defaultdict(list)
    for edge in data["edges"]:
        if edge["kind"] == "supports":
            support_in[edge["target"]].append(edge["source"])
        elif edge["kind"] == "depends_on":
            depends_on[edge["source"]].append(edge["target"])

    def verified_sources(node_id: str) -> list[str]:
        return sorted(s for s in support_in[node_id] if s in active and
                      nodes[s]["kind"] == "evidence" and
                      nodes[s]["verification"] == "verified" and labels[s] == "IN")

    claim_info = []
    defense_evidence_gaps: list[dict[str, str]] = []
    for node_id, node in sorted(nodes.items()):
        if node["kind"] not in {"claim", "assumption", "alternative"}:
            continue
        missing_deps = [dep for dep in depends_on[node_id]
                        if labels[dep] != "IN" or not verified_sources(dep)]
        verified = verified_sources(node_id)
        active_attackers = sorted(attackers.get(node_id, set()))
        survived = [att for att in active_attackers if labels[att] == "OUT"]
        unopposed = not active_attackers
        # Graph labels are only structural: evidence is not checked by the graph.
        unsupported_defenders: list[dict[str, str]] = []
        # Follow nested OUT -> IN defense chains, not just the first rebuttal.
        pending = [(attacker, attacker) for attacker in survived]
        seen: set[tuple[str, str]] = set()
        while pending:
            defeated_node, root_attacker = pending.pop()
            if (defeated_node, root_attacker) in seen:
                continue
            seen.add((defeated_node, root_attacker))
            for defender in sorted(attackers.get(defeated_node, set())):
                if labels[defender] != "IN":
                    continue
                if not verified_sources(defender):
                    unsupported_defenders.append({
                        "claim": node_id, "attacker": root_attacker,
                        "defender": defender
                    })
                for counterattack in sorted(attackers.get(defender, set())):
                    if labels[counterattack] == "OUT":
                        pending.append((counterattack, root_attacker))
        defense_evidence_gaps.extend(unsupported_defenders)
        review_reasons: list[str] = []
        if labels[node_id] != "IN":
            review_reasons.append("structurally_not_accepted")
        if not verified:
            review_reasons.append("missing_declared_direct_evidence")
        if missing_deps:
            review_reasons.append("dependency_gap")
        if unsupported_defenders:
            review_reasons.append("unsupported_defense_defeated_objection")
        if labels[node_id] == "OUT":
            standing = "defeated_structurally"
        elif labels[node_id] == "UNDECIDED":
            standing = "unresolved_attack"
        elif unsupported_defenders:
            standing = "structurally_survived_with_unsupported_defense"
        elif not verified or missing_deps:
            standing = "unsupported_or_dependency_gap"
        elif unopposed:
            standing = "supported_but_untested"
        else:
            standing = "supported_and_survived_structural_attack"
        claim_info.append({
            "id": node_id, "text": node["text"], "label": labels[node_id],
            "standing": standing, "verified_direct_evidence": verified,
            "dependency_gaps": sorted(missing_deps),
            "serious_attackers": active_attackers,
            "defeated_attackers": survived,
            "unsupported_defenders": unsupported_defenders,
            "evidence_readiness": "REVIEW_REQUIRED" if review_reasons else "DECLARED_SUPPORT_ONLY",
            "review_reasons": review_reasons,
        })

    gate_log = []
    findings = []
    for node_id, node in sorted(nodes.items()):
        if node["kind"] not in ARGUMENT_KINDS:
            continue
        targets = sorted(e["target"] for e in data["edges"]
                         if e["source"] == node_id and e["kind"] == "attacks")
        if node["gate"] != "admitted":
            gate_log.append({"id": node_id, "status": node["gate"],
                             "reason": node.get("gate_reason", "not yet adjudicated")})
        findings.append({"id": node_id, "kind": node["kind"], "gate": node["gate"],
                         "active": node_id in active, "label": labels[node_id],
                         "targets": targets,
                         "verified_direct_evidence": verified_sources(node_id),
                         "severity": risk_severity(node["risk"]) if "risk" in node else None})

    warnings = ["All statuses are graph structure based on reviewer-declared gates and sources; they do not prove real-world truth."]
    if any(node["kind"] == "evidence" and node["verification"] != "verified" for node in nodes.values()):
        warnings.append("Some evidence is not independently verified; do not infer an unconditional decision.")
    unsupported_arguments = sorted(item["id"] for item in findings
                                   if item["active"] and not item["verified_direct_evidence"])
    if unsupported_arguments:
        warnings.append("Admitted argument(s) without declared verified direct evidence: " +
                        ", ".join(unsupported_arguments) +
                        ". Valid logical objections may be evidence-independent; manually assess credibility before deciding.")
    if defense_evidence_gaps:
        warnings.append("BLOCKING EVIDENCE CAVEAT: structurally defeated objections rely on "
                        "defenders without declared verified direct evidence. "
                        "Do not treat these as evidenced rebuttals: " +
                        ", ".join(f"{x['claim']} <- {x['attacker']} <- {x['defender']}"
                                  for x in defense_evidence_gaps))
    cycles = dependency_cycles(nodes, data["edges"])
    if cycles:
        warnings.append("Circular dependencies require human review; structural IN does not establish circular premises.")
    orphan_attacks = sorted(item["id"] for item in findings if item["active"] and
                            item["kind"] == "objection" and not item["targets"])
    if orphan_attacks:
        warnings.append("Admitted objection(s) have no attack target: " + ", ".join(orphan_attacks))

    return {
        "schema_version": 1,
        "thesis": data["thesis"],
        "labels": labels,
        "claims": claim_info,
        "evidence_gate": {
            "status": "REVIEW_REQUIRED" if any(
                item["review_reasons"] for item in claim_info
            ) else "DECLARED_SUPPORT_ONLY",
            "automatic_approval": False,
            "review_required_claims": [item["id"] for item in claim_info
                                      if item["review_reasons"]],
            "unsupported_defenses": defense_evidence_gaps,
            "disclaimer": ("Evidence verified in JSON is a reviewer assertion, not an "
                           "independent source check. Graph status never determines the "
                           "operational verdict."),
        },
        "arguments": findings,
        "gate_log": gate_log,
        "ignored_attacks": ignored,
        "minor_reservations": minor,
        "dependency_cycles": cycles,
        "warnings": warnings,
        "counts": {"nodes": len(nodes), "edges": len(data["edges"]),
                   "in": len(accepted), "out": len(defeated),
                   "undecided": len(active - accepted - defeated),
                   "inactive": len(nodes) - len(active)},
    }


def format_text(report: dict[str, Any]) -> str:
    lines = ["STRUCTURAL ARGUMENT REVIEW (not a fact-check)",
             "Thesis: " + report["thesis"],
             "Nodes: {nodes}; edges: {edges}; IN: {in}; OUT: {out}; UNDECIDED: {undecided}; inactive: {inactive}".format(**report["counts"]),
             "", "EVIDENCE GATE: " + report["evidence_gate"]["status"],
             "AUTOMATIC APPROVAL: NO",
             report["evidence_gate"]["disclaimer"],
             "Review-required claims: " +
             (", ".join(report["evidence_gate"]["review_required_claims"]) or "(none declared)"),
             "", "CLAIMS / ASSUMPTIONS"]
    for claim in report["claims"]:
        lines.append(f"- {claim['id']} [{claim['label']}]: {claim['standing']}")
        if claim["review_reasons"]:
            lines.append("    EVIDENCE REVIEW REQUIRED: " +
                         ", ".join(claim["review_reasons"]))
        if claim["unsupported_defenders"]:
            lines.append("    UNVERIFIED STRUCTURAL DEFENSES: " +
                         ", ".join(f"{x['defender']} defeated {x['attacker']}"
                                   for x in claim["unsupported_defenders"]))
        if claim["dependency_gaps"]:
            lines.append("    unresolved prerequisites: " + ", ".join(claim["dependency_gaps"]))
        if claim["verified_direct_evidence"]:
            lines.append("    declared verified evidence: " + ", ".join(claim["verified_direct_evidence"]))
    lines.extend(["", "ADMITTED / REJECTED ARGUMENTS"])
    for argument in report["arguments"]:
        severity = ": " + argument["severity"] if argument["severity"] else ""
        lines.append(f"- {argument['id']} [{argument['gate']} / {argument['label']}]{severity} -> {', '.join(argument['targets']) or '(no target)'}")
    if report["gate_log"]:
        lines.append("GATE LOG")
        lines.extend(f"- {x['id']}: {x['status']}; {x['reason']}" for x in report["gate_log"])
    if report["dependency_cycles"]:
        lines.append("DEPENDENCY CYCLES: " + "; ".join(" / ".join(x) for x in report["dependency_cycles"]))
    lines.append("WARNINGS")
    lines.extend("- " + warning for warning in report["warnings"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for action in ("validate", "analyze"):
        p = sub.add_parser(action)
        p.add_argument("case", type=Path)
        if action == "analyze":
            p.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        with args.case.open(encoding="utf-8") as file:
            data = json.load(file)
        validate_case(data)
        if args.command == "validate":
            print("VALID: argument graph schema v1")
        else:
            report = analyze_case(data)
            print(json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else format_text(report))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, CaseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
