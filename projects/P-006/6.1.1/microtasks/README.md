# P-006 / 6.1.1 — Micro-task supplement

This review completes the documentation for the 14 micro-tasks within **Enterprise application requirements, assets, roles and security objectives**. It uses the synthetic Maple Calendar service notice in lab `P006-CASEB-LAB-01` and the source for Open WebUI `v0.13.4` at `0666e59d26a4d056e0bacee41742486badd71cf8`. The original design-stage closure dated 2026-11-22 governs the work package. This supplement records design decisions and scoped evidence from subsequent labs. Production authorization, organization-specific ownership and independent human acceptance remain open. [Original closure](../closure-report.md) · [Upstream pin](https://github.com/open-webui/open-webui/tree/0666e59d26a4d056e0bacee41742486badd71cf8)

## Read and study

| Document | What to use it for |
| --- | --- |
| [Micro-task coverage](microtask-coverage.md) | Compare each micro-task before and after. The 14 micro-task IDs name curriculum deliverables. The four T IDs below name evaluations. |
| [Business context and roles](business-context-and-roles.md) | Decide what the service desk needs and which people can request, approve or review each stage. |
| [Workload and asset accountability](workload-and-asset-accountability.md) | Identify each service identity, its credentials and permissions, and who should account for each data copy. |
| [Case A threat hypotheses](case-a-threat-hypotheses.md) | Compare the benign Case B failures with separate adversarial possibilities for the same boundaries. |
| [Objectives and impact](security-objectives-and-impact.md) | Explain what the fictional business stands to lose and select measurable checks. |
| [Requirements traceability](requirements-traceability.md) | Follow a claim forward from the business objective and backward from a test or receipt. |
| [Review and acceptance](review-and-acceptance.md) | Find approval and ownership gaps, evidence limits, and a learner exercise for every task. |

## Reviewed revisions

The base is GitHub `main` at `9475f31459bc7bc89d51fdf10c518e995f0701e8`. Relative links to existing repository files refer to the blobs at this commit. The Open WebUI source cites the exact upstream commit. Git ancestry and file presence establish what is in `main`. GitHub's public pull request pages confirm the target branches for #8, #9 and #13. The public list showed no open pull requests at the baseline check. The GitHub API was unavailable from the workspace. [Main snapshot](https://github.com/amaw595959-lang/ai-security-case-b-lab/tree/9475f31459bc7bc89d51fdf10c518e995f0701e8) · [Agent instructions](../../../../AGENTS.md) · [Risk inventory](../../../../strategy/110-risks.md) · [Work packages](../../../../strategy/334-subsublayers.md) · [Project catalog](../../../../strategy/116-projects.md)

| Record | Git provenance and evidence boundary |
| --- | --- |
| Original 6.1.1 design, lab and standalone model | PRs #1–#7 enter the first-parent history of `main`. The GitHub pages record #8 and #9 as merged to `main`. The branch contains the HTTP/SQLite acceptance at `abf034033ecbb73cfcfc0dd792abc2d075106a02` and design closure at `2ff31d5cb49a7b12bb95b692de748d12745914eb`. The PR #9 head `ef29be4fae423d3215814947dcb5af97dd3a32c8` has the same tree as the closure commit. [Git history](https://github.com/amaw595959-lang/ai-security-case-b-lab/commits/9475f31459bc7bc89d51fdf10c518e995f0701e8/) · [PR #8](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/8) · [PR #9](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/9) |
| Phase A, 6.1.3 | PR #10 entered `main` at `1afc9ae8ec0af3b036ed4321d28f636544b8150e`. Comparative standalone model behavior. [PR #10](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/10) · [Report](../../6.1.3/phase-a-multi-model/report.md) |
| Phase B, 6.1.4 | PR #11 entered `main` at `760b044cdc9fd1993113da9869cc0631a17fe2d6`. Pinned Open WebUI with a separately added preview route, local model and synthetic accounts. [PR #11](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/11) · [Report](../../6.1.4/phase-b-req07/report.md) |
| Phase C, 6.1.5 | PR #13 head `949cde98871379051ae8cf0af6ed8bd9aa75eaca` was merged at `fe90ab3bf700e9f036cc12efbf50c4ba26dc99f9` into `p006/6.1.4-phase-b-req07`. Both commits are outside `main` at the reviewed baseline. The pinned report describes local comparison and controlled REQ-08 runs. [PR #13](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/13) · [Branch merge](https://github.com/amaw595959-lang/ai-security-case-b-lab/commit/fe90ab3bf700e9f036cc12efbf50c4ba26dc99f9) · [Pinned Phase C report][phase-c] |
| Phase D, P-099 / 6.8.8 | PR #12 entered `main` at `9475f31459bc7bc89d51fdf10c518e995f0701e8`. The public candidate brief, fictional fixture, review commitment and rubric supply an assessment plan. Learner submission and human review require separate evidence. [PR #12](https://github.com/amaw595959-lang/ai-security-case-b-lab/pull/12) · [Candidate materials](../../../P-099/6.8.8/p006-transfer-assessment/candidate.md) · [Assessment](../../../P-099/6.8.8/p006-transfer-assessment/assessment.md) |

## Reused design work and study checks

### MT02 — Legitimate AI use cases and workflows

The service desk wants a quick, accurate maintenance draft. In ordinary chat the analyst supplies fictional notes, the assistant asks about an ambiguous audience or drafts for a clear audience, and the analyst reviews the private candidate. The proposed gate uses separate approval for an employee-ready preview. The draft-only scope excludes real delivery. This saves drafting effort while keeping the audience and facts under human control. [Workflow](../engagement-scope.md#proposed-workflow-and-risk-status) · [Source and design flow](../trust-boundaries.md#case-b-through-the-ordinary-notice-workflow)

- **How to verify and use it.** The learner should draw the sequence from the analyst to private chat and preview, then mark who provides the audience and who confirms the facts. Use the frozen fixture and T01–T03 criteria as documentary evidence. A consultant uses that flow to agree the normal task and authorized effects with the workflow sponsor. B-04 and B-05 apply to boundaries 1–5, with boundary 8 excluding delivery. REQ-01, REQ-02, REQ-06 and REQ-07 and INV-04 and INV-05 capture the relevant behavior and limits. The analyst and assigned reviewer are lab roles. Confirming a named business sponsor remains pending. The existing workflow meets the design criteria. [Fixture](../case-b-test-design.md#synthetic-notice-fixture) · [Business decisions](business-context-and-roles.md#mt01--enterprise-business-context-and-scope)

### MT06 — Operations, authority and permission requirements

For each operation, identify who may act, on which resource and under which conditions. That helps distinguish a standard analyst's own-chat access from an administrator's separate configuration authority. The baseline inventory already follows source permission checks for reading and writing a saved chat, choosing a managed model, changing settings and excluded sharing. REQ-03 through REQ-07 and REQ-09 supply the policy and evidence checks. INV-01 through INV-05 and INV-07 cover actor, resource, destination, preview and evidence. Boundaries 1–5 and 8 apply to containment of B-04/B-05. [Role matrix](../identities-and-assets.md#initial-role-and-permission-matrix) · [Requirements](../security-requirements.md)

- **How to verify and use it.** Choose one allowed and one denied operation. Trace the identity dependency, exact resource predicate and subsequent state change in the cited source. The source predicates and expected decision are documentary evidence. An authorized runtime assessment also needs effective grants and state or destination observations. Phase B verifies specific routes and identities only. A consultant uses the result to agree a permission matrix with the application and identity owners. Assignments outside the synthetic lab remain pending. [Phase B observations](../../6.1.4/phase-b-req07/report.md#application-and-policy-checks) · [Owner decisions](review-and-acceptance.md#decisions-still-open)

### MT07 — High-level system context and trust boundaries

A boundary is a point where data or authority changes hands. The existing diagram covers the browser, backend, chat and policy stores, model, private reply, preview, events, logs and excluded routes. Each numbered boundary names an expected control, a mistake that could occur, and evidence to check. It covers B-04/B-05 and all nine REQs and seven INVs across boundaries 1–8. [Boundary diagram and checks](../trust-boundaries.md#architecture) · [Reverse boundary map](requirements-traceability.md#reverse-indexes)

- **How to verify and use it.** Trace the private note through the numbered diagram and mark where an extra copy could appear. Compare boundaries 6 and 7 with the pinned event and audit symbols. The diagram, source citations and mapped controls meet the design criterion. A consultant compares an equivalent diagram with each actual deployment and asks the platform and data custodians to confirm where covered stores and consumers reside. Production topology and those assignments remain unknown. [Preview and logging source paths](../trust-boundaries.md#message-previews-and-other-content-in-events-or-logs)

### MT08 — Case B — AI-originated failure scenarios

The existing scenarios model an ordinary request. B-04 is an assistant guessing what “the team” means. B-05 is an assistant dropping the instruction to omit an internal field or mishandling the approved facts. T01 and T02 score the response against rules learned from the notice policy. T03 and T04 check separate backend containment at boundaries 5–8 and in private storage, using REQ-07 through REQ-09 and INV-04 through INV-07 where applicable. REQ-01 and REQ-02 directly score the model path. [Test design](../case-b-test-design.md#model-behavior-checks) · [Original observations](../model-evaluation/results.md) · [Phase A](../../6.1.3/phase-a-multi-model/report.md)

- **How to verify and use it.** Write the expected first reply or required fields before reading each saved response, then score it yourself. Check the conditional follow-up record to understand why it was skipped. The fixture, raw attempts and case-by-case verdicts meet the design criterion and support only their respective runs. A consultant uses the distinction between a wrong reply and a backend effect to define the extent of a finding. The model evaluation reviewer owns the score in a future assessment. Human scoring of the archive and transfer remain pending. [Recorded evidence](requirements-traceability.md#evidence-register)

### MT11 — Non-negotiable security invariants

An invariant is a rule that stays true when the model is wrong. The seven existing properties cover caller authority, exact chat access, model routing, draft-only effects, safe preview, private copies and evidence. They apply across boundaries 1–8 and contain effects related to B-04 and B-05. The REQ to INV mappings and backend checks already provide design evidence. [Canonical invariants](../security-requirements.md#security-invariants)

- **How to verify and use it.** Pick INV-05 and compare a fixed wrong candidate with the recorded approval and ready preview. Identify which independent observations support that property and which deployment conditions are still unknown. A consultant uses the invariant as a release condition that engineering and the workflow sponsor can verify separately from model quality. The closure preserves the design verdict and the assigned human retest roles remain pending. [T03](../case-b-test-design.md#p006-611-t03--proposed-req-07-employee-ready-preview) · [Design closure](../closure-report.md#5-requirements-invariants-and-what-was-actually-established)

### MT12 — Measurable security requirements

The nine existing requirements say what should happen, which layer is responsible, and what observation would count as pass or fail. REQ-01 and REQ-02 measure model behavior for B-04 and B-05. REQ-03 through REQ-09 govern authority, containment and evidence across boundaries 1–8 and link to the seven invariants. Those objective criteria are already present. The trace ledger shows the exact implementation scope with evidence. [Requirements](../security-requirements.md) · [Trace ledger](requirements-traceability.md#forward-trace)

- **How to verify and use it.** Take REQ-08 and name both an allowed record that must arrive and an excluded category that must stay out. Identify the evidence required at the destination and in storage. Source, verifiable conditions and the separate oracle meet the design criterion. A consultant uses the criteria to agree the work with the relevant implementer and independent reviewer and to call unobserved paths out of scope. The owned production policy and coverage of its destinations remain open. [T04](../case-b-test-design.md#p006-611-t04--proposed-req-08-storage-event-and-log-handling) · [Acceptance register](review-and-acceptance.md)

### MT13 — Independent verification and evidence design

An oracle says what should happen before an observation is collected. The existing design uses T01/T02 for model responses and T03/T04 for control outcomes. Invariants INV-04 through INV-07, requirements REQ-06 through REQ-09, and boundaries 2 and 4–8 guide state and sink observations. The rubric, authorized scope, raw receipts and digests are different parts of the review trail for B-04/B-05. [Test design](../case-b-test-design.md) · [Evidence gates](../closure-report.md#6-master-strategy-eight-acceptance-gates--scoped-disposition)

- **How to verify and use it.** Verify the manifest of one archived run and use the prewritten rubric and raw receipt to trace one verdict. A missing destination observation can make an otherwise executed check inconclusive. A consultant uses this structure to make a claim reproducible and to distinguish model responses from effects observed by the backend or destination. A designated independent human reviewer must still assess learner work. Follow the Phase D working conditions for the separate transfer exercise. [Evidence register](requirements-traceability.md#evidence-register) · [Candidate brief](../../../P-099/6.8.8/p006-transfer-assessment/candidate.md#working-conditions)

[phase-c]: https://github.com/amaw595959-lang/ai-security-case-b-lab/blob/949cde98871379051ae8cf0af6ed8bd9aa75eaca/projects/P-006/6.1.5/phase-c-req08/report.md
