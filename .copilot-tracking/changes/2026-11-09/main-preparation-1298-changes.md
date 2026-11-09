<!-- markdownlint-disable-file -->
# Changes: source-preserving current-main preparation (#1298)

* Task slug: main-preparation-1298, date 2026-11-09
* Plan: .copilot-tracking/plans/2026-11-09/main-preparation-1298-plan.md
* Logs (uncommitted, owned): `/tmp/i1298-mainprep.syPvb5`

## Actions

* Commit `812e61a8cce5fc5efc78bf0cc4082abe460fd854`: research, plan, details, critique and state, made before the merge.
* Ordinary merge (`--no-ff`, no conflicts, no conflict resolution) of `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477` into that commit. Merge commit `703780ae0a39620cf714d940b64e0c758c02cb8a`, tree `27f90aef0b5c28e1d0e25330be67c116c005bf08`, parents `812e61a8c` and `ef28d4da4`. Author and committer are the repository-local noreply identity; trailer present.
* No source file was edited by this lane. The merge brought only main-side changes (3 commits: two generated rubric scores and #1308 SQL priority ordering).

## Source-equivalence proof (merge-proof.log)

* `tools/rpi-checks.py` blob `bd90dd68...` and `tools/test_rpi_checks.py` blob `068121a0...` equal approved `dadcd6da8`; `git diff --name-only dadcd6da8 HEAD -- tools` is empty.
* The tools patch `9f9aacc8b..dadcd6da8` (+50 -2) is byte-identical to `origin/main..HEAD` for `tools/`.
* The seven approved tracking blobs equal `dadcd6da8`; they are unchanged. Old `fef352e0` adverse evidence and the fresh critique and Review were not edited.
* Ancestry: `dadcd6da8`, `ef28d4da4`, `8d6f029ca`, `9f9aacc8b` and `812e61a8c` are all ancestors of the merge.
* `origin/main..HEAD` non-tracking paths: only the two tool files. Main's `tools/`, workflows, `src/README.md`, `chatthreads.py` and the sensor fixture were untouched, and `mssqlstore.py` on main still imports `.chatthreads`, so the selector premise holds.

## Validation (owner demo-targeted tier; `~/.venvs/zf123-pinned`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0 matching the gate pins, no installation)

| Command | Exit | Result |
| --- | --- | --- |
| `python -m unittest discover -s tools -p test_rpi_checks.py -v` | 0 | Ran 103, OK, 0 skipped |
| same with `-k chat_schema -k changed_core_sensor -k direct_sensor` | 0 | Ran 3, OK |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on both tool files | 0 | All checks passed |
| `ruff format --isolated --line-length 100 --check` on both files | 0 | 2 files already formatted |
| `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` | 0 | no issues in 2 files |
| `git diff --check origin/main HEAD` | 0 | clean |

## Not run or not claimed

* No `rpi-checks --all`, no actual SQL or sensor MSSQL execution, no Docker, no hosted CI observation, no receipt (none existed; synthetic receipt fixtures in the unit suite are not gate passes), no other project suites. The #1308 SQL changes were merged without behavioral review here.
* Literal full-gate criterion stays unmet; `Refs #1298` only.
