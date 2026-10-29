---
title: Both demo sites redeployment plan
description: Two image-only revisions using the previously approved ACR route
ms.date: 2026-10-29
---

## Metadata

* Task ID: 3897222c-2d62-4e25-a059-eecfbdce51d0
* Task slug: both-demo-sites-redeploy
* Source: fetched origin/main d70ee60ab3d7346a9991cf64382d9985f4d09f2e
* Branch: ops/sites-redeploy-20261029, clean at intake and equal to main
* Research: .copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md
* Details: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md
* Changes target: .copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md
* Status: RPI lifecycle/local evidence handoff complete; implementation Partial, original Review Complete / Not accepted

## Executive Summary

Execution result: employee latest main is healthy with exact preservation.
Resident latest-main revision failed activation and image-only CLI introduced
two empty value fields alongside secretRefs. One recovery revision restored
the old resident digest and exact original configuration using corrected raw
ARM schema. Both sites are healthy, min0 and ACR policies exact; the requested
both-sites-latest-main outcome is NOT achieved. No further forward retry is
within this task's one-forward-revision limit.

Refresh both existing apps from exact fetched main using clean exported src/
and their current Dockerfiles. Reuse the earlier successful local Docker build
and VM-only ACR expose-token push route, avoiding a known failing remote task
route that would need wider worker networking. Push two new unique tags,
resolve exact manifests, restore every ACR policy field before app mutation,
then create one image/suffix-only revision per app. Prove complete preservation,
actual startup and anonymous HTTP health. Keep all existing digests.
No application edits or authenticated acceptance are included. Local evidence
commit only; coordinator owns publication gates, push and Refs-only PR.

## User Decisions and Requirements

* Run research, plan, implement, review in order with dated artifacts.
* Deploy both named apps in ama / cae-cutover-test-demo to current main.
* Use the earlier successful employee re-apply procedure and approved ACR route,
  restoring exact policies; "Proceed without cost query".
* Full config backup before mutations; preserve all env, secretrefs, identity,
  registries, ingress and min replicas 0 exactly.
* One new revision per app; rollback only for unhealthy revision or startup
  errors, never verification-tool failure alone.
* Anonymous curl probes only; no secrets, .env, private data, SQL, other apps,
  roles, subscription/network changes beyond the explicitly approved ACR route.
* Never delete ama, registry tags or images.
* No gh or push. Commit evidence locally with mandated Copilot trailer.

## Goals

Give owner both review sites on new immutable main-built images, with safe
rollback material, unchanged runtime configuration and durable non-secret proof.

## Scope and Non-Goals

Only the two specified existing apps and temporary approved ACR exception.
No source changes, infrastructure deployment, role/SQL operations, auth bypass,
model requests, cost queries, broad cleanup, image deletion or publication.

## Functional Requirements

* Build employee from src/api/Dockerfile and resident from
  src/api/Dockerfile.resident-demo, each with src/ context.
* Compare configuration, identity, all stable resource properties, complete
  template (excluding only image/revision suffix) and auth metadata.
* Prove exactly one added revision for each app using before/after list and
  explicit revision show; never retry an ambiguous update.
* Prove both old and new manifests exist while registry route is available.

## Non-Functional Requirements

* Restrict backup directory to0700 and private JSON/log files to0600.
* Never retrieve listSecrets or Key Vault values, print raw env/config/logs or
  persist registry tokens. Docker token/config used only in owned temporary
  external config, cleaned after push; credentials via stdin.
* Nonblocking shared heavy lock for local builds; do not interrupt foreign work.
* Bounds: local build1200s each, individual policy calls60s, each push420s,
  each app convergence600s. Registry opening separately bounded per image to
 600s, private-first restoration in finally plus120s readback. Restore before
  any app writes; no whole-registry overwrite.
* Preserve original errors and classify tool failures separately from runtime.

## Acceptance Criteria

* AC1: source SHA/tree and clean build export documented; both builds succeed.
* AC2: two new digest-pinned images exist; both old manifests protected; exact
  full ACR policy projection equality after restoration.
* AC3: one new revision each; active, latest=ready, healthy/provisioned, correct
  digest; complete baseline equality except two intended per-app template fields.
* AC4: min0/max4 employee, min0/max1 resident unchanged; env/refs, auth, ingress,
  identities, registries and non-target fields exactly equal.
* AC5: curl public/health probes; health200 and positive new-revision startup or
  replica readiness; employee /200 byte-equal main public welcome page,
  /app and protected JS401/redirect, and resident
  public page without anonymous case data. No authenticated feature claims.
* AC6: ordered phase evidence, one independent critique and one Review, local
  evidence-only commit with privacy-safe identity and mandated trailer; no push.

## Test Ownership and Locked Boundaries

No canonical test changes or removals. Maximum additions: zero test/source files.
Semantic verification consists of exact app/config/ACR equality, manifest
HEAD/GET digest equality, revision set comparison, log classification and curl.
No regression suite rerun is needed for evidence-only artifacts; no new
application behavior is authored. No full local publication receipt claimed.
The complete gate and immediate receipt verification remain required before
coordinator publication unless separately authorized; no inherited exception.
Generated targets: private backups/build export and sanitized evidence only.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Preserve and build (complete)

* [x] P01-T01: Full private baseline backup, exact clean main export and both builds.
* [x] P01-T02: Push both unique tags via approved route, prove manifests, restore exact ACR.

<!-- rpi:phase id=P02 -->
### P02: Refresh and verify both apps (partial; resident recovered, not latest main)

* [x] P02-T01: Employee one image-only revision; prove exact preservation and health.
* [ ] P02-T02: Resident latest-main outcome unmet: one forward revision failed activation; one old-image recovery verified with exact original config.
* [x] P02-T03: Final cross-check both apps and ACR; record actual partial result.

<!-- rpi:phase id=P03 -->
### P03: Independent Review and local handoff (complete)

* [x] P03-T01: One independent Review against complete execution evidence, Complete / Not accepted.
* [x] P03-T02: Reconcile evidence/state, commit locally, leave publication to coordinator.

## Dependencies and Recovery

P01-T02 depends on both successful builds and baseline backup. P02 depends on
successful digest proof and exact ACR restoration. Independent app updates are
executed sequentially to bound the failure surface, not as a shared transaction.
If one fails, preserve the successful other deployment.

Before each update re-read exact app/auth projection and compare baseline;
refuse on concurrent drift. Update only --container-name, --image,
--revision-suffix with -o none. No env/scale/auth/ingress flags.
After ambiguous CLI failure inspect the named suffix/list, never repeat mutation.
Tool-only failures block verification but not trigger rollback.

If actual unhealthy/provisioning-failed/startup-error evidence appears, restore
only that app's backed-up old digest with image-only update (configuration was
never intentionally changed). This failure-only recovery may create one extra
rollback revision; disclose the exception to the one-forward-revision target.
If drift indicates another actor changed fields, do not overwrite that work.
Never change revision mode, traffic, ingress or SQL to repair a deployment.
If new source requires unavailable schema/config, rollback the failing app and
record blocker rather than changing SQL.

## Critique Disposition

Exactly one fresh independent critique executed, original verdict Revise,
retained at .copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Applied directly | Details Frozen Execution Contracts: monotonic per-window deadline, reserved restoration budget and bounded subprocess/network operations |
| PC-002 High | Applied directly | Details Frozen Execution Contracts: exhaustive named comparator exclusions; all other fields protected |
| PC-003 Medium | Applied directly | Details Frozen Execution Contracts: separate manifest and config equality chains |
| PC-004 High | Applied directly | Details Frozen Execution Contracts: immediate per-app acceptance and bounded single recovery postconditions |
| PC-005 Medium | Applied directly | Details Frozen Execution Contracts: explicit anonymous curl routes, statuses and resident static-shell predicates |

No unresolved significant/divergent user decision. No second critique.
The later original Review retains RV-003: actual executor restoration sub-bounds
did not fully implement the accepted PC-001 contract, despite all observed
windows restoring quickly and exactly. This is open later implementation work;
the original planning disposition is not rewritten or treated as closure.

## Follow-Up Items

* Highest priority: Research actual resident startup refusal and CLI secretref
  serialization. Source now requires17 view columns, whereas older evidence
  records16; this remains a hypothesis, not a live SQL diagnosis. Any later
  resident forward retry needs separate authorization and exact-template route.
* Correct local executor exact-secretRef request handling (RV-002) and
  restoration/readback deadline enforcement (RV-003) with synthetic tests
  before a later retry; no live failure injection authorized.

* Authenticated owner review of employee/resident features is separate from
  anonymous rollout proof; no secret access is authorized.
* Coordinator must satisfy publication gates and create a Refs-only PR; this
  task does not push, merge or claim hosted/human approval.

## Handoff

Original independent Review executed Complete / Not accepted. Original dated
evidence committed locally as59049aa80de14972c717e1d31a27309b984e7c7c,
privacy-safe author/committer and requested trailer verified. P01 and
employee/final-safety proof complete; resident latest-main acceptance unmet
despite verified recovery. Local handoff complete; automatic session remains
running at Follow-up awaiting selection. No push, fixes, more rollouts or repeated Review. Original
critique, Review and failed execution evidence preserved.
