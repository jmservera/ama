---
title: Issue 152 supported devices and widths research
description: Evidence for the remaining open acceptance criteria of #152
ms.date: 2026-11-01
---

## Disposition

Research executed 2026-11-01. Task slug `issue-152-supported-devices`.

## Findings

* Issue comments (closure audit 2026-10-31) record AC 2 to 4 as engineering-proven
  by #317 and #401. AC 1 (owner decision on devices) and AC 5 (complete
  AC-034/AC-043 profile acceptance) are unmet.
* `src/api/checks/workbench-manifest.json` already pins widths 320, 390, 768,
  1024, 1280, eleven profiles and nine workflows (partial or deferred), and
  lists `Supported devices/browsers` under `unknowns`.
  `src/api/tests/test_workbench.py` pins widths and profile structure.
* The PRD lists OQ-004 and OQ-011 (device and assistive-tool contexts) as open;
  the WCAG baseline names 320, 390, 1280 CSS px, 200 percent text, 400 percent zoom.
* No document records a device decision proposal for the owner to ratify.

## Constraints

* Only the owner can decide supported devices; an agent may propose and must
  not mark the decision made. AC 1 and AC 5 cannot be closed by this work.
* Source in `src/`, tests outside the package, no `mvp/` changes.

## Planning readiness

Ready. Slice: a proposal for owner ratification (`docs/reference/research/ux/supported-devices-proposal.md`),
a `supported_devices` block in the manifest with status `proposed`, and a test
pinning the block to the engineering widths and keeping the decision unratified.
