---
title: Issue 96 served Held draft download consumer changes
description: Changes record for the initial served HTTP and Funding-screen consumer of the existing Held export
ms.date: 2026-11-10
---

## Status

Implementation complete on branch `feat/demo-held-form-download-96-1110` (base fe59ef56). Refs #96 only.
The original stub persisted before implement-start is kept at the external evidence run folder.

## Changes

* `src/api/src/zava_forward/api/server.py`: imports the existing `form_export`; adds `held_download_enabled` (default OFF; needs `ZF_FORM_HELD_DOWNLOAD=synthetic-demo-only` and `ZF_DEPLOYMENT_PROFILE=demo`, never `trusted-proxy`, read per request); exact GET route `/api/cases/{id}/form-review/{draft}/held-export` delegating to `form_export.draft_export` on every request; 404 when OFF, 409 JSON with no attachment when not Held; 200 attachment `held-form-draft-export.json`, `private, no-store`; view flag `held_download_enabled` only when ON.
* `src/api/src/zava_forward/api/web/role-screens.js`: `fundingDraftPanel(draft, caseId, downloadEnabled)` renders a native anchor "Download Held draft (unreviewed)" only for an enabled, available draft with an id, plus Not submitted / eligibility Not assessed / snapshot-version note.
* `src/api/tests/test_form_held_download_api.py` (new, 5 tests), `test_finance_grants_screens.py` (+1), `test_role_endpoint_inventory.py` (explicit route entry + coverage test).
* `src/api/checks/held_form_download_browser_check.py` (new): private synthetic fixture, loopback server, keyboard download, history/hash/notices, no non-safe page requests, stale-snapshot semantics, 360 px fit, denied roles.
* `src/api/README.md`: route, default-OFF switches, attestation limit.

## Amendments and divergences

* No existing demo guard fit (the chat guard is chat-specific); a minimal default-OFF switch was added as planned.
* Core exporter/history/dependency, schema, SQL, auth, Bicep and shared fixtures untouched.

## Validation (raw logs external, exit codes direct)

* API: held download 5, finance grants screens 20, endpoint inventory 24, form staging API 14, role screens conformance 11: all OK.
* Core unchanged reruns: export, dependencies, review, staging: all OK.
* `node --check role-screens.js`, `ruff check src tests checks`, `mypy src` + new checker, `git diff --check`: pass.
* Browser checker under non-queued `flock -n /tmp/ama-rpi-heavy.lock`: exit 0, all PASS. No axe scan, no AT or WCAG acceptance.
* Not run: SQL Server, blanket full gate, `--changed` gate, other browser checkers, hosted CI.
* Pre-existing files are not ruff-format clean; only new files were formatted.

## Scoped web review (Web Interface Guidelines, fetched 2026-11-10)

* `role-screens.js:1297` native anchor with `download`, text label states action and "(unreviewed)": pass.
* `role-screens.js:1297` link has visible text, no icon-only control; focus uses existing `.btn` styles: pass.
* `role-screens.js:1296-1298` status note follows the link in plain language; no autoplay or automatic download: pass.
* `role-screens.js:1297` long href template line matches the file's existing style: no finding.
* No new colour-only signal, motion, or form controls. 360 px fit checked by the browser checker only; no axe, no AT.
