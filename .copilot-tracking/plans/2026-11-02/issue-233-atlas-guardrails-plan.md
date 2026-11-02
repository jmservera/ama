# Plan: issue 233 atlas guardrails slice

* [x] Add src/api/tests/test_role_screens_conformance.py (static checks, no rendered claims).
* [x] Update the trace doc with a static guardrail section and narrowed unmet-criteria wording; ms.date 2026-11-02.
* [x] Update the reference index row and append a log entry.
* [x] Focused validation: new test, accessibility baseline, design system, atlas trace tests and checker, `tools/rpi-checks.py --changed`.

Critique (executed once, inline): the test must not claim conformance; scope it as source-level and keep the withheld-text rule guarded as proposed. Applied directly. No conflict with confirmed decisions; no user decision required.
