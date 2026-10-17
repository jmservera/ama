---
title: In-VNet staff initialization review
description: One post-implementation evidence review for Refs #360
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: 360-run-in-azure.
* Boundary: full offline implementation, tests, runbook and acceptance audit.
* Plan: .copilot-tracking/plans/2026-10-16/run-in-azure-plan.md.
* Details: .copilot-tracking/details/2026-10-16/run-in-azure-phase-details.md.
* Critique: .copilot-tracking/reviews/2026-10-16/run-in-azure-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/run-in-azure-changes.md.
* Research: .copilot-tracking/research/2026-10-16/run-in-azure-research.md.
* Compared final transport/worker/shared initializer/setup integration, image
  copies, Bicep/role matrix/guard, new and existing fake-az/SQL tests, CI gates,
  infra runbook, cut-over acceptance table, reference index and log diff.

## Opening Review State

Implementation and local validation are complete; every source-plan marker is
reconciled. Privacy-safe commit/push/PR publication remains parent-owned.
No live Azure execution, image build, private dataset, tenant modification,
network change or approval is in this review's acceptance boundary.
Read-only review; only this record is authored. One Review, performed directly,
with no review fan-out or second review planned.

## Execution Status

Complete. This is an offline source/evidence assessment, not a deployment,
security certification or accessibility/legal conformance determination.

## Plan-to-Change Reconciliation

| Marker | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Shared lazy person resolver preserves SQL validation-before-Graph order; worker uses canonical protected preparation/atomic installation, post-commit reread, MI-only restart adapter and copied manifest/helpers | Reconciled; original local behavior retained by regressions |
| P01-T02 | Explicit mode bypasses local SQL; blocked candidate/check falls back; validation/uncertain apply never retries remotely. Source guards, secretRef, authenticated results, deadlines and owned cleanup are present | Reconciled within stated offline boundary |
| P02-T01 | Fake az covers explicit/automatic paths, generated admin/seed, codes-free output, privacy, job/start/create/log/stop/delete failure, timeout, collision and interruption. Runbook/evidence/index/log updated | Reconciled; no inference of live acceptance |
| P02-T02 | 304 infra tests, 32 responsive local app auth tests, CI-gated Ruff/format, scoped mypy and offline Bicep | Reconciled; publication is parent-owned next action |

## Critique and Implementation-Time Decisions

| Finding | Disposition evidence | Assessment |
| --- | --- | --- |
| PC-001 | Worker restarts through own MI; standalone Bicep assigns only app/revision/replica reads and restart at API scope | Literal job-owned restart retained, no operator token |
| PC-002 | Public CLI source documents explicit execution/replica/container JSON-line log streaming and live-pod requirement. Worker holds encrypted result for 60 seconds; client bounds subprocess and requires terminal success | Feasibility grounded in interface source; live endpoint access remains a prerequisite |
| PC-003 | Exact ama/subscription resource bindings, identity principal/tenant versus SQL admin, matching environment/subnet, private Entra-only SQL/database, pinned source image and allowlisted registry/env | Refusal fixtures cover material guards; no network mutation |
| PC-004 | Only pre-mutation candidate/check fallback; validation returns stop; unknown local apply timeout has regression proving no remote apply | Reconciled |
| PC-005 | Manual one-replica job, retry limit zero, canonical SQL lock/transaction, post-commit drift refusal and restart on SQL no-op | Reconciled locally; not live SQL concurrency proof |
| PC-006 | Collision refusal, run-tag ownership, stop then delete/absence check, uncertain-create refusal and explicit cleanup errors/recovery | Reconciled for normal/handled failures; hard termination remains documented residual |
| PC-007 | AES-GCM fresh key/nonce and AAD bind version/run/operation/input; bounded indexed ciphertext, duplicate/missing/tampered/wrong-key refusal, count/status validation | Reconciled; indexed reconstruction does not rely on log arrival order |
| PC-008 | Pure SQL person-resolver interface; operator resolves complete manual/generated people; image copies initializer/helpers/manifest without altering proof ENTRYPOINT | Reconciled; compatible image not built here |

The initial operator-only restart proposal was corrected before implementation,
not accepted as a divergence. Nullable ARM registry credential fields are
accepted only when empty; forwarded configuration is reconstructed as
server/MI only. Source tags retain governance metadata. The existing built-in
role matrix stays enforced, with a separate explicit custom-role inventory/test.
The reference log diff adds only its new terminal section.

## Findings and Routing

### RV-001 [Medium]: Deployment prerequisites remain unexecuted

* Evidence: infra/cutover-proof.Dockerfile, infra/staff-initializer-rbac.bicep,
  infra/README.md, docs/architecture/cutover-evidence-pack.md.
* Impact: the old image lacks the worker, and the MI cannot restart the API
  without its narrowly scoped assignment. A source-only PR is not a live fix.
* Destination: distinct authorized deployment follow-up, not current source work.
* Next action: reviewed private image build/publication, init image digest update
  and API-scoped role deployment in ama. Do not open services to repair a build.

### RV-002 [Medium]: Live private SQL/log/restart/browser behavior is unproved

* Evidence: infra/tests/test_staff_azure.py and cut-over criterion audit.
* Impact: fake az cannot establish permission propagation, logstream endpoint
  reachability, actual SQL transactions, Azure deletion/retention or real people.
* Destination: distinct authorized validation follow-up after RV-001.
* Next action: execute check then apply using the same private roster, verify
  codes-free outputs/cleanup and authorized browser sign-in. Keep issue criteria
  unchecked until the coordinator has actual evidence.

### RV-003 [Low]: Cross-host serialization and hard-kill cleanup remain manual

* Evidence: existing advisory lock behavior and new leftover-job runbook.
* Impact: no Azure-enforced cross-host mutex or finally guarantee on power loss
  is claimed. SQL transactions protect individual writes, not operator windows.
* Destination: distinct operational rehearsal/hardening follow-up if needed.
* Next action: serialized operator window; inspect exact owned job before
  stop/delete, then check persisted SQL state before retry. Do not regenerate
  an existing immutable roster or delete unowned/source resources.

## Defects and Remaining Work

No known source-blocking defect identified in this one review. All three
findings are explicit live/operational residuals, not silently completed
acceptance criteria. No correction/re-review loop is requested. No source-plan
tasks remain; commit/push/PR publication is still parent-owned.

## Validation Evidence

| Validation | Result | Boundary |
| --- | --- | --- |
| Installed source distributions with pip in session venv after missing-package failure | Passed | No package-manifest or system environment override |
| Absolute-PYTHONPATH unittest discovery, infra/tests | 304 passed, no skips | Final source state, including nullable ARM registry response |
| Absolute-PYTHONPATH test_auth | 32 passed | Responsive loopback app with synthetic fixtures; expected missing-law-store diagnostic, no model call |
| Ruff E/F/I/B/UP and format, all ten CI-gated infra files | Passed | New gates persisted in src-ci.yml; existing workflow/check names unchanged |
| Scoped mypy, worker and transport | Passed | Uses existing dynamic SQL interfaces; not full-repository type coverage |
| Standalone Bicep build/lint and full-suite compiled-template checks | Passed | Local compiler only; no Azure management call |
| Git diff/append-only log/link review | Passed | No mvp/prototype/private dataset/env/editor/issue-tracking edits |
| Azure/image build/tenant/browser/human approval | Not run | Explicitly forbidden or outside offline evidence boundary |

## Outcome

Execution: Complete. Outcome: Residual work.

Offline implementation is consistent with the requested behavior and safety
boundary; it is not a conformant live-deployment acceptance claim while RV-001
through RV-003 remain. No invented approvals, legal activation, resident consent,
safety decisions or financial commitments are introduced. ADR 0005's accepted
synthetic-development-only status is preserved.

## Closeout Routing

Parent publishes the existing topic branch and PR with Refs #360, without
merging or ticking issue criteria. RV-001 is the first authorized follow-up;
RV-002 depends on it. RV-003 remains a separate operational constraint.

## Correction cycle 1 Review opening (2026-10-17)

Task remains 360-run-in-azure, PR #370 on feat/run-in-azure-360.
One read-only Review for the explicitly requested correction cycle, not a
repetition of the original implementation Review above. Compared boundary:
delta from 296037b239d20179de4048f0bc9f837b4704bb86 in both workflow installs,
infra/tests/test_pipeline.py, quality-gate runbook and correction sections of
the same research/plan/details/critique/changes/state artifacts.
P03-T01/T02 complete; P03-T03 publication is parent-owned after this Review.
No source edits or follow-up implementation are authorized by this Review.
Execution: In progress. Prior RV-001/RV-002/RV-003 remain unresolved.

### Correction reconciliation and assessment

* P03-T01: both actual full-infra discovery steps install the existing hashed
  runtime lock, explicitly supplying real AES-GCM. PyYAML pin, test discovery,
  workflow/check names and all guards remain. A single new test method
  rejects all six missing/unhashed/late-install mutations in both workflows.
* P03-T02: fresh Python 3.12.3 pip-only /tmp venv with no system site packages
  reproduced the CI failure, then passed the full suite after the exact
  workflow dependency installation. No test skips or mocked crypto.
* The prior manifest whitelist and non-vacuous decoded-result timeout tests
  from 126ecae are preserved byte-for-byte, as are transport runtime and
  proof Dockerfile. Source delta is confined to workflow test setup, its
  existing contract tests and the directly related quality-gate instructions.
* PC-009 was rejected correctly: the worker's /tmp restriction is contradicted
  by the parent's actual successful venv creation and failure reproduction.
  Substituting project-local storage would violate explicit caller direction.
  One correction-candidate critique only; no unresolved significant decision.
* The runbook dependency instructions are an immediately relevant update,
  not a policy or architecture divergence. Plan/details/changes/state reflect
  completed P03-T01/T02 and parent-owned P03-T03 publication.

### Correction validation commands and results

`V=/tmp/ama-360-correction1-YRmaea`. Exact expanded lint file set and complete
commands are also retained in the correction changes record.

| Command or check | Result |
| --- | --- |
| `python3 -m venv "$V"`; source `pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`; `pip install 'PyYAML==6.0.3'`; staff unittest discovery | Expected baseline exit 1: 21 tests, 14 failures/four errors, absent cryptography; same failure as run 38983585607 |
| `"$V/bin/python" -m pip --quiet install --require-hashes -r src/api/requirements.txt`; `"$V/bin/python" -m pip check` | Passed, cryptography 50.0.2, PyYAML 6.0.3, no broken requirements |
| `REQUIRE_AZ_BICEP=1 "$V/bin/python" -m unittest discover -s infra/tests -q` | 307 passed, no skips, 67.359 seconds |
| `"$V/bin/python" -m unittest discover -s infra/tests -p test_staff_azure.py -v` | 21 passed, real crypto/context/timeout/cleanup regressions |
| `"$V/bin/python" -m unittest discover -s infra/tests -p test_pipeline.py -q` | 28 passed, including six operator-dependency mutation subcases |
| `"$V/bin/python" -m pip --quiet install 'ruff==0.17.1' 'mypy==2.4.0'` after missing Ruff exit 127 | Existing CI pins installed in the disposable venv only |
| `"$V/bin/ruff" check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 $FILES` and `"$V/bin/ruff" format --isolated --line-length 100 --check $FILES` | All ten existing CI-gated files pass, ten already formatted |
| `"$V/bin/mypy" --strict src/check-container.py`; `"$V/bin/mypy" --strict infra/scripts/pipeline.py`; `"$V/bin/mypy" --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff-azure-worker.py` | All three passed |
| `for file in infra/*.bicep infra/modules/*.bicep; do az bicep build --file "$file" --stdout > /dev/null || exit 1; az bicep lint --file "$file" || exit 1; done` | Passed, local Bicep 0.48.1 only, no Azure management request |
| `git diff --exit-code 296037b -- infra/.dockerignore infra/tests/test_staff_azure.py infra/cutover-proof.Dockerfile infra/scripts/staff_azure.py`; `git diff --check` | Passed, prior corrections unchanged |
| `"$V/bin/python" /home/azureuser/.copilot/session-state/7f2b1f61-4561-4385-be14-7db4ef3c98a0/files/correction1-mutations.py` | Three baseline tests pass; seven source mutants killed by intended assertion, no errors/skips; six workflow mutation subcases rejected |

Mutation boundary: five context negative controls remove parent/file inclusion
pairs for the four staff scripts and app-registration manifest; two transport
negative controls accept decoded output before Succeeded or remove execution
timeout refusal. All use in-memory mutation and real crypto. Initial removal
of a single staff file allowance survived the old context test's prefix matcher
because the parent inclusion still matched; this limitation is recorded rather
than hidden. The final pair mutations prove omitted-source detection, not full
Docker ignore semantic equivalence or a built image. Actual image validation
remains RV-001/RV-002, not a new inferred pass.

### Correction findings, routing and outcome

No source-blocking defect identified in the bounded dependency correction.
Review execution: **Complete**. Outcome: **Residual work**, because the
original deployment/acceptance findings are explicitly still open:

* RV-001 [Medium]: authorized private image build/publication, pinned digest
  and API-only restart-role activation remain unexecuted. Same authorized
  deployment follow-up; no action taken here.
* RV-002 [Medium]: actual tenant/mailbox authority, private log/SQL/job cleanup,
  restart/fresh replicas and real browser/human acceptance remain unproved.
  Same operator validation follow-up after RV-001; no live Graph work.
* RV-003 [Low]: cross-host serialization and hard-kill cleanup remain an
  explicit operational rehearsal/recovery boundary.

No Azure writes/deployments/image builds/role assignments/secrets/private data,
service exposure, spending or resource-group deletion. No test skipping, guard
weakening, merge or force-push. Remote CI at the to-be-published correction head
has not run yet and is not represented by these local results.
Parent may reconcile publication receipts and push/update PR #370 with Refs
#360, then stop as requested. This Review does not start a second Review,
source correction or automatic follow-up task.

### Parent publication evidence (not another Review)

Reviewed correction source was committed and pushed as
6976ae9649de291409c771986b818b83e0ebc8ae. PR #370 update/readback confirmed
the same branch/head and open main-targeting PR. Full infra discovery was
rerun at that committed head, using the same clean /tmp pip venv:
`REQUIRE_AZ_BICEP=1 /tmp/ama-360-correction1-YRmaea/bin/python -m unittest discover -s infra/tests -q`;
307 passed, no skips, 66.039 seconds. Final receipt publication changes only
tracking artifacts; assessed executable/workflow/runbook tree remains identical.
Review remains Complete / Residual work, with all original live blockers open.
