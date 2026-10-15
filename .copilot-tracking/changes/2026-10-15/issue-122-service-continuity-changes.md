---
title: Issue 122 service continuity changes
---

* Added `continuity.py`, `tests/test_continuity.py`.
* Modified `ai.py` (gate hook), `ai_tasks.py` (Quarantined status, epoch check, review gate), `assistants.py` (db-level suspension checks, quarantine, views, export), `server.py` (routes), `store.py`, `sqlstore.py` (persist `continuity`), `mvp/README.md`.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` gives 531 tests OK (85 skipped). `tools/rename-zava-tests.py` fails here only on missing `pptx`/`PIL` modules, as it does without these changes.
* No knowledge-base files changed, so `docs/reference` index and log are untouched.

## Second pass: PR 269 review fixes (after merging origin/main)

* Merged `origin/main` cleanly (no conflict in `docs/reference/log.md`).
* `assistants.export` now returns proposals plus `total`, `truncated` and `supported`; the 5,000 limit is no longer silent.
* `continuity_export` records `complete`, `incomplete_reasons`, `assistants` counts, the ledger head (count, hash) and sealed digests.
* `verify_export` fails an incomplete bundle, a ledger tail cut short of the recorded head, a chain shorter than a digest, and an optional externally held `expected_head`.
* JSON store: AI task suspension is enforced and tested; assistants are SQL only and the bundle states `assistants.supported: false`.
* SQL portability: no `INSERT OR REPLACE/IGNORE`, `AUTOINCREMENT` or `PRAGMA` in the continuity code; `meta` reads use the same T-SQL-rewritten pattern as `procurement`, writes go through `_meta_set`.
* Validation: continuity tests 14 OK; full discover run recorded in the review. Docker is not usable here (permission denied), so `ZF_TEST_MSSQL=1` was not run locally; the `mssql` CI job is the evidence.
