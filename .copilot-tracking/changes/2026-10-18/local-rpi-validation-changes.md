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
