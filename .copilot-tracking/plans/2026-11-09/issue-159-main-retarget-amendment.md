<!-- markdownlint-disable-file -->
---
title: Issue 159 main retarget amendment (research, plan, details)
description: Prospective amendment before merging main into the child and re-running selected checks
ms.date: 2026-11-09
---

## Research

* Parent #189 merged via #1313 at 17:35:18Z; main squash `0dc4dd35ce9ea6bddd1d4ca34d5f8ec6e234adfe`, fetched `origin/main` equals it. The child is not a required #189 acceptance dependency.
* Static check before merge: `git diff HEAD origin/main -- src` shows only the removal of this child's own 113 lines (4 files), so main's source for those paths equals the pre-feature parent state. No unexpected overlap is predicted; this is proven again after the merge by comparing the merged tree's source with `de79f4b8b`.
* Independent Functional review of `de79f4b8b` at 16 paths: approve, zero findings (functional-findings.json). Original source, tests, critique, review and adverse records stay immutable.
* Evidence gap: the earlier final standalone Core Ruff logs keep intermediate failures and no later successful raw output is visible.

## Plan

* Eventual PR targets main with Refs #159 and Refs #189 (coordinator re-evaluation); the old parent-topic target is superseded.
* Step 1 commit this amendment. Step 2 fetch main and ordinary `--no-ff` merge it; no rebase, amend, force or rewrite. Stop on unexpected source overlap.
* Step 3 re-run on the composed source in fresh, non-overwriting files: Ruff 0.17.1 `check .` and `format --check .` for Core and API; mypy 2.4.0 for Core and API; the earlier focused Core chat and regulatory and API chat, regulatory, role-inventory and resident selections. The opt-in local Chromium skip stays explicit.
* Step 4 append dated changes, Review and target disposition; update state; handoff.

## Details and limits

* No source, fixture, config or ignore edits to pass checks; any relevant failure is reported and stops for a bounded coordinator disposition. No new corrective cycle (history stays 1 confirmed, 1 possible, true total unknown). No browser, SQL Server, full gate, services, cloud, models or private data. Owned venv only because none exists (previous one removed); install only declared dev dependencies.
