---
title: Resident decisions changes and validation
description: Issue 86 implementation evidence, commands, results and limits
ms.date: 2026-10-15
---

Task: issue-86 / resident-decisions-86. Declared scope: full P01-P03 plan.
Implementation and single Review complete; PR #319 published. Mergeability
and hosted CI are blocked by newer-main conflicts, not reported as passed.
No deployment or private data access authorized.

## Intake and Research Commands

* `git status --short && git branch --show-current`: clean at intake, expected
  feat/src-resident-decisions-86. `gh pr list --head
  feat/src-resident-decisions-86 --state all --json number,state,baseRefName,url`:
  no previous PR. `gh api user --jq '{id,login}'`: 8036360 / jmservera.
* `gh issue view 86 --comments`: exit 0 but no rendered output on this host.
  `gh issue view 86 --comments --json title,body,comments`: exit 1; CLI does not
  permit both options. Corrected `gh issue view 86 --json title,body,comments`:
  four criteria, no comments. No post-pivot comments exist in returned data.
* `for n in 296 297 298 299 300 301 302; do gh pr view "$n" --json
  number,title,state,mergedAt; done`: all merged 2026-10-15.
* `python3 --version`, `python3 -m pip --version`: Python 3.12.3, pip 26.2.1.
  `command -v ruff && command -v mypy`: tools absent from PATH.
  `python3 -m ruff --version`, `python3 -m mypy --version`: missing modules.
  `python3 -c 'import zava_forward.core, zava_forward.api; ...'`: namespace
  missing. These failures justify pip installation in an isolated venv.
* `git log -4 --oneline`, `git log -1 --format=%cs`, repeated
  `git status --porcelain=v1`: current baseline includes #314; latest commit
  reports 2026-10-16, while task artifact date retains caller date 2026-10-15.
  Only this task's artifacts were untracked after research.

## P01: Core Semantics and Guards

Plan final-candidate critique executed once. Six direct dispositions are in
the plan. Implementation uses existing case bodies, no schema changes.

Implemented scoped context revisions, supplied-source answer versions and
measure review flags; versioned representatives with current task/date/contact
checks; independent review linked to the actual contested actor. Shared resident
guards cover case advance, explicit work-order bindings and QA/handover. SQL
guards revalidate inside the existing transaction without dialect/schema changes.
Privacy projections detach histories and hide authority narratives. Legacy
case-wide answers remain historical and cannot release new scoped works.

Immediately relevant wiring: list filters, status cards and model source labels
now use the same conservative scoped status, not the legacy answer. The SQL
missing-decision filter evaluates live case state because authority expiry can
occur without a row write. This deliberately uses the existing in-memory list
path for that one filter; indexed other filters remain unchanged.

## P02: API, UI and Test Evidence

Existing resident endpoint dispatches the new actions. UI answers and answered-by
start blank; legacy answer editor removed, historical value clearly labelled.
Work-order issue/reissue/correction forms require explicit measure/revision
bindings. No data generated from contact or prefilled resident answers.
Two new test modules cover JSON/SQLite semantics, stale dependency refusal,
privacy persistence, synthetic enabled model adapter and actual local HTTP app.
Affected historical tests now supply explicit synthetic design/source/consent
fixtures and bindings instead of relying on aggregate acceptance. No tests removed.

## Validation

* `python3 -m venv .venv && .venv/bin/python -m pip install -q -e
  'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e
  'src/orchestrator[dev]' -e 'src/importer[dev]'`: exit 0.
* Initial `../../.venv/bin/python -m unittest discover ...` from repository
  root: exit 127 (wrong cwd). Corrected to `cd src/core` first.
* `.venv/bin/ruff check src/core/tests/test_resident_decisions.py`: four
  line-length findings; formatter invocation was initially behind `&&` and did
  not run. `.venv/bin/ruff format ... && .venv/bin/ruff check ...`: pass.
* `node --check src/api/src/zava_forward/api/web/{app,panels,ops}.js` (three
  individual commands): all exit 0.
* From core, `../../.venv/bin/python -m unittest discover -s tests -p
  test_resident_decisions.py -q`: 15 pass, both JSON and SQLite.
* Initial five-suite loop used API's shared-fixture PYTHONPATH for every
  project: core failed on old unscoped fixtures plus legacy governance refusal
  precedence; api 477 tests, 2 failures/8 errors/97 skipped (same fixture gaps
  and banned visible word "holds"); agents collection failed due to inherited
  core `test_dependency_rule` path; orchestrator 17 pass, importer 39 pass.
  Corrected fixture provenance/bindings, preserved governance check precedence,
  changed wording to "stops", and use project-specific PYTHONPATH below.
* From core, targeted discover runs: resident 15 pass, quality/procurement 21
  pass, finance/signoffs 29 pass; building initially 2 errors because sibling
  fixture replaced required evidence. Corrected the fixture to preserve explicit
  source documents rather than weakening the technical check.
* From api, `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python
  -m unittest discover -s tests -p test_resident_api.py -q`: 2 pass. Actual
  loopback server binds an ephemeral port, /healthz and /app respond, authenticated
  decisions/withdrawal/redress/authority/privacy work and SQL state reopens.
* Initial project-quality loop (`ruff check . && ruff format --check . &&
  mypy` per project): core 2 typing errors, api 6 typing errors; agents,
  orchestrator and importer pass. Corrected typed fixture annotation, partial
  instead of an uninferable lambda, and API payload dictionary annotations.
* `docker info --format '{{.ServerVersion}}'`: exit 1, permission denied for
  /var/run/docker.sock. Local image build/run is blocked; no permission escalation.
* From core, `PYTHONPATH=tests ../../.venv/bin/python -m unittest
  test_buildings test_hazard_referral test_quality_procurement
  test_finance_signoffs test_resident_decisions test_governance -q`: 115 pass.
* API targeted module command with `tests.test_*` and no `tests` on PYTHONPATH:
  32 run, 2 collection errors (`import test_mvp` in migrated harness). Corrected
  next invocation to use `tests` in PYTHONPATH and bare module names.
* Corrected core and api `ruff check . && ruff format --check . && mypy`:
  both pass (72 and 38 source files respectively). No broad new exemptions;
  typed test harnesses only allow calls to existing untyped migrated boundaries.

* Corrected API targeted invocation with `PYTHONPATH=tests:../core/tests:../agents/tests`
  and bare modules: 57 pass.
* First corrected full-suite loop: core 340 pass; api 479 run, 97 skipped,
  one error; agents 70 pass; orchestrator 17 pass; importer 39 pass. API
  `test_document_controls.ScanTests.test_pending_rescans_on_read_and_by_job`
  tried to rescan metadata-only SYN-EPC from the new explicit readiness fixture.
  Marked only those synthetic fixture metadata records clean with scanner
  `Synthetic metadata fixture`; no production scanner behavior was changed.
* Added explicit per-quality-record resident bindings. A withdrawn measure does
  not block acceptance/handover of its independent sibling; unknown/unbound
  evidence can be recorded but cannot authorize release.
* `.venv/bin/ruff format src/core/tests/test_resident_decisions.py
  src/core/tests/building_fixture.py`: one reformatted, one unchanged.
  Core `PYTHONPATH=tests ../../.venv/bin/python -m unittest
  test_resident_decisions test_quality_procurement test_buildings
  test_hazard_referral -q`: 65 pass. Core ruff/format/mypy pass.
* API `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python
  -m unittest test_document_controls test_resident_api test_role_matrix
  test_workflows -q`: 43 pass. API ruff/format/mypy pass.
* Final all-project loop used the following exact per-project suite commands
  from each `src/{project}`, followed by
  `../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . &&
  ../../.venv/bin/mypy`:

  | Project | Suite command prefix and runner | Result | Ruff / format / mypy |
  | --- | --- | --- | --- |
  | core | `../../.venv/bin/python -m unittest discover -s tests -q` | 342 pass, 60.017s | Pass / 19 files / 72 files |
  | api | `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q` | 479 run, 97 skipped, 131.684s, pass | Pass / 10 files / 38 files |
  | agents | `../../.venv/bin/python -m unittest discover -s tests -q` | 70 pass, 5.229s | Pass / 11 files / 16 files |
  | orchestrator | `PYTHONPATH=../core/tests ../../.venv/bin/python -m unittest discover -s tests -q` | 17 pass, 0.042s | Pass / 5 files / 8 files |
  | importer | `../../.venv/bin/python -m unittest discover -s tests -q` | 39 pass, 0.140s | Pass / 11 files / 10 files |

* Final direct transaction inspection found resident dependency cleanup duplicated
  at lock exit instead of at successful save. Moved the duplicate to successful
  save and added a nested-lock regression. Re-ran full core command above:
  **343 pass**, 58.538s; ruff/format/mypy pass. API
  `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python
  -m unittest test_resident_api test_document_controls -q`: 16 pass, 7.303s;
  API ruff/format/mypy pass.
* From api, `../../.venv/bin/python -m checks.design_system_browser_check`
  (initial and final invocations): pass. Chromium 156.0.8078.4 checks 320/390/1280px
  reflow, keyboard scrolling/Enter/Space, forced colours, reduced motion, status
  text/geometry and no uncaught JavaScript errors. This is existing synthetic
  browser evidence, not new resident usability acceptance or live inference.
* `for project in core api agents orchestrator importer; do .venv/bin/python
  -m "zava_forward.$project"; done`: five expected 0.1.0 entrypoints, exit 0.
  Namespace Python assertion: `zava_forward.__file__ is None` and five namespace
  paths, pass. Existing dependency-rule tests pass in the full project suites.
* `node --check` for each of `app.js`, `panels.js`, `ops.js`: pass.
  `.venv/bin/python -m json.tool` for the RPI state: pass.
  `git diff --check`: pass. `git diff --name-only -- .env .vscode mvp
  .copilot-tracking/github-issues`: empty; forbidden paths and mvp untouched.
* `git status --short && git branch --show-current && git diff --stat`:
  expected branch and task-only changes plus local untracked `.venv/`.
  `gh pr list --head feat/src-resident-decisions-86 --json number,state,url`:
  none. `gh api user --jq '{id,login}'`: 8036360 / jmservera.

## Documentation and Plan Reconciliation

Updated existing core/API guides, reference routing index and append-only log.
Details now match the research decision that every legacy aggregate answer is
history: aggregate refusals cannot override newer scoped choices or block an
independent sibling. QA bindings are per-record, not a case-wide hold. These
clarifications preserve issue #86's isolation requirement and critique PC-001.
No source move, SQL schema, dependency/image, regulatory or memory change.

Local test environment and raw logs are temporary and will not be staged.
The persistent command/result evidence is this artifact and the PR description.
Review and publication results follow.

## Review

Exactly one post-implementation RPI Review executed, Complete; outcome
Residual work. Canonical record:
.copilot-tracking/reviews/logs/2026-10-15/resident-decisions-86-review.md.
No implementation defect established within the bounded assessment. RV-001
operational policy, RV-002 actual complaints/human acceptance and RV-003 actual
runtime/container evidence remain distinct follow-ups; no second implementation
or Review pass was started. Refreshed `gh issue view 86 --json title,body,comments`
still returns the same four criteria and no comments.

The RPI task is completed in Follow-up; automatic session remains running,
awaiting selection after the explicitly authorized publication. No child work
is selected or started.

## Publication and Hosted Blocker

* Added-relative-link check using Python pathlib/re over added Markdown links:
  all five new relative targets exist.
* `git config --local user.email 8036360+jmservera@users.noreply.github.com &&
  git config --local user.name jmservera &&
  git config --local --get user.email`: requested noreply identity configured.
  Author and committer were also explicitly set to that address at commit.
* `git fetch origin main --quiet && git rev-list --left-right --count
  origin/main...HEAD`: two base-only commits, zero topic commits before commit.
  `git log --oneline HEAD..origin/main`: #315 task-bound RAI releases and #316
  stock/fabric migration. No merge/rebase/history rewrite was authorized or done.
* `git add -- src/core src/api docs/reference/README.md docs/reference/log.md`
  plus the seven exact task research/plan/critique/details/changes/review/state
  paths; `git diff --cached --check`: pass. Staged stat: 34 files,
  2,485 insertions/97 deletions. Staged forbidden-path/venv diff: empty.
* `printf ... | GIT_AUTHOR_NAME=jmservera GIT_COMMITTER_NAME=jmservera
  GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com
  GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -F -`:
  success, ee649f0, `feat(src): bind resident decisions to scope and representative authority`,
  required Copilot co-author trailer included. `git log -1` verified both identities.
* `bash .../skills/shared/pr-reference/scripts/generate.sh --base-branch
  origin/main --merge-base --output .venv/resident-pr-reference.xml`: success,
  3,492 lines. This temporary assembly evidence does not start another Review.
  No PR template found in .github, docs or repository root. PR body and evidence
  mapping are persisted under .copilot-tracking/pr/.
* Python combined the PR description and full command/result record, omitting
  YAML frontmatter: initial body 19,618 characters.
* `git push -u origin feat/src-resident-decisions-86`: success, new topic branch,
  upstream set. No push to main, force push, merge or deployment.
* `gh pr create --base main --head feat/src-resident-decisions-86 --title
  'feat(src): enforce scoped resident decisions and representative authority'
  --body-file .venv/resident-pr-body.md`: success,
  https://github.com/jmservera/ama/pull/319. Body uses Refs #86.
* `gh pr view 319 --json number,url,state,baseRefName,headRefName,mergeable,
  mergeStateStatus,statusCheckRollup`: OPEN, main base, expected topic head,
  CONFLICTING/DIRTY, no checks. `gh pr checks 319`: no checks reported.
* `git merge-tree --write-tree --name-only HEAD origin/main`: exit 1,
  read-only branch/worktree diagnostic. Conflicts are docs/reference/log.md,
  src/api/README.md, src/core/README.md and
  src/core/src/zava_forward/core/ai_tasks.py. Worktree/index/branch not merged.
  Rechecked PR: still CONFLICTING/DIRTY with no hosted checks.
* Final delivery metadata is committed with the same noreply identity/trailer
  and pushed with `git push origin feat/src-resident-decisions-86`; PR body is
  refreshed using `gh pr edit 319 --body-file .venv/resident-pr-body.md`.
  Exact remote head and retained Refs/no-closing-reference state are verified
  after push. No source changes or repeated Review occur during closeout.
* Temporary worktree-local `.venv/` and its raw logs/XML/body are removed after
  publication; only explicitly staged source, docs and durable artifacts enter
  the PR. Final `git status --short` must be empty.

Publication succeeded, but PR readiness is **blocked**. The requested owner
merge boundary prevents silently incorporating newer main or choosing a rebase.
Owner-authorized integration must reconcile #315/#316, resolve the four files
and rerun affected validation before CI/merge. Hosted CI is unavailable, not
passed; no local image or release evidence is invented.

## Unmet Acceptance and Follow-Up

Formal complaint integration, human accessibility/without-detriment testing,
operational authority/retention ratification, authorized real inference and
actual SQL Server/Azure execution are not evidenced by local fixtures.
