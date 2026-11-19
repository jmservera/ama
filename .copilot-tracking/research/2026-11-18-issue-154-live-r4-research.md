---
title: Research for #154 live round 4 (first unmet demo criterion)
ms.date: 2026-11-18
---

## Disposition

Executed. Rounds 1 to 3 (`2026-11-18-issue-154-live-*`, `docs/reference/research/issue-154-live-resident-ux-*`) proved criterion 5a and left criterion 3 (representative views) unproven live: no demo case has a representative.

## Finding

The code path for a representative session exists (`resident_showcase.RepresentativeShowcaseGrant`, `ResidentDemo(representative_grants=...)`) and is unit-tested, but the deployable entrypoint `src/api/src/zava_forward/api/resident_demo/__main__.py` never passes grants, and `ShowcaseReader` has no `list_representative_grants`. A deployed demo can therefore never show a representative view. This is the first unmet demo-scope criterion that needs code.

## Planning Readiness

Ready. Plan: optional synthetic grants file named by `ZF_DEMO_REP_GRANTS_PATH`, parsed fail-closed into `RepresentativeShowcaseGrant`, wired in `main()`, covered by focused tests. Criterion 5b (usability programme) is not demo scope.
