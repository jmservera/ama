---
title: RAI harm threshold incident plan (Refs #146)
date: 2026-11-14
---

* [x] Phase 1: write `src/api/tests/test_rai_harm_threshold_incident.py` with strict annotations (details: [details](../details/2026-11-14-rai-harm-threshold-incident-details.md)).
* [x] Phase 2: run ruff check, ruff format --check, mypy and the new tests.

Critique: executed once, inline. Verdict: proceed. Disposition: avoid `pyproject.toml` edits by typing untyped fixtures through `Any`; invoke dispatch after the incident through the service as the inspector role cannot invoke.
