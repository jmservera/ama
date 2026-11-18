---
title: Issue 117 live audit r2 changes
description: Changes and per-criterion result for the second live audit of #117
ms.date: 2026-11-18
---

Tier: FOCUSED, docs and evidence only. No `src` change, so mypy and ruff do not apply; `rpi-checks.py --all` was not run.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Uploads are scanned before availability | Proven: source order, offline tests (64 pass), live refusal of marker and type-mismatch uploads on the demo (synthetic local scanner), no record created. Unproven: real malware engine through the app (`ZF_SCANNER` unset; setting it is a live app change not taken); clean upload live; Defender live scan of a blob (firewall Deny on demo account; throwaway account lacked `datascanners/write`) | [audit note](../../../docs/reference/research/issue-117-live-r2-audit-2026-11-18.md) |
| Retention job, owner approval, legal hold (already ticked) | Not re-audited; endpoint 200, placeholder label, offline tests pass | same |
| Production-only | DPO and Legal approved periods; immutability lock | excluded |

## Files

* Added `docs/reference/research/issue-117-live-r2-audit-2026-11-18.md` and `issue-117-live-r2-raw/`.
* Edited `docs/reference/README.md` (index) and appended to `docs/reference/log.md`.
* Added `.copilot-tracking/evidence/2026-11-18/issue-117-live-r2/` (probe and output) and the RPI artifacts.

## Azure

Throwaway storage account `<throwaway-storage-account>` created and deleted in `ama`; role assignment went with it. Nothing else changed. Correction to the first note: Defender malware scanning on the demo account is enabled.

## Divergences

None from the plan.
