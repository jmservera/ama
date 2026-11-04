# Plan: provider input bounds for issue 116

Details: [details](../details/2026-11-04-provider-input-bounds-116-details.md). Critique: single pass, no conflicts with confirmed decisions (keep manual paths, no new serializer).

* [x] Phase 1: add InputRefused, size bounds and image allowlist in ai.py
* [x] Phase 2: behavioural tests in test_ai_input_bounds.py
* [x] Phase 3: focused tests, ruff, mypy as CI
