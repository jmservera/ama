---
title: Coordinator heatmap and lifecycle funnel issue101 research
description: Actual-source evidence and scoped read-only reporting decisions
ms.date: 2026-10-17
---

## Brief and active controls

Task 101, coordinator-lifecycle-funnel-101. Audience: implementation and independent
coordinator review. Output: convergence, focused posture selected from the bounded
user scope. Trusted evidence root: repository `.copilot-tracking/research/2026-10-17/`.
Research is read-only outside evidence and explicitly required workflow state.
The requested full ordered loop authorizes automatic continuation, not approval
of customer outcomes. Initial clean source/base is
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213 on
feat/coordinator-lifecycle-funnel-101; no existing PR.

## Questions and acceptance boundary

1. Which current filters, roles, map/list and read models can be reused exactly?
2. Which timestamped events support entries/exits/returns, and which remain unknown?
3. How can counts, denominators, holds, priority, missing geocodes and drillthrough
   reconcile without changing writers, authority or priority policy?
4. What local browser, SQL and image checks can actually be executed?

No new framework, tile provider, service, real data, Azure, paid AI, ranking,
document/provenance writers or orchestrator/doc_controls changes. Issue100 is
hierarchy, not ordering. Actual event dependency102 merged as PR394; resident88
PR392 and sensor112 PR393 are in the base. Issue117 owns the pending document
rescan scheduler and possible Store document audit integration. Shared KB
index/log edits are declared overlap; preserve all entries on later authorized
integration. No other worktree reads.

## Extension and participation register

* Repository instructions, original/addendum/index/memory and component guides:
  selected as project context; memory is not evidence.
* rpi-research: selected, ordered wider/deeper/contrarian cycle inline because
  the source trace is tightly coupled; no research worker claimed.
* web-design-guidelines and redesign-existing-projects: selected for the existing
  workbench only, to load before web edits; Fluent2/WCAG/plain-language govern.
* Public landing-page/image skills: skipped, not applicable.
* Critique and original Review: later explicit phases, not research activity.
* No interaction needed: user supplied scope, branch/base and authority limits.

## Prior knowledge gate

Backlog-manager search was incomplete. Do not infer absence of UI. GitHub issue101
read on 2026-10-17 confirms FR-020/021 and PR-005; checkboxes open. Git log and
GitHub PR metadata confirm the three merged dependencies above. Actual source
inspection, rather than prior task claims, will establish reusable contracts.

## Cycle 1

### Wider

Completed inline. Existing vanilla JS/native Fluent-foundation workbench has
overview tiles, Leaflet clusters, map keyboard/list alternatives, stage charts,
server-paged case lists and work queues. No new dashboard framework is needed.
The legacy overview and map are not a shared filtered-population contract:
map uses open cases globally, while list applies own/all/contractor/queue/search.
The map-to-list link even translates fundingprog to the different funding flag.
Use a scoped coordinator mode, not a global behavioral change to legacy views.

### Deeper

Completed inline after Wider. Reuse Store._filtered under its synchronization
lock (SQL refreshes on outer lock entry), Store.page_cases for projected summaries,
insights.map_view for existing marker/cluster construction, taskqueues current_stop
and approved_priority, and progress.history/report for timestamp precision and
event validation. Current stock fields supply area, home.type (recorded archetype)
and case.building_id; missing relationships must be an explicit Unknown bucket.
Report periods apply only to event evidence, never reconstruct current membership.
Existing returns include advance/return/reopen; only one controlled forward writer
exists. There is no authoritative general closure/exclusion stream.

### Contrarian

Completed inline after Deeper. Rejected counting current stage_since/days as entry
or exit, treating closed as accepted handover, treating Declined consent as
programme exclusion, or turning draft ranking into approved priority. Contradictory
or cutoff-ambiguous stage histories must not count as trustworthy observed
transitions. Geocode omission cannot shrink cohort counts; retain missing/invalid
coordinates in table/drillthrough with explicit coverage. Valid map fields still
pass the existing closed-field guard; do not weaken sensor112 export refusal.
Do not aggregate resident narratives, document evidence or financial pause reasons.
Existing staff rights permit all open cases; own scope narrows by owner_code,
not a hypothetical coordinator-only case assignment contract.

## Evidence register

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/app.js:325,996,1079 | Actual list, map and overview exist; reuse native elements/Leaflet |
| C2 | src/core/src/zava_forward/core/store.py:245,268 | Canonical current case filtering and summary projection |
| C3 | src/core/src/zava_forward/core/sqlstore.py:98,782 | Synchronized snapshot and SQL paging/filter semantics |
| C4 | src/core/src/zava_forward/core/progress.py:119,382,600 | Versioned validated events, inclusive UTC windows, partial/unknown history |
| C5 | src/core/src/zava_forward/core/projection.py:38,66 | Registered staff endpoint roles; contractor/default deny; field restrictions |
| C6 | src/core/src/zava_forward/core/taskqueues.py:14,46,102 | Queue/current-stop definitions and owner-approved priority distinction |
| C7 | src/core/src/zava_forward/core/insights.py:45,145 | Existing filters, grid clustering, point cap and signal semantics |
| C8 | src/core/src/zava_forward/core/export_fields.py:122 | Closed map field contract; malformed nested values must refuse |
| C9 | docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-020/021, PR-005, AC-023/024 | Requested heatmap/funnel and count reconciliation |
| C10 | docs/reference/research/ux/design-system.md, wcag-conformance-baseline.md, content-standard.md | Fluent foundation, native semantics, no conformance claim, plain language |
| W1 | https://github.com/jmservera/ama/issues/101 (retrieved 2026-10-17) | Exact three open acceptance checkboxes, parent100 hierarchy |
| W2 | https://github.com/jmservera/ama/pull/394 (retrieved 2026-10-17) | Actual event capture merged at supplied base |
| W3 | https://github.com/jmservera/ama/pull/392 and https://github.com/jmservera/ama/pull/393 (retrieved 2026-10-17) | Resident and sensor controls already merged |
| W4 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-17) | Full rules retrieved before web edits; refresh before original Review |

## Selected recommendation and alternatives

Add one read-only coordinator aggregation module and staff-only GET contract,
with one authorized current open population shared by heatmap, existing map and
paged record drillthrough. Expose own/all and existing source filters/search,
area/building/recorded-home-type heatmap grouping, explicit UTC event window,
observed distinct-case entries/exits/returns/reopens, current stopped cases,
unknown legacy history and filter exclusions. Unsupported lifecycle exclusions,
true conversion rates and complete historical totals remain null/Unknown.
No Store writer, schema or SQL query changes are needed. Existing list summary
projection is reused; bounded record pages, not all-record delivery.

Reject a second dashboard framework (C1), new synthetic history/writers (C4),
UI-only authorization (C5) and policy changes (C6). Keep legacy overview reachable
and add the coordinator view within that workstream. This is not UX widening
into forecasts, exports, timelines or new approvals.

## Validation feasibility and remaining uncertainty

Docker daemon available (29.9.0). Initial system-Python import failed with
ModuleNotFoundError; no preexisting repository venv. Restored editable source
distributions/dev tools using pip in task-local .venv, then installed Chromium
successfully. No private data read. Local SQL parity and nonroot image are feasible
but not yet executed. Browser must exercise real changed behavior, not screenshots
alone. Human understanding/approval and independent coordinator acceptance remain
unavailable and must not be self-awarded.

## Evidence, decisions and readiness

Research disposition: executed. Planning Readiness: Ready for the bounded read-only
slice. One complete focused cycle covered the material questions; another cycle
would repeat source contracts. Full historical capture, independent human/WCAG
acceptance and general lifecycle exclusion/closure writers are explicitly not
established. No blocker requires modifying issue117-owned paths.
