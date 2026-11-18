---
title: Issue 117 live changes
description: Changes record and per-criterion table for the issue 117 live evidence run
ms.date: 2026-11-18
---

Tier FOCUSED, documentation and evidence only; no `src` change, so no mypy, ruff or full gate applies. Refs #117.

## Changes

* Added `docs/reference/research/issue-117-live-scan-evidence-2026-11-18.md` and raw output under `docs/reference/research/issue-117-raw/`.
* Updated `docs/reference/README.md` and `docs/reference/log.md`.
* Added the probe script and redacted result under `.copilot-tracking/evidence/2026-11-18/issue-117-live/`.
* No Azure resource created or changed (nothing to delete). The two refused live uploads were not recorded.

## Validation

* api `test_document_controls`: 18 OK. core `test_document_rescan`, `test_resident_documents`: 46 OK (20 skipped).
* Live probe: marker upload 400, mismatch upload 400, document count 5 to 5.
* Link and diff review of changed docs. Hosted CI is not observed (no push).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Uploads are scanned before availability | Proven for the demo's synthetic local scanner (offline and live refusal). Unproven for a real engine: Defender for Storage is disabled |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion (ticked) | Not re-audited; live queue reachable, offline tests pass; live approval and hold not exercised |

## Divergences

* Two earlier live probe runs failed (empty 403 out-of-page POST; 400 missing provenance fields); outputs not retained.
