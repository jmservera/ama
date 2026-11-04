# Plan: admin-only case-data routes (Refs #920)

* Phase 1: in `route()`, when `services.cases === false`, show the existing plain-language page for every route except #/assistants, #/import and #/screens (contractor handling first).
* Phase 2: extend the Chromium check over 11 case-data routes (no case-data requests, no 4xx, no console errors); pin server 403s in unit test.
* Phase 3: focused validation, review, PR (Refs #920).

Critique: executed once, self-review; compatible. Details: [details](../details/2026-11-04-admin-routes-denial-920-details.md).
