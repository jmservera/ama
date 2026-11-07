---
title: Issue 1251 R2 hosted lint failure research
description: Evidence for the Ruff E501 hosted CI failure on PR 1252 and the corrected focused validation plan
ms.date: 2026-11-07
ms.topic: reference
---

## Adverse evidence (retained)

* Hosted Source projects CI `src-namespace`, run 42377771334, job 128418840310, step "Local gate orchestration contracts and strict checks" failed on head faf6c578e6cb5cd0b5171e51f6eab8b36c130d45. Copy: `/mnt/ama-gates/g1251-ci-r2-1107/original-ci-failure.log` (source `/tmp/1252-namespace-failure-1107.log`).
* All 17 backlog tests passed. Ruff E501 failed on `tools/test_backlog_sync.py` lines 162, 190, 205, 223 (106, 101, 112, 108 characters, limit 100). Caused by this change's added tests, not pre-existing.

## Root cause of the miss

* [.github/workflows/src-ci.yml](../../../.github/workflows/src-ci.yml) lines 257-265 require `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, `mypy --ignore-missing-imports tools/test_backlog_sync.py tools/backlog-sync.py`, plus the rpi-checks and ci-affected unit suites. The original focused plan used only E9,F, which omitted E501, I, B, UP and the format check. That adverse validation gap is disclosed, not excused.
* Local reproduction with ruff 0.17.3: same four E501 findings; `ruff format --check` also reports the file would be reformatted (three call sites). Line 162 is an f-string that the formatter cannot wrap, so it needs a manual split.
* Pre-correction AST SHA-256 of the test file: a9b04ee36123b9f010257eba143655b5bb8d6a13476a16a128f3bdb7ee24f6f5.

## Disposition

* Research: executed. Planning Readiness: Ready. Scope: formatting of the test file only; source, root-cause guard, test semantics, config and workflows unchanged. No E501 suppression.
