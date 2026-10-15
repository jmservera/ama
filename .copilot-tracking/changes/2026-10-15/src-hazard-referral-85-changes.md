---
title: Hazard referral implementation evidence
description: Changes, commands, results and acceptance limits for issue 85
ms.date: 2026-10-15
---

Task 85, src-hazard-referral-85. Scope: full bounded engineering plan.
Plan/details/critique use the same date and slug.

## P01 Core accountability

Implemented P01-T01 in the existing core WorkflowMixin and case-body storage:
immutable report source/awareness and authenticated actors, separately evidenced
sent/received/accepted states, sender follow-up, explicitly home-scoped hold,
external response/update observations and independent evidenced retrofit-only
release. No SQL or workload dependency was added.

PC-001 preserves closed-record safety intake without reopening/changing
retrofit state, ownership or consent. PC-002 adds forward-only legacy binding,
retaining original referral/repair history and unknown awareness rather than
fabricating receipt. PC-003 removes newly emitted same-day policy and
service-resolution claims, preserving historical ledger entries.

Controlled sign-off, instruction/reissue/correction, booking/completion and
quality acceptance/handover now check the existing active safety restriction.
Other household, building, consent and funding gates stay independent.
Previously unknown external response/update times remain recordable after
retrofit restart, so releasing this restriction does not close the hazard
service's continuing response/update work.

Fourteen semantic tests execute the same contract on JSON and SQLite, including
restart, actor/index/replay refusals, legacy states, AI outage, closed records,
all controlled progression paths and protected narratives/model sources.
New typed test modules use only the existing narrowly scoped permission to call
the migrated untyped store interface; no lint exclusions were added.

## P02 Staff surfaces

Implemented P02-T01: existing hazard HTTP actions now require the documented
source/evidence, plus new receive/accept/times actions. The server supplies
actor/scope and ignores forged authority. Updated safety panel exposes
closed-record intake, separate evidence, destination/follow-up, accountable
scope/role, times/unknowns and an independent restart decision. Staff wording
uses "stopped retrofit work", preserving the content standard rather than
exposing internal "hold" terminology.

Three loopback application tests start ThreadingHTTPServer on 127.0.0.1 with
wholly fictional home/staff records and SQLite state. They verify responsive
health/static endpoints, authenticated lifecycle, source/scope authority,
roles, legacy continuation and restart durability. This is an actual local
application run, not a browser/human, real-model, SQL Server or Azure run.

Related legacy test payloads now supply mandatory evidence. The existing
role-matrix work-order exercise uses a separate synthetic copy of its
privacy-canary home without an active safety restriction; it does not remove
or release the canary home's existing hazard. Duplicate work-order probes
target that same new fixture, preserving the role/isolation assertions.
The copy audit permits only the new internal `x.hold` identifier, not visible
"hold" wording. New source/evidence redaction is scoped to hazard narratives,
without hiding unrelated categorical quality/document sources.

## P03 Commands and Results

All commands run from the supplied worktree unless a component directory is
specified. File read/search/edit tools are recorded through the resulting
source/artifact diff; executable command invocations are recorded below.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current && gh issue view 85 --comments && gh pr list --head feat/src-hazard-referral-85 --state all --json number,state,baseRefName,url` | Exit 0; clean specified branch, no existing PR. Default issue display printed no content, so explicit JSON retrieval followed. |
| `gh issue view 85 --repo jmservera/ama --json title,body,comments` | Exit 0; four unchecked criteria, no comments returned. |
| `gh pr view N --json number,state,title` for N=296..302 (296 also `mergeCommit`) | All exit 0 and MERGED; reused current src implementation. |
| `python3 -c "import zava_forward.core, ruff, mypy; print('installed packages available')"` | Exit 1, missing installed `zava_forward`; restore editable packages/tools in isolated venv with pip. |
| `git log -5 --oneline` | Exit 0; current branch includes merged building #310 and handoff #311. |
| `gh api user --jq '{id,login}'` | Exit 0; id 8036360, login jmservera; requested noreply identity verified. |
| `python3 --version && python3 -m venv /home/azureuser/source/ama-wt/issue-85/.venv && .venv/bin/python -m pip install --quiet --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator -e src/importer && .venv/bin/python -m pip install --quiet 'ruff==0.17.1' 'mypy==2.4.0'` | Exit 0; Python 3.12.3, editable packages and tools restored using pip only; no runtime SQL/blob dependency added to agents. |
| `../../.venv/bin/ruff check tests/test_hazard_referral.py --fix && ../../.venv/bin/ruff format tests/test_hazard_referral.py tests/test_buildings.py && ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_referral.py' -q` (initially from repo root) | Exit 127: incorrect relative tool path. Corrected by changing to src/core. |
| `cd src/api && ../../.venv/bin/ruff check tests/test_hazard_api.py --fix && ../../.venv/bin/ruff format tests/test_hazard_api.py && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_api.py' -q` | Initial run exit 1, 3 tests/1 legacy fixture failure. Formatting passed. |
| `cd src/core && ../../.venv/bin/ruff check tests/test_hazard_referral.py --fix && ../../.venv/bin/ruff format tests/test_hazard_referral.py tests/test_buildings.py && ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_referral.py' -q` | Exit 1 at lint: 2 new long lines. Formatting first resolved both. |
| `cd src/api && ../../.venv/bin/ruff format tests/test_hazard_api.py && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_api.py' -q` | Diagnostic rerun exit 1, 3 tests/1 legacy fixture failure. The HTTP error was missing hazard index, not transport. |
| `cd src/core && ../../.venv/bin/ruff format tests/test_hazard_referral.py tests/test_buildings.py && ../../.venv/bin/ruff check tests/test_hazard_referral.py && ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_referral.py' -q` | Formatting/lint passed; tests exit 1, 12 tests/1 failure plus 4 legacy-state subtest errors. Synthetic direct edits bypassed SqlStore's touched-case tracking. Fixed fixtures to use the existing _case hook before save, not production persistence. |
| `cd src/core && ../../.venv/bin/ruff format tests/test_hazard_referral.py && ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-core-tests.log) | Exit 0, 310 tests passed in 100.824s. Existing sensor fixture ResourceWarnings only. |
| `cd src/api && ../../.venv/bin/ruff format tests/test_hazard_api.py && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-api-tests.log) | Exit 1, 475 tests: 3 failures, 1 error, 99 skipped. Coupled content wording and shared role-fixture assumptions required updates for the newly enforced safety restriction. |
| `for project in core api agents orchestrator importer; do (cd src/$project && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy); done` | All ruff checks passed. Initial core mypy had 2 lambda inference errors; all other project types passed. The exploratory loop's shell exit was 0 despite those errors; it is not counted as a passing core type gate. Replaced default-argument lambdas with typed functools.partial and reran fail-fast. |
| `for project in agents orchestrator importer; do (cd src/$project && PYTHONPATH=../core/tests ../../.venv/bin/python -m unittest discover -s tests -q) || exit; done; docker info --format '{{.ServerVersion}}'` | agents 70/70, orchestrator 17/17, importer 39/39 passed. Docker probe exit 1: permission denied connecting to /var/run/docker.sock. |
| `cd src/core && ../../.venv/bin/ruff format tests/test_hazard_referral.py && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy && ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_referral.py' -q` | Exit 0, all core tools passed and 12 hazard tests passed. |
| `.venv/bin/python tools/rename-zava-tests.py && git diff --check && git status --short && node --check src/api/src/zava_forward/api/web/app.js` | Initial exit 1: migration suite ran 25 tests with 7 errors because python-pptx/Pillow were missing; later chained checks did not execute on this attempt. |
| `docker build -f src/api/Dockerfile -t zava-forward-api:issue-85 src` | Exit 1: permission denied connecting to Docker API. No image was built; CI owns image/runtime/scan checks. No elevated permissions or shared daemon changes attempted. |
| `tail -24 docs/reference/log.md && git diff --stat && git diff --check && node --check src/api/src/zava_forward/api/web/app.js` | Exit 0; inspected append point, clean whitespace and valid JavaScript syntax. |
| `.venv/bin/python -m pip install --quiet python-pptx pillow pyyaml && .venv/bin/python tools/rename-zava-tests.py` | Exit 0, all 25 migration regressions passed; expected broken.pptx rejection is a test fixture. Missing test dependencies restored with pip only. |
| `grep -A 24 '^ERROR:' /tmp/ama-85-api-tests.log` and `git diff -- src/core/src/zava_forward/core/workflows.py src/core/src/zava_forward/core/projection.py src/core/src/zava_forward/core/store.py` | Exit 0; diagnosed work-order fixture hitting the newly enforced restriction and reviewed coupled authority/projection changes. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-api-tests-final.log) | Exit 1, 475 tests: 4 failures, 99 skipped. A role test created an extra work order when its duplicate probe still targeted the original rather than the separate unaffected fixture; fixed that probe. |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-core-tests-final.log) | Exit 0, 310 tests passed in 87.640s before adding the post-restart external-update regression. |
| `for project in core api agents orchestrator importer; do (cd src/$project && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy) || exit; done; node --check src/api/src/zava_forward/api/web/app.js && git diff --check` | Exit 0 on both subsequent all-project runs. mypy checked core 69, api 36, agents 16, orchestrator 8, importer 10 files. All ruff checks/formats, JavaScript syntax and whitespace passed. |
| `cd src/core && ../../.venv/bin/ruff format tests/test_hazard_referral.py && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy && ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_referral.py' -q && cd ../api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p 'test_hazard_api.py' -q && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy && node --check src/zava_forward/api/web/app.js` | Exit 0; final targeted core 14/14, HTTP synthetic app 3/3, core/API lint/format/types and JavaScript syntax passed. |
| `git diff --check && git status --short && head -8 docs/reference/research/ux/content-standard.md && git diff --numstat && git status --short -- mvp .env .vscode .copilot-tracking/github-issues` | Exit 0; excluded paths unchanged. Only this task's source/docs/tracking and generated local venv appeared. Venv will be removed, not committed. |
| `grep -A 21 '^FAIL:' /tmp/ama-85-api-tests-final.log && git check-ignore .venv/bin/python || true` | Exit 0; diagnosed shared fixture failures and confirmed venv is untracked, requiring explicit cleanup. |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-core-complete.log) | Exit 0, final full core suite 312/312 passed in 70.914s, including 14 new hazard semantic tests. Existing sensor-file ResourceWarnings only. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q` (output redirected to /tmp/ama-85-api-complete.log) | Exit 0, final full API suite ran 475 tests in 155.845s, OK with 99 environment/optional-integration skips. Three new loopback synthetic application tests passed; authentication-denial logs are expected negative tests. |
| `PYTHONPATH=src/core/tests .venv/bin/python - <<'PY' ... PY` (complete executable body in the canonical Review's Parent Reproduction Command) | Exit 0 reproduced RV-001: two actual SqlStore instances persisted a Completed work order after a concurrent emergency hold, with safety_raised before workorder_completed. This demonstrates a defect, not passing enforcement. |
| `.venv/bin/python -m json.tool .copilot-tracking/rpi-sessions/2026-10-15/src-hazard-referral-85-state.json > /dev/null && git diff --check && gh api user --jq '{id,login}'` | Exit 0; valid durable state, clean whitespace and verified requested noreply identity. |
| `python3` relative-link check over changed tracked Markdown (git diff --name-only, Markdown relative target existence) | Exit 0; 301 relative file links checked, all exist. Anchor targets manually reviewed for new headings. |
| `git diff --check && test -s .gitignore && test ! -L /home/azureuser/source/ama-wt/issue-85/.venv && rm -r -- /home/azureuser/source/ama-wt/issue-85/.venv` | Exit 0; removed only the local venv created for this task, not repository/user content. |
| `rm -- /tmp/ama-85-core-tests.log /tmp/ama-85-api-tests.log /tmp/ama-85-core-tests-final.log /tmp/ama-85-api-tests-final.log /tmp/ama-85-core-complete.log /tmp/ama-85-api-complete.log && git config --local user.email 8036360+jmservera@users.noreply.github.com && git status --short` | Exit 0; own temporary logs removed after outcomes were persisted; repository-local safe email configured. No excluded paths changed. |
| `git add -A && git diff --cached --check && git diff --cached --stat` followed by exact Conventional Commit message piped to `git commit -F -` with safe author/committer email environment | Exit 0; implementation/evidence commit `58c6b39`, 32 files, required Co-authored-by trailer, both emails verified as 8036360+jmservera@users.noreply.github.com. |
| `python3` generation of PR body from canonical changes command table and Review reproduction | Exit 0; 18710-character body stored only in session files, explicitly Not accepted and not merge-ready. |
| `git push -u origin feat/src-hazard-referral-85 && gh pr create --repo jmservera/ama --base main --head feat/src-hazard-referral-85 --draft --title 'feat(core): evidence hazard referrals and retrofit holds (Refs #85)' --body-file /home/azureuser/.copilot/session-state/20c846f3-50a6-4526-84fd-673f414a769c/files/issue-85-pr.md` | Exit 0; topic pushed, draft PR https://github.com/jmservera/ama/pull/314 opened to main. No push to main, no merge. |
| `gh pr view 314 --repo jmservera/ama --json number,url,isDraft,baseRefName,headRefName,headRefOid,state && gh pr checks 314 --repo jmservera/ama --json name,state,bucket,link && git status --short && git log -1 --format='%h %ae %ce%n%B'` | Exit 0; OPEN draft on correct head/base, clean tree, safe author/committer/trailer. Eleven observed checks in progress: five src projects, src-namespace/no-working-data, test, validate, image, mssql. No CI pass or rubric score asserted. |

## Amendments and Divergences

No material scope divergence. New stricter evidence prerequisites intentionally replace
legacy unaudited repair/release actions; coupled tests/UI will change together.
Prospective legacy reconciliation preserves the original record and never
fabricates historic receipt or acceptance.

## Remaining Work and Acceptance

P01-T01, P02-T01 and P03-T01 complete. All five src suites and lint/format/type
checks passed locally; migration suite and local synthetic HTTP app passed.
One Review executed Complete with outcome Not accepted. Implementation and all
RPI artifacts committed/pushed, draft PR #314 opened; only final delivery-state
bookkeeping is being committed. No source corrections or second Review follow.
Owner timing/escalation policy,
verified repairs transport, real model/SQL Server/Azure and human acceptance
remain unavailable; do not mark full issue acceptance or activate live controls.

## Issue Acceptance Boundary

Local engineering evidence covers all four issue-shaped behaviors, but these
original issue criteria remain unticked for operational acceptance:

* [ ] Retrofit tooling only creates or links a hazard case: local link-only
  behavior tested; real hazard-service contract/transport not verified.
* [ ] Referral sent, received and accepted are separately evidenced: local
  human-recorded evidence is distinct; actual service receipts not independently
  produced or verified.
* [ ] Hold scope and release decision are recorded against the accountable role:
  local whole-home role/decision evidence tested; operational authority and
  human acceptance not ratified.
* [ ] Hazard response and resident-update times are visible: external
  observations/unknowns tested; approved timing/escalation policy and live
  service source not available.

Mandatory real-platform application evidence (permitted actual AI, SQL Server
durability and Azure deployment) has not been produced. Existing AI proposal/
release/human-review controls remain wired and unchanged, not forcibly enabled
or disabled. No private data, live controls or Azure resources were touched.

## Single Review Outcome and Routed Follow-up

Canonical review:
`.copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md`.
RV-001 is a reproduced High concurrency defect: a second SqlStore can record an
active home hazard between a procurement safety check and its committing write,
allowing work-order completion afterward. Sequential passing tests do not prove
this boundary. A distinct later implementation must add transactional dependent
case validation and a two-store regression across affected procurement actions.
This RPI loop does not fix findings or repeat Review.

RV-002 routes operational responsibility/release/timing decisions to later
planning; RV-003 routes verified transport and real AI/SQL Server/Azure/human
evidence to later research/validation. No child was selected.
The PR must be draft, use Refs #85, and prominently state Not accepted and not
merge-ready. This is incomplete product delivery, not a passed safety gate.

## Delivery

Draft PR: https://github.com/jmservera/ama/pull/314, base main,
head feat/src-hazard-referral-85. First implementation/evidence commit 58c6b39.
The final documentation-only bookkeeping commit records these completed
operations and is pushed without amendment or history rewriting; its exact
commit/push result is persisted in the PR body after execution to avoid a
self-referential commit record.
Automatic RPI task execution is completed at Follow-up, session remains running
awaiting an owner-selected follow-up/Stop/manual mode. No follow-up was selected
in this non-interactive run. RV-001 blocks acceptance/merge; original issue
criteria and live/owner evidence remain open.
