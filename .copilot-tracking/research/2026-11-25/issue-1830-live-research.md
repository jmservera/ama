---
title: Issue 1830 live r14 research (2026-11-25)
ms.date: 2026-11-25
---

Opening state. Prior rounds r1 to r13 exist under `.copilot-tracking/`. Research disposition: executed (re-proof at head). Findings follow below.

## Findings (r14, head c67289436e, load 10 to 19)

* `rpi-checks.py --preflight api:test_production_config_a11y_check` passes with the development-feedback label; `api:test_does_not_exist` and `../etc/passwd` are BLOCKED; 62 timing and preflight tests OK.
* Direct #1828 map check (`checks/map_fullscreen_browser_check.py`, pinned axe sha256 prefix 880970c081707360, run with the runner's PYTHONPATH) is intermittently red: 2 of 3 first runs failed with `filter label and focus fit at 390x568`; later 4 of 4 sequential runs passed; in 3 batches of parallel instrumented runs (12 + 18) the failures were axe `target-size` on `.map-marker` 1 and 2 in state `expanded-320` (partially obscured 28x20 px; neighbours 12 px apart).
* Cause reading: the `expanded-{width}` loop resizes the viewport, then scans after only a marker count check. Leaflet's debounced 200 ms resize read and marker re-layout can still be in flight, so markers overlap transiently. The file already has `settle_map_reads` for exactly this and does not use it here.
* Other criteria unchanged from r13 (retained receipts, queue-wait logs and a same-head pair are not available; independent review and hosted CI need a PR, forbidden).
