<!-- markdownlint-disable-file -->
# Bounded live synthetic demo acceptance: research (2026-11-11, Refs #184 #1288 #108 #188 #440)

Task `issue-184-bounded-live-plan-1111`, run UUID `d7c3b05b-1d90-41d2-80b2-ee64088929e2`. Base `e691255ff7aae111ef32d585900cf82c3789a78c` (tree `5f642946376db0093f24d8d358197c39dc8fdc6a`), branch `docs/bounded-live-demo-plan-184-1111`. Research disposition: executed (read-only repository evidence plus unauthenticated public Azure Retail Prices API reads on 2026-11-11). No `az`, IoT, model, SQL or live application command ran. No `.env`, token or private dataset was read.

Owner selection 2026-11-11: "Prepare the exact bounded, costed plan; ask me before execution." This authorises planning only.

## Part A. Scope and acceptance literal

One finite synthetic same-home journey: simulator -> IoT Hub -> receiver -> retained SQL -> employee sensor UI -> actual Quality AI model call consuming the same reading IDs -> visible attributed `review-suggested` flag. #1288 counts only this actual live chain; display-only, deterministic-only, constructed-local and model-unavailable outcomes do not count.

| Item | Status on 2026-11-11 | Evidence |
| --- | --- | --- |
| #184 source (simulator, receiver, control) | Merged, PR #1304 (merge `23e944c1`, head `68fc3e61`), ancestor of base | `git merge-base --is-ancestor` |
| #1288 Quality sensor evidence and guarded AI path | Merged, PR #1331 (merge `1b7a1719`) | same |
| #188 live SQL and backfill continuity | Unproved live | issue #188 |
| #1288 separately admitted live walkthrough criterion | Unticked | issue #1288 |
| #108 model name, version, quota "confirmed in chosen region" | Unticked; live model evidence needs its own finite authority | issue #108 |
| #184 AC1 and AC3 | Unticked; AC2 ticked | issue #184 |
| #440 stabilization gating | Remains | issue #440 |

Owner authority on record: comment 6652226413 (2026-11-05) approved five-minute synthetic readings inside the existing USD700 cap and three job identity roles. It does not waive sizing, gates or deployment. The hub cost scope in `infra/iot-hub-live.bicepparam` (USD1 attributed, at most USD5 additional) expired 2026-10-31 and is not renewed. Nothing in this task renews it.

## Part B. Known resource bindings (nonsecret repo records, dated, historical)

Observations dated 2026-11-10 come from the prior admitted cloud-readiness research ([issue-184-cloud-readiness-1110-research.md](../../research/2026-11-10/issue-184-cloud-readiness-1110-research.md)) and the 108 notes. They are history, never current deployment proof. A resource existing does not prove the flow works.

| Binding | Recorded value | Date | Current status |
| --- | --- | --- | --- |
| Resource group, region | `ama`, uksouth | 2026-11-10 | Unknown now |
| IoT Hub | `iot-cutover-test-rzsrg`; B1 x1; local auth disabled; public network disabled; 2 partitions; 1-day retention; 0 custom routes; fallback route on; 1 private endpoint connection; consumer group `api-consumer` | 2026-11-10 17:54Z | Unknown now |
| Demo API app | `ca-cutover-test-demo-api`, revision `--0000027`, digest-pinned private-registry image, user-assigned identity, `ZF_SENSOR_REVIEW_DRAFTS` not set; image source commit unknown | 2026-11-10 | Unknown now |
| Container Apps environment | `cae-cutover-test-demo` | 2026-11-10 | Unknown now |
| Declared jobs | `job-live-simulator`, `job-live-receiver`: not found | 2026-11-10 | Authored in Bicep, never deployed |
| Model account | `aif-cutover-test-rzsrg` (AIServices S0, uksouth), matched to the app `AI_ENDPOINT` host label only | 2026-11-10 17:50Z | Match by label only |
| Model deployment | `standard`, GlobalStandard capacity 10, `gpt-4.1-nano` 2025-04-14, NoAutoUpgrade; 2026-11-07 limits 10 requests and 10,000 tokens per 60 s | 2026-11-07/10 | Unknown now |
| Model lifecycle | Legacy; inference retirement 2027-04-14 | 2026-11 | Dated metadata |
| Regional quota limit and unit | Unknown (empty usage list) | 2026-11-10 | Unknown |
| GlobalStandard serving region | Not attested | | Unknown |
| SQL sensor tables, control, policy, resident view | Absent on 2026-10-29; current Unknown | | Unknown |
| Event Hubs namespace `eh-iot-cutover-test-rzsrg` and hub `sensor-readings` | Intended keyless route; namespace existence never read; hub identity None and 0 custom routes imply the adapter is not activated | 2026-11-10 | Unknown |

Subscription ID, currency and offer, budget headroom and active alert: not in nonsecret repo records. Unknown.

## Part C. Receive-path blocker (central)

Second blocker found by the critique and verified in source: `assistants.py` holds dispatch of captured sensor readings with "Captured sensor readings cannot be sent to a real AI model in this release" (`ai.may_carry_captured_readings` allows only a carrier that declares it sends no bytes). On the merged source a real model call on live readings cannot occur, so the #1288 live-AI criterion is not reachable by spending approval alone; it needs an owner-decided source change or waiver, outside this planning scope. The history in the issues records this as provider activation staying off.

The IoT Hub built-in endpoint needs a shared service key for receive, and service SAS is disabled with no key retrieved. The designed keyless path is the custom Event Hub with hub system identity as Data Sender and `iotHubRoutingReady=true`. The 2026-11-10 read shows that adapter is apparently not active. Activating routing is a configuration change with new fixed spend and needs a named owner decision, a what-if, and reachability over private endpoints (not proved from the jobs). Until that is decided, no authorised receive path is known to exist, so the live journey cannot be executed even with a spend approval. Other prerequisites: operator Registry Contributor (not granted as of 2026-10-29), registered `SYN-` device and X.509 certificate, certificate Azure Files share, receiver grants (SELECT on `cases`, control and policy tables; SELECT, INSERT on reading, delivery and exception tables; AcrPull; Event Hubs Data Receiver), and SQL tables plus the reapplied resident view.

## Part D. Source-enforced limits usable as the hard envelope

Source identities at base (git blob IDs): `live_simulator.py` `bc29a9e1`, `live_receiver.py` `1089a716`, `live_control.py` `2a8efba3`, `iot_stream.py` `8eeaccbb`, `synthetic/live_readings.py` `780d462b`, `assistants.py` `7057beae`, `sensor_view.py` `99378174`, `ai_consumption.py` `4ff3848d`, `ai.py` `580838fe`, `infra/live-simulator-job.bicep` `b423a336`, `infra/live-receiver-job.bicep` `e9d294f9`, `infra/iot-hub-live.bicepparam` `a462e49b`.

* Simulator: one `live-sim-reading-v1` message per home per 5-minute UTC slot, under 1 KiB, `source_type=SYNTHETIC`, seed 184, `injected_fault=none`; up to 4 send attempts with backoff; `--once` job mode; control file (`enabled`, `expires_at`, `approval_reference`, `owner`, `homes`) gates sends; no send after expiry or stop; cohort at most 100 and window at most 14 days (the plan uses 1 home and far less); 0.25 vCPU, 0.5 GiB; replica timeout 240 s; retry 0; cron `*/5 * * * *` keeps ticking after expiry so the job must be deleted; exit codes 0, 2 refused, 3 home list unavailable, 4 failed.
* Receiver: Manual job; window default 240 s, replica timeout window + 120 s; retry 0; `--events` default 1000; refuses a stopped or expired control before opening SQL; 0.25 vCPU, 0.5 GiB.
* Quality AI (`quality-evidence`, roles Quality Inspector and Programme Manager): defaults input 12,000 chars, output 600 tokens, timeout 20 s, 2 attempts (ceiling 3), 2 active calls, scan interval 60 s; proactive activation needs `ZF_ASSIST_PROACTIVE=1`, authority, call allowance, token allowance (at least 12,600), timezone-aware expiry and a matching human-approved release (`ZF_ASSIST_RELEASE_APPROVERS`, Programme Manager). Price-unknown or missing authority holds dispatch. One proposal per six-hour reading bucket and one case with a quality record. Citations `sensor:{sensor_id}:{reading_id}`. Output is `review-suggested`, unapproved. Sensor UI visible to Quality Inspector and Programme Manager only.

## Part E. Dated pricing (public Azure Retail Prices API, retrieved 2026-11-11, USD, uksouth, list price)

List price is not the subscription offer, a quote or an invoice. Currency and unit assumption: USD per the API; subscription billing currency is Unknown.

| Meter | Price | Applies to this plan | Class |
| --- | --- | --- | --- |
| IoT Hub B1 | USD10.00 per unit per month (S1 USD25) | Existing hub, already running | Ongoing fixed, not incremental |
| gpt-4.1-nano Global Standard input | USD0.0001 per 1K tokens (USD0.10 per 1M) | Model calls | Incremental |
| gpt-4.1-nano Global Standard output | USD0.0004 per 1K tokens (USD0.40 per 1M) | Model calls | Incremental |
| gpt-4.1-nano cached input / batch | USD0.000025 / batch USD0.00005 in, USD0.0002 out per 1K | Not used | Reference |
| Container Apps vCPU active / memory active / vCPU idle | USD0.000034 per s / USD0.000004 per GiB-s / USD0.000004 per s | Job executions | Incremental, small |
| Container Apps environment meters (effective 2026-11-01): planned maintenance, private endpoint, management | USD0.1 per hour each | Whether they apply to the existing consumption environment is Unknown | Possible ongoing fixed |
| Event Hubs Standard: throughput unit / ingress | USD0.03 per hour (about USD21.90 for 730 h) / USD0.028 per 1M events | Only if the keyless adapter is activated | New fixed spend |
| Log Analytics analytics logs ingestion / analysis | USD2.88 / USD2.3 per GB | Whether any ingestion applies is Unknown | Unpriced liability |
| Private Link endpoint | Query returned no rows; infra README unverified allowance USD0.01 per endpoint-hour | Unknown | Unknown |
| Azure SQL tier, ACR build or push, Azure Files share | Not retrieved | Unknown | Unknown |

Source meter IDs for the model rows: input `5a96380c-2dbe-5b68-b0da-e71db0e00147`, output `0af08775-3bab-5db5-ac98-5ddb9fbd3c30`, cached `6d8d7eb1-7495-546e-8763-3721f356b797`; effective 2025-04-01.

Contradictions flagged, not resolved silently:

* `infra/README.md` recalled IoT Hub B1 near USD25; the retail API and the owner-checked figure say USD10. The API retrieval is used and the README is left as recorded history.
* `infra/README.md` recalled Container Apps rates USD0.000024 per vCPU-s and USD0.000003 per GiB-s; the API today shows USD0.000034 and USD0.000004. Both are shown; the API value is used for the arithmetic.
* The earlier [price source record](../../../docs/reference/resources/azure-ai-price-source-2026-10-31.json) kept all rates null (Unavailable). This run's rates are a new dated retrieval, not an approved OD-51 price record and not an edit of the earlier one. The assistant gate (`ai_consumption.price()`) requires an official `prices.azure.com` or `azure.microsoft.com` URL and a rate per million tokens; whether a human-approved record exists in SQL is Unknown.

## Part F. Candidate envelope arithmetic (PROPOSED, not approved, not an enforced currency cap)

* Transport: 1 home, 60 minutes: at most 13 five-minute slots, so at most 13 successful sends and 52 send attempts. Negligible against hub limits; hub quota headroom Unknown.
* Receiver: at most 4 executions, each at most 360 s (about 1,440 s total) at 0.25 vCPU and 0.5 GiB.
* Model: at most 4 calls, token allowance 50,400 (4 x 12,600). Worst case per call at the conservative char-as-token bound: 12,000 x USD0.0001/1K = USD0.0012 plus 600 x USD0.0004/1K = USD0.00024, total USD0.00144. Four calls: USD0.00576, at list price.
* Compute worst case: receiver 1,440 s x (0.25 x 0.000034 + 0.5 x 0.000004) = about USD0.0155; simulator 13 runs x 240 s = 3,120 s at the same rate, about USD0.0336. Sum about USD0.05 before any free grant, at list price.
* These incremental figures are small, but they are not a cap: Azure enforces counts, tokens and timeouts here, not currency; budget alerts are notifications, not stops. Cost status is Unknown until the close conditions in the plan are met.

## Part G. Unknown register (exact owner or platform prerequisite)

| Unknown | Prerequisite and owner |
| --- | --- |
| Subscription ID, billing currency, offer | Owner or platform admin states it in the approval |
| Aggregate USD700 headroom, active budget alert (#146) | Finance and platform owner |
| OD-51 approved price record and finance approval | Finance and Grants Lead, Digital service owner, Data and Performance Lead, Executive Director of Assets (human) |
| Hub current usage, daily messages, regional quota and unit for `gpt-4.1-nano` | Platform owner read, after separate read authority |
| Event Hubs adapter, route state, private reachability | Owner decision plus approved what-if |
| Operator Registry Contributor, device registration, certificate share | Owner grant; credential owner Juan Manuel Servera |
| SQL tier cost, table, control, policy and view state; case and home | Owner names case and home; SQL admin applies reviewed schema |
| Image source commit and digest provenance | Platform owner build attestation |
| Assistant release, approvers, `ZF_ASSIST_*` app configuration | Programme Manager release approver, human |
| Serving region attestation and provider data-handling approval | Platform owner and data protection reviewer |
| Resident, consent, legal and safety approvals | Named humans; no simulated company agent can approve real authority. Synthetic data only, so no resident data is intended. |

Prior evidence is history, not current proof. Original adverse evidence (E12/E13 unused, harness confound, absent tables on 2026-10-29, expired scope) is preserved and not rewritten.

## Planning Readiness

Ready for a plan with cost status Unknown. Not ready for execution.
