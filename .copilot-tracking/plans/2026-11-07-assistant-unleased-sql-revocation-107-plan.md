---
title: Plan for unleased SQL revocation coverage (#107)
description: One focused test mixin, run on SQLite as a proxy and on disposable SQL when admitted
ms.date: 2026-11-07
---

Research: [research](../research/2026-11-07-assistant-unleased-sql-revocation-107-research.md). Details: [details](../details/2026-11-07-assistant-unleased-sql-revocation-107-details.md). Critique: [critique](2026-11-07-assistant-unleased-sql-revocation-107-critique.md).

## Decisions

* Tests only in `src/api/tests/test_assistant_release.py`; no production, schema, approval or attestation change.
* Keep the broader C10 bundle, approver, serving attestation and attribution gaps unticked.
* No SQL, browser, scanner, image, provider, Azure, lock or FULL run now; no push, PR, tick or cleanup.

## Phases

* [ ] Phase 1: add the mixin, a SQLite proxy class and a `ZF_TEST_MSSQL`-gated MSSQL class.
* [ ] Phase 2: run SQLite and static checks with own-source packages; record skips.
* [ ] Phase 3: author Review, commit and freeze; hand off the SQL selector.
