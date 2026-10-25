# Phase details: corrections (issue 462)

Written 2026-10-25 before critique and implementation.

## A. Limiter key
* `client_key(peer, xff_values, mode)` in `resident_showcase.py`: mode `peer` returns peer. Mode `ingress-rightmost` joins all `X-Forwarded-For` lines, takes the last comma entry, strips it, parses with `ipaddress.ip_address`, returns the canonical string; any failure returns peer.
* `config_from_env` reads `ZF_DEMO_CLIENT_ADDRESS`; `ShowcaseConfig.client_address`; `app.py` takes it and calls the resolver with `headers.get_all("X-Forwarded-For")`; `__main__` passes it.
* Tests in `test_resident_showcase.py` (resolver and config) and `test_resident_demo_api.py` (real socket: spoofed prefix cannot evade, two clients independent, default ignores header).

## B. Stale email
* `IdentityMap.email_for` reverse map; `authorise` gains a required `expected_email`; `login` and `view_for` pass the map email; login passes canonical typed email through the map lookup already.
* Tests: DB email changed after start denies login and a live session; unchanged passes.

## C. Verifier tool
* `core/verifier_tool.py` with `check_strength(password) -> str|None` and `build_verifier(password)`; `tools/resident_demo_verifier.py` main with injectable `getpass`.
* Tests with fake constants only; test for tty refusal, mismatch, weak, output contains no password text.

## D. Docs and evidence
API/core README lines, changes artifact, one review, state, local commit.
