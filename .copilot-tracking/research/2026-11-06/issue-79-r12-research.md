---
title: Issue 79 research, continuation r12 (inherited runner findings 1 and 2 from the whole-feature assessment)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

This research, the plan and the details are committed before any r12 test or source edit. No r4 to r11 record, source, test, log, receipt or state file is edited, repaired or regraded. The r9 FULL receipt and the r10 and r11 outcomes stand as historical evidence for their own heads.

## Brief

* Topic: two inherited #79 runner boundary issues found by the independent whole-feature assessment of child head `b7f6186d` (verdict approve_with_comments, four Medium). Findings 3 and 4 belong to the #1231 helper and manual integration and are out of scope.
* Purpose: decide the smallest behavior-preserving corrections in the runner and its existing tests.
* Posture `focused` (bounded internal task with named source targets). Output mode `convergence`. Provenance: caller brief.
* Extensions: repository instructions (`.github/copilot-instructions.md`) selected; web guidance skipped (no web files). No delegation: two tightly coupled findings in one module, handled inline.
* No interactive question was needed: the brief fixes scope, expected outputs and exit codes.

## Identity and pins (intake)

* Same original session `e4869dea-7260-432e-a2dd-1c7a3e01e32c`, branch `feat/ranking-publication-runner-79`, head `397419724e68b24bce879512a24c7df430177f87`, tree `c728049e33a3a0e20d9a7bf16b3738fabfbc14d7`, ignored-inclusive status empty.
* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, declared parent `feat/case-workbench-integration-73` at `ead177ef90d24666557708ea344848a1be43bdf8`, both unchanged. No rebase, merge, push or retarget. The #1231 child worktree is not touched.
* Research disposition `executed`; Planning Readiness `Ready`.

## Evidence read

* Assessment `functional-findings.json` and `metadata.json` under `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/review-1231-b7f-whole-functional-r64/`, read and not edited. The assessment is static; it ran no reproduction.
* Runner `src/core/src/zava_forward/core/ranking_publication_runner.py`, helper `ranking_publication.py` and `ranking.snapshot`.

## Wave 1, wider

Candidate boundaries where an `OSError` can leave the runner as a traceback: `ranking_publication.verify` (three runner calls to the helper's `_names`/open), the `free_bytes` callback, and `os.path.exists`. Candidate duplicate-identity sources: `load_cases`, direct `run(cases=...)`, the CLI.

## Wave 2, deeper

* C1 `ranking_publication.py:83-87`: `_names` calls `os.listdir` with no handler, so an unreadable archive directory raises `PermissionError`. The per-record `try` in `verify` (line 96 onward) covers only record contents, so a record-level read error is already a problem line.
* C2 `ranking_publication_runner.py:159` (verify operation) and `:185` (schedule and publish) call `verify` outside any handler. A failure escapes `run` and `main` as a traceback with no JSON.
* C3 `ranking_publication_runner.py:75-79,288`: `_free_bytes` calls `shutil.disk_usage`; the call at 288 is outside the publish `try`, so an `OSError` from the probe escapes. Injected `free_bytes` callbacks can raise too.
* C4 `ranking_publication_runner.py:250-260` and `ranking.py:160`: `ranking.snapshot` uses `next(...)` with no default when two adjacent ordered cases have identical rule keys. Duplicate cases (same `id`, hence all keys equal including `case_id`) make the generator empty and raise `StopIteration`. The runner's handler lists KeyError, TypeError, ValueError and AttributeError only. `load_cases` accepts duplicates because it checks only mapping shape and boolean `closed`.
* Case identity is `c["id"]` (ranking.py rows use `c["id"]`). An unhashable or missing id already raises TypeError or KeyError inside the existing handler.

## Wave 3, contrarian

* A broad `except Exception` or catching `StopIteration` would hide real defects and would also hide that the pure ranking algorithm has an unguarded `next`. Rejected: the brief forbids a broad catch and a ranking change.
* Treating an unreadable directory as an empty archive would report `due` and could let `publish` write a duplicate publication. Rejected: it hides the fault.
* Putting the uniqueness check only in `load_cases` would miss direct `run` callers. Rejected: the check belongs at the `run` boundary before ranking. `load_cases` stays as is.
* Changing the helper to return a problem for `listdir` failures would change helper behavior owned by #1231 overlap. Rejected: handle in the runner.
* Counter-risk: the assessment is static. Each finding is therefore reproduced by a failing regression test before any source edit; a finding that fails to reproduce gets no change.

## Decisions (convergence)

* F1 storage: add one small runner helper that calls `verify` and converts `OSError` into a check result with `count` 0, `latest` None, one problem line naming the exception type and strerror, and an `unreadable` marker. Use it at both call sites.
  * `verify` operation: status `problem` (exit 1), problem line, `overdue` None. Never `ok`.
  * `schedule`: status `problem`, `due` and `next_window_start` None, not `current`.
  * `publish`: refusal `archive_unreadable` with permissions and location guidance, exit 2, no write.
  * Capacity probe: wrap the `free_bytes` call; on `OSError` return refusal `capacity_missing` with the probe error type and guidance.
* F2 duplicates: inside the existing source-invalid `try`, before `ranking.snapshot`, compare the count of distinct `id` values with the case count; on a repeat return refusal `source_invalid` with a next action, writing nothing. Exit 2 through `main` follows from the existing `refused` mapping.
* Alternatives kept: raising in `load_cases` (insufficient), changing `ranking.snapshot` (out of scope), broad catches (rejected above).

## Limits

* Light checks only: the existing runner and publication test selector, Ruff, format and mypy with installed tools, external caches and no bytecode. No gate, SQL, browser, container, install or lock.
* Unchanged: the pure ranking algorithm, helper, concurrency and manual API behavior, policy, signoff and scheduling. Named policy-owner signoff, Legal retention and scheduled retained operation remain unproven. The corrected head needs a fresh FULL gate and a fresh independent whole-feature assessment; no earlier receipt covers it.
