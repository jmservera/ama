# Plan: #215 doubt route and no-source held-state parity (2026-11-14)

* Add `src/api/tests/test_epic215_doubt_route_held_state_wcag_parity.py`: static UI contract tests (non-colour cues, keyboard-operable doubt control, plain-language mode copy) and runtime tests over every `STAFF_ROLES` role on the synthetic SQL fixture (answer, no-source and refused turns, doubt receipt, idempotence, plain ASCII copy, no approval claims).
* Zero-mutation check: snapshot cases, law reg_* tables and rule history before and after each role loop; only chat and audit records may change.
* Focused tier only: unittest, ruff check, ruff format --check, mypy.
* Critique (once): the risk is overlap with siblings and brittle string pins; mitigated by asserting only the held-state surfaces and runtime behaviour. Applied directly. Refs #215.
