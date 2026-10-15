---
title: Issue 150 implementation review
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Scope and Evidence

Task ID: 150. Slug: src-design-system-150. Review date: 2026-10-15.
One post-implementation Review of the full supplied task boundary, distinguishing
the delivered partial foundation slice from completion of issue #150.

* Plan: .copilot-tracking/plans/2026-10-15/src-design-system-150-plan.md.
* Details: .copilot-tracking/details/2026-10-15/src-design-system-150-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-15/src-design-system-150-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-15/src-design-system-150-changes.md.
* Research: .copilot-tracking/research/2026-10-15/src-design-system-150-research.md.
* Evidence: actual Git diff, new browser harness, local commands/results, owner
  issue decisions, accepted ADR 0006 and parity matrix.

## Opening Review State

Goal: compare implemented foundations, status cues, documentation and validation
against the corrected plan and confirmed owner direction. P01/P02 complete and
reconciled. Acceptance basis: five issue criteria, source/dependency rules,
critique PC-001 through PC-004, explicit evidence limits and Refs-only delivery.
First comparison: source changes and executable evidence, not full adoption
acceptance. Review is read-only except this record; no further implementation
or second Review. Docker unavailable; human/live-service acceptance unavailable.

## Execution Status

Complete. The parent directly inspected the supplied artifacts, complete
implementation diff and new browser module, and evaluated local evidence.
No independent implementation-review worker ran; the bounded evidence fits
one direct assessment. One independent plan critique ran earlier.

## Plan-to-Change Reconciliation

| Scope | Evidence | Reconciliation | Gap |
| --- | --- | --- | --- |
| P01-T01 | Source-pinned neutral/type/spacing/radius/motion mapping, legacy aliases and representative resolved native styles | Complete | Not a packaged Fluent runtime |
| P01-T02 | DOM-built shapes/codes, explicit safety counts, selected words, shared Enter/Space handler and list equivalent | Complete for tested states | Full human accessibility remains open |
| P02-T01 | Five suites, all project lint/types, non-exempt browser checks, 31 real synthetic app assertions | Complete with declared unavailable checks | 97 environment-dependent skips; Docker denied |
| P02-T02 | Design synthesis, API guide, knowledge-base index/log and RPI evidence | Complete | Adoption gate remains explicit |
| P03-T01 | This one Review complete; parent owns subsequent privacy-safe commit, push and Refs PR | Ready for delivery | Commit/PR cannot be evidenced before creation |

## Completed Work Assessment

The API owns all new code/tests/checks. No mvp module is revived, shared core
imports no workload, no SQL statement/schema is introduced, and no agents image
dependency changes. Playwright is API development-only and absent from runtime
requirements; the existing source-CI API job now runs the harness and isolated
lint/format checks without inherited migration exemptions.

The stylesheet consumes the new mapping in buttons, fields, cards and headings.
Legacy screens retain aliases. Theme/body/focus deviations are explicit rather
than falsely called official Fluent recipes. Existing token tests now cover
camel-case tokens, semantic alias resolution and exact sourced values.

The real map endpoint supplies both >500-home cluster and three-point modes.
Circle/O, square/W, triangle/! use borders plus text; key and control names agree.
Cluster safety counts include zero. Selected-filter words do not depend on
border colour. DOM-built tooltips avoid interpreting a record as markup.
Explicit Enter/Space activation is necessary with the bundled Leaflet; local
browser execution verifies actual zoom requests and case hash navigation.

Named keyboard-scrollable table regions contain the observed 320px overflow,
preserving native headers and table structure. The browser checks cover actual
scrolling, not just a narrower viewport. Forced-colour/reduced-motion results are
bounded automated evidence, not screen-reader or user acceptance.

AI model paths/configuration, server review authority, deterministic ordering,
human approval and resident consent are unchanged. An existing AI warning and
assistant registry are exercised; successful real inference is not claimed.

## Implementation-Time Plan and Detail Update Assessment

| Update | Reason/evidence | Decision handling | Assessment |
| --- | --- | --- | --- |
| Named table scroll regions | Browser found two wide Overview tables overflowing at 320px after tokenized padding | Directly related foundation/reflow correction; no new owner choice | Plan/details/changes reconciled |
| Pinned API development Playwright and CI steps | Clean CI must resolve strict import types and execute new browser regression | Test tooling only; no production dependencies or new exemptions | Scope/details and evidence accurately updated |
| Explicit custom-marker keyboard handler | Actual keypress did not trigger click in bundled Leaflet | Ordinary implementation correction, not changed business behavior | Enter and Space browser evidence supports it |

## Critique and Material Revision Assessment

PC-001 is resolved for honest partial delivery by keeping full adoption open;
not resolved as completed Fluent adoption. PC-002 has precise official source
mapping and rendered-value evidence. PC-003 has isolated lint/format plus strict
mypy. PC-004 has explicit P03 Review/commit/push/PR ownership and Refs-only intent.
No owner decision was invented, no second critique or repeated Review ran.

## Plan Follow-Up Assessment

| Follow-up | Why outside delivered slice | Owner and required next evidence | Route |
| --- | --- | --- | --- |
| Actual Fluent component integration | Native token foundations do not fulfill runtime adoption | Delivery workstream; actual selected Fluent implementation, rendered states, packaging/CSP and accessibility evidence, or explicit owner acceptance of a substitute | Distinct follow-up RV-001 |
| Human accessibility acceptance | Synthetic checks are not human/screen-reader evidence | Owner/accessibility reviewer; representative tasks and assistive-technology evidence | Distinct follow-up RV-002 |
| Live/runtime gates | Docker denied; no real inference/SQL Server/Azure execution in this change | CI for image/SQL tests, authorized operator for live validation | Distinct follow-up RV-003 |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Owner-selected Fluent UI adoption remains incomplete

Evidence: design-system decision and plan explicitly state no Fluent runtime
component integration is shipped. The owner rejected retaining the bespoke UI.
Impact: this foundation PR cannot close #150 or claim adoption delivered.
Destination: distinct adoption follow-up owned by the delivery workstream.
Smallest next action: plan/integrate the actual Fluent component path and verify
rendered states, dependencies/CSP and accessibility, or obtain explicit owner
acceptance before treating native-only components as the final substitute.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Full accessibility acceptance is not evidenced

Evidence: 31 automated browser checks and local token contrast pairs; no direct
screen-reader/user session or complete workflow/state conformance assessment.
Impact: local fixes address the observed map/cluster/tile failures, not every
possible status/safety state or an entire WCAG conformance claim.
Destination: distinct accessibility follow-up, owner/human reviewer.
Smallest next action: validate representative role tasks, status comprehension,
screen readers and full zoom/reflow/state coverage; retain unverified items open.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Container and real-service evidence is unavailable locally

Evidence: Docker socket permission denied; API suite skipped 97 environment-
dependent tests. No model, SQL Server or Azure call was authorized/executed.
Impact: no local image, backend portability execution or live-AI acceptance claim.
Destination: CI image/SQL checks and separately authorized operator validation.
Smallest next action: inspect the PR CI results; do not infer live approval from
local JSON/SQLite or model test doubles. No permission escalation is warranted.

## Defects

No high-confidence implementation defect found within the delivered foundation
boundary. The open adoption/evidence work is not silently relabelled as complete.

## Routed Findings

| Finding | Destination | Owner/next action |
| --- | --- | --- |
| RV-001 | Distinct adoption implementation follow-up, planning first | Delivery workstream; actual Fluent component integration evidence |
| RV-002 | Distinct human accessibility follow-up | Owner/accessibility reviewer; observed task/assistive-technology evidence |
| RV-003 | CI and authorized validation follow-up | CI/operator; image, SQL Server and live-service evidence |

## Validation Evidence

Exact commands, failed development attempts and corrections are in the changes
record; this Review does not silently discard those failures.

| Check | Status | Result |
| --- | --- | --- |
| Five src unittest suites | Passed with skips | 898 discovered, 801 passed, 97 skipped; core 298, API 474, agents 70, orchestrator 17, importer 39 |
| Five-project Ruff check/format and mypy | Passed | New browser module also checked without wildcard exemptions |
| Final API suite/lint/format/mypy | Passed | 474 tests, 97 skips, 139.2s; strict types on 36 files |
| Real local synthetic app browser check | Passed | 31 assertions, Chromium 156.0.8078.4; real map API, synthetic pixel basemap |
| Node syntax, compileall, diff whitespace | Passed | Final source changes checked |
| Local Markdown targets and TOML/dev-only boundary | Passed | All four edited docs' local targets exist; Playwright absent from runtime requirements |
| Docker image execution | Unavailable | Permission denied on Docker socket |
| Actual SQL Server, Azure and real inference | Not run | Not replaced with synthetic evidence |
| Full Fluent runtime/human accessibility | Not accepted as delivered | Explicit remaining gates |

## Outcome

Outcome: Residual work. Review execution is Complete. The tested foundation slice
is supported by local engineering evidence, but issue #150 is not fully accepted:
Fluent runtime adoption and broader human/evidence gates remain open. Use Refs
#150, not an issue-closing keyword.

## Closeout Routing Record

No implementation defect or newly ambiguous owner decision is routed back inside
this task. RV-001/RV-002/RV-003 remain distinct follow-ups. Parent proceeds only
with P03 artifact commit, topic-branch push and main PR; no merge or new child
implementation is authorized by this Review. Do not repeat Review to verify
later closure.
