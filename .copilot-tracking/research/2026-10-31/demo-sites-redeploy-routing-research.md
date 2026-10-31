---
title: Demo redeploy routing research
ms.date: 2026-10-31
---

## Research Brief and Parameters

Task 439ddfed-247a-4d5a-85ce-c60e9b939be3, demo-sites-redeploy-routing.
Focused internal convergence research for the owner's finite full RPI loop.
Evidence root .copilot-tracking/research/2026-10-31. No source edits,
new infrastructure, AI activation or private dataset inspection.
Initial targets: original/latest redeploy records, retained scripts, SQL diff,
cache policy and resident routing. No external research needed.
Repository instructions and rpi-research selected; domain design skills skipped
because this is deployment, not web implementation. Research inline because
the operational trace is tightly coupled. Interaction unavailable and brief
sufficient; no automatic follow-up session opt-in inferred.

## Direction Controls

Standing two-site redeploy authority through 2026-11-15. Verbatim ACR decision:
"Always allow a short public-access window on the ACR, but if not possible,
use `az acr build` command". Use VM/32/defaultDeny, exact restore/readback.
Resident AI OFF. Credentials only inside bounded automation, at most two
sign-ins per account. No secrets, .env, new RBAC/private endpoints/public SQL,
RG deletion or history rewrite. Latest request adds signed-in checks and PR;
explicit repeated no-push boundary remains unresolved for publishing a new
local head, so deploy/local evidence can proceed but push is not inferred.

## Prior Knowledge and Cycle 1

Wider: original 30 October record and origin/main #596 record retrieved,
then latest cache8 record and retained current adapters inspected.
Deeper: exact transitive build/publish/rollout/verify/init bodies inspected.
HEAD fast-forwarded cleanly from owner-specified 84035ae9 to fetched main
9ecb159bd843411c2e17dc2785ab59f5e837040f, including #611 and #610.
Contrarian: a local image proof failure must never compensate a healthy app;
cold-start timeout alone is not deployment failure. Protected employee assets
must retain anonymous401/302, not be weakened to meet anonymous200.
SQL diff is NOT empty: staff SQL transport and persisted recommendation SQL
reads changed, although no .sql/DDL files changed since 4cb5964f. The caller's
"touches SQL" condition therefore holds; use original narrow counts-only init,
not new transport/RBAC rollout or blanket schema application.

## Evidence Log and Findings

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md:113 | Concrete resource subdirectory fix and local/live failure separation required |
| C2 | .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md:111 | cache8 uses retained bounded IP-only publisher and exact restoration |
| C3 | src/core/src/zava_forward/core/store.py:942 | SQL-backed saved recommendation read changed since deployed source |
| C4 | infra/scripts/staff-azure-worker.py:80 | SQL initialization transport changed, not selected for deployment |
| C5 | src/api/src/zava_forward/api/resident_demo/chat.py:174 | Whole-intent natural own-case routing is in current main |
| C6 | src/README.md:68 | Complete committed exact-head local gate required before publication |

## Alternatives and Parent Decisions

Reuse cache8 adapter fixes plus #596 narrow SQL initializer: selected.
Skip init solely because .sql diff is empty: rejected, too narrow for caller.
Run new staff transport/RBAC: rejected, outside scope and forbidden new RBAC.
Public unrestricted registry: rejected; existing VM IP-only procedure available.
Fallback az acr build retained if window unavailable, not preclaimed tested.
No additional research cycle: named questions covered and sources redundant.

## Readiness

Research execution Complete; disposition executed; Planning Readiness Ready.
Remaining execution uncertainties: actual registry propagation, live startup,
test-user authentication and exact-head publication prerequisites.
Self-check: dated evidence, source pin, controls, three waves, alternatives,
residual uncertainty and parent-owned decisions recorded.
