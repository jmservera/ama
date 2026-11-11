---
title: Issue 1259 failing-first verification changes
description: Actual results of the source-unchanged replay of the unusable-archive-path regressions, executed 2026-11-11
ms.date: 2026-11-11
---

## Scope and result

* Source, tests, tools, workflows, knowledge base and cutover files: unchanged. Only tracking records and raw evidence were added. Plan, details and research were committed (`83b33c03b`) before the first observation.
* Every result below was executed on 2026-11-11, after the fix and after merge to main. It is a replay against pinned old source, not a prospective historical red then green, and no original chronology is implied.
* Candidate A (main parent `2be660e9d`) was loadable with the current tests, so candidate B (`6d793bc3a`) was not run. One run per source, no retries.

## Provenance

* Raw logs: `.copilot-tracking/evidence/2026-11-11-1259-failing-first/` (copies of the scratch logs under `/home/azureuser/.local/share/ama/gates/g1259-ff-2122/logs/`; runner `run.sh`).
* Exports by `git archive` into `$S/cur` (`077ad5ad2`) and `$S/oldA` (`2be660e9d` source with the `077ad5ad2` tests tree, 0 differences to the current tests). All 4 source blobs per export and the runner test blob equal the plan declarations (`00-blobs.log`). The old export has no `ranking_archive_blob.py`; no Blob test was selected.
* Runs: `env -i` with `python3 -S` (Python 3.12.3), `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=src:tests` relative to the export `src/core`, scratch `HOME`, `TMPDIR` and `ZF_DATA`. The module origin print shows all three imported modules under the export, not the editable install at `/home/azureuser/source/ama`.
* One cosmetic edit to the committed raw log `20-old-source-2be660e9d-red.log`: trailing whitespace on the subtest header line was stripped for `git diff --check`; the scratch original is unchanged.
* Frozen checkout and main untouched; ruff briefly created an ignored `src/core/.ruff_cache`, removed afterwards.

## Results

| Run | Source | Selectors | Exit | Outcome |
| --- | --- | --- | --- | --- |
| `10-current-source-green.log` | current main blobs | `UnusableArchivePathTests` plus the 2 existing unreadable-archive tests | 0 | Ran 8, OK. Subtests for regular file, dangling link, dangling ancestor and mocked stat failure pass; both absent-directory controls pass |
| `20-old-source-2be660e9d-red.log` | pre-fix main parent | same 8, current tests | 1 | Ran 8, FAILED (failures=7) |
| `30-static.log` | current files | ruff check, ruff format --check, AST parse, `git diff --check` | 0 each | clean (ruff 0.17.3) |

Old-source genuine failures (defect assertions, not import errors), 6 tests and 7 failures:

* Regular file, dangling link, dangling ancestor, stat failure: verify reports `('problem', None, True)` where unknown `('problem', None, None)` is required (the overdue window is asserted true instead of unknown).
* `test_regular_file_archive_exits_nonzero_through_main`: schedule exits `0 != 1` for a regular file archive.
* `test_store_status_is_a_problem_for_a_regular_file_archive`: Store status problems `[] is not true`.
* `test_oserror_without_a_reason_is_reported_without_the_path`: the archive path appears in the verify JSON (diagnostic path leak).

Old-source passes: both absent-directory controls (first run creatable, absent folder below a link to a real folder), and the two pre-existing unreadable-archive tests (the listdir PermissionError cases the issue said did not cover this).

## Mapping to the failing-first proof

* Regular file, dangling link: red on old source across verify, schedule and publish assertions (one test body checks verify, schedule, publish and exercise per scenario), green on current. The CLI exit and Store status tests add regular-file red.
* Absent-directory support: green on both old and current, so the fix preserved first-run behaviour.
* Archive-unreadable shape and path minimization: current green; old red for the path leak and unknown window.
* Reproduces, with raw durable logs, the earlier summary of 6 tests and 7 failures (changes 2026-11-08, recovery 2026-11-09). Counts agree; the source is now the true main parent, not the 1258 parent.

## Deviations and limits

* `py_compile` in the plan was replaced by an AST parse to avoid writing bytecode; the ruff checks and the passing import already cover it.
* No prospective historical red or green: this is today's replay. The original external `red.log` files were not retrieved or relied on.
* Mocked stat failure remains a mock; check/use race, Store overdue fallback and the 226 unanalysed skips from the earlier full run are not addressed here. Only 8 selected tests were run; no Blob, full Core, API or agents suite.
* Criterion 4 evidence is supplied for review; it is not ticked here. Criterion 5 (current FULL receipt, independent exact-head assessment, hosted checks) is unmet and not waived. Issue stays open.
