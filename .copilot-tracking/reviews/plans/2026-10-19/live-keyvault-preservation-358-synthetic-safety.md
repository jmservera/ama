<!-- markdownlint-disable-file -->
---
title: Synthetic baseline lifecycle/safety assessment (supplemental, new material only)
description: Independent pre-write assessment of P02-P04 synthetic Key Vault/Container Apps baseline roundtrip for issue 358
ms.date: 2026-10-19
---

## Scope and Independence

This assesses only the NEW supplemental material: research Cycle2 (S-C1, S-W1-S-W7),
the supplemental plan sections (Supplemental Goals/Scope, S-FR1-S-FR4, S-AC1-S-AC5,
P02-P04 checklist) and matching phase-details, plus the authorized external
evidence files. It is not a repeat of the original critique or original Review.
Verified unchanged: original critique (sha256
`c4e1e226080ba9210ee0b7daac32d34e61bb50533874203b4415ffa805aea121`) and original
Review (sha256 `5fb39b9ef7b3aac4cbef810019eb1db23d6890b3c74d0baaf98059c75f9df41b`)
on disk match the inventory's recorded hashes; both remain immutable. No cloud
writes, resources or logs exist yet (`resourceWrites: 0` in both
`research-summary.json` and `inventory.json`).

Primary evidence directly inspected (sanitized, 0700/0600, no secrets):
`/tmp/issue-358-synthetic-20261019-1450/inventory.json`,
`research-summary.json`, `selected-resources.json`, `workloads-before.json`.
Also inspected: `infra/scripts/credential_arm.py` (vault_id/preflight/store) and
`infra/scripts/setup-entra.py` (`preserve_app_secrets`, `secret_reference`,
`secret_reference_digest`, `verify_secret_handoff`) to validate the plan's
claimed production code paths and sequencing against actual source, not the
plan's prose alone. No resource IDs, hashes, or private payload from the
evidence files are reproduced below.

## Findings

### F1 (Non-Blocking): Deployment code provenance is not explicit — risk of tempting a credential_arm.py modification

`credential_arm.store()` hard-validates the secret name against
`entra-[a-f0-9]{32}-[a-f0-9]{12}` and raises `CredentialError` for any other
name. The planned synthetic secret name (`issue358-synth-...`, per
`inventory.json`) cannot pass that guard. Research S-C1 correctly states the
module's "fixed credential naming/Graph context is not reused or bypassed,"
but neither the plan nor phase-details states explicitly that P03-T01 will add
**new, standalone** deployment code mirroring the technique (secureString
incremental deployment + what-if-prove-one-Create) rather than touching
`credential_arm.py`. Without that explicit instruction, an implementer under
time pressure could rationalize relaxing the regex in the production helper
to "reuse" the function — a prohibited change to the live credential pathway.
**Resolution**: before P03-T01 code is written, phase-details should state in
one sentence that `credential_arm.py` is read-only/untouched and that the
synthetic deployment uses new task-owned code co-located with the cleanup job
tooling, not a parameter/regex change to the production module.

### F2 (Non-Blocking): Key Vault data-plane token audience not stated for the cleanup job

The cleanup job must call Key Vault **data-plane** operations (list versions,
delete, purge — confirmed data-plane-only per S-W4/S-W5, and no ARM DELETE
exists for secrets). That requires an MI token for resource
`https://vault.azure.net` (or the vault's configured audience), distinct from
the ARM-plane token (`https://management.azure.com`) used for the deployment
what-if/PUT and role-assignment GETs. Phase-details P02-T02 says the job "obtains
MI token in memory, uses TLS/private DNS" but does not name the two distinct
audiences the job will need to request. If the job code requests only the ARM
audience for all calls, data-plane calls will fail — and that failure would be
indistinguishable in form from the already-observed local Forbidden/timeout
findings, making the preflight's SecretNotFound-vs-Forbidden diagnosis
ambiguous about which cause actually applied.
**Resolution**: phase-details for P02-T02/P03-T01 should name both token
audiences explicitly so the preflight's pass/fail interpretation is unambiguous
when read later (even though the fail-safe default — treat any non-SecretNotFound
result as abort-and-clean — is already safe either way).

### F3 (Suggestion): Pre-existence RBAC scoping is sound but uncited

The lifecycle requires assigning "Key Vault Secrets Officer" scoped to the
exact secret resource ID *before* that secret exists, so the P02 preflight (a
versions-metadata GET on an absent name) can distinguish RBAC-propagated
SecretNotFound from a true Forbidden/network failure. I confirmed this is a
genuinely supported Azure RBAC capability (role assignments may target a
not-yet-created child scope, e.g. `.../vaults/{v}/secrets/{name}`, per
Microsoft's Key Vault RBAC guide) — so the design is sound. Research/plan does
not currently cite this capability explicitly; S-W7 only establishes
individual-secret scoping in general, not scoping ahead of resource existence.
**Resolution**: add one citation/line to research or phase-details confirming
pre-existence scoping, so a future reader doesn't need to re-derive this before
trusting the preflight's diagnostic value. Not blocking since the fail-safe
abort-and-clean path is correct regardless of the underlying cause.

### F4 (Non-Blocking): Hard lifetime bound (16:00Z) does not state priority over in-progress cleanup

`inventory.json` records: "No later than 2026-10-19T16:00:00Z; cleanup in
finally on success/failure." The plan's safety model depends on a `finally`
block always running synchronously within the same execution. Nothing in the
plan states what takes priority if P03-T02 cleanup is still polling (e.g.
waiting out soft-delete/purge propagation, or a bounded cleanup retry) when
16:00Z passes — i.e., whether the lifetime bound governs only when new
allocations may *start*, or whether it is also a hard stop that could truncate
an in-progress cleanup. If execution were externally interrupted (session
timeout, tool stop) exactly at or near that bound before `finally` completes,
owned role assignments/MI/job/possibly-undeleted secret would be stranded with
no automatic sweep.
**Resolution**: state explicitly (in phase-details or the plan) that 16:00Z
bounds only the start of new resource allocation, and that cleanup must be
allowed to run to completion (or to its one bounded retry) even if that
extends past 16:00Z; and that if the process is killed before cleanup
completes, the externally-recorded inventory IDs are the authoritative list
for a follow-up manual cleanup pass.

### F5 (Suggestion): Shared-vault backing-hash semantics not specified

`selected-resources.json` records a `backingHashes` entry for the shared,
pre-existing Key Vault (`kv-cutovertest-rzsrg`) that the synthetic secret will
be created in and removed from. If that hash is computed over the vault
resource's own ARM properties (publicNetworkAccess, RBAC flag, bypass,
retention — consistent with what `research-summary.json.vault` records), it
should legitimately stay stable across an owned child-secret create/delete and
the invariant check is meaningful. If it were instead computed over anything
that enumerates the vault's secret list/count, it would show expected,
self-inflicted "drift" after a successful synthetic create+cleanup — a false
positive against the "existing11 workload snapshots & RG set/backing hashes
unchanged" acceptance bar. The plan/details do not state which case applies.
**Resolution**: confirm (in a one-line note at P04-T01) that shared-resource
backing hashes are computed from top-level resource properties only, not
child/secret enumeration, so the final invariant comparison cannot be
misread as a genuine regression caused by this task's own authorized activity.

## Non-Findings (explicitly checked, no issue)

* Single shared dedicated MI for both the new app (KV secret resolution) and
  the new cleanup job (secret delete/purge) is coherent: "Key Vault Secrets
  Officer" at the single-secret scope is a superset role whose dataActions
  cover get/set/delete/purge, so one role assignment legitimately serves both
  the app's reference resolution and the job's cleanup — matching the
  "minimal new dedicated MI + two exact new roles" requirement.
* Ordering in P03-T02 (delete owned app before deleting the secret) avoids a
  live app-to-secret dangling-reference race; confirmed against the plan text.
* `preserve_app_secrets`/`secret_reference_digest` in `setup-entra.py` match
  the plan's described merge/PATCH/verify sequence; no Graph or
  `secret_reference` mutation path is invoked by the planned S-FR3 call.
* Soft-delete/purge handling (7-day retention never disabled; purge-denied
  path reports residual state rather than claiming full cleanup) is correctly
  specified against S-W5's data-plane/all-version-scoped deletion finding.
* The `listSecrets`-may-not-return-a-resolved-KV-value caveat in S-AC1 is an
  honest, pre-declared limitation rather than an overclaim.
* Original immutable artifacts verified byte-identical to recorded hashes;
  no original verdict is touched or relabeled by this assessment.

## Verdict

**Suitable to proceed to P02 execution, with limits.** No Blocking issues were
identified in the new supplemental material: the core safety architecture
(preflight-before-allocation, scoped-and-minimal new RBAC, app-before-secret
cleanup ordering, soft-delete/purge handling, explicit non-overclaiming
acceptance criteria) is sound and the two load-bearing assumptions I checked
independently (pre-existence secret-scope RBAC, and Officer-role coverage for
both app and job) are both confirmed valid. The five Non-Blocking/Suggestion
items above are clarifications that reduce residual ambiguity (code-provenance
discipline, token-audience explicitness, lifetime-vs-cleanup priority, and
backing-hash semantics) and should be folded into phase-details before or
during P02-T02, but none invalidates the plan's safety model or blocks
starting the preflight step. Limits: this assessment does not execute any
Azure call, does not test the actual provider behavior, and does not
substitute for the P02-T02 preflight itself or for the pending coordinator
review of the frozen candidate.
