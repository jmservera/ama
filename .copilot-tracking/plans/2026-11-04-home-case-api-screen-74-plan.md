---
title: Plan for #74 home case API and screen slice
ms.date: 2026-11-04
---

* [x] Phase 1: route GET home-case and POST home-case-version in the API (details: ../details/2026-11-04-home-case-api-screen-74-details.md).
* [x] Phase 2: read-only `#/case-home/{id}` screen linked from the case page, with fail-closed message pointing to existing screens.
* [x] Phase 3: loopback tests (auth, separation, 404, 409, 400, retention) and README section.
* Stacked follow-ups: version-recording form, browser check, building record versioning, hosted evidence.
* Critique: one pass, self-run. Compatible findings applied: staff-only reuse of core checks, no new approval authority, no early rule check on POST.
