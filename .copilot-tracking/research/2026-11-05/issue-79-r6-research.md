---
title: Issue 79 research, continuation r6 (current-main preparation)
ms.date: 2026-11-05
---

## Identity and pins

* Task `issue-79-r6-main-preparation`, parent task `issue-79-r5-clean-candidate`. Earlier r4 and r5 research, plan, implementation and Review outcomes are preserved unchanged.
* Branch `feat/ranking-publication-runner-79`, intake head `3b145691f27224472c3f7f09b65f2cb5722eeb58` (tree `c7a2edaf499938647da41c241716c7881a6c86e3`), clean including `--ignored`.
* Main pin: `origin/main` `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (fetched 2026-11-05). Merge base was `ead177ef90d24666557708ea344848a1be43bdf8`.
* Deliberate parent target `feat/case-workbench-integration-73` (at `ead177ef9`, checked out in `/home/azureuser/source/ama-wt/parent-73`): preserved, not moved, not retargeted. Parent integration acceptance is not presumed.
* Research disposition `executed`; Planning Readiness `Ready`. Case study documents, KB index, memory and the retention policy were already read in earlier continuations; this round re-read only the retention constraints (no deletion, external caches).

## Main delta (55 files, +1808/-25)

* Gate tooling: `tools/rpi-checks.py` and `tools/test_rpi_checks.py` (#1208 Chromium prerequisite sequencing, #1215 bytecode discovery), `tools/backlog-sync.py` and its test (#1207), `.github/workflows/src-ci.yml`, `src/README.md`, a CSS file in `src/api`, rubric `latest.json`, tracking records for those issues and `docs/reference/log.md`.
* Overlap with this branch: only `docs/reference/log.md` (both append-only). Our runner, tests, `pyproject.toml` mypy override and core README are untouched by main. Merge was expected to be conflict free.

## FULL tier

FULL remains required: the candidate is a runtime ranking-publication feature with retained-record behavior (idempotent persisted publication, archive and capacity checks). Light preparation checks do not downgrade it. #96 alone owns heavy admission (pid 1592594, `--all --fresh-images --jobs 2 --lock-timeout 0 --base bb3a3b03... --out /tmp/g96-r11b-1105`); this task does not compete. Reported future order: #96, #440 required observations, #233 focused refresh, #144 full, then coordinator reassessment.

## Scope limits

No scheduler, ranking policy, sign-off, deployment or retention authority change. Criterion 3 (named policy-owner sign-off) and criterion 4 (actual scheduled and retained publication) stay open; a local invocation runner proves neither.
