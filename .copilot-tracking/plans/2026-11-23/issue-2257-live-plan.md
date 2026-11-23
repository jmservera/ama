---
title: Issue 2257 live plan (run 084412Z)
ms.date: 2026-11-23
---

1. `src/api/src/zava_forward/api/web/app.js` `mapPanel`: add a hidden "Try the map again" button after the info line, shown on a failed draw; click redraws with the failed fit flag.
2. Add `MAP_AUTO_RETRY_DELAYS = [4000]`; one automatic redraw for failures with no HTTP status; timer cleared on dispose and each draw.
3. Update the failure notice to name the control (keep the `Map unavailable: ${error.message}` string that the content test pins).
4. Regression test in `src/api/tests/test_workspace_scripts.py` (node vm) that pins the control, the bounded auto retry and no auto retry for HTTP errors.
5. Run the affected tests (workspace scripts, content standard, accessibility baseline, notices), mypy for `src/api`, ruff. Tier: FULL by rule (src change); the coordinator owns the gate, no `rpi-checks.py --all`.
6. Record the per-criterion table in the changes record.
