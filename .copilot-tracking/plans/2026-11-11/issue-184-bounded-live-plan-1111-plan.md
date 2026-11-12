<!-- markdownlint-disable-file -->
# Bounded live synthetic demo acceptance: plan (2026-11-11, Refs #184 #1288 #108 #188 #440)

Task `issue-184-bounded-live-plan-1111`, UUID `d7c3b05b-1d90-41d2-80b2-ee64088929e2`. **NO EXECUTION.** This is a frozen local planning candidate. Implement and Review are not started. Nothing here activates, deploys, sends, writes SQL, calls a model, spends, changes credentials, permissions or configuration, creates or deletes resources, or renews an expired window.

Research: [research](../../research/2026-11-11/issue-184-bounded-live-plan-1111-research.md). Details: [details](../../details/2026-11-11/issue-184-bounded-live-plan-1111-details.md). Critique: [critique](./issue-184-bounded-live-plan-1111-critique.md).

## Objective

Define the exact finite envelope, evidence and approval question for one future owner-approved live synthetic same-home run: simulator -> IoT Hub -> retained SQL -> employee UI -> actual Quality AI call -> visible attributed flag, so #1288's live criterion and #184, #188 and #108 live evidence can later be judged from real artifacts.

## Fixed decisions

* Owner 2026-11-11: plan only; ask before execution.
* Source is merged (#1304, #1331); no new source budget and no source change. Corrections already recorded stay as recorded.
* Mocked providers, constructed local SQL and display-only results do not count as acceptance.
* Human, resident, consent, safety and legal approvals stay separate; no simulated agent approves real authority.
* #440 stabilization gating remains. Whole-issue criteria remain open; no closing keyword.
* No new issue, feature scope, speculative audit, compliance expansion or external submission.

## Proposed envelope (PROPOSED; needs owner decision; cost cap Unknown)

| Dimension | Proposed hard maximum |
| --- | --- |
| Homes | 1 synthetic home on 1 owner-named case with a quality record |
| Sends | 13 successful messages, 52 attempts (4 per send), 1 message per 5-minute slot |
| Transport window | 60 minutes, then control stop |
| Receiver | 4 executions, each at most 360 s |
| Model | 4 calls, 50,400 tokens (input 12,000 chars and output 600 per call), 1 deployment `standard` (`gpt-4.1-nano` 2025-04-14) |
| Transport expiry | 60 minutes, independent control `expires_at`, timezone-aware, no renewal |
| Wallclock | 3 hours including cleanup and AI window; AI expiry set separately by owner |
| Token bound caveat | 12,000 characters is not proved to be at most 12,000 provider tokens; the provider may count more. The 50,400 figure is an allowance, not a proved provider bound (Unknown) |
| Post-expiry liability | The cron ticks until the job is deleted; a failed cleanup extends job cost, Unknown and unbounded in principle until deletion |
| Currency | Derived incremental list-price estimate about USD0.06 (model USD0.00576, job compute about USD0.05), USD, 2026-11-11 retail prices. NOT an enforced cap. Status: **Unknown** until the close conditions below hold |

Cost classes kept apart: incremental run cost (above); ongoing fixed infrastructure (existing B1 hub USD10 per month, possible Container Apps environment meters USD0.1 per hour each, and Event Hubs about USD21.90 per month if the adapter is activated); unpriced liability (Log Analytics ingestion, SQL tier, ACR, Azure Files, Private Link). Do not call the run affordable or capped until subscription currency and offer, aggregate headroom, an approved OD-51 price record, and an active budget alert are proved.

## Phases (all later, all need explicit owner approval; none started)

* [ ] Phase 0: Owner approval of the exact question in the details. Stop if refused or any blocker below is open.
* [ ] Phase 1: Read-only readiness confirmation (separate read authority) of the Unknown register items.
* [ ] Phase 2: Prepare, with owner-approved changes, receive path, device identity, SQL tables, jobs and assistant release.
* [ ] Phase 3: Finite run within the envelope, stopping at first failure.
* [ ] Phase 4: Cleanup and evidence closeout: stop control, delete jobs, revoke certificate, record actual usage and cost.

## Blockers

| Blocker | Clearing action |
| --- | --- |
| **Source guard blocks the AI step**: `assistants.py` (`may_carry_captured_readings`, `ai.py`) holds dispatch with "Captured sensor readings cannot be sent to a real AI model in this release", so a real `gpt-4.1-nano` call on captured readings cannot occur on the merged source. The #1288 live criterion (actual model consumption of the same IDs) is therefore NOT reachable by approval alone | Owner decision, outside this plan: change or waive the guard (a source change, contradicting "no new source budget", needing its own RPI, privacy and release review) or accept that the criterion stays unproved. Until then the model envelope is conditional and no model call is authorised |
| Proactive scanner covers open cases and all registered capabilities, not only the named case | Prove isolation (or a scoped release) before enabling proactive mode; otherwise stop |
| Control `expires_at` is the only transport stop; the cron keeps ticking, failed sends can still exit 0, and retries are bounded only by source attempts | Set transport expiry to 60 minutes independently of the 3-hour wallclock; monitor send counts; delete the schedule at expiry |
| Receiver reads from the latest position, so four short windows do not cover 60 minutes | Schedule each receiver window to start before selected sends; state which readings must be retained (at least the readings cited by the flag) |
| No authorised receive path known (Event Hubs adapter apparently inactive; built-in endpoint needs a disabled shared key) | Owner chooses the keyless adapter or another path, with price and what-if |
| Subscription currency, headroom, budget alert, OD-51 price record unknown | Named owner and finance reviewer supply them |
| Operator Registry Contributor and device certificate not granted | Owner grant; credential owner Juan Manuel Servera |
| SQL tables, control, policy and view state unknown | SQL admin applies reviewed schema after approval |
| Assistant release and `ZF_ASSIST_*` configuration absent or unknown | Programme Manager release approver (human) |
| Hub cost scope expired 2026-10-31 | New owner-dated scope in the approval; this task does not renew |
| #440 stabilization | Stays gated |

Classification: documentation-only planning, focused tier; no source, infrastructure, SQL or deployment change. A later execution is the full tier (deployment, SQL, security-sensitive).

## Follow-ups (evidence-grounded, not selected)

1. Owner answers the approval question (clears the plan; highest value, lowest effort).
2. Finance and platform supply currency, headroom, alert and OD-51 record (unblocks any cost claim).
3. Decide the receive path (largest design risk).
