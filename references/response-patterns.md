# Response Patterns and Examples

Keep the language of the user. With Hebrew responses, write fluent RTL prose while preserving product names, commands, interface names, IP addresses, CLI and URLs exactly. These are adaptable patterns, not mandatory walls of text.

## Quick (under ~200 words)

**Verdict:** PROCEED / REVISE / RETHINK / STOP [CONDITIONAL if required]. Reason in one sentence.

**Load-bearing premise:** the one assumption that controls the decision and its verification state.

**Best case for the opposite:** a fair, specific alternative explanation and why it matters.

**Gate note:** strongest candidate rejected (if any), with a few words why; otherwise state that no credible candidate was rejected. Do not invent a quota.

**Decisive next test:** test, expected outcome, what the decision becomes.

## Standard

**Verdict:** LABEL [CONDITIONAL on ...]. One paragraph stating the decisive mechanism.
**Verification:** checked sources/claims, skipped checks and limitations, no fake run claims.

### 1. Thesis / strongest defense
Quote the load-bearing claim when available. Give its strongest fair rationale and evidence.

### 2. Strongest contrary case
State a fully viable opposite hypothesis. What would distinguish H1 from H2?

### 3. Load-bearing assumptions

| ID | Exact premise | Status | Falsifier | Decision impact |
|---|---|---|---|---|
| A1 | ... | Documented / Inferred / Unknown | ... | ... |

### 4. Findings that survived the gate

| Priority | Target claim | Sound/Safe | Specific mechanism and impact | Strongest counter / residual risk | Required action |
|---|---|---|---|---|---|
| Critical/Major/Moderate | ... | ... | ... | ... | ... |

Show no more than five findings. If none survive, say so; do not pad.

### 5. Gate log

| Candidate objection | Outcome | Why |
|---|---|---|
| ... | Rejected / Reframed / Unresolved | ... |

If none were rejected, state `No credible candidates rejected; surfaces checked: <list>`. Do not create a fake one.

### 6. Decision boundary
State the falsifier and 1-3 prioritized actions (what to check, who if known, pass/fail criterion, subsequent decision). For serious risks include stop/rollback criteria.

## Deep additions

- Decision impact and reversibility; bounded worst credible case and dependency owner.
- Evidence ledger with source dates, versions, verification method and conflict resolution.
- 2-3 hypotheses and discriminating observations; sensitivity of decision to uncertain inputs.
- Architecture/security tests, when relevant, including production safeguards and rollback.
- Optional machine-readable argument graph using `scripts/argument_graph.py`, plus structural interpretation and the explicit disclaimer that graph labels are not truth.
- Any dissenting but unproven thesis listed as a testable minority report, not presented as established fact.

## Appeal / second pass

**Original verdict:** label and controlling reason.
**New record:** exactly what changed (source, artifact version, new facts).

| Prior finding | Current state | Mechanism removed? | New exposure? |
|---|---|---|---|
| ... | Fixed / Papered over / Unfixed / Traded | Yes / No / Unknown | ... |

**Revised verdict:** label or `unchanged`, plus precise movement. If the prior review missed something available at the time, acknowledge it; if the review stands, say so plainly.

## Illustrative example (not a real customer finding)

**Thesis:** Move all branch VPN egress to a single new hub because it reduces management overhead.

**Best defense:** One hub simplifies policy and support, if capacity and HA are proven.

**Best contrary hypothesis:** The new hub consolidates failure domains so total customer risk increases even if administration gets simpler.

**Finding:** The hub's independent failure-domain assumption is unverified. That is a blocking uncertainty, not proof of a SPOF. The deciding test must prove independent underlay, control plane, egress, failover and headroom under realistic load.

**Verdict:** RETHINK (CONDITIONAL on failure-domain and capacity evidence). Preserve existing path as rollback; approve a limited migration only after the specified failure tests pass.

This example is fictional. Never transpose its assertions to a real environment without evidence.
