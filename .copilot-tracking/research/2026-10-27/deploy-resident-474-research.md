<!-- markdownlint-disable-file -->

# Task Research: deploy-resident-474

| Field | Value |
|---|---|
| Date | 2026-10-27 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/deploy-resident-474-research.md |

## Research Brief

Deploy merged PR #474 to the existing isolated Azure synthetic resident site and
prove registered-resident login, own-case isolation, gauges/history, advisory
assistant, top-right sign-out and expiry. Audience: owner and independent reviewer.
Output mode: convergence, preparing deployment planning.

## Research Parameters

Focused posture, selected for a bounded deployment with named prior evidence.
Code scope: resident server/provider, existing image and infrastructure runbooks.
External scope: current ama resource metadata and official Azure capability data.
Evidence root: .copilot-tracking/. Research makes no application/cloud mutations.
Budget: additional USD30, including at most USD20 Azure OpenAI; expiry
2026-10-31T23:59Z. Only ama. All three apps min replicas 0; all eight jobs Manual.
No secrets/.env reads or output, broad grants, SQL/employee changes or new groups.

## Extension Registry and Provenance

Repository instructions and RPI research are selected. UI implementation skills
are not selected for deployment-only work; revisit if web source edits are needed.
Independent critique and Review are required later. Research stays inline because
the release is one tightly coupled evidence trace.

## User Participation and Research Decisions

The user explicitly requests all four phases in order and authorizes deployment,
managed-identity Azure OpenAI and live browser/expiry checks. No further routine
confirmation is needed. The referenced coordination SQL table is unavailable in
this session; the supplied dated owner approval is the authority, not an invented
SQL readback.

## Direction Controls

Start latest origin/main in chore/deploy-resident-474 at the requested worktree.
The supplied worktree already exists, clean, on that branch at origin/main
885ee05fc45122cf7a1ea4f7f003dc88bfda08ee; preserve it rather than recreate it.
No closing keywords. Scoped --changed gate replaces the full gate for this task.
Use timeout-zero heavy lock for builds/gates, pip not uv. Ingress test-only.

## Research Questions

1. What exact merged image/configuration and provider surface must be deployed?
2. Which current resources, budget evidence and least-privilege model route exist?
3. How can live sign-in and expiry be proved without reading credentials?
4. Which #462 criteria can be proved, and which remain historical/human gates?

## Prior Knowledge Gate

PR #474 is merged at 2fbb42f0ed80b84429fc7962eda1e04e3265e15e.
Latest main also contains #476's min-replica correction. Prior release files are
present at the owner-designated ~/.ama462-evidence/release-2026-10-26/.

## Research Cycle Log

Cycle 1, Wider: inspected merged PR/issue criteria, prior release scripts, current
ama inventory, role assignments, app configuration metadata and model inventory.
Reflection: there are FOUR existing apps, not three. All four are min 0 and all
eight jobs Manual. Preserve all four. Resident ingress starts disabled.

Cycle 1, Deeper: traced resident startup, immutable image context, topic-provider
injection, budget-reservation contract, owner-held password and 1800-second session.
Reflection: deploying #474 does not activate Azure OpenAI. Startup always injects
the deterministic provider and rejects AI configuration. No model deployment or
resident inference role exists. Existing login uses the owner's offline-held
password, unavailable to this non-interactive task without violating no-read rules.

Cycle 1, Contrarian: checked whether mere Azure model provisioning, a forged
session, a temporary password replacement or root HTTP success could satisfy
acceptance. Rejected all: provisioning without host wiring is unused spending;
forging or replacing credentials would not prove the unchanged deployed login.
The merged adapter additionally requires a durable atomic reviewed-tariff ledger,
which is not supplied. Alerts and low quota are not a USD20 hard cap.
Reflection: deploy the exact merged code, prove unauthenticated live denials and
asset identity, and explicitly leave authenticated/model criteria unproved.
No further in-scope search can supply the owner-held password or missing source
wiring. An activation implementation is a separate engineering scope, not a
deploy-only mutation eligible for the user's scoped-gate exception.

## Evidence Log

| ID | Evidence | Finding |
|---|---|---|
| C1 | src/api/Dockerfile.resident-demo:1-48 | src context, pinned base, non-root merged server |
| C2 | src/api/src/zava_forward/api/resident_demo/__main__.py:17-51 | SQL MI projection, deterministic default; no AI host injection |
| C3 | src/api/src/zava_forward/api/resident_demo/assistant.py:60-114 | Disabled adapter requires durable reservation and explicit token callback |
| C4 | src/core/src/zava_forward/core/resident_showcase.py:32-35,61-70 | 1800-second sessions and forbidden AI environment prefixes |
| C5 | docs/architecture/resident-assistant-prototype.md:39-80 | No durable ledger/activation wiring; no verified numeric tariff |
| C6 | .copilot-tracking/changes/2026-10-26/resident-release-462-changes.md | Prior positive-login/expiry gaps and ungated interim image explicitly retained |
| W1 | https://github.com/jmservera/ama/pull/474, retrieved 2026-10-27 | Merged 2fbb42f0; rubric 75 vs baseline 74 |
| W2 | Azure ARM ama readbacks, 2026-10-27 | Four apps min0; eight jobs Manual; SQL Standard/10 DTU; resident ingress null |
| W3 | Owner-designated release-2026-10-26/push3.sh and cost-ledger.txt | Approved narrow ACR route, restore prior policy; prior estimates not fresh charges |
| W4 | Azure consumption budget readback, 2026-10-27 | ama accrued USD309.49076053371493; budget alerts are not hard caps |
| W5 | Azure Cognitive Services account/deployment/role readbacks, 2026-10-27 | Existing private AIServices resource; zero deployments; no resident inference grant |

Tools: system Python lacks Playwright; dependency restoration is permitted after
that observed missing-module failure. Browser MCP is another available route.
The original coordination_state table is not present in the session database.

## Findings, Decisions and Readiness

Research disposition: executed. Planning Readiness: Ready for exact merged-code
deployment with explicit partial-acceptance boundaries, not model activation.

Selected: prefer ACR remote build without policy changes; if refused, lock-protected
local build and the approved VM-IP/token push route with exact policy restoration.
Deploy resident image only while ingress remains closed, enable only for live
checks, then disable and verify workload configuration invariants.

Unresolved: positive registered login, own-case authenticated gauges/history/
assistant/logout and natural session expiry require an owner-held credential,
which must not be read here. Model activation requires new reviewed host/ledger
engineering. Neither is silently waived or counted as passed.

Cost admission: the owner's NEW additional USD30 allocation is the fresh task
headroom, not the expired USD50 or old USD5. Reserve at most USD1 for a bounded
build/test window, retain USD20 unspent for blocked model work and USD9 headroom.
Use local build if remote service unavailable; no new paid resource. Record actual
operations/duration and unknown delayed charges, not fabricated zero billing.

Self-check: all three waves completed in order; alternatives, direct evidence,
caller boundaries, uncertainties and parent-owned readiness recorded.
