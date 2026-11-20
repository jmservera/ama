---
title: Issue 203 guard live research
ms.date: 2026-11-19
---

Disposition: executed. Planning Readiness: Ready. Demo, desktop only, no Azure action.

Findings: `python3 tools/check-legacy-references.py` exits 1 with 3 violations in `docs/reference/research/2026-11-19-issue-202-mvp-workflow-retirement.md` (lines 11, 25, 29: retired path without archive tag). `python3 -m unittest tools.test_check_legacy_references` fails `test_repository_has_no_violations`. Cause: `RECORD_PATTERN` only exempts dated live notes named `issue-N-...-DATE`; the new note is named `DATE-issue-N-...`. Criterion 1 had been proven earlier and has regressed on this head.

Remaining unticked criterion 5 (deployed app and CI green) needs digest provenance and a `main` push CI run, previously recorded as unproven; unchanged.
