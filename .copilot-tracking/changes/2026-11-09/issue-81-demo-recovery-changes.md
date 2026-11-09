---
title: Issue 81 demo recovery changes and author review
description: Changes, observed demo-targeted checks and one author Review for the local main reconciliation of PR 1240
ms.date: 2026-11-09
task_slug: issue-81-demo-recovery
status: complete-local-blocked-sql
---

Refs #81. Plan: [plan](../../plans/2026-11-09/issue-81-demo-recovery-plan.md); details: [details](../../details/2026-11-09/issue-81-demo-recovery-details.md); research: [research](../../research/2026-11-09/issue-81-demo-recovery-research.md).

## Changes

* Seed `6ef6dc368ae3f8739095f740aa1e68634bd52922` (tree `0006f193`) merged with fetched `origin/main` `b46a9ad9a9619db535368d1b2cbbddec8110e122` by one ordinary merge commit `4bdfb890a` (tree `0ce4ed23`), parents seed and main. Disclosure: the merge was executed while the recovery research was being gathered, before these artifacts were written; the research, plan and details were then written prospectively for validation and review, not backfilled.
* Five conflicts: `.github/rubric/scores/latest.json` resolved to main; `docs/architecture/cutover-evidence-pack.md` (3 hunks, main's date and sections first, parent's #81 alignment checkpoint kept whole after them) and `docs/reference/README.md` (parent side empty, main kept); `src/api/checks/employee_chat_browser_check.py` and `src/api/tests/test_assistant_release.py` resolved by the recorded earlier resolution and equal to main (the seed's changes there were main content from the f548 merge, not parent intent).
* Result relative to main: 191 files, source limited to core (`appointments`, `complaints_route`, `gates`, `procurement`, `quality`, `resident_decisions`, `store`), core tests and README, one evidence-pack section, and `.copilot-tracking` records. No append-only log entry or prior tracking file was modified or removed.
* No push, PR edit, rebase, reset, ticking or deployment.

## Observed checks (owner demo-targeted tier; not complete gate)

Scratch install `/mnt/ama-gates/g81-recovery-1109` (venv, Python 3.12.3, non-editable installs of core, agents, api, ruff 0.17.4, mypy 2.4.1, `PYTHONDONTWRITEBYTECODE=1`, synthetic `ZF_DATA`). Run from `src/core/tests` on merged tree `0ce4ed23`.

| Check | Exit | Result |
| --- | --- | --- |
| `unittest test_gates` | 0 | 20 OK |
| `unittest test_resident_decisions` | 0 | 308 run, 110 skipped (opt-in SQL Server classes) |
| `unittest test_quality_procurement` | 0 | 136 OK (logged tracebacks are expected negative-path output) |
| `unittest test_hazard_referral test_handoff_lifecycle` | 0 | 61 run, 1 skipped (JSON-only ordering) |
| `unittest test_ranking_publication test_ranking_publication_runner` | 0 | 76 OK |
| `ruff check src tests`, `ruff format --check src tests` (core) | 0, 0 | clean, 216 files formatted |
| `mypy` (core) | 0 | 270 source files clean |

## Blocked: owned SQL Server run

Planned owned loopback container run of `ZF_RESIDENT_MSSQL=1 test_resident_decisions` was not admitted. Nonqueued `flock -n /tmp/ama-rpi-heavy.lock` returned BUSY (holder: another operator session's `flock` process; containers `zf-1292-sql` and an `ama-sensor110` container were running, none mine). Per policy I did not wait, poll, inspect or interrupt. No container was started or removed by this lane. The 110 skipped resident-decision tests are therefore unproven in SQL, and the #1292 reload defect was not reproduced or excluded on SQL here. Dependency: merged #1292 plus an admitted owned SQL run on the final exact head; resume only on a coordination event.

## Review (author, one execution)

* Outcome: conformant for the local reconciliation and the selected non-SQL checks only. Not independent, hosted or human review; no FULL gate.
* Findings: Medium, open: SQL acceptance blocked (lock busy, #1292 dependency). Medium, carried: original #1226 replacement-route follow-up and owner-blocked #1238. Low: old receipt `g81-r15-1106` covers `c5edb320a` and cannot validate the seed (adds #86) or this merged head. Low: merge preceded the written plan, disclosed above.
* Boundaries verified by source ancestry only: #82 (`81c106998`, with earlier #898 #1035 #1097 on main) and #86 (`6ef6dc368`) are ancestors; consent, resident decision records, hazard ownership, manual and complaint routes are retained in source; nothing approves Legal, resident, AT or owner decisions.
* Residual: independent exact-head review, hosted CI, SQL, browser/accessibility, live and professional criteria; the four #81 criteria and #440 stay unticked, issue stays open.
