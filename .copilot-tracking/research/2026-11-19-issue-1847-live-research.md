---
title: Issue 1847 live research (nomination bootstrap isolation)
ms.date: 2026-11-19
---
# Research: #1847 on main 910adb0a1 (demo, desktop, FOCUSED tier)

* Research disposition: reused. Prior proof: docs/reference/research/nomination-bootstrap-isolation-proof-1847-2026-11-18.md (criteria 1-5 proven on 16880f509; criterion 6 unproven for demo).
* Fix already on main: 7de4a8110 (#1849) rejects foreign modules without purging sys.modules; regression in src/core/tests/test_nomination_bootstrap.py.
* No Azure involvement. Scope is test bootstrap only; owner decisions exclude the full gate for the demo.
* Plan: re-run focused tests on current head to confirm criteria 1-5 still hold; criterion 6 is not a demo criterion.
* Planning Readiness: Ready.
