---
title: Issue 572 chat-panel gate review
ms.date: 2026-11-01
---

Review executed once. Outcome: documentation-only change is conformant; criterion 4 is not proven.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Wire exact case into owned Chromium stage with opt-in | Met on main | `tools/rpi-checks.py` selector and `ZF_BROWSER_TESTS=1` env |
| 2 Fail closed on unexpected skips | Met on main | exact (test, reason) pair, `project-api` only |
| 3 Regression coverage | Met on main | `tools/test_rpi_checks.py` chat-panel tests, 55 OK |
| 4 Fresh complete exact-head gate | Unproven | Requires the complete local gate and a verified receipt; hosted CI is separate and not evidence for this criterion |

Routed follow-up: owner follows the [local RPI gate](../../src/README.md#local-rpi-gate) on the final head (fetch main, `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-dir>`, then `--verify-receipt <receipt.json> --base <current-origin-main-sha>`). Tick criterion 4 and close #572 only after receipt verification succeeds against the current head and reviewed main base.
Human review checkboxes remain unchecked.
