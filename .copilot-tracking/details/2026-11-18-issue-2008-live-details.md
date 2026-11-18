---
title: Issue 2008 phase details
ms.date: 2026-11-18
---

* Workbook sheets: `Cases` (declared structure; headers use aliases Ref, Property address, Post code, Workflow stage, plus unmapped Resident name and Notes) and `About this demo`.
* Rows: clean rows; rows with empty address, wrong postcode, empty stage; one duplicate reference pair (blocking conflict).
* Web surface is CSV only (`/api/import-check`), so live proof uses the CSV saved from `Cases`; xlsx conflicts are proven by the local CLI preview only. State this honestly.
* Evidence outside the tree: raw outputs and screenshots go under the docs research folder (small PNGs), ids redacted; no state JSON overwritten.
