---
title: Inventory-managed staff intake and independent QA 132 extension E3 research and readiness
ms.date: 2026-11-11
---

Extension E3 under the existing Nov10 extension for #132: E1, E2 and E3 spent, two remain; no automatic E4 and no new budget. Refs #132, #131, #440. Stage: Research and Plan only. Nothing was run in this stage (no unit test, pip, browser, Ruff, mypy, probe or mutation control). Research disposition: `executed` (read-only, existing files and logs). Planning Readiness: `Ready`.

## Process finding on E2 (disclosed, not repaired)

* The E2 draft commit `3c395740d11630529eb79a760d19fb4e8b967fb4` was not planned before it was coded. From the native session log (`events.jsonl` of session a68777f0, 1-based line of each tool start; Root's own cited numbers differ by counting convention but the order is the same): behaviour probes at 159 and 169, the first edit adding `declare_inventory` at 179, the in-process negative control at 203, the first research artifact at 293 and the critique agent at 337.
* So the original E2 research, plan, details and critique are retrospective. The plan was written with every phase checked. The critique reviewed the already drafted candidate (the E2 critique record says so; the handoff disclosed it only in part). No pre-code critique exists for E2.
* The E2 records and logs are preserved unchanged. This E3 is a forward adoption: it plans verification and adoption of the pre-existing unchanged draft. It does not claim the draft was authored after planning and does not fabricate earlier phase markers.

## Identity of the draft input

| Item | Value |
| --- | --- |
| Branch, head | `test/demo-inventory-intake-qa-132-1111`, `3c395740d11630529eb79a760d19fb4e8b967fb4` |
| Tree | `b65f820a49e78e4d3b5b18abb5d9e2b3a5c34161`; parent and base `7e2744cf7774825b21c73fffbc075b95755239cc` |
| Source diff vs base | `src` only `src/api/tests/test_staff_intake_api.py`, 53 insertions, 0 deletions; `git diff 7e2744cf HEAD -- src` SHA-256 `2472c5af61e64651ebf73a221e0336184aa06b5bd24edb3c37c7e78e2c4ec44f` |
| Test file | SHA-256 `1048770a5355a9fe7a078992c0f9553ba94f907f3c9b9cbf37293a83e28c940c`, git blob `50fb4ec4c452b1b77a45d0bd071df8c9027319b2` |
| Worktree | clean at the start of this stage |
| Local `origin/main` | `05f11ebe9c9c04b5b3d12bc4db5889dae3b01d46` (PR 1428), one commit past the base; not fetched in this stage |

## Draft contents read (the two cases)

* `test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa`: capture, real `tenure_inventory_record` (households null, Unknown), acknowledgement 200 and still `Submitted`, independent accept refused 409 with the inventory-Unknown reason and `TENURE_HOLD`, repeated after restart, record `Submitted`, inventory view `Unknown`.
* `test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held`: capture, accept 200 before the hold, hold, handover refused 409, record `Accepted`, a later capture records `Submitted`, its accept refused 409.
* Inheritance (Root's correction accepted): the cases sit in `StaffIntakeApi`, so they run on the SQLite-backed base class and on `JsonStaffIntakeApi` (JSON), and on the env-gated MSSQL subclass only when opted in. E2 handoff wording "JSON and SQLite" is correct; any E2 phrase implying JSON only is superseded by this record.

## Guard trace relevant to the sensitivity diagnostic (static)

* `accept_quality` (`quality.py:310`): safety clear, `_qrec`, then `require_resident_clear` (line 315), then state check, `require_quality_evidence`, `_independent`. `hand_over_quality` (line 371): `require_safety_clear`, `_qrec`, `require_resident_clear` (line 378), evidence check for `Accepted`, `_qmove`.
* `Store.require_resident_clear` (`store.py:613`) raises `GateError(resident_gate(c, bindings))`; `SqlStore.require_resident_clear` (`sqlstore.py:1064`) calls the base then records a read dependency. Both accept and handover therefore share one resident-clear call; `handover_blockers` (`quality.py:86`) is a projection and is not on the accept or handover path.
* Other guards after the resident guard: state check, evidence, independence. After the inventory hold, the pre-hold accepted record has evidence and independence satisfied, and the Submitted records were created by Sam and are accepted by Quil or Pam, who are independent per the existing positive control. A clean bypass is therefore plausible, not assured.

## Weakness in the E2 negative control (preserved adverse result)

The E2 control patched `_inventory_managed` to False, so the inventory route never opted in and the test failed at `tenure_inventory_view` during setup (`KeyError`). It proves dependence on the inventory setup only, not sensitivity of the held-accept and held-handover assertions. The E2 changes record already calls it weak.

## Current-main compatibility (static)

`git diff --name-only 7e2744cf origin/main` outside `.copilot-tracking` lists only AI consumption files (`ai.py`, `ai_consumption.py`, `assistants.py` and two AI test files). It does not touch `test_staff_intake_api.py`, `quality.py`, `resident_decisions.py`, `staff_intake.py` or `store.py`. Compatibility is expected but unobserved; it needs one actual run.

## Limits and boundaries

Test-only; no application defect identified (Root's read agrees). MSSQL, hosted CI, human QA, resident consent, Legal tenure interpretation and Home Ownership data are unobserved or human boundaries. The hold is caller-declared synthetic data. This stage grants and claims nothing about implementation, review or publication.
