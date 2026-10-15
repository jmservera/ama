---
title: Transactional hazard hold correction changes
description: Implementation and executable validation evidence for PR 314
ms.date: 2026-10-15
---

## Scope and Current State

Task hazard-hold-rv001, parent src-hazard-referral-85. Full bounded plan.
Research reused, one final-candidate critique Pass with no findings.
Implementation and requested local validation complete.
Single child review execution Complete, outcome Residual work.
RV-001 corrected locally; RV-002 documentation satisfied but policy unratified,
RV-003 live service/platform/human evidence remains open.
Plan: .copilot-tracking/plans/2026-10-15/hazard-hold-rv001-plan.md.
Details: .copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md.

## P01 Implementation

Initial regression reproduced five unsafe procurement transitions, including
Completed. Quality/signoff/advance already conflicted on case writes but did
not perform the required transaction-local hazard predicate. All nine now
register shared dependencies. save reloads hazards and rowversion under its
existing writer transaction before writes; GateError and ConflictError both
rollback/discard pending case/procurement/audit state. Dependencies clear after
save, discard and outer lock exit.

Core/API READMEs distinguish demonstrator release roles from unratified
operational release authority and response/update/escalation policy.
No removals, new runtime dependency, schema or policy authority.

## Commands and Results

All commands run in the specified worktree unless a component directory is
shown. Read/search/edit tools are evidenced by source and artifact diffs.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current && git fetch origin` | Clean specified branch, upstream fetched successfully |
| `gh pr view 314 --json title,body,isDraft,baseRefName,headRefName,url` | Existing draft, main base, specified branch, RV-001 openly blocking |
| `gh api user --jq '{id,login}'` | Verified 8036360 / jmservera |
| `git merge-tree --write-tree HEAD origin/main` | Only docs/reference/log.md conflicted |
| `git merge origin/main --no-edit` | Expected log conflict |
| `python3 /tmp/reslog.py` | Exit 1: helper requires file argument; no files changed |
| `python3 /tmp/reslog.py docs/reference/log.md && git add docs/reference/log.md && git -c user.email=8036360+jmservera@users.noreply.github.com commit --no-edit -m "Merge origin/main into feat/src-hazard-referral-85" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"` | Exit 0; cb7444b merges main, preserves both append-only logs |
| `git config --local user.email 8036360+jmservera@users.noreply.github.com` | Exit 0 |
| `/tmp/zf164/bin/python -c "import zava_forward.core, zava_forward.api; print(list(zava_forward.core.__path__)); print(list(zava_forward.api.__path__))"` | Interpreter's editable imports point at another worktree; validation must explicitly bind this worktree's src paths, not mutate shared editable installation |
| `cd src/core && PYTHONPATH=src:../agents/src:../api/src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -p test_hazard_referral.py -k interleaved -q` | RED before store changes: exit 1; 1 test, 9 subtests, 5 unsafe procurement failures (no gate) and 4 pre-existing case-write conflicts; log /tmp/ama-85-rv001-red.log |
| `cd src/core && /tmp/zf164/bin/ruff format tests/test_hazard_referral.py && PYTHONPATH=src:../agents/src:../api/src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -p test_hazard_referral.py -q && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy` | Tests 18 passed; lint exit 1 with four B023 loop-closure reports; downstream format/type checks did not run. Bound callback arguments using partial, no suppression. |
| `cd src/core && /tmp/zf164/bin/ruff format tests/test_hazard_referral.py && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy && PYTHONPATH=src:../agents/src:../api/src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -p test_hazard_referral.py -q` | Exit 0; lint, format, mypy (71 files) passed; 18 hazard tests passed in 7.944s |
| `cd src/api && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && MYPYPATH=../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/mypy && PYTHONPATH=../core/tests:../agents/tests:../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -p test_hazard_api.py -q` | Exit 0; lint, format, mypy (36 files) passed; 3 loopback hazard HTTP tests passed in 3.103s |
| `cd src/core && PYTHONPATH=src:../agents/src:../api/src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -q` | Exit 0; 325 tests passed in 118.749s; /tmp/ama-85-rv001-core.log |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests:../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -q` | Exit 0; 475 tests run in 199.856s, OK with 97 optional/environment skips; /tmp/ama-85-rv001-api.log |
| `cd src/core && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy && cd ../api && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && MYPYPATH=../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/mypy` | Exit 0 final static gates; core 71 and API 36 source files checked |
| `git diff --check && git diff -- src/core/src/zava_forward/core/sqlstore.py src/core/src/zava_forward/core/store.py src/core/tests/test_hazard_referral.py src/core/README.md src/api/README.md` | Exit 0; correction inspected, no whitespace errors |
| `git status --short -- mvp .env .vscode .copilot-tracking/github-issues` | Empty; excluded owner paths and mvp untouched by correction |
| `gh pr view 314 --json isDraft --jq .isDraft` | true before final correction delivery |

## Validation Environment Correction

Use requested /tmp/zf164/bin tools and CI test-helper PYTHONPATH, extended with
the five current worktree src paths to override unrelated editable packages.
This preserves isolation without pip modification of a shared environment.
No uv and no packages installed. Record exact commands below.

## Remaining Evidence and Follow-Ups

P01-T01/P01-T02/P02-T01 complete. One review complete; delivery bookkeeping pending.
Four added test methods cover all nine guarded transitions, stale-clear
version conflicts, rollback of pending audit/procurement/case state, clean
next requests and transaction-local reload with a concurrent writer unable to
commit between validation and commit. The serialized-writer case permits the
completion that commits before intake, then blocks subsequent correction.
RV-002 remains unratified; RV-003
live service/platform/human acceptance remains out of scope.

## Amendments and Divergences

No significant divergence or new user decision. Immediately relevant environment
correction: explicitly bind this worktree sources because shared interpreter
editable installs point elsewhere. Plan/details reflect the correction.
Original implementation/review artifacts remain unchanged; this selected child
task owns correction and its one review. No policy approval or product acceptance
is inferred from local engineering evidence.
