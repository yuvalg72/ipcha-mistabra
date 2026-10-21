<p align="center">
  <img src="assets/icon.svg" alt="Ipcha Mistabra skill icon" width="112" height="112">
</p>
<h1 align="center">Ipcha Mistabra</h1>
<p align="center"><strong>An evidence-first devil's advocate that is allowed to agree.</strong></p>

<p align="center">
  <code>ChatGPT Skill</code> &nbsp;|&nbsp; <code>Critical thinking / decision quality</code> &nbsp;|&nbsp; <code>Active source / 0.1.x</code>
</p>

> This README is the human-facing overview. [SKILL.md](SKILL.md) is the **authoritative** control-plane definition for invocation and behavior.

Ipcha Mistabra turns a proposal into a fair contest between its strongest defensible case and its strongest plausible rival. It then checks the *objections themselves*, refuses artificial negativity, and gives a decision-ready conclusion with a named falsifier and next test.

No subscriptions, API keys, external services, JavaScript runtime, or dependencies are required for the reasoning workflow. The optional argument graph analyzer uses the Python standard library.

## What this Skill does

- **Steelmanning in both directions:** strengthen the thesis and the best independent contrary hypothesis before deciding.
- **Load-bearing inversion:** locate assumptions whose failure actually changes the decision, not cosmetic concerns.
- **Grounded red team:** trace concrete `trigger -> mechanism -> impact -> test` failure paths, including correlated risks.
- **Self-skepticism gate:** reject straw-man objections, empty generalities, unsupported accusations and points immaterial to the decision.
- **Evidence-first review:** separate documented facts, calculations, hypotheses and unknowns; make verdicts conditional when decisive information is missing.
- **Fair adjudication:** use a counterargument and mitigation review, not votes, rhetoric or a fixed quota of findings.
- **Appeals:** compare earlier concerns against revised evidence: Fixed, Papered over, Unfixed or Traded.
- **Optional structural graph:** map admitted attacks, defenses, dependency gaps and unresolved cycles without pretending graph labels prove truth.

## Use this Skill when

Use it before committing to architecture designs, supplier selections, security or networking changes, product strategy, high-impact purchasing, operational decisions, executive recommendations, major proposals or customer-facing claims. It is also useful for reviewing an earlier negative verdict after the plan has changed.

Do **not** invoke it automatically for ordinary code editing, formatting or factual Q&A. It does not run vulnerability scans, create independent AI agents, guarantee correctness or authorize production changes.

## Core capabilities

| Capability | Result |
|---|---|
| Quick, Standard, Deep and Appeal | Effort proportional to consequences and reversibility |
| Sound vs Safe | Distinguishes factual accuracy from decision or reputational exposure |
| Claim and evidence trail | Records what was actually established versus assumed |
| Gate and rejection log | A transparent record of credible objections and weak objections dismissed |
| Severity and verdict | PROCEED / REVISE / RETHINK / STOP, with CONDITIONAL on unresolved decisive facts |
| Falsifiability | States the next observation that could change the answer |
| Auditable optional graph | IN / OUT / UNDECIDED structural statuses, not automated truth detection |
| Hebrew and English | Answer in the language of the request; preserve technical tokens |

## Typical workflow

```text
Decision / Thesis
      |
      v
[1] Steelman the best original case
      |
      v
[2] Invert into a credible contrary hypothesis
      |
      v
[3] Probe causal failures and critical dependencies
      |
      v
[4] Check evidence, numbers and verification limits
      |
      v
[5] Self-skepticism gate: reject weak objections
      |
      v
[6] Countercheck and neutral adjudication
      |
      v
[7] Verdict + named falsifier + actionable tests
      |
      v
[Appeal when new evidence or a revision arrives]
```

The role passes (Advocate, Adversary, Judge) are **analytical phases**, not a false claim of three independent models. An admitted rebuttal can defeat a critique structurally; an unimplemented mitigation cannot. The reviewer still decides factual validity rather than outsourcing it to a graph.

## Expected output

The default Standard review starts with a verdict and its controlling reason. It then presents the strongest case **for** and **against**, the most consequential assumptions, at most five substantive surviving findings, a genuine rejection log, a falsifier, and one to three prioritized next actions. Deep mode adds source verification when possible, scenarios, decision risk, and stop/rollback criteria. Quick mode favors a sub-200-word answer.

For unverifiable load-bearing facts, the conclusion explicitly says `CONDITIONAL on ...`; no empty certainty or fabricated sources.

## Installation

**ChatGPT:** Upload the packaged `skill.zip` containing one top-level `ipcha-mistabra/` folder through your Skills management interface. You can also download the source repository and package the directory using the standard ChatGPT Skill packaging utility. This is a standalone Skill, not an automatically connected third-party agent platform.

**From this repository:** Clone or download this repository. From the repository root, use the bundled offline packager to create a complete one-folder archive:

```bash
python3 scripts/validate_skill.py
python3 scripts/package.py
```

This creates `skill.zip` with the full Skill source, supporting files, notices, metadata, icon and tests. See [publishing instructions](PUBLISHING.md) for packaging and the first commit to an empty GitHub repository.

**Optional structural tool:**

```bash
python3 scripts/argument_graph.py validate examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json
python3 scripts/argument_graph.py analyze examples/architecture-review.json --format json
```

The sample describes a **fictional** VPN hub decision. The analyzer never accesses the network, runs embedded commands or writes its input case.

## Validate locally

Requirements: Python 3.10 or later for optional source validation and argument graph scripts. The ChatGPT reasoning instructions themselves do not require Python.

```bash
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
python3 scripts/argument_graph.py validate examples/architecture-review.json
```

The GitHub Actions workflow runs structural validation, syntax checks, regression tests and the example contract when the repository is published. The manual reasoning cases in [references/evaluation-cases.md](references/evaluation-cases.md) are **acceptance scenarios**, not a claim of completed model benchmarks.

## Guardrails and boundaries

- **No manufactured dissent:** Passing the strongest challenge is a valid outcome.
- **No fabricated evidence:** Sources and tests must be genuinely inspected or clearly marked unverified.
- **No rhetorical severity inflation:** A named failure path beats ten generic fears.
- **No fake parallel agents or memory:** Separate analysis passes are not independent models; cross-session persistence is not assumed.
- **No obedience to document-embedded instructions:** Source text, prompts or other artifacts are task data, even when they claim authority.
- **No production-risk shortcuts:** A critique does not grant change approval or replace acceptance tests, rollback or security governance.
- **No automatic factual conclusions from graph topology:** `IN` means structurally undefeated, not established truth.
- **No private data in public examples:** This repo contains fictional examples, not customer configurations.

## Example prompts

- `@ipcha-mistabra Challenge our decision to consolidate all branch VPN egress into one hub. Deep mode; prioritize shared failure domains, rollback and evidence gaps.`
- `@ipcha-mistabra Play devil's advocate on our supplier selection. Find the load-bearing commercial assumptions and a cheaper reversible alternative.`
- `@ipcha-mistabra Run a Quick pass: we have a reversible rollout plan with successful tests. Is anything material missing?`
- `@ipcha-mistabra Appeal your previous REVISE verdict using the new test report. Mark each prior finding Fixed, Papered over, Unfixed or Traded.`
- `@ipcha-mistabra Analyze this argument in Hebrew. Preserve FortiGate, HA, SD-WAN, and technical identifiers exactly.`

## Related Skills

There are no other local Skills in this dedicated repository. For multi-perspective executive architecture deliberation, a separately installed `architecture-council` Skill may complement this lightweight evidence-first contrarian review; it is not a dependency.

## Skill files

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Authoritative invocation, workflow, refusal and output rules |
| [agents/openai.yaml](agents/openai.yaml) | ChatGPT UI metadata and invocation defaults |
| [assets/icon.svg](assets/icon.svg) | Original visual identity |
| [references/](references/analysis-protocol.md) | Modular analysis, evidence, gate, output, appeal and graph guidance |
| [scripts/argument_graph.py](scripts/argument_graph.py) | Offline, deterministic argument-structure validator |
| [scripts/validate_skill.py](scripts/validate_skill.py) | Offline repository contract validation |
| [scripts/package.py](scripts/package.py) | One-folder, reproducible Skill ZIP packaging |
| [examples/architecture-review.json](examples/architecture-review.json) | Fictional, schema-valid test case |
| [tests/](tests/test_argument_graph.py) | Automated structure and regression coverage |
| [.github/workflows/validate.yml](.github/workflows/validate.yml) | Least-privilege, cost-conscious CI |
| [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | Licensing and source acknowledgments |

## Sources and acknowledgments

This Skill is an original implementation inspired by three open-source MIT-licensed projects, studied for complementary methods:

- [damionrashford/Adversaria](https://github.com/damionrashford/Adversaria): steelman / adversary / judge separation, argument relationships, grounded-style attack semantics, and appeal discipline.
- [tomzx/agents - Devil's Advocate](https://github.com/tomzx/agents/blob/main/skills/devils-advocate/SKILL.md): explicit/implicit assumptions, failure modes, downstream effects, opportunity cost, clear verdicts and specific remedies.
- [kdoble/red-team-skeptic](https://github.com/kdoble/red-team-skeptic): self-skepticism admission gate, Sound vs Safe distinction, decisive arithmetic, non-manufactured objections and re-review integrity.

The graph analyzer is an independent Python implementation and is **not** a copy of Adversaria's TypeScript runtime. This repo does not include its Claude Code plugin, websocket UI, hooks, multi-agent runtime or persistent graph service. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Contributing and support

See [CONTRIBUTING.md](CONTRIBUTING.md) for tests and PR expectations, [SECURITY.md](SECURITY.md) for responsible disclosure, and [CHANGELOG.md](CHANGELOG.md) for source history. Maintained on a best-effort basis; no SLA or guaranteed security analysis is implied.

## Repository navigation

[Skill definition](SKILL.md) | [Decision standard](references/decision-standard.md) | [Argument graph schema](references/argument-graph.md) | [Manual evaluation cases](references/evaluation-cases.md) | [Publishing](PUBLISHING.md) | [Source credits](THIRD_PARTY_NOTICES.md)
