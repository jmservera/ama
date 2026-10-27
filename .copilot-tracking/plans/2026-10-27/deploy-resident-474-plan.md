<!-- markdownlint-disable-file -->
# RPI Plan: Deploy resident PR 474

## Task Metadata

* Task ID and slug: deploy-resident-474
* Date: 2026-10-27
* Planning status: Ready for authorized deployment subset; full acceptance blocked
* Details: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/deploy-resident-474-plan-critique.md

## Executive Summary

Deploy exactly the merged resident source at main 885ee05f to the existing
resident app, preserving employee/SQL/job boundaries. Test live HTTPS in a short
window and close ingress afterward. Publish original evidence with an explicitly
partial outcome wherever required proof is unavailable.

### What You May Not Know

There are four existing apps, all min0, and eight Manual jobs. The merged assistant
is deterministic: its optional Azure adapter has no runtime activation wiring or
durable cost ledger. Provisioning a model alone cannot satisfy that requirement.
The owner's password is held offline; this task must not read secrets or change
the shared credential to manufacture a positive login result.

### Unresolved Decisions or Blockers

Model activation and credential-dependent live checks remain requested but blocked,
not removed from acceptance. Deploy the independent authorized merged features
without claiming those gates passed. No source changes are planned.

## User Decisions and Requirements

* Run research, plan, implement, review in order; commit dated original artifacts.
* Deploy #474; Refs #462, #466, #467, #468, #469. No closing keywords.
* Additional USD30 through 2026-10-31T23:59Z; Azure OpenAI <=USD20, MI only,
  smallest suitable deployment/low quota and deterministic fallback.
* Existing ama only, no broad grants/private endpoints/secret reads; preserve SQL
  and employee login; every existing app min0 and all eight jobs Manual.
* Start latest main in the supplied worktree/topic branch; open evidence PR to main.
* Build/gate timeout-zero lock, pip not uv; scoped --changed receipt, not full gate.
* Prove real resident login/isolation/gauges/assistant/top-right sign-out/expiry;
  ingress open only during testing and final ingress state explicit.

## Goals

Replace the old interim resident image with the current merged features and give
the owner reproducible deployment identity and honest live acceptance evidence.

## Scope and Non-Goals

In scope: resident image build/push, existing resident image update and the merged
read-only resident view deployment, temporary ingress, safe browser/API tests,
restoration and evidence. No application edits,
model-host/ledger engineering, credential rotation, SQL business-data writes, employee changes,
new groups, private endpoints or unrelated grants. The sole permitted SQL release
operation is the exact already-merged CREATE OR ALTER resident projection view;
no table, row, principal, grant, role, sizing or employee change.

## Functional Requirements

The resident revision must serve merged assets and retain existing session,
own-case projection and read-only advisory behavior. Unsupported AI activation is
reported blocked, retaining the existing deterministic assistant.

## Non-Functional Requirements

* Resident min0/max1; other apps and eight Manual jobs unchanged.
* ACR policy and network rules restored exactly, even after failed push.
* Ingress disabled at conclusion, authority expiry unchanged, no secret output.
* Fresh USD30 task envelope: reserve USD1 build/test, retain USD20 model allocation
  and USD9 contingency. Actual delayed charges unknown; report estimates as such.
* Build/gate must acquire /tmp/ama-rpi-heavy.lock with timeout0; contention blocks
  only the affected heavy operation and never authorizes concurrent heavy work.

## Acceptance Criteria

* Image source, digest, active revision and public URL recorded.
* Live Playwright proves unauthenticated UI, generic invalid-login denial,
  unauthorized/forged-session and staff-route denial, security headers and assets.
* Registered-login, own-case post-login features, logout and natural 1800-second
  expiry are passed only if genuine credentials can be supplied within no-read
  rules; otherwise explicitly blocked, never replaced by mocks or forged sessions.
* Azure OpenAI activated only with reviewed runtime MI/ledger wiring; otherwise
  blocked and no unused model or role is created.
* Final ingress disabled; all four apps min0, eight jobs Manual; SQL and employee
  configuration metadata invariant. ACR restoration exact.
* Independent critique and one original Review retained, then scoped receipt
  verified immediately before push and evidence PR created without issue closure.
* Human/hosted approvals remain incomplete until genuinely supplied.

## Sources

Research: .copilot-tracking/research/2026-10-27/deploy-resident-474-research.md,
C1-C6 and W1-W5. Prior owner-designated release scripts and cost ledger are inputs,
not copied approval or fresh validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Release merged image and compatible projection

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Snapshot and build/push

Save sanitized app/job/SQL/ACR metadata and cost admission externally. Try ACR build
with no network mutations under the heavy lock. If unavailable, local locked
Docker build, then narrowly approved ACR VM-IP/token push with finally restoration.
Record failures and immutable digest. No image context beyond src/.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Deploy compatible resident projection and image

While ingress is disabled, update existing resident container to exact digest,
retain all other configuration, await healthy revision. No broad Bicep deployment.
The first live attempt found ProgrammingError at SQL startup: the merged reader
requires sensor_home_id/sensors_json absent from the previous deployed view.
Deploy only the third batch of merged infra/sql/resident-showcase.sql through one
execution override of the existing Manual initializer/identity, after transactional
metadata/principal preflight. Compare original fourteen columns and permission
snapshots; add exactly the two merged sensor projection columns; rollback on any
unexpected change. Do not execute table/principal/grant batches or read case data.

<!-- rpi:phase id=P02 -->
### [x] P02: Live verification and closure

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run bounded live checks

Enable HTTPS ingress only for tests, run actual Playwright and negative API checks,
record credential-blocked tests honestly, then disable ingress in finally.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Verify restoration and cost ledger

Compare ACR policy, non-resident app configuration, all replica minima/jobs/SQL.
Record duration, estimate and billing uncertainty. Map #462 criteria precisely.
After verified ingress closure, deactivate only the tested resident revision
to stop ongoing compute; retain deployed image/min0/max1 and record stopped/zero.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publication

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Independent Review and scoped gate

Run one independent Review against implementation/evidence, route findings without
a same-task review loop. Commit original artifacts and implementation evidence.
Fetch main and require it remains an ancestor of the candidate. Run
python3 tools/rpi-checks.py --changed --lock-timeout 0 --base <current-main-sha>
--out <new-external-directory>. Verify with --verify-receipt <external-receipt.json>
--required-scope partial --base <current-origin-main-sha> immediately before a
bounded independent exact-head publication assessment and again immediately
before push. This assessment is not a repeated RPI Review. If main moves outside
candidate ancestry, stop publication, record source/base delta and do not silently
merge/rebase/force-push. Open PR only if publication gates permit.

## Test Ownership and Coverage

Owner: parent deployment task. Canonical code/tests unchanged; exact removals none;
maximum committed new test/source files zero. Generated evidence: sanitized JSON,
screenshots and command logs externally; dated tracking summaries committed.
Semantic checks: live HTTPS denials and source asset parity. Regression checks:
cloud configuration invariants. Credential-dependent and AI checks remain
separately blocked; no acceptance credit for local or historical stand-ins.

## Dependencies

P01-T02 follows P01-T01; P02 follows healthy resident revision; P03 follows closure
and invariant capture. Fresh critique precedes any deployment mutation.

## Critique Disposition

One independent critique executed, original verdict Revise retained. All eight
compatible findings are applied directly; no further critique is commissioned.

| Finding | Owner and disposition | Resolving plan/evidence |
|---|---|---|
| PC-001 High | Parent, applied | Details P01-T01: deny-before-expose, close-first restoration, normalized actual IP rules, exact canonical equality and publication block on failure |
| PC-002 High | Parent, applied | Details P02-T01: owned independent watchdog, absolute deadline, null-ingress readback, failure blocks publication |
| PC-003 Medium | Parent, applied | Details P01-T01: rate/quantity admission, no remote run with unknown bound, recorded cancellation/terminal state and separated reservations |
| PC-004 High | Parent, applied | P03-T01 explicit --lock-timeout 0 and verifier --required-scope partial |
| PC-005 High | Parent, applied | P03-T01 ancestry stop, no silent reconciliation |
| PC-006 High | Parent, applied | P03-T01 independent exact-head assessment after receipt, original Review preserved |
| PC-007 High | Parent, applied | Details P01-T01 exact-image Trivy and non-secret runtime/refusal contracts precede deployment |
| PC-008 Medium | Parent, applied | Details preservation projection whitelist; allowed resident image/revision/temporary-ingress deltas, no hidden-value acceptance |

## Follow-Up Items

* Implement reviewed MI host wiring and durable USD20 inference reservation ledger;
  this requires a new application/infrastructure engineering scope and its gates.
* Owner-run authenticated live session, features and natural expiry with the
  offline-held credential; do not read or replace it in this task.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md.
First eligible task P01-T01 after critique. Blocked requirements stay explicit.
