# Instructions for Codex and other coding agents

Read this file and the actual source documents in `strategy/` before undertaking work.

## Source of truth
- `strategy/110-risks.md`: user-maintained inventory of 73 proposed Case B and 37 original risk identifiers.
- `strategy/334-subsublayers.md`: user-maintained canonical technical work packages.
- `strategy/116-projects.md`: user-maintained project descriptions and mappings.

**These strategy files have not yet been added.** Do not claim to have read them, or invent their contents, until they exist in the repository. Preserve their canonical IDs when they are provided.

## Initial assignment
- Work package: `6.1.1` — Enterprise application requirements, assets, roles and security objectives.
- Project: `P-006` — Secure-by-Default LLM Application Reference Architecture.
- Case B: `B-04` — User-Intent Misunderstanding.
- Case B: `B-05` — Security Constraint Omission.
- Reference system (to inspect, not assume): `https://github.com/open-webui/open-webui`.

## Working principles
1. Learn and document legitimate requirements before building tests.
2. Distinguish actual repository/source findings from assumptions, simulation, and proposed experiments.
3. Assess benign-origin failure modes without inventing an attacker in Case B.
4. Verify any security consequence against independent backend policy, source, telemetry, and receipts.
5. Never fabricate outputs, receipts, citations, findings, remediation results, or tests.
6. Use synthetic data and explicitly authorized targets.
7. Do not run destructive or privileged operations without an approved, isolated setup.
8. Produce reviewable, versioned and sanitized artifacts; request review before substantial changes.
