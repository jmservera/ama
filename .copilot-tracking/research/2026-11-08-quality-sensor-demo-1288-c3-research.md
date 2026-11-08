# Research: #1288 correction 3 (C3)

Written 2026-11-08T20:52Z, before any product or test edit. Refs #1288, #107. No closing claim.

## Authority and scope

The owner authorised up to three further bounded correction cycles for this issue only after C1 and C2. C3 is the first. It does not waive resident consent, safety, human review, spend, validation, deployment or live-model gates. Source and light local tests only; no Azure, model, SQL Server, Docker, browser or other heavy process. The FULL gate, actual SQL, query plans, browser/axe, release and live walkthrough are separately admitted later actions. #184 is unmerged; this branch is not stacked on it and its contract is not assumed.

## Start state

Head `8d95ae9613eed30b1e3fc2b1e03170de8c6391a5`, tree `32a3f744703a092ddd9aea7685223a3124a9d3fb`, branch `feat/quality-sensor-demo-1288`, tracked clean. Evidence read in full: the independent C2 functional findings (4 High, 2 Medium), the C1-to-C2 committed diff and the coordinator light probes (mechanism probes, not SQL or browser reproduction). Original, C1 and C2 artifacts, reviews and `/tmp` raw outputs are preserved.

## Findings confirmed in the committed code

| # | Sev | Confirmed cause |
| --- | --- | --- |
| 1 | High | `sensor_view.capture_source` sets `state` from the 366-day newest window only (`"ok" if window else "no-readings"`), but `before`/`after` context is queried separately around the anchor and kept. `assistants._withhold_sensors` returns early unless stored state is `ok`, so a context-only capture skips current-consent projection; the UI also hides context tables for `no-readings` while the model received them. Probe confirms. |
| 2 | High | `_scrub_events` stubs only `output`/`edited_output`. The required free-text `verification.note`, `review.note` and each review event `note` are persisted and projected unchanged, so a reviewer who saw a value can leave it visible after withdrawal. |
| 3 | High | `scan` passes the coarse `known` flag to `eligible`, but the Quality gap branches (no measures, missing/not-accepted records, checklist gaps) return `True` before it is read. Each same-bucket arrival changes the exact task id, so another task and model call is enqueued. Probe confirms for missing measures. |
| 4 | High | `claim` reads only the first 50 events of every kind and defaults to `proactive` when no requested invocation is in that prefix; a manual request after event 50 is hidden and a sensor-cited result is labelled autonomous L4. |
| 5 | Medium | The per-home control index is filled only by `_schema` called from `configure`, which also deletes and replaces policy and controls. Nothing initialises it on an existing configured store, so captures are unavailable until an operator reconfigures (destructive). Backfill runs only when the index is entirely empty, so a partial index is not repaired, and a missing index row hides a decline (read side checks only sampled sensors and the rows it finds). |
| 6 | Medium | `review()` loads the projected view body (`_view`) and writes it back, so rejecting after withdrawal replaces the durable snapshot and output with redacted stubs; restoring consent cannot recover them. |

## Design decisions

1. Source state: `ok` when any captured value-bearing array (window, before, after) is non-empty. Latest stays null with freshness unknown when the window is empty. `_withhold_sensors` keys on the captured citations, not on the stored state, so UI, model and projection agree.
2. Withheld projection also stubs `verification.note`, `review.note` and event `note` fields (other fields kept); durable originals are untouched and projections return when consent is granted.
3. Throttle: one shared helper decides due-ness for `scan` and `forecast`. It first applies `eligible` (which keeps non-sensor changes eligible), then skips only when the exact task does not exist yet and the coarse scheduling signature is already known. Manual requests never pass through it, so they are not suppressed, and non-sensor changes alter the coarse signature so they are not suppressed.
4. Dispatch provenance: durable `manual_requested` on the task body, written atomically in `_enqueue` (new task or re-invoke of a pending/leased/disabled task; an in-flight dispatch is marked requested). `claim` binds `dispatch.trigger` from it. A task without the field (legacy) or any ambiguity is `requested`, never proactive. No event-prefix scan.
5. Migration: an idempotent, transactional reconcile that derives the per-home index from existing controls (adds missing, removes orphans), never touching policy, controls or consent. It runs at `Assistants.migrate` (store start) and from a `SensorConsumer` method; `configure` keeps its behaviour. The reader also fails closed when index and control row counts differ (both tables are cohort bounded, at most 100).
6. Review writes the stored body: checks use the projected view, the update is applied to a fresh stored row. Verify/accept/edit-accept while consent is withheld are refused (the reviewer cannot see the evidence). Reject is allowed and preserves the stored snapshot/output.

## Alternatives rejected

* Counting more events or raising the 50 limit: still ambiguous at the next boundary.
* Throttling by changing task identity back to the coarse signature: reverts the C2 evidence/identity binding.
* Dropping and recreating the index in a migration: needs a write lock window and can fail open; reconcile is additive with a read-time count guard.

## Validation tier

FULL is required (SQL consent/control schema and security-sensitive projection, owner decision D4). It is a later coordinator-admitted action: `python3 tools/rpi-checks.py --all --base <sha> --out <external dir>`, receipt verification, then exact-head review. Not started here. Now: focused SQLite suites only.

## Pending (not claimed)

Actual SQL Server run of the Mssql variants and index query plans, Chromium/axe/keyboard/reflow, FULL gate, release and serving-model attestation, #184 semantic integration, live walkthrough.
