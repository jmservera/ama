<!-- markdownlint-disable-file -->
# RPI Changes: climate-source-evidence-178

## Metadata

Task 178; 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md
Details: .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md

## Execution Status

Complete, full plan P01-P03 and P01-T01/P02-T01/P03-T01. No remaining active-plan
markers. Canonical edits followed numerical evidence. Approved scope excludes runtime,
stock/infra, downloads, copied provider pages/raw datasets and human approvals.

## Completed Work

### P01-T01: Reproducible temperature evidence

Added local-only standard-library tools/climate_station_bounds.py and
tools/test_climate_station_bounds.py; generated derived-only
docs/reference/research/climate-source-evidence-178.json.
Eight unittest methods passed. Actual Durham invocation from the phase details
passed input SHA guard; 360 calendar months, 351 accepted pairs and nine estimated
exclusions per field. Report SHA-256
f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615.
No RH inferred, no raw file copied into repository, no downloader.

### P02-T01: Canonical comparison and source register

Integrated dated online section into existing sensor synthesis, explicitly
retaining the prior offline section as historical. Compared all named candidates
and owner leads; locked regional HadUK UUID, citation, OGL/access distinction,
actual login response, Durham measured values and original criterion audit.
Updated reference index/log and the directly coupled core README status.
The generator remains unchanged; owner approval UNMET and RH unavailable.

### P03-T01: Evidence reconciliation

Completed validation below; plan markers/details and handoff synchronized.
No issue checkbox changed. Research records region product lock from PC-003.
All four phase artifacts use the stable task identity/date.

## Implementation-Time Plan and Detail Updates

Immediately relevant current-state update: added the core README's existing
climate-status paragraph to P02 targets because its "not retrieved" wording
and offline-only routing became stale after real retrieval. No runtime change,
new requirement or user decision. Plan scope/details/test ownership reconciled;
no new critique needed. CLI also requires explicit source URL to avoid false
attribution when analyzing a different station; exact details command updated.
Critique PC-001/002/003 remain resolved.

## Validation Record

| Command / check | Result |
| --- | --- |
| python3 -m unittest discover -s tools -p 'test_climate_station_bounds.py' -v | PASS: eight test methods, including CLI success/nonzero hash failure, synthetic quality/missing/duplicate/schema/date/empty cases |
| Exact real-record command in details P01-T01 | PASS: 360 present calendar months, 351 valid pairs, nine estimated exclusions per field, zero missing/provisional in window, 1,401 out-of-window rows |
| Independent inline Python Decimal calculation, not importing helper | PASS: every min/max value and all tied month/source-line occurrences; counts and input hash independently checked |
| Helper replay piped to cmp against committed-target JSON | PASS: byte-identical; SHA-256 f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615 |
| python3 -m compileall -q tools/climate_station_bounds.py tools/test_climate_station_bounds.py | PASS |
| Added relative-link/anchor check | PASS: six added local targets/anchors |
| Append-only log byte-prefix and excluded-path git diff check | PASS: original/addendum/memory/regulatory snapshots/core runtime/infra/support unchanged |
| git diff --check | PASS |
| Initial all-history link scan | FAILED on pre-existing docs/reference/log.md link to retired mvp/README.md#entra-id-on-container-apps. Not introduced here; no unrelated repair. Changed-link scan above passed |
| Ruff/mypy | Not run: not installed/on PATH and no tools-wide configured lint/type target; no dependency installs added for this standard-library tool |
| App build/live DB/Azure/model/full-stock checks | Not applicable/not run: no runtime/deployment/generator changes; no delivered application acceptance claimed |

## Pre-Review Reconciliation

Ready: P01-P03 and all tasks checked with evidence; details/changes/handoff
agree. Owner reuse approval and paired-record access remain unmet issue gates,
not uncompleted implementation markers or permission to expand implementation.

## Blockers and Follow-Up Items

Owner reuse/automated-access review, authorized paired RH/temperature packet
and competent geography/cadence interpretation remain outside this delivery.

## Return-to-Caller State

Implementation complete for the bounded full plan; original issue partially
evidenced, not accepted. One post-implementation Review is next, owned by
the active RPI parent. No source changes should be made to close findings in
that same Review; route later work and then commit/push/open PR as requested.
