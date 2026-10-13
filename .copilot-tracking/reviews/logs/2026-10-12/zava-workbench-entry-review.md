---
title: Public Welcome and Entra Account Review
description: One post-implementation Review with explicit human acceptance boundary
ms.date: 2026-10-12
---

## Scope and Evidence

* Task ID: zava-workbench-entry-2026-10-12.
* Review date: 2026-10-12.
* Scope: Full supplied task comparison; no claim of unavailable human acceptance.
* Plan: .copilot-tracking/plans/2026-10-12/zava-workbench-entry-plan.md.
* Details: .copilot-tracking/details/2026-10-12/zava-workbench-entry-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-12/zava-workbench-entry-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-12/zava-workbench-entry-changes.md.
* Research: .copilot-tracking/research/2026-10-12/zava-workbench-entry-research.md.
* Source: 15e8158, publication state 80d4a47, continuing PR #65.

## Opening Review State

Compare requested public entry, protected data, real own-photo integration and
account controls against source, deployment and validation. All canonical
artifacts are present and reconciled. The acceptance basis is the plan's
functional/nonfunctional requirements, acceptance criteria and five disposed
critique findings. Read-only source/evidence; write only this Review record.
The owner is unavailable for fresh legitimate photo/consent/switch acceptance.
Keep that gate open; assess its absence instead of inventing a browser session.

## Execution Status

Execution Complete. One Review only; no repeat of the prior
zava-entra-acceptance Review.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01 welcome/account | Public root, exact platform exemptions, explicit Microsoft entry, native account panel, fixed own-photo proxy | Implemented; rendering defect RV-001 |
| P02 token store | Actual scoped grants, key-disabled private container, five-day renewal, staged activation | Source/deployment reconciled |
| P03 tests/deploy/publish | 284 MVP, 15 initializer, 22 migration tests; current-head CI/image/SQL and live boundaries | Technical checks pass; success-photo rendering coverage was missing |
| P03-T02 acceptance | Fresh real-user photo/consent/switch unavailable | Correctly unchecked; RV-002 |
| Follow-ups | Prior tenant naming/roles retained | Outside this UI scope, not silently accepted |

## Implementation-Time Updates and Critique Assessment

PC-001 exact platform exemptions verified live. PC-002 container/single-secret
grants verified from real inventory. PC-003 retained dedicated-account isolation
because existing evidence identities have account-wide Contributor.
PC-004 credential/auth error coverage prioritized, 13 test additions remain
within the cap. PC-005 versionless rotation/refresh supported in platform
documentation and deployed config; synthetic expiry executes refresh once.
Targeted activation reused identical module parameters instead of redeploying
unchanged foundation. These updates preserve the approved intent.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: CSP blocks the new photo's Blob object URL

* Scope: P01-T02, real-photo acceptance.
* Evidence: app.js uses URL.createObjectURL for the proxy photo; server.py
  restricts img-src to self/data/map host without blob:. A live Chromium
  check using only the public Zava logo as binary input reproduced image
  load failure under the actual CSP, independently of a personal photo.
* Impact: Even a successful delegated Graph request cannot show the picture.
  Error/initials tests passed but did not cover a successful photo display.
* Destination: Later rpi-implement in a distinct necessary repair task.
* Smallest action: Add blob: only to img-src, retain other directives and
  add a regression plus successful live binary-image rendering check.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Real-user photo, consent and switching remain unaccepted

* Evidence: The legitimate acceptance form reports owner unavailable.
  Administrative Graph login is not a workbench browser session.
* Impact: No evidence yet of that user's delegated token/photo or actual
  account chooser/logout experience. Missing photo versus missing consent
  must not be inferred from synthetic fixtures.
* Destination: Distinct owner acceptance follow-up.
* Smallest action: Fresh legitimate sign-in after deployment and confirm
  account photo/status plus sign-out/account selection. No credentials shared.

## Validation Evidence

| Scope | Status | Boundary |
| --- | --- | --- |
| Unit/API | Passed | MVP 284, 26 existing skips; initializer 15; migration 22 |
| Infrastructure/JS | Passed | Bicep build/lint and JS syntax |
| Exact-head CI 80d4a47 | Passed | MVP test/image/security/SQL, MVP and prototype validation |
| Real Azure | Passed | Both deployments; real renewal; scopes, grants and latest-ready revision 0000003 |
| Anonymous/browser welcome | Passed | Real logo, root/assets 200, no data requests, mobile no overflow |
| Photo success display | Failed | Actual CSP rejects a synthetic public-logo Blob URL |
| Personal photo/consent/switch | Unavailable | Owner unavailable; no forged principal/session |
| New rubric scoring | Pending | Separate non-regression/capstone process; not completion evidence |

## Defects and Routing

RV-001 is one implementation defect, routed to a distinct repair loop.
RV-002 is residual owner acceptance, not a code defect. Prior registration
display name proper-warm-api and ProperWarm role bridge remain the separate
tenant migration follow-up already recorded by the plan.

## Outcome

Outcome Defects found. Technical source/deployment checks passed, but real
binary image rendering reveals a blocking CSP defect. Do not call the UI
conformant. Fix in the user-authorized necessary repair loop, not by changing
source during this Review or repeating it. Preserve real-user acceptance
as a later gate. The prior Review is not rewritten.
