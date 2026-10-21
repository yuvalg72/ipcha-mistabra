# Source acknowledgments and third-party notices

Ipcha Mistabra is original source authored for this repository, incorporating **methodological ideas** from the following projects. It does not bundle their source implementations, Agent prompts, plugin runtimes, local state systems, or web assets.

## Open-source sources reviewed

1. **Adversaria**, by Damion Rashford. https://github.com/damionrashford/Adversaria . MIT License, Copyright (c) 2026 Damion Rashford. Concepts considered: steelman, adversary, judge, graph relations, defeat of attacks, appeals.
2. **Devil's Advocate** within `tomzx/agents`, by Tom Rochette. https://github.com/tomzx/agents/blob/main/skills/devils-advocate/SKILL.md . Repository MIT License, Copyright (c) 2025 Tom Rochette. Concepts considered: explicit and implicit assumptions, failure modes, blind spots, opportunity cost, second-order effects.
3. **Red Team Skeptic**, by Ken Doble. https://github.com/kdoble/red-team-skeptic . MIT License, Copyright (c) 2026 Ken Doble. Concepts considered: rejection of generic objections, separate Sound/Safe review, objective admission tests, arithmetic re-derivation, appeals.

The corresponding original repositories contain the definitive license texts and their own attribution requirements. No endorsement or affiliation is claimed. The MIT license for this repository applies to its original source, not a relicensing of third-party projects.

## What was not transplanted

The graph engine is newly implemented in Python using standard grounded-attack concepts. There is no claim of technical equivalence with Adversaria's full TypeScript engine, WebSocket transcript, persistent memory, Claude-specific hooks, runtime agent dispatch, or verdict API. The ChatGPT Skill simulates role-separated reasoning **within one model pass** unless the host independently supplies multiple agents.
