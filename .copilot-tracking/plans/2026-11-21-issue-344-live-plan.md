# Plan: issue 344 live (2026-11-21)

Tier: FULL (src change), local commit only; no `rpi-checks.py --all`.

* [x] Phase 1: research and live probes (see research note)
* [ ] Phase 2: fix `Store.unaccepted_handoffs` so a handoff whose `offered_at` cannot be aged (missing or no timezone) is left out of the ageing list instead of failing the endpoint with 500; it stays visible in `/api/handoffs` and `/api/handoffs/unowned`
* [ ] Phase 3: regression test in `src/core/tests/test_handoff_escalation_83.py` (JSON and SQL store classes)
* [ ] Phase 4: run core handoff tests, mypy and ruff in `src/core`
* [ ] Phase 5: research note under docs/reference/research/ with the per-criterion table; index and log entries
* [ ] Phase 6: changes record, review, commit

Not changed: Easy Auth `RedirectToLoginPage` (owner decision plus infra redeploy needed); blocked parity items (#349, #350, #210).
