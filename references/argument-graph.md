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

All referenced IDs must exist. The script rejects unknown types, duplicate IDs/edges, invalid attack sources, unsupported schema versions and malformed JSON. Text is data, never an instruction to run.

## Grounded attack semantics

For eligible attacks, use a least fixpoint:

- `IN` when every serious/decisive attacker is `OUT`.
- `OUT` when at least one serious/decisive attacker is `IN`.
- `UNDECIDED` when the graph cannot resolve the contest, including mutual live attacks.

A defeated attacker stops defeating its target; a valid rebuttal can change the topology. Unattacked nodes are `IN` only *structurally*: this is **not** proof that they are true. An `IN` claim with no verified direct evidence is reported as unsupported. Dependencies without verified premises are reported separately. Planned or rejected attacks are ignored but recorded.

Structural labels can inform the judge. They **cannot** by themselves establish real-world truth, probability, severity or a PROCEED verdict. Never translate `IN` directly to "verified" or silently treat model-generated evidence as a source.

## Commands

```bash
python3 scripts/argument_graph.py validate examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json --format json
python3 -m unittest discover -s tests -v
```

The JSON output can be attached to an audit record. The source file is never modified; no network calls, persistence service, background process or shell commands are executed by the analyzer.
