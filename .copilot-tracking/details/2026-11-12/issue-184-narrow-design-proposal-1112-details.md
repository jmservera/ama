<!-- markdownlint-disable-file -->
# Narrow engineering proposal for the #184 live demo: details (2026-11-12)

Phase details for [the plan](../../plans/2026-11-12/issue-184-narrow-design-proposal-1112-plan.md), after [the critique](../../plans/2026-11-12/issue-184-narrow-design-proposal-1112-critique.md). Documentation only; the deliverable is the subsection "Narrow engineering design proposal (2026-11-12, Refs #184)" in [the IoT research plan](../../../docs/reference/research/iot-sensor-analytics-research-plan.md#narrow-engineering-design-proposal-2026-11-12-refs-184). Source facts and anchors are in [the research](../../research/2026-11-12/issue-184-narrow-design-proposal-1112-research.md).

## Phase 1: Proposal section in the IoT research plan

* Add one subsection before `## Constraints` covering five parts: correlation and receive semantics, expiry and attempt fence, finite model and compute admission, staged source proposals with tests and evidence plan, and approval handoffs. Includes an anchor table at base `b6f61b12`.
* Apply critique findings 1-7 and 9 as stated in the critique dispositions; finding 8 was applied to the research file.
* Keep the guard unchanged and unstaged; record the live-model criterion as unreachable pending owner decision D2.
* Success: every cited anchor exists; no claim of approval, price certification, exactly-once billing or remote cancellation; assumptions marked PROPOSED or unverified.

## Phase 2: Index and log

* One pointer in [the reference index](../../../docs/reference/README.md) in the #110/#184 paragraph; one appended entry in [the log](../../../docs/reference/log.md). Earlier entries untouched.
* Frontmatter `ms.date` of the IoT research plan moves to 2026-11-12.

## Phase 3: Validation (documentation tier)

* Relative link and anchor check of changed Markdown, whitespace check with `git diff --check`, JSON parse of the state record, confirmation that no 2026-11-11 artifact, source, test, infra or guard file changed. No runtime, test suite or complete gate; nothing installed.

## Phase 4: Original author Review

* One review, not independent; routes open work to the coordinator's independent exact-head review. No second Review.

## Decisions kept open for the owner

| Id | Decision | Why not decided here |
| --- | --- | --- |
| D1 | Run marker visible to the Quality projection | `scenario` change affects the wire consumer; owner choice |
| D2 | Any real-model route | Guard forbids it; needs privacy and consent design plus independent review |
| D3 | Durable fence substrate and simulator write permission | Simulator is read-only on SQL by owner approval; lock semantics unverified |
| D4 | Proactive-scanner cohort allow-list | Behavior change in the assistants path |
| D5 | Cohort, slots, attempts, call and token budgets | Finite numbers belong to the named authorization |
| D6 | Schedule-deletion deadline, accountable owner, teardown | Required by the compute envelope and the rev2 prerequisites |
