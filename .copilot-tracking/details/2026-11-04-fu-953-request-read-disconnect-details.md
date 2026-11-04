# Details: issue 953

## Phase 1

* `src/api/src/zava_forward/api/server.py`: `parse_request` override stores `_request_parsed`; `handle_one_request` resets `_request_parsed` and `_body_read_failed`; `_body` sets `_body_read_failed` when `rfile.read` raises ConnectionError.
* `_unhandled`: a ConnectionError with the response started, a failed body read, or an unparsed request logs WARNING `http-error <method> <path> client-disconnect exc=<name> phase=<request-read|response-write>` and returns without a 500 attempt. Everything else keeps ERROR and the 500 answer.

## Phase 2

* `tests/test_error_logging.py`: `test_client_disconnect_during_request_read_logs_warning_not_error` patches `parse_request` to raise ConnectionResetError; asserts only WARNING records, the phase text, no `status=500`, no secret.
