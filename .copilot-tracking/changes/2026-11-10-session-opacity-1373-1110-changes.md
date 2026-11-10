---
title: Issue 1373 resident session opacity test-oracle changes
ms.date: 2026-11-10
task_id: 1373-session-opacity-1110
---

## Status

Implemented 2026-11-10 from HEAD `9e71736bc09984b07d77c122747483548b580c7d` (implement started with source clean). Source change is one file; production source is unchanged (`git diff --name-only 9e71736bc -- src` lists only the test file).

## Source change

`src/core/tests/test_resident_showcase.py` (+41, -2):

* Rewrote `SessionTests.test_round_trip_and_handle_is_opaque`: five-part `v1` structure, 24 lowercase hex keyed handle equal to `handle("C-1")`, no case id in the structural parts, different case and different key give different handles, real `verify` returns `(handle, sid)`, expiry equals NOW + 1800 s and equals the token expiry part. The whole-token absence assertion is removed.
* Added `test_valid_signature_may_contain_case_id_substring`: frozen synthetic key, NOW clock, nonce `b"synthetic-nonce!"` and sid `0000000000000024`, issued through the real `issue` with only the module's sid source patched. It asserts the genuine MAC contains `C-1` (and the structural parts do not), recomputes the MAC independently with `hmac` and `base64`, verifies through the real `verify`, checks expiry and that a one-character MAC change is denied.
* Added the helper `_issue_with_sid` and imports `hmac`, `SimpleNamespace`, `mock`.
* No `_mac` or `verify` mock, no run-time search or retry, no skip, no entropy or alphabet change.

## Red before, green after

* Red before: the unmodified old assertion `assertNotIn("C-1", token)` fails on the frozen fixture through unchanged `issue`/`verify`; real `verify` returned the correct handle, sid and expiry (redacted summary: verify ok, handle ok, sid `0000000000000024`, expiry ok, token length 99). The fixture search found the match at attempt 37 of a 2,000,000 bound. The assertion message echoes the token, so the raw log stays outside the repository (`/tmp/i1373-1110/raw-red-before.log`); only the redacted display (`red-before-redacted.log`) is described here.
* Adverse intermediate result retained: the first run of the new regression failed because my independent MAC formula omitted the `|` separator between nonce and body that `_mac` uses. It was a test-authoring error (the production codec was correct); the formula was fixed to `purpose|nonce|body` and the failure assertion changed to a boolean so it no longer echoes a MAC. The raw first-attempt log is outside the repository.
* Green after (venv `/tmp/venv-1373-1110`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0, own editable install of `src/core`):
  * `SessionTests`: 10 tests OK (was 9; one added). 200 consecutive repeat runs: no failure.
  * `tests.test_resident_showcase`: 41 tests OK.
  * Core discovery `python -m unittest discover -s tests -q` from `src/core`: 2,865 tests OK, skipped=347 (CI observed 2,864 plus one new test; skip count unchanged).
  * `ruff check .` passed; `ruff format --check .` 235 files already formatted; configured `mypy` (project `files`) no issues in 288 source files.
* Preserved by unchanged tests: malformed/version/length/tampered-body and MAC denial, expiry and authority cutoff, restart and key rotation, logout and revocation (including full store and concurrent logouts), CSRF.

## Residuals

* Not run: hosted CI, full or `--changed` gate, browser, SQL, API suites. The owner selected the targeted tier; actual hosted required tests remain required later.
* Out of scope and unchanged: `token[:-2] + "xx"` in `test_tamper_expiry_and_garbage_denied` is vacuous only if a genuine MAC ends in `xx`. Not claimed as fixed.
* No authentication bypass was found or introduced, and no security acceptance is claimed.
