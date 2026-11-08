---
title: Issue 79 review, continuation r12 (author-only)
ms.date: 2026-11-06
---

## Chronology and boundary

This author-only Review was created after the implementation commit `ec23c61651822012685e281965ef6850e543c47f` (tree `f50f88b519c8a19351a531a9e684c196a3f0f54e`) and after all checks recorded in the Changes record. It follows the planning commit `79d86e272bc980b8452c4914c5636888cde8b65b`, which preceded every test and source edit. It is not an independent or human review and leaves human approval unchecked. Reviewed boundary: inherited #79 findings 1 and 2 only.

Artifacts compared: research, plan (including its Critique Disposition), details, changes and state for r12, plus the committed source and test diff.

## Execution and outcome

* Execution: Complete for the supplied boundary.
* Outcome: Conformant with residual work (items below). No fresh FULL, no independent assessment.

## Reconciliation

* Plan P01 to P04 match the evidence: planning commit first, RED (`red1`, exit 1, 4 of 4 failing for the stated reasons: `PermissionError`, `OSError`, `StopIteration`), minimal fixes, GREEN (`green2` 45 tests, 0 skips, exit 0), `ruff2`, `format2` and `mypy2` exit 0.
* The preserved first failures (`ruff1` E501, `format1`, one wrapped test line) are recorded in the Changes record. The README sentence was added after `green2`; it touches no code.
* Diff read in full from the commit: runner `_verify` wrapper, `due`/`next_window_start` None when unreadable, `archive_unreadable` refusal, wrapped capacity probe, duplicate `id` refusal before `ranking.snapshot`. The ranking algorithm, `load_cases` and the helper are unchanged. No broad catch and no `StopIteration` handler.
* Requirements: unreadable archive never reads as empty or healthy (verify and schedule `problem`, exit 1; publish `archive_unreadable`, exit 2); probe `OSError` gives `capacity_missing`, exit 2; duplicates give `source_invalid` JSON, exit 2, no archive written (the archive directory is not even created).

## Findings

* RV-001 Low, process: the plan critique was a single self-run pass, not the default fresh critique worker. Disclosed in the plan. Destination: none for this task; noted for the independent reassessment.
* RV-002 Low, coverage: no test covers `--exercise` with an unreadable archive (exercise lists the problem and writes nothing by construction, unexercised) or an unhashable or missing `id` through the new duplicate check (existing handler already covers `TypeError` and `KeyError`, unexercised for this path). Destination: later `rpi-implement` only if the independent reviewer asks.
* RV-003 Residual, unproven: `ranking_publication._names` treats a non-directory archive path as empty (`os.path.isdir` false), which is existing helper behavior outside this boundary and was not reproduced or changed. Destination: `rpi-research` if the owner of the helper (#1231 overlap) wants it assessed.
* RV-004 Residual: the permission-denied tests simulate `os.listdir` and `shutil.disk_usage` failures with mocks; no real unreadable directory was exercised (running as a possibly privileged user would not prove it). Destination: independent reassessment.

## Validation and limits

* Author-run light checks only; Ruff 0.17.3 and mypy 2.4.1 differ from the pins. No gate, SQL, browser, Docker, install, lock, cloud, push, cleanup or deletion.
* Missing evidence: a fresh FULL gate on the corrected head, a fresh independent whole-feature assessment, hosted checks, named policy-owner signoff, Legal retention decision and scheduled retained operation. #1231 findings 3 and 4 are untouched and sequenced after this parent; any eventual child publication targets #73 with `Refs #79`.

## Routing

* Next: coordinator integrates this parent with the #1231 child, then corrects that child's two findings; then fresh FULL and independent assessment.
