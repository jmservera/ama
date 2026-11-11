<!-- markdownlint-disable-file -->
# Bounded live demo plan revision 2: research (2026-11-11, Refs #184 #1288 #108 #440)

Task `issue-184-bounded-live-plan-rev2-1111`. Actual native CLI session: `053b0ad3-0c8d-46d8-b30c-e3b1f3fcdb3f` (resumed). Original candidate: HEAD `76e21e9a78bd7d90996361237b2e63e8717bf29f`, tree `a798c6493c873fbd978f521c5ed8f2fe6602634f`, base `e691255ff7aae111ef32d585900cf82c3789a78c`; worktree clean at start (checked). Root admitted ONE documentation-only revision under the same planning scope. No source correction, guard bypass, cloud, model, SQL, deployment, spend, credential or resource action is granted, and none ran. Research disposition: executed, read-only (repository source reads plus unauthenticated public Retail Prices reads).

Inputs: the complete independent adverse report, preserved unaltered at [the review copy](../../reviews/2026-11-11/issue-184-bounded-live-plan-1111-independent-76e21-report.json) (2 High, 4 Medium). The five original planning artifacts stay unchanged: [research](./issue-184-bounded-live-plan-1111-research.md), [plan](../../plans/2026-11-11/issue-184-bounded-live-plan-1111-plan.md), [details](../../details/2026-11-11/issue-184-bounded-live-plan-1111-details.md), [critique](../../plans/2026-11-11/issue-184-bounded-live-plan-1111-critique.md), [state](../../rpi-sessions/2026-11-11/issue-184-bounded-live-plan-1111-state.json).

## Source verification of each finding (base `e691255f`, read-only)

| Finding | Source evidence | Verdict |
| --- | --- | --- |
| 1 receiver start | `iot_stream.py` `HubReceiver.run` passes `starting_position="-1"` with `starting_position_inclusive=False` to `EventHubConsumerClient.receive`: the beginning of the retained stream, not latest. Hub retention recorded as 1 day (2026-11-10), so a window can replay retained events. Success returns only when `len(receipts) >= max_events`; otherwise the deadline gives `StreamError("RUN_DEADLINE")`, which `live_receiver.main` maps to exit 2. Default `--events` is 1000. A stop or expiry seen by the watcher raises `RUN_STOPPED`, also exit 2 | Confirmed; original claim "reads from the latest position" was wrong |
| 2 expiry | `live_simulator.run` asks `gate` before every slot only; `send_slot` has an attempt loop (`limits.attempts`) with backoff sleeps and no control reload. `--once` bounds one process. No durable global counter exists | Confirmed; expiry prevents new slot admission, not an in-flight retry loop |
| 3 reservation | `ai.py` `_request` sets `bound = len(body)` (serialized provider JSON bytes, ASCII, with overhead and escapes) and reserves `bound` plus `max_tokens`; `ai_consumption` admission sums prior actual tokens or outstanding `input_bound + output_bound` and holds with `call-budget-limit`, `token-budget-limit` or `money-budget-limit`. Each physical attempt calls `reserve` | Confirmed; 12,000 characters is not the bound |
| 4 timeout | `live-receiver-job.bicep`: `replicaTimeout: windowSeconds + 120` | Confirmed; 360 s window means 480 s replica |
| 5 provenance | Original critique file states one invocation and author-applied dispositions | Confirmed |
| 6 approval | Original details question bundled spend, liabilities and execution | Confirmed |

Also read, unchanged: the captured-readings guards (`assistants.py` dispatch hold, `ai.py` `_request` `captured-readings-transmission-unavailable` unless a simulation seal exists) and the proactive scanner over open cases. Both stay protected prerequisites. A seal or simulation route is not proposed as a workaround.

## New public price retrieval (2026-11-11T17:03:14Z)

Compact exact records, queries, UTC timestamp, SKU, meter, region, currency, unit, type and effective date are in [the price records file](./issue-184-bounded-live-plan-rev2-1111-price-records.json). It is a NEW retrieval; the original retrieval's temporary payloads were removed and are not reconstructed. All HTTP 200. Rates reproduced: IoT Hub B1 USD10 per month; `gpt 4.1 nano` global input USD0.0001 and output USD0.0004 per 1K tokens; Container Apps standard vCPU active USD0.000034 per second and memory USD0.000004 per GiB-second; Container Apps environment planned maintenance, private endpoint and management meters USD0.1 per hour each effective 2026-11-01; Event Hubs Standard throughput unit USD0.03 per hour and ingress USD0.028 per 1M. The model product naming under `serviceName` differed from the first guess (Q2 and Q3 empty), so the model rows came from a meter-name query. Not retrieved, so Unknown: Log Analytics, Private Link, SQL tier, ACR, Azure Files, free grants, offer and billing currency.

## Corrected arithmetic (illustrative, USD list price, no free grant)

* Per replica-second at 0.25 vCPU and 0.5 GiB: 0.25 x 0.000034 + 0.5 x 0.000004 = USD0.0000105.
* Receiver upper bound: window 360 s means replica timeout 480 s; 4 replicas = 1,920 s = USD0.02016.
* Simulator upper bound: replica timeout 240 s x 13 triggers = 3,120 s = USD0.03276 (the original figure USD0.0336 was a small arithmetic error).
* Model: the actual reservation is serialized-byte based; 4 x (12,000 + 600) is not a proof. USD0.00576 is an illustration only.
* Illustrative total about USD0.059. It is not a worst case, not a cap and not an actual cost.

Cost classes: incremental illustration (above); existing fixed (B1 hub USD10 per month, running regardless); possible newly ongoing (Event Hubs adapter about USD21.90 for 730 hours of throughput unit, plus ingress; Container Apps environment meters whose applicability is Unknown), which needs an accountable owner, duration and teardown before any request; unpriced liability (Log Analytics, Private Link, SQL, ACR, Azure Files, post-expiry ticks and failed cleanup). Unknown liability is a hold.

## Provenance facts (finding 5)

* `d7c3b05b-1d90-41d2-80b2-ee64088929e2` was generated by the author before writing the original artifacts; it is an artifact and task identifier, not a native session UUID. The actual native CLI session is `053b0ad3-0c8d-46d8-b30c-e3b1f3fcdb3f`.
* Per the supplied process evidence, the original wrapper `.log.exit` file is MISSING and the shared launcher may have been edited while other instances were running, so the capture may be confounded. No exit status is inferred (not 0) and no exit file is recreated.
* The original critique was one recorded pre-revision `rubber-duck` invocation with seven author-applied dispositions. It was not an independent reconfirmation of `76e21e9a`. The adverse report is a separate exact-head assessment, not retroactive proof of the original's independence.

Planning Readiness: Ready for a revised plan. Not ready for execution.
