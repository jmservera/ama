---
title: Issue 2186 details 2026-11-26
description: Phase details for the rubric-score relaxation
ms.date: 2026-11-26
---

## Phase 1

`tools/rpi-checks.py`: prefix tuple gains `.github/rubric/scores/`. `moved_path_blocker` gains `if receipt_inert_path(path): return ""` after the `pr_paths` check.

## Phase 2

`tools/test_rpi_checks.py`: cases `rubric score files` (allowed) and `rubric scripts` (blocked, `.github/rubric/scripts/prepare.py`).
