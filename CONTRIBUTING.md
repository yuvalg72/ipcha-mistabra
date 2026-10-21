# Contributing

Propose changes through an issue or a pull request. Keep improvements focused on measurable review quality, grounded evidence handling, honest verdicts, false-positive reduction, or auditable argument semantics.

## Development

Use Python 3.10+ and the standard library. No dependency installation is required.

```bash
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
python3 scripts/argument_graph.py validate examples/architecture-review.json
```

Add a regression test and a manual evaluation case for every behavior-changing fix. Do not present a manually written expected outcome as a passed LLM benchmark. When changing verdict or gate semantics, update the control-plane `SKILL.md`, relevant references, and tests together.

## Pull request expectations

1. Describe the specific failure mode or improvement and how it changes decisions.
2. Include realistic before/after examples without proprietary or personal data.
3. Record compatibility, risk and rollback impacts where relevant.
4. Validate local links, code syntax, schema and unit tests.
5. Wait for actual CI completion and review of all blocking comments; CI success alone does not imply approval.

Do not add a persistent server, network egress, external dependencies, broad privileges or autonomous production actions without an explicit design and security review. Never commit tokens, secrets or customer configurations.
