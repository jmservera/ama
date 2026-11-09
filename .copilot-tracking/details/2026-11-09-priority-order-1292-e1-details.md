<!-- markdownlint-disable-file -->
# Details: issue 1292 extension E1 (2026-11-09)

Plan: [plan](../plans/2026-11-09-priority-order-1292-e1-plan.md).

## Phase 0: integrate main

`git fetch` then `git merge origin/main` (ordinary merge commit, message states no sibling code). Expected text overlap only in `src/core/README.md`; resolve preserving both intents. Record merged head, tree and `git diff --stat` for `src`.

## Phase 1: strict legacy metadata

File: `src/core/src/zava_forward/core/sqlstore.py`, `_suspect_ranges`.

* Read `rec_order_legacy` with a direct `SELECT value FROM meta WHERE key='rec_order_legacy'` so an absent key (no row) differs from a present value.
* Absent: no legacy range (never backfilled by that candidate); unchanged.
* Present: `json.loads`; require a `dict`, with key `rows` an `int` that is not `bool` and `>= 1`; the single range is `(1, rows)`. Any other content (invalid JSON, empty string, `{}`, `[]`, scalar, `null`, missing/negative/zero/string/bool/float count) returns `[everything]`, exactly as the C1 and batch readers do. Catch only `ValueError` and `TypeError` from `json.loads`/validation. Zero count is not a produced state (producer writes `len(keyed) >= 1`), so it is malformed.
* No guessing the latest record: the review then flags each employee's newest eligible record not provably latest, writes no ordinal, and the existing guard makes it non-actionable.

## Phase 2: UI ask

File: `src/api/src/zava_forward/api/web/app.js`, `priorityPanel`.

* `ask`: return early when `pending || checkHistory`; set `pending`; `try` paint success; `catch (e)` set `checkHistory = mutationNeedsHistory(e)` and `paint(null, e.message)`; `finally` clear `pending` and `aria-busy`.
* `paint(null)` and the "Suggest again" branch render the control only when `!checkHistory`; when latched render `h("p", { role: "status" }, "Reload the workspace and check priority review history before requesting another suggestion.")` in place of the button. Existing `role="alert"` error text remains. No new CSS, no new control, native button retained, permissions and Fluent classes untouched.
* Initial GET failure unchanged (read, no latch).

## Phase 3: tests

* `src/core/tests/test_priority_order.py`: class `LegacyMetadata(SqliteFixture)` (inherits no ordering tests) with a fixture building positive heuristic ordinals identified only by `rec_order_legacy`, deleting `rec_order_review`, and parametrised cases invalid JSON, `{}`, `[]`, `null`, `""`, missing `rows`, negative, zero, string, bool, float; each asserts unresolved newest, `latest_priority` `order_confirmed`/`actionable` false, accept and edit raise `PermissionError`, ordinals unchanged, batch source `review`, metadata text unchanged. Controls: valid positive count flags exactly the proven-ambiguous latest; absent key with insert-time ordinals flags none. `MssqlLegacyMetadata` repeats it on the owned SQL Server.
* `MssqlLegacyEdges`, `MssqlC3Corrections`, `MssqlC4Corrections`: SQL Server variants of the affected classes through a shared owned-database mixin extracted from `MssqlPriorityOrder` (no behaviour change to that class). Tests that cannot run on SQL Server by construction are skipped individually with a reason, never wholesale.
* `MssqlLockTimeoutBegin` (opt-in owned loopback): connection A takes `BEGIN IMMEDIATE`; connection B patches `mssqlstore.BEGIN` to a short `@LockTimeout`, expects the real timeout error, then reads `SELECT @@TRANCOUNT` (0) on B, rolls A back, and B runs `BEGIN IMMEDIATE`/`COMMIT`. The fake-driver tests stay.
* `src/api/tests/test_case_journey.py`: test that starts the real `ThreadingHTTPServer` with `make_handler`, a `SqlStore` whose `ai_priority` raises `CommittedReloadError`, posts `/api/ai/priority` over HTTP (real 409 body), and feeds status and body to the shipped `app.js` `api` and `priorityPanel` inside the Node DOM harness with a `fetch` returning that real response; asserts no enabled creation button, a status text, and a second click makes no second request. Variants for `uncertain` (503/transport) and an ordinary refusal (retry stays enabled). Replace nothing; the existing source-string test stays.

## Phase 4: validation (demo-targeted)

Commands recorded in the changes file: `test_priority_order` (SQLite, then SQL under `flock -n /tmp/ama-rpi-heavy.lock` with the task-owned container script), `test_resident_decisions`, `test_case_journey`, API tests that touch `/api/ai/priority` and priority panel, ruff and mypy configured for `src/core` and `src/api`, import provenance.

## Phase 5: records

README paragraph in `src/core/README.md` stating the strict legacy-row rule; changes record, one review, local commit with the noreply identity.
