---
title: Issue 111 inherited sensor draft correction changes
ms.date: 2026-11-10
task_id: 111-sensor-draft-inherited-repair-1110
---

Plan: [plan](../plans/2026-11-10-sensor-draft-111-inherited-repair-1110-plan.md). Details: [details](../details/2026-11-10-sensor-draft-111-inherited-repair-1110-details.md).

## Status at registration (prospective)

Registered 2026-11-10 BEFORE `implement-start`. No source edit has been made; the worktree is clean at `d5e7ac2ef560a09a7035ef55d038b40315313977`. The sections below are plans to be replaced by actual results before `implement-done`.

## Planned files

* `src/core/src/zava_forward/core/sensor_review_draft.py`
* `src/core/tests/test_sensor_review_draft.py`
* `src/core/pyproject.toml` (one new mypy override stanza)

## Budget record (Root-authorized)

Root authorized exactly ONE inherited correction batch on 2026-11-10 after the dated D2 proof (`handoff-111-dated-budget-audit-1336.md`). This batch consumes ONE.

| Date | Source | Case | Debit | Remaining bound |
| --- | --- | --- | --- | --- |
| 2026-11-03 | PR 871 Copilot review, no visible corrective commit | Uncertain historic | 0 or 1, before 2026-11-09 | see below |
| 2026-11-04 | R2 own-test expectation fix inside the initial increment | Uncertain historic | 0 or 1, before 2026-11-09 | see below |
| 2026-11-04 | PR 1075 source fix `bfa3d6c22` | Uncertain historic | 0 or 1, before 2026-11-09 | see below |
| After 2026-11-09 08:00:39Z | none | none | 0 | default five minus at most three leaves at least 2 before this batch |
| 2026-11-10 | this inherited batch, Root-authorized | Confirmed introduced defects (JSON audit after commit; Core mypy) | 1 (consumed) | conservative proven minimum at least 1 afterwards |

The one-time additional five is NOT relied on, no exhaustion is claimed, and no fresh five or reset applies. A second batch needs the Root's explicit selection; there is no self-retry. C1, C2 and C3 are acceptance criteria, not debits.

## Actual changes, divergences, validation

Source files changed (only these three):

* `src/core/src/zava_forward/core/sensor_review_draft.py`
  * `_persist` uses a `committed` flag with `try/finally` instead of `except BaseException`. The JSON path marks the draft committed as soon as `store.save()` returns, so memory is kept. The SQL path still audits then saves and treats `CommittedReloadError` as committed, with the same pending-audit trim and list restore when nothing committed.
  * New `DraftAuditError(RuntimeError)` carries the committed draft view. It is raised from an `OSError` audit failure after the JSON save. Other audit exceptions propagate unchanged with memory kept.
  * `CommittedReloadError` is now a top-level import (no import cycle). Every function and parameter is annotated (`DraftStore = Store | SqlStore`, `User`, `Json`). No cast, `type: ignore`, broad catch or fallback was added.
* `src/core/tests/test_sensor_review_draft.py`
  * Four JSON production-store regressions (audit failure after save keeps memory and disk, unrelated save and reload keep the draft, same-key retry is idempotent and keeps `created_at` and `created_by`, non-I/O audit failure keeps the draft). They failed on the frozen head `d5e7ac2ef` (log `frozen-head-regressions.log`) and pass now.
  * Full typing pass. Mixins are typed as `TestCase` under `TYPE_CHECKING`. Optionals are narrowed with asserts. Thread starts use plain loops. A dead `signal(policy=None) if False` branch was simplified to `signal()`.
* `src/core/pyproject.toml`: one `[[tool.mypy.overrides]]` stanza with `disallow_untyped_calls = false` for the module and its test, following the existing "typed code calls untyped Store" precedents.

Divergences:

* The module and one pyproject append were written with a one-off Python rewrite instead of the edit tool for two mechanical edits. Content was reviewed by diff and mypy afterwards.
* Main (`c9e15acb`) was not adopted: its changes touch `server.py`, `store.py` and `sqlstore.py`, not these files.

Validation (from `src/core` with `/tmp/zf-111-1110/venv`, module import origin asserted in this worktree; logs under `phase111-inherited-repair-evidence-1110/`):

* `ruff check .` pass, `ruff format --check .` pass (235 files), configured full Core `mypy` pass (288 files, 0 errors) in `lint-type.log`.
* Core draft tests: 65 ran, OK, 22 skipped (the opt-in MSSQL class). Analysis selectors `test_sensor_analysis*`: 30 ran, OK, 10 skipped. API `test_sensor_review_draft_api`: 6 OK (`tests-working-tree.log`).

Not run (stated gaps): live MSSQL for the restructured SQL control flow (SQLite only), full gate, `--changed`, browser. A retry after an audit-after-commit failure returns the existing draft and does not write the missing audit entry; the caller sees `DraftAuditError` once and is told to inform the programme manager.
