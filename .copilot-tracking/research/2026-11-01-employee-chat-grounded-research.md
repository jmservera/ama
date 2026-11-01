<!-- markdownlint-disable-file -->
# Employee chat grounded on the selected case: research (2026-11-01)

Task: `employee-chat-grounded`. Branch `feat/employee-chat-grounded`. Refs #530.
Research disposition: executed. Planning Readiness: Ready.

## Owner feedback

Live employee chat answers "why is this case blocked?" and "Why is funding not
started yet?" with only the storage notice plus the fixed unavailable text and
a list of every workflow skill. It is not grounded on the selected case.

## Findings (code evidence)

* `src/api/src/zava_forward/api/server.py` route `/api/chat/unstored-ask` calls
  `ChatPanel.ask_unstored` only when `privacy.decision()["approved"]` is false.
* `ChatPanel.ask_unstored` (`src/core/src/zava_forward/core/chat_panel.py`)
  authorises the case with `case_context` but then discards it
  (`skill_sources(skill, {})`) and always returns the fixed notice plus FALLBACK
  with all workflow skill purposes as citations. The refusal router
  (`out_of_scope`) runs first and stays.
* `ChatIsolation.case_context` uses `store.detail(case_id, user)` (the role's
  projection) then `export_fields.chat_case`, which drops `reason`, `work`,
  `gate`, `funding` and documents. The projected detail itself already carries
  the recorded status line, `work` (reason, next_action, owner, source,
  blockers with step, reason, owner, next_action, source), `gate` reasons,
  `funding` (route, status, reference), `funding_ok`, `documents`,
  `checklist`, `technical_missing` and open `hazards`.
* Roles without `projection.can_see_reason` have notes held by
  `redact_staff_detail`; the top-level `reason` is not used for those roles.
* The stored/model path (`ChatPanel._ask`) is bound to a persisted thread,
  `iso.privacy._require()` and meter finalisation (`publish_output`). A
  stateless model call would bypass those controls, so it is not added. Rules
  only is the safe result when storage is unapproved.
* `chat-widget.js`: `externalFocus` hides the panel on any focus outside it.
  That matches the owner note that the employee panel "closed itself". The
  resizable employee panel defaults to 35vw by 70dvh.
* Existing proof: `src/api/checks/employee_chat_browser_check.py` (Chromium,
  Playwright installed locally); Node focus tests in
  `src/api/tests/test_chat_widget_focus.py`.

## Decisions

* Rules-only grounded router over the projected case, in a new pure module
  `chat_case_answers.py`; no model call, nothing stored, no record change.
* Intent matching by word families, not literal phrases. Funding, blocked,
  missing, next step, owner, status, otherwise a suggestion list for this case.
* Cite the recorded case facts (`ZF-n/path`), not workflow skills.
* A different case id in the question is not answered; the user is told to open
  that case. The selected case is still authorised by the existing path.
* Employee panel: stays open on outside focus (resizable panel only), default
  40vw by 80dvh.
* Content standard: reason, owner, next action; no banned words (gate, hold,
  provenance, trace, snapshot, envelope); ASCII punctuation.

## Follow-ups

* Stateless model answer when storage is unapproved: needs its own registry and
  consumption design (ADR); out of scope here.
