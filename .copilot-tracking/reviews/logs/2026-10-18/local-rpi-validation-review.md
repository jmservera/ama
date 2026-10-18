<!-- markdownlint-disable-file -->
# Review: Local-first validation and Actions budget

## Scope and Evidence

* Task ID: actions-budget-local-rpi; slug: local-rpi-validation.
* Review date: 2026-10-18; scope: full P01-P03 local implementation.
* Assessed source: base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd through
  2c98c0e3fac0657bb67f093ac8f4561685c8c8d3, plus reconciled completion metadata.
* Plan: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md
* Details: .copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-18/local-rpi-validation-changes.md
* Research: .copilot-tracking/research/2026-10-18/local-rpi-validation-research.md
* Actual execution: /tmp/rpi-413-run05/receipt.json and its command logs,
  workflow coverage, browser evidence, scans and SPDX.

## Opening Review State

* Goal: execute the one original Review, assessing accepted requirements,
  implementation evidence, original critique dispositions and remaining gates.
* Scope: all approved local changes and dated evidence, not authorization to
  publish or merge. No claim of independent exact-head coordinator assessment.
* Readiness: all implementation markers reconciled; complete actual matrix
  verified on the implementation commit. Metadata edits invalidate that receipt
  for publication and require the final post-artifact-commit rerun.
* Acceptance basis: live issue #413, owner-qualified local-only invocation,
  accepted full plan/details and parent dispositions PC-001/PC-002.
* First boundary: source-bound failure behavior and unique workflow coverage,
  followed by RPI evidence and hosted-only limitations.
* Read-only boundary: write only this original Review record; no source fixes,
  new critique, amended Review or repeated Review.
* Initial blockers: independent assessment, protection mapping, hosted checks
  and publication are intentionally outside this invocation. Local evidence is
  available; these limits do not prevent an honest local review.

## Execution Status and Outcome

* Execution status: Complete.
* Outcome: Not accepted.
* This is the one original Review, executed directly in the qualified CLI
  session. No review worker, independent coordinator assessment, earlier Review
  or later closure verification is implied.
* The complete actual matrix passes, but the verifier trust-boundary defect
  RV-001 prevents accepting this candidate for publication. A passing final
  matrix receipt cannot override this adverse outcome.

## Requirements and Plan Comparison

| Boundary | Assessment and evidence |
| --- | --- |
| Research and accepted plan | Actual focused three-wave research precedes implementation. Current implementation acceptance matches live #413 read again during Review. Historical planning rationale remains distinguishable from dated execution. |
| P01-T01 command parity | Read the entire runner and focused tests, then the remaining 537-line source diff. Frozen workflow hashes and 98 per-step coverage rows preserve unique checks, with hosted-only operations explicitly separated. |
| P01-T02 actual execution | Run05 has 17 passing groups and 183 command rows. Receipt sidecar, every recorded file hash and source matrix/helper hashes were checked directly during Review. Expected missing-dependency/readiness probes are recorded nonzero probes, not failed required commands hidden as success. |
| Source isolation and resources | Candidate/snapshot cleanliness, detached exact-HEAD installs, external HOME/cache/data, loopback-only Python test connections, owned SQL proof, random ports, exact-ID cleanup and shared heavy lock are implemented. Snapshot input evidence is empty; no owned SQL container remains. |
| Receipt validity | Source/base/tool/evidence/group/image checks exist; focused tests exercise ordinary tampering. RV-001 shows an untested execution path before environment validation, so fail-closed verification is not established. |
| P02-T01 guidance | Three named guidance surfaces use the canonical command and require exact-head verification, independent assessment and invalidation after later changes. Obsolete mandatory mvp discovery and local-failure cloud fallback were removed. |
| P03-T01 retained coverage | Full dictionary equality preserves the hosted MSSQL job/selectors independently of disabled legacy workflows. SPDX, logo stress, compileall, migration, both JS checks, union guards, native actionlint and strict harness lint are retained. |
| P03-T02 triggers and boundaries | Source CI remains PR-update plus dispatch, without main-push repetition; legacy files are dispatch-only. Manual release, privileged Source CI workflow_run linkage and helper files have no diff. No remote setting/write/publication occurred. |
| Test budget and ownership | Exactly 12 focused methods; exactly two existing infra files extended; no behavioral assertion/test removal, domain edit or helper modification. |
| Original critique | Original Revise blob remains 4d314830793b4be909892692bac352c47b36cc7e. Parent PC-001/PC-002 dispositions are unchanged; no new critique ran. RV-001 is an implementation finding, not a rewritten critique. |

## Actual Validation Evidence

Run05 receipt: `/tmp/rpi-413-run05/receipt.json`, source
2c98c0e3fac0657bb67f093ac8f4561685c8c8d3, base
612cbed78a35a4ab426571aa7d2aeb0ae6d691dd. It was actually verified before the
final metadata edits; it is historical, not the eventual publication receipt.

| Suite | Total | Executed | Skipped |
| --- | --- | --- | --- |
| core | 1194 | 1045 | 149 |
| agents | 105 | 105 | 0 |
| api | 935 | 635 | 300 |
| orchestrator | 46 | 46 | 0 |
| importer | 39 | 39 | 0 |
| orchestration | 12 | 12 | 0 |
| infrastructure, REQUIRE_AZ_BICEP=1 | 359 | 359 | 0 |
| exact real MSSQL selectors | 243 | 242 | 1 |

Every skip ID/reason is retained in command rows/logs. General discovery
contains existing opt-in SQL/browser cases and backend non-applicability; it
does not assert that those integrations ran. The explicit SQL group's only
skip is the declared JSON-only separate-file audit-ordering method. Actual
Chromium design-system/workbench and 17 regulatory/verified axe states ran.

All four canonical images passed the unchanged helper; the separate external
logo0600 build also passed. All four fixable HIGH/CRITICAL gates have zero
findings. Each full report retains 61 HIGH and two CRITICAL unfixed package
findings; no vulnerability-free-image claim is made. SPDX-2.3 package counts
are API 130, agents 110, orchestrator 129 and importer 122. Actual DB freshness,
immutable image IDs and evidence hashes are in the receipt.

Adverse run01/run02/run03 receipts and the first browser probe remain
preserved, with their causes and actual corrective execution in the changes
record. They are not overwritten or described as passes.

## Findings

### RV-001 [High]: External receipt verification executes unvalidated environment code

* Related requirements: P01-T02, P02-T01; fail-closed tamper/identity handling
  and inert external receipt evidence.
* Evidence: tools/rpi-checks.py:149-164 invokes
  `OUT/venvs/PROJECT/bin/python -m pip freeze --all` before hashing startup
  `.pth` files. tools/rpi-checks.py:1062-1075 reaches that invocation before
  comparing environment identities and before validating command/file/group
  completeness. A plain SHA256 sidecar is integrity metadata, not provenance
  for executable files beside an externally supplied receipt.
* Actual bounded reproduction: an isolated disposable git fixture supplied
  correct current source/tool headers and a matching receipt SHA256 sidecar.
  A reviewer-authored benign replacement core environment executable wrote
  only a marker in that owned scratch directory. The verifier executed it,
  then rejected the incomplete fixture with FileNotFoundError. Observed
  `REVIEW_PROBE_UNTRUSTED_ENV_BINARY_EXECUTED_BEFORE_VALIDATION=True`.
* Probe evidence:
  `/tmp/rpi-413-evidence/original-review-verifier-probe.log` and
  `/tmp/rpi-413-local-validation.log`. The fixture was removed after the probe;
  no private file, credential, network endpoint or real dataset was accessed.
* Impact: a replaced environment executable or changed Python startup file
  can run code in the coordinator process's user context before rejection.
  Environment scrubbing does not make arbitrary local executable code inert.
  This is separate from extra-selector regex validation: receipt command
  arrays are not replayed, but executable receipt-adjacent input is trusted.
* Smallest resolving work: make verification data-only for external
  environments, using trusted code to inspect bounded metadata/startup/package
  identities without launching receipt-adjacent interpreters or importing
  their startup files. Add a regression inside the existing 12-method budget
  proving replacement binaries and `.pth` content cannot execute during
  verification; require a fresh full exact-head gate after correction.
* Severity/confidence: High, 10/10 for reproduced code execution.
* Destination: separately authorized RPI Implement follow-up using the
  existing accepted plan; do not fix or verify closure in this Review.
* Owner: coordinator assigns the qualified corrective CLI invocation.
* Status: Open, blocking publication and implementation acceptance.

## Implementation Adjustments and Follow-Ups

The exact JSON-only SQL non-applicability and external browser scratch/bytecode
policy are evidence-backed implementation adjustments, not permission to skip
required integration checks. The helper/harness assertions remain unchanged.
No change requires a new design decision or repeated original critique.

| Item | Disposition, owner and next action |
| --- | --- |
| RV-001 | Blocking; coordinator routes a distinct corrective Implement invocation, preserving this original adverse Review. No source change or second Review is performed here. |
| Independent exact-head assessment and 403 required-context mapping | Coordinator/owner, before any authorized publication/merge. No hosted or protection acceptance is inferred. |
| Retained hosted checks | Coordinator/owner after explicit publication authorization; unavailable in this no-push invocation. |
| Cache/pin or changed-scope optimization | Deferred by accepted plan; owner selects later only after the complete gate is trustworthy. Full mode remains mandatory. |
| Artifact retention cleanup | Deferred; owner first authorizes evidence-preservation review. No cleanup of historical adverse evidence. |
| Managed workflow billing audit | Deferred; owner requests read-only billing evidence rather than estimating account charges from job durations. |

## Limitations and Routing

This is local original RPI Review, not a security certification, fresh-context
HVE behavior acceptance, independent coordinator assessment or proof of
GitHub/Azure/OIDC/reviewer/deployment controls. No such execution is claimed.
Required human checks remain uncompleted. Existing unfixed vulnerability
reports remain visible, not silently waived.

The final artifact commit and subsequent full matrix have not happened at
Review close. They may create a complete exact-head receipt, but cannot close
RV-001 or change this verdict. Preserve this record unchanged as the original
adverse Review; the parent may reconcile handoff metadata and freeze the
requested local candidate without claiming delivery acceptance.

| [.copilot-tracking/research/2026-10-18/local-rpi-validation-research.md](.copilot-tracking/research/2026-10-18/local-rpi-validation-research.md) | Actual focused research |
| [.copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md](.copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md) | Accepted full plan |
| [.copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md](.copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md) | Command and safety details |
| [.copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md) | Unchanged original critique |
| [.copilot-tracking/changes/2026-10-18/local-rpi-validation-changes.md](.copilot-tracking/changes/2026-10-18/local-rpi-validation-changes.md) | Actual implementation/execution history |
| [.copilot-tracking/reviews/logs/2026-10-18/local-rpi-validation-review.md](.copilot-tracking/reviews/logs/2026-10-18/local-rpi-validation-review.md) | Complete original Review, Not accepted |

## Next Steps

Parent: commit the dated evidence and this adverse Review, then perform the
requested final exact-head full matrix and external receipt handoff without
publication or source fixes. Coordinator: assess the frozen candidate and
route RV-001 to a separately authorized corrective `/rpi-implement` invocation.
Do not authorize push while RV-001 remains open. This original Review is not
repeated, overwritten or reported as conformant.
