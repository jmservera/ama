---
title: Issue 1373 resident session opacity test-oracle details
ms.date: 2026-11-10
task_id: 1373-session-opacity-1110
---

## Phase 1 details

Constants on `SessionTests` (found by the single bounded offline search recorded in the research; not searched at run time):

* `NONCE = b"synthetic-nonce!"` (16 bytes) and `COLLIDING_SID = "0000000000000024"`. With `self.key` (`b"k" * 32`), `NOW` as the clock and this nonce, the real MAC of case `C-1` contains `C-1`.

Helper `_issue_with_sid(codec, case_id, sid)`: `mock.patch.object(rs, "secrets", SimpleNamespace(token_hex=lambda _n: sid))` around `codec.issue(case_id)`. Nothing else is patched; `_mac` and `verify` run unchanged.

Rewritten `test_round_trip_and_handle_is_opaque` (random sid, default codec):

* Five dot-separated parts; version `v1`.
* Handle equals `codec.handle("C-1")` and matches `^[0-9a-f]{24}$`.
* `C-1` is absent from the four structural parts (version, handle, expiry, sid); the MAC component is deliberately not inspected.
* Different case gives a different handle; different key gives a different handle for the same case.
* `verify(token)` returns `(handle, sid)` with the sid equal to the token's sid part; the returned expiry equals `int(NOW.timestamp()) + SESSION_SECONDS` and equals the token's expiry part.

New `test_valid_signature_may_contain_case_id_substring` (frozen regression):

* Codec with `self.key`, `self.clock`, `NONCE`; token from `_issue_with_sid(..., "C-1", COLLIDING_SID)`.
* Assert with booleans (no token in failure text) that `C-1` is in the MAC component and not in the structural parts, which shows the old whole-token assertion fails deterministically.
* Recompute the MAC independently with `hmac` and `base64` from key, nonce and body, and assert it equals the MAC part (shows the signature is genuine, not fabricated).
* `verify` returns `(codec.handle("C-1"), COLLIDING_SID)`; expiry equals `int(NOW.timestamp()) + SESSION_SECONDS`; tampering the MAC is still denied (flip one character to a different alphabet character).

Untouched: tamper/version/length/garbage/expiry, restart/key rotation, logout/revocation and CSRF tests, and all production files.

## Phase 3 commands (venv `/tmp/venv-1373-1110`)

From `src/core`:

* `python -m unittest tests.test_resident_showcase.SessionTests -v`
* `python -m unittest tests.test_resident_showcase -q`
* `python -m unittest discover -s tests -q` (Core discovery; the result is reported as run)
* `ruff check .`, `ruff format --check .`, `mypy` (configured, no file list)

From the repository root: `git diff --stat 9e71736bc..HEAD -- src` and `git status --short` to prove production source unchanged and scope limited to the one test file.

The old assertion is exercised against the final file's constants by re-running `/tmp/i1373-1110/red_before.py` (outside the repository).
