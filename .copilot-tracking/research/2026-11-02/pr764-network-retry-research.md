---
title: PR 764 third CI failure research
date: 2026-11-02
---

Disposition: executed. Planning Readiness: Ready.

* Failing step: src-api "Synthetic design-system browser checks", run 41461333355 job 125330936287, `Chat unavailable` not found, then TargetClosedError.
* The step runs: employee_acceptance_check, design_system_browser_check, regulatory_ux_check, case_journey_browser_check and `test_chat_panel...test_browser_warning_failure_keyboard_refusal_and_live_log`. Other src-api steps: unit, ruff, mypy, harness lint.
* Reproduced locally (venv, pip): only the chat panel test fails, in 6.8 s.
* Root cause: the test simulates an outage with `route.abort()` on `/api/chat/status`. That is a network-level `TypeError` in `fetch`. `fetchReadRetrying` (eca010432) retried network errors three times (500+1500+3000 ms), so `Chat unavailable` appeared after the 5 s expect timeout. Earlier fixes covered JSON bodies and status restoration but not network errors.
* Synthetic HTTP failures with JSON bodies were already excluded (59f289c4d). POSTs use plain `fetch`.
