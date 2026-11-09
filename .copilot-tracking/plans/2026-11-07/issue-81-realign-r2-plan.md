<!-- markdownlint-disable-file -->
# Plan: issue #81 parent re-alignment (2026-11-07)

Research: [research](../../research/2026-11-07/issue-81-realign-r2-research.md). Details: [details](../../details/2026-11-07/issue-81-realign-r2-details.md). Prospective: written before any rebase or test run.

## Objective

Local rebase of `feat/controlled-lifecycle-integration-81` (frozen head `c5edb320a`) onto the final `origin/main` after #1245 and any score-only rubric commit, preserving all three child contributions, #1245 disclaimer/browser/UI/log content and #1241. Prepare a clean frozen head. No new behavior, no FULL gate, no push or remote write.

## Phases

* [ ] P1 Bounded wait for run `42361331168`, final fetch, re-pin main, inspect delta (stop and re-plan if the new delta touches parent source beyond `quality.py`/`projection.py`).
* [ ] P2 Backup refs (`refs/ama/issue81-r2-pre-realign` at `c5edb320a`), commit these prospective records plus critique and dispositions on the old base.
* [ ] P3 `git rebase origin/main`; genuine conflicts resolved keeping both intents; unclear conflicts stop with evidence.
* [ ] P4 Proof: ancestry, `range-diff`, per-path blob comparison for the 8 child source/test paths (expect `quality.py` to differ only by main's additive hunk; others identical), original evidence paths unchanged, main-side files equal main.
* [ ] P5 Focused regressions and static checks in scratch (below).
* [ ] P6 Dated addendum in `docs/architecture/cutover-evidence-pack.md`, changes record, author Review, state, commit, clean ignored-inclusive freeze.

## Blocker rules

* If the rubric run has not completed after about 20 minutes of bounded waits, report the blocker and do not freeze on a possibly stale base; local preparation on `312fa3dcc` may be left unfrozen only if recorded as such.
* A failed required regression or unavailable check means "aligned" is not claimed.

## Focused regression selection (no service, no heavy gate)

Isolated scratch venv (`/mnt/ama-gates/r2-81-realign-1107`), `env -i` allowlist, `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`/`ZF_DATA`/caches, no `ZF_RESIDENT_AZURE_TEST`, `AZURE_*`, `MSSQL*`. Package-scoped pip installs only after an actual missing-dependency failure; prove import origin is this worktree. From `src/core` with `PYTHONPATH=src:tests`:

| Check | Covers |
| --- | --- |
| `test_gates test_quality_procurement test_hazard_referral` | #1226/#1228/#1229 quality, provenance, capacity Pass/Fail/Unknown |
| `test_list_export` | #1241 `checklist_rows` beside the fail-closed quality module |
| `test_resident_decisions test_resident_documents test_resident_choice_queue test_bulk_edits test_aftercare test_consultation_controls test_change_provenance` | resident, authority and consent refusals |
| `ruff check`, `ruff format --check`, `mypy` in `src/core` | static |
| From `src/api` (api package in scratch venv): `test_chat_panel test_loading_feedback test_role_endpoint_inventory test_list_export_api test_form_staging_api` with `PYTHONPATH=tests:../core/tests:../agents/tests` | main-side #1245/#1241 content still passes beside parent core; included only if installs succeed without services |

Declared not run: FULL gate, browser harnesses, SQL Server/Azure, Docker, scanner, performance.

## Critique routing

One independent critique of this plan before P3. Compatible findings applied directly, none repeated; significant unresolved divergence becomes a blocker.

## Amendment 1 (post-critique, before the rebase)

Applies every disposition in [critique](./issue-81-realign-r2-critique.md): explicit `quality.py` content proof, pinned-then-refetched base, explicit local core/agents installs with per-package origin proof, core required and API best-effort (unavailable means unverified), add `test_finance_grants_screens`, and a precise `env -i` allowlist excluding `ZF_RESIDENT_MSSQL` and `ZF_RESIDENT_AZURE_TEST`.
