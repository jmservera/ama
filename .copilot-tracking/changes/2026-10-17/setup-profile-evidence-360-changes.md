<!-- markdownlint-disable-file -->
# RPI Changes: setup-profile-evidence-360

## Correction ONE Intake (2026-10-17)

Coordinator independent exact-head 9561938a assessment: Revise, two Medium
defects. Authorized correction ONE covers case-insensitive structural ARM ID
binding and bounded supported template-envelope/resource validation. Preserve
the original critique and single Review unchanged; no new full Review/self-Pass.
No active own CI-watch shell remains. Fresh main is 22670277, beyond the current
topic base 3f544fb9; no new rebase authorized or attempted. Normal own-branch
commit/push only. Live/private publisher 403 and tenant/browser/SQL/AI gates
remain unmet. Failing-first evidence and correction disposition follow.

## Metadata

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Related plan: .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md
* Implementation date: 2026-10-17

## Execution Status

* Original source/RPI/PR delivery: Complete. Authorized correction ONE:
  implemented, validated and source published normally at ed29c364.
* Declared invocation scope: full plan; implementation starts P01-T01
* Completed scope markers: P01/P02/P03/P04 and all eight tasks
* Remaining active-plan tasks: none; independent corrected-head acceptance and
  conflicting main integration remain coordinator-owned, no further rebase authorized
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

## Authorized Integration Continuation (2026-10-17)

* Coordinator explicitly authorized only this branch's rebase and an exact
  expected-old-remote force-with-lease from
  cea89c43a9979daabe1eb09032c85d451b137584. No main or other-worktree write,
  cloud mutation, Graph, SQL, live setup or paid rubric dispatch authorized.
* Actual command: `git fetch origin main fix/setup-profile-evidence-360`, then
  `git rebase origin/main`, onto
  3f544fb9cda2c51b219db2cc8368c7525bbe0c86 (#387).
* Only actual conflict: docs/reference/log.md. Removed conflict markers,
  retained exact complete upstream byte prefix and appended the original own
  entry byte-for-byte. README auto-merged; every other upstream routing line
  verified retained. Resolved with `git add docs/reference/log.md` and
  `GIT_EDITOR=true git rebase --continue`.
* Rebased candidate: bffba7475dfbc551a0836601ba67c3af62f809c1, with source
  commit 154e59c7. No correction to source or tests was needed.
* Exact added/removed binary infra source/test patch SHA-256 on both old/new
  bases: d1de2f05de59c2460cb793daf751d3fa8bbeb22c2a073eda281677c181f64f37.
* File SHA-256 fingerprints unchanged across rebase:

| File | SHA-256 |
| --- | --- |
| infra/scripts/setup-entra.py | a89954e9971f6a8aa1d99c43bb99278625f63d0e053679135af8de59dcb0274a |
| infra/tests/test_setup_entra.py | ef8ee58cf10843609e7f34cff9a9a0d1c2b4139c0d683cdc3801bdf94c83970f |
| Original plan critique | 48931b8edc0be01fc925293721d305a60446e61e3e7f663ba509d8d674883ed9 |
| Original single Review | 65721ae7cec37255bcf0dbc37b9baebd0282d62e50e8646b0f43d261540476a6 |

* `git diff 3f544fb9 HEAD -- src` is empty: all merged quality,
  assistant/current-version evidence and shared recovery changes are untouched.
* Installed editable core/agents/api/orchestrator distributions point to this
  worktree. Fresh combined complete setup/staff/auth/secret suite: 200 passed
  in 4.589 seconds. Invocation used the installed session venv Python with
  unittest loading test_setup_entra, test_staff_azure,
  test_initialize_workbench_staff, test_initialize_api_auth and
  test_secret_lifecycle from infra/tests.
* README configured three-file ruff lint and format checks passed; changed-line
  ruff against origin/main reports zero introduced diagnostics and 225 untouched
  legacy diagnostics. compileall and `git diff --check origin/main...HEAD`
  passed. No dependency installation or manifest change required.
* No new full Review or critique; original artifacts byte-unchanged. No source
  correction cycle. This section is explicit integration evidence, not a
  replacement verdict or claimed independent coordinator Pass.
* Ordinary CI inspected: src-ci.yml and mvp-validation.yml both include infra
  pull-request paths and workflow_dispatch. No checks existed before push.
  If automatic checks remain absent, only ordinary validation on this branch
  will be dispatched. No paid rubric workflow is requested.
* Source CI's infrastructure workflow_run is gated to successful pull_request
  events; manual workflow_dispatch cannot activate its Azure what-if jobs.
* Publication/check receipt follows below. Live ACR403/private publisher and
  actual tenant/browser/SQL/AI gates remain unmet.

### Integration Publication Receipt

* Exact authorized command executed successfully:

```bash
git push --force-with-lease=refs/heads/fix/setup-profile-evidence-360:cea89c43a9979daabe1eb09032c85d451b137584 origin HEAD:refs/heads/fix/setup-profile-evidence-360
```

* Integrated evidence head:
  9c0ffe22202ecf241e5c5d4f03d0b03553ab28bf. GitHub remote ref and PR #391
  head matched; mergeable MERGEABLE, base 3f544fb9, checks initially queued
  (UNSTABLE is not a green/accepted verdict).
* Ordinary checks appeared automatically on the own branch: Source projects CI
  39067847373 and MVP validation 39067847374, both pull_request events.
  Their infra path filters matched. No manual workflow dispatch was necessary;
  no paid rubric, release/deployment or cloud workflow was dispatched.
* This receipt-only normal fast-forward commit follows the authorized rebase
  publication. Exact final-head status is reported on PR #391 and in the
  coordinator handoff; queued, cancelled, skipped or absent checks are not
  represented as green.
* Original critique and Review, source/test fingerprints and new-base src
  preservation are unchanged. No new RPI cycle or full Review.
* Automatic continuation stops at clean pushed head/resume state per owner.

## Correction ONE Validation and Disposition

* Separate implementation disposition:
  .copilot-tracking/changes/2026-10-17/setup-profile-evidence-360-correction-one.md.
* Coordinator exact-9561938a independent verdict remains Revise, two Medium
  defects. Correction evidence is not an independent Pass; no new full Review.
* First run, before source edits:
  `profile-venv/bin/python -m unittest discover -s infra/tests -p test_setup_entra.py -k test_correction -v`
  yielded two methods, four failures (invalid envelope accepted), one error
  (valid mixed-case Providers binding refused).
* Corrected IDs use full anchored case-insensitive parsing with canonical
  subscription UUID and exact ama/provider/type/name scope. Normalized IDs
  compare exactly; wrong group/provider/type/subscription or child scope refuse.
* Template envelope validation now gates profile resolution. Missing/foreign/
  malformed schemas, unsupported language/resource forms and nested deployment
  contracts explicitly refuse. Literal/default profile rules and independent
  development/test evidence remain unchanged. No generic ARM evaluator added.
* Final installed-distribution runner:

```python
import sys, unittest
sys.path.insert(0, "infra/tests")
suite = unittest.defaultTestLoader.loadTestsFromNames([
    "test_setup_entra", "test_staff_azure", "test_initialize_workbench_staff",
    "test_initialize_api_auth", "test_secret_lifecycle",
])
result = unittest.TextTestRunner(verbosity=1).run(suite)
sys.exit(not result.wasSuccessful())
```

* Executed with existing session files/profile-venv/bin/python: 206 tests
  passed, 4.500 seconds (123 setup plus unchanged 83 staff/auth/secret tests).
  Six new methods, table-driven boundaries; reported three-deployment regression
  and actual/default production vetoes pass. No original test removed.
* Existing exact README ruff lint/format commands pass (three configured files);
  correction-line ruff zero introduced, 225 untouched legacy diagnostics.
  compileall and git diff --check pass. No new dependency or manifest changes.
* Full infra discovery not claimed; no missing-YAML import error represented
  as Pass. The required complete named suites are the validation boundary.
* Final corrected file SHA-256:

| File | SHA-256 |
| --- | --- |
| infra/scripts/setup-entra.py | f1579774ae790e56130a80c5377945294021471ff682a9c481583f755076f25d |
| infra/tests/test_setup_entra.py | d1e7a9af987816b8429a4845d0d3bb8f8718effbc11319d04000b2c6dc461849 |

* Original critique/Review hashes match the prior recorded fingerprints.
  Exact prior KB log byte prefix preserved; no src/quality/assistant/recovery
  changes. Fresh main 22670277 recorded only; no rebase performed.
* Prior exact-9561938a ordinary Source CI 39067901027 and MVP validation
  39067900996 completed success. Those prior-head results are not corrected-head
  acceptance and do not supersede coordinator Revise.
* No cloud/live setup, private inputs, Graph, SQL, tags/IAM/network changes,
  paid rubric, merge or issue closure. ACR403/private publisher and real
  tenant/browser/SQL/AI gates remain unmet.

## Correction ONE Publication Receipt

* Source commit: ed29c364f4656e9c091b907c8fced30dba266f03,
  fix(infra): validate setup ARM identities and template envelopes.
* Actual commands: fresh `gh api user --jq '[.id,.login] | @tsv'`,
  repository-local privacy-safe name/email, explicit author/committer environment,
  `git commit` with Refs #360 and required Copilot coauthor trailer, then
  `git push origin HEAD:refs/heads/fix/setup-profile-evidence-360`.
  Normal fast-forward 9561938a -> ed29c364 succeeded. No rewrite/rebase.
* `git ls-remote --heads origin fix/setup-profile-evidence-360` and
  `gh pr view 391 --json headRefOid,baseRefName,state,mergeable,statusCheckRollup`
  verified matching source head, OPEN, base main, CONFLICTING, empty checks.
* Fresh main advanced to 22670277; no unauthorized integration attempted.
  Source correction complete but merge is blocked and independent acceptance
  still belongs to coordinator.
* Inspected .github/workflows/src-ci.yml and mvp-validation.yml: both ordinary
  validation workflows allow workflow_dispatch on own branch. Infra paths
  qualify for PR validation but conflicting PR has no checks. Inspected
  infra-plan.yml: cloud what-if requires workflow_run.event pull_request, so
  a dispatch is excluded. src-deploy.yml is explicit dispatch/main-only and
  is not invoked. No paid rubric dispatch.
* This receipt is a normal documentation fast-forward. Dispatch only ordinary
  Source projects CI and MVP validation on its final pushed head, then record
  exact run IDs/status on PR #391. Until observed, no corrected-head CI success
  claimed. Original adverse assessment remains unchanged.

## Authorized Latest-Main Integration After Correction ONE

* New coordinator authorization supersedes the earlier no-further-rebase limit
  only for this own topic. Clean local/remote old head bcefa42d verified before
  writes, fetched main and read actual graph: #390 at 22670277 on 3f544fb9.
* Executed `git rebase origin/main`; six own commits replayed. Only actual
  conflict docs/reference/log.md, resolved by retaining upstream block then
  all own blocks, including exact separating newline. Index auto-merged.
* Exact-byte assertion: new log = origin/main log + old own append suffix
  relative to 3f544fb9. All own routes and new/changed main routes retained.
* Exact infra source/test binary patch SHA-256 before and after:
  489207739cb04e225ee54ebc162f66372dc41cddb08a7ef328b5d21db55934db.
  Corrected source/test and original critique/Review hashes unchanged.
* `git diff origin/main HEAD -- src .github/workflows` empty: every upstream
  runtime, progress precision/sequence, Store/server/workflow and test config
  change retained exactly. No runtime conflict, no resident scope or #102
  historical-capture expansion.
* Existing profile-venv, unittest loader test_setup_entra: 123 passed, 2.677s.
  Exact README three-file ruff lint/format, source/test compileall and whitespace
  checks pass. Original 206-test correction result remains historical, not
  falsely represented as rerun. No unrelated SQL/Docker/live work repeated.
* Expanded integration proof is in separate correction ONE disposition.
  No new full Review, critique, retrospective phase or self-Pass.
* Publish with exact expected-old lease
  refs/heads/fix/setup-profile-evidence-360:bcefa42d536096082227e1d59e80c6e605831eaa.
  Final receipt HEAD/check status belongs in PR #391 handoff. All live gates
  remain unmet; no merge/issue closure/cloud/paid-AI/private-input actions.
