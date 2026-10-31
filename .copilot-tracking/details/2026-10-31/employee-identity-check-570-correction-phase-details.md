---
title: Employee identity correction phase details
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

Task 570-correction, employee-identity-check-570-correction.
Research Ready; original Review remains Not accepted.

<!-- rpi:phase id=P01 -->
## P01: Correct and integrate

<!-- rpi:task id=P01-T01 -->
### P01-T01: RV-002

Change observer signature to accept fresh admission. Use a dedicated internal
admission-loss exception, handled as blocked without leaked error text.
Guard after hash changes/case-link navigation and before later offered-control
interactions; retain outer pre/post probes. Test map and case navigation with
wrong-origin and lost expected-account sessions, including second case-link
transition. Explicitly assert no next interaction and later stage blocked.
No Browser Page facade that silently delegates unsafe actions.

<!-- rpi:task id=P01-T02 -->
### P01-T02: RV-001

Correlate response with selected filter query/origin; validate total/mode/shown/
items and renderer-required point/cluster fields. Compare actual list labels/
links and markers/status to same in-memory payload, including empty state.
Count page errors only while observer active and remove handler finally;
never retain raw errors. Refuse HTTP/JSON/schema/error/mismatched render.
Bound actual rendering wait; do not mistake cleared busy or changed status
for render completion. Actual Chromium routed response negatives and preserved
normal observer coverage use public synthetic fixture only.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Integrate and validate

Non-rewriting merge of fetched main. Main side only for rubric latest.json;
preserve both append-only log additions. API README reflects new callback and
render boundaries without claiming atomic-session or live acceptance.
Pip external venv after observed missing namespace import. Run focused tests
first then API discovery, Ruff/mypy and tools/test_rpi_checks.py.
No existing ignored inputs removed: final gate from clean detached exact HEAD.

<!-- rpi:phase id=P02 -->
## P02: Review and publication

<!-- rpi:task id=P02-T01 -->
### P02-T01: Original correction Review

One fresh read-only reviewer assesses correction against original finding
reproductions and complete changed runner/test/guide. Preserve its original
outcome; route new findings later, do not repeat this Review.
Resolve GitHub-derived noreply author/committer email before commit and include
requested Copilot trailer. Commit implementation and dated original evidence.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Current-base complete gate

Use documented gate's shared lock with finite timeout, owned local SQL/browser/
scanner prerequisites, all checks plus explicit Chromium selectors. External
fresh output and clean exact-head validation worktree; fetch main before gate
and immediately before default full-scope receipt verification.
Independent exact-head assessment is separate from original Review. Any input/
base/tool change invalidates receipt. No skip, synthetic receipt, cloud fallback
or protection change. Missing required prerequisite blocks publication.
Push -u origin HEAD without force and open main PR only with passing gates.
Refs #570 explicitly names original live employee chat/map/case unmet; no
issue checkbox/closing keyword absent reviewed proof of every criterion.

## Residual Evidence Boundary

No new independent identity value supplied; two previous directory methods
denied. Zero credential reads/sign-ins in correction, two authorized attempts
remain unused. Owner/identity administrator attestation needed for live lane.
No ordinary approval prompt is required for explicitly requested publication.

## Direct Critique Dispositions and Executable Contracts

PC-001: Track map requests initiated only after selected-filter activation,
matching authorized origin/flag/area. Pre-activation responses are excluded.
Track matching request completion/failure and all fit/viewport follow-ups.
After response tasks and two animation frames, accept only with no pending
matching requests, unchanged request generation, no errors and exact latest
payload rendered projection. Polling is finite; no fixed sleep is a success
oracle. Retain listeners through this settlement and remove them in finally.
Browser cases cover delayed pre-activation data, valid bounds-triggered
replacement and failed/mismatched replacement.

PC-002: Require points/clusters, integer total/shown (not booleans), shown equals
items length. Points total equals items length, unique nonempty string id/name,
kind normal/long/hazard. Clusters positive integer count, integer hazards/long
within count, sum count equals total. Finite numeric lat/lon in geographic
ranges. Bounds null only for empty or four finite geographically valid ordered
values containing coordinates. Compare actual list labels/links, marker labels/
counts and exact mode status. Empty points require zero list/markers and
"0 homes shown". Additional producer metadata is allowed.

PC-003: Add exactly three methods: test_navigation_admission (mocked map/all/
case-link and chat-ready origin/session loss, blocked reducer and canary
privacy), test_map_payload (mode-specific schema subtests), and
test_chromium_map_contract (actual points/clusters/empty plus malformed items/
kind/coordinates/bounds/counts, stale/follow-up/mismatched rendering and
listener cleanup). Preserve all existing methods and update callback mocks
in place. CLI and full gate explicitly execute:

* api:test_employee_acceptance_check.AcceptanceTests.test_chromium_rosterless
* api:test_employee_acceptance_check.AcceptanceTests.test_chromium_wrong_account
* api:test_employee_acceptance_check.AcceptanceTests.test_chromium_map_contract
