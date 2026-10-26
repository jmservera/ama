<!-- markdownlint-disable-file -->
---
title: Issue 350 main acafc6ee integration plan and details
description: Prospective plan and phase details
ms.date: 2026-10-26
---

Prospective; before critique and merge.

* [ ] Phase 1: one independent critique; commit research, plan and critique before the merge.
* [ ] Phase 2: `git merge --no-ff origin/main` (normal merge, no rebase, no force). Expect no conflict. If `log.md` conflicts, keep both entries append-only; if rubric files conflict, take main's with a recorded rationale, never synthesise scores. No source or fixture change unless a real conflict requires it.
* [ ] Phase 3: verify with the existing topic-bound environment `/home/azureuser/rehearsal-350/venv` (confirm `zava_forward.core.__path__` resolves to this worktree): `PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.test_check_demo_feedback` (expect 88 OK); `ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --check` (width 88) from `/mnt/ama-rpi-gates/issue462-helper-correction1/venv/bin/ruff`; verify the merge delta has no topic-file change. No Docker, browser, gate or install.
* [ ] Phase 4: one independent integration review; record the actual return; changes and state records; commit.
* [ ] Phase 5: final-head clean candidate and future gate plan under `/mnt/ama-rpi-gates/` (output absent, `--lock-timeout 0`, base the then-current main); the gate does not run until the 349 shared no-cache image gate fix is published and integrated (explicit dependency). Stop for the coordinator.
