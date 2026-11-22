---
title: Issue 1258 live research r2
ms.date: 2026-11-22
---

Research disposition: executed (reuses prior notes as inputs; new checks below). Planning Readiness: Ready.

* Main check: `git fetch origin main`; origin/main and HEAD are both 10cad2e413. No diff in `src/core` between them.
* Issue 1258 is open; only AC5 is unticked (original RPI, current FULL receipt/verification, independent exact-head review, hosted checks). Last owner comment (2026-11-18) ticked AC1-AC4 with mocked proof.
* Prior notes: `docs/reference/research/ranking-archive-ancestor-durability-evidence-2026-11-22.md` and the r2-r6 live notes.
* Constraints: no push or PR, so hosted checks cannot run; `rpi-checks.py --all` is forbidden; no src change so tier is focused.
* Plan: rerun the core publication tests at this head, run an strace-backed real first-publication into a nested temp archive to show fsync ordering, record a per-criterion table.
