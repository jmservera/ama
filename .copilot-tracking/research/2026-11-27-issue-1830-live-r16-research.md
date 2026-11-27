---
title: Issue 1830 live r16 research (2026-11-27)
ms.date: 2026-11-27
---

Task: find an angle r2 to r15 did not cover for #1830 criterion 2 (preflight must reject invalid input and label results as non-receipt feedback). Disposition: `executed`. Planning readiness: Ready. Synthetic demo, desktop only; no live Azure, no secrets, no push.

Angle: argument handling of `rpi-checks.py --preflight` when combined with other gate options.

Reproduction at head `b64c6e95dd` (before any edit):

* `--preflight api:test_production_config_a11y_check --extra-test api:test_production_config_a11y_check.ProductionConfigA11yCheck.test_nope` exits 0, "Ran 3 tests", "Preflight passed for 1 selector(s)". The bogus extra selector is neither validated nor run.
* `--preflight S --extra-test S` also passes silently; the user may believe two checks ran.
* `--base`, `--out`, `--jobs`, `--stack` are likewise accepted and ignored in preflight mode (code: `main()` branches on `args.preflight` before reading them).

Defect: fail-open argument handling in a path whose purpose is to refuse invalid input. Fix direction: reject every gate-only option under `--preflight`.
