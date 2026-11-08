---
title: Issue 149 parent main e2ec integration research
ms.date: 2026-11-08
---

## Evidence

Parent f8c1be6c (tree d4b8d2b9) has merge-base b284d0d3 with fetched main e2ecee25. Main moved 480 files (15684 insertions): tracking records, rubric scores, and substantive source, tools and workflow changes, including `src/api/.../server.py`, `src/core/.../store.py`, `ranking_publication*.py`, SQL and sensor checks, `tools/rpi-checks.py`, `tools/ci-affected.py` and `.github/workflows/src-ci.yml`. The parent delta relative to main is only the operator and atlas checker, tests, UX docs, records and log entries. Overlap risk is mainly `docs/reference/log.md` and `docs/reference/README.md` (both append or index edits) and `src/api/README.md`. The third diagnostic's date qualifications and the retained b470 Pass 0 (parent increment, 480-line movement) stand; this is integration, not a fourth diagnostic.

Planning readiness: Ready.
