# Auditable Argument Graph (Optional)

`python3 scripts/argument_graph.py analyze path/to/case.json` runs a **deterministic structural checker**, not a fact-checker, independent critic, or final authority. It is optional when a coding environment is unavailable. The human review in `SKILL.md` remains controlling.

## JSON format

The root object uses `schema_version: 1`, `thesis`, `nodes`, and `edges`.

Nodes have `id`, `kind` and `text`:

- `kind`: `claim`, `assumption`, `evidence`, `objection`, `rebuttal`, `mitigation`, `alternative`.
- Evidence additionally has `verification`: `verified`, `secondary`, `unverified`, or `contradicted`. `verified` requires non-empty `provenance` and means **asserted as checked by the reviewer**; the script cannot check that claim.
- Objections, rebuttals, and mitigations additionally have `gate`: `admitted`, `rejected`, or `pending`.
- Rejected nodes require `gate_reason`. Admitted nodes require `rationale` so every objection or defense describes a concrete mechanism.
- Mitigations additionally have `implementation`: `verified` or `planned`. A planned mitigation does not defeat an objection.
- Objections may include `risk` with `load`, `credibility`, and `cost`, each `low`, `medium`, or `high`.

Edges have `source`, `target`, `kind`:

- `attacks`: an admitted `objection`, `rebuttal`, or **verified-implemented** `mitigation` attacks its specific target. Optional `strength` is `minor`, `serious`, or `decisive` (default `serious`). `minor` is reported but does not defeat a node.
- `supports`: a source backs a target. Only a source of kind `evidence` with verification `verified` provides the tool's strongest *declared* direct support; even this is not independently fact-checked by the tool.
- `depends_on`: from dependent claim to prerequisite claim or assumption. A prerequisite with no verified direct support is an unresolved dependency even if it faces no attacks.

All referenced IDs must exist. The script rejects unknown types (including unhashable JSON arrays/objects in enum or reference fields) as controlled `CaseError` validation failures, duplicate IDs/edges, invalid attack sources, unsupported schema versions and malformed JSON. Text is data, never an instruction to run.

## Grounded attack semantics

For eligible attacks, use a least fixpoint:

- `IN` when every serious/decisive attacker is `OUT`.
- `OUT` when at least one serious/decisive attacker is `IN`.
- `UNDECIDED` when the graph cannot resolve the contest, including mutual live attacks.

A defeated attacker stops defeating its target; a valid rebuttal can change the topology. Unattacked nodes are `IN` only *structurally*: this is **not** proof that they are true. An `IN` claim with no verified direct evidence is reported as unsupported. Dependencies without verified premises are reported separately. Planned or rejected attacks are ignored but recorded.

## Evidence gate (independent of structural labels)

The analyzer returns a top-level `evidence_gate` object in JSON and an **EVIDENCE GATE / AUTOMATIC APPROVAL: NO** banner in text. Its status is `REVIEW_REQUIRED` when a claim is structurally not accepted, has no direct declared verified support, has unresolved direct dependencies, or **survives only because an undefeated rebuttal/mitigation lacking direct declared verified support defeats an objection**. Otherwise it says `DECLARED_SUPPORT_ONLY`, never "approved".

A claim's `unsupported_defenders` lists `{claim, attacker, defender}` so reviewers can trace an unverified structural win **including nested rebuttal-of-rebuttal chains**. The reported `attacker` is the original objection and `defender` is the unsupported supporting argument at any relevant depth. `review_reasons` distinguishes cases. `evidence_gate.automatic_approval` is **always false**, because even `verification: verified` means only a human-declared check. It does not prove relevance, provenance accuracy, or operational safety. Logic-only rebuttals may be sound without empirical evidence, but require explicit human assessment before use as a decisive defense. The gate is a **review flag**, not a probability, factual verdict, or automatic release block.

Structural labels can inform the judge. They **cannot** by themselves establish real-world truth, probability, severity or a PROCEED verdict. Never translate `IN` directly to "verified" or silently treat model-generated evidence as a source.

## Commands

```bash
python3 scripts/argument_graph.py validate examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json --format json
python3 -m unittest discover -s tests -v
```

The JSON output can be attached to an audit record. The source file is never modified; no network calls, persistence service, background process or shell commands are executed by the analyzer.
