---
title: Issue 1830 live r17 research (2026-11-27)
ms.date: 2026-11-27
---

Research disposition: executed. Scope: synthetic demo, no live Azure, no secrets. Angle: new defects in `tools/rpi-gate-timing.py` input handling (r16 covered `--preflight` options). Findings are added below as probes run.

## Findings

* Probe: synthetic schema 4 full receipts (valid sha256 binding, in /tmp, deleted afterwards) with one field removed each. `rpi-gate-timing.py report` ends in an uncaught `KeyError` traceback for a missing `jobs`, missing `image_cache`, and missing `sealed` (with `--log`). Other malformed inputs already give a clean `TimingError` exit 2 (r13, r14 work). `compare` indexes `r["sealed"]` the same way.
* Defect: hash-valid receipts lacking those fields bypass the fail-closed input checks of `load_receipt`.
* Planning readiness: Ready. Fix in `load_receipt`: require `jobs` int, `image_cache` str and an aware ISO `sealed`, each as `TimingError(EXIT_INPUT)`.
* Criteria 1, 3 and 4 gaps are unchanged from r16: retained `/tmp` receipts are gone, no gate optimisation exists, review and CI need a PR. Criterion 2 remains proven.
