---
title: Changes for the 107 fresh-main preparation
description: One normal merge of admitted main 7551e50 into the 107 topic, light checks and honest limits
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-full-handoff-plan.md) with its prospective amendment. Original records and commits are preserved.

## Integration

* Start head dec3bc5da343a3f964c7fd77e29eaa76f969f5e5, tree f19a7af68c5e14cefbb197b200cb08cdbd6b0297; local ref `backup/issue-107-dec3bc5da-pre-merge` kept (the amendment commit sits after it).
* One normal merge (no fast-forward) of main 7551e50e904cd4d696ed74ecd6fb1e0cb6be1ba8 (PR 1249 merge, after 1247). No conflicts; no rebase, force or rewrite. Source delta of the topic versus main is the one test in `src/api/tests/test_assistant_release.py` plus `.copilot-tracking` records. No production change; the inherited merged checker is untouched.

## Correction to the plan amendment

The amendment's selector line garbled a class name. The actual classes in `src/api/tests/test_assistant_release.py` are DependentPolicyRelease, Release, Legacy and TaskReleaseRecord; the new test is `Release.test_racing_workers_and_restart_after_revocation_keep_allowance_and_make_no_call`. The amendment is not rewritten.

## Light checks (own-worktree pip venv in /mnt/ama-gates/g107-755-preparation-1107, PYTHONDONTWRITEBYTECODE=1, external XDG/ruff/mypy caches, from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`)

| Command | Result |
| --- | --- |
| import-origin probe of `zava_forward.core/agents/api` | all under this worktree (the user-level editable installs point at the canonical checkout, so earlier session runs on this topic imported canonical src; only the test file differed) |
| `python -m ruff check .` (api, core) | passed |
| `python -m ruff format --check .` | 116 files already formatted |
| `python -m mypy` | no issues, 188 files |
| `python -m unittest test_assistant_release -q` | 46 OK, exit 0 |
| `python -m unittest test_assistant_release test_assistants test_continuity -v` | 188 OK, exit 0, 58 skipped (all 'needs disposable SQL Server (ZF_TEST_MSSQL=1)'); log in scratch |

Not run: FULL gate, SQL Server, browser, scanners, images, provider, Azure. The skips are not FULL evidence. The pip egg-info directories were removed after the run so the tree is ignored-inclusive clean; the scratch venv is external and not reusable for the gate.
