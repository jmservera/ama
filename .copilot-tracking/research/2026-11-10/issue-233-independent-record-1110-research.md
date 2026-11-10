---
title: Issue 233 independent qualification record research
description: Metadata-only research for the independent functional qualification of the two-screen tension coverage candidate
ms.date: 2026-11-10
---

## Disposition and readiness

Research disposition: executed (read-only, metadata). Planning Readiness: Ready.

## Evidence read

* Independent Functional assessment 709b5365-5029-49c7-92f7-1d7576b54718 (`independent-233-two-screen-coverage-1110/functional-findings.json` under the coordinator evidence root): verdict approve_with_comments, 0 Critical/High/Low, 1 nonblocking Medium. It read all 13 changed files at head 6725ba50.
* Medium finding, `src/api/checks/atlas_tensions_browser_check.py` lines 407-413: the expected current design version `1` is tested as a substring of the whole Design version panel, which also holds the recorded timestamp `2026-10-20T09:00:00Z`. A rendered version of 2, Unknown or an omitted value could still pass. This is a static counterexample, not a browser mutation run and not a product defect. Reading the current source at the same lines confirms the assertion is unchanged at 6725.
* Follow-up issue #1362 (https://github.com/jmservera/ama/issues/1362): OPEN, generic template, no labels, created 2026-11-10 (confirmed read-only with `gh issue view`; no write).
* Coordinator logs: the original seven-event witness verified exit 0 at head 6725/tree c4ca, log sha256 6dd6bead...fa6. Root focused 11 unit tests passed on unchanged 6725 with the borrowed interpreter and candidate-first PYTHONPATH. The concrete-source log asserts 42 concrete zava_forward module files, the Core store, the checker and the API `__main__` entrypoint in the 233 worktree, and states that the namespace also exposes a fallback path.
* Root diagnostics preserved: an initial test import failure because the pinned lint venv lacks Playwright; an all-namespace-path guard assertion that failed because an extra editable fallback exists (not because a concrete Core or checker import was wrong); then a diagnostic printing actual paths and Playwright 1.64.0, after which the concrete-module guard and 11 units passed. No dependency install or environment mutation. Diagnostic findings, not blind retry, not a failure waiver.

## Findings for the record

* Overall current-version coverage is PARTIAL. No claim that every new assertion is semantically correct.
* Baseline 194, final 362 browser checks, units 8 to 11 and 19 Core manifest tests remain producer observations. Root did not rerun the browser, axe or assistive technology. No browser mutation negative control is claimed.
* Provenance: candidate-first source setup and served JS hashes were observed; the earlier independent provenance qualification stays, with an additive Root partial resolution. It is not a retroactive full host attestation, and not every namespace path belongs to the 233 worktree.

## Scope limits

* Metadata only. No src (including README), fixture, helper, test, app, dependency, Core, role or recipe change. Do not fix the assertion or tests. Numeric correction balance UNKNOWN; no repair or new allowance is granted.
* Original records, state, logs, self-review and the first design-version-2 overlay adverse record stay immutable.

## Follow-ups (ranked)

1. Human-owned decision on issue #1362 (exact-field current design version assertion plus a negative control), under finite authority that Root must reconcile first.
2. Independent review of this metadata record.
