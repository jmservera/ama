---
title: Issue 107 live r12 plan
ms.date: 2026-11-25
---

## Plan

* [x] Phase 1: live read-only probes (revision, authenticated registry, release denial, delivery gate) recorded under `.copilot-tracking/evidence/107-live/`.
* [ ] Phase 2: extend `assistant_process_worker.py` with `provider`, `endpoint`, `deployment` variations; add three separate-process tests reusing `check_process_wide_binding`.
* [ ] Phase 3: run SQLite and disposable SQL Server runs, ruff, mypy; record per-criterion table in the changes record and a research note.

Tier: FULL (test code under `src/api`); `rpi-checks.py --all` is never run by the worker.

## Critique (executed once)

Verdict: accept. Findings: (1) the new tests must fail without the worker change (mutation check); (2) endpoint/deployment are provider attributes, so the variation must be applied after provider creation; (3) live probes are read-only and must not print sign-in values; (4) a revision change observed mid-probe belongs to another worker and must be recorded, not acted on. All compatible; applied directly. Delivered-build criterion stays unproven: creating an approved release needs a named approver (OQ-017).
