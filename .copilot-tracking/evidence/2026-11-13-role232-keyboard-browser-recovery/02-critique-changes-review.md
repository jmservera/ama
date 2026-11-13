---
title: "#232 axe recovery: critique, changes and Review (2026-11-13)"
ms.date: 2026-11-13
---

## Critique (independent, before execution): Proceed with changes

Applied: qualify provenance as possibly mixed-source (server import origins unobserved), hash the design-system
document (done, hashes.txt), verify no leftover server or browser process after each selector (leftover-*.txt, 0 lines).

## Changes (validation only)

No source change. Each selector ran in a non-queued `flock -n` lock plus `systemd-run --user --scope`
(MemoryMax=2G, MemorySwapMax=0); the scope's memory.max 2147483648 and swap.max 0 were printed before the browser
command (run-*.out line 1). Both direct exits 0, stderr empty, no FAIL. Axe 4.10.3 (sha 880970c0...8a68bb) passed on
`main`: no violations, no incompletes, both selectors. Chromium 156.0.8078.4. Fresh guidelines fetch HTTP 200, same sha as before.

## Review (independent, read actual outputs): Partial

* Ancestor cgroup limits were not recorded, so "effective" limits are scope-level only.
* "Once each" is not independently proven beyond the retained outputs.
* Import probe is separate from the server; foreign editable path fallback remains.
* Tab reach at 1280 px only; 232s text assertion covers heading/panel only.

Frozen, not corrected. Not WCAG, AT, named-human or whole-issue acceptance. Original attempt files are unchanged.
