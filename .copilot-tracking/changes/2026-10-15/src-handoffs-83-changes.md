---
title: Issue 83 implementation evidence
ms.date: 2026-10-15
---

Task #83 / src-handoffs-83. Declared scope: full bounded plan.
Plan and details in their canonical 2026-10-15 directories; one critique
executed and PC-001 to PC-004 disposed by planning parent.

## P01/P02 Implementation

Complete. Core WorkflowMixin records versioned return/reopen provenance,
requires source and next action for every new write, and derives authority and
receiving owner from authenticated user/current case, never request overrides.
Legacy persisted history remains unchanged and renders unknown values.

Preserved Offered/Declined storage with canonical Sent/Rejected status. Added
Received, Escalated and Completed; recipient-only receipt/accept/reject,
sender/manager-only withdrawal/manual escalation, named-manager escalation
target, and accepting-owner-only completion. Only acceptance transfers ownership.
All transitions append deep-copied versioned snapshots and existing audit events.
Accepted unfinished work cannot be overwritten.

Legacy hand_over and suggestion buttons now offer instead of immediately
assigning. Removed the redundant immediate-handover form. Queue/detail distinguish
accountable owner, destination, proposed/confirmed receiver, chase owner, urgency,
UTC due date, next action and independent resident-update responsibility.
Pending commitments survive transitions/replacement offers and cannot silently
change. Need-role projection covers free text and contractor/unknown-role denial.
Existing coordination-assistant triggers include all unaccepted states;
proposal/release/consent/safety authority is unchanged.

Added two typed test modules (16 JSON/SQLite semantics, five loopback HTTP
contracts), plus five CI-only SQL Server replays in the existing mssql suite.
No test removals. Existing successful return/reopen regressions now supply
explicit synthetic source/next-action values. API mypy resolves core source;
new harnesses permit calls into migrated untyped interfaces without suppressing
their own type errors. Updated API/core guides, reference index and append-only
log. No runtime dependency, SQL schema, deployment or mvp code change.

## Commands and Results

Read-only intake:

* `git status --short && git branch --show-current`: clean, feat/src-handoffs-83.
* `gh issue view 83 --comments`; `gh issue view 83 --json title,body,comments`:
  three unticked criteria, one owner src-pivot comment.
* `gh pr list --head feat/src-handoffs-83 --state all --json number,state,baseRefName,url`:
  no prior PR.
* `gh pr view N --json title,body,mergeCommit` for N=296,297,298,299,300,301,302:
  merged migrations/dispatch inspected.
* `git log -1 --oneline`: f593555 baseline.
* `python3 --version && python3 -m pip --version`: Python 3.12.3, pip 26.2.1.
* `command -v ruff`, `command -v mypy`, `python3 -m ruff --version`,
  `python3 -m mypy --version`: missing tools.
* `gh api user --jq '{id,login}'`: confirmed owner id/login and noreply address.
* `python3 -m venv .venv && .venv/bin/python -m pip install --quiet -e 'src/core[dev]' -e src/agents -e src/api -e src/orchestrator -e src/importer`:
  passed; pip-only local editable install after missing-tool failures.
* Baseline loop, each project:
  `(cd src/$project && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q)`:
  core 261 passed; agents discovery failed because shared test_dependency_rule
  shadowed owning tests. Corrected path ordering, not a source failure.
* Corrected baseline loop for agents/orchestrator/importer/api:
  `(cd src/$project && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q)`:
  70/17/39/459 passed (API 92 skips). Total baseline 846.
  Existing core sensor fixture ResourceWarnings retained; no unrelated fix.

Implementation checks, corrections and reruns (all from the assigned worktree):

| Command | Observed result |
| --- | --- |
| `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest -q test_workflows test_ui_support test_role_endpoint_inventory && node --check src/zava_forward/api/web/app.js` | 44 passed, JS syntax passed |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -p test_handoff_lifecycle.py -v` | Initial 16 tests: six subcase errors in repeated resident-update fixture setup; corrected replacement fixture semantics, not enforcement |
| `cd src/core && ../../.venv/bin/ruff check tests/test_handoff_lifecycle.py && ../../.venv/bin/mypy` | Initial ruff failure: import order and five loop-lambda bindings; fixed before mypy ran |
| `.venv/bin/ruff check --fix src/core/tests/test_handoff_lifecycle.py src/api/tests/test_handoff_api.py` | First run fixed import, found one long assertion; split it, rerun passed |
| `.venv/bin/ruff format src/core/tests/test_handoff_lifecycle.py src/api/tests/test_handoff_api.py` | Two new modules formatted; subsequent reruns unchanged |
| `(cd src/core && ../../.venv/bin/python -m unittest discover -s tests -p test_handoff_lifecycle.py -q) && (cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest -q test_handoff_api test_workflows test_ui_support test_role_endpoint_inventory)` | 16 + 49 passed after fixture correction |
| `(cd src/core && ../../.venv/bin/mypy) && (cd src/api && ../../.venv/bin/mypy)` | First core run found unresolved absolute `dataset` import. Switched to namespace fixture import. Core then passed; API found explicit fixture export, core source resolution and heterogeneous request-body type issues. Added explicit fixture re-export, core mypy source path and `dict[str, object]` annotation; both passed |
| `cd src/core && ../../.venv/bin/mypy && ../../.venv/bin/python -m unittest discover -s tests -p test_handoff_lifecycle.py -q` | Passed typing and 16 tests |
| `cd src/api && ../../.venv/bin/mypy && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest -q test_handoff_api` | Passed typing and five HTTP tests, repeated after fixture/path correction |
| `node --check src/api/src/zava_forward/api/web/app.js` | Passed, repeated after coherent UI changes |
| `docker build -f src/api/Dockerfile -t zava-forward-handoffs-83:local src` | Not runnable locally: permission denied connecting to `/var/run/docker.sock`; CI image job required |
| `.venv/bin/python tools/rename-zava-tests.py` | Initial 25 tests had seven missing pptx/PIL dependency errors |
| `.venv/bin/python -m pip install --quiet -r tools/rename-zava-requirements.txt && .venv/bin/python tools/rename-zava-tests.py` | Restored existing pinned tooling after missing-dependency failure; 25 passed |
| All-project loop below, first full candidate | Core 277, API 464 (92 skipped), agents 70, orchestrator 17, importer 39; all ruff/format/mypy passed. Later final contract added five guarded SQL Server replays |
| `node --check src/api/src/zava_forward/api/web/app.js && (cd src/core && ../../.venv/bin/python -m unittest discover -s tests -p test_handoff_lifecycle.py -q) && (cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest -q test_workflows test_handoff_api test_ui_support test_accessibility_baseline test_design_system)` | 16 + 45 passed after mandatory core provenance and duplicate UI removal |
| Final all-project loop, first attempt | Core 277 passed; ruff/format passed; mypy flagged one empty-list test variable annotation. Added `tuple[object, ...]`; no production change |
| Final quality/remaining-project loop below | Core quality tools passed; API 469 (97 skipped), agents 70, orchestrator 17, importer 39 passed; all project ruff/format/mypy passed |
| `git diff --check`, `git diff --stat`, `git diff --numstat`, `git status --short --untracked-files=normal` | Whitespace clean, scoped implementation/docs/artifacts only; task-created `.venv` kept out of staging |

The all-project command was:

```bash
for project in core api agents orchestrator importer; do
  (cd "src/$project" &&
    PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q &&
    ../../.venv/bin/ruff check . &&
    ../../.venv/bin/ruff format --check . &&
    ../../.venv/bin/mypy) || exit
done
```

After the final core-only type annotation correction, its quality gates were
rerun, followed by the same remaining-project loop for api/agents/orchestrator/
importer. Final total: 872 discovered, 775 passed, 97 skips (92 baseline plus five new CI-only
SQL Server HTTP replays). No failed final local gate. Existing migrated modules
retain pre-existing lint/type exemptions; this is not a claim that the entire
legacy implementation is strictly typed.

## Local App and Browser Evidence

Started the actual App/HTTP server with the new synthetic fixture harness:

```bash
cd src/api
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -u - <<'PY'
import threading
from test_handoff_api import HandoffApi
app = HandoffApi()
app.setUp()
print('Synthetic-only smoke app:', app.base, flush=True)
try:
    threading.Event().wait()
finally:
    app.doCleanups()
PY
```

Observed responsive loopback app at `http://127.0.0.1:37717`, welcome/workbench
HTTP 200, synthetic password login 200. No private dataset, model endpoint,
external sending or billable service was used or configured.

Playwright tools: navigate to `/`, login via same-origin `/api/login`, navigate
to `/app#/case/ZF-1`; set `#ho-to`, `#ho-note`, `#ho-next`, `#ho-urgency`; click
"Offer the case"; inspect UI and API. Sent showed Sam as accountable/chase owner,
unconfirmed receiver. Sign in as Rae; click "Record receipt (not acceptance)":
Received retained Sam and hid duplicate receipt. Sign in as Sam; fill escalation
reason and click "Record manual escalation": Escalated named Pam, retained Sam.
Manager queue also returned Escalated, Sam accountable/chase, null confirmed
receiver. Sign in as Rae; click "Accept this case": Accepted changed owner and
confirmed receiver to Rae, exposing completion control. Fill `#ho-done`, click
"Complete handoff": Completed retained Rae and hid repeat completion. Exact
history: Sent, Received, Escalated, Accepted, Completed.

Filled `#ret-to` Funding check, reason, synthetic source and next action; clicked
"Send back". Observed Funding check, version 1, source "Synthetic report 83",
authenticated Rae identity/role, receiving owner Rae and next action "Review
funding evidence", visible in history. This is engineering browser evidence,
not human usability/accessibility conformance or real model effectiveness.
One initial public-page console resource error was not used as workflow evidence.

## Amendments and Divergences

PC-001 simplified receiving owner to existing accountable owner; no return/reopen
selection path. PC-004 disposition follows one-review rule: in-scope review
defects would block passing acceptance and require draft publication.
No new schema, dependency or model task is planned.

Current-state refinement: new core return/reopen writes require source and next
action too, not just HTTP writes. Only persisted legacy history remains unknown.
This closes an otherwise incomplete enforcement surface without inventing
provenance; updated the four successful legacy regression calls with explicit
synthetic references. Removed the redundant immediate-handover UI form in favour
of the canonical handoff panel; legacy endpoint and suggestion buttons offer only.

## Acceptance and Remaining Work

* [x] Return/reopen metadata local evidence.
* [x] Distinct handoff states and named accountability local evidence.
* [ ] Approved-time operational escalation: excluded, OD-09 unresolved.
* [ ] SQL Server/image CI evidence.
* [ ] Live Azure/model and human acceptance: not run/claimed.

## Review Handoff

One bounded post-implementation Review executed: Complete, outcome Residual
work; no in-scope correctness/permission defect found. Canonical record:
`.copilot-tracking/reviews/logs/2026-10-15/src-handoffs-83-review.md`.
RV-001 routes approved timing to owner/Programme planning; RV-002 routes image/
SQL Server CI to PR maintainer and separately authorized live evidence to
owner/Digital. No second Review or child implementation in this loop.
Implementation and local validation are complete. Publication is parent-owned.
Operational timing, real SQL Server/image CI, live AI/Azure and human acceptance
are explicit residuals, not claimed local successes. Use Refs #83, not Closes.

## Final Repository Checks

* `git diff --check`: passed after review.
* Focused `git diff`/source comparison covered workflow, store, projection,
  assistant eligibility, HTTP/UI wiring, tests and tooling configuration.
* `git diff --name-only -- mvp .env .vscode .copilot-tracking/github-issues`:
  empty. Added-core-SQL scan found none of INSERT OR REPLACE/IGNORE,
  AUTOINCREMENT or PRAGMA.
* Python standard-library check of state JSON/artifact paths and local link
  targets in API/core guides and reference index: passed.
* Synthetic smoke app stopped with `stop_bash(handoff-smoke)` after successful
  responsive browser checks. Task-created `.venv` is excluded from staging.
* `gh api user --jq '{id,login}'` rechecked account; repository-local
  `git config --local user.email 8036360+jmservera@users.noreply.github.com`
  and `git config --local user.name jmservera` set for private-email-safe
  author/committer. Assigned branch rechecked; no main write or merge.

## Publication

Pending authorized topic-branch commit/push and PR creation. Review permits a
bounded non-closing PR; issue criterion 3 stays unticked. CI image/SQL Server
results must be checked on GitHub, not inferred from local skips.
