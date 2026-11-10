---
title: Issue 96 served Held draft download consumer review
description: Single author post-implementation review of the initial served Held download consumer
ms.date: 2026-11-10
---

## Execution and outcome

* Review executed once, by the implementing author (no nested agent). Independent exact-head assessment is still required before publication.
* Outcome: Conformant for the planned scope, with open qualifications below. Assessed boundary: uncommitted diff against fe59ef56 plus the original RPI artifacts.

## Findings

* Route delegates to the unchanged `form_export.draft_export` on every request; test asserts body, hash and history equal the core result. Repeated GET leaves the store unchanged. Evidence: `test_form_held_download_api.py`, browser checker exit 0.
* Rights are re-checked per request: unauthenticated 401; contractor, finance viewers and revoked roles refused; cross-case, unknown, malformed, extra-segment and POST give no attachment. Default OFF and each switch alone give 404.
* UI renders the link only for an enabled, available draft; no automatic download; later download is current (version 3 vs 2 shown), with a visible version/hash note.
* Core, schema, SQL, auth, Bicep, shared fixtures and #153/#130/#131 tests are untouched.

## Open items routed to later work

* Qualification: `ZF_FORM_HELD_DOWNLOAD` is an operator attestation; the store has no synthetic-provenance marker, so the code cannot prove data is synthetic. A provenance marker would need a separate scoped approval.
* Not run: SQL Server, hosted CI, axe, assistive-technology testing, blanket gates. Browser checker is not wired into CI.
* Real templates, real data export and operational submission remain unapproved. No human, legal or Finance approval is implied.
* Closure of #96 is not claimed (Refs only).

## Follow-ups

1. Wire the browser checker into an owned CI step (ease high, value medium).
2. Add a synthetic-provenance marker to the store (value high, needs approval).
3. Run axe and AT checks on the Funding screen with the pinned `ZF_AXE_JS`.
