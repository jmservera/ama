# Plan: #1288 correction 4 (C4)

Written 2026-11-08T21:35Z (real clock) after the C4 research and before any product or test edit. Refs #1288, #107. No closing claim. Details: `.copilot-tracking/details/2026-11-08-quality-sensor-demo-1288-c4-details.md`.

## Phases

* [ ] P1 Red tests first in `src/api/tests/test_quality_sensors.py` (SQLite only); unique logs `/tmp/c4-red-*.txt` with exit codes.
* [ ] P2 F1 verified index marker, strict reconcile, fail-closed reads.
* [ ] P3 F2/F3 scheduling scoped to current release/epoch and latest eligible task; stale-before-dispatch replaced once.
* [ ] P4 F4 dispatch trigger frozen per fence.
* [ ] P5 F5 accurate dual-horizon `AS_OF_RULE`.
* [ ] P6 Green light suites, ruff, README. No web edit expected; if one is needed refresh the web-design-guidelines raw source before editing and again before review.
* [ ] P7 Changes artifact, one Review, state JSON, commit (privacy-safe email, Refs #1288, Copilot trailer).

## Red/green test plan (all synthetic, SQLite, scripted provider labelled as a mock)

| Test | Red now because | Green means |
| --- | --- | --- |
| Equal-count wrong-home index: (A,A1),(B,A2) with A2 declined for A | view of A is granted | A not granted and detail/list/export withheld after a model return, with fixed marker absent or digest mismatch |
| Missing plus orphan with equal counts | granted | not granted until a successful migrate; migrate then restores exact index, policy and controls byte-identical, marker valid |
| Failed reconcile (unrelated malformed or home-less control) | old wrong index kept, granted | marker removed, all consent unknown, readings and historical citations withheld; fixing the control and migrating restores |
| Marker absent on a legacy store | granted | unknown until migrate; migrate idempotent (second run no write change) |
| Release activation, unchanged eligible case (Quality and assessment-preparation) | `_due` false forever | scan and forecast both offer new work once; a second scan under the same release is throttled |
| Epoch advance, unchanged eligible case | same | same |
| Non-sensor A to B to A with a new same-bucket reading | suppressed by historical A | new task offered; sensor-only arrival after it still throttled |
| Enqueue, same-bucket arrival, stale claim, rescan, restart, dispatch | first task stale, bucket suppressed, 0 calls | stale task not counted, exactly one replacement, one provider call, allowance used once; arrivals after dispatch throttled |
| Provider barrier: proactive dispatch then manual request in flight, then release | returned output labelled requested | trigger stays proactive, `manual_requested` true, invocation event recorded |
| Manual before claim; retry after timeout with and without a request in between | n/a or unproven | pre-claim request labelled requested; retry attributed by the flag at its own claim |
| Old anchor (500 days) context capture | rule says 366 days only | rule states newest-window horizon and 30-day-around-anchor context that may be older, capped at as-of, in the UI payload and in the provider prompt; IDs equal |

## Critique (executed once, final candidate)

Verdict: proceed with amendments, applied directly.

* A bare count-equal marker adds nothing over C3; the per-home digest is what detects a compensating swap, so it is mandatory.
* Reconcile must compute everything before writing and clear the marker on any exception, so a swallowed error cannot leave a stale proof.
* Ordering by `created_at` can tie; treat tied latest tasks as matching if any matches (conservative toward throttling inside one clock tick) and advance the test clock to avoid reliance on ties.
* Do not touch `claim` allowance code; the finite allowance stays the limit. A replacement is bounded by the stale task having made no call.
* Keep the diff in `sensor_consumer.py` small (overlaps #184); put digest logic in `sensor_view` and import it.

## Validation

Light: `test_quality_sensors`, `test_assistants`, `test_assistant_release`, `test_sensor_consumer`, `test_sensor_ingestion`, `test_sensor_consistency`, ruff (line length 100; `assistants.py` F,E9 only). PENDING and not run: FULL gate, SQL Server variants and query plans, browser/axe/keyboard/reflow, release and serving-model attestation, #184 semantic merge, live walkthrough.
