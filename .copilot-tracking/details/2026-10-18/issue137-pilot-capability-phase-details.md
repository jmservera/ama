<!-- markdownlint-disable-file -->
# RPI Phase Details: issue137-pilot-capability

Task ID 137; 2026-10-18. Plan:
.copilot-tracking/plans/2026-10-18/issue137-pilot-capability-plan.md.
Research: .copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Publish exact bounded evidence | Completed; README table/legend, dated ADR delta and index/log |
| P02 | Reproduce and validate documentation | Completed; 2026-10-19 identical GET reproduction and both-base byte comparison |
| P03 | Preserve original Review and deliver | In progress; commit/rebase then original Review, final commit and external full gate |

<!-- rpi:phase id=P01 -->
## P01: Publish bounded evidence

Context: W1 contradicts current README supersession, not the correctly dated
historical ADR snapshot. R1-R17 contain narrow capabilities and missing quotas.
Boundary: documentation only. Dependency: final critique disposition.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reconcile prose and add dated evidence

Replace the unsupported 2026-10-16 supersession in Environments and its later
repetition. Change current pipeline status from region/ownership unverified
to selected owner/region but unverified service/account/approval evidence.
Add a 2026-10-18 current-status delta adjacent to later ADR evidence. Separate
2026-10-15 decision date from 2026-10-18 retrieval. Leave the historical
2026-10-08/09 table, ADR proposals and deployment receipts intact (PC-002).
Explain rather than edit the prohibited parameter example's stale comment.
Insert dated table with request, command IDs, returned values/units, scope and
Pass/Unknown/Blocked limitations; explicit management GET command legend.
Distinguish GlobalStandard inference usageNames from same-SKU fine-tuning
entries; no maxCapacity interpretation or unit conversion without returned
evidence. Update reference routing/log because durable guidance changes.
Completion: coherent prose/table with no template/example diff.

<!-- rpi:phase id=P02 -->
## P02: Reproduce and validate

Context: first observations are dated research, not guaranteed stable quota.
Boundary: identical GET surfaces only, same account binding privately checked.
Dependency: P01.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Repeat queries and verify evidence

Archive first-run private receipts, rerun identical bounded commands with
installation disabled, compare allowlisted fields and sanitized failures.
Never expose account IDs or raw responses; inspect staged content for UUIDs,
resource paths, private names/IPs, emails and secret fields. Source SHA-256
hashes for main/example/service modules must match Research/base.
Verify added relative links and git diff --check; inspect only task diff.
Record exact execution results, discrepancies and unresolved gaps. Reproduction
is dated 2026-10-19, not backdated; preserve 2026-10-18 adverse evidence.
Verify exact configuration bytes against approved main fa659cfd021100f7c64f8ec73bbff76c03adf234.
The 2026-10-19 owner direction supersedes the old doc-only testing exemption:
the canonical full local matrix is mandatory after final commit.
Completion: changes record links every phase/task to concrete evidence.

<!-- rpi:phase id=P03 -->
## P03: Original Review and delivery

Context: user requires exactly one original Review, not closure by self-review.
Boundary: no post-Review correction or second original Review.
Dependency: P02 evidence and consistent plan/details/changes.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute one Review, preserve and deliver

Activate rpi-review once, assess actual final content and evidence, preserve
its original verdict/findings. Leave human acceptance unchecked. Route gaps
to coordinator. Resolve gh account privately, configure repository-local
noreply email, include required Copilot trailer. Explicitly stage docs and
all six RPI artifact categories/state; no private scratch. First commit the
coherent preserved batch, then perform the owner-authorized clean rebase of this
unpublished run-owned branch onto fa659cfd021100f7c64f8ec73bbff76c03adf234,
stopping on ambiguous conflicts. Complete Review against reconciled source,
then commit all final artifacts. No push/PR is authorized.
Run and verify the canonical full local gate at that final commit with
PATH=/tmp/rpi-413-tools:$PATH, a new external output directory, shared heavy
lock, isolated owned SQL/containers/cache/data and no inherited real cloud/model
credentials for test children. No commits after the gate.
Completion: exact HEAD/base/merge-base, clean status, actual matrix/receipt and
artifact inventory reported externally. Coordinator owns independent exact-head
review, literal remaining criterion assessment and later publication.

PC-001 final privacy gate: after original Review generation and explicit staging,
inventory all staged paths, inspect complete staged additions and full contents
of new artifacts, including Review/state/changes, with no outgoing PR authorized.
Check identifiers/private names/IPs, account inventory and secret fields against
the allowlist. Public handles, source hashes and required noreply attribution
are allowed. Any later staged-content change requires rerunning this gate.
Failure stops commit/push and routes to coordinator without modifying the
original Review or launching another Review.
