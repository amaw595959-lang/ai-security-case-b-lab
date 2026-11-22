# 6.1.1 — Enterprise application requirements, assets, roles and security objectives

**Canonical project:** P-006 — Secure-by-Default LLM Application Reference Architecture

**Initial Case B scenarios to design**
- B-04: User-Intent Misunderstanding.
- B-05: Security Constraint Omission.

**Reference application:** Open WebUI (inspect actual source and deployed configuration before making claims).

## First deliverables (design-stage completed; 2026-11-22)
- [x] Engagement scope and authorized reference target/version
- [x] User and workload identity inventory
- [x] Assets and sensitive resource classification
- [x] Role, permission and operation matrix
- [x] System context and trust boundary diagram
- [x] Testable security requirements and invariants
- [x] Proposed legitimate-use Case B scenarios
- [x] Independent verification methods and evidence plan

## Evidence and closure boundaries

**Design-stage status: CLOSED (2026-11-22).** All eight source-grounded design deliverables above have corresponding completed records. See the [formal closure report](closure-report.md), which reconciles the canonical acceptance gates, evidence and deferred work. The checkbox status refers to document/design completion **only**; it does not certify a live Open WebUI instance or learner competency.

| Artifact | Evidence / current status |
| --- | --- |
| Engagement scope, pinned source and exclusions | [Engagement scope](engagement-scope.md); deployed Open WebUI build and runtime authorization remain UNKNOWN |
| Human/workload identities, assets, roles and permissions | [Inventory](identities-and-assets.md); effective runtime identity and grants remain NOT_TESTED |
| Data flow and trust boundaries | [Trust-boundary model](trust-boundaries.md); eight source-grounded boundaries, proposed controls separated |
| Nine security requirements and seven invariants | [Requirements and invariants](security-requirements.md); existing source mechanisms versus proposed controls clearly distinguished |
| Four B-04/B-05 and control scenario designs | [Case B test design](case-b-test-design.md); independent expected results frozen before the run |
| Standalone offline practice | [Practice lab](practice-lab/README.md); 49 recorded passing pytest checks of fixed synthetic replies and isolated components |
| Real standalone model evaluation | [SmolLM2 evaluation](model-evaluation/results.md); five actual model calls, B-04 FAIL / B-05 FAIL for that exact artifact and settings; T01-C NOT_TESTED; independent AI-assisted raw-response review (not human sign-off) |
| Isolated REQ-07 backend demonstration | [HTTP/SQLite integration demo](req07-http-integration/README.md); independent rerun 20/20 tests and 6/6 T03 variants, merged PR #8; **not an Open WebUI integration** |
| Evidence quality, limitations, deferred gates | [Closure report](closure-report.md); 30/30 archived model SHA-256 items and 5/5 demo SHA-256 entries checked; unknown integration/retention and learner review remain OPEN |

**Required distinctions:** Model behavior failures are not proof of deployed Open WebUI authorization failures. The REQ-07 prototype is tested only as a stand-alone local HTTP/SQLite service with synthetic principals. REQ-08 real event, audit, storage, backup and retention enforcement is NOT_TESTED. Actual Open WebUI app/model/backend integration, runtime effects, human learner sign-off and independent unfamiliar-system transfer are NOT_TESTED or PENDING.

**Next work package:** **6.1.2 — Reference architecture, component inventory and data-flow design**, continuing to 6.1.3/6.1.4/6.1.5 for model integration, actual IAM/trust-boundary enforcement, deployment, REQ-07/REQ-08 runtime tests, ownership, remediation and retest.

**Safety:** Synthetic data only; no Open WebUI vulnerability or actual unauthorized external action is claimed.

