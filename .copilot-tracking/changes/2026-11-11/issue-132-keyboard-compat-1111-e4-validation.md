---
title: Issue 132 keyboard probe E4 validation record
description: Additive validation record for the E4 candidate f8939a5a, covering the CI-exact typing rerun and corrected sequence (issue 132)
ms.date: 2026-11-11
---

## Scope

Additive to the [original Changes](issue-132-keyboard-compat-1111-e4-changes.md), which is preserved verbatim. Authorized by the [validation amendment](../../plans/2026-11-11/issue-132-keyboard-compat-1111-e4-validation-amendment.md). Session `3daf20c8-310c-4926-85ce-96019ffd6646`; candidate head `f8939a5a438b3fac62c548d2a42c50f36f8a2778`, tree `b2b765c565a82fff758292e688cf084b41c55e35`, base `35eb0e559c7d0660ab87594732675b71be7bee67`. No source, test, product or config edit was made. E4 spent, E5 remains.

## Corrected typing sequence

The original Changes said full-project mypy ran once. Actual sequence in the original E4: (1) 24 errors in 10 files before restore; (2) 4 errors in 1 file after private editable installs; (3) 2 errors with ad-hoc `MYPYPATH=../agents/src`. Those runs were not the CI command and the two `unused-ignore` errors were an artefact of the ad-hoc path, not evidence about the baseline. They remain recorded as failed original runs.

## CI contract and restoration

`.github/workflows/src-ci.yml` installs for api with `pip install -e ../core -e ../agents -e ".[dev]"` (Python 3.12), then runs `mypy` with no `MYPYPATH`, then `ruff check . && ruff format --check .`. A fresh private venv `/tmp/zf132-e4v/venv` (Python 3.12.3, pip 24.0; HOME, TMP, pip, mypy and ruff caches under `/tmp/zf132-e4v`) ran exactly that install from `src/api`: exit 0, log `/tmp/zf132-e4v/install.log`. Versions: mypy 2.4.0, ruff 0.17.1, playwright 1.64.0, core, agents and api editable from this worktree (CI is editable too; neither core nor agents ships `py.typed`). No other project, extra, tool or shared environment; no credentials, `.env` or default data read.

## Results (single attempt each)

| Selector | Command | Real exit | Output |
| --- | --- | --- | --- |
| Full API typing | `mypy` in `src/api`, no `MYPYPATH` | 0 | `Success: no issues found in 232 source files` (`/tmp/zf132-e4v/mypy.out`, `mypy.exit`) |
| Lint | `ruff check .` | 0 | `All checks passed!` (`ruff-check.out`) |
| Format | `ruff format --check .` | 0 | `149 files already formatted` (`ruff-format.out`) |
| Unit | `python -m unittest tests.test_specialist_keyboard_check -v` | 0 | Ran 7, OK (`unit.out`) |

No baseline diagnostic run was needed or made because typing passed. No code fix is claimed: the earlier residual was environment classification, not a change to any file.

## Source unchanged proof

After all runs `git status --short` was empty and `git diff f8939a5a HEAD -- src` was empty. Executable blob ids at HEAD: `src/api/README.md` `e2bcbbcbbecbc4dbc24b6b9a135eb60ba96c1d5e`; `src/api/checks/specialist_keyboard_browser_check.py` `0df2dcec1be63db93e8b99bb8d9ff3cb06915917`; `src/api/tests/test_specialist_keyboard_check.py` `f8633117257b6f51624a538a292529f54021e993`.

## Retained and not claimed

* The single original browser run (exit 0, 805 PASS, 15 negatives, seven roles with `regions: []`) is retained only for these same executable blobs; it was not a metadata-head run and was not rerun. Axe was not run; no assistive-technology, human, consent or production claim.
* Original limit stands: the existing probe does not record `/api/workorders` statuses or the empty-order text, so the absent-order cause is source-derived and not browser-observed.
* The [copied author Review](../../reviews/2026-11-11/issue-132-keyboard-compat-1111-e4-author-review.md) is placement of the original, not a fresh or independent Review. Root's independent exact-head review precedes any push. Whole #132, #134 and #233 stay open.
