# Details: assistants denial (Refs #920)

## Phase 1 to 3

* `src/api/src/zava_forward/api/server.py`: `/api/me` services gains `assistants`.
* `src/api/src/zava_forward/api/web/assistants.js`: shared text "AI assistance is not available for your role. Use the ordinary case controls; no one is waiting on a suggestion." Manual path is the ordinary case controls. Human approval boundaries are unchanged because no proposal can be requested or reviewed in this state.
* `src/api/tests/test_expected_denials.py` and `src/api/checks/expected_denials_browser_check.py`.

## Validation (focused tier)

Not security, infrastructure, SQL or deployment work. No gate, benchmark or full suite run.
