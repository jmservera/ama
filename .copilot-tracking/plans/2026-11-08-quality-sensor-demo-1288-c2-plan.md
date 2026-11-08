# Plan: #1288 correction 2 (C2)

Written 2026-11-08T20:21Z after the C2 research and before product edits. Refs #1288, #107. No closing claim.

## Phases

* [ ] P1 Exact capture identity (finding 1): `assistants.signature` = digest of the full snapshot; add `scheduling_signature` (coarse) for the `signature` column, `scan` and `forecast`; task id from the exact value.
* [ ] P2 Fail-closed withdrawal (finding 2): whole-output and event-field stubs.
* [ ] P3 Dispatch-bound trigger (finding 3): `dispatch` at claim, used by `review_flag`.
* [ ] P4 Complete per-home consent (finding 4): control-home index table, lookup, fail-closed rules.
* [ ] P5 As-of and horizons (finding 5): capture/view bounds, future flag, UI text.
* [ ] P6 Account summary label (axe) and web guideline review of every changed web file.
* [ ] P7 Light tests (SQLite) and static checks; heavy SQL/browser PENDING.
* [ ] P8 Changes artifact, review (one), state, commit.

## Critique (one, executed 2026-11-08T20:22Z, verdict: proceed with amendments)

* Exact identity would enqueue a model request on every five-minute reading. Amendment: the scheduling key keeps the coarse value in the existing column, so scan/forecast cost is unchanged; only manual invocation or an actual substantive change creates new work.
* A clock in the capture would churn identity. Amendment: as-of is a filter only; empty/withheld/unavailable captures stay identical across clock-only changes (regression required).
* New table needs the consumer schema to have run. Amendment: absent or unindexed means unknown (withheld), never granted; report as an activation prerequisite.
* Trigger attribution must survive retries. Amendment: recompute at each claim; the last claim produced the output.
* Rejected: stubbing human review notes (not model-derived); a per-sensor-ID guess list (finding 4).

## Test plan (names are behaviours; no constant-restating tests)

* Same-bucket distinct arrival: view latest, provider request IDs/values, task reuse (new task id), old task stale.
* Same-bucket context change (anchor-adjacent row) invalidates.
* Scheduling: scan does not enqueue per reading within the bucket.
* Withdrawal: uncited summary/finding/unknown and `edited_output` events stubbed in detail, list, export, raw JSON.
* Manual completion then proactive scan stays `manual-proposal`; proactive completion then manual invoke stays `review-suggested`.
* Unsampled declined noncanonical control: capture withheld and every historical projection withheld; unindexed control fails closed; per-home lookup uses key access only.
* Future row excluded, boundary equal-to-as-of included, old (beyond horizon) excluded, missing; future never fresh.
* Existing C1 regressions kept (provenance, collision, retrofit, roles, multi-seal stability).

## Details

Files: `sensor_view.py`, `sensor_consumer.py` (table only), `assistants.py`, `ops.js`/`assistants.js` (text only), `index.html` (account name), `src/core/README.md`, `src/api/tests/test_quality_sensors.py`.
Validation now: ruff, `node --check`, SQLite unittest subset. PENDING (coordinator admission): real SQL Server helper and new regressions under the heavy lock, real Chromium/axe/keyboard/reflow, `tools/rpi-checks.py --changed`, exact committed-tree import proof.
