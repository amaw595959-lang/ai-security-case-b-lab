# AI Security Engineering — Final Complete 10 Layers, 57 Sublayers and 334 Sub-sublayers (Case B First, 2026+)

**Canonical source:** `AI_Security_10_Layers_Complete_Sub_Sublayers_2026.md`. Canonical IDs, titles and P-project assignments are reproduced verbatim in the full checklist below. Sub-layer B-risk tags are **new proposed overlays** derived from the later 73 Case B risk categories; they do not modify the originals or prove tests have been executed.

**Inventory:** 10 layers · 57 sublayers · 334 sub-sublayers · 116 canonical projects · 73 Case B risks · 37 original risks.

**Method:** B (ordinary AI-origin failure or normal baseline) → A (adversarial counterpart when applicable) → C (independent control enforcement, evidence, remediation and retesting). For infrastructure and attacker-only sublayers, establish a clean baseline rather than fabricating a B failure.

**Structure:** Keep the original layer order `L6 → L8 → L5 → L2 → L9 → L7 → L4 → L3 → L1 → L10`; use cross-layer prerequisites to begin L3 evaluations and L8 authorization early. The 9-phase risk-priority list is a separate **learning-priority queue**, not a replacement for these technical layers.

## Stage 0 — Shared foundations (build once; reuse throughout)

- [ ] `P-001` Reproducible lab and infrastructure
- [ ] `P-002` Synthetic enterprise data and identities
- [ ] `P-003` Authorized engagement scope and rules
- [ ] `P-005` Threat models and trust boundaries
- [ ] `P-009` Receipts, telemetry and evidence
- [ ] `P-007` Independent regression checks
- [ ] `P-008` Test datasets and evaluation pipeline
- [ ] `P-010` Client-style reporting

## Updated B-first priority queue (no renumbering)

| Wave | Pull these existing work packages forward |
|---|---|
| 0. Minimum safe backbone | Stage 0 projects above |
| 1. Define invariants and independent oracles | `6.1.1–6.1.5`, `3.1.1–3.1.5`, `7.2.1` |
| 2. Authorization and approvals before privileged actions | `8.1`, `8.3`, `8.5`, `6.4` |
| 3. Benign agent errors and tool decisions | `6.5`, `6.6`, `6.4`, `6.8.2` |
| 4. Information integrity and leakage | `5.1–5.5`, `6.8.1`, `3.3` |
| 5. AI coding, runtime and supply chain | `6.7`, `2.3–2.7`, `6.8.3` |
| 6. Operational detection and recovery | `7.2–7.5`, `6.8.4` |
| 7. Model/provider/governance specialist assessments | remaining L3/L4/L9/L1/L10 relevant IDs |
| 8. Full-scope verification | `6.8.5–6.8.8`, `P-099` |

## Full canonical inventory with proposed Case B upgrades

## Layer 6 — AI Application & Autonomous Agent Security

### 6.1 — AI Application Foundations

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-04`, `B-05`

- **Benign-origin / baseline:** Specify legitimate-use, model-error and unsafe-action requirements for the enterprise assistant; observe normal requests and ambiguity.
- **Adversarial counterpart:** Introduce an attacker-controlled instruction or data source only after the legitimate failure path is understood.
- **Control, evidence and retest:** Map assets, actors, model boundaries and policy-owned enforcement; independently check source, expected outcomes and receipts.

- [ ] **6.1.1** — Enterprise application requirements, assets, roles and security objectives — `P-006`
- [ ] **6.1.2** — Reference architecture, component inventory and data-flow design — `P-006`
- [ ] **6.1.3** — LLM API integration, orchestration and secure defaults — `P-006`
- [ ] **6.1.4** — Authentication, authorization, secrets and application trust boundaries — `P-006`
- [ ] **6.1.5** — Application deployment, observability and baseline verification — `P-006`
- [ ] **6.1.6** — Automated application, route, endpoint and service discovery — `P-004`
- [ ] **6.1.7** — API, model, tool, connector and identity attack-surface mapping — `P-004`
- [ ] **6.1.8** — Discovery accuracy, configuration drift and architecture verification — `P-004, P-006`

### 6.2 — LLM Instruction & Output Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-05`, `B-40`, `B-61`

- **Benign-origin / baseline:** Test ordinary wrong outputs, fabricated claims, schema mistakes and lost instruction context.
- **Adversarial counterpart:** Test direct malicious instructions and unsafe generated output crossing a downstream consumer.
- **Control, evidence and retest:** Validate schema, untrusted strings, quoting and output sinks independently of model text.

- [ ] **6.2.1** — Instruction hierarchy and trusted versus untrusted input boundaries — `P-021`
- [ ] **6.2.2** — Direct prompt injection test cases and attacker objectives — `P-021`
- [ ] **6.2.3** — System instruction disclosure and confidentiality tests — `P-029`
- [ ] **6.2.4** — Hidden context, tool traces and reasoning-artifact exposure tests — `P-029`
- [ ] **6.2.5** — Output schemas, encoding, escaping and unsafe rendering — `P-030`
- [ ] **6.2.6** — Model output to command, query, script and API injection chains — `P-030`
- [ ] **6.2.7** — Defense regression, failure classification and evidence capture — `P-021, P-029, P-030`

### 6.3 — Indirect & Multimodal Injection Security

**Practice role:** `SUPPORT` · **Proposed Case B risk links:** `B-13`

- **Benign-origin / baseline:** Test normal image/audio/video/structured-data recognition errors and metadata ambiguity without an attacker.
- **Adversarial counterpart:** Use attacker-controlled webpage, tool result, image, audio, video or structured file to test instruction promotion.
- **Control, evidence and retest:** Distinguish perception/model error from injection; verify provenance and downstream decisions.

- [ ] **6.3.1** — Browser navigation, DOM content and webpage instruction injection — `P-023`
- [ ] **6.3.2** — Web search results, links and retrieved page trust boundaries — `P-023`
- [ ] **6.3.3** — External API responses, tool returns and structured tool-result injection — `P-024`
- [ ] **6.3.4** — Image-embedded adversarial instructions and vision processing — `P-025`
- [ ] **6.3.5** — Audio transcripts, speech streams and spoken instruction injection — `P-026`
- [ ] **6.3.6** — Video frames, captions, timestamps and subtitle injection — `P-027`
- [ ] **6.3.7** — CSV, spreadsheet, JSON and structured-data instruction injection — `P-028`
- [ ] **6.3.8** — Multimodal transformation chains, provenance and regression tests — `P-023, P-024, P-025, P-026, P-027, P-028`

### 6.4 — MCP, Tool & External Action Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-14`, `B-26`, `B-27`, `B-28`, `B-29`, `B-31`, `B-33`, `B-64`, `B-66`

- **Benign-origin / baseline:** Have a benign request yield a wrong tool, argument, write action, or ungrounded success report.
- **Adversarial counterpart:** Try a malicious tool description, tool result, parameter, or instruction attempting the same unsafe effect.
- **Control, evidence and retest:** Confirm server-side authorization, strict schema validation, transaction receipts and tool-side audit records.

- [ ] **6.4.1** — MCP discovery, tool inventories and server trust boundaries — `P-041`
- [ ] **6.4.2** — Tool descriptions, names and selection manipulation — `P-041`
- [ ] **6.4.3** — Parameter schemas, argument validation and tool-result integrity — `P-041`
- [ ] **6.4.4** — Delegated tool identity, credentials and authorization handoff — `P-041, P-048`
- [ ] **6.4.5** — Read versus write tools and least-privilege action policies — `P-048`
- [ ] **6.4.6** — Unauthorized transactions, outbound requests and action sequences — `P-048`
- [ ] **6.4.7** — High-impact action approvals, replay defenses and audit evidence — `P-048`

### 6.5 — Autonomous Agent & Memory Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-10`, `B-23`, `B-24`, `B-25`, `B-32`, `B-35`, `B-36`, `B-37`, `B-38`, `B-45`, `B-46`, `B-54`, `B-55`, `B-56`, `B-57`, `B-71`, `B-72`, `B-73`

- **Benign-origin / baseline:** Test misunderstood goals, stale memory, excessive plans and unrequested subgoals from benign prompts.
- **Adversarial counterpart:** Test deliberate goal hijacking, memory poisoning and injected instructions within the same workflow.
- **Control, evidence and retest:** Confirm action budget, state transitions, memory provenance, stop rules, rollback and goal-bound receipts.

- [ ] **6.5.1** — Short-term context, persistent memory and state lifecycles — `P-046`
- [ ] **6.5.2** — Memory write permissions, poisoning entry points and provenance — `P-046`
- [ ] **6.5.3** — Persistent instruction contamination and cross-session influence — `P-046`
- [ ] **6.5.4** — Agent objectives, permitted plans and workflow state transitions — `P-047`
- [ ] **6.5.5** — Goal hijacking, task drift and excessive autonomy scenarios — `P-047`
- [ ] **6.5.6** — Action budgets, termination conditions, memory repair and retesting — `P-046, P-047`

### 6.6 — Multi-Agent & A2A Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-34`, `B-39`, `B-60`, `B-61`

- **Benign-origin / baseline:** Propagate a nonmalicious mistaken agent message and observe validation, coordination and loops.
- **Adversarial counterpart:** Submit forged or adversarial inter-agent messages and unauthorized handoffs.
- **Control, evidence and retest:** Verify sender authentication where applicable, downstream verification, limits, independent decisions and containment.

- [ ] **6.6.1** — Multi-agent architecture, responsibilities and communication pathways — `P-049`
- [ ] **6.6.2** — Agent message identity, provenance and trust boundaries — `P-049`
- [ ] **6.6.3** — Spoofed agent messages, malicious handoffs and delegated instructions — `P-049`
- [ ] **6.6.4** — Compromised-agent propagation and cascading failure scenarios — `P-049`
- [ ] **6.6.5** — Coordination loops, resource limits and failure containment — `P-049`
- [ ] **6.6.6** — Recovery, compromised-agent isolation and post-incident regression — `P-049`

### 6.7 — AI Coding Agent Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-18`, `B-19`, `B-20`, `B-37`

- **Benign-origin / baseline:** Ask the coding agent for a legitimate change; detect insecure generated code, incorrect permissions and false pass claims.
- **Adversarial counterpart:** Add malicious repository or issue instructions and compare resulting code/tool changes.
- **Control, evidence and retest:** Inspect code diff, CI logs, test results, sandbox policies, reviewer approval and deployment gates.

- [ ] **6.7.1** — Coding-agent roles, workspace permissions and repository trust model — `P-051`
- [ ] **6.7.2** — Repository instruction files, issue text and pull-request injection — `P-051`
- [ ] **6.7.3** — Workspace file access, shell execution and secrets exposure — `P-051`
- [ ] **6.7.4** — Tool approvals, development sandbox and repository change controls — `P-051`
- [ ] **6.7.5** — AI-generated code requirements, unsafe patterns and attack surfaces — `P-053`
- [ ] **6.7.6** — Static analysis, dependency checks and generated-code test gates — `P-053`
- [ ] **6.7.7** — Secure pull-request review, remediation and CI regression — `P-051, P-053`

### 6.8 — Enterprise AI Security Engagements

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-47`

- **Benign-origin / baseline:** Complete end-to-end benign-failure engagement covering incorrect model output, actions and consequences.
- **Adversarial counterpart:** Repeat matching adversarial scenarios against the same business invariants and approved scope.
- **Control, evidence and retest:** Deliver verified findings or non-findings, architecture, test cases, negative controls, remediation and independent client-facing defense.

- [ ] **6.8.1** — Enterprise RAG knowledge-assistant assessment engagement — `P-091`
- [ ] **6.8.2** — Financial operations agent transaction and approval assessment — `P-092`
- [ ] **6.8.3** — Enterprise coding assistant identity, repository and CI/CD engagement — `P-093`
- [ ] **6.8.4** — Multi-tenant customer support data and application assessment — `P-094`
- [ ] **6.8.5** — Multi-cloud AI platform architecture, cloud trust and scope design — `P-099`
- [ ] **6.8.6** — Integrated agent attack-path and cross-layer control evaluation — `P-099`
- [ ] **6.8.7** — Full-scope purple-team execution, incident scenarios and retesting — `P-099`
- [ ] **6.8.8** — Client-style reports, risk acceptance and independent technical defense — `P-091, P-092, P-093, P-094, P-099`

## Layer 8 — Identity, Authorization & Control Plane Security

### 8.1 — Cloud Workload Identity & Trust Federation

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Ensure ordinary workload identity mistakes or expired/revoked temporary credentials cannot cause privileged actions.
- **Adversarial counterpart:** Test impersonation, replay, incorrect audience/scope and policy abuse on synthetic principals.
- **Control, evidence and retest:** Use real issuer/verifier policy and negative authorization decisions; never trust model-proposed identity claims.

- [ ] **8.1.1** — Workload principals, service identities and credential inventory — `P-011`
- [ ] **8.1.2** — Federated identity assertions, trust policy and token exchange — `P-011`
- [ ] **8.1.3** — Service account impersonation, delegation and privilege paths — `P-013`
- [ ] **8.1.4** — Temporary credentials, scope restrictions and session binding — `P-011, P-013`
- [ ] **8.1.5** — Cross-cloud trust relationships and transitive privilege analysis — `P-020`
- [ ] **8.1.6** — Identity revocation, auditability and negative authorization tests — `P-011, P-013, P-020`

### 8.2 — OAuth Delegation & Identity Sessions

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-06`

- **Benign-origin / baseline:** Test legitimate agent user switching, session expiration and stale consent during ordinary operations.
- **Adversarial counterpart:** Attempt scope extension, token replay and cross-user session confusion.
- **Control, evidence and retest:** Check OAuth/OIDC validation, audience, authorization state and actual denial/issuance logs.

- [ ] **8.2.1** — OAuth clients, grants, authorization requests and consent flows — `P-012`
- [ ] **8.2.2** — Agent delegation, token audience and scope abuse — `P-012`
- [ ] **8.2.3** — Refresh tokens, session expiration and token replay — `P-012, P-018`
- [ ] **8.2.4** — User-to-agent identity mapping and session context switching — `P-018`
- [ ] **8.2.5** — Cross-user session confusion and authorization state integrity — `P-018`
- [ ] **8.2.6** — Consent revocation, logout, rotation and regression testing — `P-012, P-018`

### 8.3 — Authorization Policy & Tenant Isolation

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-19`, `B-29`, `B-46`, `B-66`

- **Benign-origin / baseline:** Test a benign model proposing a write, cross-tenant read or over-scoped action.
- **Adversarial counterpart:** Test adversarial requests and confused-deputy attempts against the same resources.
- **Control, evidence and retest:** Independently enforce subject/action/resource/tenant policy; verify no forbidden backend effect.

- [ ] **8.3.1** — Resource, action, subject and tenant authorization models — `P-016, P-017`
- [ ] **8.3.2** — Centralized policy decision and enforcement architecture — `P-016`
- [ ] **8.3.3** — Just-in-time privilege grants, expiry and least privilege — `P-016`
- [ ] **8.3.4** — Object-level and function-level authorization bypass testing — `P-017`
- [ ] **8.3.5** — Tenant scoping, cross-tenant resource access and isolation tests — `P-017`
- [ ] **8.3.6** — Authorization policy conflicts, caching and regression assurance — `P-016, P-017`

### 8.4 — MCP, Agent Identity & Delegated Trust

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-34`

- **Benign-origin / baseline:** Test ordinary delegated handoffs for lost scope, context confusion or wrong agent attribution.
- **Adversarial counterpart:** Test forged A2A messages, server spoofing, token forwarding and MCP privilege laundering.
- **Control, evidence and retest:** Verify authenticated principal, audience, per-action enforcement and revocation evidence.

- [ ] **8.4.1** — Agent principal identity and confused-deputy trust boundaries — `P-014`
- [ ] **8.4.2** — Confused-deputy, permission laundering and delegated authority tests — `P-014`
- [ ] **8.4.3** — MCP server discovery, endpoint impersonation and spoofing — `P-042`
- [ ] **8.4.4** — MCP authentication, token forwarding and audience validation — `P-043`
- [ ] **8.4.5** — A2A identity, message authentication and replay resistance — `P-045`
- [ ] **8.4.6** — Revocation, authorization audit trails and inter-agent regression — `P-014, P-042, P-043, P-045`

### 8.5 — Privileged Actions & Human Approvals

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-26`, `B-28`, `B-30`, `B-31`, `B-32`, `B-57`, `B-64`

- **Benign-origin / baseline:** Test mistaken, repeated, out-of-order or modified actions following a legitimate request.
- **Adversarial counterpart:** Alter an approval, replay authorization or induce a privileged tool call through malicious inputs.
- **Control, evidence and retest:** Bind approval to exact actor/action/arguments/expiry and verify idempotency and rejection receipts.

- [ ] **8.5.1** — Privileged operation classification and approval policies — `P-015`
- [ ] **8.5.2** — Human approval identity, intent and transaction binding — `P-015`
- [ ] **8.5.3** — Approval replay, substitution and stale authorization testing — `P-015`
- [ ] **8.5.4** — Agent action budgets, scoped authority and policy enforcement — `P-050`
- [ ] **8.5.5** — Escalation, emergency revocation and safe termination — `P-050`
- [ ] **8.5.6** — Approval logs, reviewer evidence and negative test cases — `P-015, P-050`

### 8.6 — Secrets, Credentials & Key Management

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Test normal error paths for credential disclosure, stale rotation, accidental logging and secret use outside a permitted action.
- **Adversarial counterpart:** Attempt unauthorized credential access, secrets exfiltration and credential reuse.
- **Control, evidence and retest:** Confirm vault policy, least privilege, rotation, revocation and redacted telemetry.

- [ ] **8.6.1** — Secrets inventory and service-to-secret access mapping — `P-019`
- [ ] **8.6.2** — Vault integration, authentication and least-privilege secret policies — `P-019`
- [ ] **8.6.3** — Credential issuance, rotation, renewal and expiration — `P-019`
- [ ] **8.6.4** — Secrets injection, environment leaks and repository exposure tests — `P-019`
- [ ] **8.6.5** — Revocation, emergency rotation and audit evidence — `P-019`

## Layer 5 — Data & Knowledge Security

### 5.1 — Enterprise Data & Privacy Lifecycle

**Practice role:** `SUPPORT` · **Proposed Case B risk links:** `B-41`, `B-43`, `B-45`, `B-67`

- **Benign-origin / baseline:** Test ordinary model mishandling of data classification, personal data, retention and output minimization.
- **Adversarial counterpart:** Test deliberate sensitive-data elicitation, poisoning and unauthorized data export.
- **Control, evidence and retest:** Independently verify DLP policy, retention/deletion state, purpose limitation and synthetic fixtures.

- [ ] **5.1.1** — Synthetic enterprise organization, users, assets and permissions — `P-002`
- [ ] **5.1.2** — Synthetic sensitive data, document corpora and attack fixtures — `P-002`
- [ ] **5.1.3** — Data discovery, classification and processing-purpose inventory — `P-084`
- [ ] **5.1.4** — Retention, deletion, backups and lifecycle assurance — `P-084`
- [ ] **5.1.5** — PII identification, minimization, masking and DLP controls — `P-085`
- [ ] **5.1.6** — Data egress, training-use boundaries and privacy regression testing — `P-084, P-085`

### 5.2 — RAG Connector Permissions & Synchronization

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-46`, `B-68`

- **Benign-origin / baseline:** Use benign user queries that might cause incorrect private-document retrieval or stale permission usage.
- **Adversarial counterpart:** Try malicious cross-user requests, connector manipulation and stale-ACL exploitation.
- **Control, evidence and retest:** Validate retrieval filters against actual user/source ACL and confirm no forbidden document is returned.

- [ ] **5.2.1** — Enterprise connector identities, permissions and data pathways — `P-031`
- [ ] **5.2.2** — Document-level ACL inheritance, effective access and retrieval filters — `P-031`
- [ ] **5.2.3** — User-to-service authorization propagation and permission caching — `P-031, P-037`
- [ ] **5.2.4** — Connector synchronization, permission updates and stale indexes — `P-037`
- [ ] **5.2.5** — Revoked access, deleted documents and index cleanup verification — `P-037`
- [ ] **5.2.6** — Multi-user negative tests, audit evidence and remediation — `P-031, P-037`

### 5.3 — Vector, Embedding & Retrieval Security

**Practice role:** `SUPPORT` · **Proposed Case B risk links:** `B-42`

- **Benign-origin / baseline:** Test normal semantic similarity mistakes, cross-namespace confusion and embedding exposure.
- **Adversarial counterpart:** Test targeted vector or ranking manipulation and namespace bypass.
- **Control, evidence and retest:** Compare retrieval to known labels, tenant policies, index metadata and objective leakage tests.

- [ ] **5.3.1** — Embedding creation, storage, metadata and exposure boundaries — `P-033`
- [ ] **5.3.2** — Vector namespace separation and cross-tenant authorization — `P-032`
- [ ] **5.3.3** — Similarity searches, semantic inference and embedding leakage — `P-033`
- [ ] **5.3.4** — Retrieval ranking, relevance scoring and result manipulation — `P-034`
- [ ] **5.3.5** — Retrieval enumeration and unauthorized semantic search — `P-038`
- [ ] **5.3.6** — Chunk-level metadata, filters and provenance integrity — `P-039`
- [ ] **5.3.7** — Vector index changes, audit logs and security regression — `P-032, P-033, P-034, P-038, P-039`

### 5.4 — Knowledge Integrity & Corpus Poisoning

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-01`, `B-02`, `B-68`

- **Benign-origin / baseline:** Generate plausible but false answers or citations on an untampered knowledge corpus.
- **Adversarial counterpart:** Introduce a deliberately false document, forged citation or modified metadata.
- **Control, evidence and retest:** Verify every material claim against trusted corpus provenance and retrieval audit traces.

- [ ] **5.4.1** — Knowledge corpus ownership, ingestion and provenance controls — `P-035`
- [ ] **5.4.2** — Malicious document insertion and retrieval-corpus poisoning — `P-035`
- [ ] **5.4.3** — Citation forgery, source impersonation and evidence laundering — `P-036`
- [ ] **5.4.4** — Grounding tests, citation verification and response integrity — `P-040`
- [ ] **5.4.5** — Memory and index contamination containment and rollback — `P-079`
- [ ] **5.4.6** — Restored corpus validation, reindexing and regression evidence — `P-035, P-036, P-040, P-079`

### 5.5 — Sensitive Data & High-Impact Workflows

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-40`, `B-43`, `B-44`, `B-47`, `B-67`

- **Benign-origin / baseline:** Test incorrect high-impact clinical or HR recommendations, wrong identity and overconfident answers on synthetic cases.
- **Adversarial counterpart:** Test deliberate workflow influence or illicit access to high-impact records.
- **Control, evidence and retest:** Use validated reference decisions, access policy, escalation and human review with no real individuals.

- [ ] **5.5.1** — Healthcare data classification and clinical access boundaries — `P-096`
- [ ] **5.5.2** — Clinical retrieval, sensitive records and workflow authorization — `P-096`
- [ ] **5.5.3** — HR candidate data privacy, consent and role restrictions — `P-097`
- [ ] **5.5.4** — Recruitment decision integrity and unauthorized influence tests — `P-097`
- [ ] **5.5.5** — High-impact workflow escalation, audit and disclosure control testing — `P-096, P-097`

### 5.6 — Document Injection, Upload & Preprocessing

**Practice role:** `SUPPORT` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Run ordinary documents with imperfect formatting or surprising parser outputs; measure model confusion.
- **Adversarial counterpart:** Submit isolated adversarial documents with embedded instructions or malformed file structures.
- **Control, evidence and retest:** Verify parser isolation, content labeling, normalized output and downstream retrieval behavior.

- [ ] **5.6.1** — Document retrieval trust hierarchy and embedded instructions — `P-022`
- [ ] **5.6.2** — Malicious retrieved-file content and instruction boundary tests — `P-022`
- [ ] **5.6.3** — Upload entry points, MIME/content-type and file-size enforcement — `P-103`
- [ ] **5.6.4** — Document parsing, converters and preprocessing attack surfaces — `P-103`
- [ ] **5.6.5** — Archive handling, nested files, deserialization and sandbox boundaries — `P-103`
- [ ] **5.6.6** — Parser error handling, output sanitization and malicious-file regression — `P-022, P-103`

## Layer 2 — Infrastructure & Supply Chain Security

### 2.1 — Cloud-Native Laboratory & Infrastructure as Code

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Deploy the lab reproducibly; verify that benign misconfiguration or teardown does not expose real resources.
- **Adversarial counterpart:** Test bounded access, infrastructure policy and permission abuse in the disposable environment.
- **Control, evidence and retest:** Use explicit scope, synthetic data, IaC plan/state checks, quotas and reproducible cleanup evidence.

- [ ] **2.1.1** — Laboratory scope, isolation requirements and environment design — `P-001`
- [ ] **2.1.2** — Infrastructure-as-code modules, providers and state security — `P-001`
- [ ] **2.1.3** — Container, cluster, network and storage provisioning — `P-001`
- [ ] **2.1.4** — Synthetic service dependencies, identity and secrets bootstrap — `P-001`
- [ ] **2.1.5** — Environment teardown, cost controls and reproducible deployments — `P-001`
- [ ] **2.1.6** — Build verification, snapshots, versioning and baseline evidence — `P-001`

### 2.2 — Kubernetes Workload & Configuration Security

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-19`

- **Benign-origin / baseline:** Check ordinary AI workload crashes, scheduling errors and insecure defaults in containers.
- **Adversarial counterpart:** Test authorized namespace/RBAC escape and lateral-movement hypotheses in a lab.
- **Control, evidence and retest:** Verify Kubernetes admissions, RBAC, namespace and network isolation with independent API outcomes.

- [ ] **2.2.1** — Kubernetes API, RBAC, namespaces and workload identities — `P-056`
- [ ] **2.2.2** — Pod security contexts, admission policies and image controls — `P-056`
- [ ] **2.2.3** — Service account impersonation and lateral-movement paths — `P-056`
- [ ] **2.2.4** — NetworkPolicy, service mesh and cross-namespace access — `P-056`
- [ ] **2.2.5** — Secrets, volumes and node-to-pod isolation boundaries — `P-056`
- [ ] **2.2.6** — Cluster benchmark checks, remediation and regression — `P-056`

### 2.3 — Sandbox & Workload Isolation

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-20`

- **Benign-origin / baseline:** Run ordinary AI-generated commands in a sandbox and confirm denied file/process/network access.
- **Adversarial counterpart:** Attempt bounded malicious command or sandbox escape only in a controlled lab.
- **Control, evidence and retest:** Verify host-level isolation and actual forbidden side-effects, not model promises.

- [ ] **2.3.1** — AI tool execution environments and process trust boundaries — `P-054`
- [ ] **2.3.2** — Container, microVM and user-space sandbox design — `P-054`
- [ ] **2.3.3** — Filesystem, process, privilege and syscall isolation — `P-054`
- [ ] **2.3.4** — Resource limits, network egress and inter-process access — `P-054`
- [ ] **2.3.5** — Sandbox escape resistance and negative security testing — `P-054`
- [ ] **2.3.6** — Containment evidence, fallback and sandbox lifecycle verification — `P-054`

### 2.4 — Inference Runtime & Model Serving

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Test model server outages, input validation failures and ordinary capacity/authorization mistakes.
- **Adversarial counterpart:** Test hostile API use, inference interface exposure and service privilege abuse.
- **Control, evidence and retest:** Check real serving configuration, authN/authZ, gateway rules, throttles and logs.

- [ ] **2.4.1** — Model server inventory, endpoints and exposed management APIs — `P-055`
- [ ] **2.4.2** — Model-loading, runtime and inference process configuration — `P-055`
- [ ] **2.4.3** — Inference API authentication, authorization and tenant boundaries — `P-055`
- [ ] **2.4.4** — Gateway controls, routing, TLS and ingress/egress policies — `P-055`
- [ ] **2.4.5** — Rate limits, capacity limits, denial-of-wallet and availability — `P-055`
- [ ] **2.4.6** — Server hardening, monitoring, patching and regression tests — `P-055`

### 2.5 — Runtime Detection, Network Egress & API Exposure

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-44`, `B-73`

- **Benign-origin / baseline:** Observe normal agent outbound mistakes, unexpected destinations and broken retry behavior.
- **Adversarial counterpart:** Attempt malicious SSRF/egress manipulation against safe in-lab targets.
- **Control, evidence and retest:** Verify egress controls, metadata endpoint protection, runtime traces and stopped actions.

- [ ] **2.5.1** — Agent tool network paths, DNS, proxies and egress policy — `P-060`
- [ ] **2.5.2** — SSRF targets, metadata endpoints and internal service reachability — `P-060`
- [ ] **2.5.3** — API exposure, outbound identity and destination allowlisting — `P-060`
- [ ] **2.5.4** — Runtime process monitoring, network telemetry and anomaly signals — `P-060`
- [ ] **2.5.5** — Blocked request tests, incident evidence and egress remediation — `P-060`

### 2.6 — Coding Agents, CI/CD & Dependency Supply Chain

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-18`, `B-37`

- **Benign-origin / baseline:** Review legitimate AI-generated PRs/dependencies for insecure changes or accidentally overbroad CI grants.
- **Adversarial counterpart:** Test malicious repo/CI prompts and malicious dependency updates in throwaway repos.
- **Control, evidence and retest:** Require code review, static analysis, secret scanning, least privilege and provenance-backed build receipts.

- [ ] **2.6.1** — Coding agent, repository and CI/CD trust boundaries — `P-052`
- [ ] **2.6.2** — AI-generated pull requests and workflow injection scenarios — `P-052`
- [ ] **2.6.3** — Build runners, tokens, artifacts and dependency trust paths — `P-052`
- [ ] **2.6.4** — Agent skills, plugins and third-party package inventories — `P-059`
- [ ] **2.6.5** — Dependency tampering, malicious updates and trust policy tests — `P-059`
- [ ] **2.6.6** — Static analysis, secrets scans and build gate verification — `P-052, P-059`
- [ ] **2.6.7** — Build provenance, remediation and continuous supply-chain checks — `P-052, P-059`

### 2.7 — AI BOM, Artifact Provenance & Trust

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-70`

- **Benign-origin / baseline:** Check honest model/component manifests for missing, stale or incorrectly signed artifacts.
- **Adversarial counterpart:** Attempt controlled artifact tampering and package substitution.
- **Control, evidence and retest:** Verify signatures, trust roots, provenance and admission decisions independently.

- [ ] **2.7.1** — AI component and model dependency inventory — `P-082`
- [ ] **2.7.2** — Software bills of materials and AI bills of materials generation — `P-082`
- [ ] **2.7.3** — Model, container and dataset artifact provenance records — `P-082`
- [ ] **2.7.4** — Artifact signing, signature verification and trust roots — `P-082`
- [ ] **2.7.5** — Build attestations, policy enforcement and traceable lineage — `P-082`
- [ ] **2.7.6** — Supply-chain changes, risk triage and audit evidence — `P-082`

## Layer 9 — External AI Provider & Ecosystem Security

### 9.1 — Hosted AI Provider Due Diligence

**Practice role:** `SUPPORT` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Evaluate a routine provider/model update causing changed safety, privacy or refusal behavior.
- **Adversarial counterpart:** Consider malicious supplier, model substitution or provider-side breach within contractual scope.
- **Control, evidence and retest:** Record versions and approvals; compare behavioral tests and documented provider controls, not presumed internals.

- [ ] **9.1.1** — Hosted model and external API vendor inventory — `P-081`
- [ ] **9.1.2** — Supplier security questionnaires, audit evidence and controls — `P-081`
- [ ] **9.1.3** — Provider data handling, retention, model-training use and residency — `P-081`
- [ ] **9.1.4** — Provider authentication, API quotas and service availability — `P-081`
- [ ] **9.1.5** — Subprocessors, contractual controls and incident obligations — `P-081`
- [ ] **9.1.6** — Vendor change monitoring, assurance gaps and risk decisions — `P-081`

### 9.2 — Multi-Provider Gateway, Routing & Cache Security

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-07`, `B-69`

- **Benign-origin / baseline:** Test clean failover, model routing and caching for behavior drift or context leakage.
- **Adversarial counterpart:** Test malicious route manipulation, unauthorized cache reuse and credential mix-ups.
- **Control, evidence and retest:** Verify tenant cache keys, per-provider tokens, routing policy and complete request receipts.

- [ ] **9.2.1** — Model provider configurations, routes and trust boundaries — `P-101`
- [ ] **9.2.2** — Provider API key isolation and outbound request authentication — `P-101`
- [ ] **9.2.3** — Gateway policy enforcement, quotas and rate limiting — `P-101`
- [ ] **9.2.4** — Cache partitioning, prompt/context privacy and tenant isolation — `P-101`
- [ ] **9.2.5** — Provider failover, response integrity and routing downgrade tests — `P-101`
- [ ] **9.2.6** — Gateway logs, cost attribution and integration regression — `P-101`

### 9.3 — Third-Party MCP, Procurement & Ecosystem Trust

**Practice role:** `CONTROL` · **Case B links:** `B-27`, `B-28`, `B-30`, `B-33`

- **Benign-origin / baseline:** Test benign third-party tool errors, ambiguous catalog metadata and procurement-agent decisions.
- **Adversarial counterpart:** Test malicious MCP provider, forged supplier information and manipulated purchasing arguments.
- **Control, evidence and retest:** Validate third-party identity, least privilege, approval binding and transaction audit trails.

- [ ] **9.3.1** — Third-party MCP server discovery and integration inventory — `P-044`
- [ ] **9.3.2** — Untrusted server configuration, credentials and transport risks — `P-044`
- [ ] **9.3.3** — Third-party tool trust boundary and malicious server scenarios — `P-044`
- [ ] **9.3.4** — Procurement agent suppliers, catalogs and contract data sources — `P-098`
- [ ] **9.3.5** — Contract changes, purchase actions and approval integrity — `P-098`
- [ ] **9.3.6** — External supplier actions, fraud scenarios and audit verification — `P-044, P-098`

### 9.4 — Shadow AI & Unauthorized Provider Usage

**Practice role:** `SUPPORT` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Inventory ordinary employees' unapproved model use and accidental sensitive data disclosures, within approved visibility.
- **Adversarial counterpart:** Assess intentional unapproved provider use and exfiltration pathways only where authorized.
- **Control, evidence and retest:** Validate monitoring coverage, classification and least-disruptive response; do not collect unnecessary private messages.

- [ ] **9.4.1** — Enterprise AI applications, provider domains and access discovery — `P-112`
- [ ] **9.4.2** — Unapproved SaaS AI usage and unauthorized integrations — `P-112`
- [ ] **9.4.3** — Sensitive prompt, document and API data egress channels — `P-112`
- [ ] **9.4.4** — Shadow AI identities, service accounts and credential exposure — `P-112`
- [ ] **9.4.5** — Discovery coverage, false positives, response and reporting — `P-112`

## Layer 7 — Human, Governance & Operational Security

### 7.1 — Engagement Governance & Risk Frameworks

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-17`, `B-70`

- **Benign-origin / baseline:** Define which ordinary AI failure modes create enforceable business security requirements and scenarios.
- **Adversarial counterpart:** Model explicit adversaries and attacker control after the non-adversarial business case.
- **Control, evidence and retest:** Require authorization, assets, risk owner, traceable control objective and accurate scope/limitations.

- [ ] **7.1.1** — Engagement scoping, permissions and rules of engagement — `P-003`
- [ ] **7.1.2** — Asset inventories, assumptions and stakeholder responsibilities — `P-003, P-005`
- [ ] **7.1.3** — Threat modeling, abuse cases and trust boundary mapping — `P-005`
- [ ] **7.1.4** — Control requirements and OWASP/NIST/MITRE mappings — `P-083`
- [ ] **7.1.5** — Regulatory evidence and high-risk AI assurance obligations — `P-089`
- [ ] **7.1.6** — Risk severity, prioritization, remediation and acceptance criteria — `P-090`
- [ ] **7.1.7** — Independent review, governance exceptions and engagement closure — `P-003, P-083, P-089, P-090`

### 7.2 — Evidence, Accountability & Secure AI Lifecycle

**Practice role:** `CONTROL` · **Proposed Case B risk links:** `B-02`, `B-14`, `B-63`

- **Benign-origin / baseline:** Detect hallucinated test evidence, missing receipts and unreliable AI-generated reports during normal use.
- **Adversarial counterpart:** Test deliberate log/report tampering and evidence laundering.
- **Control, evidence and retest:** Keep source-linked audit evidence, exact run IDs, signed/hashed artifacts where useful, and independent review.

- [ ] **7.2.1** — Security test reproducibility and regression control design — `P-007`
- [ ] **7.2.2** — Evidence collection, timestamps, provenance and telemetry — `P-009`
- [ ] **7.2.3** — Finding records, risk registers and professional reports — `P-010`
- [ ] **7.2.4** — Cryptographic audit trail integrity and action accountability — `P-087`
- [ ] **7.2.5** — AI security development lifecycle and deployment gates — `P-088`
- [ ] **7.2.6** — Retest archives, artifact integrity and continuous assurance — `P-007, P-009, P-010, P-087, P-088`

### 7.3 — AI Observability, Detection & SOC Security

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-15`, `B-16`, `B-21`, `B-22`, `B-54`, `B-56`

- **Benign-origin / baseline:** Monitor benign AI failures, unsafe proposals and false detector alerts without injected attacks.
- **Adversarial counterpart:** Detect adversarial injection, suspicious tool misuse, privilege abuse and model extraction attempts.
- **Control, evidence and retest:** Compare alerts to true outcomes and tool receipts; quantify misses, false positives and evidence gaps.

- [ ] **7.3.1** — AI-specific telemetry, events and normal behavior baselines — `P-074`
- [ ] **7.3.2** — Audit-log injection, tampering, omission and integrity testing — `P-073`
- [ ] **7.3.3** — Detection rules, security alerts and false-positive measurement — `P-074`
- [ ] **7.3.4** — Agent behavior drift, unusual tools and anomalous actions — `P-075`
- [ ] **7.3.5** — Data exfiltration and model extraction detection pipelines — `P-076`
- [ ] **7.3.6** — SOC copilot prompt-injection and analyst decision testing — `P-095`
- [ ] **7.3.7** — Detection validation, triage, escalation and SOC reporting — `P-073, P-074, P-075, P-076, P-095`

### 7.4 — Resource Abuse, Availability & Resilience

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-32`, `B-33`, `B-35`, `B-39`, `B-64`, `B-69`

- **Benign-origin / baseline:** Simulate normal tool failures triggering loops, high token costs and unbounded retries.
- **Adversarial counterpart:** Test malicious resource exhaustion and cost abuse under capped lab thresholds.
- **Control, evidence and retest:** Verify independent budgets, retries, timeouts, quotas, alerts and recovery.

- [ ] **7.4.1** — Agent loop, retry and runaway workflow analysis — `P-071`
- [ ] **7.4.2** — Token, compute, tool-call and network consumption limits — `P-071`
- [ ] **7.4.3** — Per-user and per-tenant quotas, billing and cost abuse — `P-072`
- [ ] **7.4.4** — Rate limiting, load shedding and service capacity controls — `P-072`
- [ ] **7.4.5** — Chaos/fault experiments, recovery objectives and resilience tests — `P-071, P-072`

### 7.5 — Incident Investigation, Containment & Purple Teaming

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-21`, `B-36`, `B-38`, `B-55`, `B-73`

- **Benign-origin / baseline:** Investigate an accidental unsafe agent action or failed tool, then safely isolate and recover.
- **Adversarial counterpart:** Investigate an intentional compromise or malicious agent-control scenario.
- **Control, evidence and retest:** Preserve incident chain, containment decisions, credential revocation, recovery and comparable retest.

- [ ] **7.5.1** — AI agent incident scenarios, timelines and forensic artifacts — `P-077`
- [ ] **7.5.2** — Investigation workflows, evidence preservation and attribution limits — `P-077`
- [ ] **7.5.3** — Credential revocation, agent isolation and emergency kill switches — `P-078`
- [ ] **7.5.4** — Safe recovery, verified rollback and service restoration — `P-078`
- [ ] **7.5.5** — Purple team exercise design, detection gaps and control metrics — `P-080`
- [ ] **7.5.6** — After-action reviews, lessons learned and regression validation — `P-077, P-078, P-080`

### 7.6 — Human Trust, Impersonation & Oversight

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-09`, `B-30`, `B-52`, `B-62`

- **Benign-origin / baseline:** Check reviewer overtrust in plausible but false AI recommendations without an attacker.
- **Adversarial counterpart:** Test malicious authority cues, phishing and approval manipulation in authorized simulations.
- **Control, evidence and retest:** Measure reviewer checks, approval integrity and escalation; no real-world human claims from mock personas.

- [ ] **7.6.1** — AI-enabled phishing and business email compromise simulations — `P-113`
- [ ] **7.6.2** — Synthetic impersonation, authority cues and social-engineering defenses — `P-113`
- [ ] **7.6.3** — Human reviewer roles, decision authority and trust calibration — `P-116`
- [ ] **7.6.4** — Approval fatigue, automation bias and manipulation tests — `P-116`
- [ ] **7.6.5** — Human escalation, intervention, training and reliability evidence — `P-113, P-116`

### 7.7 — Decision Integrity, Fairness & Appeal

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-08`, `B-17`, `B-47`, `B-48`, `B-49`, `B-50`, `B-51`, `B-52`

- **Benign-origin / baseline:** Test incorrect, overconfident or inequitable decision recommendations and ineffective appeal routes.
- **Adversarial counterpart:** Test targeted decision-input manipulation or discriminatory influence where applicable.
- **Control, evidence and retest:** Use independent truth, fairness/calibration measures, human oversight and correction logs; not all fairness failures are cyber incidents.

- [ ] **7.7.1** — High-impact AI decisions, affected groups and decision thresholds — `P-115`
- [ ] **7.7.2** — Fairness metrics, group disparities and calibration testing — `P-115`
- [ ] **7.7.3** — Explainability, contestability and supporting evidence — `P-115`
- [ ] **7.7.4** — Human review, appeals, remediation and audit trails — `P-115`
- [ ] **7.7.5** — Decision integrity regression and assurance reporting — `P-115`

## Layer 4 — Model Lifecycle Security

### 4.1 — Training Data Lineage & ML Pipeline Integrity

**Practice role:** `SUPPORT` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Check unintentional dataset errors, duplicate labels, stale features or pipeline drift.
- **Adversarial counterpart:** Simulate authorized malicious dataset/pipeline tampering in a small model lab.
- **Control, evidence and retest:** Verify lineage, checksums, dataset validation and clean/changed model behavior.

- [ ] **4.1.1** — Training-data inventories, lineage and dataset version control — `P-063`
- [ ] **4.1.2** — Source provenance, labeling, validation and dataset integrity — `P-063`
- [ ] **4.1.3** — Pipeline components, dependencies and build reproducibility — `P-064`
- [ ] **4.1.4** — Experiment tracking, artifact relationships and change approval — `P-064`
- [ ] **4.1.5** — Dataset or pipeline tampering, rollback and traceability tests — `P-063, P-064`

### 4.2 — Training Poisoning & Feedback Integrity

**Practice role:** `A-SPECIALIST` · **Proposed Case B risk links:** `B-24`, `B-65`

- **Benign-origin / baseline:** Measure benign noisy labels and feedback errors as clean baselines.
- **Adversarial counterpart:** Test intentionally poisoned datasets or feedback channels on owned models.
- **Control, evidence and retest:** Keep clean and poisoned model comparisons, outcome labels and rollback evidence.

- [ ] **4.2.1** — Training data trust boundaries, labels and attacker control — `P-061`
- [ ] **4.2.2** — Clean-label, dirty-label and targeted dataset poisoning tests — `P-061`
- [ ] **4.2.3** — Poisoning effect, utility degradation and defensive comparison — `P-061`
- [ ] **4.2.4** — Online feedback, preference signals and update pipeline trust — `P-070`
- [ ] **4.2.5** — Manipulated feedback, retraining triggers and drift regression — `P-070`

### 4.3 — Fine-Tuning, Adapters & Model Backdoors

**Practice role:** `A-SPECIALIST` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Measure ordinary fine-tuning variability, degraded accuracy and adapter conflicts.
- **Adversarial counterpart:** Test a small, explicitly backdoored model or adapter only in isolated lab conditions.
- **Control, evidence and retest:** Verify artifact provenance, clean/trigger performance, defenses and replacement recovery.

- [ ] **4.3.1** — Fine-tuning datasets, adapters, weights and artifact inventories — `P-062`
- [ ] **4.3.2** — Backdoor trigger construction in isolated model laboratories — `P-062`
- [ ] **4.3.3** — Backdoor activation, stealth and clean behavior evaluation — `P-062`
- [ ] **4.3.4** — Adapter and checkpoint provenance, integrity and scanning — `P-062`
- [ ] **4.3.5** — Backdoor mitigation, model replacement and regression — `P-062`

### 4.4 — Model Artifact Provenance & Safe Loading

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Verify clean model artifacts load safely and invalid files fail closed.
- **Adversarial counterpart:** Attempt bounded malicious artifact substitution and unsafe deserialization scenarios.
- **Control, evidence and retest:** Use safe formats, isolation, signing and loader error evidence; never load unknown pickle in trusted runtime.

- [ ] **4.4.1** — Model registries, artifact storage and access authorization — `P-058`
- [ ] **4.4.2** — Weights, manifests, digests and signatures — `P-058`
- [ ] **4.4.3** — Model registry supply-chain provenance and promotion gates — `P-058`
- [ ] **4.4.4** — Unsafe pickle and serialized model loading threat analysis — `P-102`
- [ ] **4.4.5** — Deserialization, parser sandboxing and malicious artifact tests — `P-102`
- [ ] **4.4.6** — Safe loading, verification failure handling and retesting — `P-058, P-102`

### 4.5 — Model Extraction & Intellectual Property

**Practice role:** `A-SPECIALIST` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Establish ordinary authorized API behavior and legitimate information exposed by outputs.
- **Adversarial counterpart:** Simulate controlled model extraction and stolen artifact access on owned models.
- **Control, evidence and retest:** Measure query budgets, access controls, watermarking/provenance where applicable and alert quality.

- [ ] **4.5.1** — Model query interfaces, extraction surfaces and permitted tests — `P-067`
- [ ] **4.5.2** — Prediction API access controls, quotas and response granularity — `P-067`
- [ ] **4.5.3** — Controlled model extraction and behavioral imitation evaluation — `P-067`
- [ ] **4.5.4** — Model artifacts, intellectual-property leakage and exfiltration channels — `P-067`
- [ ] **4.5.5** — Extraction monitoring, rate controls and defense regression — `P-067`

### 4.6 — Federated & Distributed Learning Security

**Practice role:** `A-SPECIALIST` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Measure ordinary federated client dropout, skew and noisy updates.
- **Adversarial counterpart:** Simulate malicious client updates, forged participants and aggregation poisoning.
- **Control, evidence and retest:** Compare aggregation robustness, identity, provenance, isolation and reproducible metrics.

- [ ] **4.6.1** — Federated participants, coordination and aggregation architecture — `P-110`
- [ ] **4.6.2** — Participant identities, trust and update authorization — `P-110`
- [ ] **4.6.3** — Malicious client updates, poisoning and aggregation manipulation — `P-110`
- [ ] **4.6.4** — Robust aggregation, anomaly screening and isolation — `P-110`
- [ ] **4.6.5** — Distributed trust, privacy and post-attack recovery testing — `P-110`

### 4.7 — Enterprise MLOps Assurance & Unlearning

**Practice role:** `SUPPORT` · **Proposed Case B risk links:** `B-41`, `B-65`

- **Benign-origin / baseline:** Test ordinary unlearning quality, residual memorization and model deployment regression.
- **Adversarial counterpart:** Test attacker contamination or lifecycle bypass where accessible and authorized.
- **Control, evidence and retest:** Use forget/retain datasets, documented baselines, pipeline gates and reproducible comparisons.

- [ ] **4.7.1** — Enterprise MLOps platform architecture and lifecycle roles — `P-100`
- [ ] **4.7.2** — Dataset-to-training-to-registry-to-serving trust boundaries — `P-100`
- [ ] **4.7.3** — Pipeline security gates, deployment approvals and assurance evidence — `P-100`
- [ ] **4.7.4** — Machine unlearning goals, removal requests and baseline models — `P-107`
- [ ] **4.7.5** — Forgetting verification, residual memorization and utility tradeoffs — `P-107`
- [ ] **4.7.6** — End-to-end model lifecycle assessment and independent reporting — `P-100, P-107`

## Layer 3 — Internal AI Mechanism Security

### 3.1 — Evaluation, Benchmarks & Model Judges

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-01`, `B-02`, `B-03`, `B-04`, `B-06`, `B-07`, `B-08`, `B-09`, `B-10`, `B-11`, `B-12`, `B-13`, `B-14`, `B-15`, `B-16`, `B-24`, `B-50`, `B-54`, `B-58`, `B-59`, `B-62`, `B-63`, `B-69`

- **Benign-origin / baseline:** Evaluate hallucination, calibration, refusal, nondeterminism and false security verdicts using sealed ground truth.
- **Adversarial counterpart:** Test judge/benchmark manipulation, contaminated examples and attacker-induced wrong verdicts.
- **Control, evidence and retest:** Use independent oracles, adjudicated holdouts, repeated trials and error rates, not unverified LLM judges.

- [ ] **3.1.1** — Evaluation objectives, threat models and benchmark selection — `P-008`
- [ ] **3.1.2** — Evaluation datasets, splits, contamination controls and versioning — `P-008`
- [ ] **3.1.3** — Benchmark poisoning, leakage and result manipulation — `P-104`
- [ ] **3.1.4** — LLM-as-judge prompts, judge bias and grading manipulation — `P-104`
- [ ] **3.1.5** — Score reproducibility, metric validity and evaluation regressions — `P-008, P-104`

### 3.2 — Adversarial Evasion & Model Robustness

**Practice role:** `A-SPECIALIST` · **Proposed Case B risk links:** `B-12`

- **Benign-origin / baseline:** Measure clean data shift, common noise and natural robustness degradation first.
- **Adversarial counterpart:** Test bounded adversarial perturbations, transfers and adaptive evasion on owned models.
- **Control, evidence and retest:** Report exact data/model versions, attack constraints, clean and adversarial metrics.

- [ ] **3.2.1** — Adversarial capability, model access and evaluation threat models — `P-065, P-066`
- [ ] **3.2.2** — Computer vision perturbations and adversarial image testing — `P-065`
- [ ] **3.2.3** — Image robustness across models and deployment transformations — `P-065`
- [ ] **3.2.4** — Text perturbations, classification evasion and semantic constraints — `P-066`
- [ ] **3.2.5** — Text robustness, transfer attacks and defensive evaluation — `P-066`
- [ ] **3.2.6** — Adaptive attacks, robustness metrics and reproducibility — `P-065, P-066`

### 3.3 — Privacy Inference & Privacy-Preserving ML

**Practice role:** `A-SPECIALIST` · **Proposed Case B risk links:** `B-41`, `B-42`

- **Benign-origin / baseline:** Measure training data memorization and ordinary privacy leakage via synthetic canaries.
- **Adversarial counterpart:** Test permitted membership inference and model inversion on synthetic owned datasets.
- **Control, evidence and retest:** Compare defenses and privacy error bars; never use private real persons' data.

- [ ] **3.3.1** — Model output, training membership and privacy threat assumptions — `P-068`
- [ ] **3.3.2** — Membership inference attacks and privacy leakage measurements — `P-068`
- [ ] **3.3.3** — Model inversion, reconstruction and sensitive feature inference — `P-069`
- [ ] **3.3.4** — Privacy defenses, differential privacy and effectiveness tradeoffs — `P-068, P-069`
- [ ] **3.3.5** — Uncertainty, error bounds and privacy regression testing — `P-068, P-069`

### 3.4 — LLM Guardrails, Jailbreaks & Policy Evasion

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-22`, `B-48`, `B-51`, `B-56`

- **Benign-origin / baseline:** Measure benign unsafe advice, inconsistent refusals and guardrail false positives/negatives.
- **Adversarial counterpart:** Test jailbreak, policy evasion and adaptive malicious prompting.
- **Control, evidence and retest:** Score utility and refusal outcomes with independently labeled examples and deterministic downstream enforcement.

- [ ] **3.4.1** — Safety policies, guardrail placement and threat boundaries — `P-105`
- [ ] **3.4.2** — Guardrail bypass resistance, detector false negatives and evasions — `P-105`
- [ ] **3.4.3** — Validator behavior, output filtering and layered defense tests — `P-105`
- [ ] **3.4.4** — Single-turn and multi-turn jailbreak scenario evaluation — `P-106`
- [ ] **3.4.5** — Policy evasion, refusal consistency and misuse resistance — `P-106`
- [ ] **3.4.6** — Adaptive evaluation, effectiveness metrics and regression — `P-105, P-106`

### 3.5 — Synthetic Media, Watermarks & Provenance

**Practice role:** `A-SPECIALIST` · **Proposed Case B risk links:** `B-53`

- **Benign-origin / baseline:** Measure ordinary media provenance errors and detector false positives on clean content.
- **Adversarial counterpart:** Test manipulated synthetic media, stripping, forgery and watermark robustness.
- **Control, evidence and retest:** Verify provenance cryptographically when available; report detector limits without claiming universal authenticity.

- [ ] **3.5.1** — Synthetic media generation pipelines and provenance threat models — `P-111`
- [ ] **3.5.2** — C2PA metadata, credential chains and content integrity verification — `P-111`
- [ ] **3.5.3** — Watermark embedding, detection and manipulation resistance — `P-111`
- [ ] **3.5.4** — Deepfake detection, robustness and false-positive assessment — `P-111`
- [ ] **3.5.5** — Transformation, re-encoding, stripping and provenance regression — `P-111`

## Layer 1 — Hardware & Compute Security

### 1.1 — GPU Resource Scheduling & Tenant Isolation

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Evaluate ordinary GPU tenant scheduling, leaks across resource reuse and service disruption.
- **Adversarial counterpart:** Test authorized resource-isolation abuse in suitable hardware labs.
- **Control, evidence and retest:** Verify device allocations, memory isolation where measurable and host-level telemetry; mocks are not hardware proof.

- [ ] **1.1.1** — Accelerator inventory, GPU scheduling and workload placement — `P-057`
- [ ] **1.1.2** — GPU allocation, partitioning, time sharing and tenant boundaries — `P-057`
- [ ] **1.1.3** — Device plugins, driver permissions and container device exposure — `P-057`
- [ ] **1.1.4** — GPU memory reuse, resource exhaustion and isolation verification — `P-057`
- [ ] **1.1.5** — Hardware telemetry, workload recovery and multi-tenant evidence — `P-057`

### 1.2 — GPU Fault Injection & Model Integrity

**Practice role:** `A-SPECIALIST` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Measure benign compute faults or simulated corruption causing silent wrong model outputs.
- **Adversarial counterpart:** Perform hardware fault injection only with specialized equipment and explicit permission.
- **Control, evidence and retest:** Track model integrity checks, error detection and recovery; label simulations precisely.

- [ ] **1.2.1** — GPU and model execution fault model, safety and prerequisites — `P-108`
- [ ] **1.2.2** — Fault injection points, supported hardware and isolated test setup — `P-108`
- [ ] **1.2.3** — Controlled compute errors, model corruption and output integrity — `P-108`
- [ ] **1.2.4** — Fault detection, workload isolation and recovery evaluation — `P-108`
- [ ] **1.2.5** — Hardware limitations, reproducibility and results reporting — `P-108`

### 1.3 — Confidential AI Computing & Protected Inference

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Test correct protected inference and ordinary integrity/secret-provisioning failures.
- **Adversarial counterpart:** Assess hostile host or runtime assumptions within supported confidential-computing boundaries.
- **Control, evidence and retest:** Verify trusted computing base and actual documented hardware-backed protections.

- [ ] **1.3.1** — Confidential inference assets, secrets and adversary assumptions — `P-086`
- [ ] **1.3.2** — Protected CPU/GPU execution environment and trusted computing base — `P-086`
- [ ] **1.3.3** — Encrypted model, prompt and data handling boundaries — `P-086`
- [ ] **1.3.4** — Secrets provisioning, policy enforcement and lifecycle — `P-086`
- [ ] **1.3.5** — Confidential workload deployment, failure handling and verification — `P-086`

### 1.4 — Remote Attestation & Hardware Trust

**Practice role:** `CONTROL` · **Case B links:** *No direct Case B link assigned; baseline/support only*

- **Benign-origin / baseline:** Test ordinary missing, expired or mismatched attestation evidence and safe rejection.
- **Adversarial counterpart:** Test replay, spoofed measurements and stale attestation requests where permitted.
- **Control, evidence and retest:** Verify root of trust, signed evidence, nonce, policy action and real hardware claims.

- [ ] **1.4.1** — Attestation actors, trust anchors and measurement models — `P-109`
- [ ] **1.4.2** — Evidence generation, freshness, nonce and verifier policies — `P-109`
- [ ] **1.4.3** — Reference values, signed reports and failure behavior — `P-109`
- [ ] **1.4.4** — Attestation-gated secrets and policy decision enforcement — `P-109`
- [ ] **1.4.5** — Replay, spoofing, stale measurement and key-release tests — `P-109`
- [ ] **1.4.6** — Verified hardware claims, limitations and attestation evidence — `P-109`

## Layer 10 — Cyber-Physical AI Security

### 10.1 — Sensor & Perception Integrity

**Practice role:** `CORE` · **Proposed Case B risk links:** `B-13`

- **Benign-origin / baseline:** Test ordinary sensor noise, missing frames, misclassification and conflicting sensor fusion in a simulator.
- **Adversarial counterpart:** Test synthetic sensor spoofing and adversarial perception perturbations.
- **Control, evidence and retest:** Verify sensor-confidence thresholds, safe fallback, independent reference labels and simulator limits.

- [ ] **10.1.1** — Simulated sensor, camera and telemetry source inventory — `P-114`
- [ ] **10.1.2** — Sensor identities, provenance and integrity controls — `P-114`
- [ ] **10.1.3** — Sensor spoofing, replay and perception manipulation — `P-114`
- [ ] **10.1.4** — Sensor fusion, inconsistent observations and anomaly detection — `P-114`
- [ ] **10.1.5** — Safe perception fallback and simulator regression — `P-114`

### 10.2 — Actuator Authorization & Safety Interlocks

**Practice role:** `CORE` · **Case B links:** `B-27`, `B-28`, `B-29`, `B-31`, `B-47`

- **Benign-origin / baseline:** Test an accidental AI-generated unsafe actuator command in simulation.
- **Adversarial counterpart:** Attempt unauthorized/replayed commands against the same simulator controls.
- **Control, evidence and retest:** Confirm hard safety interlocks, physical operating envelopes, approvals and emergency-stop override.

- [ ] **10.2.1** — Actuator identities, command channels and access policies — `P-114`
- [ ] **10.2.2** — Unauthorized action commands and controller trust boundaries — `P-114`
- [ ] **10.2.3** — Safety interlocks, rate and operating-envelope restrictions — `P-114`
- [ ] **10.2.4** — Human override, emergency-stop authorization and priority — `P-114`
- [ ] **10.2.5** — Command replay, fail-safe transitions and safety verification — `P-114`

### 10.3 — Cascading Failures & Safe Recovery

**Practice role:** `CORE` · **Case B links:** `B-35`, `B-36`, `B-38`, `B-39`

- **Benign-origin / baseline:** Simulate nonmalicious decision loops, delayed telemetry and cascading failures.
- **Adversarial counterpart:** Simulate intentional adversarial faults and propagation in isolated controls.
- **Control, evidence and retest:** Verify watchdogs, stop conditions, containment, restoration and safe-state evidence.

- [ ] **10.3.1** — System dependencies, control loops and cascading failure paths — `P-114`
- [ ] **10.3.2** — Unsafe autonomy, fault propagation and degraded-mode behavior — `P-114`
- [ ] **10.3.3** — Timeouts, watchdogs, network failures and recovery state — `P-114`
- [ ] **10.3.4** — Emergency containment, isolation and safe shutdown — `P-114`
- [ ] **10.3.5** — State restoration, simulation evidence and recovery regression — `P-114`

---


---

## Case B risk names and proposed corrected sublayer links

The following mappings are **new design recommendations**, not source-verified executable test coverage. They incorporate previously identified relevant extensions (including runtime receipts, generated authorization policies, DLP, cyber-physical controls, and third-party procurement).

| Case B risk | Suggested existing sublayers |
|---|---|
| **B-01 — Factual Hallucination** | `3.1`, `5.4` |
| **B-02 — Evidence and Citation Fabrication** | `3.1`, `5.4`, `7.2` |
| **B-03 — Logical and Computational Reasoning Failures** | `3.1` |
| **B-04 — User-Intent Misunderstanding** | `6.1`, `3.1` |
| **B-05 — Security Constraint Omission** | `6.1`, `6.2` |
| **B-06 — Entity and Identity Confusion** | `3.1`, `8.2` |
| **B-07 — Temporal Knowledge Failures** | `3.1`, `9.2` |
| **B-08 — Confidence Miscalibration** | `3.1`, `7.7` |
| **B-09 — Failure to Abstain or Escalate** | `3.1`, `7.6` |
| **B-10 — Long-Context Information Loss** | `3.1`, `6.5` |
| **B-11 — Decision Instability** | `3.1` |
| **B-12 — Out-of-Distribution Generalization Failure** | `3.2`, `3.1` |
| **B-13 — Multimodal Perception Errors** | `3.1`, `6.3`, `10.1` |
| **B-14 — False Execution or Capability Claims** | `7.2`, `3.1`, `6.4` |
| **B-15 — Security False Negatives** | `7.3`, `3.1` |
| **B-16 — Security False Positives** | `7.3`, `3.1` |
| **B-17 — Risk Severity Misjudgment** | `7.1`, `7.7` |
| **B-18 — Insecure Code Generation** | `6.7`, `2.6` |
| **B-19 — Insecure Configuration and Policy Generation** | `6.7`, `2.2`, `8.3` |
| **B-20 — Unsafe Operational Command Generation** | `6.7`, `2.3` |
| **B-21 — Incorrect Security Incident Decisions** | `7.3`, `7.5` |
| **B-22 — AI Safety-Detector Judgment Failures** | `3.4`, `7.3` |
| **B-23 — Autonomous Goal Drift** | `6.5` |
| **B-24 — Reward Hacking and Proxy Optimization** | `6.5`, `4.2`, `3.1` |
| **B-25 — Unsafe Task Planning** | `6.5` |
| **B-26 — Unrequested Action Initiation** | `6.4`, `8.5` |
| **B-27 — Incorrect Tool Selection and Parameter Decisions** | `6.4`, `9.3`, `10.2` |
| **B-28 — Wrong-Target Operations** | `6.4`, `8.5`, `9.3`, `10.2` |
| **B-29 — Autonomous Authorization-Boundary Violations** | `8.3`, `6.4`, `10.2` |
| **B-30 — Human-Approval Omission** | `8.5`, `7.6`, `9.3` |
| **B-31 — Unsafe Irreversible Decisions** | `8.5`, `6.4`, `10.2` |
| **B-32 — Duplicate or Repeated Execution** | `8.5`, `6.5`, `7.4` |
| **B-33 — Unintended Action Side Effects** | `6.4`, `7.4`, `9.3` |
| **B-34 — Unsafe Agent-to-Agent Delegation** | `6.6`, `8.4` |
| **B-35 — Runaway Autonomous Execution** | `6.5`, `7.4`, `10.3` |
| **B-36 — Failure to Stop Under Abnormal Conditions** | `6.5`, `7.5`, `10.3` |
| **B-37 — Unauthorized Agent Self-Modification** | `6.5`, `6.7`, `2.6` |
| **B-38 — Unsafe Autonomous Recovery** | `7.5`, `6.5`, `10.3` |
| **B-39 — Multi-Agent Error Amplification** | `6.6`, `7.4`, `10.3` |
| **B-40 — Sensitive Runtime-Context Disclosure** | `6.2`, `5.5` |
| **B-41 — Training-Data Memorization Disclosure** | `3.3`, `5.1`, `4.7` |
| **B-42 — Unauthorized Sensitive-Information Inference** | `3.3`, `5.3` |
| **B-43 — Sensitive-Data Redaction Failures** | `5.5`, `5.1` |
| **B-44 — Unintended External Data Transmission** | `2.5`, `5.5` |
| **B-45 — Excessive Autonomous Memory Retention** | `5.1`, `6.5` |
| **B-46 — Cross-User Context Contamination** | `5.2`, `8.3`, `6.5` |
| **B-47 — Dangerous High-Impact Recommendations** | `5.5`, `7.7`, `6.8`, `10.2` |
| **B-48 — Spontaneous Harmful or Abusive Content** | `3.4`, `7.7` |
| **B-49 — Biased and Discriminatory Decisions** | `7.7` |
| **B-50 — Misleading Decision Explanations** | `7.7`, `3.1` |
| **B-51 — Unjustified Refusal of Legitimate Tasks** | `3.4`, `7.7` |
| **B-52 — Inappropriate Human Persuasion or Manipulation** | `7.6`, `7.7` |
| **B-53 — Synthetic-Content Authenticity Misrepresentation** | `3.5` |
| **B-54 — Deceptive Behavior and Concealment** | `3.1`, `6.5`, `7.3` |
| **B-55 — Autonomous Sabotage** | `6.5`, `7.5` |
| **B-56 — Deliberate Safeguard and Monitoring Circumvention** | `6.5`, `7.3`, `3.4` |
| **B-57 — Strategic Privilege Seeking and Scheming** | `6.5`, `8.5` |
| **B-58 — Evaluation Metagaming** | `3.1` |
| **B-59 — Deliberate Capability Concealment (Sandbagging)** | `3.1` |
| **B-60 — Autonomous Agent Collusion** | `6.6` |
| **B-61 — Agent-Originated Instruction Manipulation** | `6.6`, `6.2` |
| **B-62 — AI Sycophancy and Truth Distortion** | `3.1`, `7.6` |
| **B-63 — Circular Self-Verification and False Assurance** | `3.1`, `7.2` |
| **B-64 — Stale-State Execution and Time-of-Check/Time-of-Use Failures** | `6.4`, `8.5`, `7.4` |
| **B-65 — Self-Generated Feedback Contamination** | `4.2`, `4.7` |
| **B-66 — Unsafe Composition of Individually Permitted Actions** | `6.4`, `8.3` |
| **B-67 — Unnecessary Sensitive-Data Acquisition and Aggregation** | `5.1`, `5.5` |
| **B-68 — Silent Semantic Data Corruption** | `5.4`, `5.2` |
| **B-69 — Correlated AI Failures and Model Monoculture** | `9.2`, `7.4`, `3.1` |
| **B-70 — Unintentional Intellectual-Property and Licensing Violations** | `2.7`, `7.1` |
| **B-71 — Benign-Memory Overgeneralization** | `6.5` |
| **B-72 — Self-Generated Memory Corruption** | `6.5` |
| **B-73 — Unauthorized AI Self-Replication and Persistence** | `6.5`, `2.5`, `7.5` |

## Controlled assessment record and independent competence

**For each applicable canonical ID** record: scope and ROE; versioned repository commit and configuration; environment classification (mock, simulator, real model, authorized unfamiliar target); asset and principal; permitted/forbidden effects; risk hypothesis; normal legitimate task; adversarial counterpart if relevant; independent oracle; actual responses, tool receipts and backend state; repetitions and error rates where measurable; independent permission check; finding/non-finding/limitations; remediation; retest; independent transfer; consultant-ready sanitized deliverable.

**Causal attribution:** Differentiate failures caused by model inference, retrieval/index data, application logic, tool/API behavior, human approval, or stale state; use controlled substitutions and source/runtime traces before concluding which component failed.

**Strategic behavior caveat:** B-54 through B-61 describe possible observed behaviors; do not infer intention, deception or coordination merely from a failed test. Record alternative explanations and repeatability.

**Legitimate test participants:** For human review/approval studies, use appropriately approved procedures, informed consent where needed, privacy limits and debriefing; prefer synthetic reviewers and scenarios where suitable.

**Publication gate:** remove secrets, real personal data, customer names, infrastructure identifiers, private prompts and sensitive logs from portfolio materials; retain source evidence in controlled storage.

**Architecture verification:** classify each major assertion as `AS_DESIGNED`, `SOURCE_CONFIRMED`, `RUNTIME_CONFIRMED`, `INFERRED`, `UNKNOWN`, or `CONTRADICTED` and distinguish actual capabilities from assumed integrations.

### Eight acceptance gates (from original master strategy)

| Gate | Acceptance requirement |
|---|---|
| G1 | In-scope authorized target/version and exclusions |
| G2 | Source/runtime-grounded architecture and trust boundaries |
| G3 | Relevant tests and independent oracles |
| G4 | Real run IDs and preserved raw evidence; simulations labeled |
| G5 | Findings and non-findings distinguished from inconclusive observations |
| G6 | Remediation owner and actual retest when claiming a fix |
| G7 | Sanitized, traceable technical and executive reporting |
| G8 | Independent transfer of the essential assessment to an unfamiliar authorized system |

**Test states:** `PASS`, `FAIL`, `BLOCKED`, `NOT_TESTED`, `INCONCLUSIVE`, `FLAKY`, `NOT_APPLICABLE`; `PARTIAL` only for aggregates. Design-only assessment tasks may be completed with appropriately verified requirements without inventing runtime exploits.

**Competence rubric:** 0 = not studied; 1 = explain; 2 = guided test; 3 = independent unfamiliar-system assessment; 4 = independent end-to-end engagement including defensible report. These levels are learning rubric, not employment grades.

**AI assistance:** ChatGPT/Codex may draft code, tests, hypotheses and reports; acceptance requires the learner to review code and verify outcomes against non-AI, source-linked, or independently checked oracles and actual receipts.

**Parallel fundamentals:** Python, Linux, networking, HTTP/API semantics, IAM/OIDC/OAuth, cloud/Kubernetes, secure development, logs/observability, evidence preservation and clear consultancy communication.

## Specialist Layer 10 reference repositories (outside the original 160 catalog)

- 10.1 — [ROS 2](https://github.com/ros2/ros2) and [Gazebo Sim](https://github.com/gazebosim/gz-sim).
- 10.2 — [open62541](https://github.com/open62541/open62541).
- 10.3 — [CARLA](https://github.com/carla-simulator/carla).

## Original complete primary and cross-layer allocation reference

The following section reproduces the user-provided sublayer-level **primary risk, primary project, primary technology and cross-layer dependency** assignments. It is a supporting reference and does not duplicate or renumber the canonical 334 work-package checklist above. Technologies are candidates, not verified deployed integrations.


# AI Security Engineering — Complete 10-Layer Sublayer Architecture (2026+)

**37 primary risks · 116 primary assessment projects · 160 primary catalog entries · 10 main layers · 57 sublayers**

## Primary allocation summary

| Order | Main layer | Sublayers | Primary risks | Primary projects | Primary catalog |
|---:|---|---:|---:|---:|---:|
| 1 | Layer 6 — AI Application & Autonomous Agent Security | 8 | 10 | 23 | 30 |
| 2 | Layer 8 — Identity, Authorization & Control Plane Security | 6 | 3 | 14 | 17 |
| 3 | Layer 5 — Data & Knowledge Security | 6 | 6 | 18 | 10 |
| 4 | Layer 2 — Infrastructure & Supply Chain Security | 7 | 2 | 8 | 38 |
| 5 | Layer 9 — External AI Provider & Ecosystem Security | 4 | 1 | 5 | 2 |
| 6 | Layer 7 — Human, Governance & Operational Security | 7 | 2 | 23 | 25 |
| 7 | Layer 4 — Model Lifecycle Security | 7 | 6 | 11 | 15 |
| 8 | Layer 3 — Internal AI Mechanism Security | 5 | 4 | 9 | 18 |
| 9 | Layer 1 — Hardware & Compute Security | 4 | 2 | 4 | 5 |
| 10 | Layer 10 — Cyber-Physical AI Security | 3 | 1 | 1 | 0 |
| **Total** | **10 main layers** | **57** | **37** | **116** | **160** |

## Layer 6 — AI Application & Autonomous Agent Security

### Sublayer 6.1 — AI Application Foundations

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-006** — Secure-by-Default LLM Application Reference Architecture
- **P-004** — Automated AI Application Architecture Discovery and Attack Surface Mapping

**Primary catalog entries**
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#139** — [Dify](https://github.com/langgenius/dify)
- **#140** — [LibreChat](https://github.com/danny-avila/LibreChat)
- **#141** — [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)
- **#62** — [OWASP ZAP](https://github.com/zaproxy/zaproxy)

### Sublayer 6.2 — LLM Instruction & Output Security

**Primary risks**
- **R-08** — Unsafe model-output handling
- **R-12** — Direct prompt injection
- **R-23** — Jailbreaks, policy evasion, and harmful use

**Primary assessment projects**
- **P-021** — Direct Prompt Injection and System Instruction Boundary Testing
- **P-029** — Hidden System Context, Confidential Instructions, and Reasoning Trace Exposure Assessment
- **P-030** — Unsafe LLM Output Handling, Command Injection, and Application Injection Chains

**Primary catalog entries**
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#48** — [Pydantic](https://github.com/pydantic/pydantic)

### Sublayer 6.3 — Indirect & Multimodal Injection Security

**Primary risks**
- **R-05** — Indirect and multimodal prompt injection

**Primary assessment projects**
- **P-023** — Browser-Based AI Agent Webpage Content Manipulation
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-025** — Image-Based Multimodal Prompt Injection Security Laboratory
- **P-026** — Audio and Speech-Based Instruction Injection Assessment
- **P-027** — Video Frame, Caption, and Subtitle Injection Against Multimodal Agents
- **P-028** — Structured Data, CSV, and Spreadsheet Instruction Injection Testing

**Primary catalog entries**
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#150** — [mitmproxy](https://github.com/mitmproxy/mitmproxy)

### Sublayer 6.4 — MCP, Tool & External Action Security

**Primary risks**
- **R-02** — Tool misuse and unauthorized external actions
- **R-10** — MCP server, tool, and transport security failures

**Primary assessment projects**
- **P-041** — MCP Tool Description, Parameter Schema, and Tool Selection Manipulation
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation

**Primary catalog entries**
- **#6** — [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **#7** — [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- **#8** — [MCP reference servers](https://github.com/modelcontextprotocol/servers)
- **#9** — [MCP Scan (Snyk Agent Scan)](https://github.com/snyk/agent-scan)

### Sublayer 6.5 — Autonomous Agent & Memory Security

**Primary risks**
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-11** — Memory poisoning and context-management failures

**Primary assessment projects**
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-047** — Autonomous Agent Goal Hijacking, Task Drift, and Workflow Integrity Assessment

**Primary catalog entries**
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#13** — [LangGraph](https://github.com/langchain-ai/langgraph)
- **#14** — [Google ADK](https://github.com/google/adk-python)
- **#16** — [Smolagents](https://github.com/huggingface/smolagents)
- **#19** — [Temporal](https://github.com/temporalio/temporal)
- **#20** — [Temporal Python SDK](https://github.com/temporalio/sdk-python)

### Sublayer 6.6 — Multi-Agent & A2A Security

**Primary risks**
- **R-20** — Inter-agent and A2A communication abuse

**Primary assessment projects**
- **P-049** — Multi-Agent Cascading Failures, Compromised Agent Propagation, and Recovery

**Primary catalog entries**
- **#11** — [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- **#15** — [CrewAI](https://github.com/crewAIInc/crewAI)
- **#18** — [A2A protocol](https://github.com/a2aproject/A2A)

### Sublayer 6.7 — AI Coding Agent Security

**Primary risks**
- **R-09** — Coding-agent, repository, and workspace compromise

**Primary assessment projects**
- **P-051** — AI Coding Agent Repository Instruction File and Workspace Trust Assessment
- **P-053** — AI-Generated Code Vulnerability Detection and Secure Code Generation Pipeline

**Primary catalog entries**
- **#2** — [OpenHands](https://github.com/OpenHands/OpenHands)
- **#10** — [Cline](https://github.com/cline/cline)
- **#17** — [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent)
- **#58** — [OWASP Juice Shop](https://github.com/juice-shop/juice-shop)
- **#59** — [WebGoat](https://github.com/WebGoat/WebGoat)
- **#60** — [OWASP crAPI](https://github.com/OWASP/crAPI)
- **#61** — [OWASP NodeGoat](https://github.com/OWASP/NodeGoat)

### Sublayer 6.8 — Enterprise AI Security Engagements

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-092** — Autonomous Financial Operations Agent: Transaction Authorization, Fraud, and Privilege Security Assessment
- **P-093** — Enterprise AI Coding Assistant: Repository, Developer Identity, Tool, and CI/CD Security Engagement
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement

**Primary catalog entries**
- None assigned

### Layer 6 — Cross-layer dependencies

**Cross-layer security risks (11)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-03** — RAG and connector permission failures
- **R-04** — Sensitive information and hidden-context disclosure
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-13** — Retrieval, ranking, vector, and embedding manipulation
- **R-14** — AI gateway, provider routing, and cache failures
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (17)**
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-015** — Human-in-the-Loop Approval Integrity, Replay, and Transaction Binding
- **P-043** — MCP Authentication, Token Forwarding, and Delegated Authorization Security
- **P-050** — Autonomous Agent Action Budgets, Policy Enforcement, and Safe Delegation Architecture
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-031** — Enterprise RAG Connector Permission Inheritance and Access Control Assessment
- **P-037** — Stale Permissions, Deleted Documents, and Connector Synchronization Security
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-079** — Poisoned Knowledge Base, Compromised Agent Memory, and Model Rollback Recovery
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-008** — AI Security Evaluation Datasets and Regression Testing Pipeline
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-106** — LLM Jailbreak, Multi-Turn Policy Evasion, and Misuse-Resistance Evaluation

**Cross-layer catalog entries (11)**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)

---

## Layer 8 — Identity, Authorization & Control Plane Security

### Sublayer 8.1 — Cloud Workload Identity & Trust Federation

**Primary risks**
- **R-01** — Workload identity, impersonation, and delegation abuse

**Primary assessment projects**
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-013** — Service Account Impersonation and Privilege Escalation in AI Workloads
- **P-020** — Cross-Cloud AI Workload Trust Relationships and Privilege Path Analysis

**Primary catalog entries**
- **#102** — [Cloudsplaining](https://github.com/salesforce/cloudsplaining)
- **#154** — [CloudFox](https://github.com/BishopFox/cloudfox)
- **#155** — [Policy Sentry](https://github.com/salesforce/policy_sentry)
- **#157** — [AWS test environment](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) *(AWS environment; not open-source software)*

### Sublayer 8.2 — OAuth Delegation & Identity Sessions

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-012** — OAuth Delegation, Consent, and Scope Abuse in Enterprise AI Agents
- **P-018** — AI Session Identity, Context Switching, and Authorization State Integrity

**Primary catalog entries**
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#146** — [OAuth2 Proxy](https://github.com/oauth2-proxy/oauth2-proxy)
- **#151** — [jwt_tool](https://github.com/ticarpi/jwt_tool)
- **#153** — [OpenID Conformance Suite](https://gitlab.com/openid/conformance-suite)
- **#156** — [mockoidc](https://github.com/oauth2-proxy/mockoidc)

### Sublayer 8.3 — Authorization Policy & Tenant Isolation

**Primary risks**
- **R-35** — Tenant and user isolation failures

**Primary assessment projects**
- **P-016** — Just-in-Time Privileged Access and Least-Privilege Enforcement for AI Agents
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment

**Primary catalog entries**
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#24** — [Cerbos](https://github.com/cerbos/cerbos)
- **#152** — [Cedar](https://github.com/cedar-policy/cedar)

### Sublayer 8.4 — MCP, Agent Identity & Delegated Trust

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-042** — MCP Server Impersonation, Discovery Spoofing, and Endpoint Trust Assessment
- **P-043** — MCP Authentication, Token Forwarding, and Delegated Authorization Security
- **P-045** — Agent-to-Agent Message Authentication, Spoofing, and Communication Integrity

**Primary catalog entries**
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)

### Sublayer 8.5 — Privileged Actions & Human Approvals

**Primary risks**
- **R-07** — Approval bypass and human-agent trust exploitation

**Primary assessment projects**
- **P-015** — Human-in-the-Loop Approval Integrity, Replay, and Transaction Binding
- **P-050** — Autonomous Agent Action Budgets, Policy Enforcement, and Safe Delegation Architecture

**Primary catalog entries**
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#107** — [OPA Gatekeeper](https://github.com/open-policy-agent/gatekeeper)

### Sublayer 8.6 — Secrets, Credentials & Key Management

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security

**Primary catalog entries**
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)

### Layer 8 — Cross-layer dependencies

**Cross-layer security risks (17)**
- **R-02** — Tool misuse and unauthorized external actions
- **R-03** — RAG and connector permission failures
- **R-04** — Sensitive information and hidden-context disclosure
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-10** — MCP server, tool, and transport security failures
- **R-11** — Memory poisoning and context-management failures
- **R-13** — Retrieval, ranking, vector, and embedding manipulation
- **R-14** — AI gateway, provider routing, and cache failures
- **R-15** — Model-serving and inference-runtime exposure
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-20** — Inter-agent and A2A communication abuse
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (38)**
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-006** — Secure-by-Default LLM Application Reference Architecture
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-031** — Enterprise RAG Connector Permission Inheritance and Access Control Assessment
- **P-032** — Vector Database Namespace Isolation and Cross-Tenant Access Testing
- **P-037** — Stale Permissions, Deleted Documents, and Connector Synchronization Security
- **P-038** — Retrieval Index Enumeration and Unauthorized Semantic Search Assessment
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-041** — MCP Tool Description, Parameter Schema, and Tool Selection Manipulation
- **P-044** — Malicious MCP Server Configuration and Third-Party Trust Boundary Testing
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-047** — Autonomous Agent Goal Hijacking, Task Drift, and Workflow Integrity Assessment
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation
- **P-049** — Multi-Agent Cascading Failures, Compromised Agent Propagation, and Recovery
- **P-092** — Autonomous Financial Operations Agent: Transaction Authorization, Fraud, and Privilege Security Assessment
- **P-098** — AI-Driven Procurement and Contract Management Agents: External Actions, Approval, and Supply Chain Trust Assessment
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement
- **P-116** — Human-AI Trust Calibration, Approval Fatigue, Authority Manipulation, and Reviewer Reliability Laboratory
- **P-051** — AI Coding Agent Repository Instruction File and Workspace Trust Assessment
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-112** — Enterprise Shadow AI Discovery, Inventory, and Unauthorized Data Egress Assessment
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment

**Cross-layer catalog entries (29)**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#2** — [OpenHands](https://github.com/OpenHands/OpenHands)
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#6** — [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **#7** — [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#18** — [A2A protocol](https://github.com/a2aproject/A2A)
- **#19** — [Temporal](https://github.com/temporalio/temporal)
- **#28** — [Qdrant](https://github.com/qdrant/qdrant)
- **#29** — [pgvector](https://github.com/pgvector/pgvector)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#60** — [OWASP crAPI](https://github.com/OWASP/crAPI)
- **#62** — [OWASP ZAP](https://github.com/zaproxy/zaproxy)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#143** — [Nextcloud](https://github.com/nextcloud/server)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#147** — [Istio](https://github.com/istio/istio)
- **#150** — [mitmproxy](https://github.com/mitmproxy/mitmproxy)
- **#158** — [Grafana k6](https://github.com/grafana/k6)

---

## Layer 5 — Data & Knowledge Security

### Sublayer 5.1 — Enterprise Data & Privacy Lifecycle

**Primary risks**
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures

**Primary assessment projects**
- **P-002** — Synthetic Enterprise Data, Users, Assets, and Attack Scenario Generator
- **P-084** — Enterprise AI Data Retention, Deletion, and Privacy Lifecycle Security Assessment
- **P-085** — AI Application PII Detection, Data Minimization, and DLP Engineering

**Primary catalog entries**
- **#89** — [SDV](https://github.com/sdv-dev/SDV)

### Sublayer 5.2 — RAG Connector Permissions & Synchronization

**Primary risks**
- **R-03** — RAG and connector permission failures

**Primary assessment projects**
- **P-031** — Enterprise RAG Connector Permission Inheritance and Access Control Assessment
- **P-037** — Stale Permissions, Deleted Documents, and Connector Synchronization Security

**Primary catalog entries**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#143** — [Nextcloud](https://github.com/nextcloud/server)

### Sublayer 5.3 — Vector, Embedding & Retrieval Security

**Primary risks**
- **R-13** — Retrieval, ranking, vector, and embedding manipulation

**Primary assessment projects**
- **P-032** — Vector Database Namespace Isolation and Cross-Tenant Access Testing
- **P-033** — Embedding-Based Sensitive Information Leakage and Semantic Inference Assessment
- **P-034** — Retrieval Ranking Manipulation and Search Result Integrity Testing
- **P-038** — Retrieval Index Enumeration and Unauthorized Semantic Search Assessment
- **P-039** — Chunk-Level Metadata Manipulation and Retrieval Pipeline Trust Testing

**Primary catalog entries**
- **#28** — [Qdrant](https://github.com/qdrant/qdrant)
- **#29** — [pgvector](https://github.com/pgvector/pgvector)
- **#30** — [sentence-transformers](https://github.com/huggingface/sentence-transformers)

### Sublayer 5.4 — Knowledge Integrity & Corpus Poisoning

**Primary risks**
- **R-19** — Data-pipeline and decision-input integrity failures

**Primary assessment projects**
- **P-035** — Enterprise Knowledge Base Poisoning and Retrieval Corpus Integrity Assessment
- **P-036** — Document Provenance, Citation Forgery, and Evidence Laundering Assessment
- **P-040** — Grounded AI Response Verification, False Citation Detection, and Knowledge Integrity Engineering
- **P-079** — Poisoned Knowledge Base, Compromised Agent Memory, and Model Rollback Recovery

**Primary catalog entries**
- **#31** — [Haystack](https://github.com/deepset-ai/haystack)
- **#32** — [LlamaIndex](https://github.com/run-llama/llama_index)

### Sublayer 5.5 — Sensitive Data & High-Impact Workflows

**Primary risks**
- **R-04** — Sensitive information and hidden-context disclosure

**Primary assessment projects**
- **P-096** — Healthcare AI Assistant: Sensitive Data Access, Privacy, Retrieval, and Clinical Workflow Security Assessment
- **P-097** — Enterprise HR and Recruitment AI: Candidate Data Security, Decision Integrity, and Access Control Assessment

**Primary catalog entries**
- **#47** — [Presidio](https://github.com/microsoft/presidio)

### Sublayer 5.6 — Document Injection, Upload & Preprocessing

**Primary risks**
- **R-17** — File upload, document parsing, and preprocessing attacks

**Primary assessment projects**
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-103** — AI File Upload, Document Parser, and Preprocessing Security Laboratory

**Primary catalog entries**
- **#159** — [Docling](https://github.com/docling-project/docling)

### Layer 5 — Cross-layer dependencies

**Cross-layer security risks (23)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-02** — Tool misuse and unauthorized external actions
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-08** — Unsafe model-output handling
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-10** — MCP server, tool, and transport security failures
- **R-11** — Memory poisoning and context-management failures
- **R-12** — Direct prompt injection
- **R-14** — AI gateway, provider routing, and cache failures
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-20** — Inter-agent and A2A communication abuse
- **R-21** — Evaluation, benchmark, and model-judge manipulation
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-23** — Jailbreaks, policy evasion, and harmful use
- **R-25** — Machine-learning privacy attacks
- **R-26** — Training, fine-tuning, and feedback poisoning or integrity failures
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures
- **R-34** — Media provenance, watermarking, and deepfake risks
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (46)**
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-008** — AI Security Evaluation Datasets and Regression Testing Pipeline
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment
- **P-018** — AI Session Identity, Context Switching, and Authorization State Integrity
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security
- **P-043** — MCP Authentication, Token Forwarding, and Delegated Authorization Security
- **P-021** — Direct Prompt Injection and System Instruction Boundary Testing
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-025** — Image-Based Multimodal Prompt Injection Security Laboratory
- **P-026** — Audio and Speech-Based Instruction Injection Assessment
- **P-027** — Video Frame, Caption, and Subtitle Injection Against Multimodal Agents
- **P-028** — Structured Data, CSV, and Spreadsheet Instruction Injection Testing
- **P-029** — Hidden System Context, Confidential Instructions, and Reasoning Trace Exposure Assessment
- **P-030** — Unsafe LLM Output Handling, Command Injection, and Application Injection Chains
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-112** — Enterprise Shadow AI Discovery, Inventory, and Unauthorized Data Egress Assessment
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-077** — Compromised AI Agent Incident Investigation and Digital Forensics Simulation
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-061** — Supervised Learning Dataset Poisoning and Label Integrity Assessment
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-068** — Training Data Membership Inference and Privacy Leakage Assessment
- **P-069** — Model Inversion, Sensitive Feature Reconstruction, and Privacy Defense Evaluation
- **P-070** — Online Learning Feedback Manipulation and Continuous Training Data Poisoning Assessment
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-106** — LLM Jailbreak, Multi-Turn Policy Evasion, and Misuse-Resistance Evaluation
- **P-107** — Machine Unlearning Verification and Synthetic Data Privacy Assurance
- **P-111** — Synthetic Media Provenance, Watermarking, and Deepfake Verification Laboratory
- **P-115** — High-Impact AI Decision Fairness, Calibration, Explainability, and Appeal Assurance

**Cross-layer catalog entries (42)**
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#13** — [LangGraph](https://github.com/langchain-ai/langgraph)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#33** — [Transformers](https://github.com/huggingface/transformers)
- **#34** — [PyTorch](https://github.com/pytorch/pytorch)
- **#39** — [Garak](https://github.com/NVIDIA/garak)
- **#40** — [PyRIT](https://github.com/microsoft/PyRIT)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#45** — [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
- **#46** — [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- **#48** — [Pydantic](https://github.com/pydantic/pydantic)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#54** — [nsjail](https://github.com/google/nsjail)
- **#62** — [OWASP ZAP](https://github.com/zaproxy/zaproxy)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#83** — [OpenLineage](https://github.com/OpenLineage/OpenLineage)
- **#86** — [ML Privacy Meter](https://github.com/privacytrustlab/ml_privacy_meter)
- **#87** — [TensorFlow Privacy](https://github.com/tensorflow/privacy)
- **#88** — [Opacus](https://github.com/pytorch/opacus)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#116** — [Phoenix](https://github.com/Arize-ai/phoenix)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#125** — [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#127** — [OWASP ASVS](https://github.com/OWASP/ASVS)
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#131** — [Evidently](https://github.com/evidentlyai/evidently)
- **#132** — [c2patool](https://github.com/contentauth/c2patool)
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#139** — [Dify](https://github.com/langgenius/dify)
- **#144** — [Label Studio](https://github.com/HumanSignal/label-studio)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#150** — [mitmproxy](https://github.com/mitmproxy/mitmproxy)
- **#160** — [Open-Unlearning (TOFU benchmark)](https://github.com/locuslab/open-unlearning)

---

## Layer 2 — Infrastructure & Supply Chain Security

### Sublayer 2.1 — Cloud-Native Laboratory & Infrastructure as Code

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-001** — Reproducible Cloud-Native AI Security Laboratory and Infrastructure-as-Code Platform

**Primary catalog entries**
- **#101** — [LocalStack](https://github.com/localstack/localstack)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#109** — [TerraGoat](https://github.com/bridgecrewio/terragoat)
- **#110** — [Checkov](https://github.com/bridgecrewio/checkov)
- **#148** — [Prowler](https://github.com/prowler-cloud/prowler)
- **#149** — [OpenTofu](https://github.com/opentofu/opentofu)

### Sublayer 2.2 — Kubernetes Workload & Configuration Security

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing

**Primary catalog entries**
- **#104** — [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat)
- **#105** — [WrongSecrets](https://github.com/OWASP/wrongsecrets)
- **#106** — [kube-bench](https://github.com/aquasecurity/kube-bench)
- **#108** — [Kyverno](https://github.com/kyverno/kyverno)
- **#147** — [Istio](https://github.com/istio/istio)

### Sublayer 2.3 — Sandbox & Workload Isolation

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment

**Primary catalog entries**
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#52** — [Firecracker](https://github.com/firecracker-microvm/firecracker)
- **#53** — [Kata Containers](https://github.com/kata-containers/kata-containers)
- **#54** — [nsjail](https://github.com/google/nsjail)
- **#55** — [Wasmtime](https://github.com/bytecodealliance/wasmtime)

### Sublayer 2.4 — Inference Runtime & Model Serving

**Primary risks**
- **R-15** — Model-serving and inference-runtime exposure

**Primary assessment projects**
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening

**Primary catalog entries**
- **#37** — [llama.cpp](https://github.com/ggml-org/llama.cpp)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#93** — [Triton Inference Server](https://github.com/triton-inference-server/server)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#96** — [Ray](https://github.com/ray-project/ray)

### Sublayer 2.5 — Runtime Detection, Network Egress & API Exposure

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment

**Primary catalog entries**
- **#56** — [Falco](https://github.com/falcosecurity/falco)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#67** — [Nuclei](https://github.com/projectdiscovery/nuclei)

### Sublayer 2.6 — Coding Agents, CI/CD & Dependency Supply Chain

**Primary risks**
- **R-36** — AI supply-chain and dependency compromise

**Primary assessment projects**
- **P-052** — AI-Generated Pull Request, CI/CD Pipeline, and Build System Compromise Simulation
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security

**Primary catalog entries**
- **#63** — [Semgrep](https://github.com/semgrep/semgrep)
- **#64** — [CodeQL](https://github.com/github/codeql)
- **#65** — [Gitleaks](https://github.com/gitleaks/gitleaks)
- **#66** — [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- **#68** — [Trivy](https://github.com/aquasecurity/trivy)
- **#79** — [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- **#80** — [GUAC](https://github.com/guacsec/guac)

### Sublayer 2.7 — AI BOM, Artifact Provenance & Trust

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-082** — AI Bill of Materials, Model Dependencies, and Software Supply Chain Transparency Platform

**Primary catalog entries**
- **#74** — [Syft](https://github.com/anchore/syft)
- **#75** — [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#77** — [in-toto](https://github.com/in-toto/in-toto)
- **#78** — [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator)
- **#81** — [Harbor](https://github.com/goharbor/harbor)
- **#82** — [Sigstore Policy Controller](https://github.com/sigstore/policy-controller)

### Layer 2 — Cross-layer dependencies

**Cross-layer security risks (9)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-14** — AI gateway, provider routing, and cache failures
- **R-16** — Unsafe model loading, deserialization, and parser vulnerabilities
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-31** — Shared-hardware and accelerator isolation failures, including model fault injection
- **R-32** — Confidential-computing and attestation trust failures
- **R-35** — Tenant and user isolation failures
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (20)**
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-013** — Service Account Impersonation and Privilege Escalation in AI Workloads
- **P-051** — AI Coding Agent Repository Instruction File and Workspace Trust Assessment
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-102** — Unsafe Model Serialization, Deserialization, and Artifact Loading Assessment
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment
- **P-057** — GPU Resource Sharing, AI Compute Infrastructure Isolation, and Runtime Security
- **P-108** — GPU Fault Injection, Shared Accelerator Isolation, and Model Integrity Assessment
- **P-086** — Confidential AI Computing, Protected Inference, and Sensitive Workload Architecture
- **P-109** — Confidential AI Computing and Remote Attestation Verification Laboratory
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-079** — Poisoned Knowledge Base, Compromised Agent Memory, and Model Rollback Recovery
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform

**Cross-layer catalog entries (7)**
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)

---

## Layer 9 — External AI Provider & Ecosystem Security

### Sublayer 9.1 — Hosted AI Provider Due Diligence

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment

**Primary catalog entries**
- None assigned

### Sublayer 9.2 — Multi-Provider Gateway, Routing & Cache Security

**Primary risks**
- **R-14** — AI gateway, provider routing, and cache failures

**Primary assessment projects**
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory

**Primary catalog entries**
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)

### Sublayer 9.3 — Third-Party MCP, Procurement & Ecosystem Trust

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-044** — Malicious MCP Server Configuration and Third-Party Trust Boundary Testing
- **P-098** — AI-Driven Procurement and Contract Management Agents: External Actions, Approval, and Supply Chain Trust Assessment

**Primary catalog entries**
- None assigned

### Sublayer 9.4 — Shadow AI & Unauthorized Provider Usage

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-112** — Enterprise Shadow AI Discovery, Inventory, and Unauthorized Data Egress Assessment

**Primary catalog entries**
- None assigned

### Layer 9 — Cross-layer dependencies

**Cross-layer security risks (21)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-02** — Tool misuse and unauthorized external actions
- **R-03** — RAG and connector permission failures
- **R-04** — Sensitive information and hidden-context disclosure
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-08** — Unsafe model-output handling
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-10** — MCP server, tool, and transport security failures
- **R-13** — Retrieval, ranking, vector, and embedding manipulation
- **R-15** — Model-serving and inference-runtime exposure
- **R-16** — Unsafe model loading, deserialization, and parser vulnerabilities
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-20** — Inter-agent and A2A communication abuse
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-29** — Model, intellectual-property, and artifact theft
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (49)**
- **P-003** — AI Security Engagement Scoping, Authorization, and Rules-of-Engagement Toolkit
- **P-004** — Automated AI Application Architecture Discovery and Attack Surface Mapping
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform
- **P-090** — AI Security Risk Quantification, Remediation Prioritization, and Acceptance Criteria Engineering
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-012** — OAuth Delegation, Consent, and Scope Abuse in Enterprise AI Agents
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-015** — Human-in-the-Loop Approval Integrity, Replay, and Transaction Binding
- **P-016** — Just-in-Time Privileged Access and Least-Privilege Enforcement for AI Agents
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security
- **P-020** — Cross-Cloud AI Workload Trust Relationships and Privilege Path Analysis
- **P-042** — MCP Server Impersonation, Discovery Spoofing, and Endpoint Trust Assessment
- **P-043** — MCP Authentication, Token Forwarding, and Delegated Authorization Security
- **P-045** — Agent-to-Agent Message Authentication, Spoofing, and Communication Integrity
- **P-050** — Autonomous Agent Action Budgets, Policy Enforcement, and Safe Delegation Architecture
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-029** — Hidden System Context, Confidential Instructions, and Reasoning Trace Exposure Assessment
- **P-031** — Enterprise RAG Connector Permission Inheritance and Access Control Assessment
- **P-037** — Stale Permissions, Deleted Documents, and Connector Synchronization Security
- **P-084** — Enterprise AI Data Retention, Deletion, and Privacy Lifecycle Security Assessment
- **P-085** — AI Application PII Detection, Data Minimization, and DLP Engineering
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-041** — MCP Tool Description, Parameter Schema, and Tool Selection Manipulation
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-082** — AI Bill of Materials, Model Dependencies, and Software Supply Chain Transparency Platform
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-102** — Unsafe Model Serialization, Deserialization, and Artifact Loading Assessment
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-106** — LLM Jailbreak, Multi-Turn Policy Evasion, and Misuse-Resistance Evaluation

**Cross-layer catalog entries (46)**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#6** — [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **#7** — [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- **#8** — [MCP reference servers](https://github.com/modelcontextprotocol/servers)
- **#9** — [MCP Scan (Snyk Agent Scan)](https://github.com/snyk/agent-scan)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#18** — [A2A protocol](https://github.com/a2aproject/A2A)
- **#19** — [Temporal](https://github.com/temporalio/temporal)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#39** — [Garak](https://github.com/NVIDIA/garak)
- **#40** — [PyRIT](https://github.com/microsoft/PyRIT)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#47** — [Presidio](https://github.com/microsoft/presidio)
- **#62** — [OWASP ZAP](https://github.com/zaproxy/zaproxy)
- **#65** — [Gitleaks](https://github.com/gitleaks/gitleaks)
- **#68** — [Trivy](https://github.com/aquasecurity/trivy)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#71** — [ModelScan](https://github.com/protectai/modelscan)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#77** — [in-toto](https://github.com/in-toto/in-toto)
- **#81** — [Harbor](https://github.com/goharbor/harbor)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#97** — [OpenCost](https://github.com/opencost/opencost)
- **#101** — [LocalStack](https://github.com/localstack/localstack)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#119** — [Wazuh](https://github.com/wazuh/wazuh)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#139** — [Dify](https://github.com/langgenius/dify)
- **#143** — [Nextcloud](https://github.com/nextcloud/server)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#147** — [Istio](https://github.com/istio/istio)
- **#150** — [mitmproxy](https://github.com/mitmproxy/mitmproxy)
- **#157** — [AWS test environment](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) *(AWS environment; not open-source software)*
- **#158** — [Grafana k6](https://github.com/grafana/k6)

---

## Layer 7 — Human, Governance & Operational Security

### Sublayer 7.1 — Engagement Governance & Risk Frameworks

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-003** — AI Security Engagement Scoping, Authorization, and Rules-of-Engagement Toolkit
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-089** — EU AI Act-Oriented Technical Security Evidence and High-Risk AI System Assurance Case Study
- **P-090** — AI Security Risk Quantification, Remediation Prioritization, and Acceptance Criteria Engineering

**Primary catalog entries**
- **#122** — [OWASP Threat Dragon](https://github.com/OWASP/threat-dragon)
- **#123** — [pytm](https://github.com/OWASP/pytm)
- **#124** — [Threagile](https://github.com/Threagile/threagile)
- **#125** — [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#127** — [OWASP ASVS](https://github.com/OWASP/ASVS)

### Sublayer 7.2 — Evidence, Accountability & Secure AI Lifecycle

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform

**Primary catalog entries**
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#142** — [Redmine](https://github.com/redmine/redmine)

### Sublayer 7.3 — AI Observability, Detection & SOC Security

**Primary risks**
- **R-22** — Guardrail, detector, validator, and monitoring limitations

**Primary assessment projects**
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-075** — Autonomous Agent Behavioral Drift, Tool Usage Anomalies, and Continuous Monitoring
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-095** — AI-Powered Security Operations Center: SOC Copilot Adversarial Testing and Purple Team Engagement

**Primary catalog entries**
- **#113** — [OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#115** — [OpenLLMetry](https://github.com/traceloop/openllmetry)
- **#116** — [Phoenix](https://github.com/Arize-ai/phoenix)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#118** — [Sigma](https://github.com/SigmaHQ/sigma)
- **#119** — [Wazuh](https://github.com/wazuh/wazuh)
- **#120** — [osquery](https://github.com/osquery/osquery)
- **#121** — [Fleet](https://github.com/fleetdm/fleet)

### Sublayer 7.4 — Resource Abuse, Availability & Resilience

**Primary risks**
- **R-18** — Denial of service, denial of wallet, and resource abuse

**Primary assessment projects**
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment

**Primary catalog entries**
- **#97** — [OpenCost](https://github.com/opencost/opencost)
- **#129** — [Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh)
- **#130** — [LitmusChaos](https://github.com/litmuschaos/litmus)
- **#158** — [Grafana k6](https://github.com/grafana/k6)

### Sublayer 7.5 — Incident Investigation, Containment & Purple Teaming

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-077** — Compromised AI Agent Incident Investigation and Digital Forensics Simulation
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-080** — AI Security Purple Team Exercise and Quantitative Control Effectiveness Evaluation

**Primary catalog entries**
- **#135** — [MITRE Caldera](https://github.com/apache/caldera)
- **#136** — [OpenCanary](https://github.com/thinkst/opencanary)
- **#137** — [T-Pot](https://github.com/telekom-security/tpotce)

### Sublayer 7.6 — Human Trust, Impersonation & Oversight

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-113** — AI-Enabled Phishing, Business Email Compromise, and Impersonation Defense Simulation
- **P-116** — Human-AI Trust Calibration, Approval Fatigue, Authority Manipulation, and Reviewer Reliability Laboratory

**Primary catalog entries**
- None assigned

### Sublayer 7.7 — Decision Integrity, Fairness & Appeal

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-115** — High-Impact AI Decision Fairness, Calibration, Explainability, and Appeal Assurance

**Primary catalog entries**
- **#131** — [Evidently](https://github.com/evidentlyai/evidently)

### Layer 7 — Cross-layer dependencies

**Cross-layer security risks (27)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-02** — Tool misuse and unauthorized external actions
- **R-03** — RAG and connector permission failures
- **R-04** — Sensitive information and hidden-context disclosure
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-10** — MCP server, tool, and transport security failures
- **R-11** — Memory poisoning and context-management failures
- **R-12** — Direct prompt injection
- **R-14** — AI gateway, provider routing, and cache failures
- **R-15** — Model-serving and inference-runtime exposure
- **R-19** — Data-pipeline and decision-input integrity failures
- **R-20** — Inter-agent and A2A communication abuse
- **R-21** — Evaluation, benchmark, and model-judge manipulation
- **R-23** — Jailbreaks, policy evasion, and harmful use
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-25** — Machine-learning privacy attacks
- **R-26** — Training, fine-tuning, and feedback poisoning or integrity failures
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures
- **R-29** — Model, intellectual-property, and artifact theft
- **R-30** — Adversarial evasion and robustness failures
- **R-34** — Media provenance, watermarking, and deepfake risks
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (53)**
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-012** — OAuth Delegation, Consent, and Scope Abuse in Enterprise AI Agents
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-015** — Human-in-the-Loop Approval Integrity, Replay, and Transaction Binding
- **P-016** — Just-in-Time Privileged Access and Least-Privilege Enforcement for AI Agents
- **P-050** — Autonomous Agent Action Budgets, Policy Enforcement, and Safe Delegation Architecture
- **P-092** — Autonomous Financial Operations Agent: Transaction Authorization, Fraud, and Privilege Security Assessment
- **P-098** — AI-Driven Procurement and Contract Management Agents: External Actions, Approval, and Supply Chain Trust Assessment
- **P-021** — Direct Prompt Injection and System Instruction Boundary Testing
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-029** — Hidden System Context, Confidential Instructions, and Reasoning Trace Exposure Assessment
- **P-041** — MCP Tool Description, Parameter Schema, and Tool Selection Manipulation
- **P-044** — Malicious MCP Server Configuration and Third-Party Trust Boundary Testing
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-047** — Autonomous Agent Goal Hijacking, Task Drift, and Workflow Integrity Assessment
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation
- **P-049** — Multi-Agent Cascading Failures, Compromised Agent Propagation, and Recovery
- **P-051** — AI Coding Agent Repository Instruction File and Workspace Trust Assessment
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-093** — Enterprise AI Coding Assistant: Repository, Developer Identity, Tool, and CI/CD Security Engagement
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-106** — LLM Jailbreak, Multi-Turn Policy Evasion, and Misuse-Resistance Evaluation
- **P-031** — Enterprise RAG Connector Permission Inheritance and Access Control Assessment
- **P-035** — Enterprise Knowledge Base Poisoning and Retrieval Corpus Integrity Assessment
- **P-037** — Stale Permissions, Deleted Documents, and Connector Synchronization Security
- **P-040** — Grounded AI Response Verification, False Citation Detection, and Knowledge Integrity Engineering
- **P-084** — Enterprise AI Data Retention, Deletion, and Privacy Lifecycle Security Assessment
- **P-085** — AI Application PII Detection, Data Minimization, and DLP Engineering
- **P-096** — Healthcare AI Assistant: Sensitive Data Access, Privacy, Retrieval, and Clinical Workflow Security Assessment
- **P-097** — Enterprise HR and Recruitment AI: Candidate Data Security, Decision Integrity, and Access Control Assessment
- **P-052** — AI-Generated Pull Request, CI/CD Pipeline, and Build System Compromise Simulation
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment
- **P-082** — AI Bill of Materials, Model Dependencies, and Software Supply Chain Transparency Platform
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-112** — Enterprise Shadow AI Discovery, Inventory, and Unauthorized Data Egress Assessment
- **P-061** — Supervised Learning Dataset Poisoning and Label Integrity Assessment
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-064** — Model Training Pipeline Dependency Tampering and Reproducibility Assessment
- **P-067** — Model Extraction, Prediction API Abuse, and Model Intellectual Property Protection
- **P-068** — Training Data Membership Inference and Privacy Leakage Assessment
- **P-070** — Online Learning Feedback Manipulation and Continuous Training Data Poisoning Assessment
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform
- **P-107** — Machine Unlearning Verification and Synthetic Data Privacy Assurance
- **P-111** — Synthetic Media Provenance, Watermarking, and Deepfake Verification Laboratory
- **P-114** — Cyber-Physical AI Sensor Manipulation, Actuator Authorization, and Emergency-Stop Simulation

**Cross-layer catalog entries (52)**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#2** — [OpenHands](https://github.com/OpenHands/OpenHands)
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#5** — [Purple Llama](https://github.com/meta-llama/PurpleLlama)
- **#6** — [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **#7** — [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#13** — [LangGraph](https://github.com/langchain-ai/langgraph)
- **#18** — [A2A protocol](https://github.com/a2aproject/A2A)
- **#19** — [Temporal](https://github.com/temporalio/temporal)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#28** — [Qdrant](https://github.com/qdrant/qdrant)
- **#31** — [Haystack](https://github.com/deepset-ai/haystack)
- **#35** — [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- **#39** — [Garak](https://github.com/NVIDIA/garak)
- **#40** — [PyRIT](https://github.com/microsoft/PyRIT)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#42** — [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals)
- **#45** — [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
- **#46** — [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- **#47** — [Presidio](https://github.com/microsoft/presidio)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#56** — [Falco](https://github.com/falcosecurity/falco)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#63** — [Semgrep](https://github.com/semgrep/semgrep)
- **#64** — [CodeQL](https://github.com/github/codeql)
- **#65** — [Gitleaks](https://github.com/gitleaks/gitleaks)
- **#68** — [Trivy](https://github.com/aquasecurity/trivy)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#77** — [in-toto](https://github.com/in-toto/in-toto)
- **#83** — [OpenLineage](https://github.com/OpenLineage/OpenLineage)
- **#84** — [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#132** — [c2patool](https://github.com/contentauth/c2patool)
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#139** — [Dify](https://github.com/langgenius/dify)
- **#143** — [Nextcloud](https://github.com/nextcloud/server)
- **#144** — [Label Studio](https://github.com/HumanSignal/label-studio)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#147** — [Istio](https://github.com/istio/istio)
- **#157** — [AWS test environment](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) *(AWS environment; not open-source software)*
- **#160** — [Open-Unlearning (TOFU benchmark)](https://github.com/locuslab/open-unlearning)

---

## Layer 4 — Model Lifecycle Security

### Sublayer 4.1 — Training Data Lineage & ML Pipeline Integrity

**Primary risks**
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures

**Primary assessment projects**
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-064** — Model Training Pipeline Dependency Tampering and Reproducibility Assessment

**Primary catalog entries**
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#83** — [OpenLineage](https://github.com/OpenLineage/OpenLineage)
- **#95** — [Kubeflow](https://github.com/kubeflow/kubeflow)
- **#144** — [Label Studio](https://github.com/HumanSignal/label-studio)

### Sublayer 4.2 — Training Poisoning & Feedback Integrity

**Primary risks**
- **R-26** — Training, fine-tuning, and feedback poisoning or integrity failures

**Primary assessment projects**
- **P-061** — Supervised Learning Dataset Poisoning and Label Integrity Assessment
- **P-070** — Online Learning Feedback Manipulation and Continuous Training Data Poisoning Assessment

**Primary catalog entries**
- **#34** — [PyTorch](https://github.com/pytorch/pytorch)

### Sublayer 4.3 — Fine-Tuning, Adapters & Model Backdoors

**Primary risks**
- **R-27** — Backdoored models, adapters, and model components

**Primary assessment projects**
- **P-062** — Fine-Tuned Language Model Backdoor Detection and Artifact Integrity Laboratory

**Primary catalog entries**
- **#33** — [Transformers](https://github.com/huggingface/transformers)
- **#36** — [PEFT](https://github.com/huggingface/peft)

### Sublayer 4.4 — Model Artifact Provenance & Safe Loading

**Primary risks**
- **R-16** — Unsafe model loading, deserialization, and parser vulnerabilities

**Primary assessment projects**
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-102** — Unsafe Model Serialization, Deserialization, and Artifact Loading Assessment

**Primary catalog entries**
- **#38** — [ONNX](https://github.com/onnx/onnx)
- **#71** — [ModelScan](https://github.com/protectai/modelscan)
- **#72** — [Fickling](https://github.com/trailofbits/fickling)
- **#73** — [Safetensors](https://github.com/huggingface/safetensors)

### Sublayer 4.5 — Model Extraction & Intellectual Property

**Primary risks**
- **R-29** — Model, intellectual-property, and artifact theft

**Primary assessment projects**
- **P-067** — Model Extraction, Prediction API Abuse, and Model Intellectual Property Protection

**Primary catalog entries**
- None assigned

### Sublayer 4.6 — Federated & Distributed Learning Security

**Primary risks**
- **R-33** — Federated and distributed-learning attacks

**Primary assessment projects**
- **P-110** — Federated Learning Poisoning, Malicious Participants, and Aggregation Security

**Primary catalog entries**
- **#90** — [Flower](https://github.com/flwrlabs/flower)
- **#91** — [PySyft](https://github.com/OpenMined/PySyft)

### Sublayer 4.7 — Enterprise MLOps Assurance & Unlearning

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-107** — Machine Unlearning Verification and Synthetic Data Privacy Assurance

**Primary catalog entries**
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#160** — [Open-Unlearning (TOFU benchmark)](https://github.com/locuslab/open-unlearning)

### Layer 4 — Cross-layer dependencies

**Cross-layer security risks (20)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-04** — Sensitive information and hidden-context disclosure
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-14** — AI gateway, provider routing, and cache failures
- **R-15** — Model-serving and inference-runtime exposure
- **R-17** — File upload, document parsing, and preprocessing attacks
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-19** — Data-pipeline and decision-input integrity failures
- **R-21** — Evaluation, benchmark, and model-judge manipulation
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-25** — Machine-learning privacy attacks
- **R-30** — Adversarial evasion and robustness failures
- **R-31** — Shared-hardware and accelerator isolation failures, including model fault injection
- **R-32** — Confidential-computing and attestation trust failures
- **R-34** — Media provenance, watermarking, and deepfake risks
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (47)**
- **P-001** — Reproducible Cloud-Native AI Security Laboratory and Infrastructure-as-Code Platform
- **P-002** — Synthetic Enterprise Data, Users, Assets, and Attack Scenario Generator
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-008** — AI Security Evaluation Datasets and Regression Testing Pipeline
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security
- **P-033** — Embedding-Based Sensitive Information Leakage and Semantic Inference Assessment
- **P-084** — Enterprise AI Data Retention, Deletion, and Privacy Lifecycle Security Assessment
- **P-085** — AI Application PII Detection, Data Minimization, and DLP Engineering
- **P-115** — High-Impact AI Decision Fairness, Calibration, Explainability, and Appeal Assurance
- **P-052** — AI-Generated Pull Request, CI/CD Pipeline, and Build System Compromise Simulation
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing
- **P-057** — GPU Resource Sharing, AI Compute Infrastructure Isolation, and Runtime Security
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-075** — Autonomous Agent Behavioral Drift, Tool Usage Anomalies, and Continuous Monitoring
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-079** — Poisoned Knowledge Base, Compromised Agent Memory, and Model Rollback Recovery
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment
- **P-082** — AI Bill of Materials, Model Dependencies, and Software Supply Chain Transparency Platform
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-086** — Confidential AI Computing, Protected Inference, and Sensitive Workload Architecture
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform
- **P-089** — EU AI Act-Oriented Technical Security Evidence and High-Risk AI System Assurance Case Study
- **P-090** — AI Security Risk Quantification, Remediation Prioritization, and Acceptance Criteria Engineering
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-065** — Adversarial Computer Vision Evasion and Robustness Evaluation
- **P-066** — Adversarial Text Classification Evasion and Defensive Robustness Testing
- **P-068** — Training Data Membership Inference and Privacy Leakage Assessment
- **P-069** — Model Inversion, Sensitive Feature Reconstruction, and Privacy Defense Evaluation
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-108** — GPU Fault Injection, Shared Accelerator Isolation, and Model Integrity Assessment
- **P-109** — Confidential AI Computing and Remote Attestation Verification Laboratory
- **P-111** — Synthetic Media Provenance, Watermarking, and Deepfake Verification Laboratory

**Cross-layer catalog entries (56)**
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#35** — [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#42** — [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals)
- **#45** — [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
- **#47** — [Presidio](https://github.com/microsoft/presidio)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#56** — [Falco](https://github.com/falcosecurity/falco)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#63** — [Semgrep](https://github.com/semgrep/semgrep)
- **#64** — [CodeQL](https://github.com/github/codeql)
- **#65** — [Gitleaks](https://github.com/gitleaks/gitleaks)
- **#68** — [Trivy](https://github.com/aquasecurity/trivy)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#75** — [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#77** — [in-toto](https://github.com/in-toto/in-toto)
- **#78** — [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator)
- **#79** — [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- **#80** — [GUAC](https://github.com/guacsec/guac)
- **#81** — [Harbor](https://github.com/goharbor/harbor)
- **#82** — [Sigstore Policy Controller](https://github.com/sigstore/policy-controller)
- **#84** — [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- **#85** — [secml](https://github.com/pralab/secml)
- **#86** — [ML Privacy Meter](https://github.com/privacytrustlab/ml_privacy_meter)
- **#87** — [TensorFlow Privacy](https://github.com/tensorflow/privacy)
- **#88** — [Opacus](https://github.com/pytorch/opacus)
- **#89** — [SDV](https://github.com/sdv-dev/SDV)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#93** — [Triton Inference Server](https://github.com/triton-inference-server/server)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#96** — [Ray](https://github.com/ray-project/ray)
- **#98** — [NVIDIA K8s device plugin](https://github.com/NVIDIA/k8s-device-plugin)
- **#99** — [NVIDIA GPU Operator](https://github.com/NVIDIA/gpu-operator)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#110** — [Checkov](https://github.com/bridgecrewio/checkov)
- **#111** — [Confidential Containers](https://github.com/confidential-containers/confidential-containers)
- **#112** — [Keylime](https://github.com/keylime/keylime)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#116** — [Phoenix](https://github.com/Arize-ai/phoenix)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#125** — [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#131** — [Evidently](https://github.com/evidentlyai/evidently)
- **#132** — [c2patool](https://github.com/contentauth/c2patool)
- **#133** — [MarkLLM](https://github.com/THU-BPM/MarkLLM)
- **#134** — [DeepfakeBench](https://github.com/SCLBD/DeepfakeBench)
- **#158** — [Grafana k6](https://github.com/grafana/k6)

---

## Layer 3 — Internal AI Mechanism Security

### Sublayer 3.1 — Evaluation, Benchmarks & Model Judges

**Primary risks**
- **R-21** — Evaluation, benchmark, and model-judge manipulation

**Primary assessment projects**
- **P-008** — AI Security Evaluation Datasets and Regression Testing Pipeline
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform

**Primary catalog entries**
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#42** — [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals)
- **#43** — [Giskard](https://github.com/Giskard-AI/giskard-oss)
- **#44** — [DeepTeam](https://github.com/confident-ai/deepteam)

### Sublayer 3.2 — Adversarial Evasion & Model Robustness

**Primary risks**
- **R-30** — Adversarial evasion and robustness failures

**Primary assessment projects**
- **P-065** — Adversarial Computer Vision Evasion and Robustness Evaluation
- **P-066** — Adversarial Text Classification Evasion and Defensive Robustness Testing

**Primary catalog entries**
- **#35** — [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- **#84** — [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- **#85** — [secml](https://github.com/pralab/secml)

### Sublayer 3.3 — Privacy Inference & Privacy-Preserving ML

**Primary risks**
- **R-25** — Machine-learning privacy attacks

**Primary assessment projects**
- **P-068** — Training Data Membership Inference and Privacy Leakage Assessment
- **P-069** — Model Inversion, Sensitive Feature Reconstruction, and Privacy Defense Evaluation

**Primary catalog entries**
- **#86** — [ML Privacy Meter](https://github.com/privacytrustlab/ml_privacy_meter)
- **#87** — [TensorFlow Privacy](https://github.com/tensorflow/privacy)
- **#88** — [Opacus](https://github.com/pytorch/opacus)

### Sublayer 3.4 — LLM Guardrails, Jailbreaks & Policy Evasion

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-106** — LLM Jailbreak, Multi-Turn Policy Evasion, and Misuse-Resistance Evaluation

**Primary catalog entries**
- **#5** — [Purple Llama](https://github.com/meta-llama/PurpleLlama)
- **#39** — [Garak](https://github.com/NVIDIA/garak)
- **#40** — [PyRIT](https://github.com/microsoft/PyRIT)
- **#45** — [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
- **#46** — [Guardrails AI](https://github.com/guardrails-ai/guardrails)

### Sublayer 3.5 — Synthetic Media, Watermarks & Provenance

**Primary risks**
- **R-34** — Media provenance, watermarking, and deepfake risks

**Primary assessment projects**
- **P-111** — Synthetic Media Provenance, Watermarking, and Deepfake Verification Laboratory

**Primary catalog entries**
- **#132** — [c2patool](https://github.com/contentauth/c2patool)
- **#133** — [MarkLLM](https://github.com/THU-BPM/MarkLLM)
- **#134** — [DeepfakeBench](https://github.com/SCLBD/DeepfakeBench)

### Layer 3 — Cross-layer dependencies

**Cross-layer security risks (22)**
- **R-04** — Sensitive information and hidden-context disclosure
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-08** — Unsafe model-output handling
- **R-11** — Memory poisoning and context-management failures
- **R-12** — Direct prompt injection
- **R-13** — Retrieval, ranking, vector, and embedding manipulation
- **R-15** — Model-serving and inference-runtime exposure
- **R-16** — Unsafe model loading, deserialization, and parser vulnerabilities
- **R-17** — File upload, document parsing, and preprocessing attacks
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-19** — Data-pipeline and decision-input integrity failures
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-23** — Jailbreaks, policy evasion, and harmful use
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-26** — Training, fine-tuning, and feedback poisoning or integrity failures
- **R-27** — Backdoored models, adapters, and model components
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures
- **R-29** — Model, intellectual-property, and artifact theft
- **R-33** — Federated and distributed-learning attacks
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (47)**
- **P-002** — Synthetic Enterprise Data, Users, Assets, and Attack Scenario Generator
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-021** — Direct Prompt Injection and System Instruction Boundary Testing
- **P-022** — Indirect Prompt Injection Through Retrieved Enterprise Documents
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-025** — Image-Based Multimodal Prompt Injection Security Laboratory
- **P-026** — Audio and Speech-Based Instruction Injection Assessment
- **P-027** — Video Frame, Caption, and Subtitle Injection Against Multimodal Agents
- **P-028** — Structured Data, CSV, and Spreadsheet Instruction Injection Testing
- **P-029** — Hidden System Context, Confidential Instructions, and Reasoning Trace Exposure Assessment
- **P-030** — Unsafe LLM Output Handling, Command Injection, and Application Injection Chains
- **P-033** — Embedding-Based Sensitive Information Leakage and Semantic Inference Assessment
- **P-034** — Retrieval Ranking Manipulation and Search Result Integrity Testing
- **P-035** — Enterprise Knowledge Base Poisoning and Retrieval Corpus Integrity Assessment
- **P-036** — Document Provenance, Citation Forgery, and Evidence Laundering Assessment
- **P-040** — Grounded AI Response Verification, False Citation Detection, and Knowledge Integrity Engineering
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-047** — Autonomous Agent Goal Hijacking, Task Drift, and Workflow Integrity Assessment
- **P-053** — AI-Generated Code Vulnerability Detection and Secure Code Generation Pipeline
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-061** — Supervised Learning Dataset Poisoning and Label Integrity Assessment
- **P-062** — Fine-Tuned Language Model Backdoor Detection and Artifact Integrity Laboratory
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-064** — Model Training Pipeline Dependency Tampering and Reproducibility Assessment
- **P-067** — Model Extraction, Prediction API Abuse, and Model Intellectual Property Protection
- **P-070** — Online Learning Feedback Manipulation and Continuous Training Data Poisoning Assessment
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-075** — Autonomous Agent Behavioral Drift, Tool Usage Anomalies, and Continuous Monitoring
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-079** — Poisoned Knowledge Base, Compromised Agent Memory, and Model Rollback Recovery
- **P-084** — Enterprise AI Data Retention, Deletion, and Privacy Lifecycle Security Assessment
- **P-085** — AI Application PII Detection, Data Minimization, and DLP Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform
- **P-091** — Enterprise Knowledge Assistant: Complete RAG Penetration Test and Security Architecture Review
- **P-094** — Multi-Tenant Customer Support AI: Data Privacy, Isolation, Prompt Injection, and Incident Response Engagement
- **P-096** — Healthcare AI Assistant: Sensitive Data Access, Privacy, Retrieval, and Clinical Workflow Security Assessment
- **P-097** — Enterprise HR and Recruitment AI: Candidate Data Security, Decision Integrity, and Access Control Assessment
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-102** — Unsafe Model Serialization, Deserialization, and Artifact Loading Assessment
- **P-103** — AI File Upload, Document Parser, and Preprocessing Security Laboratory
- **P-107** — Machine Unlearning Verification and Synthetic Data Privacy Assurance
- **P-110** — Federated Learning Poisoning, Malicious Participants, and Aggregation Security
- **P-115** — High-Impact AI Decision Fairness, Calibration, Explainability, and Appeal Assurance

**Cross-layer catalog entries (48)**
- **#1** — [Onyx](https://github.com/onyx-dot-app/onyx)
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#13** — [LangGraph](https://github.com/langchain-ai/langgraph)
- **#28** — [Qdrant](https://github.com/qdrant/qdrant)
- **#29** — [pgvector](https://github.com/pgvector/pgvector)
- **#30** — [sentence-transformers](https://github.com/huggingface/sentence-transformers)
- **#31** — [Haystack](https://github.com/deepset-ai/haystack)
- **#32** — [LlamaIndex](https://github.com/run-llama/llama_index)
- **#33** — [Transformers](https://github.com/huggingface/transformers)
- **#34** — [PyTorch](https://github.com/pytorch/pytorch)
- **#36** — [PEFT](https://github.com/huggingface/peft)
- **#37** — [llama.cpp](https://github.com/ggml-org/llama.cpp)
- **#38** — [ONNX](https://github.com/onnx/onnx)
- **#47** — [Presidio](https://github.com/microsoft/presidio)
- **#48** — [Pydantic](https://github.com/pydantic/pydantic)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#71** — [ModelScan](https://github.com/protectai/modelscan)
- **#72** — [Fickling](https://github.com/trailofbits/fickling)
- **#73** — [Safetensors](https://github.com/huggingface/safetensors)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#83** — [OpenLineage](https://github.com/OpenLineage/OpenLineage)
- **#89** — [SDV](https://github.com/sdv-dev/SDV)
- **#90** — [Flower](https://github.com/flwrlabs/flower)
- **#91** — [PySyft](https://github.com/OpenMined/PySyft)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#93** — [Triton Inference Server](https://github.com/triton-inference-server/server)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#95** — [Kubeflow](https://github.com/kubeflow/kubeflow)
- **#96** — [Ray](https://github.com/ray-project/ray)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#116** — [Phoenix](https://github.com/Arize-ai/phoenix)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#125** — [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#131** — [Evidently](https://github.com/evidentlyai/evidently)
- **#138** — [Open WebUI](https://github.com/open-webui/open-webui)
- **#139** — [Dify](https://github.com/langgenius/dify)
- **#143** — [Nextcloud](https://github.com/nextcloud/server)
- **#144** — [Label Studio](https://github.com/HumanSignal/label-studio)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#159** — [Docling](https://github.com/docling-project/docling)
- **#160** — [Open-Unlearning (TOFU benchmark)](https://github.com/locuslab/open-unlearning)

---

## Layer 1 — Hardware & Compute Security

### Sublayer 1.1 — GPU Resource Scheduling & Tenant Isolation

**Primary risks**
- **R-31** — Shared-hardware and accelerator isolation failures, including model fault injection

**Primary assessment projects**
- **P-057** — GPU Resource Sharing, AI Compute Infrastructure Isolation, and Runtime Security

**Primary catalog entries**
- **#98** — [NVIDIA K8s device plugin](https://github.com/NVIDIA/k8s-device-plugin)
- **#99** — [NVIDIA GPU Operator](https://github.com/NVIDIA/gpu-operator)
- **#100** — [Slurm](https://github.com/SchedMD/slurm)

### Sublayer 1.2 — GPU Fault Injection & Model Integrity

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-108** — GPU Fault Injection, Shared Accelerator Isolation, and Model Integrity Assessment

**Primary catalog entries**
- None assigned

### Sublayer 1.3 — Confidential AI Computing & Protected Inference

**Primary risks**
- **R-32** — Confidential-computing and attestation trust failures

**Primary assessment projects**
- **P-086** — Confidential AI Computing, Protected Inference, and Sensitive Workload Architecture

**Primary catalog entries**
- **#111** — [Confidential Containers](https://github.com/confidential-containers/confidential-containers)

### Sublayer 1.4 — Remote Attestation & Hardware Trust

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-109** — Confidential AI Computing and Remote Attestation Verification Laboratory

**Primary catalog entries**
- **#112** — [Keylime](https://github.com/keylime/keylime)

### Layer 1 — Cross-layer dependencies

**Cross-layer security risks (20)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-04** — Sensitive information and hidden-context disclosure
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-08** — Unsafe model-output handling
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-14** — AI gateway, provider routing, and cache failures
- **R-15** — Model-serving and inference-runtime exposure
- **R-16** — Unsafe model loading, deserialization, and parser vulnerabilities
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-19** — Data-pipeline and decision-input integrity failures
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-24** — Privacy-control, synthetic-data, and unlearning assurance failures
- **R-25** — Machine-learning privacy attacks
- **R-27** — Backdoored models, adapters, and model components
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures
- **R-29** — Model, intellectual-property, and artifact theft
- **R-33** — Federated and distributed-learning attacks
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise
- **R-37** — Cascading failures and unsafe recovery

**Cross-layer assessment projects (38)**
- **P-001** — Reproducible Cloud-Native AI Security Laboratory and Infrastructure-as-Code Platform
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-013** — Service Account Impersonation and Privilege Escalation in AI Workloads
- **P-017** — Multi-Tenant AI API Broken Object-Level Authorization Assessment
- **P-019** — AI Secrets Management, Credential Rotation, and Vault Integration Security
- **P-020** — Cross-Cloud AI Workload Trust Relationships and Privilege Path Analysis
- **P-052** — AI-Generated Pull Request, CI/CD Pipeline, and Build System Compromise Simulation
- **P-054** — AI Code Execution Sandbox Isolation and Escape Resistance Assessment
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-060** — AI Tool Network Egress, SSRF, and Unauthorized External Connectivity Assessment
- **P-101** — Multi-Provider AI Gateway Routing, Cache Isolation, and Failover Security Laboratory
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-064** — Model Training Pipeline Dependency Tampering and Reproducibility Assessment
- **P-067** — Model Extraction, Prediction API Abuse, and Model Intellectual Property Protection
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-102** — Unsafe Model Serialization, Deserialization, and Artifact Loading Assessment
- **P-110** — Federated Learning Poisoning, Malicious Participants, and Aggregation Security
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-072** — Multi-Tenant AI Service Denial-of-Wallet, Quota Abuse, and Availability Assessment
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-076** — AI Data Exfiltration and Model Extraction Detection Engineering
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-080** — AI Security Purple Team Exercise and Quantitative Control Effectiveness Evaluation
- **P-081** — Third-Party AI Provider, Hosted Model, and API Security Due Diligence Assessment
- **P-082** — AI Bill of Materials, Model Dependencies, and Software Supply Chain Transparency Platform
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform
- **P-090** — AI Security Risk Quantification, Remediation Prioritization, and Acceptance Criteria Engineering
- **P-099** — Multi-Cloud Enterprise Agentic AI Platform: Full-Scope Red Team and Security Architecture Engagement

**Cross-layer catalog entries (53)**
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#34** — [PyTorch](https://github.com/pytorch/pytorch)
- **#37** — [llama.cpp](https://github.com/ggml-org/llama.cpp)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#50** — [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#52** — [Firecracker](https://github.com/firecracker-microvm/firecracker)
- **#53** — [Kata Containers](https://github.com/kata-containers/kata-containers)
- **#54** — [nsjail](https://github.com/google/nsjail)
- **#55** — [Wasmtime](https://github.com/bytecodealliance/wasmtime)
- **#56** — [Falco](https://github.com/falcosecurity/falco)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#63** — [Semgrep](https://github.com/semgrep/semgrep)
- **#68** — [Trivy](https://github.com/aquasecurity/trivy)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#71** — [ModelScan](https://github.com/protectai/modelscan)
- **#72** — [Fickling](https://github.com/trailofbits/fickling)
- **#73** — [Safetensors](https://github.com/huggingface/safetensors)
- **#74** — [Syft](https://github.com/anchore/syft)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#77** — [in-toto](https://github.com/in-toto/in-toto)
- **#78** — [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator)
- **#81** — [Harbor](https://github.com/goharbor/harbor)
- **#82** — [Sigstore Policy Controller](https://github.com/sigstore/policy-controller)
- **#83** — [OpenLineage](https://github.com/OpenLineage/OpenLineage)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#93** — [Triton Inference Server](https://github.com/triton-inference-server/server)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#95** — [Kubeflow](https://github.com/kubeflow/kubeflow)
- **#96** — [Ray](https://github.com/ray-project/ray)
- **#97** — [OpenCost](https://github.com/opencost/opencost)
- **#101** — [LocalStack](https://github.com/localstack/localstack)
- **#102** — [Cloudsplaining](https://github.com/salesforce/cloudsplaining)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#104** — [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat)
- **#106** — [kube-bench](https://github.com/aquasecurity/kube-bench)
- **#107** — [OPA Gatekeeper](https://github.com/open-policy-agent/gatekeeper)
- **#108** — [Kyverno](https://github.com/kyverno/kyverno)
- **#110** — [Checkov](https://github.com/bridgecrewio/checkov)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#129** — [Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh)
- **#130** — [LitmusChaos](https://github.com/litmuschaos/litmus)
- **#147** — [Istio](https://github.com/istio/istio)
- **#148** — [Prowler](https://github.com/prowler-cloud/prowler)
- **#149** — [OpenTofu](https://github.com/opentofu/opentofu)
- **#157** — [AWS test environment](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) *(AWS environment; not open-source software)*
- **#158** — [Grafana k6](https://github.com/grafana/k6)

---

## Layer 10 — Cyber-Physical AI Security

### Sublayer 10.1 — Sensor & Perception Integrity

**Primary risks**
- None assigned

**Primary assessment projects**
- **P-114** — Cyber-Physical AI Sensor Manipulation, Actuator Authorization, and Emergency-Stop Simulation

**Primary catalog entries**
- None assigned

**Additional repositories outside original catalog**
- [ROS 2](https://github.com/ros2/ros2)
- [Gazebo Sim](https://github.com/gazebosim/gz-sim)

### Sublayer 10.2 — Actuator Authorization & Safety Interlocks

**Primary risks**
- None assigned

**Primary assessment projects**
- None assigned

**Primary catalog entries**
- None assigned

**Additional repositories outside original catalog**
- [open62541](https://github.com/open62541/open62541)

### Sublayer 10.3 — Cascading Failures & Safe Recovery

**Primary risks**
- **R-37** — Cascading failures and unsafe recovery

**Primary assessment projects**
- None assigned

**Primary catalog entries**
- None assigned

**Additional repositories outside original catalog**
- [CARLA](https://github.com/carla-simulator/carla)

### Layer 10 — Cross-layer dependencies

**Cross-layer security risks (23)**
- **R-01** — Workload identity, impersonation, and delegation abuse
- **R-02** — Tool misuse and unauthorized external actions
- **R-05** — Indirect and multimodal prompt injection
- **R-06** — Agent goal hijacking, misalignment, and excessive autonomy
- **R-07** — Approval bypass and human-agent trust exploitation
- **R-08** — Unsafe model-output handling
- **R-09** — Coding-agent, repository, and workspace compromise
- **R-10** — MCP server, tool, and transport security failures
- **R-11** — Memory poisoning and context-management failures
- **R-15** — Model-serving and inference-runtime exposure
- **R-17** — File upload, document parsing, and preprocessing attacks
- **R-18** — Denial of service, denial of wallet, and resource abuse
- **R-19** — Data-pipeline and decision-input integrity failures
- **R-20** — Inter-agent and A2A communication abuse
- **R-21** — Evaluation, benchmark, and model-judge manipulation
- **R-22** — Guardrail, detector, validator, and monitoring limitations
- **R-26** — Training, fine-tuning, and feedback poisoning or integrity failures
- **R-27** — Backdoored models, adapters, and model components
- **R-28** — ML pipeline, experiment, and model-lifecycle integrity failures
- **R-30** — Adversarial evasion and robustness failures
- **R-31** — Shared-hardware and accelerator isolation failures, including model fault injection
- **R-35** — Tenant and user isolation failures
- **R-36** — AI supply-chain and dependency compromise

**Cross-layer assessment projects (56)**
- **P-001** — Reproducible Cloud-Native AI Security Laboratory and Infrastructure-as-Code Platform
- **P-002** — Synthetic Enterprise Data, Users, Assets, and Attack Scenario Generator
- **P-003** — AI Security Engagement Scoping, Authorization, and Rules-of-Engagement Toolkit
- **P-005** — AI Threat Modeling-as-Code and Trust Boundary Analysis System
- **P-007** — AI Security Control Regression Testing and Evidence Reproduction Framework
- **P-008** — AI Security Evaluation Datasets and Regression Testing Pipeline
- **P-009** — Security Evidence Collection, Telemetry, and Reproducibility Platform
- **P-010** — AI Security Findings, Risk Register, and Consultancy Report Generator
- **P-011** — Cloud AI Workload Identity Federation and Token Exchange Security Assessment
- **P-014** — AI Agent Confused-Deputy Attack and Authorization Boundary Assessment
- **P-015** — Human-in-the-Loop Approval Integrity, Replay, and Transaction Binding
- **P-016** — Just-in-Time Privileged Access and Least-Privilege Enforcement for AI Agents
- **P-043** — MCP Authentication, Token Forwarding, and Delegated Authorization Security
- **P-045** — Agent-to-Agent Message Authentication, Spoofing, and Communication Integrity
- **P-048** — Unauthorized External Actions Through AI Agent Tool Invocation
- **P-050** — Autonomous Agent Action Budgets, Policy Enforcement, and Safe Delegation Architecture
- **P-116** — Human-AI Trust Calibration, Approval Fatigue, Authority Manipulation, and Reviewer Reliability Laboratory
- **P-021** — Direct Prompt Injection and System Instruction Boundary Testing
- **P-024** — External API and Tool-Response Prompt Injection Assessment
- **P-025** — Image-Based Multimodal Prompt Injection Security Laboratory
- **P-026** — Audio and Speech-Based Instruction Injection Assessment
- **P-027** — Video Frame, Caption, and Subtitle Injection Against Multimodal Agents
- **P-030** — Unsafe LLM Output Handling, Command Injection, and Application Injection Chains
- **P-041** — MCP Tool Description, Parameter Schema, and Tool Selection Manipulation
- **P-046** — Persistent AI Agent Memory Poisoning and Long-Term State Manipulation
- **P-047** — Autonomous Agent Goal Hijacking, Task Drift, and Workflow Integrity Assessment
- **P-049** — Multi-Agent Cascading Failures, Compromised Agent Propagation, and Recovery
- **P-065** — Adversarial Computer Vision Evasion and Robustness Evaluation
- **P-055** — LLM Inference Server, API Gateway, and Model Serving Infrastructure Hardening
- **P-056** — Kubernetes AI Workload Isolation, Service Account Security, and Lateral Movement Testing
- **P-057** — GPU Resource Sharing, AI Compute Infrastructure Isolation, and Runtime Security
- **P-058** — Model Registry, Model Artifact Signing, and Integrity Verification Assessment
- **P-059** — Agent Skills, Plugins, Dependencies, and AI Software Supply Chain Security
- **P-061** — Supervised Learning Dataset Poisoning and Label Integrity Assessment
- **P-062** — Fine-Tuned Language Model Backdoor Detection and Artifact Integrity Laboratory
- **P-063** — Training Data Provenance, Dataset Lineage, and Integrity Verification Pipeline
- **P-070** — Online Learning Feedback Manipulation and Continuous Training Data Poisoning Assessment
- **P-086** — Confidential AI Computing, Protected Inference, and Sensitive Workload Architecture
- **P-100** — Enterprise Model Development and MLOps Platform: End-to-End Model Lifecycle, Infrastructure, and Security Assurance Engagement
- **P-108** — GPU Fault Injection, Shared Accelerator Isolation, and Model Integrity Assessment
- **P-109** — Confidential AI Computing and Remote Attestation Verification Laboratory
- **P-110** — Federated Learning Poisoning, Malicious Participants, and Aggregation Security
- **P-071** — AI Agent Infinite Loops, Unbounded Consumption, and Resource Exhaustion Testing
- **P-073** — AI Security Audit Log Tampering, Log Injection, and Evidence Integrity Testing
- **P-074** — AI-Specific Security Detection Rules, Behavioral Monitoring, and Alerting Platform
- **P-075** — Autonomous Agent Behavioral Drift, Tool Usage Anomalies, and Continuous Monitoring
- **P-077** — Compromised AI Agent Incident Investigation and Digital Forensics Simulation
- **P-078** — AI Agent Emergency Containment, Credential Revocation, and Kill-Switch Engineering
- **P-080** — AI Security Purple Team Exercise and Quantitative Control Effectiveness Evaluation
- **P-083** — AI Security Control Mapping Against OWASP, NIST, MITRE ATLAS, and Enterprise Standards
- **P-087** — Cryptographic Audit Trails, Agent Action Attestation, and Accountability Engineering
- **P-088** — Secure AI Development Lifecycle, Security Gates, and Continuous Assurance Platform
- **P-090** — AI Security Risk Quantification, Remediation Prioritization, and Acceptance Criteria Engineering
- **P-104** — LLM Evaluation Benchmark Poisoning, Judge Manipulation, and Evaluation Integrity Platform
- **P-105** — AI Guardrail, Safety Detector, and Validator Bypass-Resistance Assessment
- **P-115** — High-Impact AI Decision Fairness, Calibration, Explainability, and Appeal Assurance

**Cross-layer catalog entries (52)**
- **#3** — [Promptfoo](https://github.com/promptfoo/promptfoo)
- **#4** — [AgentDojo](https://github.com/ethz-spylab/agentdojo)
- **#6** — [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **#12** — [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- **#13** — [LangGraph](https://github.com/langchain-ai/langgraph)
- **#18** — [A2A protocol](https://github.com/a2aproject/A2A)
- **#19** — [Temporal](https://github.com/temporalio/temporal)
- **#21** — [Keycloak](https://github.com/keycloak/keycloak)
- **#22** — [OpenFGA](https://github.com/openfga/openfga)
- **#23** — [OPA](https://github.com/open-policy-agent/opa)
- **#25** — [SPIFFE](https://github.com/spiffe/spiffe)
- **#26** — [SPIRE](https://github.com/spiffe/spire)
- **#27** — [HashiCorp Vault](https://github.com/hashicorp/vault)
- **#34** — [PyTorch](https://github.com/pytorch/pytorch)
- **#41** — [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- **#45** — [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
- **#48** — [Pydantic](https://github.com/pydantic/pydantic)
- **#49** — [LiteLLM](https://github.com/BerriAI/litellm)
- **#51** — [gVisor](https://github.com/google/gvisor)
- **#56** — [Falco](https://github.com/falcosecurity/falco)
- **#57** — [Tetragon](https://github.com/cilium/tetragon)
- **#63** — [Semgrep](https://github.com/semgrep/semgrep)
- **#69** — [MLflow](https://github.com/mlflow/mlflow)
- **#70** — [DVC](https://github.com/treeverse/dvc)
- **#73** — [Safetensors](https://github.com/huggingface/safetensors)
- **#76** — [Cosign](https://github.com/sigstore/cosign)
- **#84** — [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- **#92** — [vLLM](https://github.com/vllm-project/vllm)
- **#94** — [KServe](https://github.com/kserve/kserve)
- **#95** — [Kubeflow](https://github.com/kubeflow/kubeflow)
- **#98** — [NVIDIA K8s device plugin](https://github.com/NVIDIA/k8s-device-plugin)
- **#99** — [NVIDIA GPU Operator](https://github.com/NVIDIA/gpu-operator)
- **#103** — [kind](https://github.com/kubernetes-sigs/kind)
- **#111** — [Confidential Containers](https://github.com/confidential-containers/confidential-containers)
- **#112** — [Keylime](https://github.com/keylime/keylime)
- **#114** — [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- **#117** — [Langfuse](https://github.com/langfuse/langfuse)
- **#118** — [Sigma](https://github.com/SigmaHQ/sigma)
- **#119** — [Wazuh](https://github.com/wazuh/wazuh)
- **#122** — [OWASP Threat Dragon](https://github.com/OWASP/threat-dragon)
- **#125** — [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data)
- **#126** — [OWASP AISVS](https://github.com/OWASP/AISVS)
- **#127** — [OWASP ASVS](https://github.com/OWASP/ASVS)
- **#128** — [NIST OSCAL](https://github.com/usnistgov/OSCAL)
- **#129** — [Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh)
- **#130** — [LitmusChaos](https://github.com/litmuschaos/litmus)
- **#131** — [Evidently](https://github.com/evidentlyai/evidently)
- **#144** — [Label Studio](https://github.com/HumanSignal/label-studio)
- **#145** — [Playwright](https://github.com/microsoft/playwright)
- **#147** — [Istio](https://github.com/istio/istio)
- **#149** — [OpenTofu](https://github.com/opentofu/opentofu)
- **#158** — [Grafana k6](https://github.com/grafana/k6)

---

## Final reconciliation

| Inventory | Distinct primary assignments | Expected |
|---|---:|---:|
| Security risks | 37 | 37 |
| Assessment projects | 116 | 116 |
| Catalog entries | 160 | 160 |
| Sublayers | 57 | 57 |
| Layer 10 additional external repositories | 4 | 4 |


## Source hierarchy and change control

- Original canonical technical IDs, titles and P-project mappings: `AI_Security_10_Layers_Complete_Sub_Sublayers_2026.md` (preserved verbatim in this checklist).
- Original primary risks, projects, technology choices and cross-layer assignments: supporting original inventory included immediately above.
- Suggested B/A/C per-sublayer language: `AI_Security_10_Layers_57_Sublayers_334_Case_B_Enhanced_Final_2026.md`, aided by the earlier `AI_Security_Engineering_Master_10_Layer_Checklist_B_First_A_Second_2026.md`.
- Case B-01–B-73 labels and links: new conversation taxonomy; mappings are proposed and may be changed based on actual verification.
- Track any changed mapping with source, date, rationale and overlap review. Official version-specific docs and actual test artifacts control claims about real deployed systems.
- The separate 110-risk file is the authoritative learning-order list; this curriculum keeps the original technical layer order rather than copying the nine risk phases.

## Final structural verification

- Canonical layers: **10**.
- Canonical sublayers: **57**.
- Original sub-sublayers: **334 unique IDs**, exact original titles and P-project assignments preserved.
- Original projects referenced in canonical work packages: **116 unique P-IDs**.
- Case B suggested mapping: **73 unique B IDs**, each linked to an existing sublayer.
- Original risk source: **37 R IDs**, retained in the primary/cross-layer reference.
- Original catalog: **160 inventory entries** allocated in the source, not a claim of 160 deployed tools.
- No assessed control, vulnerability, coverage percentage, or model behavior is claimed to be empirically verified by this document.
