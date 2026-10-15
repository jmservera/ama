---
title: "Review: conversational assistant panel (#159)"
ms.date: 2026-10-15
---

## Execution and outcome

* Review executed once after implementation. Outcome: conformant for the delivered slice; three acceptance criteria stay open for evidence reasons (below). No material code findings open.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Panel available from a permitted case, never required | Met (code) | `chat.js` collapsed `details` on the case card; contractor role refused by the existing `chat` category; `test_chat_panel` web test and browser run |
| Cited, abstains, labelled | Met | `parse_reply` and abstain tests; label on every kind |
| Follow-ups keep case context, re-check permissions each turn | Met | `test_follow_up_keeps_case_context`, `test_every_turn_rechecks_role_and_case` |
| Only a proposal or draft via the independent review; no controlled-record change | Met (partly evidenced) | `test_chat_cannot_change_a_controlled_record`; proposals use `Assistants.invoke`. The SQL-enabled invoke success path is not exercised locally (the assistants SQL tests are skipped without SQL Server); CI evidence needed |
| Model failure falls back to workflow-only | Met | `test_model_failure_falls_back_to_workflow_only`, agents `test_chat_model` |
| Keyboard operable, screen-reader tested, announces | Partly | Keyboard run and `aria-live` log verified; screen-reader test not done, so the criterion stays unticked |

## Findings routed to later work

* Screen-reader test with a named reader and browser (owner or tester action).
* Live model run against the Azure endpoint and real chat data after OD-45 to OD-49.
* Streaming and resumable panel are not delivered.
* The temporary mypy and ruff exemptions for moved files are unchanged (tracked in #199 follow-up).
* Citations are projected field paths, which are coarse; a friendlier source label list is a UX follow-up.
