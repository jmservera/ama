---
title: Existing-resource preservation execution record
description: Actual no-write blocked disposition for issue 358
ms.date: 2026-10-19
---

## Task and Scope

Task ID issue-358-live-preservation; slug live-keyvault-preservation-358.
Full plan scope P01, all three tasks, dated2026-10-19.
Branch test/live-keyvault-preservation-358.
Starting HEAD/base7f96d9957b28cb174aa759c842376f24087d71a3.
Original independent critique Complete/Pass for no-write disposition only,
zero findings. No source change or live mutation is authorized by that verdict.

## Execution State

Implementation started after original critique. P01-T01 complete:
final same-target read-only metadata comparison and owned bytecode cleanup.
P01-T02/P01-T03 complete. Full P01 no-write implementation disposition complete;
original independent Review pending. AC1 remains Blocked / Not run.

## Research Operations Actually Executed

Read complete issue358 body/comments and merged374; source and current guides.
CLI account read establishes servicePrincipal, not tenant authority.
CLI app show/list and auth metadata projections, then actual production
Azure.rest GET at API_VERSION2025-07-01 for all3 exact existing apps.
App-scope permission metadata reads show read/write/listSecrets action
allowed, not provider/policy success. First local standalone projection
failed on null initContainers and was corrected before production-boundary
read; no mutation or result fabrication. Agents auth GET failed kind=request.
Actual production require_demo read-only probe refuses malformed/unknown
deployment template/parameters; no roster/private data inspected.

External directory /tmp/issue-358-live-preservation-20261019-1416 (0700):
research-management-summary.json and profile-summary.json (0600).
Only sanitized summaries; no raw payload/token/secret/private roster saved.

## Operations Not Executed

No preserve_app_secrets live inventory call, listSecrets, secret_reference
mutation, password creation, Graph, SQL, browser authentication, image
publication, PATCH, deployment, restart, traffic/identity change, sentinel
secret/binding creation, clone or other resource allocation. No hand-written
proxy payload is claimed. No KV value read or backing-service write.

## Source and Validation Boundary

No actual narrow defect found. Production helper/tests/#374 behavior unchanged.
No new offline tests, mutation suite or dependency install. Required validation
for this evidence-only blocked disposition: final metadata, Markdown links,
diff whitespace and historical/source/memory preservation.
No full heavy gate: explicitly excluded by owner for no-change blocked result.
No frozen review-ready publication candidate or authoritative receipt exists.
All evidence remains local pending coordinator handoff; no push/PR/merge,
manual status, issue/board/settings update or history rewrite.

## Rollback and Cleanup

Cloud inventory empty: no resources, tags, locks, credentials or bindings
created/changed by this run, so no rollback or cloud deletion needed.
Four14:19:01 run-owned bytecode files were inspected and individually removed:
staff_azure.cpython-312.pyc, credential_arm.cpython-312.pyc,
setup-entra.cpython-312.pyc and staff_roster.cpython-312.pyc. Empty cache
directory removed; final git ignored-status for infra/scripts empty.
No mutation payload/secret backup file exists. Sanitized0600 summaries retained.

## P01-T01 Final Metadata

At2026-10-19T14:24:58.576195Z, unchanged production Azure.rest GET re-read all3
exact apps. All compared null-presence/count/revision/ready/lock/handoff fields
match initial research. KV/reference and env/scale/registry counts remain0.
No comparison of plaintext values was attempted or necessary.
External final-management-summary.json is0600; stat confirms directory0700
and all3 summary files0600. No task-owned cloud state exists to roll back.

## P01-T02 Durable Evidence and Validation

Added dated current observations and explicit limits to infra/README.md,
docs/architecture/cutover-evidence-pack.md and docs/reference/README.md;
appended docs/reference/log.md. No production documentation links to tracking.
2026-10-19T14:26:44Z evidence validation passed: expected4 tracked Markdown
changes only, six dated section links resolve, diff whitespace clear, state
JSON parses. Original log exact byte prefix; source/setup tests/legacy CLI/
both case studies/memory and all7 original358 artifacts byte-identical to base.
External evidence-validation.json0600 retains exact paths/check results.
No behavioral tests claimed; no source or runtime changed.

## P01-T03 Reconciliation and Review Handoff

All current P01/task markers and plan/details/changes are synchronized.
No material divergence from critiqued no-write plan. Original critique retained
unchanged; AC1 is not checked or converted to acceptance. Ready only for one
independent original Review of actual blocked disposition, not publication.
Current HEAD remains supplied base;4 modified Markdown files and6 current RPI
files are local evidence (Review file will be the7th current artifact).
No commit requested/performed for a review-ready candidate because none exists;
no gate/receipt/publication is claimed. Do not mistake local persistence for
clean frozen commit or independently assessed head.

## Remaining Work and Follow-Up

One original independent Review remains. Actual live criterion needs a genuinely populated
already-authorized eligible target, or separately scoped state preparation.
Profile-evidence repair belongs to future guarded roster setup, not permission
to invent a populated inventory or bypass the existing guard.

## Supplemental Scope Opening (2026-10-19)

Owner explicitly selects SAME-task autonomous continuation with an isolated
synthetic baseline, not existing-app modification. Original P01/no-write history
above remains true for its execution window. Supplemental research cycle2 is
complete; amended plan/details P02-P04 exist before resource writes.
Original Review SHA256:
5fb39b9ef7b3aac4cbef810019eb1db23d6890b3c74d0baaf98059c75f9df41b.
Original critique SHA256:
c4e1e226080ba9210ee0b7daac32d34e61bb50533874203b4415ffa805aea121.
Both remain immutable; no second original critique or Review is authorized.
External inventory/research/11-workload baseline snapshots are0600 under
/tmp/issue-358-synthetic-20261019-1450, directory0700. All initial five IDs absent.
No cloud writes yet. New bounded lifecycle safety assessment pending.

P02-T01 complete: one independent supplemental safety assessment inspected
actual primary metadata and source. Verdict Suitable to proceed with limits;
all F1-F5 clarifications applied directly before writes (standalone secure
deployment, distinct vault/ARM token audiences, provider-tested pre-existence
scope, cleanup-over-deadline priority/recovery inventory, top-level hash bounds).
Original critique and Review remain unchanged. Implementation may now attempt
only the bounded conditional P02 private cleanup-route preflight.

### P02 Operator Corrections and Safe Retry Boundary

Initial local absence check hit production AzureError's generic classification
for RoleAssignmentNotFound; exact diagnostic confirmed absence, no writes.
Next owned-job start included provider-returned volumes, which StartJobExecutionTemplate
rejects with HTTP400 ("Unknown properties volumes ... not supported").
Corrected only external operator body to containers. No source/helper defect.
One actual private preflight execution then failed; its local log-framing parser
also failed, so its cause is not inferred. All exact task-owned jobs, roles and
identities were deleted after each attempt; no secret/deployment/app was created.
At15:00:52Z all11 workload snapshots, RG membership and backing hashes match.
An exact-owned-execution Log Analytics query was denied InsufficientAccessError;
this is a concrete diagnostics permission result, not a vault-route diagnosis.
Permit one diagnostic preflight retry with direct owned console capture0600 and
corrected parser, within the same scoped resources/lifetime. No vault secret
will be allocated unless the actual private metadata preflight passes.

At15:04:01Z the diagnostic execution established an actual HTTP200 versions
response from inside the private environment, not a network/permission barrier.
The external worker had incorrectly treated all200 responses as pre-existing
state. Correct its absence test to require200 with an exact empty value array
and no continuation (or404 SecretNotFound), plus deleted-name404. Nonempty or
ambiguous responses still abort. This is an operator-script/schema correction,
not a production helper defect or acceptance relaxation. All four temporary
allocations again verified absent; original11 workloads/backing/RG unchanged.

## P02/P03 Actual Successful Supplemental Execution

At15:04:42Z the corrected owned lifecycle began; private synthetic-only preflight
Succeeded15:05:53Z with actual versions200 empty/no continuation and deleted404.
Dedicated temporary identity/secret-scoped Officer/registry AcrPull were
provider-accepted; no tenant/subscription/existing-identity change.
Exact one-Create secureString what-if preceded native deployment; actual secret
metadata verified versioned URI, enabled, expiry and owner. No real secret read.

New app baseline Succeeded15:06:41Z before fresh actual GET/listSecrets.
Unchanged infra/scripts/setup-entra.py preserve_app_secrets reconciled real
inventories; unchanged Azure.rest PATCHed only properties.configuration
at15:06:42Z. Actual readback observed InProgress through15:07:04Z, then
Succeeded15:07:07Z; fresh GET/listSecrets at15:07:08Z passed exact:
KV URL/identity pair, unrelated random value, full configuration, template/
unused secretRef binding, MI, tags, latest/ready revision and resolved synthetic
KV value against the known random input. All eight comparisons true.
Hashes remain only in external0600 private-comparison-hashes.json.
No Graph/password/secret_reference/full-setup or existing-app write occurred.

The app used the existing private digest with a harmless Python sleep command,
no ingress/rules, min0/max1,0.25CPU/0.5GiB. One actual replica was observed;
this is explicitly not a zero-runtime/zero-cost claim. Across all attempts,
two earlier failed private preflight executions plus successful preflight and
cleanup were bounded by120sec/retries0. No premium resource/new environment/
vault/network/image publication. Successful lifecycle elapsed267.405319seconds;
incremental charges are not yet settled or claimed zero.

## P03-T02 Exact Cleanup and Unchanged Existing Resources

App deleted before vault cleanup. New owned cleanup job Succeeded15:08:20Z:
only exact owner/run-tagged single-version synthetic secret deleted/purged;
active versions empty and deleted secret404 verified without value GET.
Owned deployment history, job/executions, exact role pair and MI removed.
Final15:09:10Z confirms all seven inventory entries absent, zero cleanup
failures and original11 workload snapshots/RG resource membership/top-level
environment/vault/registry hashes exact. Earlier failed allocations were also
fully cleaned; subsequent exact probes verify all ten historical role IDs
RoleAssignmentNotFound. No RG deletion or existing workload restoration.
External source/owner/lifetime/inventory/journal/primary records remain0600
under0700 directory; no raw value/token/credential is retained in evidence.

## P04-T01 Primary Evidence Access and Scope Reconciliation

Generated primary summary:
.copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json.
Includes actual original sanitized metadata, helper/source identity, real
async transitions, eight named comparisons, provider/worker outcomes, exact
synthetic cleanup names/counts, limitations and external operator-source hashes.
No tenant/private IDs, values or private value-comparison hashes. Coordinator
can directly inspect this file in the worktree; no invented independent
verification or replacement Review is claimed. Original hashes still match.
Updated existing infra/evidence/index and append-only log, no new KB page.
No source/test changes or helper bug, so no unnecessary regression/refactor.

S-AC1-S-AC4 complete for the actual temporary synthetic component scope.
The baseline was real and established before preservation, but was created
for this exercise, not an originally populated deployed app. Original Review
remains Partial / Residual, RV-002/profile remains open, and original AC1/
issue closure requires coordinator judgement. No issue/status/settings change.

## P04-T02 Frozen Candidate Handoff

Pre-freeze evidence is ready for gh-derived local noreply author AND committer,
Conventional Commit and Copilot trailer. Full --all17-group local gate must
run on the subsequent clean frozen HEAD/base with the fixed shared heavy lock,
credential-scrubbed environment and preserved Node PATH, no uv. Receipt path:
/tmp/issue358-rpi-final-20261019-1520/receipt.json.
Post-freeze actual completion state:
/tmp/issue-358-synthetic-20261019-1450/final-state.json.
These external records avoid changing HEAD after validation; this committed
snapshot truthfully leaves the gate pending. No push/PR before coordinator
independent exact-head review/receipt; no repeat original Review or merge.

Pre-freeze validation complete: all eight actual comparisons pass, primary
summary contains no resource IDs/tenant GUIDs, original critique/Review hashes
match,533 source/test/history/memory/case-study files are byte-identical to base,
old log is an exact byte prefix,15 preservation links resolve, JSON parses and
git diff whitespace is clear. No ignored/untracked scratch is retained in the
candidate. Existing installed gate tools were located after PATH probes found
them missing: /tmp/rpi-413-tools contains verified Bicep0.48.1, actionlint1.7.7,
ShellCheck0.9.0 and Trivy0.76.0. The gate appends that directory to the existing
PATH, retaining Node24.21.0 at its existing NVM path; no package install or uv.
