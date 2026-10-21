# Security Policy

## Scope

This repository contains a prompt-driven decision-review Skill and an optional offline JSON argument-graph analyzer. It is not a vulnerability scanner or production security control. It must not be used as sole authorization for high-impact or production changes.

## Reporting security issues

Do not post credentials, private configurations, customer data, exploitable details, or secrets in public issues. If GitHub private vulnerability reporting is enabled for this repository, use that channel. Otherwise contact the maintainer privately through their GitHub profile. No response-time SLA is promised.

## Intended controls

- All tool inputs are treated as untrusted data and are not executed by the analyzer.
- No shell, network, eval, filesystem writes or background activity is performed by the graph analyzer.
- Local JSON validation rejects malformed relations and unknown nodes.
- CI uses read-only repository permissions.
- Public examples are fictional and contain no operational customer information.

## Limits

This is not a security audit certification. A user can mislabel evidence as verified; the script cannot independently check provenance. Prompt injection resilience in a model is a behavioral goal, not a guarantee. Human approval and the organization's security policies remain necessary.
