# Analysis Protocol: Opposing Hypotheses Without False Balance

This is a conditional expansion of the seven stages in `SKILL.md`. Use it for Deep review, high-risk architecture decisions, and unclear causality.

## A. Define an answerable contest

Capture the decision in one sentence, the success metric, the decision window, who owns the risk, and alternatives including doing nothing. Split the thesis into independently testable claims rather than a narrative blob.

Build **H1**: the best defensible version of the user's thesis. Then build **H2**: the most plausible *different causal explanation or option*, not simply `not H1`. A useful contrary hypothesis makes different predictions. Also consider **H3**: a third option that avoids the apparent binary.

| Question | H1 | H2 | Why it matters |
|---|---|---|---|
| What would we observe if true? | Specific prediction | Distinguishing prediction | Enables discrimination |
| What evidence is already known? | Cited fact or unknown | Cited fact or unknown | Prevents rhetoric substituting for data |
| What could falsify it? | Test or observation | Test or observation | Forces intellectual risk on both sides |
| What does acting on it cost if wrong? | Downside and reversibility | Downside and reversibility | Grounds the decision |

Do not claim opposing explanations have equal probability unless comparable evidence supports that conclusion. A generous representation of an argument is not the same as endorsing its truth.

## B. Keep three review roles conceptually distinct

These are analysis **phases**, never an assertion that multiple independent agents ran.

1. **Advocate:** Create the strongest reasonable H1 from the actual claim, including its documented favorable conditions. Make its dependencies explicit.
2. **Adversary:** Build a plausible H2/H3, find load-bearing vulnerabilities and real decision reversals. Stress-test H1's strongest interpretation.
3. **Judge:** Check both cases symmetrically, inspect the evidence trail and rejected objections, and explain precisely why one conclusion controls the verdict.

If the judge discovers a stronger defense or flaw, revise the prior phase's claim openly. Avoid rhetorical theatrics. The judge must have a way to conclude "no significant objection survives."

## C. Target the critical path

1. **Problem validity:** Is the problem real, correctly defined, and important enough to solve now?
2. **Dependency validity:** What needs to be true technically, commercially, operationally, legally, and organizationally?
3. **Change-of-world check:** Would a previously correct assumption now be false due to scale, versions, vendors, regulation, staffing, or timing?
4. **Failure paths:** Write events in `trigger -> mechanism -> consequence -> detection -> recovery` form.
5. **Opportunity cost:** What better action is displaced? Would a bounded pilot resolve uncertainty sooner?
6. **Second-order effects:** Does the solution create vendor lock-in, new trust boundaries, concentration of failure, latent maintenance costs, or incentive changes?

Do not introduce a risk just because it belongs to a generic checklist. The path must plausibly reach the decision.

## D. Stakeholder and adversary lenses

Select relevant lenses; do not present an exhaustive checklist as findings:

- **Expert reviewer:** unsupported performance/security claims, incorrect primitives, missing comparative evidence.
- **Operator/SRE:** observability, on-call ownership, blast radius, rollback, recovery time, day-two maintenance.
- **Security/privacy/compliance:** trust boundaries, least privilege, exposure, data retention, legal obligations, exception handling.
- **Finance/procurement:** total cost, exit cost, concentration, commercial dependencies, contract mismatch.
- **Customer/end user:** experience, unacceptable downtime, hidden transition work, supportability.
- **Management/decision owner:** success criteria, approval authority, decision latency, downside asymmetry.
- **Hostile critic:** the strongest contextually valid counterexample or number that undermines a public claim.

An incentive is a reason to inspect evidence, never independent proof of dishonesty or error.

## E. Architecture and cybersecurity variant

When the case involves production networking or security, inspect only applicable dimensions:

- Data plane versus control plane, management plane, physical/shared dependencies, common-mode failures.
- HA failover paths, session continuity, state synchronization, routing convergence, last-mile and upstream diversity.
- Trust boundary movement, least-privilege policy, management access, logging, detection and response.
- Fortinet or vendor-specific behavior: version, model, license, capacity, relevant configuration and documented limitations (verify, do not assume).
- MTU/MSS, tunnel encapsulation, QoS and shaping interactions, realistic throughput under inspection.
- Observability, test traffic and acceptance evidence, staged deployment, rollback triggers and fail-safe state.

Never invent device commands, model limits, addressing, interfaces, measured latency, or an asserted vendor behavior. A design-level concern is not a confirmed configuration defect without evidence.

## F. Socratic discriminators

Prefer three questions that can change a decision over twenty that merely increase unease:

- Which single observation would force us to reject the favored explanation?
- What assumption is most important **and** most uncertain?
- If a competitor proposed the same plan, what specific evidence would we demand before approving it?
- What outcome would distinguish an implementation failure from an incorrect strategy?
- Which defense exists today, and which is only promised after deployment?

## G. Decision record

End Deep reviews with an explicit decision boundary: what to do now, what to measure, who should verify it (if known), and which result triggers approval, redesign, or stop. Preserve dissent as an unresolved hypothesis with a test, not as a decorative minority opinion.
