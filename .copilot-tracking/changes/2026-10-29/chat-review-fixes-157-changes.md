---
title: Chat review fixes 157 changes
description: Implementation evidence and validation boundary
ms.date: 2026-10-29
---

Task: `157-chat-review-fixes-2026-10-29`; full P01-P03 scope.
Plan/details/critique: dated `chat-review-fixes-157` artifacts.
Critique: Complete / Pass, zero findings, accepted without rerun.

## Initial State

Requested first `git pull --rebase`: exit 0, fast-forward c5d8873a.
Clean open PR 503 branch feat/agent-chat-157; rubric remote update untouched.
Missing `.venv/bin/python` and global package import were observed (exits
127 and 1). Restored local venv and installed existing core/agents/api dev
distributions, exit 0; no dependency manifests changed.

## P01-P02 Implementation

Red reproductions (before source changes):

* Core focused selectors: exit 1, six tests, three failures and three errors.
  The expanded dispatched block was 4,730 characters >4,000; B's follow-up
  lost B's question; legacy content leaked into the prompt; actor_role was
  missing on JSON/SQLite restart and migration.
* Agents callback selectors: exit 1, two methods with subtests, three errors
  and two failures. Callback RuntimeError escaped the adapter and the panel
  took its generic one-call/no-usage path.

P01 now catches callback errors at their actual boundary, logs exception class
only, and returns typed admission/completion-check-failed consumption. The
completion result's validated usage and calls are retained without authorizing
its text. Existing explicit revocation and disabled behavior remains.

P02 measures and appends the identical expanded history block, including
wrappers. Shared storage records actor_role; SQL column lists, fresh DDL and
SQLite/MSSQL additive migration paths persist it. Unknown legacy roles are
excluded, not inferred. Updated both owning READMEs.

Initial green: `PYTHONPATH=src/core/tests .venv/bin/python -m unittest
test_chat_panel test_chatthreads -q`: exit 0, 38 tests.
`PYTHONPATH=src/core/tests:src/agents/tests .venv/bin/python -m unittest
test_chat_model -q`: exit 0, 7 tests.
One subsequent SQL restart history integration regression extends this coverage.

## P03 Validation and Remaining Gates

Core full-package Ruff check/format check/mypy: exit 0, 106 formatted files,
159 source files typed. Agents first Ruff run rejected loop closures in new
tests (B023); replaced them with bound Mock return/side effects, without
production changes. Agents rerun check/format/mypy: exit 0, 20 formatted files,
24 typed files. Final checks after the additional SQL test are recorded below.
No push, az or other worktree operations permitted.
Full publication gate and actual SQL Server/human/hosted acceptance cannot be
inferred from focused local checks; keep unmet evidence explicit.

## Amendments and Divergences

Immediately relevant current-state amendment: the full agents suite exposed
`KeyError: actor_role` in regulatory_chat's atomic direct-repository writer
(106 tests, one setUpClass error). Wire those paired writes and doubt receipts
to the new field; copied old messages retain unknown roles rather than
receiving a new owner's role. This is tightly coupled storage compatibility;
plan/details updated, no new user decision or repeated critique.
The first core full-suite attempt also covers that pre-correction snapshot;
it ran 1,493 tests in 335.691s, exit 1, seven regulatory-chat errors and
191 integration skips. All seven errors were missing actor_role in the same
direct-writer path, not unrelated baseline failures. Corrected affected tests
and then the complete core suite were rerun, not merely assumed green.

## Final Validation

Python 3.12.3, editable distributions in this worktree's restored `.venv`,
Ruff 0.17.1 and mypy 2.4.0. All fixture data is constructed/synthetic.

| Command (from repository root unless cd shown) | Result |
| --- | --- |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -q` | Exit 0; 1,493 tests, 191 skips, 301.182s |
| `cd src/agents && PYTHONPATH=tests:../core/tests ../../.venv/bin/python -m unittest discover -s tests -q` | Exit 0; 122 tests, no skips, 35.535s |
| `cd src/core && PYTHONPATH=tests ../../.venv/bin/python -m unittest test_chat_panel test_chatthreads test_chat_memory test_chat_privacy test_regulatory_chat test_sqlstore test_dependency_rule -q` | Exit 0; 119 tests, no skips, 56.101s |
| `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_chat_panel test_chat_isolation test_chat_fixture_roles test_mssqlstore -q` | Exit 0; 267 tests, 188 SQL Server skips, 31.640s |
| `cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy` | Exit 0; 106 formatted files, 159 typed files |
| `cd src/agents && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy` | Exit 0; 20 formatted files, 24 typed files |
| `git diff --check` | Exit 0 |

Eight focused test methods added, none removed. Shared storage method executes
for both JSON and SQLite, with opt-in SQL Server inheritance.

Core skip reasons: 188 declared integration opt-ins (1 isolated synthetic Azure
SQL, 187 owned/local SQL Server variations), plus three runtime backend-specific
non-applicabilities: JSON-only separate-file audit ordering, SQL writer
dependency checks, JSON file rollback only. These remain skips, not passes.
API's 188 skips require `ZF_TEST_MSSQL=1` and its disposable SQL Server;
no such server was selected or accessed. No actual SQL Server migration pass
is claimed.

Final raw core full/focused logs are retained outside git in this session's
`files/chat-fixes-core-full-final.log` and `files/chat-fixes-core-focused.log`.
The original full-core failure is preserved in the dated summary above and
session tool output. No authoritative gate receipt exists for this candidate.

## Original Review and Local Delivery

Source implementation and validation complete. Single independent Review:
execution Complete; outcome Conformant with justified divergence, bounded to
implementation. No implementation defects. RV-001 actual SQL Server validation
and RV-002 publication/hosted/human/activation evidence remain Medium residuals,
routed to separate authorized follow-up work. The reviewer independently passed
62 tests and both packages' Ruff/check-format/mypy.
Report: .copilot-tracking/reviews/logs/2026-10-29/chat-review-fixes-157-review.md.
No source or test edits followed Review; only parent closeout tracking changed.
P03-T02 concludes at the authorized local commit persistence boundary.
Author/committer use the authenticated account's repository-local noreply
identity (`8036360+jmservera@users.noreply.github.com`) and the requested trailer.
The commit includes these dated original artifacts; its self-referential hash
is intentionally obtained from git after committing, not embedded here.
Required human, real-model/activation, actual SQL Server and hosted checks are
not substituted by these local engineering results. No push or az was used.
