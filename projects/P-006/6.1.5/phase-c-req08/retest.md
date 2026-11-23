# Phase C remediation and retest

**REQ-08 · PASS for the assessed isolated paths.** The repaired lab delivered all four expected notice records to the approved metadata sink, preserved unrelated native dispatch and security auditing, and confirmed logical expiry through a separate SQLite reader. Run `dab48940-85cf-4222-a418-ffccaccd5690` finished with exit code `0`. [Execution](evidence/retest/runtime-execution.txt) · [Independent observations](evidence/retest/runtime-observations.jsonl)

## Finding and baseline

The historical overlay intercepted all native operational delivery. A probe of the pinned dispatcher recorded `chat.created`, `user.role_updated` and `message.created` at the downstream observer, with one call to the session-disconnection boundary. The same probe with the original controlled overlay reached that observer zero times, made zero calls to that boundary, and still wrote one scoped record. The original inbox function was also replaced. The test observes the socket sink call with a spy. It establishes a loss of event-driven behavior in the overlay. Native application handlers can have additional protections. [Defect analysis](defect-analysis.md) · [Baseline comparison](evidence/retest/baseline-dispatch.txt)

Before changing the implementation, the archived manifest matched all 22 entries and `verify.py` replayed the receipts. A fresh run of the old launcher returned `0` in both modes. Run `9401d574-8c3a-4c44-9c0e-19688cac420d` reproduced the deliberate preview and audit-body comparison. Run `0a0b0993-376f-4f05-8f5e-121de1dce0a6` reproduced the original scoped journal and logical deletion. Those old checks could pass while the unrelated observer remained disconnected. Two initial baseline probe attempts exited `1` during startup with an empty application session key. The retry generated an ephemeral key in memory and reached both comparison modes. These failed attempts supply no dispatch verdict. [Legacy commands](evidence/retest/legacy-rerun.txt) · [Legacy observations](evidence/retest/legacy-observations.json) · [Startup attempts](evidence/retest/baseline-attempts.txt) · [Historical manifest](evidence/SHA256SUMS)

## Remediation and scope

A small patch checks a trusted request context at the pinned publisher and before its direct completion-to-inbox call. The fixture route checks a verified account ID and invokes the native chat handler. It projects the approved metadata before any native event fan-out. A rejected delivery records a fixed reason. The separate ordinary application and security routes retain native behavior. The retained metadata audit covers normal authentication and administration, and the scoped route records its own body-free HTTP decision. [Policy and boundaries](event-security-policy.md) · [Source patch](overlay/notice-events.patch) · [Policy implementation](overlay/capture.py)

The target was the isolated Linux amd64 Open WebUI `0.13.4` image `sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1` for upstream commit `0666e59d26a4d056e0bacee41742486badd71cf8`. The original event and middleware module hashes matched the image before patching. The real SmolLM2 artifact used the approved loopback llama.cpp route. Both app and model had no external interface or published port. The experiment used temporary SQLite, local journals and fictional accounts and content. [Source and image checks](evidence/retest/runtime-execution.txt) · [Runtime namespace and hashes](evidence/retest/topology.txt)

| Check | Observed result |
| --- | --- |
| Offline policy, malformed input and failure handling | `12/12` standard-library tests passed. They cover binding, metadata, ordering, duplicate delivery, rejection, failed sinks and body-free HTTP audit. [Test transcript](evidence/retest/component-tests.txt) |
| Pinned dispatch and inbox boundaries | The fixed publisher delivered the unrelated events despite an injected native sink failure. The original role callback was awaited once. The direct inbox spy was called for the ordinary completion and bypassed for the admitted notice. The scoped stream delivered both failure types with no raw error and recorded malformed, duplicate, unsupported and failed-consumer decisions. The observed failure text contained zero instances of the restricted sentinel. [Pinned probe](evidence/retest/fixed-dispatch.txt) |
| Real unrelated path | Four ordered native chat records and one role-update event reached a separate observer. Read-only SQLite confirmed the role changed from standard to pending. The same analyst's ordinary chat was retained and received native delivery. [Runtime ledger](evidence/retest/runtime-observations.jsonl) |
| T04-A and T04-B · Notice delivery | Four ordered metadata records arrived for one attempt, including chat creation, both message events and completion. Five positive native observations were already present. The scoped request added zero native observer records. The approved private chat still contained the exact synthetic input and the saved assistant reply matched the actual routed model response. [Runtime ledger](evidence/retest/runtime-observations.jsonl) |
| T04-B and T04-C · Audit and logging | The notice journal recorded `401`, `403`, `400` and `200`. Native authentication and administrative audit entries arrived with zero body-bearing records. The ordinary application console had zero occurrences of the three assessed content indicators. [Runtime ledger](evidence/retest/runtime-observations.jsonl) · [Console observation](evidence/retest/console-check.txt) |
| T04-D · Private reads and expiry | The owner read the private chat. The unrelated account was denied. An independent SQL connection saw one chat and two messages before expiry and zero afterward. The former owner then received `401`. The after-state was observed 12.165 seconds after the recorded final pre-expiry check. The unrelated chat remained, and the six observed share, tool, automation and notification stores stayed unchanged. [Expiry and effects receipt](evidence/retest/runtime-observations.jsonl) |

The first app retest, `f8d9b813-d810-48ab-8b75-c9140b2e66a2`, also exited `0`. The final repeat includes the pinned dispatch probe in the launcher. The synthetic response is used to observe downstream handling. This remediation retest makes no new B-04 or B-05 model-behavior verdict. [First app retest](evidence/retest/initial-runtime.txt)

## Commands and reviewer acceptance

The execution records include the actual launcher arguments, run IDs and exit codes. The before-change probe used the same image with `--network none` and then loaded the historical overlay for the second mode. The offline checks can run without Docker. [Reproduction](README.md#reproduce-the-isolated-retest)

~~~bash
phase=projects/P-006/6.1.5/phase-c-req08
python3.12 -B -m unittest discover -s "$phase/tests" -v
bash -n "$phase/run_lab.sh"
(cd "$phase/evidence" && sha256sum --strict -c SHA256SUMS)
python3.12 -B "$phase/verify.py"
(cd "$phase/evidence/retest" && sha256sum --strict -c SHA256SUMS)
~~~

The reviewer can compare the scope predicate with the source patch and replay the archived manifests. In the runtime ledger, match the positive notice event attempt to its HTTP and expiry decisions, then check that the ordinary actor and role transition reached the native sink. Inspect the security probe in a fresh isolated run to distinguish its simulated consumer failure from the real model and SQLite observations. Accept only the paths with those positive observations and the stated limits. The lab maintainer is the proposed owner of the integration. Human acceptance remains pending. [Retest manifest](evidence/retest/SHA256SUMS) · [Acceptance criteria](event-security-policy.md#acceptance)

## Remaining verification

The fix and verdict apply to the isolated admitted operation. Broader event and audit coverage, later edits to governed conversations, streaming, durable delivery or deduplication, crash recovery, provider error diagnostics outside the guarded publisher, external collectors, backup restore, rotation and physical data remnants need separate evidence. The probe observes native socket and inbox calls with spies. The application run observes native sink arrival and database effects in the exercised paths. Production adoption and security assurance remain unverified.
