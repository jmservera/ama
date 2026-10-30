---
title: Resident AI 563 owner-enabled activation plan
ms.date: 2026-10-30
---

Task ID: 563-owner-enable-20261030T1710Z.
Slug: resident-ai-activation-563-owner-enable. Parent: 563/resident-ai-activation-563.

## Executive Summary

Bounded activation was attempted using only the two documented variables and
the existing account-scoped MI. Owner monitors cost and waives the live ledger
pre-read; runtime admission/USD20/November1 expiry remained untouched.
Disabled/denied/consent baseline passed. The ready enabled revision passed
configuration checks, but post-deploy authenticated browser verification timed
out without an observed model response. Both variables were removed and exact
effective backed-up configuration restored in a fresh ready revision100%.
Activation acceptance remains Unmet. Two sign-ins exhausted; no further login.
Independent Review Complete / Not accepted, local candidate committed.
Full local gate blocked after600s shared-lock timeout; no receipt or pass.
Final evidence-only local closeout records that outcome; no push.

## Sources

Research C1-C10:
.copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md.
Details:
.copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md.
Previous resident-ai-activation-563 artifacts remain historical and unchanged.

## User Decisions and Requirements

* Owner decision 2026-10-30T17:10Z, verbatim: "Enable AI, I will take care of checking the cost and will warn you if there's a problem".
* No live cost-ledger read required; no SQL public access or SQL migration.
  Keep configured USD20 ceiling and exclusive 2026-11-01 pilot expiry.
  Redeploy authority remains through 2026-11-15.
* Only ca-resident-demo / RG ama and existing aoai-resident-469/resident-mini.
  Use existing narrow MI role, no keys, employee app changes or new resources.
* Exact current app backup before mutation; only needed env/secretrefs;
  min replicas0, every job Manual, never delete ama.
* Live consented pest answer with AI label, collapsed sources, out-of-scope
  rules/manual route, safe unconfigured/denied path; rollback on failure.
* Credentials inside automation only, no logs/screenshots/commits; at most
  two sign-in attempts. Warm health with long timeouts/retries.
* Ordered full RPI loop with dated artifacts, local commit with required
  trailer and Refs #563 only; no push.
* Heavy lock /tmp/ama-rpi-heavy.lock only for local gates, flock -w 600.

## Goals

Demonstrate actual resident AI under unchanged authority and safeguards,
or restore the exact baseline and report a precise runtime blocker.

## Scope and Non-Goals

Resident environment configuration, private evidence helpers and dated RPI
evidence only. No source/UI edits, ledger reads/writes/migration, role changes,
keys, job execution, networking changes, endpoints or resource groups.
No employee app mutation; read-only before/after preservation projection allowed.
No human/content/WCAG acceptance or completed-issue claim.

## Functional Requirements

FR1: Back up exact app show, revision list, auth show and jobs list privately,
mode0700/0600; hash bytes. Capture employee configuration hash read-only.
No secret retrieval; returned secret references/metadata suffice since unchanged.
FR2: Prove health and anonymous denial, one real form sign-in, client no-consent
no-request and server no-consent400; pre-change disabled repair label/manual route.
FR3: Set exactly ZF_DEMO_ASSISTANT_ENABLED=true and
ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com.
Re-read and compare template modulo these two vars and revision suffix,
app-wide config, identity, auth and jobs.
FR4: Warm /healthz with180s timeout and up to three attempts/delay. Use the same
browser session after reload; at most two login submissions across all runs,
one intended, no blind password retry. Submit one consented synthetic rat
question and one out-of-scope question (capital of France).
FR5: Require actual200 AI-generated reply, relevant pest acknowledgement,
explicit uncertainty/no invented diagnosis and housing-officer route,
host-known sources and collapsed Sources. Measure thin label geometry per
existing browser check. Out-of-scope must be labelled rules with task limit
and manual route, not AI. No mocks or browser interception.
Compare each factual/process claim to the actual in-memory limited case
projection and host repair guidance. Unsupported or indeterminate claims,
including invented visits, timing, contacts or reporting, fail verification.
Retain only safe claim/source categories, decisions and sanitized prose;
do not export the underlying private projection.
FR6: On failure after update starts, restore backed-up original env using
surgical removal of the two previously absent variables. Require baseline
effective template modulo suffix, config/identity/auth/jobs, ready restored
revision100% traffic and health. Retain failed candidate evidence.
Azure Single mode does not permit targeting old revision traffic; restoring
identical effective configuration in a fresh ready revision is the supported
route, not a reason to change revision mode. SDK-added empty value alongside
an unchanged secretRef is ignored only for effective-env comparison.
If surgical restoration cannot establish equality, use the protected backup
to restore template; do not broaden resource/secret changes. Restoration
failure is an explicit urgent blocker, never success.

## Non-Functional Requirements

No credential/token/cookie/request-header/payload output. Browser recording,
screenshots, tracing, HAR, video, storage-state exports and debug logs off.
Mask both login fields, clear after submission, disable core dumps and sanitize
exceptions to stage/type/status only. Raw configs private external files only.
Every operational command/HTTP result recorded via sanitized argv/time/exit and
checks; bounded synthetic answer text may be retained after secret exclusion.
Only one actual paid question planned; maximum two only for a documented
non-inference transient, never repeat a deterministic fallback.
No automatic inference retries or cost/expiry bypass.
Runtime reservation denial or SQL failure is a verification failure requiring
rollback; owner monitoring does not authorize unmetered transport.

## Acceptance Criteria

AC1: Exact fresh private backup hashes and safe restoration route established.
AC2: Live disabled/unconfigured, anonymous denied and no-consent checks pass.
AC3: Actual consented grounded AI answer, thin AI label and collapsed sources;
claim-to-source comparison supports every factual/process claim. Unsupported
or indeterminate grounding fails AC3 and requires restoration.
AC4: Actual out-of-scope rules fallback/manual route.
AC5: Only intended two-variable delta; image/MI/auth/secrets/min0/jobs and
employee configuration unchanged. If AC3/4 fail, exact restoration proven
and activation explicitly Unmet, not an accepted substitute.
AC6: One critique with dispositions, one independent Review with original
outcome preserved, local commits/trailer/no push, full local gate actual result.
Human acceptance remains unchecked.

## Phase Checklist

<!-- phase: P01 -->
### P01: Preserve and activate

* [x] P01-T01: Restore missing pinned browser tooling externally and back up configuration.
* [x] P01-T02: Warm and capture disabled/denied/no-consent baseline in one browser session.
* [x] P01-T03: Apply only two variables, warm and verify actual AI/out-of-scope; restore on failure.

<!-- phase: P02 -->
### P02: Reconcile and persist

* [x] P02-T01: Reconcile exact configuration, live evidence and limitations.
* [x] P02-T02: Execute one independent Review, commit locally and attempt full external gate.

Dependencies: P01-T02 follows T01; T03 follows T02. P02-T01 follows T03 including
mandatory restoration on failure; P02-T02 follows reconciliation.
The first baseline passed with one sign-in; no model call occurred before a
strict env serialization assertion stopped rollout. Original attempt retained.
A second bounded attempt corrects only equivalent secretRef serialization and
requires actual new-revision readiness before live verification; two total
sign-ins maximum remains binding.
P01 execution complete through mandatory restoration, not successful activation.
P02-T01 original-to-final effective template/config/identity/auth/jobs equality
is proven; employee templates/config/identity also unchanged. P02-T02 execution
complete: original Review Not accepted; local commit433daef9; full gate
attempt blocked on600s shared-lock timeout, no receipt. Human acceptance
unchecked. Completed execution does not meet activation AC3/AC4.

## Test Ownership and Locked Boundary

Owner: parent operations executor. Source/test removals: none. Source/test
additions: zero. Canonical targets: new dated RPI artifacts only.
Generated targets: private external helpers/config backups/results/browser
runtime and full-gate output. Regression: exact normalized config equality,
unchanged image/auth/jobs/employee. Semantic: live actual AI relevance and
host-known grounding, not scripted model. No local mocked response replaces
live proof. No screenshots. Full gate after original Review and candidate
commit, new external output; use existing runner, bounded600s heavy admission,
no foreign-process interruption. Gate failures remain publication blockers.
No source change means focused source suites are not a proxy for live checks.

## Critique Disposition

Exactly one independent critique executed, original verdict Revise, two Medium
findings preserved in the critique artifact.
PC-001 applied: explicit claim-to-source comparison against actual in-memory
host guidance/case projection, safe evidence categories and fail-to-rollback.
PC-002 rejected: its premise that this execution prohibits temporary-directory
operations is not present in the parent execution boundary. The owner expressly
requires /tmp/ama-rpi-heavy.lock, and the repository's existing gate uses that
shared lock with native600s bounded admission. No substitute lock or tooling
edit is authorized or needed. Keep actual gate failure/unavailability explicit.
No significant unresolved owner decision; no second critique.

## Follow-Up Items

1. Investigate post-redeploy authenticated browser timeout using finer
   stage/status evidence and a separately authorized sign-in allowance.
   No observed enabled-model response or out-of-scope proof in this task;
   exact source of timeout unknown. Runtime admission remains uninspected.
2. Human review of real generated content and operational/resident acceptance
   remains distinct from structural/browser proof.
3. Coordinate a later free heavy-lock slot and run the complete exact-head
   local gate. Current attempt blocked before checks, no receipt. If earlier
   SQL integration setup failure recurs, resolve locally, never live SQL/
   skip tokens as a substitute.
4. If runtime admission fails, separately authorize investigation/migration
   in the private SQL environment; do not resume the waived pre-read blocker
   or broaden this task.

## Handoff

Full ordered RPI execution and local closeout complete, actual activation
Unmet. Original critique Revise and Review Complete / Not accepted preserved.
Full gate Blocked, no eligible receipt. No additional login/model attempt,
source correction, repeated Review or push. Automatic session remains at
Follow-up awaiting an authorized next selection; no child started.
Changes destination:
.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-owner-enable-changes.md.
