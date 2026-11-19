---
title: Issue 2008 research, synthetic demo workbook for the import
description: Research record for the synthetic Excel demo workbook (Refs #2008, #80)
ms.date: 2026-11-18
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Findings so far

* The importer library (`src/importer`, #80) has a declared `case-list` structure (sheet `Cases`; fields reference, address, postcode, stage; optional status, owner), alias column matching, conflict detection (missing required column, several columns matching, duplicate reference) and a row-level preview. CLI: `python -m zava_forward.importer preview FILE`.
* The deployed demo web surface does not read .xlsx. `importView` in `src/api/src/zava_forward/api/web/app.js` accepts CSV only and posts text to `/api/import-check`, which maps name/address/postcode/phone, lists rows to fix and counts matches to existing homes; it reports no duplicate-key conflicts. The README states the xlsx web surface is not built.
* Consequence: the workbook can be previewed in full (mapping, conflicts, row preview) only by the local CLI; the deployed demo can be exercised with a CSV saved from the workbook's Cases sheet. No src change is in scope (focused tier).

## Plan hooks

* Generator under `src/importer` (tools or module), using the existing `write_workbook`; workbook committed under docs fixtures; test outside the package.
* Live proof with Playwright on the deployed API app, credentials read at runtime and never printed.
