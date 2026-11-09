---
title: Quality sensor demo 1288 E2 research
ms.date: 2026-11-09
---

Written 2026-11-09T10:19Z, before any E2 source edit. Refs #1288, #107. No closing claim. Task `issue-1288-e2`, parent `issue-1288-e1` (frozen at `21763da26866929549c21ce48ba8a0aa9ebfa5b1`). E2 is the second of the five ADDITIONAL corrections after C1-C8 (E1 was the first); three remain after E2.

## Inputs read

* Independent functional review of the E1 head (`independent-1288-current/functional-findings.json`, read-only coordinator file, not copied): verdict request_changes, F1 High, F2 to F4 Medium. Original C7 and E1 reports are preserved unchanged.
* Source in this worktree: `core/ai.py`, `core/ai_consumption.py`, `core/assistants.py` (`DispatchGate`, `execute`, `_adopt`, `_due`, `forecast`, `scan`, `review_flag`), `api/server.py` composition, `api/web/assistants.js`, `api/checks/quality_sensors_browser_check.py`, E1/C7 tests.
* Base: `origin/main` fetched at `1f28d09130c8e058a0436d468e6a22f3c4c24f47`; merged locally as `c772364fc806484ac2c17ad80815a8b7f2bfb5b4` with no conflicts. Main changed only `paired_equity.py`, docs and workflow files since the branch base, none of the paths E2 edits. PR1301 and PR1222 are merged. The unmerged #1292 branch is not imported; see schema overlap below.

## Reproduction of each finding in current source

| Finding | Evidence in current source | Disposition |
| --- | --- | --- |
| F1 High: suspension between the last userland check and `sock.send` | `ai.py` `bounded_send` computes `left`, sets `settimeout(limit)` and calls `sock.send`. A suspension between the check and the send lets the database gate row expire and a withdrawal commit; on resume the send proceeds with the cached positive timeout. No userland check can close this: a check is a read, the send is a later separate kernel call. `DispatchGate`'s own docstring admits it ("Not covered: a process or VM suspended ..."). | Confirmed by reasoning and by the maintainers' own docstring. A faithful deterministic repro needs a send point to suspend at, which is the thing to remove. |
| F2 Medium: adoption repeats the same 100-row prefix | `_due` deletes an `incomplete-history` slot on every observing scan, `_adopt` re-reads offset 0 with ORDER BY `dispatched DESC, revision DESC, id`. Nothing advances. | Confirmed in code. Regression with a qualifying task behind 120 newer manual tasks at the unchanged cap. |
| F3 Medium: forecast persists adoption | `forecast` calls `_due(..., observe=False)`; `_due` calls `_adopt` unconditionally when no slot exists, which INSERTs or UPDATEs `assistant_schedule` (via `_occupy` or the empty/incomplete insert) and adds to `self.incomplete`. | Confirmed in code. Regression compares all `assistant_schedule` rows and in-memory held state before and after. |
| F4 Medium: rotation reported as "no longer retained" | `capture_source` selects the newest 12 in a 30-day window plus 4 context rows each side by `ORDER BY observed_at`. A cited row outside those arrays is `missing_ids` while the `sensor_reading` row still exists. `assistants.js` line 25 says "no longer retained". | Confirmed in code. Regression adds arrivals so citations rotate out while rows stay stored. |

## F1 option analysis (no atomic physical safety is claimed)

* Option A, a further userland check or a larger margin: rejected by the brief and by the physics. A margin only shortens the unsafe window.
* Option B, a protocol where withdrawal cannot commit until every previously authorised sender has irrevocably stopped: the withdrawal writer would have to learn that a suspended or hung process (possibly another host) has stopped. Only a lease the sender cannot outlive, such as a kernel/hardware-enforced deadline, or an external proxy that enforces the lease, could do that. The repository has no such mechanism, and a blocking withdrawal would deny the resident's choice for as long as a peer is stalled. Not provable here.
* Option C, selected: an ENFORCED fail-closed boundary at the only transport. The real `Ai` client refuses, before the financial reservation, token acquisition and any socket, a request flagged as carrying captured sensor readings. The assistant dispatch also holds the task before claiming a provider slot, with the explicit manual-route text. Because no real send exists for these readings, there is no sender that can transmit after a withdrawal. Resident choice is not denied: withdrawal commits immediately, and the manual route is the stated output.

What stays allowed: a carrier that is not the real `Ai` client and that declares `sends_no_bytes` (the in-process mock/test doubles used by the engineering suites and the browser check). That is a composition declaration about the sink, not provenance of the data. No provenance is inferred from `SYN` identifiers, sensor labels or a caller flag on the data. A hostile in-process double could lie about `sends_no_bytes`; that is a composition-trust limit, disclosed, not claimed as enforcement against such code.

Impact to disclose: with this boundary the real Quality AI cannot be given captured IoT readings, so a separately authorised real-AI demo gets no sensor-grounded flag; the other assistants and Quality evidence without captured readings are unaffected. Live acceptance criteria that require real-AI use of the IoT values stay unproven. A different strategy (for example a lease-enforcing egress proxy) would be a runtime/provenance/consent decision and needs a scoped owner decision; it is not made here.

Removed as now unreachable and misleading: `_gated_opener`, `bounded_send`, `CHUNK`, `Deadline`, `DISPATCH_GATE`, `dispatch_gate`, `honours_dispatch_gate`, `_provider_honours_gate`. The database gate row, the triggers that reject direct control writes while a gate is live (original E1 F2), and the per-attempt gate for non-transmitting carriers remain.

## F2 and F3 design

A single, side-effect-free adoption computation returns a slot tuple or an incomplete result. Persisting happens only in an observing scan. For an incomplete search the row keeps a durable keyset cursor, `(dispatched, id)` of the last examined task, stored in the existing `paused_at` (double) and `task_id` columns of the incomplete schedule row (unused for that state), so no schema change. The next scan resumes strictly after the cursor: each scan still reads at most `ADOPT_ROWS * ADOPT_PAGES` (5 x 20 = 100, unchanged); progress is guaranteed because history is finite; a restart resumes from the stored row. Ordering is `dispatched DESC, id` (revision removed from the order because it is mutable and would break a stable cursor; `dispatched` is written at claim). `forecast` and other non-observing callers never write or mutate `self.incomplete`.

## F4 design

Smallest truthful fix: wording "not present in the current bounded capture" and a `basis` field on `cited_comparison`; no claim of deletion, no new queries. Bounded primary-key lookups would need a new consent-authorised read path; not needed for truthfulness. The regression keeps old rows stored while their citations rotate out, next to the actual deletion and unavailable cases.

## Schema overlap with unmerged #1292

E2 adds no table or column. It reuses `assistant_schedule` columns introduced in E1 (`seen`, `paused_at`) and repurposes two for the incomplete-history cursor. #1292 (persistence) may also alter assistant persistence; no #1292 code is imported or required, so no stop condition applies. Overlap is the `assistant_schedule` table shape; the coordinator must compare it when #1292 merges.

## Test and validation plan summary

Focused: new `test_quality_sensors_e2.py` plus changed E1/C7 tests; API modules `test_quality_sensors test_assistants test_technical_quality_screens test_sensor_consistency test_sensor_handover_demo test_sensor_sql_check test_quality_sensors_e1 test_quality_sensors_c7 test_quality_sensors_e2`; core `test_sensor_consumer test_sensor_analysis_store test_sensor_analysis_mssql`; affected SQL groups on an owned disposable SQL Server under the nonqueued shared lock; browser/axe check; same-tool ruff and mypy baseline versus head normalized diagnostics. No full runner, no model or Azure call, no private data.

## Planning readiness

Ready. Research disposition: executed.
