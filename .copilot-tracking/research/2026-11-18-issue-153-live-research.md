# Research: issue 153 live plain-language audit (2026-11-18)

Task: issue-153-live. Disposition: executed. Planning readiness: Ready.

## Evidence

* Live apps: ca-cutover-test-demo-api (rev 0000031), ca-resident-demo (rev 0000012); sign-in scripted at runtime.
* Staff SPA: 13 nav views scanned; banned terms absent; snake_case path in queue Source lines (app.js:841).
* AI label "AI suggestion, not approved. Not an instruction." present on Assistant proposals.
* Errors: 404 "Case not found."; 403 "Your role does not include this." (reason only).
* Resident page clean of banned terms; two unexplained abbreviations (dMEV, EPC).
* Incident: a shape-check command printed the credential files to the session log; no repo file holds them.
* Findings and per-criterion table: docs/reference/research/plain-language-live-153-2026-11-18.md.

Scope: docs/evidence only. Audit workbench copy (status names, errors, AI labels) on the live synthetic demo
against docs/reference/research/ux/content-standard.md. Only unticked criterion: "Resident-facing wording is
reviewed by a named human before any use".
Owner decisions 2026-11-18: demo, desktop only, live Azure authorised (rg ama), no DPO/Legal or person-run AT.
