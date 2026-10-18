---
title: Issue 76 current-stage blockers changes
description: Actual implementation, validation and publication evidence
ms.date: 2026-10-18
---

## Execution Boundary

Task 76; full approved plan. Ordered RPI and publication complete; first gate was
P01-T01, all new defect
tests red before production edits. No source correction cycle used. Exact base
6c1e376ff1241316272df22a5a3a6853aae9f87b. Research baseline preserved: eight
semantic failures through real JSON Store and SQLite SqlStore, exit 1.
Existing base suites passed 25 core/SQL tests and 3 real loopback API tests.
Initial system Python failed for missing zava_forward; then task-local pip
installed editable core[dev,sql], agents, api[dev]. No other installer used.

## Original Critique

Exactly one execution, verdict Revise, three Medium findings. All directly
disposed in plan/details before implementation; no second critique.
SHA-256:
31e254f7de129957080e78d751f63ccac157d43f18ef2270f30cd4422e8bd1a7.
Original immutable path:
.copilot-tracking/reviews/plans/2026-10-18/issue-76-current-stage-blockers-critique.md.

## Validation Environment

Remaining commands run from repository root unless component cd is shown:
env -i PATH="$PATH" HOME="$PWD/.venv" TMPDIR="$PWD/.venv/issue76-tmp"
with installed .venv/bin/python and test-only PYTHONPATH as recorded.
tempfile.gettempdir() verified absolute workspace-local scratch. Original
research used ordinary synthetic OS temporary directories; no private datasets.
No model calls, billable inference, cloud writes, private environment files or
support reads. Docker available with local mssql/server:2022-latest image.

## P01-T01 Red Evidence

All six new methods executed before production edits. Initial test run exposed
test-harness errors (nonexistent stock method, missing Store-initialized funding
field in replacement case, SQL modifications not marked through _case). Original
red.txt retained, not counted as semantic proof. Corrected harness used existing
stock_reconcile, preserved funding and marked modified cases through _case.
red-harness-corrected.txt: six tests, 38 assertion failures, zero errors.
Current-hold positive control passed; exact-source diff was empty before both
runs. Upgrade assertion failed on stale certified old-format flags, not on
missing revision symbol. These are pre-source harness refinements, not source
correction cycles.

Exact red command (both receipts differ only in output filename):

```bash
git diff --exit-code -- src/core/src src/api/src &&
env -i PATH="$PATH" HOME="$PWD/.venv" TMPDIR="$PWD/.venv/issue76-tmp" \
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
test_taskqueues.StoreQueueParity.test_current_stage_requirements_through_real_stores \
test_taskqueues.StoreQueueParity.test_current_holds_keep_membership_owner_and_hazard_clock \
test_taskqueues.StoreQueueParity.test_json_prerequisite_clearing_and_stage_changes_survive_restart \
test_sqlqueues.SqlQueueMembership.test_old_certified_memberships_refresh_without_case_or_audit_writes \
test_sqlqueues.SqlQueueMembership.test_prerequisite_clearing_refreshes_other_process_and_restart \
test_task_queue_api.TaskQueueApi.test_current_stage_membership_detail_csv_and_role_projection -q
```

## Implementation and Validation

P01-T02: actual final-check stage activates funding/resident/technical requirements;
membership and reason/action use the same existing active set. Redundant fallback
removed so a pending handoff cannot supersede an active final-check stop.
P02-T01: MEMBERSHIP_REVISION=2 appended to SQL fingerprint forces atomic old-index
refresh while keeping public work-queues-1 and default/reset contract unchanged.
No store gates, projection, resident implementation or tests changed.

### Local outcomes before candidate freeze

* Focused corrected suites: 34 tests passed (focused.txt); unchanged semantic
  probe: all eight observations coherent (after.txt).
* Coupled test_buildings, test_stock_reconciliation, test_finance_signoffs,
  test_workflows, test_handoff_lifecycle, test_hazard_referral, test_role_matrix,
  test_sqlreads and test_sqlstore: 180 tests, OK, one existing skip. Includes
  60,000-case synthetic queue/read probes; no private stock.
* First configured static run found two new fixture inference errors in
  test_taskqueues; explicit dict[str, Any] annotations fixed them. Original
  static.txt retained. Corrected full configured core/API Ruff, format, mypy
  passed: 124 core and 56 API files (static-corrected.txt).
* First actual MSSQL attempt reached SQL 16.0.4305.5 but its test import needed
  the API component working directory. Container removed even on failure.
  Corrected runner uses existing component cwd and absolute test-only imports:
  nine inherited MSSQL tests passed with no skips, including upgrade, clearing,
  restart, independent connections and atomic failure controls. Both original
  and corrected raw receipts retained; both task-owned servers removed.
* Docker src-context build succeeded, image
  sha256:a394fca4752b17700f69e1034a92247b3a72d5a41582cdf55d54d5523c837a12.
  Packaged runtime at UID 10001, read-only root, no external network and owned
  temporary filesystem ran 34 queue/SQL/real loopback HTTP tests successfully.
  No UI/browser or operational accessibility acceptance is claimed.

Actual OS-process coverage is added inside the existing SQL lifecycle method,
not a new method: a child writer changes final-check applicability and funding
while the parent keeps a warm independent reader. This tightens the evidence
beyond two connections being described as other-process parity. Final runs
completed: focused-final.txt 34 passed; mssql-final.txt nine passed, no skips,
including actual child-process writes; static-final.txt all configured checks
passed. Docker-runtime-final.txt 34 passed at UID 10001 against final mounted
test files and unchanged built production packages. Production correction
remained unchanged throughout. All task-owned SQL containers removed by traps.

### Exact validation commands

The sanitized prefix described above is abbreviated here as ENV only for
readability; every actual application invocation used the explicit env -i.

```bash
env -i PATH="$PATH" HOME="$PWD/.venv" TMPDIR="$PWD/.venv/issue76-tmp" \
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
test_taskqueues test_sqlqueues test_task_queue_api -q

env -i PATH="$PATH" HOME="$PWD/.venv" TMPDIR="$PWD/.venv/issue76-tmp" \
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
test_buildings test_stock_reconciliation test_finance_signoffs test_workflows \
test_handoff_lifecycle test_hazard_referral test_role_matrix test_sqlreads test_sqlstore -q

env -i PATH="$PATH" HOME="$PWD/.venv" TMPDIR="$PWD/.venv/issue76-tmp" \
PYTHONPATH=src/core/tests .venv/bin/python \
.copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-probe.py

root="$PWD"
(cd src/core && "$root/.venv/bin/ruff" check . &&
 "$root/.venv/bin/ruff" format --check . && "$root/.venv/bin/mypy")
(cd src/api && "$root/.venv/bin/ruff" check . &&
 "$root/.venv/bin/ruff" format --check . && "$root/.venv/bin/mypy")

bash .copilot-tracking/changes/2026-10-18/issue-76-current-stage-blockers-mssql.sh
docker build --quiet -t ama-issue76-blockers:local -f src/api/Dockerfile src

docker run --rm --name ama-issue76-nonroot-final --network none --read-only \
 --tmpfs /tmp:rw,nosuid,size=256m \
 -v "$PWD/src/core/tests:/tests/core:ro" -v "$PWD/src/api/tests:/tests/api:ro" \
 -e PYTHONPATH=/tests/core:/tests/api -e HOME=/tmp -w /tests/api \
 --entrypoint python ama-issue76-blockers:local -c \
'import os,unittest; print("runtime_uid", os.getuid(), flush=True); assert os.getuid()==10001; suite=unittest.defaultTestLoader.loadTestsFromNames(["test_taskqueues", "test_sqlqueues", "test_task_queue_api"]); result=unittest.TextTestRunner(verbosity=1).run(suite); raise SystemExit(not result.wasSuccessful())'
```

The one coupled skip is the pre-existing "JSON-only separate-file audit ordering"
branch in test_hazard_referral (not applicable to the SQL variant).
No Azure access was authorized. Full repository suites, live Entra acceptance,
live tenant role-policy, human definition/WCAG/user acceptance and browser
journeys were not performed. No web edits. These are not passed gates.

## Review and Publication

P01/P02 complete; P03-T01/T02 ready. Source/test/docs boundary is seven tracked
files, with production edits only taskqueues.py and sqlstore.py. No #86 protected
paths changed. Candidate freeze receipt records exact base, diff digest and all
seven file hashes. Original Review then executed exactly once: Complete / Residual work, bounded
offline correction Conformant, no defects at any severity. Reviewer independently
ran 34 focused tests and all eight original-probe observations, verified freeze
and critique hashes; supplied MSSQL/Docker/coupled/static evidence assessed
separately. No source correction or second Review.

Original Review SHA-256:
527ed27ad92296fbbd42f2e148b14f9e8aed1d482748608a003da7f2aa5ff895.
Original critique remains
31e254f7de129957080e78d751f63ccac157d43f18ef2270f30cd4422e8bd1a7.
Frozen seven-file candidate remains
ba6bf081f159b30f36286c1a95256895991143ffd0956c9d0708b4a28004725f.

Remote main was original base at research/prefreeze checks, then advanced during
Review to observed 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096. No fetch-based
integration, rebase, force-push or merge performed. Topic publication retains
the explicit original base and records drift; coordinator must authorize any
later integration. No exact-integrated-head acceptance is inferred.

gh api user resolved public account id/login for repository-local noreply
author/committer identity. Source/evidence commit
ee8634c8754c68ad95dc3166d2a98918eee2ca45 pushed normally and main-target
PR https://github.com/jmservera/ama/pull/407 created. Issue remains OPEN.
P03-T04 publication complete; publication receipt and final state are persisted
in a following artifact-only commit. No source or original-evidence changes.
Hosted checks pending at initial inspection, not claimed green. Stop for
coordinator complete independent exact-head review and integration authorization.
