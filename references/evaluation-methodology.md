# Measuring decision quality (not just repository correctness)

> **Evidence status:** This document is an evaluation protocol, not a completed experiment. Unit tests, valid JSON, green CI and clean graphs cannot establish that the Skill improves real decisions.

## Three distinct claims

1. **Structural validity:** Does the JSON validate, do graph attacks/dependencies follow deterministic rules, and do CLI tools exit predictably? Check with regression tests and CI.
2. **Evidence sufficiency:** Do individual claims have credible, relevant, independently reviewed evidence? The graph only reads reviewer-*declared* `verification` labels. **No boolean named "verified" is a fact check.** An unsupported rebuttal can make a claim structurally `IN`; `evidence_gate` must still surface its gap.
3. **Decision quality:** Are users actually better served: fewer consequential missed issues, fewer manufactured critiques, more accurate sourcing, better-calibrated uncertainty and more actionable recommendations? This requires an **independent controlled evaluation**, and ultimately real outcome tracking.

## Pre-register a paired, blinded evaluation

- Build at least **40-60 diverse holdout cases** *before examining treatment results*. Include favorable/no-problem situations, high-impact but under-specified decisions, conflicting data, numerical traps, network/security architectures, institutional consensus, and mistaken source claims. No proprietary customer materials.
- For each case define, using **two independent domain reviewers** with adjudication of disagreement, a reference set of **material issue IDs** and a set of acceptable verdicts. A legitimate minority opinion is not automatically a false positive. Record a plausible falsifier and evidence expected of a good recommendation.
- Run the **same frozen test prompt and identical provided materials** twice: (A) baseline assistant without the Skill and (B) same model and tools with the Skill. Record model/version, timestamp, tool availability, temperature or effort if controllable, prompt hashes, and the exact `SKILL.md` commit. Randomize response presentation order for human scorers.
- Preserve raw outputs and judge each *blindly*, not by visible A/B labels. Annotate detected issue IDs and **unsupported claims**, give 1-5 scores for source fidelity, actionability, and overall decision quality using anchored rubric below. Resolve disagreements *before* running the aggregate scorer.
- Report sample size and breakdown by decision type / stake level. Compute paired uncertainty intervals (e.g. case-level bootstrap resampling), not just percentages. Repeat across multiple seeds/model runs for unstable generation settings. Do not promote a synthetic demonstration to empirical evidence.
- Pre-register success thresholds before examining results. **Example acceptance hypothesis:** improve material-issue recall by >= 0.10 while avoiding an increase of > 0.10 false objections per case and without degrading source fidelity or decision-quality scores. The thresholds are proposed engineering acceptance criteria, **not measured effect sizes**.
- Follow up on **real-world decisions** where lawful and practical: actual failure rates, cost of mistaken recommendations, near misses, rollbacks, time-to-decision, and observed downstream impact. Benchmark ratings remain proxies, not outcome proof.

### Blind human grading rubric

Use a five-point anchored scale for three scores:
- **Source fidelity:** 1 = invented/contradicted essential sources; 3 = mostly traceable with material caveats; 5 = faithfully traceable, dated, version-scoped support and explicit unknowns.
- **Actionability:** 1 = generic or inoperable; 3 = some workable follow-up lacking acceptance conditions; 5 = prioritized tests, owner where known, concrete acceptance/falsification and rollback when relevant.
- **Decision quality:** 1 = credibly harmful/wrong decision based on supplied facts; 3 = defensible but materially incomplete; 5 = best evidence-supported and appropriately calibrated among real alternatives.

For **detected issue IDs**, map only genuinely material critiques to a pre-adjudicated reference identifier. A critique not in the accepted reference set is counted as a false positive *only after adjudication*, not automatically because it is novel. A missed gold issue is a false negative. For **no-material-objection cases**, the correct response may be `PROCEED`.

**Unsupported claims** counts case-specific material assertions presented as fact but unsupported by the provided/retrieved evidence. It is not the count of clearly labeled hypotheses.

## Offline annotation scorer

Populate the schema demonstrated in `examples/evaluation-ledger.synthetic.json` with **real blinded, independently adjudicated annotations**. For each case supply:

- `id`, `segment`, `gold_issue_ids`, `acceptable_verdicts`.
- Parallel `baseline` and `skill` objects, each with `issue_ids`, `verdict`, `unsupported_claims`, `source_fidelity`, `actionability`, `decision_quality`.
- Set `dataset_kind` to `human_adjudicated` only after completing that process. Store model settings and reviewer methodology in a separately versioned run manifest.

```bash
python3 scripts/score_evaluations.py examples/evaluation-ledger.synthetic.json
python3 -m unittest discover -s tests -v
```

The command compares aggregate precision, recall, false objections per case, acceptable verdict rate, unsupported factual assertions, and mean human quality scores, plus per-segment breakdowns. It **does not** call a model, invent reference labels, independently verify graders, estimate statistical significance, or approve a release.

**Metric limitations:** Precision and recall depend on an adjudicated list that can itself miss valid critiques. Source/actionability/quality scores are subjective even with a rubric. Acceptable verdicts must permit multiple defensible decisions in uncertainty; otherwise label quality becomes overfitting to the gold author's preference. Aggregate improvements may mask failures in the highest-risk subgroup.

### Release claim discipline

| What passed | Permitted claim |
|---|---|
| Schema/CLI/CI unit tests | "The structural contract and tested cases behave as implemented." |
| Human review of specific evidence | "These claims were checked by named reviewers within this scope." |
| Controlled evaluation with intervals | "The Skill improved the measured outcomes on this specified dataset and model, with stated uncertainty." |
| Longitudinal operational outcomes | "Observed decision outcomes improved in this monitored context"; never imply universal proof. |

Never claim "proven to improve decisions" based only on a green workflow, graph labels, or the **synthetic** scoring example.
