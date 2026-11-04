# Research: issue 953 ConnectionError noise on request read

Date: 2026-11-04. Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* PR for #924 ("answer 500 for backend ConnectionError before response starts") merged: backend ConnectionError before the response starts answers 500 and logs ERROR; a ConnectionError after the response started logs WARNING `client-disconnect`. No PR addresses #953.

## Findings

* `src/api/src/zava_forward/api/server.py` `_unhandled`: a ConnectionError with `sent == False` falls through to `logger.error(... status=500 ...)` regardless of where it was raised. A client that drops while the request line, headers or body are being read has not started a response either, so it logs ERROR and tries to send a 500 to a closed socket.
* Request read points: `BaseHTTPRequestHandler.parse_request` (request line and headers, called inside `handle_one_request`) and `_body()` (`rfile.read`) used by POST.
* Backend ConnectionError (store or provider call inside a handler) occurs after parsing and outside `_body`, so the two can be told apart with two flags.

## Options

1. Treat every ConnectionError as WARNING: breaks #924 (backend failure must be ERROR and 500).
2. Track read phase (chosen): `parse_request` override records parsed state; `_body` marks a failed body read.

## Acceptance criteria status before work

* Client disconnect during request read does not log ERROR: unmet.
* Backend ConnectionError still 500 and ERROR: met by existing test `test_backend_connection_error_before_response_returns_500_and_is_logged`.
* Related #921: context only.
