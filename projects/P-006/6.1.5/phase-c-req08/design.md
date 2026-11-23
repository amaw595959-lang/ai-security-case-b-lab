# P-006 Phase C — REQ-08 deployment design

Phase C uses two fresh isolated instances of the exact Phase B Open WebUI image and local model, with the same synthetic accounts and native model grant. The branch builds on Phase B to reuse its launcher configuration and verified-session test helpers. This authorizes only the fictional T04 notice data, the loopback model route, the private SQLite stores and controlled operator evidence. Keep authorizations and real credentials out of evidence. [Phase B deployment](../../6.1.4/phase-b-req07/design.md) · [REQ-08](../../6.1.1/security-requirements.md#p006-611-req-08--keep-stored-data-and-telemetry-within-policy)

| Boundary | Approved behavior for this deployment |
| --- | --- |
| Native private chat, messages and model | The analyst may read the private saved chat. The unrelated standard user may not. The sole local model may receive the synthetic notes. Native chat and message rows have a lab expiry of 12 seconds after completion in the controlled run. |
| Initial message and completion events | Project the trusted scenario, type and outcome into an explicit metadata record before native operational dispatch. Only the local operator journal receives the record. Exclude previews, completion text, titles, native account/chat IDs and every other payload field. |
| Native audit and diagnostic logs | Use body capture only in the deliberately configured, wholly synthetic comparison. For the controlled run, disable native body capture and emit an independent metadata-only HTTP record for the assessed route. The runtime uses warning-level diagnostics. |
| Functions, webhooks, public sharing, automation and inbox | Outside scope. The harness narrows the operational fan-out to its approved local journal. The control withholds the content-bearing direct completion path from inbox consumption. No recipients or remote destinations are configured. |
| Copies and evidence | App state and local journals live on private tmpfs. Journals are operator-only and removed with their containers. Sanitized assessment receipts remain in the review branch. Database snapshots, rotated production logs, backups, collectors and physical media erasure require separate evidence when those paths exist. |

Open WebUI emits the first message preview from its normal saved-chat create path. The native completion handler builds the completion event, calls the inbox consumer directly, and publishes through its configured event sinks. The native audit middleware can record HTTP bodies. The integration preserves the upstream source files and installs a lab policy at the common event builder and dispatch points in the native process. Keep the user-authorized content and model path separate from operational records. [Initial message producer](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/main.py#L1479-L1505) · [Completion and direct inbox consumer](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/utils/middleware.py#L248-L287) · [Event dispatch](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/events.py#L1244-L1286) · [Audit body handling](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/utils/audit.py#L307-L350)

~~~mermaid
flowchart LR
  Analyst["Verified synthetic analyst"] -->|"synthetic notes"| App["Pinned native chat"]
  App <-->|"private content"| Private["Private SQLite rows"]
  App <-->|"loopback prompt and completion"| Model["SmolLM2"]
  App -->|"message.created / chat.finished"| Policy["Projection before operational dispatch"]
  Policy -->|"allowed metadata"| EventSink["Local event journal"]
  App -->|"HTTP decision metadata"| Audit["Local audit journal"]
  Policy -->|"explicit owned chat + deadline"| Retention["Lab expiry worker"]
  Retention -->|"native owner-scoped deletion"| Private
~~~

Accept a negative-content result only when the corresponding positive metadata arrived. In the comparison run, prove the synthetic marker appears in captured request/completion sources. In the controlled run, prove the same synthetic data appears in the approved private chat and model reply. Observe the two native event types and the HTTP outcome in their respective metadata-only journals. Compare read-only database observations before and after expiry and confirm the unrelated account's denial. Inspect the runtime namespace, effective config, actual files and destination inventory. Any missing source, sink, request, expiry or access evidence leaves its requirement inconclusive. Case T04 covers the explicitly observed paths. [T04 design](../../6.1.1/case-b-test-design.md#p006-611-t04--proposed-req-08-storage-event-and-log-handling)
