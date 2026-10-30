<!-- markdownlint-disable-file -->
# RPI Changes: deploy-resident-474

## Metadata

Date: 2026-10-27. Task ID/slug: deploy-resident-474.
Plan: .copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md.
Details: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md.

## Execution Status

Full plan declared. Implementation outcome Partial: P01 and P02 execution complete;
P03 original Review/publication remains. No application/test source changes.
B1 authenticated credential-dependent proof and B2 Azure runtime/ledger remain
blocked and are not accepted as completed requirements.

## Execution Summary

One independent final-candidate critique returned Revise. Parent applied all
PC-001 through PC-008 before mutation; the original critique is retained.
User-authorized independent exact merged-image deployment may proceed, but
full requested acceptance remains unavailable.

## P01-T01: Pre-mutation admission

Fresh owner's USD30 is a new allocation. Retain USD20 for model work and USD9
contingency, reserve USD1 for this bounded release/test.
Azure retail API (https://prices.azure.com/api/retail/prices, uksouth,
Container Registry / Azure Container Apps, retrieved 2026-10-27) returns:
ACR task USD0.0001/vCPU-second; ACA USD0.000034/vCPU-second,
USD0.000004/GiB-second, USD0.40/million requests. No free grant assumed.

Admit one remote build, 2 vCPU * 600s * 0.0001 = USD0.12; terminal cancellation
required after timeout. Local fallback adds no Azure build run. At most two
startup-overlapping resident revisions for 2400s:
2 * 2400 * (0.25 * 0.000034 + 0.5 * 0.000004) = USD0.0504.
At most 1000 test requests = USD0.0004. Reserve the remaining USD0.8292 for
bounded metadata/registry/vault/logging/egress ancillary operations, not a quoted
tariff or hard cap. No model deployment/calls/roles are admitted. Actual billed
charges remain delayed/unknown, not zero. Stop if remote status or budget becomes
unknown; no silent consumption of model allocation.

## Validation Record

No live check has run yet. Missing system Playwright observed; restoration may
use pip in an external venv. Scoped evidence-PR gate is distinct from fresh
image scan/contracts and authenticated acceptance.

## P01-T01: Image release completed

ACR attempt one failed local Dockerfile lookup before queueing. Corrected CLI path
queued the single admitted run dbf, 2 CPU, 2026-10-27T09:12:03.743491Z to
09:12:15.735447Z, terminal Failed: private registry login 403. No network policy
was changed for that remote attempt. Estimated ACR task charge <=USD0.0024.

Timeout-zero heavy-lock local Docker build passed. Exact image/source label:
885ee05fc45122cf7a1ea4f7f003dc88bfda08ee. Trivy0.76.0 with fresh external DB,
src/trivy.yaml, ignore-unfixed HIGH/CRITICAL exit1 passed with zero fixable findings.
Fresh contracts passed: UID10001, no packaged working dataset, all resident assets
packaged/readable, read-only root/cap-drop/no-new-privileges invocation and missing
configuration refuses startup. No live secret or SQL data used in contracts.

The approved expose-token/VM-IP ACR push succeeded. Exact canonical ACR restoration
passed: public Disabled, exports disabled, bypass None unchanged,
defaultAction Allow, no IP or virtual-network rules. Cleanup status successful.
Original build, scan/DB, image-contract, digest and push/restoration evidence lives
externally in the session files/deploy-474 directory.

## P01-T02: Resident revision updated

Image-only az containerapp update succeeded while ingress remained null. Digest:
sha256:0568deb725e7258c3b09d425b6c0a28a736a2e23434fc22c350bac6333888043.
Revision ca-resident-demo--0000002 became latestReady and Healthy before exposure.
Resident min0/max1 retained. No Bicep, role, SQL, credential or employee update.

## P02-T01: Live-test opening

Use an externally stored Playwright harness with no owner password. Arm an
independent owned 30-minute closure watchdog and verify PID before ingress.
The harness always disables ingress, verifies ARM null and external non-service,
and only then terminates that specific watchdog. No authenticated pass will be
claimed from fabricated cookies or merged asset identity.

## Required merged-view deployment discovered by real startup

The first live attempt FAILED readiness; no browser pass was obtained. Console
classification yielded only "Refusing to start: SQL read failed (ProgrammingError)."
System events confirmed restart loops despite ARM reporting Healthy/latestReady.
Ingress was closed by cleanup and external root returned404. Original failure
is retained externally in live-result.json, not overwritten.

Root-cause trace: merged resident_showcase_sql.py selects sixteen columns, while
the previous release applied the pre-sensor fourteen-column view. The merged
infra/sql/resident-showcase.sql already supplies the compatibility view.
P01-T02 is reopened until actual application health. Apply only that merged view
batch transactionally through an execution-only override of the existing Manual
initializer and existing SQL admin MI. This is a required deployment operation,
not new source engineering, credential work, data migration, permission grant or
SQL sizing change. The earlier blanket "no SQL writes" was over-narrow planning;
the precise boundary now permits only this published projection DDL while
preserving all business data and SQL permissions. No user approval is invented.
Additional compute bound <=USD0.0126 within release allowance. All other scope,
critique history, blockers, test ownership and source SHA remain unchanged.

Existing initializer execution job-cutover-test-init-4ws8vuw Succeeded,
09:25:53Z to09:26:30Z. Its transaction verified existing principal SID, no extra
rights, fourteen old columns, applied exact merged view batch SHA256
d55376da6fe3b6131c261d342a4aa10b55d3b406b172818e2d6b6eeba02dcdc3,
verified sixteen expected columns and unchanged permissions, then committed.
Receipt explicitly reports no case-data read and no table/row/grant change.
Existing job definition/identity remained untouched; only this execution's
container command was overridden. Compute estimate <=USD0.000777.

## Implementation-Time Updates

All eight critique findings applied as compatible safety clarifications.
No new user decision, source/test changes, second critique or acceptance waiver.

## Blockers and Remaining Work

Owner-held shared credential is unavailable under the no-read rule. Positive
login, own-case authenticated gauges/history/assistant/logout and natural
session expiry must not be represented as passed.
Azure OpenAI activation needs reviewed MI host wiring and atomic durable
USD20 ledger; retain deterministic provider and do not spend on an unused model.

## P02: Actual live evidence and final stop

The second live attempt passed27 actual HTTPS/Playwright checks. Tests prove
sign-in UI/limitations/labels, no anonymous case content, generic invalid and
unknown login denial, CSRF/cross-origin denials, unauthorized view/assistant and
case-selector denial, four absent employee routes, forged expired-looking cookie
denial, security headers, byte-exact four merged assets, header-contained Account/
sign-out markup, 320px anonymous reflow, real invalid-login UI and no script errors.
They do NOT prove registered login, rendered authenticated features or natural
expiry. Forged-cookie denial is explicitly not expiry proof.

First window09:17:54.511847Z to09:24:09.399877Z (failed startup). Second
window09:27:30.672831Z to09:28:13.101355Z (passed available checks).
Both independently watchdog-protected, HTTPS-only and closed with ingress null
and external404. After closure min0 still had one running resident replica, so
only tested revision0000002 was deactivated. Final active=false, replicas0,
running=Stopped, deployed image retained. No always-on resident compute intended.
All four apps min0; eight jobs Manual; three non-resident safe app projections
unchanged; SQL Standard/10 DTU; resident SQL principal permissions unchanged;
exact ACR policy equality. Employee interactive login was not tested.

## Cost ledger and evidence retention

Committed sanitized machine receipts:
.copilot-tracking/changes/2026-10-27/deploy-resident-474-evidence/.
Cost ledger distinguishes USD1 reservation, individual rate-based estimates,
no model operations, delayed unknown billing and baseline spending.
Compute/request estimate upper subtotal USD0.053977 excludes unknown ancillary
charges within the release allowance; it is not an invoice or hard cap.
Original raw outputs, two anonymous screenshots, scripts, fresh scan/DB and
original failed attempt are preserved at
~/.ama462-evidence/release-2026-10-27-474/ with committed hashes.
No historical evidence was deleted. Full all-severity report attempts were
blocked by another task's heavy lock; exact-image blocking scan passed.

## Issue 462 criterion mapping

| Original criterion | This deployment's evidence | Status |
|---|---|---|
| Prospective RPI plus threat model | Research/plan/details/one critique preceded mutations; original Review next; earlier threat model not regraded | Partial |
| Dependencies and unchanged rubric gates | #474 merged, hosted rubric75 vs74; no bypass or manual score edit; no whole historical dependency reassessment | Partial |
| Resident identity, negative access, staff/canaries and employee login | Actual anonymous/forged/selector/staff-route denials; genuine login/cross-resident/canary/employee journeys not run | Partial |
| Secret/session/abuse controls | Existing MI/vault references preserved, no secret read; actual CSRF/origin/header denials; authenticated cookies/expiry/abuse not fully tested | Partial |
| SQL/image/browser/local/hosted gates | Actual view transaction, non-root image/refusal and27 live checks; scoped evidence gate follows; historical source gates not fresh full gate | Partial |
| Authorized finite cloud/cost boundary | Supplied fresh USD30, preflight/rate admission/ledger; existing ama only, no roles/groups/endpoints, SQL sizing unchanged; billing delayed | Scoped operational evidence |
| Actual HTTPS/login/isolation/browser deployment | Real HTTPS200 and merged asset parity; actual login and authenticated isolation unproved | Partial |
| Identity/URL/limits/resources/expiry/stop | Exact source/digest/revision, URL, preserved resources, expiry and stopped/closed final state recorded | Scoped evidence; not whole issue acceptance |

No whole-issue acceptance, human approval or production/WCAG acceptance is claimed.

## Pre-Review Reconciliation

P01/P02 markers and phase details current; original startup failure preserved.
P03 publication remains pending. Documentation/index/log updated with current
authorization and explicit partial delivery. B1/B2 stay open, canonical follow-ups
remain in the plan. Ready for one independent original Review of this boundary.

## Original Review and publication preparation

The one independent Review executed Complete; deployment execution Partial;
full-task outcome Not accepted. RV-001 retains genuine authenticated/expiry
acceptance; RV-002 retains MI/model/ledger engineering. No full-service acceptance
or second Review is claimed.

RV-003 identified a narration typo: actual before/after ACR bypass is None, not
AzureServices. The publication-preparation sentence above is corrected to the
unchanged raw receipts; no cloud policy change or Review regrading occurred.
The original Review, original adverse startup/build evidence and all raw hashes
remain unchanged. The separate final exact-head publication assessment must
evaluate the committed evidence candidate; it is not another RPI Review.

P03 commit, --changed receipt, exact-head assessment and PR remain external
publication steps. A passed partial receipt will not imply service acceptance.
