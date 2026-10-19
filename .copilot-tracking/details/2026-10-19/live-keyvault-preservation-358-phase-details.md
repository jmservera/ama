---
title: Existing-resource preservation phase details
description: Original no-write implementation details for issue 358
ms.date: 2026-10-19
---

## Task and Evidence

Task ID issue-358-live-preservation; slug live-keyvault-preservation-358.
The matching original research and plan dated2026-10-19 are authoritative.
Live source base7f96d9957b28cb174aa759c842376f24087d71a3 is unchanged.
One inline continuous research trace; no mock or source fix.
Actual app ARM inventories are null, so the criterion is not executable
without preparing materially different state.

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve the concrete blocker and safety inventory

Purpose: follow the owner's concrete-blocker stop path without fabricating
actual preservation success or running another mock-only/heavy delivery.
Dependency: original independent critique of final candidate plan/details.
Allowed write boundary: new dated task RPI files, infra/README.md,
docs/architecture/cutover-evidence-pack.md, docs/reference/README.md and
append-only docs/reference/log.md. No other tracked files.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Final read-only invariant and cleanup check

Use unchanged production Azure.rest GET at API_VERSION for the same three
RG apps. Compare secret/null/KV/binding/revision metadata with initial
sanitized record. No POST listSecrets, Graph, PATCH, deployment or restart.
If concurrent change appears, report and retain unknown rather than rollback.
Check task-created bytecode only; retain external summary files0600. No cloud
objects were created, hence no cloud delete or lock cleanup is authorized.
Completion: dated final read summary, exact cleanup inventory and limitations.
Completed2026-10-19T14:24:58Z: every compared count/null/revision/ready/lock/
handoff field stable. External final-management-summary.json0600 retained.
Four own14:19 bytecode files removed individually and empty cache directory
removed. No cloud cleanup or rollback required; no mutation was performed.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update existing durable evidence

Record the source-path distinction: preserve_app_secrets has no Graph/image
dependency; full secret_reference mutating path creates a password and full
setup includes runtime/SQL/restart. No function/guard is changed.
Quote exact primary blocker (zero actual KV pairs/secretRef bindings),
secondary actual profile guard refusal and permission metadata limits.
Preserve older offline-only observations as dated history. Link new deltas
from existing runbook/evidence/index; log append only; memory untouched.
Completion: coherent changed Markdown with no secret/identifier payload.
Completed: existing runbook, cutover evidence pack, KB index and append-only
log have dated deltas; six new local section links resolve. Old log is exact
base-byte prefix; source/tests/memory/case studies and all7 old358 RPI artifacts
are byte-identical. No prior outcome rewritten.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Reconcile original RPI evidence and handoff

Changes record distinguishes executed reads from unexecuted mutation/helper
rebuild/listSecrets and gate. Original critique/Review are immutable after
completion; route residuals later. Reconcile task markers, result/outcome,
state and external logs before independent original Review. No source/tests
added/removed; maximum additions0; no generic passing test substitute.
Completion: AC2 evidence-disposition outcome, AC1 still Blocked / Not run.
The coordinator decides any later publication route; no publication candidate
or authoritative full-gate receipt is claimed for this blocked result.
Completed before Review: P01/tasks, plan/details/changes/state reconciled;
AC1 Blocked/Not run, original Review pending, all implementation evidence
local/uncommitted, unchanged HEAD/base. Validation summary external0600.

## Supplemental Implementation Direction (2026-10-19)

Same task/slug/base. P01 is historical no-write evidence; P02-P04 implement
the owner's later selected real isolated synthetic baseline. Original critique
and Partial/Residual Review are immutable. External ownership inventory:
/tmp/issue-358-synthetic-20261019-1450/inventory.json,0600 in0700 directory.
All five initial IDs are actually absent; deployment absence is independently
confirmed from exact DeploymentNotFound plus deployment-list metadata.
No resource writes at this handoff.

<!-- rpi:phase id=P02 -->
### [x] P02: Establish bounded private lifecycle prerequisites

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Independently assess new lifecycle material before writes

Read cycle2 research and supplemental plan including limits, exact inventory
and private research summary. Write only supplemental safety assessment, never
original critique or Review. Assess native-secret creation AND deletion route,
MI/role bounds, private image, zero ingress/replicas, concurrency, async provider
validation, fail-safe cleanup, cost/lifetime and representative acceptance.
Record all actionable findings once, with direct dispositions before allocation.
Completed: supplemental safety assessment directly inspected all four supplied
external primary metadata files and unchanged source; Suitable with limits.
F1-F5 planner-owned clarifications accepted; no open decision-critical finding.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Preflight task-owned identity/roles/private cleanup job

Selected existing environment is internal/public Disabled, Consumption, same
approved private VNet as vault endpoint and private registry. Dedicated MI
has no tenant/subscription grants: Secrets Officer at exact new synthetic
secret scope, AcrPull at exact existing registry only. Record random role UUIDs
in inventory and GET absence before PUT. Use production Azure.rest transport.
New manual job uses already deployed private API digest with fixed Python
stdlib-only command, no entrypoint/default API execution, no packages or secrets.
Only task-owned job may start/override, never any existing workload.
Code obtains MI token in memory, uses TLS/private DNS, emits only fixed statuses
and error codes. Preflight reads versions metadata of exact absent synthetic
name and must get404 SecretNotFound or HTTP200 exact empty value array/no
continuation, plus deleted-name404; never Forbidden/network error. Retry only
bounded identity propagation. Resource body files0600 auto-removed.
Worker audience is https://vault.azure.net; operator ARM authorization is
separate and never passed to the worker. Pre-existence secret-scope role support
is tested by actual provider PUT/readback/preflight, not inferred from a source
that merely documents individual-secret scope. All other names fail closed.

<!-- rpi:phase id=P03 -->
### [x] P03: Execute synthetic baseline preservation and cleanup

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Establish baseline and exercise production preservation

Depends on P02 success. Incremental ARM deployment secureString synthetic
payload; what-if must show exactly one Create at owned vault-secret ID and no
other actionable changes. Poll deployment terminal; verify owner tag, expiry,
enabled and actual secretUriWithVersion. No real value reads or credential
helper naming guard bypass. Capture returned synthetic version only privately.
Synthetic deployment code is external task-owned operator code, not a production
credential_arm.py edit, invocation with an invalid name or guard relaxation.
Create own app with attached dedicated MI,0.25CPU/0.5GiB, no ingress/rules,
min0/max1, Consumption, pinned private API image, harmless sleep override.
Configuration contains KV reference and unrelated random value; one unused env
secretRef may point to the unrelated synthetic secret, only on this new app.

Require successful provisioning before fresh baseline GET/listSecrets.
Only owned app POST listSecrets allowed; both values are synthetic. Exact
hash comparisons remain external. Actual preserve_app_secrets reconciles
configured/listed inventory. Payload matches production pattern
properties.configuration = current configuration merged with preserved secrets.
Use actual Azure.rest PATCH, no Graph/secret_reference/password path.
Poll terminal provisioning (bounded), then actual fresh GET/listSecrets.
Require exact expected fields, binding, template/MI/tags and revision readiness.
Keep provider-normalization differences explicit; no silent success fallback.
Read replicas for the owned app to qualify min0 versus actual execution.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Prove owned cleanup and existing workload invariants

Finally runs even after any allocation/request ambiguity. Read exact owned IDs
and ownership tags before delete; missing is successful only if actual404.
Delete app and poll absent. New cleanup job runs fixed exact-synthetic DELETE,
checks active versions404, polls deleted metadata, purges owned synthetic only
if policy permits, verifies deleted404; no vault-list or value GET. Seven-day
policy is never disabled. If purge is denied, report retained soft-delete state
and exact expiry rather than full cleanup. Secret is never created unless
preflighted private route exists. No secret cleanup payload runs on existing jobs.
Delete exact owned deployment history, job, role assignments, MI, polling404;
never RG/delete by wildcard. Compare original11 workload hashes and active
revision/readiness, selected backing raw hashes and full RG resource-ID set.
Any concurrent drift is reported, never rolled back.
Stop new allocations by15:45Z; cleanup must continue past the16:00Z target
if necessary, with any overrun reported. External exact inventory is recovery
authority after interruption. Backing hashes are top-level ARM properties/
metadata only; child-secret enumeration is never folded into them.

<!-- rpi:phase id=P04 -->
### [ ] P04: Preserve supplemental execution and freeze unpublished candidate

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Reconcile evidence and durable documents

Append actual evidence to same-task artifacts; preserve original verdict/hash.
Primary in-worktree summary holds counts, timestamps, source/base, exact method
boundary, sanitized provider codes, named comparisons, inventory cleanup
booleans and operation counts, no IDs/private payload/value hashes. Historical
external no-write summaries are redacted into the same primary summary so a
reviewer can inspect evidence directly without external-read authority.
Existing docs/index/log use normal documentation links, no tracking references.
Original populated deployed-app/full setup/profile acceptance remains distinct.

<!-- rpi:task id=P04-T02 -->
#### [ ] P04-T02: Commit and execute full external-receipt gate

No new original Review is performed; coordinator owns independent exact-head
assessment of supplemental evidence and gate receipt. Commit all same-task
candidate evidence before gate, gh-derived local noreply for author/committer,
Conventional Commit plus required trailer. Fetch main; full --all actual17 groups
with credential-scrubbed environment and unchanged Node PATH, shared fixed lock,
external output/receipt, no uv or remote fallback. Frozen HEAD remains unchanged
after gate; receipt verification current origin/main and clean status. If gate
blocks, preserve actual group failures, no skip or fabricated passing receipt.

## Supplemental Completion Evidence

P02-T02: real secret-scoped role provider PUT/readback succeeded before secret
existence. Private job versions metadata200 empty/no continuation and deleted
metadata404 passed15:05:53Z. Prior operator failures were cleaned and retained.
P03-T01: native one-Create what-if/deployment verified; versioned real reference
and ordinary random secret were established before PATCH. Unchanged production
helper and Azure.rest PATCH followed by actual InProgress/Succeeded polling
and fresh GET/listSecrets passed all eight exact comparisons15:07:08Z.
One app replica existed at readback, min0 is not claimed as zero runtime.
P03-T02: cleanup worker Succeeded15:08:20Z, active/deleted secret absent;
app/deployment/job/roles/MI absent by15:09:10Z. Fresh role probes confirm all ten
historical UUIDs RoleAssignmentNotFound. Before/after all11 existing workloads
and RG membership/top-level backing hashes match. No existing workload changed.
P04-T01: durable docs/index/append-only log updated; sanitized primary summary
is in-worktree. Original critique/Review hashes unchanged; no new Review.
P04-T02: pending post-commit exact-HEAD full17-group gate, external receipt and
external final-state record as named in plan; frozen tracked evidence must not
be edited after the gate. Coordinator exact-head review remains outstanding.
