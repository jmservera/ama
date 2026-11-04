---
title: Details for #74 home case browser evidence slice
ms.date: 2026-11-04
---

* Phase 1: synthetic data from `building_fixture` plus one dependency and one hold; staff user pam@example.test opens `#/case-home/ZF-2`. Asserts labelled home and building regions, building items only in the building panel, sibling ZF-3 evidence absent, version status and notice, manual links, no write controls, one h1 and four h2, 320 px and 1280 px reflow, optional axe 4.10.3, no non-safe requests, no script errors.
* Phase 2: `app.js` shows "This home's share of shared cost {id}: GBP {amount}. Source: {source}".
* Phase 3: `src/api/README.md` Versioned home case section.
