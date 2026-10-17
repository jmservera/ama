---
title: In-VNet staff initialization changes
description: Implementation and validation evidence for Refs #360
ms.date: 2026-10-16
---

## Scope

### P04 rebase-only opening (2026-10-17)

Research reused/Ready and Plan verification Complete/Ready. Caller explicitly
requests the remaining rebase/validation/Review/publication phases, then stop.
Baseline clean HEAD d0500035863a596812a018c1e755a393b9c31e21;
origin/main c9ba95f and remote topic lease d0500035863a596812a018c1e755a393b9c31e21.
Authenticated GitHub account resolved using gh api user; repository-local
privacy-safe email configured before new commits. Preparation evidence is
committed locally before rebase so no stash, dirty-tree bypass or work loss is
needed. No implementation scope beyond preserving both merged intents.
All previous log/result claims below remain historical, not rerun evidence.

### P04-T01 rebase result

`GIT_EDITOR=true git rebase origin/main` completed onto c9ba95f.
Only conflicts: docs/reference/README.md and docs/reference/log.md while
replaying 37af66e. Rerere supplied the index resolution; manually inspected
against origin/main and confirmed its entire index plus the #360 row.
Log resolution retained the entire upstream side (#176, #178, #175 and
other historical entries), then appended the existing #360 section unchanged.
No new historical log entry or past validation claim was invented.
No source conflict occurred; infra/README.md merged automatically.

Post-rebase source boundary: 1d204df. `git diff --exit-code d050003 HEAD --
.github/workflows infra docs/architecture` passed: image, dockerignore,
timeout tests, transport, hashed requirements and runbook are identical.
`git diff --exit-code origin/main HEAD -- src docs/reference/research` passed:
#176 synthetic source/tests/docs and #175 privacy delivery are unchanged.
All upstream 2026-10-17 recovery artifact directories also compare identically.
`git diff --check` passed. Fresh venv's first staff discovery failed honestly
with missing zava_forward; source/dependency installation follows that
missing-package failure. Validation is not yet complete.

### P04-T02 validation (2026-10-17)

Assessed rebased source HEAD: 1d204df. New venv:
`/tmp/ama-360-rebase-ZSRcWK`, Python 3.12.3,
`include-system-site-packages = false`. Commands from repository root:

```bash
V=$(mktemp -d /tmp/ama-360-rebase-XXXXXX)
python3 -m venv "$V"
"$V/bin/python" -m unittest discover -s infra/tests -p test_staff_azure.py -q
"$V/bin/python" -m pip --quiet install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator
"$V/bin/python" -m pip --quiet install 'PyYAML==6.0.3'
"$V/bin/python" -m pip --quiet install --require-hashes -r src/api/requirements.txt
"$V/bin/python" -m pip check
"$V/bin/python" -m unittest discover -s infra/tests -p test_staff_azure.py -q
"$V/bin/python" -m unittest discover -s infra/tests -p test_pipeline.py -q
REQUIRE_AZ_BICEP=1 "$V/bin/python" -m unittest discover -s infra/tests -q
"$V/bin/ruff" --version
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
git diff --check
git diff --exit-code d050003 HEAD -- .github/workflows infra docs/architecture
git diff --exit-code origin/main HEAD -- src docs/reference/research
```

Initial clean-venv discovery: missing zava_forward (one import error);
dependency install followed that failure. Subsequent results: pip check passed;
staff **21 passed** (0.240 s), pipeline **28 passed** (6.034 s),
full infra **307 passed, zero skips** (68.284 s).
Ruff initially absent (exit 127); installed only existing pinned tools after
that failure. Exact existing ten-file Ruff E/F/I/B/UP and format commands
passed; all three existing mypy invocations passed. All infra/module local
Bicep build/lint commands passed without Azure service access.
Whitespace and source equality checks passed.

Additional byte assertions passed: origin/main log is an exact prefix of
the resolved log; every original d050003 log section remains unchanged;
all rows from both index versions survive; every upstream tracked
synthetic-determinism-176 recovery artifact and synthetic-dictionary-175
artifact is byte-identical. No source changes or test changes were required.
Docker access is denied by the caller's VM evidence; no Docker command,
bypass or image build was attempted. No Azure service calls/writes, roles,
private datasets, secrets or new behavior. Prior live blockers stay open.

P04-T01/T02 complete. Review-ready: no source conflict, ambiguity, divergence
or unresolved local validation failure. P04-T03 Review/publication remains.

### P04 local closeout before single publication

Research reused/Ready, Plan verification Complete/Ready, Implement Complete,
one rebase-resolution Review Complete, outcome Residual work for unchanged
RV-001/RV-002/RV-003 only. P04 local markers are complete; no source defect
or new implementation scope. Only tracking evidence changed after validated
source 1d204df. The final evidence commit will be published once with explicit
`--force-with-lease=refs/heads/feat/run-in-azure-360:d0500035863a596812a018c1e755a393b9c31e21`.
This is an intended action, not a claim it already ran. PR #370 readback and
final response will identify the actual published SHA and receipt; no extra
tracking-only commit/push follows reporting that SHA.

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

### Correction publication receipt and final-head boundary

Research **Complete**, Plan **Complete**, Implement **Complete**, Review
**Complete**, outcome **Residual work**. Source correction
`6976ae9649de291409c771986b818b83e0ebc8ae` was pushed normally to the same
feat/run-in-azure-360 branch. Existing PR #370 was updated in place, Refs #360
only. GitHub readback confirmed that exact source head, open state and main
base. Local worktree was clean after the source publication.

The complete infra command was rerun at committed source head 6976ae9:
`REQUIRE_AZ_BICEP=1 /tmp/ama-360-correction1-YRmaea/bin/python -m unittest discover -s infra/tests -q`.
Result: **307 passed, zero skips, 66.039 seconds**. The final publication
receipt commit changes tracking artifacts only; its executable/workflow,
dockerignore, test and runbook tree is identical to this validated source
head. The PR's headRefOid is the authoritative final publication SHA; do not
mistake baseline 296037b or original 37af66e for the corrected final source.
Final report and PR identify the publication head after the receipt push.

No merge, force-push or Azure operation. RV-001/RV-002/RV-003 remain unresolved;
no operational acceptance, live CI result or authority is invented.
