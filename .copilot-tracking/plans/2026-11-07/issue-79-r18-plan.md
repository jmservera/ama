---
title: Issue 79 plan, correction cycle 1 for the 357e842d assessment
ms.date: 2026-11-07
---

Task `issue-79-r18-357-assessment-corrections`. Planning readiness: ready. Critique: one prospective self-critique below, executed before any test or source change.

## Executive summary

Fix three Medium runner findings with the smallest behavior-preserving changes in `ranking_publication_runner.py`, with regressions in the existing runner test file and one README sentence. Light checks only.

## User decisions and requirements

* Direct run callers cannot bypass policy key, version and content hash validation; structured refusal.
* A future archived publication date is an invalid schedule state in verify and schedule and guards non-exercise publish; exercise stays no-write; historical records unchanged.
* A blocked schedule exits nonzero with the JSON refusal preserved; successful exits unchanged.
* No change to approvals, thresholds, consent, registry authority, archive names or bytes, infrastructure, helper or child. No FULL, push, rebase or acceptance ticks.

## Phases

* Phase 1: research, plan and details committed before tests or source.
* Phase 2: add regressions, run them and record RED.
* Phase 3: implement the three corrections; run the focused tests, Ruff, format and mypy with pinned tools; record GREEN.
* Phase 4: Changes, state, author Review, README and log entry, commit.

## Acceptance criteria

* A signed policy modified without recomputing its hash is refused with `policy_invalid` for publish, schedule and exercise; no archive write.
* A future-dated record beside an older legitimate one gives verify and schedule status `problem` with a future-date problem and null due/overdue; publish refuses `archive_date_future` and writes nothing; exercise returns `exercise` without writing; earlier-dated records still report current.
* CLI `schedule` with the unsigned shipped policy and with an unknown policy exits 2 with JSON status `blocked`; due/current exits stay 0.
* Existing tests still pass; Ruff, format, mypy clean; ignored-inclusive clean worktree.

## Self-critique

* Risk: refusing a bad registry for exercise could hide an unsigned exercise. Acceptable: a hash mismatch is registry corruption, not an approval question, and exercise still needs a trustworthy policy to be meaningful.
* Risk: exiting 2 for blocked changes a scheduler's observed code for the shipped unsigned policy. That is the intended finding; the README is updated and the JSON is unchanged.
* Risk: marking future dates null for due could look like losing `latest`. Mitigation: `latest` stays visible.
* Rejected: tolerances for clock skew (invented policy), helper changes (child lane), broad exception catches.

## Follow-up items

* Coordinator: merge this parent ancestry into the corrected child, then a new combined FULL, independent exact-head assessments and hosted checks.
* Helper-level future-date validation remains a possible child question.
