# Plan: live briefing observer for #531 (2026-11-01)

* Scope: read-only `briefing` observer in `src/api/checks/employee_acceptance_check.py` plus tests. UI behaviour and approval boundaries unchanged. Criterion 7 stays unmet (needs owner live run).
* Phases:
  * [x] Add `briefing` observer to `OBSERVERS` (navigate to `#/`, wait for `.briefing [data-record-id]` or `.briefing .ai-label`, assert label, Sources used, time, no alert; no clicks except none).
  * [x] Update `tests/test_employee_acceptance_check.py` (observer count 4; real fixture run asserts briefing stage passes).
  * [x] Update api README live acceptance note.
  * [x] ruff, format, mypy, unit tests.
  * [ ] Commit, push, PR with Refs #531.
* Critique (single pass, direct): keep observer read-only and boolean-only to honour the live contract; do not add review-action clicks (would record a review live); order after `case` is unnecessary but place last so existing stage order is stable. Verdict: proceed.
* Validation: focused unit tests, ruff check/format, mypy.
