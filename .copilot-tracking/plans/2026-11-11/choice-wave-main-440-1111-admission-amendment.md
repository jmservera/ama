---
title: Resident-choice CSV feature-wave checkpoint admission amendment (Refs #440)
description: Additive execution admission with actual merged main e09b21f1d and Root's assessment conditions; written before any test
ms.date: 2026-11-11
---

## Status

Additive. The original research, plan, details, single critique (conformant after CW-01 to CW-06, all applied by the author) and state stay unaltered. No second critique was run and nothing here claims retrospective planning. Written and committed before the merge of main and before any test.

## Actual facts supplied by Root and re-read here

* PR 1435 squash-merged 2026-11-11T02:40:30Z as `e09b21f1d7effb6f5a4bfff8315db99bf59c2372`, tree `9a52f75ea5bc4ac39f0e7f468c45ed2301e931a6`. Fresh `origin/main` equals it. Parent chain from planning pin `1b169fe7d` is this one commit.
* `src` tree `87ea0ed8db9f180aec258eed42ca6232a7c97b6a` equals the reviewed candidate. `docs` `9a33d247`, `infra` `f7f31c09`, `tools` `432a4e8f` and `.github` `8ee22819` equal the planning pin (read by `git rev-parse`; `git diff` of those four trees is empty). The only non-tracking paths changed since the pin are under `src/api`.
* Root's gate: 19 hosted PR checks SUCCESS, MERGEABLE, independent approve on `1febb4b`. Issue #1420 CLOSED. Whole #80, #73 and #440 stay OPEN. Closure grants no production, real-data, privacy, retention, resident, human or assistive-technology approval.
* New main scorer run 42947632230 was in progress at Root's observation. Main CI for this commit is pending or unobserved: it is not claimed as passed. Root explicitly permits focused local observations on the source-equal merged pin meanwhile; a relevant failure stops affected acceptance only.

## Execution conditions (from Root's assessment and instruction)

* Ordinary no-ff merge of pinned `e09b21f1d` only; no rebase, force push or guessed merge. Stop on conflict or source mismatch. If `origin/main` advances, record it separately and keep the pin. Before observations `src`, `docs`, `infra`, `tools` and `.github` must equal the admitted main; only own tracking files differ.
* Admitted: C7, C1 to C6, I1 (static 107 plus 4 = 111, re-derived from actual source, divergences recorded) and one fresh story 232 browser run (B1). Omitted: whole Capacity, importer suite, SQL, Docker, `test_case_journey`, story 232s, full gate. No source, fixture, role, schema, workflow, manifest or test edit.
* Owned private HOME only (never the real HOME), private TMPDIR, cache, browser profile and scratch outside the checkout; existing matching Chromium cache linked read-only if needed. No `.env`, private or default data.
* Install only needed `src` distributions into a task-private venv, and only after actual missing import evidence; importer is not installed unless a selector needs it. Preserve preflight and install adverse evidence. Module origins must be under this worktree; the same Python and Playwright that B1 uses is preflighted before locking.
* B1: exactly one `flock -n -E 99`, `timeout 900`, no nesting; pinned axe hash, existing matching Chromium, memory headroom and a free lock required, else blocked and recorded.
* A missing CSV module on main blocks that surface and acceptance; not-run does not satisfy the checkpoint.
* No retry-to-green; after a failure only independent admitted selectors continue.
* Trace stays document-qualified, draft, in-review and proposed as read; the update-owner link is weak and partial. Co-observed inventory cases prove no new combined journey and not whole #132, #80, #73 or #440. Candidate evidence stays candidate history; fresh results are local synthetic only.
