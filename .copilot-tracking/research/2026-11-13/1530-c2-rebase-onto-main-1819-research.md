---
title: 1530 c2 rebase onto main research
ms.date: 2026-11-13
---

## Scope

Rebase PR #1542 (`feat/demo-case-safety-usability-1530`, head `5eaf0959d`) onto `origin/main` `2c71e2c2173388ef219361376c37c3d0a853e354`. Merge base is `ca7803e85`. No push, no issue edits.

## Evidence

* Branch has two commits above the merge base (`fbe1ed26f`, `5eaf0959d`).
* Likely conflict files: `scenario-manifest.json`, `cutover-reference-inventory.tsv`, `docs/reference/log.md`.
* Preserve main's digests; recompute the recipe SHA-256 for `case_view_ux_browser_check.py` and regenerate the inventory with `zava_forward.core.synthetic.cutover_audit`.
* Optional polish: open `.safety-details` and `.safety-optional` disclosures before the axe scan of the populated safety panel (from the c1 closure review).

Research disposition: executed. Planning Readiness: Ready.
