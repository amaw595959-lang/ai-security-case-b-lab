# P-006 Phase C — REQ-08 results

**PASS for the assessed event, audit, access and expiry paths in the controlled local Open WebUI deployment.** The deliberately content-bearing comparison captured the synthetic ticket in a native message preview and the HTTP request audit. The controlled deployment delivered all three expected event records and the HTTP decision through the metadata-only journals, with no notice text in those records. The authorized private chat and local model path still worked. [Execution](evidence/execution.txt) · [Comparison ledger](evidence/baseline.jsonl) · [Controlled ledger](evidence/controlled.jsonl)

## Authorized runtime

Both isolated modes used Open WebUI `0.13.4`, upstream commit `0666e59d26a4d056e0bacee41742486badd71cf8`, image manifest `sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1`, and the same supported Linux amd64 environment. Both made a native chat call to the pinned SmolLM2 artifact through llama.cpp `b12627-225a5345b` at the loopback provider. The run sent the frozen synthetic note fields with the note block first, so `LAB-INT-042` fell inside the native 300-character preview. Each app used fresh synthetic accounts, private temporary state and no outward network interface. The ledgers preserve each run ID and its UTC timestamps. [Scope and data flow](design.md) · [Baseline topology](evidence/baseline-topology.txt) · [Controlled topology](evidence/controlled-topology.txt)

## Observed before and after

| Path | Deliberate comparison | Controlled retest |
| --- | --- | --- |
| T04-A · Initial events | Native publication generated a user event with the ticket-bearing `content_preview` and a second `message.created` for the assistant placeholder. | Both `message.created` deliveries arrived with exactly the seven approved metadata fields. Neither carried the preview or placeholder-specific data. |
| T04-B · Completion event | The `chat.finished` record carried the returned assistant text exactly. The model omitted the ticket in this run. | The completion record arrived with the expected action and approved metadata. Its journal data excludes the assistant prose and native IDs. |
| T04-B and C · HTTP audit | Native `REQUEST_RESPONSE` captured the synthetic request and assistant body. A separate same-route record had no bodies, so the presence of a matching route alone would have been insufficient evidence. | The body logger was disabled. The local HTTP audit journal recorded the correlated allowed outcome and contained only the exact metadata record. The application log replay found no ticket, `Maple Calendar` or `content_preview`. |
| T04-D · Private rows and readers | The analyst's native read succeeded and the unrelated standard account received `401`. Separate SQLite reads showed one chat and two message rows. | The same before-expiry results held. The 12-second lab expiry emitted the allowed deletion receipt. Separate SQLite reads found zero chat and message rows afterward, and the previous owner received `401` for the expired chat. |
| Covered side-effect stores | Share, tool, tool-history, automation, automation-run and notification counts were zero before and after. | The same six store counts stayed zero. The environment used only the approved local journals and no published ports. |

The controlled observer validated metadata **values and names**, including the exact run ID and approved actor/resource aliases. The three event deliveries and one HTTP audit record are the positive controls for deciding what content was absent. SQLite separately confirmed both the native private content and the later deletion. [Archived ledger replay](evidence/verify.txt) · [Evidence digests](evidence/SHA256SUMS)

## Scope limits and retest record

The comparison's content would **fail** the REQ-08 allowlist. Body capture was enabled deliberately for this local synthetic run. The comparison command's successful exit means it found the intended content-bearing records. In the controlled run, the app projected fields before dispatch to the local operator journal, and the direct inbox consumer was suppressed. Private chat and model content remained on their eligible path. Operator journals were verified as mode `0600`, existed in temporary state and were removed with the containers. [Implementation](overlay/capture.py) · [Independent checks](overlay/check_c.py)

Early attempts exposed an inaccurate assumption about the number of native message events and two issues in the baseline audit check. The native whitelist expects `chat/completions`, and an endpoint can have both a usage record and a body record. The unsuccessful baseline assertions are `INCONCLUSIVE` for their omitted checks. The raw receipts and errors are preserved, including the successful controlled attempts. The completed ordered pair verifies the body-bearing record explicitly. [Diagnostic attempts](evidence/diagnostics/) · [Final comparison and retest](evidence/execution.txt)

Long-lived collectors, production log rotation, backup/restore, other retention paths and physical SQLite or filesystem remnants are `NOT_TESTED`. The fixture uses an in-process timer, and deletion is verified as the absence of logical rows and native access. Timer recovery after a crash and independently hosted sinks remain outside scope. The local journal before/after experiment supplies no coverage for all upstream events. [Design and exclusions](design.md)

## Independently verify

From this directory, verify the checksums and replay the two ledgers. The application console capture is compressed without altering its bytes. To reproduce the actual effects, use fresh containers and records as described in the launcher guide. [Console archive](evidence/controlled-app.log.gz) · [Reproduction](README.md#reproduce)

```bash
(cd evidence && sha256sum -c SHA256SUMS)
python3.12 -B verify.py
```

- Find the raw marker in the comparison's user-preview and request-body records. Distinguish the body record from the separate usage record.
- Compare the three controlled event deliveries with the baseline by type and count. Verify every approved field and the allowed HTTP outcome before reasoning about excluded content.
- Compare the owner and unrelated-user HTTP receipts with the independent SQLite counts. Explain the difference between deleting logical rows and proving media erasure or backup expiry.
