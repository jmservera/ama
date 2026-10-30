---
title: Resident activation timeout recovery plan
ms.date: 2026-10-30
---

## Task Metadata

Task ID563-timeout-recovery-20261030; slug resident-ai-activation-563-timeout-recovery.
Date2026-10-30. Planning Complete/Ready; one independent critique Complete/Pass.
Details/critique/changes use this slug and date in their canonical directories.

## Executive Summary

Fix the live verification sequence, not authentication: restart intentionally
invalidates existing sessions. Back up exact current configuration, enable the
two documented variables, wait for a ready revision and warmed health, then
sign in fresh. Require an actual grounded AI pest reply and out-of-scope rules
fallback. If verification fails, restore effective backed-up configuration.

### What You May Not Know

Keeping the same session through redeploy is invalid by design, even with an
unchanged signing secret. Longer waits alone cannot restore that session.
Healthy startup and an old model role do not prove runtime reservation/model
success. USD20 and November1 expiry still fail closed.
Fresh post-rollout login now works and the enabled pest request completed200,
but returned "Summary by rules - AI unavailable or usage limit reached", not AI.
Both variables were removed and exact effective original baseline restored in
ready100% recover-safe-180814. Activation remains Unmet. Two of four newly
granted sign-ins used; no blind inference retry. The inactive pod's console
is unavailable; existing workspace telemetry is network-perimeter denied.
Complete local publication gate is independent and may remain lock-blocked.
One independent Review is Complete / Not accepted; RV-001 routes runtime
diagnosis to later work, RV-002 schedules the remaining local closeout.

## Sources

Research .copilot-tracking/research/2026-10-30/resident-ai-activation-563-timeout-recovery-research.md
C1-C9; prior owner-enable artifacts remain unchanged.

## User Decisions and Requirements

* Owner authorizes activation and personally monitors cost; no ledger read or
  SQL public access. Existing USD20 ceiling and2026-11-01 expiry stay configured.
* Four new sign-in submissions total, credentials only inside automation;
  no credential output, screenshots, recordings or commits.
* Existing resident app/account/deployment only; min0, all jobs Manual.
  No new endpoints, broad RBAC/groups, employee mutation or deleting ama.
* Redeploy authority through2026-11-15; back up exact current configuration
  first, rollback failed verification, leave successful activation enabled.
* Ordered full RPI loop with dated artifacts, local commits/trailer, Refs #563
  only, no push; coordinator publishes. Heavy lock only for local gates,
  flock -w600.

## Goals

Remove the stale-session verification defect and obtain truthful live
activation evidence without weakening any access, consent or cost boundary.

## Scope and Non-Goals

Private execution helper plus new tracking evidence; narrowly related API
operations documentation clarifying process-bound post-rollout login if useful.
No application behavior change, images/build/deployments of source, SQL access/
migration, added settings, secret changes, RBAC, network, jobs or employee writes.
No whole-issue closure, human content acceptance or accessibility conformance.

## Functional Requirements

FR1: Capture exact current app, auth, revisions and jobs privately with hashes,
and read-only employee template/config/identity baseline for preservation.
No secret-list operation or raw config in git. Confirm expected current image,
Single mode, absent two assistant variables, min0/max1 and Manual jobs.
FR2: Apply exactly ENABLED=true and ENDPOINT documented in API README.
Wait up to10minutes for latest==ready, Succeeded and100% traffic. Warm health
with240s request timeouts, three attempts and15s delay; retry only anonymous
idempotent navigation/health. No inference retry.
FR3: Fresh context AFTER rollout and warm. Detect visible content OR sign-in
OR error after navigation. Persist each UI substep and only request path/method/
status/UTC, never body/headers/cookies. At most four login submissions tracked
before submit, one intended; no blind retry on401/429 or unknown login response.
A new sign-in is allowed only after observed process/session invalidation with
a healthy current revision; never authenticate across rollout.
FR4: Anonymous assistant denial; client no-consent no-request; direct server
no-consent400; exactly one consented synthetic pest request; actual200 AI label,
known collapsed sources, thin geometry, factual/process claims compared to
in-memory own-case projection/host guidance. Out-of-scope France question must
be rules-labelled inability/manual route. No credentials, account names, case
addresses or raw record in evidence. Safe actual reply may be retained after
credential and private-field exclusion; otherwise safe claim categories/hashes.
FR5: Any failed verification after mutation, including fallback/unsupported
claims, removes only the two previously absent variables. Wait fresh ready100%
revision, warm health and prove effective baseline template/config/identity/
auth/jobs/employee preservation. Normalize only empty value alongside unchanged
secretRef and revision suffix. On rollback failure explicitly report urgent
blocker, never weaken validation or change mode to force traffic.

## Non-Functional Requirements

NFR1: Private root0700/files0600, no trace/HAR/video/storage export/screenshots,
mask login email as password, clear fields, disable core dumps/debug. Credentials
read only inside automation; exceptions stage/type/fixed codes, never raw values.
NFR2: Persist before/after command argv, exit/time/hash; HTTP stage/status and
dispatch immediately, including failures. No success-shaped silent fallbacks.
NFR3: Reuse existing pinned browser runtime after missing system dependency
observation; no dependency-manifest changes. No local heavy lock for cloud work.

## Acceptance Criteria

AC1: Exact fresh backups and hashes before mutation; permitted delta only.
AC2: Live actual AI pest answer with relevant acknowledgement, honest limits,
housing-officer route and source-supported factual/process claims.
AC3: Thin AI-generated label <=24px high, <=85% body font, weight400, no
padding/border; sources collapsed. Out-of-scope rules/manual fallback.
AC4: Anonymous denial and client/server no-consent protection.
AC5: <=4 new sign-ins; unchanged scale/jobs/image/MI/auth/secrets/employee.
Failed AC2-4 triggers verified effective backup restoration, not success.
AC6: One critique/dispositions, one independent Review, local persistence,
actual full gate attempt/result. Missing gate receipt blocks publication,
not evidence recording. Human acceptance remains unchecked.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and activate safely

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Back up, validate helper and activate

Exact private backups, invariant guard, two-variable activation, ready/warm;
no credentials read before healthy ready rollout.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Fresh-session live proof or rollback

Depends T01. State-aware login, no-consent/denied/AI/grounding/out-of-scope;
mandatory rollback on any failed changed-candidate verification.
Execution complete via verified rollback; AI/grounding/thin label and
out-of-scope acceptance Unmet/Not proven, not converted to completed acceptance.

<!-- rpi:phase id=P02 -->
### [ ] P02: Reconcile, review and persist

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Reconcile evidence and local closeout

Depends P01-T02 including rollback branch. Update markers/details/state and
changes, preserve commands/results and independent outcomes. One independent
Review, local commits with authenticated privacy-safe identity and trailer.
Fetch main; complete local --all gate on clean committed candidate with600s
heavy-lock admission. Final external receipt only if gate completes; any later
commit invalidates it. No push, merge, issue closure or claim of human approval.

## Test Ownership and Locked Boundary

Parent owns live automation and configuration verification; no tests removed,
maximum zero source-test additions. Canonical new targets: seven tracking
artifacts; generated private helper/backups/results and local gate output
external. Possible source-document target only src/api/README.md operational
login caveat. Semantic live proof is not replaced by scripted model/unit tests.
Existing process-restart tests provide regression basis; focused unittest
test_resident_showcase.SessionTests/test_resident_demo_api restart selector,
using installed distributions, plus AST syntax/config invariant checks.
Full gate existing tools/rpi-checks.py only; no tooling bypass or cloud fallback.

## Critique Disposition

One final-candidate independent critique Complete/Pass, zero findings, preserved
at .copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan-critique.md.
No unresolved owner decision; no second critique.

## Follow-Up Items

* Human resident/content and operational acceptance remains separate; owner.
* Diagnose actual runtime fallback using existing private-perimeter telemetry
  under separate authorized access; disabled app retained. Current logs cannot
  distinguish accounting denial/failure, MSI, transport or response validation.
  Do not read the ledger or open workspace/SQL networking as a workaround.
* Coordinator must obtain a fresh exact-head/current-main complete local gate
  and independent exact-head approval before publication if unavailable here.

## Handoff

Changes .copilot-tracking/changes/2026-10-30/resident-ai-activation-563-timeout-recovery-changes.md.
P01 execution complete through rollback, actual activation Unmet.
One original Review Complete / Not accepted. P02-T01 local commit/gate pending.
No new cloud/browser/model action or repeat critique.
