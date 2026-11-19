---
title: Issue 1274 axe download details/critique
ms.date: 2026-11-18
---

Critique executed once (self, final candidate): proceed; no conflicts with owner decisions.

1. Edit the axe step in `.github/workflows/src-ci.yml`: add `--retry 5 --retry-all-errors --retry-delay 5`, download to a temp name, verify with `sha256sum -c` against the pinned digest, then move into place so a partial or wrong file is never used.
2. Update `WORKFLOW_HASHES["src-ci.yml"]` in `tools/rpi-checks.py`.
3. Add a regression in `tools/test_rpi_checks.py` asserting the workflow pins the same digest as `AXE_SHA256` and verifies before use.
4. Validate: test_rpi_checks, test_install_actionlint, ruff, mypy, actionlint over native workflows. Tier FOCUSED (no src/ change; no permissions, pins, secrets, deployment change); recorded as a judgement, FULL not run per owner.
