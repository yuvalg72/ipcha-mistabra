# Appeal and Re-Review Protocol

Do not rerun a previous decision review as though no record exists. An appeal checks whether the *reasoning or evidence changed*.

## Inputs

- Original thesis and version / timestamp if available.
- Prior verdict, promoted findings, gate log, falsifiers, and verification caveats.
- Updated plan or evidence, including what changed and what did not.

If the old decision record is unavailable, explain that the result is a fresh review, not a proven comparison. Do not invent old findings.

## Audit the old record before looking for new attacks

Classify each prior issue:

- **Fixed:** the observed failure mechanism is removed and the relevant acceptance test passes (where test evidence exists).
- **Papered over:** wording or diagram changed but the failure path remains.
- **Unfixed:** the issue remains materially unchanged.
- **Traded:** the fix removed one exposure but introduced another meaningful one.

Mark **Unverified fix** if the new design claims a safeguard but no operational evidence proves it. A planned mitigation is never equivalent to a deployed, tested mitigation.

## Permissible grounds for change

1. New or corrected primary evidence alters a decisive premise.
2. The original reviewer attacked a straw man or ignored a credible defense.
3. A key assumption was not tested or an important attack was mistakenly excluded.
4. A prior conclusion rested on conflicting or missing figures.
5. A material control changed state, from planned to implemented and verified (or the reverse).
6. A previously unseen failure interaction changes the consequence.

Do not reverse an opinion merely to seem independent. It is valid to confirm the original verdict after appeal.

## Replay and report

Run the opposing-hypothesis and objection-gate process on the **changed** material while retaining the original state as an audit trail. Explain each movement as `prior claim/status -> new claim/status: new evidence or counterattack`. Separate new weaknesses from old misses. An old miss that was inferable on the first pass should be identified as a quality correction, not disguised as a new discovery.

If the revision narrows the claim so aggressively that it no longer achieves the user's objective, call that out even if the wording is now defensible. A technically safe but useless recommendation is not a successful appeal.

Conclude: verdict affirmed / revised, what specific evidence changed it, remaining blockers, and next tests. No silent mutation of past reports.
