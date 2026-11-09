---
title: Issue 1259 frozen parent c5 integration plan
description: Prospective plan to merge exact frozen parent 52f9b61bb into the path-health child and adapt health semantics to the Blob contract
ms.date: 2026-11-09
---

## Objective and boundary

Locally merge exact parent commit `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` into `fix/ranking-archive-path-health` (ordinary non-fast-forward merge, no rebase, reset, force, amend of earlier commits, push, PR, issue or board change). Reconcile `ranking_publication.py` by intent. Verify, with failing-first tests where a gap exists, that the configured Blob operational archive never reports unknown or unreadable as healthy-empty, that diagnostics are path-free, and that the runner refuses to PUT when the listing is unreadable, while valid-empty and pagination stay correct and direct conditional create never lists. Local filesystem code stays fixture support. Refs #1259 only; nothing closes.

## Ordering

This plan, its details and the single critique are committed before any merge or source edit. The preparation record's own ordering divergence is not restated as fixed.

## Tier

DEMO targeted and impacted tests and lint/type on changed files (owner decision for this demo push). No `rpi-checks --all`, SQL, browser, emulator, cloud or scanners. Mocked REST is not Azure acceptance. Hosted checks, independent exact-head review and human approval remain.

## Cycle budget

Historical productive review-correction cycles: 0 (research record). This task consumes cycle 1 of 5; four remain.

## Phases

* [x] 1. Research (done, `...-parent-c5-research.md`).
* [x] 2. Plan, details, one critique (this file, details, critique); compatible findings applied.
* [ ] 3. Merge exact `52f9b61bb` locally with `--no-ff` and a prospective message; resolve the two conflicts by intent: keep both import sets (drop the child import if unused after resolution only when ruff proves it unused), merge the `verify` signature to `Archive` with a docstring that states both the Blob listing rule and the local-folder rule; keep both sides' tests in the runner test file. No other hand edits to parent files.
* [ ] 4. Failing-first probe: add Blob path-health matrix tests (below) and run them before any source edit; record the actual pass or fail of each. A test that passes on merged source is regression coverage, not a fix; do not add duplicate production code.
* [ ] 5. Source edit only for a probed failure (candidate: runner `_verify` reason text for fixed, path-free Blob error messages). Smallest change, no new policy.
* [ ] 6. Targeted tests, ruff check and format check on changed files, mypy on changed source, from this worktree via `PYTHONPATH`.
* [ ] 7. Changes record, one Review, state, commit, handoff.

## Test matrix (runner and archive level, mocked Blob transport)

* Listing statuses 403, 404, 500 and a transport raise whose message carries the SAS and account URL: schedule gives the unknown window (never due or current), verify gives a problem with `overdue` unknown, publish gives `archive_unreadable` with zero PUT and no blob; no output contains the account host, container, SAS or sentinel.
* Malformed and endless-pagination listings: same outcome.
* Valid empty `Blobs` and a multi-page listing: valid empty is a healthy first run (overdue true, count 0, no problems); pagination returns all names; publish works.
* Direct `ranking_publication.publish` conditional create with an unreadable listing configured: succeeds and issues no list request (no invented listing dependency).
* Critique PC-3: a first page that succeeds followed by a later page that fails gives `archive_unreadable` with no PUT; the Store/API publication route with an unreadable listing configured succeeds by conditional create with no list request.
* Critique PC-2: representative Blob errors surface through the runner with their fixed path-free text (HTTP status, storage unreachable, listing unreadable), not `reason not available`.
* Critique PC-1 (routed, not fixed here): scratch-only probe of a duplicated `NextMarker` in the frozen parent listing parser; no failing test is committed, the result is reported as a parent-owned follow-up with the exact policy choice.
* Local `Path` arm: the child's regular-file, dangling-link, absent-directory and stat-failure tests still pass after the merge (fixture support only).

## Stop rules

Stop productive edits if a selected test fails for a reason outside this scope, if the merge needs a material policy choice (record the exact choice), or if reconciliation would duplicate a parent fix. A failing selected test is not waived.

## Remaining criteria (not satisfied here)

Real Azurite or account run, container and role grant, WORM, Bicep, deployment, folder-record migration decision, FULL stack receipt on parent-current-main, independent exact-head review, hosted checks and human approval. All #1259 acceptance criteria stay literal and unticked; no AC is rewritten.
