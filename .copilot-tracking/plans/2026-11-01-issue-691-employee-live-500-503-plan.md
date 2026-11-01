# Issue 691 plan: employee live 500 and 503/403 handling

Date: 2026-11-01. Research: `.copilot-tracking/research/2026-11-01-issue-691-employee-live-500-503-research.md`.

## Phases

* [x] Phase 1: server observability. In `src/api/src/zava_forward/api/server.py` `_send`, log one line for any status >= 500 and any non-200/304 response on `/vendor/` asset paths (method, path, status, no query, no headers).
* [x] Phase 2: UI plain language. In `chat.js` add `unavailableNote(feature, error, manual)`: 403 gives "not available for your role", 503 gives "not switched on in this environment", otherwise original text. Use it for assistants, regulatory status and law alerts. Skip `/api/assistants` and `/api/chat/regulatory/status` for `Application Administrator`.
* [x] Phase 3: tests in `src/api/tests/test_employee_live_responses.py`: leaflet bytes for GET, HEAD, `?v=`, conditional 304 and 16 concurrent GETs; 5xx and vendor non-200 logging; chat.js source guards.
* [x] Phase 4: validation (unit tests, ruff check, ruff format --check, mypy for `src/api`), then commit, push, PR.

## Critique (single pass)

Executed. Verdict: proceed. Disposition: logging must not include query or user data (applied); do not claim leaflet cause fixed (applied; PR uses Refs). No conflict with confirmed decisions.

## Risks

Logging volume is limited to errors. UI skip for administrators must not hide anything staff see.

## Correction cycle 2026-11-01

* [x] Log in an overridden `send_response` so framework and application responses are logged once.
* [x] `unavailableNote` and the alert message use role wording only for a client-confirmed role denial (`roleDenied`); otherwise a neutral message with the server explanation and the manual route.
* [x] Replace the source-order test with a Node VM test that runs `chatCasePanel` and `regulatoryChatPanel` with stubs: administrators request neither endpoint, staff request both. Critique not repeated (one pass rule).

## Correction cycle 2 2026-11-01

* [x] Read `path` and `command` defensively in `send_response`, treat a `ValueError` from `urlparse` as an empty path, and add raw-socket regression tests (414, 400, 501).
