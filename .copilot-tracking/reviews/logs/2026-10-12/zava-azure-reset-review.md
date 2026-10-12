---
title: Zava Azure Reset and Naming Review
description: One review of the implemented reset, rebuild and remaining tenant acceptance gate
ms.date: 2026-10-12
---

## Scope and evidence

* Task ID: `zava-azure-reset-2026-10-12`.
* Scope: owner-authorised reset/rebuild, fixes, names/references and explicitly
  partial live acceptance; no broader agent implementation.
* Plan: .copilot-tracking/plans/2026-10-12/zava-azure-reset-plan.md
* Details: .copilot-tracking/details/2026-10-12/zava-azure-reset-phase-details.md
* Changes: .copilot-tracking/changes/2026-10-12/zava-azure-reset-changes.md
* State: .copilot-tracking/rpi-sessions/2026-10-12/zava-azure-reset-state.json
* Critique/research: no separate new artifact; owner-directed execution reused
  the tested migration and deployment contract. No fresh critique is claimed.
* Source boundary: new deployment/token/test diff from `23e1376` to `9ab3c19`,
  current rebuild documentation and compiled naming/link/deployment evidence.

## Opening review state

The goal is to assess the rebuild and identify unmet acceptance, not silently
close the tenant gate. Plan/details/changes are reconciled. P01 and authorised
P02-T01 checks are complete; P02-T02 review/publication is the final boundary.
The source/evidence boundary is read-only; only this review record is writable.
The existing API registration cannot be read/managed by the available operator.
Compare deletion scope, deployment outcomes, workload identity/model access,
names/references and the remaining signed-in browser gate.

## Execution status

Execution: Complete. One comparison was executed on 2026-10-12. Complete review
execution does not mean complete migration acceptance.

## Plan-to-change reconciliation

| Marker | Evidence and reconciliation | Assessment |
| --- | --- | --- |
| P01-T01 | Frozen inventory, private credential/mapping capture and identity classification; private locator is empty after transfer/seed | Reconciled |
| P01-T02 | Generic ARM and consumption-budget indexes empty before foundation; group/operator retained; old workload identities removed | Reconciled |
| P01-T03 | Both group deployments succeeded; real image, new SQL grants/fixture and protected ingress | Reconciled |
| P02-T01 | Health/auth-denial, identity-backed SQL/model calls and revision-restart durability passed; signed-in browser checks explicitly blocked | Partial acceptance is accurately bounded |
| P02-T02 | Naming/link/deck evidence assessed; final publication follows this review | Review complete; delivery metadata pending |

## Completed work assessment

The conditional application module and guarded alerts/output implement a real
foundation-only bootstrap, rather than exposing a placeholder workbench.
Explicit API model access/configuration preserves the separately proposed
runner default. The token change selects the actual user-assigned API identity;
both unit tests and real workload model calls support that behaviour. The role
override preserves external issued claims without pretending to rename them.

All 67 generic live resources are free of old-brand names; the separately
indexed budget is `budget-forward-test`. The real API image/HTML has the new
names. The final scan has zero text/path replacements. Its five binary
candidates are logo refreshes, not residual names: all five decks' paragraph
text has no old-brand matches. Previously validated five-deck/61-source assets
were not changed by this reset, so reuse their visual evidence.

Changed-document fragments and relative targets pass. Eight pre-existing
actual target defects remain; the earlier raw baseline included two code-example
placeholders. No new missing target was introduced. Historical snapshots,
append-only log history, preserved external URLs and tenant-issued role values
are distinct, documented exceptions.

## Implementation-time updates and critique assessment

Service deletion ordering and separately indexed budgets were immediately
relevant corrections preserving the authorised scope. Foundation/application
staging and the opt-in real model path fix tightly coupled cold-start and runtime
gaps; no case authority, consent or workflow decision right changed. Plan and
details record the deletion corrections and remaining acceptance gate.
No unaccepted significant decision or repeated critique was introduced.
No fresh independent planning critique is claimed for this owner-directed reset.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Tenant transition and authenticated browser acceptance remain open

* Scope: P02-T01 and full migration acceptance.
* Evidence: Azure Graph app read still returns `Insufficient privileges`;
  tools/rename-zava.md records the new callback and retained role-value mapping.
  API/browser auth entry is protected, but no interactive session was tested.
* Impact: successful sign-in, scoped My cases/All cases and rendered map/tiles
  are not proven. Tenant role/name migration cannot be declared complete.
* Destination: distinct tenant-owner follow-up, followed by `rpi-implement`
  for the remaining authorised acceptance/configuration work.
* Smallest next action: authorised owner adds the documented callback while
  preserving redirects/assignments, completes the role/name transition, then
  verifies real browser login, 443 open cases, scoped lists and map/tiles.
  Remove the transitional map only after replacement claims are issued.

## Defects and routed findings

No new implementation or reference defect was found in the assessed boundary.
RV-001 is required residual work, not an auth bypass recommendation. Existing
worker placeholders and planned Decision 1 scoring are outside this reset;
neither is presented as implemented. Existing link defects remain out of scope.
No fresh research or planning handoff is required.

## Validation evidence

| Evidence | Status | Result or boundary |
| --- | --- | --- |
| Foundation/application group deployments | Passed | Both succeeded after verified empty reset |
| Public probes after rollout/restart | Passed | Health 200, API 401, browser/login entry 302 |
| API workload SQL/model probes | Passed | 980 cases / 443 open; SQL writes; standard/capable both `source=ai` |
| Actual revision restart | Passed | SQL and per-model audit entries persisted |
| Deployed HTML and cloud naming | Passed | New names; no old generic resource names |
| Migration regression suite | Passed | 21 tests |
| MVP suite | Passed | 272 tests, 26 existing skips; two new identity regressions |
| Bicep compilation/diff check | Passed | No warnings or whitespace defects |
| Markdown targets/changed fragments | Passed within change boundary | No new failures; eight pre-existing actual target defects |
| Five PPTX text and existing render evidence | Passed / reused | No old-brand paragraph text; no deck change during reset |
| Interactive Entra/lists/map | Unavailable | Tenant owner callback/role action required; no substitute evidence claimed |

## Outcome and routing

Outcome: Residual work. Reset/rebuild, workload SQL/AI and active repository/cloud
branding are supported. Full migration acceptance is not complete while RV-001
remains open. Review is executed once; later tenant/acceptance work does not
require repeating this task's Review.

Final delivery remains publication to the existing open #65 and its checks.
The single supported ranked follow-up is tenant transition plus signed-in
acceptance, because it clears the actual remaining user-visible gate.
