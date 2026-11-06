---
title: Issue 79 plan, continuation r12
ms.date: 2026-11-06
---

Task `issue-79-r12-runner-storage-and-duplicates`, parent `issue-79-r10-runner-assessment-findings`. Planning readiness: ready.

## Executive summary

Two inherited runner boundary defects reported by the whole-feature assessment get regression tests first (real RED), then minimal runner fixes: archive enumeration and capacity probe `OSError` become structured problems or refusals with nonzero exit, and duplicate case ids are refused as `source_invalid` before ranking. The ranking algorithm, helper, concurrency and manual API behavior stay untouched. Light checks only. A fresh FULL gate and a fresh independent assessment are still required for the corrected head.

## User Decisions and Requirements

* Handle only inherited #79 findings 1 and 2; #1231 findings 3 and 4 are out of scope and sequenced after this parent.
* Reproduce each failure through `run` and `main` before fixing; no broad catch, no fake fallback, no `StopIteration` catch.
* Unreadable archive is never healthy or empty. Duplicate ids give `source_invalid` JSON, exit 2, no archive write.
* Smallest behavior-preserving change to the runner and its existing tests; README only if necessary.
* Light only: no FULL, SQL, browser, container, install, lock, cloud, cleanup or deletion. External caches and no bytecode.
* Preserve all earlier original and adverse records; commit research, plan and details before any test or source edit.

## Goals and scope

* Goal: structured, actionable results instead of tracebacks for these two inputs.
* Non-goals: ranking algorithm, helper, concurrency, manual API, policy, signoff, scheduling, dependencies.

## Requirements and acceptance criteria

* Verify with `listdir` PermissionError: status `problem`, exit 1, a problem line, never `ok`.
* Schedule with the same failure: status `problem`, `due` and `next_window_start` None, never `current`.
* Publish with the same failure: refusal `archive_unreadable`, exit 2, nothing written.
* Capacity probe `OSError` through `run` and `main`: refusal `capacity_missing` naming the error, exit 2, no write.
* Duplicate open case through direct `run` and CLI: `source_invalid`, exit 2, JSON output, no archive file.
* Valid behavior (existing 41 tests) unchanged.

## Phase Checklist

* [ ] P01: commit this research, plan and details first.
* [ ] P02: add regression tests to `test_ranking_publication_runner.py`; run once and keep the raw RED output at a fresh path under `/tmp/79-functional-r12-1106/`.
* [ ] P03: minimal corrections in `ranking_publication_runner.py`; run the combined selector, Ruff, format and mypy once each to new log paths.
* [ ] P04: write Changes and state, validate JSON, links and diff, then a dedicated author-only Review and commit.

Details: [details](../../details/2026-11-06/issue-79-r12-details.md). Research: [research](../../research/2026-11-06/issue-79-r12-research.md).

## Critique Disposition

Single self-run pass before any test or source edit (no worker dispatched, recorded as a deviation from the default fresh-worker critique; the change is a few lines reusing existing statuses). Findings applied directly: the unreadable-archive result must not set `due` true (it would claim a publication is needed on an unknown archive), so `due` and `next_window_start` are None; the exercise operation keeps writing nothing and lists the problem; `capacity_missing` is reused for a failed probe rather than a new code. Nothing significant or divergent. No second critique runs.

## Follow-Up Items

* #1231 findings 3 and 4 (manual HTTP hard-link error, cleanup failure outcome): after this parent, on the child.
* Loose `as_of` validation in `publish` and the helper's schema hardening: unchanged, inherited.

Tier: FULL for the whole feature; this continuation is light.
