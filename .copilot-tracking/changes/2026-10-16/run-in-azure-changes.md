---
title: In-VNet staff initialization changes
description: Implementation and validation evidence for Refs #360
ms.date: 2026-10-16
---

## Scope

Full plan 360-run-in-azure. P01 complete; P02 validation/delivery active. One critique executed,
PC-001 through PC-008 accepted. No Azure execution or image build authorized.

## Amendments

Worker-owned restart replaces the initial operator-only proposal to honor the
literal requirement. A standalone Bicep template grants only API reads/restart
to the existing SQL-admin identity; it is not deployed in this task.
The logs interface has a documented running-pod dependency; hold encrypted
results briefly while polling, then require successful execution status.

## P01 Implementation

* Added explicit/automatic Azure candidate/check/apply transport, with no
  fallback after uncertain local apply or validation refusal.
* Canonical SQL preparation now accepts a lazy person resolver, preserving
  existing pre-Graph validation order. Worker receives locally resolved people,
  uses MSI SQL, rereads after commit and invokes canonical replica convergence
  through a fixed-target MI ARM adapter.
* Proof image adds two modules, the existing initializer/roster helper and
  manifest. Original proof entrypoint and installed package/driver base remain.
* Standalone Bicep adds API-only custom restart role and ama guard, separately
  inventoried/tested in role-assignments.json. No identity or broad role added.

## P02 Evidence and adjustments

* Fake az covers explicit/fallback setup, generated admin/seed preservation,
  codes-free Azure output, secret transfer, encryption, source guards, timeout,
  job/start/create/log/stop/delete failure, interruption and collision.
* Local input is bounded to 12 KiB for secret transport. Job tags retain
  existing source governance tags. Each command honors execution deadline;
  cleanup has its own 90-second budget and ownership/absence proof.
* A pre-provisioning 404 after an uncertain create is not called cleanup proof.
  Cleanup refusal prints owned resource name and exact runbook recovery.
* ARM registry responses may include null username/password reference fields.
  Guards accept those empty fields but reject populated credentials; the job
  receives only the reconstructed server/MI pair. The final 304-test run
  includes this realistic response fixture.
* Updated runbook, cut-over acceptance table, reference index and append-only
  log. CI now gates the new Python modules/test with Ruff and scoped mypy.
* Existing role-matrix parser handled only built-in roles; extended it with a
  separate inventoried custom-role assertion rather than weakening the matrix.
* No package manifests changed. Missing local source distributions and
  Ruff/mypy were installed using pip in a session-only venv after validation
  failed for missing packages/tools. No system-environment override.

## Validation

Targeted staff tests: 34 passed; setup tests: 95 passed. Final full infra
run: 304 passed without skips (including all targeted cases).
Standalone Bicep build/lint passed without Azure access. All ten CI-gated infra
Python files passed Ruff/format; new worker/transport mypy passed.
Responsive loopback app auth suite: 32 passed; synthetic missing-law-store
diagnostic is expected, not a raw private-data failure. No live model call.
Live image build, role deployment, job/log/private SQL, real Entra/browser,
cross-host enforced mutex and human acceptance remain Not run/unmet.

## Review Handoff

Implementation and docs are ready for one Review. No source blockers or plan
divergences remain. The live prerequisites are explicit acceptance gaps, not
reported passes. Review owns later-work routing; no current-task correction loop.
Publication (privacy-safe commit/push/PR) follows the recorded review outcome.

## Publication

Implementation commit: 37af66e, pushed to origin/feat/run-in-azure-360.
PR: https://github.com/jmservera/ama/pull/370, targeting main, Refs #360.
Authenticated owner account was resolved before committing; author and
committer use the repository-local privacy-safe noreply address. No merge,
force-push, issue checkbox mutation or Azure execution was performed.

Review execution is Complete; outcome Residual work. Implementation is
delivered; authorized image/role activation, live acceptance and serialized
operator recovery remain distinct follow-ups, not active implementation.

The installed commit/PR commands referenced supplemental instruction files
not present at their advertised paths; no repository citation-policy file
was found. Repository/user conventions were used. Existing tracked
.copilot-tracking/pr/pr.md was not overwritten; PR body and generated XML
reference were kept in the session workspace.

## Correction cycle 1 (2026-10-17): P03 opening

Baseline: 296037b239d20179de4048f0bc9f837b4704bb86, clean worktree on
feat/run-in-azure-360, open PR #370. Research Complete/Ready; Plan Complete/Ready.
One correction-candidate critique executed; PC-009's project-local venv
suggestion rejected against caller direction and successful parent /tmp
reproduction. No second critique. Scope: P03-T01/T02 implementation and
validation, then P03-T03 read-only Review/publication. Prior evidence and
RV-001/RV-002/RV-003 remain historical and explicitly unresolved.

Fresh Python 3.12.3 venv `/tmp/ama-360-correction1-YRmaea` was created using
`python3 -m venv`; pip installed source packages with `--no-deps` and pinned
PyYAML, matching MVP CI. Baseline staff suite: 21 tests, 14 failures/four
errors, absent cryptography exactly matching failed CI run 38983585607.
No crypto mocks, test skips or guard relaxation. No Azure/data/secret/live
Graph work, image build, deployment, spending or network change.

### P03-T01 implemented

Both actual infra-discovery workflows now run the identical
`pip install --require-hashes -r src/api/requirements.txt` before discovery,
retaining pinned PyYAML. This reuses cryptography 50.0.2 and its hashed
dependencies rather than an incidental src-CI transitive install or a new
test-specific version. Existing workflow validator now requires that ordered
command; one new test method rejects missing, unhashed and late installation
in both workflows (six subcases). Quality-gate runbook commands updated.
No runtime source, Dockerfile, dockerignore or existing staff tests changed.

### P03-T02 clean pip validation commands and results

All commands run from repository root. `V` below abbreviates the actual
`/tmp/ama-360-correction1-YRmaea`; it was created by
`V=$(mktemp -d /tmp/ama-360-correction1-XXXXXX) && python3 -m venv "$V"`.
Python 3.12.3, `include-system-site-packages = false`; no uv or activation of
the primary checkout environment. Log files remain in that disposable venv.

```bash
"$V/bin/python" -m pip --quiet install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator
"$V/bin/python" -m pip --quiet install 'PyYAML==6.0.3'
"$V/bin/python" -m unittest discover -s infra/tests -p test_staff_azure.py -q
```

Before correction dependencies: exit 1, 21 tests, 14 failures/four errors.
Missing cryptography blocks encryption setup before cleanup/timeout tests.
This reproduces CI run 38983585607 without mocking crypto.

```bash
"$V/bin/python" -m pip --quiet install --require-hashes -r src/api/requirements.txt
"$V/bin/python" -m pip check
REQUIRE_AZ_BICEP=1 "$V/bin/python" -m unittest discover -s infra/tests -q
"$V/bin/python" -m unittest discover -s infra/tests -p test_staff_azure.py -v
"$V/bin/python" -m unittest discover -s infra/tests -p test_pipeline.py -q
```

Passed: pip check, **307 full infra tests, no skips** (67.359 seconds),
21 staff tests and 28 pipeline tests. Real cryptography 50.0.2 encrypts and
decrypts; PyYAML 6.0.3 supplies workflow parsing. The full suite includes
compiled Bicep policy/mutation checks with REQUIRE_AZ_BICEP=1.

Ruff invocation first failed because the clean venv lacked Ruff (exit 127).
Installed only the existing CI tool pins after that missing-tool failure:

```bash
"$V/bin/python" -m pip --quiet install 'ruff==0.17.1' 'mypy==2.4.0'
FILES="infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py infra/scripts/pipeline.py infra/tests/test_pipeline.py infra/scripts/staff_azure.py infra/scripts/staff-azure-worker.py infra/tests/test_staff_azure.py src/check-container.py infra/tests/test_container_contract.py"
"$V/bin/ruff" check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 $FILES
"$V/bin/ruff" format --isolated --line-length 100 --check $FILES
"$V/bin/mypy" --strict src/check-container.py
"$V/bin/mypy" --strict infra/scripts/pipeline.py
"$V/bin/mypy" --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff-azure-worker.py
for file in infra/*.bicep infra/modules/*.bicep; do
  az bicep build --file "$file" --stdout > /dev/null || exit 1
  az bicep lint --file "$file" || exit 1
done
git diff --exit-code 296037b -- infra/.dockerignore infra/tests/test_staff_azure.py infra/cutover-proof.Dockerfile infra/scripts/staff_azure.py
git diff --check
```

Passed: E/F/I/B/UP on all ten existing gated files, all ten already formatted,
all three mypy invocations, every infra/module Bicep local build/lint and
whitespace review. Bicep CLI 0.48.1 compiled locally only; no Azure resource
request. Prior context/timeout corrections and runtime transport are unchanged.

### Preserved regressions and mutation controls

Executed:

```bash
"$V/bin/python" /home/azureuser/.copilot/session-state/7f2b1f61-4561-4385-be14-7db4ef3c98a0/files/correction1-mutations.py
```

The session-only harness leaves source untouched and uses real AES-GCM.
Three baseline tests pass: every proof COPY source survives context,
decoded-result/Running execution times out with verified cleanup, and both
workflows reject missing/unhashed/late requirements (six workflow subcases).
Seven in-memory negative controls are killed by the intended assertion,
with no errors/skips: remove each of five parent/file context allowance
pairs (staff_roster.py, staff_azure.py, staff-azure-worker.py,
initialize-workbench-staff.py, entra/app-registration.json); accept a decoded
result before terminal Succeeded; remove execution-loop timeout refusal.

Initial single-file-allowance mutation survived: the existing context test's
prefix matcher still accepts the parent directory allowance. The corrected
negative controls explicitly remove both inclusion routes and establish
omitted-source rejection. This is not a claim that the lightweight matcher
implements every Docker ignore rule or proves an actual image. The original
dockerignore and new regression tests from 126ecae remain byte-for-byte intact.

### Correction review readiness

P03-T01/T02 complete; P03-T03 Review/publication remains. No implementation
blocker or new user decision. This correction proves only offline dependencies
and regressions at the final changed executable/workflow tree. RV-001 image
and API-only role activation, RV-002 live private job/log/SQL/restart/browser
and tenant evidence, RV-003 serialized operation/hard-kill recovery remain
unmet. A green offline correction does not establish live acceptance.

### Correction Review completion

Research Complete, Plan Complete, Implement Complete for P03-T01/T02.
One correction-cycle Review Complete, outcome Residual work, no identified
source-blocking defect. RV-001/RV-002/RV-003 remain open and unchanged.
Only P03-T03 publication/receipt remains. GitHub account id/login resolved
fresh and repository-local noreply configured for author and committer.
The commit skill's supplemental instruction file is still unavailable and
the advertised changed-files tool is not exposed; repository/user commit
conventions and Git inspection apply. No extra PR-review agent or rewrite of
the tracked PR scratch file is needed for updating the existing PR.
