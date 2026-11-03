---
title: Issue 572 post-#757 verification research
ms.date: 2026-11-03
---

Delivered by merged PRs #575, #595, #600, #606, #757 (code) and #627, #719, #731, #756, #789 (evidence). On main b9db38c73, criteria 1 to 3 hold: tools/rpi-checks.py registers the exact chat-panel case with its ZF_BROWSER_TESTS opt-in, the allowlist is not broadened, and tools/test_rpi_checks.py covers required execution and fail-closed unexpected skips. The two blockers recorded by the 2026-11-02 rerun review (core mypy at test_chat_case_answers.py:64; case-journey tab wait) were addressed by #757. Criterion 4 (fresh complete exact-head gate with browser and MSSQL) is unmet and is run by the coordinator, not in this slice. Planning readiness: Ready. Research disposition: reused.
