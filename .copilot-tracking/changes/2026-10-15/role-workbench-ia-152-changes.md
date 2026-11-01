---
title: Role workbench IA 152 changes
description: Implementation and command evidence for shared workbench IA
ms.date: 2026-10-15
---

## Execution Scope

Current invocation: bounded RV-001 follow-up on PR #317, related to P01-T02
and PC-003. Reuse the existing browser harness to hold the initial briefing
through My cases -> All cases -> My cases, prove failure before the fix, then
repair only its request/cache lifecycle in `src/api`. Update this ledger,
the original review disposition and PR body without repeating Review.
Run the requested absolute-PYTHONPATH API suite, CI design-system browser
entry point, `/tmp/zf164/bin/mypy .`, ruff lint and format checks. Preserve
the open device decision and full AC-034/043 gates. No new product decision,
private-data access, deployment or dependency change is intended.

Regression-first evidence: `/tmp/zf164/bin/python -m
checks.workbench_browser_check` with the requested absolute PYTHONPATH first
failed because the sanitized server subprocess could not import the local
namespace packages. Restored missing editable installs with
`/tmp/zf164/bin/python -m pip install --no-deps -q -e src/core -e src/agents
-e src/api`; no manifests changed. Rerun against unchanged app.js reached the
held briefing and failed `cancelled briefing retried on each queue return`.
This is the expected RV-001 failure, not a passing regression.

Full plan for task `152`, slug `role-workbench-ia-152`. Implementing P01 then
P02 on the specified branch. Research Ready; one critique executed and all
six dispositions recorded in plan/details. No owner decisions inferred.

## Intake and Environment Commands

* `git status --short && git branch --show-current`: clean initial worktree,
  branch `feat/src-role-workbench-ia-152`.
* `gh issue view 152 --comments`; `gh issue view 152 --json title,body,url`;
  `gh issue view 152 --json body --jq .body`: five unchanged criteria, src
  pivot and shared-IA scope confirmed. Later body read used `head -150`.
* `gh pr list --head feat/src-role-workbench-ia-152 --state all --json number,state,baseRefName,headRefName,url`:
  no existing PR. `git log -6 --oneline`: baseline a48d502 includes #313.
* `gh pr view 313 --json title,body,mergeCommit` and `--json body --jq .body`:
  merged Fluent foundations available. `for n in 296 297 298 299 300 301 302;
  do gh pr view "$n" --json number,title,state,mergedAt; done`: merged moves.
* `gh api user --jq '{id,login}'`: authenticated account matches required
  privacy-safe identity, id 8036360.
* `command -v python3; command -v ruff; command -v mypy;
  python3 -c 'import playwright; import zava_forward.api; print("installed packages available")'`:
  Python present; tools absent; import failed `ModuleNotFoundError: playwright`.
* `ls -d .venv src/api/.venv 2>/dev/null; python3 --version; git status --short;
  git check-ignore ...research.md`: Python 3.12.3, no existing venv, new tracking
  visible/not ignored (final check exit 1).
* `python3 -m venv .venv && .venv/bin/python -m pip install -q
  -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]'
  -e 'src/orchestrator[dev]' -e 'src/importer[dev]'`: pass, pip only.

## P01/P02 Implementation

Completed P01-T01/T02 and P02-T01/T02/T03 engineering/documentation scope.
New typed API navigation descriptor, `/api/me` metadata, no new client role
map. Own/programme scope, current nav, skip link, full reset, back context,
request cancellation, explicit errors and expanded early safety details.
Token-based wrapping preserves named scrollable wide tables. No SQL, permission,
deployment, resident consent or model release changes.

Added one API module, one unit test file, one browser check and JSON manifest.
Existing isolated browser launcher is reused by callback, and its CI entry
point executes both suites. Scratch is under ignored root `.venv/`; subprocess
environment excludes credentials/private data/model/deployment settings.
Existing Finance/proposal/time catch paths now ignore cancelled old views;
map requests capture route lifetime, clear stale results and expose failures.

API README, UX synthesis, reference index and append-only log updated. No edits
to `.env`, `.vscode`, issue-sync tracking, memory, original case or `mvp/`.

## Validation

All commands below run in the specified worktree. `PY` is written out as
`.venv/bin/python` in root commands, `../../.venv/bin/python` inside projects.

| Command | Result |
| --- | --- |
| `.venv/bin/python -m playwright install chromium` | Pass; existing development-only dependency and browser restored after missing-tool failure |
| `cd src/api && ../../.venv/bin/python -m checks.workbench_browser_check` | First run reached five widths, then failed because inline style injection violates the application's CSP. Replaced test-only inline style tag with CSSOM root-font setting; did not relax CSP |
| `.venv/bin/ruff check src/api/src/zava_forward/api/workbench.py src/api/tests/test_workbench.py` | Pass |
| `.venv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 src/api/checks/design_system_browser_check.py src/api/checks/workbench_browser_check.py` | Initially import/line/closure findings; corrected. Final run passes without exemptions |
| `.venv/bin/ruff format --isolated --line-length 100 src/api/src/zava_forward/api/workbench.py src/api/tests/test_workbench.py src/api/checks/design_system_browser_check.py src/api/checks/workbench_browser_check.py` | Formatted new browser check; other three unchanged |
| `node --check src/api/src/zava_forward/api/web/app.js` | Pass |
| `cd src/api && ../../.venv/bin/python -m checks.workbench_browser_check` (second run) | Reached reset then callback failed: Playwright supplies Request as second positional argument. Corrected closure capture, not production behavior |
| `for project in core agents api orchestrator importer; do (cd "src/$project" && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q) || exit; done` | Core 325 pass in 120.541s; then agents discovery failed because globally supplied fixture paths shadowed its test_dependency_rule. Corrected command to documented per-project paths |
| `for project in core agents api orchestrator importer; do (cd "src/$project" && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy) || exit; done` | Initial core/agents pass, API mypy found Any return in new browser IDs helper. Added runtime list/string guard. Final full five-project run passes: core 71, agents 16, API 40, orchestrator 8, importer 10 checked files |
| `for project in agents api orchestrator importer; do (cd "src/$project" && if [ "$project" = api ]; then export PYTHONPATH=../core/tests:../agents/tests; elif [ "$project" = orchestrator ]; then export PYTHONPATH=../core/tests; fi && ../../.venv/bin/python -m unittest discover -s tests -q) || exit; done` | Agents 70 pass (6.609s), API 480 run: 383 pass/97 skipped (148.206s), orchestrator 17 pass, importer 39 pass. Total 931 tests: 834 pass, 97 expected SQL Server skips |
| `.venv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 --fix src/api/checks/design_system_browser_check.py src/api/checks/workbench_browser_check.py` | Fixed import order, left two long lines; manually split. Final strict lint pass |
| `.venv/bin/ruff format --isolated --line-length 100 --check src/api/checks/design_system_browser_check.py src/api/checks/workbench_browser_check.py` | Final pass, two formatted files |
| `cd src/api && ../../.venv/bin/python -m checks.workbench_browser_check` (third run) | All staff paths passed; contractor expected order was wrong in independent fixture oracle. Existing server ranks hazard first even in the minimal contractor projection; corrected expected IDs to ZF-4, ZF-1 without changing runtime policy |
| `docker build -f src/api/Dockerfile -t zava-forward-api:issue-152 src` | Blocked: permission denied connecting to unix:///var/run/docker.sock. No sudo, daemon change or alternate deployment |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -v 2>&1 \| grep -E 'skipped\|Ran \|^OK'` | API 480 run: 383 pass/97 skipped (127.002s); all skips require disposable SQL Server with ZF_TEST_MSSQL=1 |
| `cd src/api && ../../.venv/bin/python -` (local Store inspection, see below) | Confirmed existing contractor IDs ZF-4 then ZF-1; output contains only constructed fixture fields |
| `.venv/bin/ruff format --isolated --line-length 100 src/api/checks/workbench_browser_check.py src/api/checks/design_system_browser_check.py` | Final formatting pass |
| `cd src/api && ../../.venv/bin/mypy && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p test_workbench.py -q` | Pass, 40 typed files and 3 new navigation/manifest unit tests |
| `cd src/api && ../../.venv/bin/python -m checks.design_system_browser_check` | Initial combined run exposed scrollable table regression: broad inherited anywhere-wrap removed expected horizontal scrolling. Narrowed normal-wrap to `.table-scroll table`, retaining narrow case wrapping |
| `cd src/api && ../../.venv/bin/python -m checks.design_system_browser_check` (next run) | All baseline visual/keyboard checks reached final assertion, which detected unhandled cancelled map requests. Bound map requests to original route lifetime and explicitly handle cancellation/failure |
| `cd src/api && ../../.venv/bin/python -m checks.workbench_browser_check` (intermediate run) | Caught 320px case overflow from broad table normal-wrap during the correction; final scoped table rule fixes both surfaces |
| `cd src/api && ../../.venv/bin/python -m checks.design_system_browser_check` (final combined run) | Pass, both complete browser suites; Chromium 156.0.8078.4. Baseline 505-home map/tokens/forced colours/reduced motion/scrollable table and >50-row return; IA eight auth roles, fixed queues/navigation, five widths, 200% root text, safety-first form order, filter/back/reset, old-response cancellation, history, load failure, expiry and unchanged case |
| `for file in src/api/src/zava_forward/api/web/*.js; do node --check "$file" || exit; done` | Pass, every first-party script |
| `git diff --check` | Pass |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_workbench test_design_system test_accessibility_baseline test_ui_support test_role_matrix -q` | Named-module invocation failed because, unlike discovery, it does not add `tests/` to the module path |
| `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_workbench test_design_system test_accessibility_baseline test_ui_support test_role_matrix -q` | Final targeted regression pass, 34 tests in 4.136s |
| `git diff --check && git status --short && find .venv -maxdepth 1 -type d -name 'zf-browser-*' -print && git ls-files mvp && git diff --numstat` | Pass; no browser scratch remains, only `mvp/README.md` tracked and no mvp edit |
| `tail -35 docs/reference/log.md && git diff --stat && git status --short` | Reviewed append point and scope; found root venv not yet ignored, added exact root ignore |

The first suite loop printed project labels with `printf`; labels are omitted
from table commands above without changing executed test semantics. Repeated
lint loops for `api orchestrator importer` passed after the helper correction.
The Store-inspection heredoc imported `synthetic_data`, created a
TemporaryDirectory under `../../.venv`, wrote `synthetic.json`, opened Store,
and printed `s.list_cases(s.staff['contractor@example.test'])` IDs and
`s.page_cases(u)['items']`; its owned scratch was removed.

Existing core tests emitted ResourceWarning for unclosed sensor test fixture
files; no test failed. Their existing temporary-data behavior was not modified.
Browser-owned processes were health-checked and terminated in finally; no
private dataset or actual provider endpoint was used.

## Issue Acceptance Disposition

* [ ] Supported devices and widths decided with owner: no decision invented.
* [x] Layout checks at defined engineering widths including 320 CSS px.
* [x] Navigation describes existing permitted queues, defaults to own scope,
  no role simulator. Broad directories remain explicitly labelled and existing
  access is not narrowed or expanded by this work.
* [x] Existing permitted safety content remains expanded; no responsive hiding.
* [ ] Full cross-profile AC-034/043 acceptance: partial manifest/evidence only.

Implemented checks do not turn the PRD's global Not run criteria into accepted
product requirements. Use Refs #152, not Closes.

## Amendments and Divergences

Local judgment: callbacks/CSSOM tests corrected after tool failures; cancelled
map/Finance/proposal/time root views handled as a directly coupled consequence
of request lifetime. No new product decision or second critique. Added exact
root venv ignore to keep local tooling/fixtures untracked. Full previous row
focus/scroll/pagination restoration is explicitly not delivered; returned queues
restart page one. This is the documented partial UX-07 boundary.

## Review Handoff

Ready for one post-implementation Review of the bounded shared-IA slice.
Research/plan/details/critique/changes agree; no introduced failure is knowingly
open. Publication follows Review; no merge or actual-platform success claimed.

## Single Review Outcome and Publication Disposition

Review subsequently executed Complete, outcome Defects found. This supersedes
the pre-Review readiness statement above. A new real-app delayed-briefing
scenario reproduces RV-001: the cached briefing request is aborted during
mine/all/mine navigation, but the reused box remains "Reading your cases..."
without a retry. Ordinary case controls still work. No post-Review source fix
or repeated Review is performed; that repair is the highest-ranked distinct
follow-up. Publish a draft PR, not an accepted/ready slice.

Review record:
`.copilot-tracking/reviews/logs/2026-10-15/role-workbench-ia-152-review.md`.
RV-002 owner devices, RV-003 full manifest/row recovery and RV-004 live/human
evidence remain open. The three engineering checkboxes above do not waive the
introduced assistance-recovery defect or complete full acceptance.

Review commands/results:

* `git --no-pager diff -- src/api/src/zava_forward/api/web/app.js` and a
  separate diff of CSS/index/launcher/server/panels/assistants/timecapture:
  inspected complete production diff. Initial combined diff was too large,
  so it was reread in these two bounded calls.
* `python3 -` relative-link/state check: parsed relative links in
  `src/api/README.md`, reference index and UX synthesis; all file targets exist.
  State JSON passes duplicate-key rejection.
* `cd src/api && ../../.venv/bin/python -` Review heredoc: imported shared
  `main` and `synthetic_data`, launched Chromium and real synthetic API,
  intercepted `**/api/briefing`, logged in Sam, waited for rows, navigated All
  cases then My cases, printed held request count/heading/loading counts,
  released old response, printed heading count. Result: healthy server; one
  request total before/after return, one heading and one loading placeholder
  after return; no new request when obsolete response released. This is
  reproducible RV-001 evidence, not a passing regression. All owned resources
  cleaned in finally/context managers.

Publication preflight:

* `git status --short && git branch --show-current`: only this task's files,
  branch `feat/src-role-workbench-ia-152`; prohibited paths unchanged.
* `gh api user --jq '{id,login,name}'`: authenticated id `8036360`, login
  `jmservera`. `git config --local user.email
  8036360+jmservera@users.noreply.github.com` and readback: privacy-safe address.
* `gh pr list --head feat/src-role-workbench-ia-152 --state all --json
  number,state,url`: no existing PR.
* `git fetch origin main --quiet && git rev-list --left-right --count
  origin/main...HEAD && git diff --check`: base advanced one commit since
  task intake (`1 0`), whitespace clean. No merge, rebase, force push or main
  write is authorized/performed; CI will assess the PR against current main.
* PR-template glob: no template found; description derives from canonical
  changes and the one completed Review, without an extra Review pass.

The lifecycle is complete through one Review; this is not product acceptance.
Parent state is Follow-up/completed, automatic session running without a
selected child. Publication is explicitly authorized by the original request.

## Publication Results

* Explicit `git add` of the 24 task paths followed by `git -c
  user.email=8036360+jmservera@users.noreply.github.com commit -F -`: pass,
  `35f29a6`, Conventional Commit and required coauthor trailer.
* `git push --set-upstream origin feat/src-role-workbench-ia-152`: pass,
  only the named topic branch published.
* `gh pr create --draft --base main --head feat/src-role-workbench-ia-152
  --title 'feat(api): add shared role workbench IA and responsive layout'
  --body-file <session>/files/issue-152-pr-body.txt`: pass,
  https://github.com/jmservera/ama/pull/317. Generated body includes this
  entire command ledger, not only a link.
* `gh pr view 317 --json number,url,isDraft,baseRefName,headRefName,
  mergeStateStatus,statusCheckRollup`: verified draft/main/named-topic;
  `DIRTY`, empty checks. `git log -1 --format=...` verified both author and
  committer privacy-safe email and final coauthor trailer. `git diff
  origin/main...HEAD --name-only` confirmed only the intended 24 paths.
* `git merge-tree --write-tree HEAD origin/main`: exit 1, read-only merge
  analysis identifies only `docs/reference/log.md` as conflicting. No worktree,
  ref or history is altered and no actual merge/rebase/force-push is performed.
* `gh run list --branch feat/src-role-workbench-ia-152 --limit 5 --json
  databaseId,name,event,status,conclusion,url`: empty. `gh pr view 317 --json
  mergeable,mergeStateStatus,statusCheckRollup`: `CONFLICTING`/`DIRTY`, no checks.
  **CI has not run**; it is not a passing CI claim.

Publication blocker PUB-001: current main advanced during this task and its
append-only reference-log entry conflicts with this topic's appended entry.
An explicitly authorized branch reconciliation must preserve both entries
before PR CI can evaluate the merge. No permission to merge/rebase work or
rewrite history is inferred. The draft records this in addition to RV-001.

Final evidence synchronization updates only this ledger and parent state,
clarifies 931 run = 834 passed + 97 skipped, then uses an ordinary second
Conventional Commit with the same privacy-safe identity/trailer and a normal
topic push. It does not alter the completed Review or source.

* Evidence sync commit `efa6141` and normal topic push succeeded. Its preceding
  `python3 -` state-schema assertion failed because PUB-001 was accidentally
  inserted in `confirmed_decisions` rather than `blockers`; the shell continued
  to the separate commit command. Corrected that metadata location in a new
  commit without amending history. Re-run uses fail-fast shell execution and
  asserts exact blocker IDs, decision shape, unique keys and artifact existence.

## Open Acceptance and Evidence

Owner device/browser support, full eleven-profile/nine-workflow journey,
human/screen-reader checks, real model/SQL Server/Azure remain unproven.
Offline synthetic checks do not satisfy actual inference acceptance.

## RV-001 Follow-Up Result on PR #317

RV-001 is fixed. This later user-authorized implementation supersedes the
historical open-defect/publication status above without repeating Review.
Only production code, tests and the component guide under `src/api` changed;
the review disposition and existing tracking evidence are reconciled separately.

`aiBox` captures each load's route signal, registers a pending-request abort
listener that synchronously invalidates only that box's cache, and unregisters
it when the request settles. Completed briefings remain cached across routes.
Late cancelled responses cannot mutate the replacement panel. Non-abort
failures show an alert and retry instead of silently removing assistance.
API guide documents the recovery boundary. No rights, model configuration,
human approval or resident consent gates changed.

The existing workbench browser check holds the first briefing before login
completes, navigates mine/all/mine, requires one new request per route, fulfills
the newest response, then releases obsolete responses. It checks recovered
content, one panel, no stale/loading content, completed-cache retention, and
failure/retry with workflow-only mode preserved. Its request-count assertion
failed without the production fix and passes with it.

| Command | Result |
| --- | --- |
| `cd src/api && PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests python3 -m unittest discover -s tests -q` | Pass: 498 run, 400 passed, 98 skipped, 126.171s |
| `cd src/api && /tmp/zf164/bin/python -m checks.design_system_browser_check` | Pass twice after production fix; final run includes explicit failure/retry test. Both complete suites; Chromium 156.0.8078.4, no uncaught JS errors |
| `cd src/api && /tmp/zf164/bin/mypy .` | Pass: 40 source files |
| `cd src/api && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check .` | Pass: 11 files formatted |
| `cd src/api && /tmp/zf164/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/design_system_browser_check.py checks/workbench_browser_check.py` | Initial additional strict check found local-import ordering and an unbound loop capture in the new callback; corrected both. Final pass |
| `cd src/api && /tmp/zf164/bin/ruff format --isolated --line-length 100 --check checks/design_system_browser_check.py checks/workbench_browser_check.py` | Pass: two files formatted |
| `cd src/api && node --check src/zava_forward/api/web/app.js` | Pass |
| `git fetch origin && git rev-list --left-right --count HEAD...origin/main` | `5 0`: main already merged by pre-existing topic commits f879827 and 84ca1d0. PUB-001 is resolved; no additional merge needed at this check |
| `gh api user --jq '{id,login}'` | Authenticated id 8036360, login jmservera; required privacy-safe email matches |
| `git diff --check` | Pass |

Existing browser launcher checked its owned loopback server health and
terminated browser/server processes and temporary synthetic fixtures.
Pip was used only to restore missing editable imports after observed failure;
no uv, dependency changes or private data access. No `.env`, `.vscode`,
issue-sync-tracking or `mvp/` changes; no properwarm.json read.

RV-001 is no longer an open implementation blocker. RV-002 supported-device
decision, RV-003 complete AC-034/043/recovery acceptance and RV-004 live/human
evidence remain open. Preserve all related unchecked acceptance gates, draft
status and Refs #152. No second Review, full acceptance or main write.

## Review follow-up 2026-11-01 (PR 659 Copilot threads)

* Refreshed stale `workbench` and `navigation-tests` SHA-256 pins in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`; `test_scenario_manifest` and `test_needs_inventory` pass, ruff clean.
* `activation` check failure is a GitHub API rate-limit in the daily AIC cache restore (infrastructure, not code); not fixable here.
