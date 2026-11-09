<!-- markdownlint-disable-file -->
# Research: issue 1292 extension E1 (2026-11-09)

Task `1292-e1-1109`, parent `1292-vc-1109`. Agent: RPI agent (hve-core-all:rpi-agent), Sonnet 5.5. Research disposition: `executed`. Planning Readiness: `Ready`.

## Authority and budget

* Owner approved five NEW additional correction cycles E1-E5 after the spent C5 through `ask_user` (coordinator brief). E1 is the first; four remain after it. C1-C5 and their adverse outcomes are preserved; no reset or renewal.
* Owner-selected demo-targeted test tier (no `rpi-checks --all`), owned nonqueued SQL, no push, PR, issue, board or merge. Source: coordinator `demo-rpi-common.md`.

## Identities

* Frozen start: `384d149ab9ae3d6708c65b1d6913892115095800`, branch `fix/demo-recovery-1292-1109`, clean.
* Fetched `origin/main` `f3532b02c01d7d21dadfe0d18f4f18b9f7502e07`: three commits since the earlier merge base `76db469b1`. `src` changes are `core/paired_equity.py`, its test and `core/README.md` only. No overlap with the files this task edits except `src/core/README.md` (text merge expected). No unmerged sibling #1288 code.

## Findings under correction (independent bounded Functional assessment, request_changes)

Source: coordinator `independent-1292-bounded/functional-findings.json`, head `384d149`. Verified against the code in this task.

### F1 High: malformed `rec_order_legacy` removes the legacy safety review

`SqlStore._suspect_ranges` (`sqlstore.py`) reads `rec_order_legacy` with `int(json.loads(value or "{}").get("rows", 0))` and turns `ValueError`, `TypeError` and `AttributeError` into `legacy = 0`. Consequences, confirmed by reading:

* Invalid JSON, `{}`, a non-object (`[]`, `"x"`, `1`, `null`), a missing `rows`, a negative count: all give `legacy <= 0`, no range is appended, the C1 and batch readers find nothing, `_review_priority_order` marks no row suspect and writes `rec_order_review`. A database with positive heuristic ordinals identified only by that row then has no unresolved flag, so accept or edit of a guessed latest record is allowed.
* `rows` as a string (`"3"`) or bool (`true`) is coerced by `int()` to 3 or 1, a guessed range.
* The empty string value is also treated as `{}` through `or`.
* The neighbouring readers (C1 `rec_order_backfills` and batch rows) already return the whole range for any malformed entry; the single legacy row is the inconsistent one. README states "any malformed entry makes every ordinal suspect".

Actual producer semantics (verified, not assumed): the only writer is `_backfill_zero_ordinals` (`sqlstore.py`), which returns early when no row has ordinal 0, and writes `rec_order_legacy` only when `start == 0` (nothing had an ordinal) with `rows=len(keyed)`, always at least 1, plus `same_second_groups` and `order`. The first-introduced writer (commit `656bacb56`) writes the same shape, also only when `rows` is non-empty. So a legitimate value is a JSON object with a positive integer `rows`. A zero or negative count is not a documented or produced state; there is no documented zero-count semantics to preserve, so it is malformed. An absent key (no row in `meta`) is legitimate: the database was never heuristically backfilled by that candidate. Absence must be distinguished from a present invalid value; `_meta_value` returns `None` for both a missing row and cannot hold NULL (`value ... NOT NULL` in SQLite and SQL Server DDL), so a direct `SELECT` is the clean test.

### F2 Medium: committed creation outcome still offers a repeat

`server.py` `POST /api/ai/priority` returns 409 `{"outcome": "committed"}` for `CommittedReloadError`; `api()` (`app.js`) keeps `status` and `outcome` on the error. `priorityPanel.ask` ignores them and calls `paint(null, e.message)`, whose `!rec` branch renders an enabled "Suggest my top 5". The review-action `act()` already latches `checkHistory = mutationNeedsHistory(e)` and disables the controls. `mutationNeedsHistory` is true for `committed`, `uncertain` and a missing status (transport loss). The existing C4 test checks the server by source substring only, which is not behaviour proof.

Design fit: `checkHistory` and `pending` already live in the panel closure; `ask` is shared by "Suggest my top 5" and "Suggest again". Initial `GET` failure must keep its current retry message (a read cannot have committed).

## Test-evidence gaps from the same assessment

* The C2/C4 edge classes (`SqliteLegacyEdges`, `SqliteC3Corrections`, `SqliteC4Corrections`) run on SQLite only. `MssqlPriorityOrder` subclasses `SqlitePriorityOrder` alone, so module totals on an admitted SQL Server do not show those classes used SQL Server.
* `MssqlBeginRecovery` uses a fake driver, including under a SQL-enabled invocation. No test takes a real lock timeout on `BEGIN`, then checks `@@TRANCOUNT` and that a second connection is usable. Production `_Conn.execute` BEGIN recovery (`mssqlstore.py`) must be read to build that proof.

## Constraints for the web change

* Loaded and fetched current [web-design-guidelines](../../.github/skills/web-design-guidelines/SKILL.md) source (`vercel-labs/web-interface-guidelines` `command.md`, fetched 2026-11-09). Relevant rules: async updates in a live region, specific error messages with a next step, buttons for actions, no destructive immediate action, `…` in loading text. The change keeps the existing `role="alert"`/`role="status"` regions, native `<button>`, Fluent classes and permissions; it removes an enabled control and adds a status paragraph only. No visual overhaul, no new styling.
* Design-system and WCAG baseline documents are preserved; this is not accessibility acceptance.

## Shared resource state

Heavy SQL work uses `flock -n /tmp/ama-rpi-heavy.lock` (nonqueued) with the coordinator's task-owned disposable SQL script pattern; if busy, do independent work. Recorded in the changes file at run time.

## Planning Readiness

Ready. Scope: `sqlstore.py` `_suspect_ranges`; `app.js` `priorityPanel.ask`/`paint`; targeted regressions (C0 metadata matrix on SQLite and owned SQL Server, real HTTP plus shipped-JS test, real lock-timeout BEGIN on SQL Server, affected edge classes on SQL Server); README sentence; local integration of `origin/main`.
