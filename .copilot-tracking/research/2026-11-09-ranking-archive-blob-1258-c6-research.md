# Issue 1258 C6 CI-profile typing, lint and format research (2026-11-09)

Refs #1258. Task `1258-ranking-archive-blob-c6`, parent `1258-ranking-archive-blob-lint-diagnostic`. Records written and committed before any main merge or source edit. Earlier records, the five spent cycles C1 to C5, the lint diagnostic and every adverse outcome are history and are not edited.

## Authority

Owner on 2026-11-09 selected five additional parent cycles C6 to C10 (durable comment 6747925505). C1 to C5 stay spent; no reset or standing renewal. C6 is active; C7 to C10 only if needed; stop when resolved. Scope: the confirmed parent Core 84 and API 9 CI-profile mypy failures, the wiring-test 10 lint errors and format diff, composition with current main, and relevant checks. Lint-only authorization was insufficient. Not authorized: Azure deployment, identity, production access, unrelated JSON migration, retention approval, filesystem or mount hardening, archive SQL redesign. Owner platform stays Blob JSON ranking-archive persistence. Demo-targeted checks, no blanket full gate. No push, PR, issue or board write.

## Research disposition

Executed (read-only baseline reproduction). Planning Readiness: Ready.

## Identities

* Candidate HEAD `b135c172aaea34524645ae955a871c3fb670bed0`, tree `ca9950d842bea7d59ba52ea35a5110fde371c18e`, branch `fix/ranking-archive-ancestor-durability`; non-tracking content equals frozen `9b1e2567`.
* Fetched `origin/main` at research time: `5c3b8b4bed4bef82b53b15274fdbbb27d9eaba74` (merge-base with HEAD `8d6f029ca`). The actual merge SHA is re-fetched and recorded in the changes file.

## Actual CI profile (read from `.github/workflows/src-ci.yml` job `project`, Python 3.12)

* core: working directory `src/core`, `pip install -e ".[dev]"` (no Blob or SQL extra), then `ruff check . && ruff format --check .`, then `mypy`.
* api: working directory `src/api`, `pip install -e ../core -e ../agents -e ".[dev]"`; the api distribution itself depends on `zava-forward-core[sql,blob]`, so this profile does install `azure-storage-blob==12.31.0` and `mssql-python==1.15.0`. Same Lint and Type check steps.
* Pins: `ruff==0.17.1`, `mypy==2.4.0` in each `pyproject.toml` `dev` extra; config is each project's own `[tool.ruff]` and `[tool.mypy]` (strict). No isolated profile, no `--select`.
* Optional-import typing: core `[[tool.mypy.overrides]] mssql_python ignore_missing_imports` covers the absent SQL driver. The Blob adapter `ranking_archive_blob.py` uses a REST transport (`Transport = Callable[..., tuple[int, Mapping[str, str], bytes]]`) and no SDK import, so SDK absence does not affect it.

## Owned environment

Directory `/tmp/c6-1258-XXXXXX` (path in `/tmp/c6-1258-dir.txt`), separate `core-venv` and `api-venv`, editable installs pointing at this worktree (`pip list` shows `zava-forward-core`, `-agents`, `-api` at `/home/azureuser/source/ama-demo-wt/issue-1258-blob/src/...`). No global install, no use of the dirty primary checkout. Core venv has no azure-storage-blob or mssql-python; api venv has both. Raw logs and SHA-256 manifest: `<dir>/base/` (`SHA256SUMS`).

## Baseline (red, retained)

| Command (project root) | Exit | Result |
| --- | --- | --- |
| core `ruff check .` | 0 | passed |
| core `ruff format --check .` | 0 | 225 files formatted |
| core `mypy` | 1 | 84 errors in 2 files, 278 source files |
| api `ruff check .` | 1 | 10 errors, all in `tests/test_ranking_publication_wiring.py` (9 E501, 1 I001) |
| api `ruff format --check .` | 1 | 1 file would be reformatted (the wiring test) |
| api `mypy` | 1 | 9 errors in 1 file, 199 source files |

Core 84 = 41 `no-untyped-def` plus 43 `no-untyped-call`, all in two core test files: `tests/ranking_blob_fixture.py` (9: 6 def, 3 call) and `tests/test_ranking_archive_blob.py` (75). The API 9 are the same fixture file reached through `mypy_path ../core/tests`; there are no API-owned typing errors. Source modules (`ranking_archive_blob.py`, `ranking_publication.py`, runner) are already clean.

## Root cause

The C5 fixture and its test were written untyped. Under `strict` they fail `disallow_untyped_defs` and `disallow_untyped_calls`. The reason C5 did not catch it is not established by the available evidence; the C5 record says only that ruff and mypy were clean on its own selection. The calls to `snap()` (from `test_ranking_publication.py`, which sits in the `ignore_errors` override list) are untyped too, so `snap` needs an annotation on its definition. The independent critique found that annotating `snap` alone is insufficient: `ranking.snapshot` (untyped, in an `ignore_errors` module) is also called at lines 74, 232 and 304 and inside `snap`, so its signature needs a typed boundary; this is recorded as a plan correction.

## Smallest proper fix (no relaxation)

* Annotate `ranking_blob_fixture.FakeBlobContainer` with real types (`dict[str, bytes]`, `dict[str, dict[str, str]]`, a call-record list, fault lists) and its transport signature returning `tuple[int, dict[str, str], bytes]`, assignable to the adapter's `Transport`.
* Annotate the helpers and test methods of `test_ranking_archive_blob.py` (`-> None`, `FakeBlobContainer`, `unittest.TestCase`, `Callable`), and give `test_ranking_publication.snap` its return type.
* Wiring test: apply the maintained formatter output (`ruff format`) and the single import-sort fix (`ruff check --select I --fix` limited to that finding), no rule changes. Verify by the project's own `ruff check .`.
* Forbidden and not planned: `Any` or `object` casts hiding errors, `type: ignore`, `# noqa`, new `pyproject` overrides or per-file ignores, config relaxation, weaker or deleted assertions.

## Main composition

Main moved from `8d6f029c` to `5c3b8b4b` (lifecycle 1240, controls 1313, photo 1315, receipts 1320 and rubric records). Main touched `src/api/src/zava_forward/api/server.py` and `src/core/src/zava_forward/core/store.py`, both also edited by this branch, so conflicts are possible. Workflows and `pyproject.toml` are unchanged by main in the compared range. Ordinary merge only, no rebase, amend or force; ambiguous conflicts stop the task.

## Limits and risks

* The fakes are not Azure durability, WORM or live acceptance.
* Main's merge may add new mypy or ruff findings; the post-merge profile is re-run in full and any new failure in this workstream is recorded, not hidden.
* No resource contention: no SQL, browser or Docker needed. The 1292 SQL campaign and 1288 E6 browser lane are not used.
