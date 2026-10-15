---
title: Changes - task-bound RAI release records
description: Issue 219 implementation and command evidence
ms.date: 2026-10-15
---

## Execution

Full plan scope P01/P02. Research Ready; one critique Complete/Revise with
PC-001 through PC-005 directly incorporated. P01 and validation complete;
documentation/index/log and phase artifacts reconciled. One Review completed:
execution Complete, outcome Not accepted. The loop is complete, not accepted
engineering delivery. Publication is a draft PR; no merge or live authority.

## Commands and Results

Commands run from repository root unless a cwd is given. Read-only views/searches
are evidence discovery, not execution validation. No private data or .env read.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current` | Clean at intake; feat/src-rai-release-record-219 |
| `gh issue view 219 --comments` and `gh issue view 219 --json title,body,comments` | Read five criteria and post-pivot owner comment |
| `gh pr list --head feat/src-rai-release-record-219 --state all --json number,state,baseRefName,url` | No prior PR |
| `gh api user --jq '{id,login}'` | Confirmed id 8036360, login jmservera |
| `gh pr view N --json number,title,state,mergedAt,baseRefName` for 296-302 | All merged into main on 2026-10-15 |
| `python3 --version` | Python 3.12.3 |
| `command -v ruff` | Missing (exit 1); chained mypy/pip probes did not execute |
| `python3 -m pip --version` | pip 26.2.1 |
| `python3 -c 'import zava_forward.core; print(list(zava_forward.core.__path__))'` | Missing installed src package (ModuleNotFoundError) |
| `ls -d .venv*` | No existing repository virtual environment |
| `git log -1 --format='%h %s'` | a2253a7, merged accountable handoff lifecycle |
| `python3 -m ruff --version; python3 -m mypy --version` | Both missing; dependency restoration justified |
| `python3 -m venv <session>/files/venv && <venv>/bin/python -m pip install -q -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'` | Exit 0; isolated pip environment, no manifests/lockfiles changed |
| `cd src/api; PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_assistant_release.py -q` (first) | 16 tests, 1 failure: old test expected the same quarantined activation after release loss. Updated to assert new disabled activation and retained historical quarantine |
| Same command (expanded first run) | 24 tests, 2 failures/1 error: new test assumptions about eligibility, case owner code and wording corrected, not production gates |
| `cd src/core; ruff check src/zava_forward/core/rai_release.py src/zava_forward/core/ai_prompts.py tests/test_rai_release.py` | Initial 9 E501 string-length errors; split strings without changing instructions. Chained format/tests/mypy did not run |
| `cd src/core; ruff format src/zava_forward/core/rai_release.py src/zava_forward/core/ai_prompts.py tests/test_rai_release.py && ruff check . && ruff format --check . && mypy && python -m unittest discover -s tests -q` | Exit 0: 303 tests, 0 failures; lint/format pass, 71 files type-checked. Existing sensor-test unclosed-file ResourceWarnings observed |
| `cd src/api; PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q > <session>/files/api-tests.log 2>&1` | Initial 480 discovered, 97 skipped, 6 failures: scripted evaluation and role-prompt tests needed explicit offline test authorization after JSON bypass closure |
| `for project in agents orchestrator importer; do (cd src/$project && PYTHONPATH=../core/tests python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy); done` (first) | Agents: 70 tests, 1 failure in separate text-task scripted harness. Loop stopped before other projects |
| Same three-project loop (after scripted harness correction) | Exit 0: agents 70, orchestrator 17, importer 39 tests; all lint/format/mypy pass (16/8/10 files). Golden datasets unchanged |
| `docker build -f src/agents/Dockerfile -t zava-forward-agents:issue-219 src` | Exit 1: permission denied connecting to unix:///var/run/docker.sock. No image/container or deployment claim |
| Release integration command above (after corrections) | 24 tests pass; then API ruff check/format/mypy pass (35 files) |
| `for project in core api agents orchestrator importer; do (cd src/$project && ruff check . && ruff format --check . && mypy); done` | All five pass; new core modules/tests included without new exclusions |
| `node --input-type=module --check < src/api/src/zava_forward/api/web/app.js` and same for `assistants.js` | Both exit 0 |
| `python tools/rename-zava-tests.py` (first) | 25 tests, 7 missing-module errors (pptx/PIL); no migration executed on repository data |
| `python -m pip install -q -r tools/rename-zava-requirements.txt && python tools/rename-zava-tests.py` | Exit 0, all 25 regressions pass. Expected corrupt-PPTX negative diagnostic emitted |
| `cd src/api; PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistants.ApiTests.test_release_record_local_http -v` (first) | 1 error: healthz is plain text, not JSON. Fixed test to read health HTTP status; chained suite did not execute |
| Same local HTTP command (corrected) | Exit 0, 1 test. Real local App responsive on ephemeral loopback; synthetic record denies with 0 provider calls, matching release allows 1 scripted call, output unapproved, unchanged domain, revocation non-actionable; listener cleaned up |
| `cd src/api; PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q > <session>/files/api-final.log 2>&1` | Exit 0: 482 discovered, 98 skipped, 0 failures in 169.489s; SQL Server conditional tests not run locally |
| Final five-project ruff check/format/mypy loop plus both JS syntax checks and `git diff --check` | All exit 0 after documentation/strong-model wiring |
| `cd src/core; python -m unittest discover -s tests -p test_rai_release.py -v` | 5 pure typed contract tests pass |
| Final release integration command after unavailable-table negative test | Exit 0: 25 tests; unavailable SQL record table logs safe diagnostic and causes 0 provider calls |
| Operational read-only commands: `git status --short`, `git diff --stat`, `git diff --numstat`, `git diff -- <changed paths>`, `git diff --check`, `wc -l docs/reference/log.md`, `tail -8 <session>/files/api-tests.log` | Scoped diff reviewed; log appended only; no prohibited paths or mvp code changed; no whitespace errors |
| Final core/API `ruff check . && ruff format --check . && mypy`, then `git diff --check && git diff --name-only -- .env .vscode .copilot-tracking/github-issues mvp && git branch --show-current` | Exit 0; 71/35 files checked, protected paths unchanged, correct topic branch |
| Review's bounded `PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python - <<'PY' ... PY` probes | Three intended invariants failed: missing-reference acceptance, historical-route reliance and stale cached denial. Exact outputs and affected paths retained in the single Review |
| Review `git diff --check`, protected-path diff, `gh issue view 219 --json body,comments`, branch PR lookup | Read-only evidence checks pass; no source/plan changes by reviewer |
| Publication safeguard `git status --short && git diff --check && gh api user --jq '{id,login}' && git remote -v` | Only task changes; privacy-safe account confirmed; origin jmservera/ama |
| `git fetch --quiet origin main && git rev-list --left-right --count origin/main...HEAD && git config --get user.name && python3 -m json.tool .copilot-tracking/rpi-sessions/2026-10-15/src-rai-release-record-219-state.json > /dev/null` | Exit 0; branch at current main (0/0), name jmservera; completed-loop state parses |
| `git diff --check && git config --local user.email 8036360+jmservera@users.noreply.github.com && git add -A`, then Conventional Commit piped to `GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -F -` | Exit 0; 4d92edf, 31 task files including all seven RPI artifacts, required Co-authored-by trailer |
| `bash <installed-pr-reference>/scripts/generate.sh --base-branch origin/main --merge-base --output <session>/files/issue219-pr-reference.xml` | Exit 0; 2,741-line diff reference generated outside repository; no duplicate Review |
| `awk '/^\| Command \| Result \|/{copy=1} /^## P01/{copy=0} copy' <changes-artifact> >> <session>/files/issue219-pr.md` | Exit 0; local command/result table incorporated into PR description |
| `git push --set-upstream origin feat/src-rai-release-record-219` | Exit 0; only topic branch pushed, remote tracking set |
| `gh pr create --draft --base main --head feat/src-rai-release-record-219 --title 'feat(core): add task-bound RAI release records' --body-file <session>/files/issue219-pr.md` | Exit 0; draft PR https://github.com/jmservera/ama/pull/315 using Refs #219 |
| `gh pr view 315 --json url,isDraft,baseRefName,headRefName,statusCheckRollup`, `git status --short`, `git log -1 --format='%h%n%ae%n%ce'` | Draft targets main from correct topic; eleven checks queued at initial publication; clean worktree; 4d92edf author and committer use confirmed privacy-safe email |

## P01 - Contract and Wiring

`rai_release.py` strictly validates the extended use/impact/evaluation contract;
existing SQL body/tables and approval routes reused. Binding includes canonical
actual prompt templates, model/use/evaluation protocol versions, existing
policy/data/provenance/permissions. Old incomplete records fail closed.

Assistant activations bind release ID/version/digest; renewal gets a fresh
release-aware activation ID. Task-wide supersession prevents routing rollback
revival; independent task releases remain unaffected. Claim, pre-dispatch,
completion, review/detail/export reliance recheck the exact record. Legacy
text/document results, cached briefings and separate priority review paths
carry/recheck the same per-invocation reference. These are implemented paths,
not accepted universal guarantees: the later Review identifies missing-reference,
current-route and cache-recovery gaps in RV-001 through RV-003.
JSON configured AI denies,
with safe visible/persisted manual-route diagnostics. OQ-017 holders remain
explicitly unknown; project contact is not appointed authority.

## P02 - Validation and Documentation

Added pure typed core contract tests and extended API release integration tests:
all 13 binding fields, omitted/invalid contract, expiry/non-finite expiry,
exercise versus actual evidence, rollback, renewal/dedup/proactive reuse,
supersession/in-flight result, cached and review denial, JSON and unavailable
SQL-store bypass controls. Existing tests retain approval/citation/permission/
consent/safety/manual-route behavior. Updated test-only scripted authorization
without changing golden evaluation datasets or production permission boundaries.

Local HTTP exercise uses real App/HTTP/SQLite and the merged nonbillable provider,
not real model inference. It also inherits the existing conditional SQL Server
API fixture used by CI. Existing checks cover dependency isolation; no agents
SQL/blob extras or dependencies added. New SQL statements use existing portable
SELECT/INSERT/UPDATE, no PRAGMA/INSERT OR/AUTOINCREMENT additions.

Updated src core/API/agents READMEs, reference index and append-only log.
Required RPI research, plan/details, critique, changes and session state will be
committed with the final review. No changes to .env, .vscode, issue mirrors,
private working data, golden evals or mvp.

## Amendments and Divergences

None requiring owner decision. Critique corrections are in the approved plan.
Local judgment: one currently active deployment per task, with separate
fast/strong expected model configuration, is simpler than deployment lists;
renewed approval explicitly supersedes task-wide. HTTP exercise is an existing
owning-suite test rather than a new script. Only two production modules and one
test module were added, below the locked budget.
Integration glue retains pre-existing migrated-module tooling exclusions;
new contract/prompt modules will be strictly checked.

## Remaining Evidence and Human Gates

OQ-017 holders/delegations and competent review unavailable. Real approved
evaluation, provider attestation, direct human oversight and Azure deployment
are not established by nonbillable synthetic tests. No acceptance checkbox
will imply those results.

## Publication

Draft PR [#315](https://github.com/jmservera/ama/pull/315) publishes commit
4d92edf and the complete RPI evidence. The draft status and explicit Review
Not accepted prevent this handoff from representing a merge-ready release.
CI was queued at initial publication; no CI pass or merge is claimed.
Publication metadata is retained in a subsequent ordinary documentation
commit on the same topic, without amending or rewriting the implementation.

## Review Handoff

P01/P02 executed. The one independent post-implementation Review is
.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md.
Execution Complete; outcome Not accepted. Passing suites do not cover the
three review-discovered states below. No second Review or in-loop source fix
is performed; the RPI one-pass contract routes these to later implementation.

| Finding | Severity | Disposition |
| --- | --- | --- |
| RV-001 | High | AI-off historical outputs lacking a release can pass None==None reliance; later rpi-implement must fail closed |
| RV-002 | High | Historical deployment passed to reliance masks current fast/strong route changes; later rpi-implement must use current route |
| RV-003 | Medium | Cached denied briefing does not recover when approval changes without a case edit; later rpi-implement must invalidate/avoid that cache |
| RV-004 | Medium residual | OQ-017/human, real model/evaluation/attestation and platform evidence remain distinct owner follow-ups |

Matching-release availability and complete material-change invalidation are
not accepted. The draft PR uses Refs #219, leaves those criteria unticked and
must not merge until the engineering defects are resolved. No user-owned
authority or evaluation was fabricated to hide this outcome.
