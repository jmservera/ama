---
title: Issue 79 research, r22 merge of main c1a16482
ms.date: 2026-11-07
---

Task `issue-79-r22-merge-main-1255`, parent `issue-79-r21-merge-main-1252`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: `feat/ranking-publication-runner-79`, head `47de325d80eda5665f3e3d3250fedce7a17c85d1`, tree `46f69e5e2af3538bc40725a9fc88b1a73684128b`, ignored-clean; PR 1239 open, base `main`. Child 1231 not touched.
* `origin/main` is `c1a164829e77efe45f5f002740bd79699b89b334`, equal to the coordinator pin and the PR 1255 merge commit; descends from `a1d265340`. No score-only descendant.
* Delta against `a1d265340` (17 paths): modified `src/api/tests/test_assistant_release.py` (`48be02b95` to `b464f5907`), `tools/rpi-checks.py` (`8406ca947` to `4ead23d75`, SQL_SELECTORS adds the unleased revocation class), `tools/test_rpi_checks.py` (`81f4109d2` to `9a64271e2`); 14 added 107 RPI records. No `src/*/src` production, schema or workflow path.
* Overlap with topic-changed paths: none; `git merge-tree` is clean.
* Preserve ref `preserve/issue-79-pre-main1255-merge` at the start head.
* Original three 357e842d Medium findings remain author-corrected only.

## Limits

* No FULL, SQL, browser or heavy lock. The SQL class is not run; hosted SQL does not select it (disclosed by coordinator).
