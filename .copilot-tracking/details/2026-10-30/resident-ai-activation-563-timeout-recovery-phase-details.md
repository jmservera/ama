---
title: Resident activation timeout recovery phase details
ms.date: 2026-10-30
---

## Metadata

Task563-timeout-recovery-20261030, slug resident-ai-activation-563-timeout-recovery.
Plan .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md.
Research same slug under research/2026-10-30, evidence C1-C9. No research gap.

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete via verified rollback, activation Unmet | T01 backup/activate; T02 live/rollback |
| P02 | Complete; publication gate blocked | T01 reconcile/review/local persistence/gate |

<!-- rpi:phase id=P01 -->
## P01: Preserve and activate safely

Context: process nonce invalidates session and CSRF at restart; prior helper
waited for content after reusing an old session. No model failure inferred.
Boundaries: resident two-var update only, no image/security changes.
Expected evidence: exact backups/hashes, healthy latest==ready/100%, actual fresh
login and AI/rules proofs, or restored baseline and precise failing substep.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Back up, validate helper and activate

Create credential-safe external helper with stage/request persistence,
four-attempt counter, strict invariant check and supported rollback; syntax
check before execution. Exact app/auth/revision/job and read-only employee
baseline bytes saved privately0700/0600. Validate original expected image,
absent enable/endpoint, min0 and Manual jobs. Apply only README two vars.
Ready polling10minutes and warm health240s/retry3; no login until ready.
Normalize only unchanged secretRef inert empty value for equality.
Completion: backups exist before update, actual permitted delta and readiness
passed. Failed mutation/unknown state invokes rollback, not credential probing.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Fresh-session live proof or rollback

Depends T01. New browser context after ready/warm; anonymous403, no-consent
client no-request/server400. No trace/HAR/video/screenshots/storage export.
Persist counter before submit; <=4 new submissions, stop on401/429/unknown.
Never reuse session across rollout; detect sign-in/error instead of waiting
blindly for content. Record POST dispatch before response, no request bodies.
One pest inference and one out-of-scope request, no inference retry. Compare
actual answer to in-memory own-case/host guidance; known source descriptions,
thin geometry, collapsed sources and manual/advisory limits required.
Credential/private-field exclusion precedes safe evidence persistence.
Completion: actual AI and rules/consent checks pass and leave enabled, OR remove
two vars and prove restored effective baseline, fresh ready100% and health.
Rollback is safe completion of execution, never acceptance of activation.
Any exception sanitized with exact last stage; rollback failure urgent blocker.

Completion evidence: first run fresh-login response200 hit an asynchronous UI
waiter race before content; failed closed and restored baseline. Preserved
second run waits correctly, login200 and own-case200, client no-consent no-request,
server400. Consented pest POST200 in3.915s rendered explicit AI-unavailable/
usage-limit rules fallback; no retry or actual AI claim. Mandatory rollback
verified all invariants and ready100% recover-safe-180814. Total2/4 sign-ins.
Thin label/AI grounding/out-of-scope Not proven because AI check failed first.
Direct first-original-to-final template/config/identity/auth/jobs/employee
comparison passed. No forbidden cloud mutation.

<!-- rpi:phase id=P02 -->
## P02: Reconcile, review and persist

<!-- rpi:task id=P02-T01 -->
### P02-T01: Reconcile evidence and local closeout

Depends P01-T02. Preserve earlier evidence; record all research/implementation
commands, argv/status/time/hash for automated cloud commands and each HTTP stage.
Reconcile plan/details/state/changes and actual acceptance before one independent
Review. Review is read-only except its exact output; no further cloud/browser/
credentials/SQL actions. Route findings to later work, do not repeat Review.
Authenticate gh account and set local privacy-safe author/committer identity;
commit original RPI evidence and implementation with Refs #563 only and trailer.
Fetch origin main and attempt full --all gate externally using flock-w600
admission only; existing runner owns shared lock, do not double-lock it.
If blocked retain exact error/no-receipt and commit evidence-only closeout.
Any later commit invalidates previous passing receipt; no publication here.
Expected completion: local persistent evidence, independent outcome and truthful
gate status; required human approval never checked off.

Immediate implementation refinement: await post-login content/error rather
than pre-login form visibility; no intent/security change or new critique.
Focused core/API restart regressions passed2/2; text-bearing local Chromium
waiter fixtures passed delayed render0.311s and explicit sign-in error, no live
login/model. Initial wrong API class selector and empty-text fixture failures
preserved in changes. Existing private workspace log access denied by perimeter;
no public access/role changes attempted. Remaining runtime failure diagnosis is
later work, not permission to replay inference with remaining two sign-ins.

One original independent Review Complete / Not accepted; RV-001 later research,
RV-002 scheduled parent local persistence/full gate. P02 remains active until
local commit and actual bounded gate result are recorded. Review outcome stays
historical; no second Review or operational correction in this task.

Scheduled local closeout now executed: candidate e3adbdbd persisted all original
evidence. Reviewed newly fetched main b9c6561a (prior PR #576 merged externally,
no relevant source/tool drift). Literal flock-w600 gate admission timed out
18:15:46-18:25:46UTC, exit1; native full runner not admitted, no groups/receipt.
P02-T01 complete as execution/evidence closeout, not successful validation or
activation. Final evidence-only local commit follows, no push. Coordinator
must obtain fresh exact-head/current-main gate and independent exact-head
assessment for successor publication; no receipt verification possible here.
