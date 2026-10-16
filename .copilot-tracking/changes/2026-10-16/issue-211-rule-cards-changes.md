---
title: Issue 211 implementation evidence
ms.date: 2026-10-16
---

Task: 211 / issue-211-rule-cards. Scope: full finalized plan.
Execution: implementation, local validation, single Review and authorized
publication complete. PR #324 to main; Refs #211 remains open.

## P01: Core persistence and lifecycle

Implement existing rulecards/lawstore reuse, shared locking, whole-operation
transactions and source-review notification. No real approval is created.

## P02: Authenticated HTTP boundary

Dedicated trusted principal capabilities, server identity/date, no fallback
approval authority, staff-only reads and owner-specific transitions.

## P03: Validation and delivery

Commands and results will be recorded below before publication. No Azure/Docker
resources planned. Private files are excluded from all reads and commit scope.

## Planning Dispositions

Critique ran once. PC-001/002/003 accepted; PC-004 contradicted explicit user
tooling direction and was rejected; PC-005 bounded by the one-pass Review rule.
No significant divergence or additional user decision.

## Implemented Behavior and Reconciliation

P01-T01/T02 complete: reuse the law SQL adapters, including driver-specific
IntegrityError lookup behind a shared adapter property; append-only portable
rule tables, explicit transactional IDs, whole-operation rollback and shared
connection RLock. Source ingestion joins its transaction through the private
non-committing rule review helper. Index rebuild has a separate transaction:
failed partial rebuild rolls back and unchanged retry repairs it. Immutable
snapshot blobs may remain orphaned after source failure, never overwritten.
Backend selection uses an adapter dialect rather than Python class identity,
so the lawstore CLI's __main__ module does not select SQLite for a SQL adapter.

P02-T01/T02 complete: staff law reads; trusted-proxy rule-author drafts and
rule-owner transitions; canonical provisioned email and server date; strict
capability separation, unique oid binding, no fallback/password/agent authority.
Spoofed authority fields are rejected. All cards stay exercise-only, and seeds
remain unassigned drafts. `reviews` is reserved as a card ID; draft IDs are
normalized consistently in the response.

P03-T01/T02 complete: existing test files extended, no new test files or removals.
Core/API README, knowledge-base index and append-only log updated.
Existing public lifecycle behavior is preserved; only malformed input, absent
authority and non-atomic failure behavior are tightened. Retained display-name
identity strings are not rewritten into new approval authority.

Ordinary local judgments: SQL column-size validation, reserved-route ID guard,
atomic derived-index retry and module-independent backend dialect are tightly
coupled reliability details, not scope or policy changes.

## Commands and Results (2026-10-16)

All commands run before any push. Repository root:
`/home/azureuser/source/ama-wt/issue-211`. `PYTHONPATH` entries constructed from
`$PWD` are absolute at execution. No private inputs were opened.

### Initial targeted checks

```bash
cd src/core
PYTHONPATH=$PWD/src:$PWD/tests python3 -m unittest discover -s tests -p test_rulecards.py -q
```

Passed 11 existing tests. After implementation, the same command passed 17 tests.
`/tmp/zf164/bin/ruff check .`, `/tmp/zf164/bin/ruff format --check .`,
`/tmp/zf164/bin/mypy` each passed in core: 28 formatted files, 81 checked
source files under existing config.

```bash
cd src/api
export PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests
python3 -m unittest tests.test_auth tests.test_lawstore tests.test_role_endpoint_inventory -q
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
/tmp/zf164/bin/mypy
```

Passed 82 tests, 13 skips initially; after the provision rollback case, passed
84 tests, 14 skips. API tooling passed: 13 formatted files, 42 source files.

### Tooling and missing-package recovery

```bash
test -x /tmp/zf164/bin/mypy && test -x /tmp/zf164/bin/ruff
/tmp/zf164/bin/mypy --version
/tmp/zf164/bin/ruff --version
```

Existing tools found: mypy 2.4.0, ruff 0.17.1. No venv creation was needed.

The first full core suite ran 398 tests with two missing installed-distribution
metadata errors; API ran 532 tests with one equivalent missing API metadata
error and 103 skips. Neither was a lifecycle/authorization test failure.
The following recovery was attempted only after those missing-dependency errors:

```bash
/tmp/zf164/bin/pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/api
```

Failed because the existing tooling venv lacked setuptools. Retried using pip's
isolated build dependency mechanism, without changing dependency manifests:

```bash
/tmp/zf164/bin/pip install --no-deps -e src/core -e src/agents -e src/api
```

Passed, installing local editable core/agents/API 0.1.0. Source egg-info metadata
is ignored and is not part of the commit. No `uv`, global install or dependency
relaxation was used.

### Full local suites after metadata restoration

```bash
cd src/core
PYTHONPATH=$PWD/src:$PWD/tests python3 -m unittest discover -s tests -q
/tmp/zf164/bin/mypy
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
```

Passed 398 tests, no skips, 130.542 seconds. Mypy, ruff and format check passed.
Pre-existing ResourceWarnings for unclosed sensor test CSVs were emitted; no
unrelated test code was changed.

```bash
cd src/api
export PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests
python3 -m unittest discover -s tests -q
/tmp/zf164/bin/mypy
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
```

Passed 532 tests, 103 skipped, 243.963 seconds. Mypy, ruff and format check
passed. These existing environment/opt-in skips mean live SQL Server, Azure,
optional Blob SDK and browser acceptance are not claimed.

### Running local app and final refinements

```bash
cd src/api
PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests \
  python3 -m unittest tests.test_auth.RuleHttpTests -q
```

Passed 6 tests, 7.956 seconds. Starts an actual loopback ThreadingHTTPServer
over temporary synthetic fixtures, verifies `/healthz` and `/app` respond, then
executes drafts, independent approval, activation, hold, release, retirement,
immutable history and restart. Negative cases cover caller spoofing, dual-role
self-approval, every owner action with wrong authority, missing CSRF, anonymous,
contractor, agent, email fallback and password-provider writes. The server is
shut down and joined; temporary fixture directories are automatically cleaned.
This is parser/server-boundary evidence, not hosted signature verification.

After the full suites, bounded refinements added portable column limits and
backend dialect selection, then exercised true partial-index rollback and
canonical/reserved card IDs. Final targeted evidence covers those changes:

```bash
cd src/core
PYTHONPATH=$PWD/src:$PWD/tests python3 -m unittest discover -s tests -p test_rulecards.py -q
/tmp/zf164/bin/mypy
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
```

Passed 17 tests (1.038 seconds) and all tooling. The same 17-test command also
passed immediately before the final index/route refinements.

```bash
cd src/api
export PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests
python3 -m unittest tests.test_auth.RuleHttpTests tests.test_lawstore -q
/tmp/zf164/bin/mypy
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
```

Passed 40 tests, 14 skipped (43.562 seconds), plus all tooling. This explicitly
checks committed source/review evidence survives a partial index failure and
the connection successfully accepts an unchanged retry. The wider 84-test
auth/law/inventory selection also passed before these final bounded refinements.

### Repository and documentation checks

`git diff --check` passed throughout; Markdown/relative links reviewed.
`git status --short` showed only the intended source/docs and dated artifacts.
`git check-ignore` confirmed generated core/API egg-info is excluded.
`gh issue view 211 --comments`, issue JSON and `gh issue view 209 --json
body,comments` confirmed the scope, src migration and named exercise owner;
no card approval was inferred.
`gh api user --jq '{id,login}'` returned id 8036360, login jmservera.
The branch was clean at intake and matches the requested topic; origin/main
was 8f00623. No prior PR existed for this branch.

## Validation Boundaries and Remaining Acceptance

Existing migrated modules/test files retain their repository mypy exemptions
and ruff format exclusions; successful project commands do not imply a new
strict typing or formatting pass for those legacy files.
SQL Server DDL is locally contract-tested, not executed against a live server.
The existing opt-in SQL Server law suite now cleans up rule tables and replays
source-change behavior, but remains skipped here. No Docker or Azure command
was necessary; no resources were created.

Unmet operational criteria: actual tenant role definitions/assignments (the
current infrastructure registration script/manifest still declares only
workbench roles), human approval of individual cards, current-source legal
interpretation/owner sign-off, SQL Server/Azure/hosted-ingress acceptance.
UI and deterministic rule engine are outside this slice. Refs #211, not Closes.
No approval is invented for Juan Manuel Servera or any other person.

## Handoff

Implementation, plan/details, validation and the single post-implementation
Review are reconciled. P03-T03 publication completed in PR #324. No
implementation restart or second Review was required.

## Single RPI Review

Review execution: Complete. Outcome: Conformant for the local labelled exercise
slice. Canonical record:
.copilot-tracking/reviews/logs/2026-10-16/issue-211-rule-cards-review.md.
No implementation defects or unaccepted decision gaps were established.

The reviewer inspected all twelve tracked-file diffs and the canonical phase
artifacts, then performed a bounded in-memory Python compatibility experiment
using `git show HEAD:src/core/src/zava_forward/core/rulecards.py` as the pre-change
implementation. Pre-change synthetic rows/approval/review were loaded, current
initialization repeated twice, all four retained tables/history/reviews compared,
v2 added and append-only rejection confirmed. An initial strict comparison
correctly detected the changed derived exercise label; persisted evidence and
all other fields were unchanged. Corrected comparison passed. This check is
review-observed evidence, not a newly committed regression test or a full rerun.
Reviewer `git diff --check` also passed.

RV-001 through RV-004 are Low residuals, not local implementation defects:
explicit tenant capability definitions/assignments; live platform/ingress
acceptance; human approval of specific cards; separate UI/engine work. They are
routed to distinct future work, not silently treated as completed or executed
inside this loop. Human approval remains unchecked/unperformed.

## Publication and Final State

Authenticated GitHub identity rechecked as 8036360 / jmservera.
`git config --local user.email 8036360+jmservera@users.noreply.github.com`
and local user name configured; author and committer email explicitly set
for the commit and verified with `git show -s --format='%h %ae %ce'`.

`git commit` created 2678443 (`feat: bind exercise rule cards to authenticated
approval roles`) with `Refs #211` and the required Copilot co-author trailer.
All twelve implementation/docs files plus the seven dated RPI artifacts were
included. No secrets, private files, generated metadata, `.vscode`, `.env` or
`.copilot-tracking/github-issues` were staged.

`git push -u origin feat/src-rule-cards-211` succeeded, without force.
`gh pr create --base main --head feat/src-rule-cards-211 --title
'feat: authenticated exercise rule cards and approval workflow (Refs #211)'
--body-file <session-files>/issue-211-pr-body.md` succeeded:
https://github.com/jmservera/ama/pull/324.
`gh pr view --json number,url,state,baseRefName,headRefName,isDraft` confirmed
OPEN, non-draft, base main, correct topic head. The body lists commands,
results, intermediate metadata recovery, all artifacts and unmet criteria.
This evidence-only completion handoff is committed and pushed on the same PR.
No main push, merge, history rewrite, new review or new work item was performed.

Task complete; automatic session remains running at Follow-up awaiting an
owner-selected next item. Ranked choices: dedicated tenant capability definition/
assignment (RV-001), live platform/ingress acceptance (RV-002), specific-card
human approval (RV-003). Stop automatic session and switch to manual mode
remain available; no follow-up has been started without selection.
