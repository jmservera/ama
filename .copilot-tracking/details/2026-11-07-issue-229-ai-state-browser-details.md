# Details: issue #229 AI state browser check

## Phase 1: fixture

* `operator_data()` appends three `kind: ai_task` recommendations: Quarantined with `fallback_reason`; mode ai, source template with a reason (fallback); mode workflow, source template, no reason (workflow-only).
* `main(..., env_overrides={"ZF_EXCEPTION_STAFF": ...})` names pam@example.test as data_steward and digital_operator. Synthetic only.

## Phase 2: browser section

* Before opening: the entry text and link are shown, no `/api/exceptions` request was made, no item table exists.
* Focus the link, press Enter (keyboard open). Within the panel assert: Quarantined row text and fallback row text distinct (per-row); workflow-only record absent and the workflow-only paragraph present; "Service state Unknown" banner and no "No outage recorded"; owner "from configuration, not an appointment"; placeholder recovery text and the note that nothing is replayed; no audit-trail or audit-history claim; empty-list and source-gap text; eligibility Unknown; no controls; labelled focusable table regions reached by Tab; reflow at 320 and 1280.
* Route-intercept `/api/exceptions` with 503 and reopen: role alert "Do not read this as all clear", no table.
* All requests recorded: no non-GET after sign-in and no request to model or AI paths (`/api/ai`, `/api/assistant`, `/api/chat`).

## Phase 3: regression test

* New cases in `tests/test_exception_register_screen.py` pattern: build the store contract from `operator_data()` with the real `exception_register` mixin, render real `role-screens.js` via Node VM, assert the checker's phrase constants appear and workflow-only is absent. Phrases live in module constants shared with the browser section.

## Phase 4: validation

* Own venv under /tmp/zf229-scratch (pip, not uv); `python -m unittest` for the focused tests, ruff check, ruff format --check, mypy on the changed files, `PYTHONDONTWRITEBYTECODE=1`, exit codes captured without pipes. Browser run only after coordinator admission.

## Critique

Executed once, independent read-only rubber-duck agent, before implementation. Verdict: four blocking and three non-blocking findings, all compatible with owner direction and applied directly (none rejected, none needing a user decision).

* 1 recommendations key absent from dataset: use `data.setdefault("recommendations", [])`; keep pam's manager login and name her via `ZF_EXCEPTION_STAFF`.
* 2 checker imports Playwright at module load: put the fixture records, staff env and expected phrases in a Playwright-free `checks/data_operator_ai_state.py`; the checker and the regression test both import it.
* 3 empty-list text cannot show with items present: add a separate intercepted constructed empty-contract scenario.
* 4 SPA hash routing and the open link: install interception, navigate to the screen without `exceptions=1`, then open by keyboard; wait for the intercepted response.
* 5 unique IDs: three distinct record ids and reasons; assert per row by source id; workflow id absent.
* 6 vacuous Tab check: assert the expected register table labels, captions and focusability first; scope controls and tables to the register panel.
* 7 request evidence: listeners installed before screen navigation and kept through all scenarios; parse URL paths; describe as browser-observed (cannot prove the server made no model call).
