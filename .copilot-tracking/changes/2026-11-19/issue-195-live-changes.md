---
title: Issue 195 live changes
---

Files: src/api/src/zava_forward/api/build_info.py (new), server.py (log line), src/api/Dockerfile, .github/workflows/src-deploy.yml, src/api/tests/test_build_info.py (new), docs/reference research note, README index, log.

Validation (FOCUSED local; tier FULL applies, not run): test_build_info 4 OK; test_role_matrix 13 OK; ruff check and format clean on new files; mypy 7 errors identical before and after (missing opentelemetry stubs, pre-existing). Full gate and rpi-checks --all not run (heavy lock held, forbidden).

| Criterion | Status |
| --- | --- |
| #440 checkpoint | Unproven (owner) |
| Children closed or deferred | Unproven (owner) |
| Image from src verified running | Partly proven; commit provenance added, rebuild not possible from this host |
