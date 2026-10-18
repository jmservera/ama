# Changes: Local-first validation and Actions budget

## Approved Scope and Execution State

* Task: actions-budget-local-rpi, full plan P01 through P03.
* Plan: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md
* Details: .copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md
* Execution: Starting P01-T01; no implementation code written yet.
* Worktree: /home/azureuser/source/ama-wt/ci-budget-plan
* Branch: docs/local-rpi-validation-plan
* Base: 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd

## Owner Authorization and Priority

On 2026-10-18 the owner approved implementation first and stated that they will
disable MVP validation and MVP CI immediately. This changes the planning-only
boundary to full implementation of the approved runner and consolidation.
The implementation must preserve their real SQL, SBOM, logo-permission,
compile, migration and data-guard coverage locally and in the retained source
workflow before claiming complete validation. No workflow state is changed by
the coordinator. No protection change or Azure deployment is authorized.

Other issue pushes/merges remain paused; the stopped #137 worktree and its
original transcript are preserved. A missing check is never a green result.

## Write and Validation Boundary

Canonical runner and at most 12 new orchestration test methods; existing
workflow coverage in the approved files, at most two existing infra test file
updates, and coordinator/component guidance. Existing domain tests and the
container helper remain unchanged. No new plan critique or repeated original
Review is authorized.

Run focused orchestration/contract checks first, then the actual complete
matrix with exact-head receipt verification before push. Record actual command
results, failures, skip reasons, dependencies and any unavailable validation
here; do not fill in future results in advance. One original RPI Review and
independent exact-head assessment remain required.

## Current Limitations

Protection/ruleset APIs returned HTTP 403 during planning. Trivy/actionlint
were not on PATH; tools may be restored only after observed prerequisite
failure, respecting pins and pip-only Python policy. No new cloud credentials,
role assignments, resources, model calls or spend are authorized.

## Research and Accepted-Plan Reconciliation

Focused research actually inspected current workflows/source and live #413
before source edits. See the dated research artifact. Updated planning-only
acceptance wording to implementation acceptance from the live issue without
changing intent, test limits or original critique. Parent PC-001 and PC-002
dispositions remain authoritative; no new critique ran.

Observed both MVP workflows disabled_manually, missing Trivy/actionlint, and
403 protection/ruleset responses. This limits remote transition acceptance,
not independent local implementation. Main equals the supplied base.
The caller authorizes integration/commit of the four initial untracked
artifacts in this worktree. No other worktree is touched. No push or PR is
authorized; final exact-head independent assessment is still required.

## P01-T01 Coverage and P01-T02 Initial Implementation

The canonical matrix is implemented in tools/rpi-checks.py, with explicit
groups for the five environments, namespace/static/infra/migration/browser,
owned SQL, four canonical images and separate logo stress. Exact native
workflow hashes freeze command parity, including dispatch-only rollback files.
Existing helper and all domain suites are unchanged. The 12 focused test
methods passed locally; strict Ruff/format and mypy passed after ordinary
implementation corrections. Full matrix has not yet run.

Actual missing Trivy 0.76.0 and actionlint were restored from their official
GitHub releases into external scratch, verifying release SHA256 manifests.
Actionlint is 1.7.7. Driver system libraries were observed present. Native
workflow actionlint passed before transition. No system install or cloud
fallback was used. Initial author-created Ruff/mypy/bytecode scratch is removed
before committing so it cannot enter candidate validation.

### P01-T02 First Actual Matrix, Adverse Receipt Preserved

Candidate dfe39a2a ran the actual core suite: 1,194 tests, 149 declared skips,
three failures and one error. The runner incorrectly forced ZF_AI=off, which
prevented existing mocked-provider contracts executing. Removed that override;
instead scrub credentials/endpoints and install a runner-owned Python audit
guard denying non-loopback test connections. No domain tests were changed.
The original failed receipt and complete output remain external at
`/tmp/rpi-413-run01/receipt.json` and the CLI log. This is not a passing run.

Continue independent required groups after an individual gate failure to
collect honest coverage, while blocking receipt success. Retain unfixed-inclusive
reports and SPDX even when a fixable scan fails. These are in-scope runner
corrections, not a new plan or critique.

### P01-T02 Complete Execution with Explicit SQL Non-applicability

Run02 executed every required family, including actual Chromium/verified axe,
all four canonical images, unchanged hardening probes, separate logo0600 image,
all scans and SPDX. Five project discoveries: core 1194/149 skipped, agents
105/0, API 935/300, orchestrator 46/0, importer 39/0. Infra 359/0.
The exact real MSSQL selectors reported 243 tests, one inherited JSON-only
separate-file audit-ordering test skipped. The runner correctly refused its
unclassified skip, preserving the adverse receipt at
`/tmp/rpi-413-run02/receipt.json`; it is not a pass.

Source inspection and actual output establish that this one precisely named
JSON-only method is not applicable to MSSQL. Enumerate its exact ID/reason as
SQL non-applicability; all other explicit integration skips still block.
No test is removed or altered. Added verification of required evidence/image
coverage and external environment package identities inside the same 12-test
budget. Four fixable scan reports contain zero findings; each unfixed-inclusive
report contains 63 package findings. These are observed run02 results only.

### P01-T02 Post-run Snapshot Guard Found Harness-generated Inputs

Run03 completed all 17 required groups successfully, including 243 selected
MSSQL tests with the exact one JSON-only non-applicable method. The final
snapshot guard refused ignored inputs, so its receipt remains failed at
`/tmp/rpi-413-run03/receipt.json`. No claim of a passing gate is made.
The design-system harness creates a root .venv scratch parent and deliberately
scrubs its server's environment, dropping bytecode suppression. Inspection
identified this as the source of generated snapshot input.

Keep that harness unchanged: route its TemporaryDirectory to external scratch,
remove only its empty scratch marker, and supply external API-environment
sitecustomize to suppress server bytecode even after environment scrubbing.
No assertion or container helper is patched. Record final snapshot inputs and
retain any contaminated snapshot rather than force-removing it. Ensure SQL
cleanup occurs before image work even when the SQL gate fails. These changes
preserve fail-closed behavior and global heavy-resource serialization.

The first targeted browser probe showed Ubuntu's standard-library
sitecustomize precedes venv sitecustomize, so that attempted policy did not
suppress server bytecode. Its adverse log is preserved. Use an external venv
.pth startup policy instead. A second actual Chromium/axe probe passed with
an empty ignored/untracked snapshot list; only generated bytecode from the
first owned probe was removed after recording its relative paths. Both browser
harnesses and src/check-container.py remain unchanged.

## P01 Complete: First Verified Full Matrix

Run04 passed all 17 required groups and verified its receipt for exact HEAD
80927265264ae28b1f411a6414f3a97c3644592f, base
612cbed78a35a4ab426571aa7d2aeb0ae6d691dd. The external receipt is
`/tmp/rpi-413-run04/receipt.json`; full command logs and scan/SBOM output share
that directory. All 12 orchestration tests and 359 infra tests passed.
Project counts/skips match run02; SQL reports 243/1 precisely enumerated
non-applicability. Final snapshot input list is empty, candidate is clean,
and the owned snapshot/container were removed. Browser and all image checks
ran, not simulated. This receipt becomes historical when P02/P03 are committed.

P01-T01/P01-T02 now have actual completion evidence. Continue P02 then P03;
the final source/artifact commit requires a new full matrix and receipt.

## P02-T01 Complete: Canonical Pre-publication Gate

Updated the coordinator, repository instructions and src README to require
the complete command, external authoritative receipt, verify-before-independent-
review/push and correction/rebase/base invalidation. Removed the obsolete
mandatory mvp command and local-failure cloud fallback. The loop now returns a
frozen local candidate before coordinator publication authorization; it does
not repeat or replace the original Review. No public README depends on internal
tracking paths. Non-tool agent frontmatter and owner merge authority are unchanged.

The 12 focused tests pass on a disposable feat/receipt-fixture topic, including
nonzero/missing/timeout blocking, matching receipt verification, contamination,
tampering, missing coverage, source identity and base movement. Actual run04
receipt verification now returns BLOCKED against the modified candidate, as
required. No push was attempted. Guidance edits were executed in this qualified
session, not through a general-purpose author. HVE Builder criteria informed
the bounded edit; no separate fresh-context HVE lifecycle/behavior acceptance
is claimed. Independent exact-head assessment is still the coordinator's gate.

## P03 Implementation and Targeted Transition Evidence

Source CI now owns the exact unchanged `mssql` job and selectors, independent
of disabled legacy workflows. Its retained jobs add four SPDX outputs, a
separate external logo0600 archive/build/helper run, compileall, both JS checks,
the tracked-data/sandbox union, migration requirements/tests, focused runner
contracts/static checks and checksum-verified native actionlint. Browser axe
download is now required, with the existing harness verifying its pinned hash.
The new runner/test and migration inputs are in PR path filters.

Source CI retains eligible pull_request updates and dispatch, removes main
push repetition; both legacy files are dispatch-only with their original jobs.
No original test assertions were removed. Exactly two existing infra files
were extended: test_pipeline.py and test_container_contract.py. Their targeted
15 contracts pass, including full dictionary equality of the retained/rollback
MSSQL job, independent dispatch, trigger/path coverage, guarded SPDX policy and
unchanged Source CI workflow_run link. Native actionlint passes all five files.
Strict runner Ruff/format/mypy and the same 12 focused methods pass.

The runner records one coverage row per native workflow step, including explicit
hosted-only checkout/event/provisioning/upload/approval/release boundaries, and
pins final native workflow hashes. External environment startup-policy hashes
also bind the harness's bytecode isolation.

Both remote MVP workflows remain disabled_manually, Source CI/what-if/manual
release remain active; no state API write was made. Privileged infra-plan,
src-deploy and src/check-container.py have no diff. Duplicate legacy test/image/
validate contexts are not fabricated. The 403 mapping limitation is an owner/
coordinator pre-merge gate, not a reason to block approved local implementation.
Original triggers are recoverable from the recorded base; reviewed trigger
restoration and owner-only explicit enable commands are in phase details.
Main still equals the supplied base. Full consolidated matrix is next; no
hosted execution or publication is claimed.
