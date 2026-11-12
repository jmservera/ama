<!-- markdownlint-disable-file -->
# Narrow engineering proposal for the #184 live demo: original author Review (2026-11-12)

Execution: ONE Review by the authoring session, once, after the documentation implementation. It is NOT independent. The coordinator's independent exact-head review remains required before any publication. No second Review is run in this task.

Boundary: the [proposal subsection](../../../docs/reference/research/iot-sensor-analytics-research-plan.md#narrow-engineering-design-proposal-2026-11-12-refs-184), index pointer and log entry, against [the plan](../../plans/2026-11-12/issue-184-narrow-design-proposal-1112-plan.md), [critique](../../plans/2026-11-12/issue-184-narrow-design-proposal-1112-critique.md) and [changes](../../changes/2026-11-12/issue-184-narrow-design-proposal-1112-changes.md).

## Outcome

Documentation candidate complete for the five requested areas; no blocking defect found by the author. Not a conformance, acceptance or approval statement.

| Check | Result |
| --- | --- |
| Five areas covered (correlation and receive, expiry and fence, finite admission, staged changes with tests and evidence plan, separate approval handoffs) | Present |
| No approval, price certification, exactly-once billing or remote cancellation claimed | Held; stated as not claimed |
| Guard not weakened or staged | Held; D2 owner decision |
| 2026-11-11 original, corrected and adverse records unchanged; chronology Medium qualified | Held (no file in that set touched) |
| Critique findings 1-9 dispositioned | Applied |
| Documentation validation | Links, whitespace, JSON passed; no runtime or gate run |

## Open items and limits

* Author review only: independence is absent. Findings the author would miss are not excluded.
* The rpi-* skill bodies were not loaded; the protocol was followed from the agent instructions.
* Line anchors were spot-checked, not re-verified one by one; `iot_stream.py` 255 is a comment about not checkpointing, which is the cited basis for "no checkpoint store".
* Unverified in the design: live Hub enqueued-time behavior and retention, share lock semantics across replicas, current prices and free grants, byte versus token bound.
* Decisions D1-D6 are unresolved and routed to the owner. Implementation permission and a named finite deployment, live, model and spending authorization are separate future handoffs, neither granted.
* No hosted CI applies to this local-only candidate.

## Routing

Later work, user-selected only: owner decisions D1-D6, then per-stage implementation permission. Nothing returns to Implement or Review in this task.
