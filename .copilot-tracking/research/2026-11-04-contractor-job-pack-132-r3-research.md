---
title: Issue 132 round 3 research
ms.date: 2026-11-04
---

Research disposition: executed (narrow). Planning Readiness: Ready.

* Merged for #132: PR 873 (core rules) and PR 1080 (staff-only read-only job-pack route). Nothing else merged.
* Unmet: persistence, write routes and staff screen (criteria 2 to 5); accessibility proof (criterion 1); owner decision and #116 identity (criterion 6).
* The #132 readiness comment asks for an owner waiver to separate a staff-only slice from #116; it is unanswered. Persistence runs through manager-only, authority-bound transactional store operations with a SQL variant, so a write slice is security, SQL and persistence sensitive and needs the complete gate plus the waiver.
* Smallest coherent slice available without the owner: a proposed decision record for criterion 6 (docs only).
