---
title: Existing-resource preservation disposition plan
description: Original bounded plan for issue 358 after current ARM investigation
ms.date: 2026-10-19
---

## Task Metadata

Task ID: issue-358-live-preservation.
Slug: live-keyvault-preservation-358.
Branch: test/live-keyvault-preservation-358.
Base: 7f96d9957b28cb174aa759c842376f24087d71a3.
Research: .copilot-tracking/research/2026-10-19/live-keyvault-preservation-358-research.md.
Details: .copilot-tracking/details/2026-10-19/live-keyvault-preservation-358-phase-details.md.

## Executive Summary

Current supplemental scope: owner-selected isolated synthetic baseline in the
existing internal private Consumption environment. P01 below remains historical.
P02-P04 add a preflighted cleanup route, real synthetic baseline and production
preservation roundtrip, then exact cleanup and frozen unpublished candidate.
Original critique/Review and their adverse limits remain unchanged. Conditional
implementation readiness depends on the new bounded lifecycle assessment below.

Record the actual no-write blocker rather than execute an empty, meaningless
secret rebuild. All three existing ama Container Apps have explicit null
secret inventories and zero KV pairs or environment secretRef bindings in
real ARM2025-07-01 GET. The remaining criterion needs actual pre-existing
references alongside unrelated secrets and bindings, so it is UNMET / Not run.
No source defect has been demonstrated and no source/test change is planned.

### What You May Not Know

The production reconciliation helper and configuration PATCH are ARM-only;
image publication and Graph are not intrinsic requirements for an identical
secret-list round-trip. Full secret_reference mutation does create a Graph
password, and full setup can alter runtime and restart; neither should run
for this check. Current app-scope permissions metadata includes write and
listSecrets/action, but no provider write was attempted. The demo's actual
require_demo guard also refuses unknown/malformed deployment evidence.
That is separate roster-profile evidence, not proof of production profile.

## Sources

Research C1-C5/W1-W5; complete live issue358/comments and merged PR374.
Primary sanitized records:
/tmp/issue-358-live-preservation-20261019-1416/research-management-summary.json
and profile-summary.json. Both mode0600 in directory0700.

## User Decisions and Requirements

* Run Research, original critiqued Plan, Implement and original Review in order.
* Use existing ama resources only; never delete RG, weaken private backing,
  rotate credentials or mutate identity/traffic/restarts merely for testing.
* Prove literal actual existing-resource preservation with real production
  helper/payload, or stop with concrete evidence; no mock-only substitute.
* Do not repeat delivered offline expiry/preservation tests absent a defect.
* Preserve all earlier issue evidence, original adverse reviews, log and memory.
* No heavy gate for a no-change blocked result. Any review-ready changed
  candidate instead requires a frozen clean commit/full17-group external gate
  before coordinator exact-head assessment; no publication in this task.

## Goals

Correct the overbroad prerequisite assumption while retaining the literal
criterion and all platform/application safety boundaries. Preserve an auditable
blocked disposition and minimum next condition.

## Scope and Non-Goals

Only dated RPI evidence plus existing infra runbook, cutover evidence pack,
KB index and append-only log. No application/helper/test/Bicep/workflow change.
No cloud mutation, listSecrets/plaintext read, Graph, SQL, image, browser
authentication, new secrets, bindings or clone.

## Functional Requirements

FR1: Record exact current three-app counts/API version and probe limitations.
FR2: Distinguish production reconciliation/ARM payload from full setup.
FR3: Preserve original historical evidence and current missing-profile outcome.
FR4: Record rollback/cleanup and next condition, not invented live success.

## Non-Functional Requirements

No IDs, tokens, credentials, private roster or raw payload in evidence.
Only sanitized external0700/0600 operator files. No Python bytecode artifacts
left by this run. No issue/board/settings/status/merge/push/PR actions.
One critique and one original Review; no retry review to relabel the outcome.

## Acceptance Criteria

AC1 (literal live criterion): preserve actual existing KV URL/identity pairs,
unrelated secrets and app secretRef bindings through a real helper/payload
round-trip. **Blocked / Not run**: no populated target. Never mark complete.
AC2 (bounded disposition): durable exact blocker and independent critique
complete; original Review pending. No cloud/source changes or stronger
readiness claim.
AC3 (safety): no secret-value read, resource allocation, mutation or cleanup
deletion; initial and final sanitized app inventories consistent.
AC4 (history): all earlier issue358/RPI evidence, log entries and memory unchanged.

## Intended Operation and Rollback

Authorized operation for this candidate: **none**. Do not issue even an
identical empty configuration PATCH: it cannot prove AC1. No mutation request
body, backup secret file, lock tag or rollback write is needed.

For a later genuinely populated target only: fresh nonproduction/profile and
coordination evidence, exact private in-memory inventory/listSecrets,
production preserve_app_secrets plus existing-configuration-only Azure.rest
PATCH, no template/identity/runtime/auth changes, explicit reference/value
and revision/traffic comparison. This would test that component boundary,
not full secret_reference credential creation/setup. Future actual payload
and independent plan/critique must be based on that resource's metadata.
If preflight finds versionless KV refresh/restart risk, unresolved concurrency,
or required template/binding changes, stop before write. No automatic retry,
restart, new credential or policy bypass as recovery.

Rollback for this run: none, because zero writes. If external concurrent
changes appear at final read, report them, do not restore someone else's state.
Remove only bytecode files attributable to this run, retain sanitized external
read summaries0600; no raw/secret files to erase and no cloud cleanup inventory.

## Test Ownership and Candidate Lock

Canonical source/test owner: existing infra setup suite, unchanged.
Test removals: none. Maximum test additions:0. Generated production targets:none.
No behavioral or regression test is warranted for an evidence-only blocked
result; do not rerun offline preservation as a proxy for AC1. Validate the
changed Markdown/link destinations/diff and final actual management metadata.
No review-ready implementation candidate is proposed; do not start the heavy
gate for this blocked no-source/no-cloud-change disposition. Keep the blocked
record local for coordinator handoff; publication remains prohibited.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve the concrete blocker and safety inventory

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Final read-only invariant and cleanup check

Read current exact app ARM metadata again; record only sanitized counts,
revision/ready state, lock/handoff presence and no-mutation status.
Check no task-owned cloud resources/tags/files exist; do not delete existing
resources. Preserve observed profile failure as such.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update existing durable evidence

Add a clearly dated delta in infra/README.md and cutover-evidence-pack.md;
update KB index and append log without rewriting earlier outcomes.
Cross-link normal docs only, no tracking paths in production documentation.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Reconcile original RPI evidence and handoff

Create dated changes record and reconcile markers/state before one original
Review. Report AC1 Blocked, no-source/no-cloud-change result and absence of
full-gate receipt. Do not invent a frozen review-ready candidate.

## Critique Disposition

Original independent critique executed2026-10-19; execution Complete, verdict
Pass solely for no-write disposition; zero findings, no PC correction required.
Artifact:
.copilot-tracking/reviews/plans/2026-10-19/live-keyvault-preservation-358-plan-critique.md.
Original content is retained unchanged. This Pass does not pass AC1 or permit
a cloud mutation. No second critique will run.

## Follow-Up Items

* Identify a genuinely populated already-authorized eligible existing target
  or separately scope/approve representative-state preparation. This is later
  work because creating state would change the same-configuration task.
* Resolve actual resource-bound demo profile evidence before automatic roster
  generation. This is not an ARM-preservation permission surrogate.

## Handoff

P01 no-write evidence disposition complete; all tasks checked against actual
evidence. Ready for the one original Review of that disposition, never AC1
execution or publication. Source remains unchanged; four existing Markdown
files plus this task's new RPI files are local/uncommitted. No full gate/receipt
or frozen candidate exists. Changes record:
.copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-changes.md.

## Supplemental User Decisions and Requirements (2026-10-19)

* Continue SAME task autonomously; retain inherited work and original hashes.
* Establish a real nonproduction temporary baseline, not a mock PATCH or
  modification of the existing running apps. No deletion of ama.
* No ingress/traffic, min0, max1; no existing template/identity/network changes.
* No real secret read, Graph password creation, registration, private data,
  publication, policy/public-access bypass or subscription/tenant grant.
* Use only exact absent task-owned RG resources; external0600 inventory records
  owner/source/lifetime. Delete owned objects on success or failure.
* Real preserve_app_secrets and Azure.rest PATCH, private comparison hashes and
  actual terminal readback; fix source only if this demonstrates a helper bug.
* Provide sanitized primary evidence IN WORKTREE; freeze clean commit using
  gh-derived local noreply author/committer and required trailer. Full actual
  17-group gate with credential scrub/fixed heavy lock and unchanged Node PATH;
  receipt external. No push/PR before coordinator independent exact-head review.

## Supplemental Goals, Scope and Requirements

S-FR1: prove private cleanup connectivity before any synthetic vault allocation.
Use one new task-owned manual job, never a start override or exec on an existing
job/app. Dedicated temporary MI receives Secrets Officer only at the new
synthetic secret scope and AcrPull only at the existing private registry.
Officer includes reference read but is required for exact-secret deletion.
No existing identity changes. Job code permits only synthetic versions/deleted
metadata and exact-secret DELETE/purge, never a GET of secret value/list vault.

S-FR2: create one synthetic KV secret through incremental secureString ARM
deployment, no output/value logs; tag source/owner/expiry, enable expiry. Capture
its actual versioned URI from ARM metadata. Existing vault privacy unchanged.
Only then create new app containing that reference/MI pair and one unrelated
random local secret. Optional unused env secretRef points ONLY to that local
synthetic secret on the new app. Pin the already deployed private API digest;
override command to a benign bounded idle command if the platform starts it.
Never privileged; no custom image, package installation or default app startup.

S-FR3: wait for baseline Succeeded; GET/listSecrets only the owned app, validate
the two synthetic entries, valid reference and exact local value. Record private
hashes externally. Freshly call unchanged production preserve_app_secrets, merge
its output with actual current configuration as production does, and issue
Azure.rest PATCH of properties.configuration only. No secret_reference call.
Poll terminal state, then GET/listSecrets again. Compare exact named pair,
local value, optional binding and all unrelated fields; report differences,
never silently normalize an observed difference into success.

S-FR4: cleanup owned app first; delete/purge only the exact synthetic secret
through the new private cleanup job. Verify active/deleted secret absent using
metadata-only calls, delete secure deployment history, job/executions, exact
new role assignments and MI; poll404/empty lists. Re-read all11 existing workloads,
their active revisions/readiness and backing configuration; compare RG inventory.
Never delete an existing object or restore concurrent external changes.

S-NFR: inventory before writes, atomic intent/result journal, paths0700/0600,
no values/tokens in argv/logs/evidence. Maximum lifetime16:00Z on2026-10-19;
job timeout120/retries0, parallelism1, completion1,0.25CPU/0.5GiB.
At most preflight plus cleanup executions, with one bounded cleanup retry only
for confirmed transient failure; each elapsed execution and app replica count
recorded. No new environment/network/vault/premium service. Charges accrue
for any actual replicas/operations; do not claim a settled zero bill from
scale settings or delayed cost reporting. If cleanup fails retain inventory
and precise unresolved IDs externally, fail the task rather than hide them.

## Supplemental Acceptance Criteria

S-AC1: successful real pre-existing-at-PATCH synthetic baseline with valid KV
pair and unrelated synthetic value; exact reference/value/binding preservation
through production helper and real ARM PATCH. If resolved KV value is unavailable
from listSecrets, explicitly state the provider validation limit.
S-AC2: terminal readback matches configuration, template, identity, tags,
revision/ready state and bindings; no unreported unintended differences.
S-AC3: exact owned resource/role/deployment/active/deleted-secret cleanup proven;
all11 existing workload hashes/readiness/active revisions and RG membership stable.
S-AC4: sanitized independently readable in-worktree primary summary, original
critique/Review hashes unchanged, existing durable docs/index/log reconciled.
S-AC5: clean frozen candidate, full17-group gate and externally verified receipt,
no publication. Synthetic evidence is not full secret_reference, Graph,
deployed-app token-store, runtime usability or whole-demo acceptance.

## Supplemental Phase Checklist

<!-- rpi:phase id=P02 -->
### [x] P02: Establish bounded private lifecycle prerequisites

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Independently assess new lifecycle material before writes

Research cycle2, exact private inventory and original hashes are available.
One bounded independent assessment writes only the new supplemental safety
assessment. Preserve original critique; resolve compatible findings directly.
Completed: independent assessment Suitable to proceed with limits; F1-F5
clarifications applied below. Original critique/Review remain byte-identical.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Preflight task-owned identity/roles/private cleanup job

Fresh absent-ID checks include UUID role assignments before any allocation.
Inventory includes exact IDs/version/source/owner/expiry and every mutation
intent. Snapshot all existing workloads and selected backing resources.
Create MI, secret-scoped Officer, registry-scoped AcrPull and new manual job.
Run only exact-synthetic metadata preflight from the internal private environment.
Absence requires404 SecretNotFound or200 exact empty versions/no continuation,
plus deleted-name404; a successful empty list is not an existing secret.
If image pull/network/authorization fails, capture exact safe error and clean
owned allocations; never create a dangling reference or orphan vault secret.

<!-- rpi:phase id=P03 -->
### [x] P03: Execute synthetic baseline preservation and cleanup

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Establish baseline and exercise production preservation

Depends on successful P02. Secure incremental deployment creates only new
synthetic secret; what-if must prove exactly that Create. Verify versioned URI
and attributes. Create no-ingress app, wait, privately validate baseline,
call actual helper/PATCH, wait, compare named exact fields and hashes.
On any provider failure skip acceptance, retain exact sanitized diagnosis.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Prove owned cleanup and existing workload invariants

Always run finally, even if setup/PATCH fails. Never broadly delete by prefix.
Only inventory-listed IDs with matching ownership and initial absence qualify.
No secret write unless metadata preflight proves the new cleanup route usable.
Cleanup job accepts fixed synthetic name and fails on any other target.
Reconcile resource counts, role IDs, deployment history and unchanged existing
workload/backing hashes; retain unresolved cleanup as blocker, not success.

<!-- rpi:phase id=P04 -->
### [ ] P04: Preserve supplemental execution and freeze unpublished candidate

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Reconcile evidence and durable documents

Append actual supplemental outcome to research/details/changes; leave original
critique and original Partial/Residual Review byte-identical. Place sanitized
primary JSON in-worktree, no tenant/private IDs/values/comparison hashes.
Update existing infra/evidence/index and append-only log. Remaining original
acceptance/profile criteria remain explicit.

<!-- rpi:task id=P04-T02 -->
#### [ ] P04-T02: Commit and execute full external-receipt gate

Read gh user id/login for repository-local noreply author AND committer.
Conventional Commit plus Copilot trailer; commit inherited and supplemental
same-task evidence only. Fetch main, retain supplied base unless current base
movement blocks requested exact-base validation. Run full --all17 groups on
frozen clean HEAD/base, fixed /tmp/ama-rpi-heavy.lock, external output, scrubbed
credential environment without replacing existing Node PATH; no uv.
Verify receipt on exact HEAD/current origin main; no later commit/dirty inputs.
Gate failure remains actual failure; no cloud fallback or skip/false receipt.
Leave coordinator exact-head assessment as next action; do not push or open PR.

## Supplemental Test Ownership and Safety Assessment

Production helper/source unchanged unless an actual demonstrated defect emerges.
Existing infra setup tests own any tightly scoped regression: removals none,
maximum additions one targeted case if necessary, no offline acceptance proxy.
Operator scripts stay external, fixed and explicit, not shipped abstractions.
Real-provider preservation comparisons are the semantic test. Documentation
links/diff/history checks and full gate own the frozen candidate's regression
validation. Original critique is immutable; new lifecycle assessment is pending
at .copilot-tracking/reviews/plans/2026-10-19/live-keyvault-preservation-358-synthetic-safety.md.

## Supplemental Safety Assessment Disposition

One independent bounded NEW-material assessment executed, suitable with limits.
F1: synthetic secure deployment is standalone external operator code; production
credential_arm.py remains read-only and its naming guard is never relaxed.
F2: worker requests only vault data-plane audience https://vault.azure.net;
production Azure CLI/ARM transport owns separate management-plane authorization.
No token is logged or passed in argv.
F3: individual-secret scoping is documented by S-W7; pre-existence acceptance
remains an actual provider/preflight condition, not a success inferred from the
assessor's uncited confirmation. Exact role PUT/readback and metadata probe
will decide it; any refusal aborts safely.
F4: stop starting new allocations by15:45Z and start cleanup immediately on
failure/success.16:00Z is target maximum lifetime, never a reason to interrupt
cleanup; any overrun is explicitly reported. External inventory supports exact
recovery after interruption, no autonomous broad sweep.
F5: backing hashes cover top-level ARM resource metadata/properties only, never
child-secret enumeration. Child secret/job/role cleanup is verified separately.
No second assessment or original critique/Review rewrite is performed.

## Supplemental Execution and Frozen Validation Boundary

P02/P03 and P04-T01 complete. Actual successful lifecycle15:04:42-15:09:10Z.
Native secret deployment Succeeded15:06:21Z; real app baseline Succeeded
15:06:41Z; actual production PATCH15:06:42Z observed InProgress through15:07:04Z
then Succeeded15:07:07Z. All eight exact comparisons passed, including actual
resolved synthetic KV value and unrelated random value. One replica existed
at readback despite min0. No source defect or source/test changes.
All seven inventory entries absent (secret active/deleted verified privately);
all ten role UUIDs across failed/cleaned operator incarnations also absent.
All11 old workloads, RG membership and selected top-level backing hashes match.
Operator/schema/parser corrections and their failed outcomes remain in changes
and primary summary; no provider failure was relabeled as a passing attempt.

In-worktree primary:
.copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json.
It includes sanitized primary observations from both original no-write and
later real execution, source identity/method boundary, actual async state
transitions, comparisons and cleanup. Secret values/IDs/comparison hashes stay
external0600. This improves review access, not original Review execution.

S-AC1-S-AC4 passed for the explicitly synthetic component scope. Original AC1
is not closed or rewritten: originally populated deployed-app/token-store/full
setup acceptance remains a coordinator judgement. RV-002 profile uncertainty
remains outside this scope. Original Review remains Partial / Residual.

P04-T02 is deliberately pending in this frozen source record: its full gate
must run AFTER the candidate commit and cannot be committed into that same HEAD.
Authoritative receipt: /tmp/issue358-rpi-final-20261019-1520/receipt.json.
Post-freeze state: /tmp/issue-358-synthetic-20261019-1450/final-state.json.
The external final state/receipt records actual gate completion without dirtying
or silently invalidating the candidate. No P04/full-gate pass is anticipated
by this committed snapshot. No push/PR or repeat original Review will run.
