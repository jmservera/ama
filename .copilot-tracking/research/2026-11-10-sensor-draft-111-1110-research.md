---
title: Issue 111 sensor review draft write/read interface research (prospective, plan-only phase)
ms.date: 2026-11-10
task_id: 111-sensor-draft-1110
---

## Disposition and scope

Research executed 2026-11-10T04:27Z to 04:45Z against this worktree's source, not the dirty primary checkout. Planning Readiness: Ready.

Scope is the first undelivered #111 increment: a NEW, default-off, manual-review-only sensor review draft write/read interface over the existing `ReviewTaskCandidate`. It is not a correction of a failed bridge, not an existing generic task API, and not activation of any rule. Refs #111 only. The issue-wide correction balance is UNKNOWN, not exhausted, reset or five available. This phase spends and grants none. No source file is edited, no real approval, professional method or company sign-off is created or implied.

Owner evidence read in full: the LAST #111 addendum ("Bounded #111 task-contract admission addendum - 2026-11-10") and the earlier #111 section in `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/demo-further-capacity-1110.md`. Its line citations were pinned to `a0f7cf1821ea0db1721b0da47026fd0ed0fda1de`.

## Identities (verified, not assumed)

| Item | Value |
| --- | --- |
| Branch | `feat/demo-sensor-drafts-111-1110` (isolated worktree) |
| Head and `origin/main` after fetch | `0d262beee2dfa6feca27680aa1d596111154c8d9` (identical) |
| Worktree state at start | clean |
| Product delta pin `a0f7cf182` to head | none for `sensor_analysis.py`, `sensor_analysis_store.py`, `store.py`, `sqlstore.py`, `projection.py`, `server.py`, `ops.js` (`git diff --stat` empty) |
| Issue 111 | open; acceptance 1 and 3 unticked, 2 ticked (exercise labels); body status text reconciled 2026-11-07 |

The addendum's source claims were re-verified here, not trusted. All hold at head (details below).

## Verified current contracts (head `0d262beee`)

* `src/core/src/zava_forward/core/sensor_analysis.py` (255 lines): `TASK_TYPE="SENSOR_REVIEW_DUE"`, `TASK_QUEUE="condition-assessment"`; `RuleApproval.validate` only checks label syntax (authenticates no person); `AnalysisPolicy.rule_approved` needs an approval whose `rule_id==RULE_ID` and `policy_version==version`; `Signal` is frozen with `input_digest`; `review_task_candidate(signal, policy)` returns `None` unless approved, SUFFICIENT, REVIEW and version-matched, otherwise a frozen `ReviewTaskCandidate` with `status="PROPOSED"`, SHA256 `task_key` over type, home, window, policy version and input digest, and no-effect flags (`changes_ranking`, `starts_clock`, `releases_hold`, `diagnoses_hazard` all False; `resident_report_unaffected` True). `as_dict()` exists. The default policy has no approval, so a candidate never exists by default.
* `sensor_analysis_store.py` (46 lines): `analyse_retained(consumer, home_id, window, as_of, policy)` reads trusted consent and retained envelopes, fails closed to INSUFFICIENT (`RETAINED_READINGS_UNAVAILABLE`, `WEATHER_INPUT_NOT_INDOOR_MEASUREMENT`), never writes. Not duplicated.
* `sensor_consumer.py:410-415`: `SensorConsumer(store)` raises `ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")` for a JSON `Store`. Retained-reading derivation is SQL-only. Case id equals sensor `home_id` (fixture `home_id="ZF-1"`; `assistants.sensors` passes `case_id` as home).
* `taskqueues.py` queues are `new/priority/stale/blocked/overdue/unowned` projections; `condition-assessment` is not accepted. `assistants.py` tasks (`Assistants.invoke` -> `_enqueue` -> `assistant_tasks`) can become `pending` and be model-dispatched; they are not an inert store and are not reused. `workflows.offer_handoff` changes real ownership; not used.
* Generic case persistence: `store.py:113-118` `save()` writes whole `self.data` JSON, `_case():1248-1253` touches the case, `detail():460-511` deep-copies the whole case (`json.loads(json.dumps(c))`, line 466). `sqlstore.py:975-980` `_row` serialises the whole case body into `cases.body` (`json.dumps(c)`), `_load_case` reloads it, `save():1133-1201` skips unchanged bodies (`body == self._snap.get(cid)`), uses `rowversion` conflict detection (`ConflictError`), validates, appends pending audit in the same transaction, rolls back and `_discard()`s in-memory state on `ConflictError/GateError/PermissionError` (lines 1212-1230). So a new case-local key persists and reloads on JSON, SQLite and MSSQL without touching either store file. Not proven for concurrency or idempotency until tests run.
* Existing mutator convention to follow: `doc_controls.place_legal_hold` (lines 219-230): `with self.lock`, `_case`, mutate, `audit`, `save`. A module-level function over a store object (like `home_case.view(self, ...)`, `exception_register`) avoids editing the `Store` mixin list at `store.py:51`.
* Role projection `projection.py`: contractor detail is an allowlist (`DETAIL_FIELDS`, line 45; `contractor_detail`) so a new case key cannot reach it. `redact_staff_detail` (148-195) is NOT an allowlist: any new case key reaches every staff role. `allowed()` classifies every `GET /api/cases/...` as kind `case` (`server.py:210-211`) and `CONTRACTOR_GET` contains `case` (`projection.py:40`), so a contractor passes the route allow-list and the handler must itself refuse.
* Existing employee sensor-screen hook (named exactly): server route `GET /api/cases/{id}/sensors` at `src/api/src/zava_forward/api/server.py:803-817` (-> `Assistants.sensors`, `assistants.py:1040-1049`, SQL only, `authorize(..., "quality-evidence", case_id)`), rendered by `sensorPanel(id)` at `src/api/src/zava_forward/api/web/ops.js:36-65` inside the Quality and handover tab (`web/app.js:1070`; the generic `/api/cases/` GET branch is later at `server.py:827`, so a new `/sensor-drafts` branch beside line 803 matches first, `["quality","Quality and handover",[sensorPanel(id), ...]]`). `SENSOR_ROLES` is `["Quality Inspector","Retrofit Programme Manager"]` (`ops.js:4`), equal to the roles of `REGISTRY["quality-evidence"]` (`assistants.py:48`, `PM` is `Retrofit Programme Manager`, line 31). No existing sensor draft/task endpoint exists; a case-field alone is not rendered by this screen.
* Case POST convention: `POST /api/cases/{id}/{act}` dispatch in `server.py` (`act == "offer-handoff"` at line 1354 and others), error mapping at lines 1449-1470 (`ConflictError` 409, `PermissionError` 403, `KeyError` 404, `ValueError` 400).

## Findings that constrain the plan

1. The smallest honest increment is NEW storage + write + read projection + a rendering inside `sensorPanel`. A standalone adapter, a replay harness or a case-JSON field alone is not delivery.
2. The draft must be recomputed from signal and policy inside the write function (call the existing `review_task_candidate`) so a caller cannot supply an inconsistent or self-approved candidate. No duplicated key formula.
3. Need-to-know cannot rely on existing staff projection: the raw case key must be removed from generic staff detail (`projection.redact_staff_detail`) and read only through a dedicated allowlisted projection limited to the two existing sensor roles.
4. JSON `Store.save()` always rewrites and bumps `version`; replays must not call `save()`. SQL `save()` skips unchanged bodies, so replays are naturally silent there.
5. Approval is unprovable. The served route can only use the default `AnalysisPolicy()` (no approval) and therefore always denies; drafts exist only when synthetic tests or a synthetic harness construct an approval labelled as such. A real approval source is a separate, human-gated future decision and is not designed here.
6. The pinned local SQL gate list (`SENSOR_MSSQL_REQUIRED_TESTS`, `tools/rpi-checks.py:187`) is owned by #1300. A new MSSQL test must use its own opt-in flag and be run directly; it is not discovered by the gate and this plan does not edit `tools/`.

`ops.js` is in `AUDITED_FILES` of `src/api/tests/test_content_standard.py:12`, so the plain-language copy audit applies to any new employee copy.

## Ownership and ordering

* #135 owns import-refusal `store/sqlstore/register` integration; #1300 owns tools. This plan edits none of `store.py`, `sqlstore.py`, import projection (`import_exceptions`), `exception_register`, `exception_feeds`, `feed_failed_imports`, `tools/`.
* Independent first choice: new module `src/core/src/zava_forward/core/sensor_review_draft.py` plus dedicated tests. Dependent-but-not-#135 shared edges, all small and listed exactly in the plan: `core/projection.py` (one pop), `api/server.py` (one GET branch beside line 803, one `act` branch in the case POST dispatch), `api/web/ops.js` (additions inside `sensorPanel`).
* Ordering edge: none of the three touches a #135-owned hook. Before the first source write, confirm no sibling worktree or open branch changes these exact files (`git diff origin/main...<branch> -- <path>`); on overlap, stop source writes and sequence after #135 parent #73 integration and a fresh rebaseline. Unknown today because no #135 branch/PR was identified by the PR search (empty result), which is an absence of evidence, not a proof.

## Not established

Real rule approval, R1 to R3 method sign-off, assistive-technology and copy acceptance, MSSQL behaviour of the new key (not run in this phase), issue-wide correction balance, whether an unpushed attempt exists.

## Critique-driven additions (2026-11-10, one critique pass)

* `assistants.authorize` (`assistants.py:680-716`) also checks the current staff row, `case_ids` and `areas` scope; a role-only gate is insufficient, so the draft routes mirror it.
* `assistants._sensors_granted` (~1006-1018) rechecks consent and withholds derived content; draft reads do the same.
* Readings dated after `as_of` can yield REVIEW in the existing analysis (`sensor_analysis.py:197`, `sensor_analysis_store.py:29`); the draft module adds its own `FUTURE_READINGS` guard and leaves those files unchanged.
* `sqlstore._discard` (`sqlstore.py:1290`) quarantines pending audit and reloads touched cases; JSON `Store.save` is a non-atomic whole-file rewrite, so audit ordering is a documented residual.
* `mssqlstore.connection_string` needs `ZF_SQL_SERVER` and `ZF_SQL_DATABASE`; the `store_at` fixture selects MSSQL by `ZF_SENSOR_MSSQL`.
