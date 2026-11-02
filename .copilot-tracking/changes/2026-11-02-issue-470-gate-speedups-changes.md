---
title: Issue 470 gate speedups changes
ms.date: 2026-11-02
---

Changed: `tools/rpi-checks.py` (shard helpers, `skipped_groups`, `base_relaxation`, `validate_stack`, `clean_identity(reviewed_base=...)`, `Runner.sharded_tests`, `plan_shards`, image cache mode, new CLI flags `--fresh-images`, `--stack`, `--stack-member`, `--exact-base`, `--jobs` default 0), `tools/test_rpi_checks.py` (15 new tests; image-build test now covers both cache modes), `src/README.md` (gate speed controls), `.github/agents/ama-backlog-delivery-coordinator.agent.md` (policy text), `docs/reference/log.md`, and these RPI artifacts.

Validation run: `python3 -m unittest discover -s tools -p test_rpi_checks.py` 71 tests OK (was 56); ruff (isolated gate rules) and `mypy --strict` clean on both tool files; `--changed` selection dry run at head 2b8a457f2 selected preflight, namespace, static, tooling and recorded 14 skipped groups with reasons; shard partition of src/api (89 modules) gave 30/29/30. Pre-existing unrelated failure: `tools/test_check_demo_feedback.py` import error under `unittest discover -s tools` (also on base).

Not run: the complete gate (`--all`), real shard execution, real parallel timing, Docker layer-cache builds, SQL, browser, Trivy. Criterion 4 (measured before/after time) is therefore not met. No receipt is claimed.
