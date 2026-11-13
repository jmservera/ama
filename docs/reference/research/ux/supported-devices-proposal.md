---
title: Zava Forward Workbench Supported Devices Proposal
description: Proposed supported device classes and CSS widths for owner ratification (issue 152, OQ-004 and OQ-011)
ms.date: 2026-11-13
ms.topic: reference
---

## Status

Decided by the owner on 2026-11-13 (Batch-2 Q1,
[#152](https://github.com/jmservera/ama/issues/152)): Desktop at 1280 CSS px,
Tablet at 768 CSS px and Mobile at 360 CSS px. Nothing here is validated by
direct user or device research, and it grants no conformance claim. Whether
field use is in scope for any role stays open under OQ-004 and OQ-011.

## Decision

| Class | CSS widths checked | Status | Basis |
| --- | --- | --- | --- |
| Desktop | 1280 | Supported (owner decision) | Primary staff workbench |
| Laptop | 1024 | Checked only, not a named tier | Kept from the earlier proposal |
| Tablet | 768 | Supported (owner decision) | Owner decision |
| Mobile | 360 | Supported (owner decision) | Owner decision |
| Large phone, reflow only | 390 | Reflow only | Kept from the earlier proposal |
| Narrow reflow | 320 | WCAG 1.4.10 reflow check only | PRD reflow width |

Widths come from `src/api/checks/workbench-manifest.json` and the browser
check in `src/api/checks/workbench_browser_check.py`. Browsers and assistive
tools are not decided; they remain the owner's call under OQ-011.

## Questions for the owner

* Name the supported browsers and assistive tools.
* Decide whether field use is in scope for any role.

## Unmet

AC-034 and AC-043 profile acceptance stays partial: eleven perspectives and
nine workflows are partial or deferred in the manifest, and human
accessibility acceptance is absent. The 360 width is added to the browser
check list but has not been run in this change.
