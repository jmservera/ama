---
title: Zava Forward Workbench Supported Devices Proposal
description: Proposed supported device classes and CSS widths for owner ratification (issue 152, OQ-004 and OQ-011)
ms.date: 2026-11-01
ms.topic: reference
---

## Status

Proposed, not decided. The owner is the decider
([#152](https://github.com/jmservera/ama/issues/152)). Nothing here is
validated by direct user or device research, and it grants no conformance
claim. Field and mobile use stays out of scope until OQ-004 and OQ-011 are
answered.

## Proposal

| Class | CSS widths checked | Status | Basis |
| --- | --- | --- | --- |
| Desktop | 1280 | Supported (proposed) | Primary staff workbench; checked at 1280 |
| Laptop | 1024 | Supported (proposed) | Checked at 1024 |
| Tablet | 768 | Supported (proposed) | Checked at 768 |
| Large phone, reflow only | 390 | Reflow only, not a supported field device | Checked at 390 |
| Narrow reflow | 320 | WCAG 1.4.10 reflow check only | Checked at 320 |

Widths come from `src/api/checks/workbench-manifest.json` and the browser
check in `src/api/checks/workbench_browser_check.py`. Browsers and assistive
tools are not decided; they remain the owner's call under OQ-011.

## Questions for the owner

* Confirm or change the supported classes above.
* Name the supported browsers and assistive tools.
* Decide whether field or mobile use is in scope for any role.

## Unmet

AC-034 and AC-043 profile acceptance stays partial: eleven perspectives and
nine workflows are partial or deferred in the manifest, and human
accessibility acceptance is absent.
