---
title: Issue 1259 C2 typing diagnostics research
description: Verified maintained mypy applicability and child-owned diagnostics versus parent 9b1e2567
ms.date: 2026-11-09
---

## Scope

Frozen child `6ead730731f0f26696dc2e4ecbf5d1b440be79d4` (tree `31df4f4ee77d5ba6d37ed521f87f5ef11ad74895`), exact parent `9b1e2567c2d0a2173b562103cd27508f75181526`. Research disposition: executed. Planning Readiness: Ready.

## Maintained command and profile

`.github/workflows/src-ci.yml` (matrix job, Python 3.12): `pip install <deps> -e ".[dev]"` then `mypy` from `src/<project>`; core deps empty, API `-e ../core -e ../agents`. `src/core/pyproject.toml` pins `mypy==2.4.0`, `ruff==0.17.1`, strict mode, `mypy_path = [src, tests]`. The `blob` and `sql` extras are not installed by CI; `mssql_python` has an `ignore_missing_imports` override. Neither `tests/test_ranking_archive_blob.py` nor `tests/ranking_blob_fixture.py` is under an `ignore_errors` override, so strict applies to both.

## Reproduction (owned venvs in a mktemp directory outside the repo; parent via `git archive`)

| Project | Child | Parent | Logs sha256 (child / parent) |
| --- | --- | --- | --- |
| core, CI profile | 86 errors, 2 files | 84 errors, 2 files | e1321de9... / 054c4b56... |
| API, CI profile | 9 errors, 1 file (core fixture) | 9 errors, 1 file | 88609b17... / d5bb1975... |

The brief's API 13 was not reproduced under the CI profile; the likely difference is an extra install profile or run configuration not proven here, so no claim is made about it. Parent errors are exact-match inherited: untyped fixture `ranking_blob_fixture.py` (9) and untyped parent tests in `test_ranking_archive_blob.py`. Mypy fails the maintained job on the parent already, so the child is not the first red cause.

Sorted diagnostic diff child versus parent (line numbers stripped) is exactly 2 added errors plus the matching note, all in the child-added test `test_conditional_create_never_lists_so_an_unreadable_listing_does_not_block_it` (added in `7fc680d0e`):

* `test_ranking_archive_blob.py:63` `no-untyped-def`: missing `-> None`.
* `test_ranking_archive_blob.py:68` `no-untyped-call`: `self.fake.requests("PUT")`, an untyped parent fixture helper.

The child-added API wiring test and runner tests add no diagnostic. `ranking_publication_runner` and its test are under `disallow_untyped_calls = false`.

## Optional-driver effect

No `azure-storage-blob` or `mssql-python` is installed in the CI profile; no diagnostic in scope is an import-missing or driver-typing effect.

## Fix design

`-> None` on the test; replace the helper call with a typed-clean comprehension over `self.fake.calls` filtered on `c[0] == "PUT"`, matching the neighbouring list-call comprehension. `requests` additionally excludes OAuth token URLs, which are not used on the SAS path of this test, so the assertion is equivalent. No `Any`, cast, ignore or fixture change. No transport, source or API behaviour change.
