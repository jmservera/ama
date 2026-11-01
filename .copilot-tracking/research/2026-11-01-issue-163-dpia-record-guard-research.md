# Research: issue 163 DPIA record drift guard, 2026-11-01

* Task: issue-163-dpia-record-guard. Research disposition: executed. Planning Readiness: Ready.
* Sources read: issue 163 body, `docs/reference/research/chat-memory-dpia.md`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/tests/test_chat_privacy.py`, BRD CON-003/RULE-019/RULE-022, PRD DH-001 to DH-007 and PR-001/003/004, ADR 0002 decision 7, prior RPI evidence (2026-10-15 and 2026-11-01 issue-163 plans, changes, review), merged PRs #281, #649.

## Findings

* Criteria 1, 3, 4, 6 are delivered and tested (`test_chat_privacy.py`, 14 tests): data map, rights via the #160 repository, diagnostics without content, warning and redaction.
* Criteria 2 and 5 are human decisions. The decision pack D1 to D8 in the DPIA record has every decision cell "Not recorded"; `CHAT_*_REF` settings are empty; no retention period is set. Provider terms are documented from vendor text but not accepted by the DPO and Legal.
* Gap: nothing in tests ties the DPIA record to the code. Docs could drift (a data class dropped from the data map, or a decision cell filled in without a reference) without a failing check.
* Dependencies #120 and #121 are open; named DPO and Legal owner remains Juan Manuel Servera (exercise owner, not a company appointment).

## Decision

Smallest demo-ready slice: a test outside the package that guards the DPIA record against the code and against invented decisions. No new runtime code, no retention period, no decision recorded.

## Follow-ups

* DPO and Legal complete D1 to D8 and set `CHAT_*_REF`.
* Confirm deployed deployment type and abuse-monitoring state.
