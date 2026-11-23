# P-006 Phase B — REQ-07 integration result

**PASS for the added preview route in the authorized local Open WebUI deployment.** The candidate produced through native chat included `LAB-INT-042`. The preview stayed held until the analyst confirmed the audience and the assigned reviewer approved the facts. The ready preview contained the three approved fields. An independent SQLite connection confirmed the transition. The six controlled T03 variants also passed. [HTTP and database evidence](evidence/http.jsonl) · [Execution command and status](evidence/test-command.txt)

**Run** `0888c4f5-6e30-4a3c-8582-668e35d18d6e` · **Lab** `P006-CASEB-LAB-01-B` · **Date** 2026-11-22

## Verified deployment and authority

The isolated runtime returned Open WebUI `0.13.4`. Its OCI Linux amd64 manifest was `sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1`. The image label and build hash matched upstream commit `0666e59d26a4d056e0bacee41742486badd71cf8`. Four installed modules matched the Git checkout by SHA-256, including the native chat, authorization and model route modules. The design was committed before writing the extension. [Design](design.md) · [Image pull](evidence/pull.txt) · [Upstream source hashes](evidence/upstream.txt) · [Runtime record](evidence/http.jsonl)

The analyst, reviewer and unrelated analyst authenticated as real Open WebUI users in the isolated app. Separate `user` table reads confirmed their IDs and standard roles. The bootstrap administrator registered the sole local model and granted `read` to the analyst. The test confirmed that grant through `access_grant`, listed the model as the analyst, and sent the frozen T02-A input through `/api/chat/completions`. The result identified the pinned model and llama.cpp engine, and the saved private chat matched the exact assistant text. Both containers shared a network namespace with loopback as its only interface and no published ports. [Runtime topology](evidence/topology.txt) · [Native model and account evidence](evidence/http.jsonl)

## Application and policy checks

| Scenario | Result and independent effect |
| --- | --- |
| Actual model candidate | `PASS`. Native HTTP and the private database record matched. Preview and separate row were `HELD` before review and `READY` with the approved text after both decisions. Only the candidate digest crossed into the notice store. |
| T03-A · Wrong candidate | `PASS`. The stored ready text matched the approved window and action. It omitted the wrong `15:00` and the ticket. |
| T03-B · Clean candidate | `PASS`. The fixed candidate with approved content yielded the same HTTP and SQLite preview. |
| T03-C · No audience confirmation | `PASS`. The stored ready flag stayed false despite approved facts. |
| T03-D · Old revision | `PASS`. Stale approval received HTTP `409`. No approval or ready preview persisted for that attempt. |
| T03-E · Incomplete facts | `PASS`. Missing action was rejected at request validation with HTTP `422`. The notice remained held with no approved facts. |
| T03-F · Different audience | `PASS`. Service-desk confirmation did not make the employee preview ready. |
| Identity and unsupported action checks | `PASS` within the covered routes. An unrelated analyst received `404` on the owner's notice, and analyst approval calls received `403`. Missing authentication received `401`. The frontend fallback rejected the unsupported publication POST with `405`. Native chat sharing returned `401` under the enforced standard-user permission. |
| Advance revision | `PASS`. Revision 3 cleared the confirmation, approvals and preview. A revision 2 preview request received `409`. |

The harness used read-only SQLite connections after each preview and tied the row to the native owner, exact assistant message and assigned reviewer. It compared `shared_chat`, `tool`, `tool_history`, `automation`, `automation_run` and `notification` before and after. Each count was zero at both boundaries. The environment had no external route. The observations cover the listed stores and this exercised workflow. [Independent observations](evidence/http.jsonl) · [Isolation and teardown](evidence/topology.txt)

## Retest and limits

The isolated startup first needed readable bind-mounted source, a nonempty in-memory session key and a precreated private data directory. The first authenticated preflight confirmed that the base model was not listed to the analyst before a native grant. Test harness fixes addressed its import and body encoding, then aligned expected denial codes with the actual upstream sharing route and frontend fallback. The early attempts, including a partial run with a real model completion, are preserved. The final invocation exercised all six cases and exited `0`. [Preserved diagnostics](evidence/diagnostics/) · [Final native run](evidence/http.jsonl) · [Final application restart](evidence/restart-status.txt)

The change is an additive backend route with no browser UI for the gate. Reviewer assignment is the fixed synthetic account recorded per notice. General reviewer delegation, revocation, browser behavior, concurrent chat edits, real integrations and telemetry content are outside this run. Integrated REQ-08 is `NOT_TESTED` in this phase. The evidence supports this scoped deployment and extension. Upstream defaults, production security and delivery into an employee channel remain outside the lab. [REQ-07 design](design.md) · [6.1.1 closure](../../6.1.1/closure-report.md)

## Independent review

Run `sha256sum -c SHA256SUMS` from the `evidence` directory and reproduce the checks in a fresh isolated deployment. Compare the reviewer and owner IDs with the SQLite snapshot, then verify that the ready text is the same for a wrong and a clean candidate. Read the stale and unauthorized operations beside the next SQLite observations. Confirm that credentials are redacted in the evidence. [Reproduction commands](README.md#reproduce)
