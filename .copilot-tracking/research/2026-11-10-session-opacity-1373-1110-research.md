---
title: Issue 1373 resident session opacity test-oracle research
ms.date: 2026-11-10
task_id: 1373-session-opacity-1110
---

<!-- markdownlint-disable-file -->

## Disposition and scope

Research executed 2026-11-10 from 09:22Z, before any edit. Disposition: `executed`. Planning Readiness: Ready.

Scope is the Core test oracle `SessionTests.test_round_trip_and_handle_is_opaque`, one directly coupled deterministic regression and RPI evidence. No production code change. This research establishes no authentication bypass and grants no security acceptance.

## Ownership check (stop rule)

* `git log -S handle_is_opaque -- src` returns only the creating commit `55c239d90` (#463). No earlier repair of this assertion exists in source history.
* `grep handle_is_opaque` over `.copilot-tracking` and `docs` returns no record. No existing exact owned or exhausted attempt is found, so the stop rule does not apply.
* Root reported 127 bodies, fresh #189/#462 comments and repository comment searches with no owner. #189's API consumption failure is a different test. This task did not repeat those GitHub searches.

## Token contract (read from `src/core/src/zava_forward/core/resident_showcase.py`)

* `SessionCodec(key, expires_at, clock, nonce)`: key at least 32 bytes; nonce defaults to `os.urandom(16)` and is injectable.
* `handle(case_id)`: first 24 hex characters of HMAC-SHA256(key, `handle|` + case id). Keyed, hex only.
* `issue(case_id)`: `v1.<handle>.<expiry>.<secrets.token_hex(8)>.<mac>`; expiry is `min(now + 1800, authority end)`; the only randomness is `secrets.token_hex(8)` and the default nonce.
* `_mac`: URL-safe base64 (43 characters, alphabet `A-Za-z0-9_-`) of HMAC-SHA256 over purpose, nonce and body. It is independent of the case id and uses the alphabet that contains `C`, `-` and `1`.
* `verify`: five parts, version `v1`, length under 256, constant-time MAC comparison, expiry/authority cutoff and revocation; returns `(handle, sid)`.

## Finding

The old assertion `assertNotIn("C-1", token)` treats any three-character substring of the URL-safe MAC as a leak. A genuine MAC contains a given 3-character string at a roughly 41 / 64^3 (about 1 in 6,400) rate per token, so the test fails randomly on valid tokens. The meaningful opacity property is that the case-bearing handle is a keyed hex digest that does not contain the case id and separates cases, not that no independent encoding can contain that string.

## Baseline evidence (offline, before edits)

* Environment: own venv `/tmp/venv-1373-1110`; `zava-forward-core` editable from this worktree; ruff 0.17.1 and mypy 2.4.0 (the `[dev]` pins), Python 3.12.3.
* One bounded offline search (`/tmp/i1373-1110/search.py`, limit 2,000,000) used the real unchanged `issue`/`verify` with key `b"k" * 32`, clock 2026-10-25T12:00Z, nonce `b"synthetic-nonce!"` and the module's `secrets` replaced by a stub returning a fixed sid. It found the first match at attempt 37: sid `0000000000000024`, MAC index 15 of 43. No `_mac` or `verify` mock, no fabricated MAC.
* Real `verify` accepted the token: handle equals `codec.handle("C-1")`, sid equals the fixed sid, expiry is NOW + 1800 s.
* The unmodified old assertion fails on this token deterministically (`/tmp/i1373-1110/red-before-redacted.log`, raw log kept outside the repository as `raw-red-before.log` because the assertion message echoes the token; neither raw file is committed).
* The existing nine `SessionTests` pass on unchanged source (random sid; passing is not evidence of correctness).

## Selected approach

* Patch only the sid random source for the test (`secrets` name in the module, with `unittest.mock.patch.object`), keep real `issue` and `verify`, use the existing test key and clock plus an explicit nonce.
* Replace the whole-token absence assertion with structural checks: five parts, `v1`, handle is 24 lowercase hex characters equal to the keyed handle, handle does not contain the case id, a different case gives a different handle, a different key gives a different handle, expiry and sid round trip.
* Keep a frozen collision regression: the fixed token genuinely contains `C-1` in the MAC component only, verifies, and returns the correct handle, sid and expiry. A boolean assertion with a fixed explanation avoids echoing the token.
* Rejected: a runtime search or retries, biasing the sid or alphabet, mocking `_mac` or `verify`, production edits, skips.

## Risks

* The patched module attribute is global to the module during the `with` block only; other tests do not run concurrently within the case.
* The frozen sid is tied to the synthetic key, clock and nonce constants; the regression asserts them explicitly so a drift fails loudly rather than silently losing the collision.
* The adjacent `token[:-2] + "xx"` tamper case in another test can pass vacuously only if the MAC already ends in `xx`; this is out of scope (no unrelated cleanup) and recorded as a residual.

## Follow-ups

None evidence-grounded beyond the residual above.
