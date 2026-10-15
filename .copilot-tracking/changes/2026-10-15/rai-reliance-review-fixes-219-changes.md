---
title: RAI reliance review fixes changes
description: Execution evidence for PR 315 follow-up
ms.date: 2026-10-15
---

## Scope and Status

Task 219-review-fixes / rai-reliance-review-fixes-219; parent 219.
Research reused/Ready; one final-candidate critique Complete/Pass, no findings.
Declared scope: complete P01/P02 plan. P01 and P02-T01 complete; single Review
Complete / Conformant for engineering. Publication pending in P02-T02.
No material divergences, new decisions or engineering blockers.

## Commands and Results

All commands run in the supplied worktree, never main. P denotes /tmp/zf164/bin.
Session files are uncommitted logs under the supplied Copilot session workspace.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current`; `gh pr view 315 --json state,isDraft,baseRefName,headRefName,body`; `git fetch origin main` | Clean correct branch, open draft PR to main; latest main fetched. |
| `git merge-tree --write-tree HEAD origin/main` | Conflict only docs/reference/log.md. |
| `git merge --no-commit origin/main`; `python3 /tmp/reslog.py docs/reference/log.md`; `git add docs/reference/log.md`; `git diff --check` | Conflict resolved with prescribed script; other changes auto-merged. |
| `gh api user --jq '{id,login}'`; `git config --local user.email 8036360+jmservera@users.noreply.github.com`; `git -c core.editor=true commit -m "chore: merge main into RAI release work" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"` | Account 8036360/jmservera confirmed; merge 80143a9 created. |
| `P/python -c 'import zava_forward.core; print(list(zava_forward.core.__path__))'` | Missing zava_forward module; dependency restoration justified. |
| `P/python -m pip install -q -e 'src/core[dev]' -e src/agents -e 'src/api[dev]'` | Exit 0; restored editable dependencies using pip only, no manifest changes. |
| Root `PYTHONPATH=../core/tests:../agents/tests P/python -m unittest discover -s tests -p test_assistant_release.py -q` | Exit 1: wrong working directory, tests not importable; corrected below. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests P/python -m unittest discover -s tests -p test_assistant_release.py -q` before production fixes | 32 tests, 20 failing subtests/assertions, no errors: missing-reference review/cache, changed fast/strong routes, stale denied briefing. |
| Same targeted command after fixes | Exit 0, 32 tests, 13.852s. |
| `for project in core api; do (cd src/$project && P/ruff check . && P/ruff format --check . && P/mypy) || exit; done` | Exit 0; both projects lint/format pass, mypy 73 core / 35 API files. |
| `cd src/core && P/python -m unittest discover -s tests -q` | Exit 0, 312 tests in 120.702s. Existing sensor-backfill unclosed-file ResourceWarnings; no failure. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests P/python -m unittest discover -s tests -q` first full run | 490 tests, 98 skipped, 3 failures and 3 errors in 225.747s: old offline JSON output harnesses supplied no release reference, so the corrected guard refused their synthetic reviews/cache reuse. |
| `git diff --check`; scoped source diff/protected-path diff; `gh pr checks 315` | Diff clean and protected paths untouched. GitHub reported no checks for the branch at that moment, not a CI success claim. |
| `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests P/python -m unittest test_ai_tasks test_assistant_release dataset.ImproveTests.test_briefing_cached_until_data_changes -q` | Exit 0: 66 tests in 18.161s, including seven regression methods and old failing output tests. |
| `cd src/agents && P/python -m unittest discover -s tests -q && P/ruff check . && P/ruff format --check . && P/mypy` | Exit 0: 70 tests in 5.740s; lint/format pass; 16 files type-checked. |
| Final core/API ruff check, ruff format --check, mypy loop above | Exit 0; 73 core / 35 API files type-checked, lint/format pass. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests P/python -m unittest discover -s tests -q` final full run | Exit 0: 490 discovered, 98 skipped, 148.305s. Conditional SQL Server tests remain skipped; no live SQL Server claim. |
| `cd src/core && P/python -m unittest discover -s tests -q` final full run | Exit 0: 312 tests in 67.178s. |
| Single post-implementation Review | Complete / Conformant within RV-001 through RV-003 engineering boundary; no new defects. Independently checked syntax/diff and 67 in-memory assertions; did not rerun full suites. RV-004 retained. |
| Final publication `git fetch --quiet origin main`; `git rev-list --left-right --count origin/main...HEAD`; `git merge-tree --write-tree HEAD origin/main` | New main a6e26fe arrived after initial merge/validation; one commit behind. Conflicts in append-only log and API README, application JS auto-merges. Integrate before publishing; preserve both README sections and use requested log resolver. |

## P01: Reliance and Cache

Seven new regression methods exercise SQL/JSON historical summary/document
accept/edit, priority view/review and cached AI with inference off, malformed
references, unaffected manual/template accept/edit and AI rejection. Route tests
cover fast summary/message/briefing, strong funding/document/priority, zero new
calls after invalidation, exact old reference rejection even after renewal.
The denied briefing test exercises a cached template followed by actual existing
record function approval at unchanged store version, one scripted generation and
subsequent cache reuse.

Shared release_current now requires nonempty typed reference fields, selects
the current registered route independently of historical model, and compares
against a real selected record; configuration absence never supplies authority.
SqlStore's default assessment now follows the same registered fast/strong
metadata. Configured fallback cache reuse requires the exact current reference;
workflow-only/unconfigured templates and released model-failure fallback cache
behavior stay available. No production ai_tasks change is needed: its existing
review guard and priority/cache guards share release_current.

Owning README documents the corrected boundaries. No new modules, schema,
dependencies, SQL, protected files or mvp changes. Seven methods and one helper
stay within the plan budget. No material plan amendments or divergences.

The first full suite exposed a tightly coupled harness assumption: JSON output
tests and the scripted agents evaluation bypassed dispatch admission but provided
no reference for later review/cache checks. Updated only their explicit offline
setup to supply a labelled scripted-output reference bound to the task binding;
production Store remains fail-closed. Reused existing _scripted setup for text
evaluation too, removing its duplicate partial setup. No golden data changed.

## P02: Validation and Publication

Required local validation complete on reviewed source. Single independent Review
Complete / Conformant; same-PR publication remains. Static checks include agents because its existing
scripted harness changed. No Docker/Azure/actual-provider attempt is represented
by these local checks, and unchanged UI needs no new browser claim.

Review: .copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md.
Late main integration is an authorized delivery action, not a repeat Review or
source-fix cycle; recheck affected API suite/tooling after the merge.

## Remaining Evidence and Human Gates

RV-004 remains open: named OQ-017 release/risk/suspension/restart holders,
approved actual evaluation, authoritative serving proof, meaningful human
oversight, permitted Docker build, SQL Server and Azure evidence. No actual
provider, private data, deployment or live approval is claimed.
