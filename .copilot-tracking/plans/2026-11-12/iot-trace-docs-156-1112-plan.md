<!-- markdownlint-disable-file -->
# Plan: demo IoT-to-UI source trace rows (iot-trace-docs-156-1112)

* Task ID `iot-trace-docs-156-1112`; research [research](../../research/2026-11-12/iot-trace-docs-156-1112-research.md); details [details](../../details/2026-11-12/iot-trace-docs-156-1112-phase-details.md); state `.copilot-tracking/rpi-sessions/2026-11-12/iot-trace-docs-156-1112-state.json`.
* Base `e4854bd7e` on branch `research/demo-156-architecture-readiness-2305`. Mode manual run to completion by the user's direction; local only.
* Tier classification: documentation-only, additive, no executable, workflow, gate, dependency or infra change, so the focused tier applies: Markdown/link review and Git diff only. No `rpi-checks`, no tests, no gate tool run. Hosted CI is not read and nothing is published.

## Phases

* [ ] Phase 1: Add the dated source-pinned section to `docs/reference/research/ux/zava-forward-prototype-profile-review.md` (insert before the `[bc-prd]:` link definitions; five rows; boundary paragraph).
* [ ] Phase 2: Add one KB index row for the update to `docs/reference/README.md` (new row after the Prototype Profile Review row at line 1057, not editing that row) and append one entry to `docs/reference/log.md` (end of file, no earlier entry touched).
* [ ] Phase 3: Verify: every cited path and line re-read; relative links resolve; additive diff proves earlier lines unchanged (only added lines in the three files); ASCII punctuation and no em dashes; `tools/check-design-trace.py` heading logic reviewed statically, not run.
* [ ] Phase 4: Commit prospective evidence, then the documentation change with its changes record, then the independent Review record, each with repository-local privacy identity and Copilot trailer. No push.

## Constraints

* Preserve the 2026-10-18 rows, the 74 count, every Not supplied design, C1 unticked, design/AT/human/live approval gaps and the Blocked gate. No new design approval.
* No assertion of a global absence of an AI guard; S6 is worded as not verified by a bounded, nonexhaustive trace.
* No Bicep, code, regulatory, spec or runbook edit; no reopened #184 minute-cadence or #146 routing campaign; no model or deployment call.
* D1 history and UNKNOWN source-correction balance respected: no code-correction grant or fresh pool is claimed.
* Evidence classes stay distinct: source-read (static) versus observed. Nothing here is observed.

## Success criteria

* Section has five rows (#189, #187, employee Quality sensor panel, cadence, five-home AI scope) each with source path and evidence class and a Not-verified or gap statement.
* `git diff --numstat` shows 0 deletions in the register and the index; the log is append-only.
* Independent Review (separate agent) finds no open material finding or the finding is routed, not re-reviewed.

## Critique disposition

Executed once by a separate agent before any edit; verdict Revise; PC-001 to PC-004 and PC-006 applied, PC-005 rejected (conflicts with the confirmed direction to commit original dated RPI evidence). Recorded in [critique](./iot-trace-docs-156-1112-critique.md). Applied wording rules for the section:

* Five homes is the owner-selected target cohort, not an enforced limit (control cap is 100).
* Library replay, speed and pause exist (`sensor_stream.py` pacer `paused`, `iot_stream.py`); the gap is an operator-facing surface not found in the bounded trace.
* Distinguish the recorded coordinator-held synthetic browser/axe witness for #189 (see the [cutover evidence pack](../../../docs/architecture/cutover-evidence-pack.md), not reproduced here) from missing design, human, assistive-technology and live acceptance.
* The cited design note supplies no sensor-panel flow; do not claim none exists anywhere.
* No link reference definitions in the new section; inline links only.
