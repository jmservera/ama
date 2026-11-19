---
title: Issue 110 plan
ms.date: 2026-11-17
---

# Plan

Findings (measured on eb51af5c9): API+hygiene IoT tests 49/49 pass; core SDK-dependent registry tests fail 34F/16E locally with SDK_MISSING (azure-iot extra not installed; environment, not defect). C1 stays unmet (no real Hub identities). C4 has README claim but no test that HTTP route modules cannot reach the consumer or define ingestion paths.

* [ ] P1 Add `src/api/tests/test_no_public_ingestion_surface.py` (AST import and path-literal guard).
* [ ] P2 Add dated closure-audit record in `docs/reference/research/iot-sensor-analytics-research-plan.md` and log entry; C1 unchanged.
* [ ] P3 Run focused tests, ruff format check, mypy for src/api.
Critique (single pass): test must not be a constant check; limit to HTTP modules; mutation red proof required.
