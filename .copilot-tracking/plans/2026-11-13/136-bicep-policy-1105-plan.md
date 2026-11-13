---
title: Issue 136 plan
ms.date: 2026-11-13
---

## Objective

Rerun four infra tests offline in a correctly built venv and record evidence; tracking-only write surface (no edits to infra/, src/, docs/). Focused tier.

## Phases

* [ ] Phase 1: Critique (independent) before any venv or test run.
* [ ] Phase 2: Create /tmp/venv-136pol-1105 with --system-site-packages, upgrade setuptools and wheel only if the editable installs need it, `pip install --no-deps -e` src/core, agents, api, orchestrator, importer; verify `zava_forward.<pkg>` paths lie inside the worktree.
* [ ] Phase 3: Run test_staff_azure, test_identity_rbac, test_private_cutover_proof, then test_bicep_policy (timeout 240s) from infra/tests, saving the producer exit code to file; record counts, skips, durations.
* [ ] Phase 4: Classify any failure as genuine or environmental; do not fix. Write changes log; delete the venv and any generated files (egg-info, __pycache__) so git status stays tracking-only.
* [ ] Phase 5: Independent review, commit with trailer.
