---
title: Inventory-managed staff intake and independent QA 132 extension E2 research
ms.date: 2026-11-11
---

Extension E2 of five under the owner's separate Nov10 extension for #132. E1 spent, this E2 spent, three remain; no automatic E3. Refs #132, #131, #440. This is a new bounded follow-up to merged PR 1425, not a reconstruction of its original RPI. Research disposition: `executed` (bounded, existing files only). Planning Readiness: `Ready`.

## Identity

| Item | Value |
| --- | --- |
| Worktree and branch | `issue-132-inventory-qa-1111`, `test/demo-inventory-intake-qa-132-1111` |
| Base | `7e2744cf7774825b21c73fffbc075b95755239cc` (eventual target `main`) |
| Consumed checkpoint | #440 `d174ab85347a49386c92a42aefe0513f6a3a9f58`, research `.copilot-tracking/research/2026-11-11-inventory-intake-main-440-1111-research.md` at the retained `issue-440-inventory-intake-main-1111` worktree |
| Exact gap (from that checkpoint) | No executable test combines an inventory-managed case, staff intake capture and acknowledgement, and an independent-QA refusal control |
| Agent qualification | `hve-core-all:rpi-agent` is not a task agent type in this session; the run used the selected RPI agent instructions with claude-sonnet-5.5 and a rubber-duck critique |

## Evidence read (existing files only)

* `src/api/tests/test_staff_intake_api.py`: `StaffIntakeApi` on `ProcurementApiFixture`, case `ZF-3`, work order `WO-0001`, `capture`, `accept`, `view`, `restart` helpers, positive control `test_recorder_is_denied_and_independent_qa_accepts` (non-inventory). Base class runs on the SQLite store, `JsonStaffIntakeApi` on JSON, `MssqlStaffIntakeApi` is env-gated.
* `src/core/src/zava_forward/core/resident_decisions.py`: `_inventory_managed` (key present, or `tenure_review_required`, or non-empty `tenure_reports`), `resident_gate` returns `[*_inventory_refusal(c), TENURE_HOLD]` for an inventory-managed case, `_res_tenure_inventory_record` (route `/api/cases/{id}/resident`, action `tenure_inventory_record`, `households` null is valid and gives status `Unknown`, sets `tenure_review_required`).
* `accept_quality` and `hand_over_quality` call the shared resident gate; `staff_intake.capture` and acknowledgement do not reference the inventory.
* `src/api/tests/test_resident_api.py`: the existing HTTP inventory request body and the 200 / 409 contract.

## Observed behaviour (throwaway probe in /tmp, not committed)

* Capture before the hold, then inventory record `Unknown`: 200. Acknowledgement afterwards: 200, quality state stays `Submitted`. Independent QA accept: 409 with reasons `The expected-household inventory is Unknown.` and `TENURE_HOLD`.
* Capture while already held is not refused: it records a `Submitted` receipt awaiting independent review (recording evidence is not acceptance). No invented refusal is asserted.
* Accepted before the hold, then hold: handover 409 with the same reasons, state remains `Accepted`. A later replacement capture records `Submitted` (superseding the accepted record, existing behaviour) and its accept is 409.
* The non-inventory handover control (accept then handover with `resident_told`) returns 200 `Handed over`, so the 409 is attributable to the hold.
* No source defect was found.

## Limits

* Test-only; JSON and SQLite store only. Neither establishes MSSQL or live acceptance. Legal tenure interpretation, the Home Ownership data owner, resident consent and real QA stay human boundaries. The hold is caller-declared; no approval is invented.
