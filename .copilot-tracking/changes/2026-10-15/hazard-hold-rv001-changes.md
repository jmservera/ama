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
| `gh api user --jq '{id,login}' && git config --local user.email 8036360+jmservera@users.noreply.github.com && git add -A -- <the five correction files and seven hazard-hold-rv001 artifacts> && printf '%s\n' 'fix(core): validate hazard holds in committing transactions' '' 'Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>' \| git commit -F -` | Exit 0; correction/evidence commit 1762ccb |
| `git push origin HEAD:feat/src-hazard-referral-85 && gh pr edit 314 --body-file <session>/files/pr314-body.txt && gh pr ready 314 && gh pr view 314 --json number,isDraft,headRefName,headRefOid,baseRefName,mergeable,url,statusCheckRollup` | Exit 0; pushed correction, honest Refs/unchecked criteria, marked ready; GitHub then reported CONFLICTING because main advanced during validation |
| `git fetch origin && git log --oneline HEAD..origin/main && git merge-tree --write-tree HEAD origin/main` | New main a6e26fe (#313); log and API README conflicts |
| `gh pr checks 314 --json name,state,link` | Exit 1: no checks yet reported immediately after initial push, not a passing CI result |
| `gh pr ready 314 --undo && git merge origin/main --no-edit; python3 /tmp/reslog.py docs/reference/log.md` | Returned PR to draft; merged new upstream design-system work, expected two documentation conflicts; supplied helper resolved log, both API README sections preserved manually |
| `cd src/core && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy && PYTHONPATH=src:../agents/src:../api/src:../orchestrator/src:../importer/src /tmp/zf164/bin/python -m unittest discover -s tests -q` | Integrated tree exit 0; all static gates passed, 325 tests passed in 55.589s; /tmp/ama-85-rv001-core-integrated.log |
| `cd src/api && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && MYPYPATH=../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/mypy` | Integrated lint/format passed; mypy exit 1 because new upstream browser-check module needs missing playwright.sync_api; suite did not run in this attempt |
| `git add docs/reference/log.md src/api/README.md && git diff --check && git ls-files -u && node --check src/api/src/zava_forward/api/web/app.js && /tmp/zf164/bin/python -m json.tool .copilot-tracking/rpi-sessions/2026-10-15/hazard-hold-rv001-state.json` | Exit 0; conflicts resolved, no whitespace/JavaScript/state errors |
| `/tmp/zf164/bin/python -m pip install --quiet --target /tmp/ama-85-rv001-deps-ab31c480 'playwright==1.64.0'` | Exit 0; restored new upstream pinned dev dependency into isolated target, no shared installation changes |
| `cd src/api && PYTHONPATH=/tmp/ama-85-rv001-deps-ab31c480 MYPYPATH=../core/src:../agents/src:src:../orchestrator/src:../importer/src:/tmp/ama-85-rv001-deps-ab31c480 /tmp/zf164/bin/mypy` | Exit 2: placing complete pip target in MYPYPATH shadows typing_extensions; suite did not run. Switched to a normal isolated type-resolution venv. |
| `/tmp/zf164/bin/python -m venv /tmp/ama-85-rv001-typeenv-ab31c480 && /tmp/ama-85-rv001-typeenv-ab31c480/bin/python -m pip install --quiet 'playwright==1.64.0'` | Exit 0; isolated development dependency environment, pip only, no browser installation |
| `cd src/api && MYPYPATH=../core/src:../agents/src:src:../orchestrator/src:../importer/src /tmp/zf164/bin/mypy --python-executable /tmp/ama-85-rv001-typeenv-ab31c480/bin/python && PYTHONPATH=../core/tests:../agents/tests:../core/src:../agents/src:src:../orchestrator/src:../importer/src:/tmp/ama-85-rv001-deps-ab31c480 /tmp/zf164/bin/python -m unittest discover -s tests -q` | Exit 0; requested mypy tool passed on 37 files with isolated dependency resolution; integrated API 477 tests run in 117.035s, OK with 97 skips; /tmp/ama-85-rv001-api-integrated.log |
| `git diff HEAD -- src/core/src/zava_forward/core/sqlstore.py src/core/src/zava_forward/core/store.py src/core/tests/test_hazard_referral.py` | Empty: upstream integration did not change the reviewed hazard implementation/regression |

## Validation Environment Correction

Use requested /tmp/zf164/bin tools and CI test-helper PYTHONPATH, extended with
the five current worktree src paths to override unrelated editable packages.
This preserves isolation without pip modification of a shared environment.
No uv. Initial correction required no installation; new upstream #313 added
pinned Playwright to api dev requirements. After its missing-import failure,
pip restored that dependency in isolated temporary target/venv locations.
Requested mypy remains /tmp/zf164/bin/mypy, using --python-executable only
for isolated third-party dependency discovery.

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

## Delivery Integration

Main advanced to a6e26fe while local validation ran. PR readiness was reverted
to draft immediately when conflict was discovered. This is upstream integration
and delivery bookkeeping, not another correction or Review loop. The hazard
transaction implementation and regression remain unchanged. Both documentation
insertions are retained, and the append-only log uses the required helper.
Full core/API suites and static gates passed again on the integrated tree:
core 325 passed, API 477 run/OK with 97 skips, ruff/format passed, mypy 71/37
files passed. No upstream feature acceptance is claimed.
