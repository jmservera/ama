# Plan: issue 1288 E6

Task `issue-1288-e6`, parent `issue-1288-e5`. Start `5271d62fa`; main `5c3b8b4be`. Research: `.copilot-tracking/research/2026-11-09-quality-sensor-demo-1288-e6-research.md`. Details: `.copilot-tracking/details/2026-11-09-quality-sensor-demo-1288-e6-details.md`. Tier: owner-selected demo-targeted (modified and impacted checks, no blanket gate); mixed change takes the strictest applicable of that tier.

## Order (research, plan, independent critique, commit, THEN main merge, THEN source)

1. Commit research, plan, details and the independent critique before any main merge or source edit.
2. Ordinary `git merge origin/main` into this branch (no rebase, amend or force). Keep both intents; simulator controls (#1313) and quality simulation are distinct routes. Stop on ambiguous conflicts and report.
3. Failing-first: two-process short-lease-stall and authority-expiry-before-send regressions (counted local TLS socket), plus the complete endpoint inventory.
4. Implement F1 (fence) and F2 (inventory).
5. Reconcile type safety under the pinned profile against green main (no suppression, cast, stub or config relaxation).
6. Targeted validation, one non-queued SQL admission only if free, original review, state and changes artifacts, handoff.

## Phases

* P1 Merge: record main SHA, conflict list, resolution per file; post-merge smoke of simulator-controls and simulation tests.
* P2 F1 fence: `Assistants.fence_send`, `Ai` send fence (connection subclass, margin, total deadline), `ai_consumption.SEND_FENCE`, `Lane.request` wiring and fail-closed support check. Two-process tests: A stalls after `begin` beyond a short lease while B reuses the slot and sends; A resumes and must not send; peer counts show one send, no overlap. Authority expiry between admission and send: no socket. Valid bounded simulation still works; slots and token accounting settle once, including failure.
* P3 F2: add `/api/assistants/simulation/quality` GET and `/observe`, `/request` POST with the public fixture payload and per-role expectations to the existing inventory; keep discovery and assertions intact.
* P4 Types: after the merge measure core and api mypy against main's baseline; fix real type errors in `sensor_consumer.py`, `sensor_view.py` and the two quality-sensor test modules by annotation, with no suppression. If the volume proves a broader scope than E6, report it clearly rather than relax.
* P5 Validate and hand off.

## Constraints

* No push, PR, issue, board, merge to main, cloud, live or model calls; no private data, `.env` or credentials; no global install.
* Private captured route stays OFF; public fixture, store and exact serialized body seal unchanged; resident, consent, human-quality, manual, release and cost safeguards retained.
* Web code only if needed: fetch current web guidelines first; Fluent 2, ASCII, native semantics.
* Heavy services: one non-queued `flock -n` admission; busy means record validation pending and stop, never wait. The 1292 SQL campaign owns its own admission; do not reuse its results.

## Acceptance

* Two-process tests fail on unchanged source and pass after the change; no late send, no excess overlap, finite accounting.
* Inventory test passes with all three routes; no waiver.
* Pinned mypy reconciled and recorded honestly; ruff and format clean on changed files.

## Amendments after the independent critique (verdict: rework; all findings dispositioned, see the critique artifact)

* A1 (High 1, residual freeze): residual named explicitly, not called microsecond; fence is two checks (request start, before the first byte); live provider needs an owner decision.
* A2 (High 2, other dispatchers): the same fence is wired into the ordinary `execute` path, which shares the cap and `_reserve`.
* A3 (High 3, transport): fenced requests use a private opener with only the fenced HTTP/HTTPS handler, `HTTPErrorProcessor` and `UnknownHandler` (no proxy, no redirect, no retry); `Connection: close`; the fence runs once per connection before the first `send`; total-deadline timer shuts the socket down; tests for multi-send, trickle read and refused redirect.
* A4 (Medium 4): split `disabled` into a current-authority check and the new-reservation capacity check; the fence uses only the former, so a valid reserved call is not refused by its own debit.
* A5 (Medium 5): valid bounds (lease 10 s minimum, timeout 5, lease >= timeout + 5); assert request bytes and bodies, not accepts, for the pre-send stall; counters zero only for a stall before the request starts; explicit event synchronisation between processes.
* A6 (Medium 6): the request-start fence runs before data hold, meter and token, so a late caller creates no financial reservation; the pre-send refusal keeps the existing conservative `dispatch_check` completion semantics and is documented.
* A7 (Medium 7): the fence is a method of the same `Assistants` that admitted (same store identity by construction); one clock domain (the database clock) is part of the stated boundary; restamp-versus-reclaim tested on SQLite locally and in the owned SQL run when admitted.
* A8 (Low 8): inventory asserts every role on all three routes; all new code (transport, worker, tests) is included in the pinned mypy and ruff results.
