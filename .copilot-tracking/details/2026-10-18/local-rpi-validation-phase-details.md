# RPI Phase Details: Local-first validation and Actions budget

## Metadata

* Task ID: actions-budget-local-rpi
* Task slug: local-rpi-validation
* Related plan: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md
* Planning state: Complete, both findings from the single critique resolved;
  full-plan implementation approved on 2026-10-18 and P01 starts first.
* The owner will disable MVP CI and MVP validation; transition validation must
  not rely on those workflows. Other backlog pushes and merges remain paused.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Local gate | RV-001 source/tests complete; final exact-head matrix pending | P01-T01, P01-T02 |
| P02 | RPI integration | Data-only verification regressions pass; independent acceptance pending | P02-T01 |
| P03 | Hosted transition | Complete local implementation; run05 verified at 2c98c0e3 | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement a complete local validation gate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Establish exact workflow-to-local coverage

Read each unique job and retain its behavior, tool version, environment and
failure rules. Deduplicate equivalent invocations, not superficially similar
checks. Inventory SQL Server selectors, image hardening, Trivy, SPDX, migration,
browser and infrastructure checks before recommending a disable.

### Command Matrix

Commands below describe the existing equivalents; implementation will execute
argv arrays with explicit working directories and a sanitized environment, not
an eval-based shell dispatcher. Paths are repository-relative. OUT and VENV are
private session scratch, never configured ZF_DATA or a tracked directory.
The command inventory is canonical at base 612cbed7 and must fail visibly if
workflow steps drift without a matrix update.

| Group | Existing command/equivalent |
| --- | --- |
| Package installation | One Python 3.12 venv per project plus namespace/integration venv. Use each project's existing dev extra and matrix dependency order: core alone; agents/orchestrator/importer with core; api with core and agents. Reuse venv only when manifest/tool identity matches; do not install dependencies from an unrelated published distribution instead of the sibling checkout. |
| Five project suites | From each src/project: python3 -m unittest discover -s tests -v; ruff check .; ruff format --check .; mypy. API PYTHONPATH includes absolute core/tests and agents/tests. Agents/orchestrator include core/tests. Preserve importer/core unset test-path behavior. |
| Namespace integration | Install all five distributions side by side; python3 -m zava_forward.core/agents/orchestrator/importer separately; import zava_forward.api.version.__version__; assert namespace __file__ is None and five __path__ entries. |
| Compile | python3 -m compileall -q src/core/src src/agents/src src/api/src src/orchestrator/src |
| Browser JS | node --check src/api/src/zava_forward/api/web/app.js; node --check src/api/src/zava_forward/api/web/assistants.js |
| Tracked-data guard | Refuse any git ls-files result for */.assistant-test-*, mvp/data and :(glob)src/**/data/**; use tracked paths only and never read private data. |
| Bicep | az bicep version; build --stdout and lint every infra/*.bicep and infra/modules/*.bicep; no deploy/what-if and no Azure login needed. |
| Infra suite | Existing PyYAML==6.0.3 and hashed src/api/requirements.txt; REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v |
| Special infrastructure lint | Ruff==0.17.1 with --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 plus isolated format --check, on exactly the groups below. |
| Tool type checks | mypy==2.4.0: --strict src/check-container.py; --strict infra/scripts/pipeline.py; --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff-azure-worker.py infra/scripts/credential_arm.py |
| Workflow syntax | actionlint -config-file infra/tests/actionlint.yaml .github/workflows/infra-plan.yml .github/workflows/src-deploy.yml .github/workflows/src-ci.yml; also lint the two legacy native workflows during transition without applying native actionlint to gh-aw Markdown/lock generation. |
| Browser harness strict lint | Exact isolated Ruff check and format flags above for src/api/checks/design_system_browser_check.py and src/api/checks/regulatory_ux_check.py, outside migration exemptions. |
| Browser runtime | In API dev venv: python3 -m playwright install --with-deps chromium only if missing; python3 -m checks.design_system_browser_check; PYTHONPATH includes api/tests, core/tests and agents/tests for python3 -m checks.regulatory_ux_check --axe <verified-axe-4.10.3-path> --out OUT/regulatory-ux-results.json. |
| Migration | Existing tools/rename-zava-requirements.txt then python3 tools/rename-zava-tests.py |

Exact special Ruff groups from src-ci.yml:

* infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py
* infra/scripts/pipeline.py infra/tests/test_pipeline.py
* infra/scripts/staff_azure.py infra/scripts/staff-azure-worker.py infra/scripts/credential_arm.py infra/tests/test_staff_azure.py
* src/check-container.py infra/tests/test_container_contract.py

Do not duplicate API and orchestrator unittest discovery a second or third time
solely because the legacy workflows did. The respective isolated project
environment and explicit SQL run retain different dependency/runtime coverage.
Package bootstrap is triggered by missing prerequisites or manifest drift, not
unconditional global pip installs on every RPI turn.

### Actual SQL Server Gate

Use mcr.microsoft.com/mssql/server:2022-latest as the current workflow's image,
record the resolved digest, accept its EULA for this disposable test only, and
generate an ephemeral strong test password outside logs. Select an unused
loopback host port and runner-owned container. Test readiness with a real query,
not process existence alone. Isolate one empty disposable database; never reuse
pilot or owner connection settings. Refuse a SQL target not mapped to the
runner's exact owned container/port before running destructive tests.

Set only in the test process: ZF_TEST_MSSQL=1, ZF_SQL_SERVER to the owned loopback
endpoint, ZF_SQL_DATABASE to the disposable database, ZF_SQL_AUTH=password,
ZF_SQL_USER=sa, generated ZF_SQL_PASSWORD, ZF_SQL_TRUST_CERT=1.
Install the existing hashed API runtime requirements after a missing dependency
check, and verify libltdl7/libkrb5-3 driver prerequisites.

From src/api with PYTHONPATH=tests:../core/tests:../agents/tests:

```bash
python3 -m unittest test_mssqlstore test_lawstore.MssqlStoreTests \
  test_assistants.MssqlContractTests test_assistants.MssqlReviewTests \
  test_assistants.MssqlDurabilityTests test_assistants.MssqlApiTests \
  test_assistants.MssqlLedgerTests
```

Count executed/skipped tests and explain existing skips individually. All
selected MSSQL contract tests must actually run; missing driver, disabled env
or inaccessible service blocks a complete pass. Existing suite-owned SQL
functions already wipe tables, which is why endpoint ownership is mandatory.
Clean up only the exact container/database created by this receipt.
Actual execution identified one inherited JSON-only non-applicable method:
test_mssqlstore.MssqlHazardReferral.test_json_postsave_audit_failure_reports_persisted_uncertainty,
reason "JSON-only separate-file audit ordering". Only that exact ID/reason is
accepted in the explicit SQL gate; it is counted, not hidden.

### Image and Scan Gate

For each api, agents, orchestrator and importer:

```bash
docker build -f src/PROJECT/Dockerfile -t zava-forward-PROJECT:RECEIPT src
python3 src/check-container.py PROJECT zava-forward-PROJECT:RECEIPT
trivy image --config src/trivy.yaml --scanners vuln --severity HIGH,CRITICAL \
  --ignore-unfixed --exit-code 1 --format json --output OUT/PROJECT-gate.json IMAGE
trivy image --config src/trivy.yaml --scanners vuln --severity HIGH,CRITICAL \
  --exit-code 0 --format json --output OUT/PROJECT-all.json IMAGE
trivy image --config src/trivy.yaml --format spdx-json \
  --output OUT/PROJECT.spdx.json IMAGE
```

PROJECT, RECEIPT, OUT and IMAGE above are explanatory placeholders, not shell
interpolation instructions to paste unreviewed. Trivy version is 0.76.0.
The all-findings command relies on src/trivy.yaml ignore-unfixed=false; ensure
no inherited Trivy variable reverses it. Nonzero scanner errors fail even the
report-only command. Capture vulnerability database freshness; an unavailable
or stale DB is not a clean scan.

The API unreadable-logo scenario is distinct: export a clean candidate build
snapshot into private scratch, set only that snapshot's logo mode to 0600,
build its API image and reuse check-container.py to verify the PNG byte/content
type response under hardened/plain startup. Record this deliberate test-input
mode change and image digest; do not chmod or dirty the actual issue checkout.
Using a second build avoids claiming the mode-stress image is the canonical
source-mode image. Never weaken Dockerfile permissions to satisfy this probe.

The existing container helper already uses random container IDs and dynamic
loopback ports, and cleans up its API startup probes. Reuse it unchanged.
Serialize heavy builds/scans/SQL/browser across loops with a shared host lock;
record lock timeout as blocked, not skipped. Determine feasible resource caps
from one baseline run on the 16 GB VM, leave OS headroom and constrain only the
new runner's containers. Do not kill or prune unrelated containers/images.

### Cloud and Managed-Workflow Boundary

Local gates can test the pipeline's fake-command and local HTTP contracts, not
GitHub job dispatch, reviewer enforcement, environment protections or job OIDC.
Approved Azure what-if and deployed HTTP/SQL probes could be invoked from an
authorized host, but they remain authenticated cloud integration evidence, not
an automatic local/no-spend check. This task must not execute them or grant new
credentials. Manual publishing still requires the existing private ACR route.
Independent CLI review replaces hosted Copilot review only under owner policy.
Final capstone scoring and real AI acceptance remain separately controlled.

### Completion Evidence

One row per workflow step in the runner manifest/matrix, zero silently omitted
unique checks, each nonlocal obligation explicitly classified, and exact command
parity checked against the current workflow revisions.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement the runner and focused failure tests

Likely new targets: tools/rpi-checks.py and tools/test_rpi_checks.py.
Existing suites own domain behavior; new tests own only orchestration,
failure propagation, isolation and evidence validity. Exact limits and commands
are fixed in the parent plan before critique: no test removals, at most 12 new
orchestration test methods, at most two existing infra-test file updates, and
no new domain/runtime tests. The existing check-container helper remains
unchanged; add orchestration rather than a second container test implementation.

Validate the runner with its 12 bounded failure categories and one actual full
matrix. The manifest must never be marked passed while a required group is
unavailable, a scanner/database failed, or tracked content changed mid-run.
Run in a fresh owned detached exact-HEAD worktree, with editable installations
bound to that snapshot. Reject untracked source/test/config inputs during
receipt creation and verification; an unchanged HEAD is insufficient if
uncommitted inputs influenced tests. Reject original candidate contamination
as well. Do not copy ignored inputs into the snapshot. Put venvs, TMPDIR,
Ruff/mypy caches and evidence outside the snapshot, disable Python bytecode
writes, and reject unexpected residual source inputs without exposing private
path names. Test untracked source, tests and config as parameterized variants
of the fixed dirty-input test category. Validate snapshot identity before and
after execution; remove only the runner-owned snapshot after evidence sealing.
Store only sanitized output in PR-visible evidence. Scrub inherited cloud/AI/
SQL environment and per-user credential locations from child test processes;
block accidental external model endpoints. Provisioning tools themselves
cannot be used to bypass an unavailable local prerequisite.

<!-- rpi:phase id=P02 -->
## P02: Integrate local evidence into RPI delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Make pushing conditional on exact-source local receipts

Likely targets: coordinator agent, component instructions and README. Preserve
full ordered RPI, original Review and independent assessment. Corrections and
rebases invalidate affected evidence; no success statuses are fabricated.

Persist current HEAD and the final receipt outside the repository; after
committing any copy of evidence, rerun against the actual final commit.
The exact-head source identity, not a timestamp or "tests ran earlier" claim,
is the push gate. Historical receipts are retained as historical, including
failed commands. Update the coordinator to refuse push/review/merge handoff
unless the current local gate verifies, while still requiring all reported and
required hosted checks until the owner explicitly changes policy.

Completion evidence: a disposable topic branch proves a failed command blocks
push orchestration, final matching evidence permits it, and source/base changes
invalidate it. Do not actually publish an intentionally failing PR to test this.

<!-- rpi:phase id=P03 -->
## P03: Consolidate hosted validation without coverage loss

<!-- rpi:task id=P03-T01 -->
### P03-T01: Verify protection and move unique hosted checks

Protection and ruleset APIs returned HTTP 403. Check contexts must not be removed
under an assumption that they are unused. SQL Server and SPDX belong to MVP CI;
compileall and migration regression belong to MVP validation.

Retain current legacy job names during transition; carry the mssql gate
unchanged in name unless required-context migration is approved. Move command
coverage before disabling triggers. Existing workflow tests reference both
src-ci.yml and mvp-validation.yml; keep the latter valid dispatch-only or update
their existing assertions to preserve equivalent placement/order/pinning
coverage, never delete the behavior tests merely to make consolidation pass.
No repository protection edits are part of this task.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Apply owner-approved trigger and disable changes

Source projects CI is the recommended retained hosted validator. Main-push
retests, intermediate branch pushes and privileged workflow_run dependencies
need explicit treatment. Azure/OIDC/approval and private publication are not
proved by successful local unit tests. Preserve manual release protections.

Recommended owner decision: keep the current pull_request event behavior, with
one consolidated hosted workflow per eligible PR update, manual releases
unchanged. A single final push is recommended but does not prevent another
matching correction/rebase from triggering another run. Cost scales with the
number of eligible updates, not just the number of PRs. Final-only/manual PR
validation is a separate unapproved policy choice, not current behavior.
Remove push-to-main duplicate triggers only after
the owner accepts losing independent post-merge regression detection; rebase
and rerun the local matrix against latest main before final review. Local
verification cannot eliminate all PR-to-merge race risk.

Optional emergency mode is not the default: temporarily disable automatic
validation only after explicit owner authorization, verify required-context
consequences, suspend automerge unless its acceptance policy is deliberately
changed, and disclose reduced independent assurance. No skip-ci trailers or
fabricated green contexts. Do not re-enable automated delivery implicitly.

Rollback evidence: initial trigger definitions are at base
612cbed78a35a4ab426571aa7d2aeb0ae6d691dd. Both MVP workflows were observed
disabled_manually before local edits. Restore those trigger definitions by a
reviewed follow-up commit if parity/enforcement regresses. Only the owner may
authorize `gh workflow enable mvp-ci.yml` and
`gh workflow enable mvp-validation.yml`; these commands were not executed.
Final-head hosted confirmation and required-context mapping remain coordinator
gates before merge, not local checks or blockers to independent implementation.

## Original Review and Local Freeze Boundary

The one original Review is Complete, outcome Not accepted. RV-001 reproduced
unvalidated external-environment code execution during receipt verification.
See the original Review at
.copilot-tracking/reviews/logs/2026-10-18/local-rpi-validation-review.md.
This is not a plan-critique rerun or a source correction. Preserve it unchanged.
The final artifact commit and exact-head matrix/receipt freeze are evidence
collection, not closure of the finding. No push is permitted; coordinator routes
a distinct corrective Implement invocation before publication can be accepted.

## Authorized RV-001 Implement Invocation (2026-10-18)

The owner authorized this distinct invocation on the existing branch/base.
Scope is P01-T02 and directly coupled P02-T01 verification only. Preserve all
original execution/adverse receipts, the accepted critique and the original
Not accepted Review byte-for-byte. No Research, critique or Review runs again.
Original Review SHA256:
f2d752e762a0f222e3955ec58773d71d189f884cf3ec47966f5671139d8188f4.

Replace pip-freeze subprocess inspection with trusted runner inspection of
bounded regular environment metadata: interpreter/configuration identities,
distribution metadata and startup files, without launching receipt-adjacent
executables or importing startup code. Reject malformed, missing, over-limit
or changed metadata explicitly. A receipt sidecar grants no executable trust.
Retain all command/group/file/tool/image/DB completeness requirements.
Extend existing tampering coverage within the 12-method ceiling; demonstrate
non-execution and rejection for replaced interpreters and malicious .pth
content, plus package/startup identity binding and coupled bounds failures.
Do not change the matrix, pins, domain tests, container/browser helpers, or
either of the two already updated infra files.

First boundary: implement data-only identities, then targeted 12-method tests,
strict Ruff/format and mypy. Reconcile markers/evidence and commit using local
GitHub noreply author/committer with Copilot trailer. Run the full actual matrix
on that clean exact HEAD in a fresh external directory and verify its receipt;
no changes/commits afterward. Execution log:
`/tmp/rpi-413-verifier-correction.log`. No publication; coordinator independently
assesses the frozen exact-head candidate.

Corrective source/tests are complete. Data-only identity records pyvenv.cfg,
interpreter bytes or un-followed link text, all distribution metadata (including
METADATA/direct_url/RECORD) and .pth/customization/editable startup identities.
Per-environment bounds are 4096 enumerated entries, depth eight for metadata,
8 MiB per metadata/startup file, 64 MiB per regular interpreter and 128 MiB
aggregate. Nonregular files and symlinked package/startup metadata fail;
no interpreter or startup file is executed/imported by identity inspection.
Receipt schema 2 rejects legacy pip-freeze identities rather than silently
converting them. Complete-matrix/tool/file/image/DB verification is unchanged.

All 12 focused methods pass with real disposable no-pip venv fixtures, including
replaced interpreter, malicious .pth/sitecustomize/usercustomize/editable code,
package/config tampering, oversized metadata, symlinks, FIFO and missing
METADATA. Marker remains absent and verification subprocess calls are restricted
to existing trusted git/Docker checks by the test spy. Strict Ruff/format/mypy
pass. Two read-only inspections of all six real historical environments also
produce identical 12 identities. Source-independent helpers, pins, domain and
infra tests are unchanged in this invocation.

This committed checkpoint precedes final exact-head execution. Its actual
outcome must be read from the fresh external
`/tmp/rpi-413-verifier-correction-final/receipt.json` and full run/verification
logs, not inferred here. RV-001 implementation disposition: addressed by
data-only code and regression evidence, pending independent coordinator
assessment; original Review remains Not accepted and unchanged.
