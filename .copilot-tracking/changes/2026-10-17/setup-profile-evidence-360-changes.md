<!-- markdownlint-disable-file -->
# RPI Changes: setup-profile-evidence-360

## Metadata

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Related plan: .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md
* Implementation date: 2026-10-17

## Execution Status

* Status: Complete for source/RPI/PR delivery; integration follow-up blocked
* Declared invocation scope: full plan; implementation starts P01-T01
* Completed scope markers: P01/P02/P03 and all six tasks
* Remaining active-plan tasks: none; concurrent main integration is separately authorized follow-up
* Approved writes: setup classifier/tests, infra runbook, existing KB route/log and dated RPI artifacts.

## Execution Summary

Research complete and one critique executed (Pass, no findings). Actual supplied
shape reproduced before source fix; contract-aware classification implemented.

## Completed Work

### Installed baseline and failing-first actual shape

* P01-T01: installed editable core/agents/api/orchestrator into isolated session
  venv before infra tests. Setup baseline: 104 passed. Staff_azure initial run
  failed because cryptography was absent; installed src/api/requirements.txt
  with --require-hashes and reran: 43 passed. Fresh combined baseline 147.
* Added regression matching coordinator-reported API/environment tags and three
  bound successful deployments. Before source edit: 1 test failed (errors=1),
  exact original Automatic demo roster refused SetupError.
* No live queries or mutations, roster/private dataset reads or cloud jobs.

### Contract-aware resource-bound classification

* P01-T02: infra/scripts/setup-entra.py resolves only deploymentProfile,
  environmentName and tags from exact successful bound history plus exported
  raw template declarations. Explicit values override literal declared defaults.
* Neutral templates contribute nothing; production defaults and all independent
  contradictions veto. Required missing, malformed/null/unresolved structures,
  denied export and wrong environment readback fail closed.
* No generic evaluator, templateLink fetch, new package or non-classifier changes.
* Existing tests updated for real named export schema and bound null rejection;
  13 added methods with table variants, within approved 18-method limit.

### Validation and durable runbook finding

* P02-T01: 200 complete setup/staff/auth/secret tests pass together. Four unsafe
  classifier mutations killed in memory without modifying source files.
* P02-T02: updated infra runbook with exact export/default and failure semantics;
  integrated source finding in existing KB index route and appended dated log.
  Historical acceptance, case original, owner memory and live controls unchanged.

## Implementation-Time Plan and Detail Updates

No deviations. Existing null-tags bound-success expectation was tightened
as explicitly planned, not silently preserved as unsafe coercion.

## Validation Record

| Check | Result | Scope |
| --- | --- | --- |
| Pre-fix baseline | 104 setup + 43 staff_azure passed | Fresh source at 1a05dfb8 |
| Actual-shape regression before fix | Failed as expected, exact SetupError | 1 test |
| Post-fix setup | 117 passed | Complete existing suite + 13 new methods |
| Staff suites | 58 passed | 43 staff_azure + 15 initialize-workbench-staff |
| Legacy auth delegate | 17 passed | test_initialize_api_auth.py |
| Secret lifecycle | 8 passed | test_secret_lifecycle.py |
| README configured ruff lint | Passed | Three explicitly configured files |
| README configured ruff format | Passed, three already formatted | Same three files |
| Combined final suites | 200 passed | 117 setup + 43 staff_azure + 15 staff initializer + 17 auth + 8 lifecycle |
| Four unsafe in-memory mutations | All killed | Production-default, neutral patch, hidden conflict, wrong environment |
| Changed setup-line ruff | Zero introduced diagnostics | 225 untouched legacy diagnostics excluded |
| compileall and git diff --check | Passed | Changed Python and complete diff |

Commands used after editable source installation:

```bash
python -m unittest discover -s infra/tests -p test_setup_entra.py -q
python -m unittest discover -s infra/tests -p 'test_*staff*.py' -q
python -m unittest discover -s infra/tests -p test_initialize_api_auth.py -q
python -m unittest discover -s infra/tests -p test_secret_lifecycle.py -q
ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py
ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py
```

Final 200-test run loads those same five modules in one unittest runner.
Initial mutation harness used an ambiguous textual locator; corrected to the
exact helper boundary before all four checks passed. No production change from
that harness correction. Changed-line lint caught long lines, fixed before
the final zero-diagnostic run; no unrelated legacy cleanup.

No live mutating setup, Azure, Graph, SQL or Docker.
No full repository/Bicep suite: source-only parser change with complete required
setup/staff and directly related compatibility coverage.

## Pre-Review Reconciliation

* Plan markers/details: P01/P02 complete, P03 Review/delivery intentionally open.
* Changes/validation and handoff: current; single critique Pass retained.
* No implementation divergence or unresolved source blocker.
* Follow-up-only live gates remain unclaimed.
* Ready for one Review of source/test/doc change, not live setup acceptance.

## Blockers

No source-delivery blocker. PR #391 CONFLICTING/DIRTY against concurrent main
3f544fb9 after #387; coordinator must authorize integration before merge/check
acceptance. No CI/rubric checks reported. Live credential and initializer
publication 403 gates remain unmet, outside source acceptance.

## Remaining Work

No active-plan delivery task remains. Integration and live acceptance are
follow-up work; no merge/rebase/force push attempted.

## One Review Result

* Execution Complete; outcome Residual work; no source defects found.
* Original: .copilot-tracking/reviews/logs/2026-10-17/setup-profile-evidence-360-review.md
* RV-001 routes live gates to distinct owner/coordinator follow-up.
* Not an independent coordinator Pass. No source correction or second Review.

## Follow-Up Items

Coordinator authorization for concurrent-main integration of PR #391 and
subsequent checks is the immediate delivery gate. It was discovered after the
one Review; recorded as follow-up only, with original Review unchanged.

Owner/coordinator live credentials/publication, then genuine tenant/browser/
SQL/AI proof and separately authorized retirement. #360 d/e remain unmet.

## Delivery Receipt

* Source and dated artifact commit: ac4b28590d8885b314f81be02c2371398270ccd4.
* Branch: fix/setup-profile-evidence-360; remote tracking head matched, clean
  working tree verified after first push.
* Main PR: https://github.com/jmservera/ama/pull/391, Refs #360, no closing keyword.
* Original Review SHA-256:
  65721ae7cec37255bcf0dbc37b9baebd0282d62e50e8646b0f43d261540476a6.
* Zero correction cycles; no source changes after the original Review.
* This receipt/state completion is a subsequent documentation-only commit,
  not a repeated Review or claim of coordinator acceptance.
* GitHub at delivery: CONFLICTING/DIRTY, empty statusCheckRollup, no workflow
  runs for the branch. No CI/rubric Pass claimed.
* Owner requested stop at clean pushed head/resume state; no automatic child.

## Return-to-Caller State

Automatic mode; Follow-up; source/RPI/PR delivery completed; session stopped by
owner instruction. Coordinator integration authorization remains a follow-up
blocker. Resume state is the canonical dated setup-profile-evidence-360 JSON.
Live credential/initializer-publication gates still unmet.
