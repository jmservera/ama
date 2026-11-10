# Plan: issue 1288 E7

Task `issue-1288-e7`, parent `issue-1288-e6`. Start `56d0bdc33`; main `2be660e9d` (no merge). Research: `.copilot-tracking/research/2026-11-09-quality-sensor-demo-1288-e7-research.md`. Details: `.copilot-tracking/details/2026-11-09-quality-sensor-demo-1288-e7-details.md`. Tier: owner-selected demo-targeted (modified and impacted checks, no blanket gate), plus the complete configured lint, format and strict mypy profiles for Core and API.

## Order

1. Commit research, plan, details and the independent critique before any source edit.
2. Failing-first: production-App real-Ai route refusal regression; loopback TLS deadline regressions (Connection: close, persistent, trickled body).
3. Implement H1 (code-disabled real-provider route) and H2 (response-owned deadline), fix the two E501.
4. Re-label lane plumbing tests that use a real `Ai` over a local peer as scripted plumbing.
5. Run complete lint, format and mypy per profile with explicit exits; targeted suites; decide SQL by diff qualification.
6. Original review of both High dispositions and lint, state and changes artifacts, handoff.

## Phases

* P1 H1: `Ai.send_fence_supported = False` (the production client never advertises a guarantee it cannot establish). `Lane.request` refuses a real `Ai` with reason `real-provider-route-unavailable` after the configured check and before `compose`, `admission.begin`, mint, credential, reservation or socket; the result keeps the manual route and fixture labels and is never presented as AI output. No environment variable, setting or request field can set the capability. A source-level regression asserts no production source assigns it True. The ordinary assistants path is unchanged and makes no claim of this guarantee. Scripted plumbing tests set the capability on an instance with a comment that the peer is a local counted socket, not a provider.
* P2 H2: replace the timer arrangement in `ai_transport.py`. `Window` takes a stable shutdown handle (the connected socket object) at first byte and is cancelled by an explicit `finish()` called from a response wrapper's `close()`, `read` exhaustion or failure; `HTTPConnection.close()` no longer cancels it. A small response proxy returned by the handlers owns `finish`. A leaked-operation assertion: after the call completes or fails, no live timer thread and no open socket remain.
* P3 Lint: wrap the two E501 lines; run `ruff format` on `sensor_consumer.py` only if it makes no unrelated rewrite beyond the reported diff.
* P4 Profiles: API profile in `.venv-1288` (core[sql,blob]); Core SDK-free profile in an owned `mktemp -d` venv with `-e src/core[dev]` only; record exits for `ruff check .`, `ruff format --check .`, `mypy`, unit tests where relevant.
* P5 Validate and hand off: targeted suites listed in details; SQL by qualified reuse or one non-queued admission.

## Constraints

* No push, PR, issue, board, cloud, live or model calls; no private data, `.env` or credentials; no global install; no new broker, proxy or provider; no cast, ignore, stub or config relaxation.
* Private captured route stays OFF; public fixture, store, key and exact-body seal unchanged; resident, consent, human-quality, manual, release and cost safeguards retained. Financial reservation, meters, uncertain liability and manual-failure semantics unchanged.
* No web source edits unless needed; then load the current web guidelines first.
* Heavy services: one non-queued `flock -n` admission only if SQL is needed; busy means record pending and stop.

## Acceptance

* Production App with a real `Ai` refuses the simulation request before credentials, reservation and socket (counted), with the manual route kept.
* Fenced transport deadline holds across headers and body for Connection: close and persistent responses; no leaked timer or socket.
* Complete Core (SDK-free) and API profiles: ruff check, ruff format --check, mypy all exit 0.
* The real-provider route stays an explicit residual; no claim that a transport-side atomic guarantee exists; AC remain unmet for the actual real-model chain.
