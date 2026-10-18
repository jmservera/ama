# Changes: Local-first validation and Actions budget

## Correction 2 Authorized Implement Opening (2026-10-18)

User/coordinator authorized three independently reproduced defects at clean
491124fcd406afea387cd95d555adcc8f9f00bde on the existing topic and unchanged
612cbed7 base: missing mandatory checks accepted by group-only verification,
host lock varying with caller temp environment, cancellation swallowed by retry
and nonretry collection. Reopened P01-T02 then coupled P02-T01 before source
edits. P01-T01/P03 remain historical complete and outside this write scope.
Only tools/rpi-checks.py, tools/test_rpi_checks.py and dated evidence/state may
change. Preserve independently confirmed RV-001 data-only verification and
all existing assertions within 12 focused methods and the original two infra
files already touched; no further infra/domain/helper/harness/workflow edits.
Original critique and adverse Review remain byte-for-byte unchanged; Review
SHA256 f2d752e762a0f222e3955ec58773d71d189f884cf3ec47966f5671139d8188f4.

Validation intent: focused regressions for required suite removal plus other
mandatory families, caller temp env and retry/nonretry cancellation; strict
Ruff/format/mypy, then privacy-safe commit with Copilot trailer. Execute complete
actual matrix at final clean HEAD into `/tmp/rpi-413-correction2-final`, verify
external receipt and make no later commit. Logs `/tmp/rpi-413-correction2.log`
and `/tmp/rpi-413-correction2-matrix.log`. No push, PR, cloud writes/spend,
private inputs, settings changes, new critique or original Review.

Remaining independent evidence review is explicit: reviewer read all 17 changed
files/5,372 lines and confirmed real receipt hashes/183 records/98 workflow
rows, suites, browser/SQL/images/scans/SPDX, but did not directly read all
102,046 original CLI lines, 19,659 corrected matrix lines or 19,451 command-log
lines. Programmatic inspection and partial reads do not establish complete
independent evidence review or acceptance. Coordinator/same reviewer owns it.

## Correction 2 P01-T02 / P02-T01 Source and Regression Evidence

tools/rpi-checks.py now binds both sealing and verification to trusted current
ordered command contracts for the entire matrix. It does not replay receipt
commands or execute environment interpreters. Contracts require exact argv,
cwd, sanitized overrides (including REQUIRE_AZ_BICEP and owned SQL opt-ins),
timeout, suite and integration identity, hashed unique log bindings and success.
Reparse every suite's test/executed/skip evidence; counts and skip reasons must
match the logged real result. Only exact bootstrap import probes may fail;
SQL query readiness can repeat at most 60 times and must end in success.
Interrupted, timed-out, unavailable or failed required checks cannot be relabeled
as probes. Schema 3 rejects older incomplete command contracts. The existing
data-only environment implementation is retained unchanged.

Pinned axe and browser outcome/executed scan evidence, scan version/image/
results, SPDX image/version/packages and clean snapshot evidence are checked.
Workflow coverage is rebuilt from the logged inventory using the same existing
classification function. Shared script/type-group/test-path constants avoid
divergent long command fragments. No new workflow framework/configuration
service or alternate executable matrix is introduced.

Host lock path is fixed /tmp/ama-rpi-heavy.lock, independent of caller temporary
environment; existing no-follow, bounded flock and serialized heavy work remain.
KeyboardInterrupt is handled separately from timeouts: exact owned child
process-group SIGINT permits helper finally cleanup, with bounded SIGKILL only
if needed. Record exit 130/interrupted=true, then rethrow before retry handling.
The outer matrix stops immediately and retains a failed receipt; only exact
owned SQL IDs and clean detached snapshot are removed.

All existing 12 focused methods remain; none removed or added beyond budget.
The tamper method constructs a complete command/evidence fixture and removes
every mandatory position one at a time, along with its file binding and a
consistent checksum. All reject. Combined removal of all eight mandatory
suites also rejects despite unchanged groups and remaining install/lint rows.
Selector/count/probe/infra-env/suite-log and browser/scan/SPDX/workflow-result
tampering reject. Existing replacement interpreter/malicious startup tests
continue to prove inert verification. Caller temp variants reach one fixed
lock path. Both retry/nonretry signal-15 KeyboardInterrupt probes stop later
commands/groups, record failed evidence and remove only the exact owned
container and detached snapshot. No expensive concurrent probe was run.

Actual coherent validation: 12 methods pass, Ruff 0.17.1 isolated E,F,I,B,UP /
py312 / line length 100 passes, isolated format --check passes and mypy 2.4.0
--strict passes for both files. Log:
/tmp/rpi-413-correction2-checks-final.log. Earlier fixture hash/lint/type failures
remain in external logs and were corrected before the final pass. Owned initial
formatter cache was removed; subsequent caches are external.

Read-only historical contract compatibility: every argv/cwd/timeout in the
183 actual prior command records matches 179 trusted mandatory positions plus
bounded SQL readiness retries. Data-only result verification also passes.
In-memory removal of all eight suites and representative Bicep, scanner,
browser and project lint/type families rejects, including removed file bindings.
Log: /tmp/rpi-413-correction2-historical-contract.log. This is supporting
regression evidence, not a current final-head gate or independent acceptance.

P01-T02/P02-T01 and containing phases are marked source/regression complete.
P01-T01/P03 are unchanged historical completion. User supplied independent
confirmation of RV-001 is retained; no original critique or adverse Review
changed, reran or became accepted. Original Review SHA256 remains
f2d752e762a0f222e3955ec58773d71d189f884cf3ec47966f5671139d8188f4.
Exactly the original two infra test files differ from base, neither in this
cycle. No domain, browser/container helper, workflow or pin changed.

## Correction 2 Final Commit and Freeze Boundary

Commit these two source files and dated evidence with GitHub-resolved local
noreply author/committer and required Copilot trailer. Then execute the complete
actual matrix, not a simulated subset:

`PATH="/tmp/rpi-413-tools:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd --out /tmp/rpi-413-correction2-final`

Fetch main, then verify using the same PATH/bytecode policy:
`python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-413-correction2-final/receipt.json --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd`.
Actual post-commit outcomes remain external in that receipt,
/tmp/rpi-413-correction2-matrix.log, /tmp/rpi-413-correction2-verify.log and
/tmp/rpi-413-correction2.log. This pre-freeze checkpoint predicts no pass.
No later commit, source modification, push or PR. Independent same-reviewer
candidate assessment and remaining complete verbose evidence review are
explicitly pending; no fabricated acceptance, hosted control or human approval.

## Approved Scope and Execution State

* Task: actions-budget-local-rpi, full plan P01 through P03.
* Plan: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md
* Details: .copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md
* Initial execution entry: Starting P01-T01; no implementation code written yet.
  Current execution and adverse original Review are recorded chronologically below.
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

## P03 Complete and Pre-Review Reconciliation

Run05 passed and verified all 17 groups and 183 actual command rows for
2c98c0e3fac0657bb67f093ac8f4561685c8c8d3 at the unchanged reviewed base.
Receipt: `/tmp/rpi-413-run05/receipt.json`. There are 98 native workflow step
coverage rows. Five project test/skip counts remain 1194/149, 105/0, 935/300,
46/0 and 39/0; focused 12/0, infra 359/0, SQL 243/1 (242 applicable executed).
Browser checks and verified axe ran; final snapshot inputs are empty.
All four fixable gates contain zero findings. Each full report contains
61 HIGH and two CRITICAL unfixed package findings, retained without ignores.
SPDX-2.3 package counts: API 130, agents 110, orchestrator 129, importer 122.
Actual DB UpdatedAt 2026-10-18T13:11:41Z, NextUpdate 2026-10-19T13:11:41Z.
Image IDs, report/SBOM hashes and every command/skip reason are in the receipt.

All in-scope implementation markers are now complete with actual evidence.
No executable divergence or domain/helper change remains. The accepted original
critique and both parent dispositions are unchanged. Review readiness is local
implementation complete, not whole-issue delivery: independent exact-head
assessment, publication authorization, remote context mapping and hosted checks
remain expressly unperformed. Execute one original RPI Review, preserve its
verdict/findings, commit these reconciled artifacts, then rerun for final HEAD.

## One Original Review Complete: Not Accepted

The original read-only Review compared full source, actual receipt/log/report
hashes, all plan/details markers, research, unchanged original critique and live
issue #413. It executed once directly in this qualified session, without a
review worker. Record:
.copilot-tracking/reviews/logs/2026-10-18/local-rpi-validation-review.md.

Execution is Complete; outcome is Not accepted. RV-001 High (10/10) reproduced
a verifier trust-boundary defect: environment_identity launches an external
receipt-adjacent Python binary before checking its environment/startup
identity or complete evidence. A safe marker-only disposable fixture ran that
binary before the verifier rejected the incomplete receipt. Probe log:
`/tmp/rpi-413-evidence/original-review-verifier-probe.log`, also appended to
the full actual CLI log. Fixture cleanup completed; no private data or network
was accessed. Source and tests were not changed during Review.

No correction, closure verification, second original Review or new critique
was performed. Route RV-001 to a separately authorized corrective Implement
invocation. The 17 passing groups do not override this adverse finding.
Independent exact-head assessment, 403 context mapping, publication permission
and retained hosted checks remain coordinator/owner gates.

## Final Artifact Commit and External Receipt Handoff

This record is committed before the requested final full matrix. Its execution
outcome is intentionally not predicted here. The authoritative final evidence
is `/tmp/rpi-413-final/receipt.json`, its sidecar and command/report logs, if
the actual final run succeeds and verifies. Until then run05 is historical
implementation evidence only. No commit after the final run is permitted
without a fresh complete rerun; the external receipt avoids self-reference.

Final matrix command, using the recorded base and restored user-space tools:
`PATH="/tmp/rpi-413-tools:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd --out /tmp/rpi-413-final`.
Verify with the same PATH/bytecode policy and
`python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-413-final/receipt.json --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd`.
Full actual CLI output remains `/tmp/rpi-413-local-validation.log`.

The requested handoff is a clean frozen local candidate, not accepted delivery.
Even a passing final receipt must retain RV-001 as a publication blocker.
Do not push, open a PR, touch another worktree or resume unrelated backlog.

## Distinct Authorized RV-001 Implement Invocation: Opening State

On 2026-10-18 the owner explicitly authorized correcting only RV-001 and
directly coupled regressions using the accepted plan. This is a distinct
Implement invocation, not a new Research, critique or original Review.
The original adverse Review remains immutable, with SHA256
f2d752e762a0f222e3955ec58773d71d189f884cf3ec47966f5671139d8188f4.
Starting HEAD is 15ac3766437b03d0f0df892fcd747b4310f124a9; branch and supplied
base match; candidate was clean, no open PR exists, fetched main is unchanged.
Original full execution log and all adverse receipts remain external untouched.

Reopened P01-T02 then P02-T01 (and their containing phases) for the bounded
implementation; previous completion evidence is historical, not erased.
P01-T01 and P03 remain complete and outside source scope. Approved write
boundary is runner/tests and dated plan/details/changes/state. Replace external
environment execution with bounded data-only interpreter/config/package/startup
inspection. Keep all complete-matrix checks and explicit errors; no allowlisted
execution or fallback. Extend the existing test categories within 12 methods.
All pins, domain tests, container/browser helpers and the two-infra-file limit
remain unchanged.

Validation intent: focused 12-method regressions and strict Ruff/format/mypy,
then commit source and reconciled evidence, run a fresh complete actual matrix
on clean final HEAD, verify the external receipt and make no later commit.
Log: `/tmp/rpi-413-verifier-correction.log`. RV-001 is not yet implemented;
independent acceptance remains coordinator-owned. No push or PR is authorized.

## RV-001 P01-T02 and P02-T01 Implementation Evidence

Replaced receipt-adjacent `python -m pip freeze --all` execution with bounded
trusted-code data inspection in tools/rpi-checks.py. Hash pyvenv.cfg, interpreter
bytes/un-followed symlink text, complete distribution metadata (including
versions, editable direct_url and RECORD) and .pth/customization/editable startup
files plus corresponding cached startup identities. Inspect no imported module,
execute no external environment interpreter, and reject symlinked/nonregular
metadata or exceeded explicit entry/depth/per-file/aggregate limits. The same
inspection seals and verifies identities. Schema 2 prevents old executable-
inspection receipts from being accepted under the changed identity contract.
No command matrix, dependency pin, domain/helper assertion or workflow changes.
Updated directly related src README inert-receipt guidance.

Expanded the existing tampered-receipt method, keeping exactly 12 focused
methods. Disposable real no-pip venvs replace the old mocked environment
identity. Valid fixture verification succeeds; changed interpreter executable,
malicious .pth/sitecustomize/usercustomize/editable code, package METADATA,
editable URL and pyvenv.cfg all reject with no marker execution. A verification
subprocess spy refuses any environment invocation. Oversized metadata, symlinked
startup/package metadata, FIFO and missing METADATA also reject. Restored
identity verifies again. Existing dirty/group-completeness assertions remain.
Original Review and original critique have no diff.

Targeted checks actually executed:

* `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools
  -p test_rpi_checks.py -v`: 12/12 pass; final log
  `/tmp/rpi-413-correction-targeted-final.log`. Expected adverse subprocess
  fixtures remain reported, not suppressed.
* Existing Ruff 0.17.1 isolated E,F,I,B,UP/py312/100 check and format:
  pass; strict mypy 2.4.0 for both runner files: pass.
  Log: `/tmp/rpi-413-correction-static.log`. Initial B023 closure lint failure
  was fixed by nesting distribution records; no failed check is called passed.
* Twice inspected all six actual historical runner environments as inert data:
  12 identities stable. Log:
  `/tmp/rpi-413-correction-real-environments.log`.
* Git diff/whitespace and original Review SHA256 checks pass. Original Review
  remains f2d752e762a0f222e3955ec58773d71d189f884cf3ec47966f5671139d8188f4.
  Exactly the original two infra files differ from base; neither changed here.
  Browser/container helpers and all domain tests have no corrective diff.

P01-T02 and directly coupled P02-T01 are checked with this implementation
evidence; their phases reconcile accordingly. RV-001 implementation disposition
is addressed, not independently accepted or a changed original Review verdict.
All adverse historical evidence is preserved. No new Research, critique or
Review has executed. Coordinator owns independent exact-head assessment and
publication/context/hosted approval; no push or PR is authorized.

## Corrective Final-Commit Freeze Protocol

Commit this source and reconciled dated evidence using the GitHub-resolved
repository-local noreply identity and required Copilot trailer. This checkpoint
cannot truthfully predict the post-commit matrix result. Run with fresh external
output, using the unchanged supplied/fetched base:

`PATH="/tmp/rpi-413-tools:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd --out /tmp/rpi-413-verifier-correction-final`

Then fetch main and use the same PATH/bytecode policy to execute:
`python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-413-verifier-correction-final/receipt.json --base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd`.
Actual complete matrix and verification logs:
`/tmp/rpi-413-verifier-correction-matrix.log` and
`/tmp/rpi-413-verifier-correction-verify.log`, alongside the full corrective
execution transcript `/tmp/rpi-413-verifier-correction.log`. Do not overwrite
prior outputs, change/commit candidate files afterward, or publish. A failed
run remains adverse evidence, never a passing receipt. The final external
receipt and logs are authoritative for freeze outcome, not this pre-run record.
