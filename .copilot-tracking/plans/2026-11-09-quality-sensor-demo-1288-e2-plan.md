---
title: Quality sensor demo 1288 E2 plan
ms.date: 2026-11-09
---

Written 2026-11-09T10:20Z after the E2 research and before any E2 source edit. Refs #1288, #107. No closing claim. Owner-selected demo-targeted validation (no full gate). E2 is the second of the five additional authorised cycles after C1-C8; three remain after it. Base: local merge of `origin/main` `1f28d09130c8e058a0436d468e6a22f3c4c24f47` into E1 head `21763da2`.

## Phases

* [ ] P1 Reproduce: add focused E2 regressions and run them on unchanged source; record failures. A hypothesis that does not fail is recorded as not reproduced.
* [ ] P2 F1 boundary: real `Ai` refuses captured readings before any reservation, token or socket; assistant dispatch holds before provider hand-off with the manual-route text unless the carrier is not `Ai` and declares `sends_no_bytes`; API composition applies the same policy; remove the unreachable fence machinery; rewrite the DispatchGate docstring to its true, narrower claim.
* [ ] P3 F3: side-effect-free adoption; non-observing callers never write `assistant_schedule` or `self.incomplete`.
* [ ] P4 F2: durable keyset cursor for incomplete adoption, resume per scan within the unchanged cap.
* [ ] P5 F4: truthful wording in `assistants.js` and a `basis` field; update the browser check expectations.
* [ ] P6 Web: load `web-design-guidelines`, fetch every current rule, review the changed web file; browser and axe check (engineering only).
* [ ] P7 Validation: affected SQLite/loopback modules, affected SQL groups on an owned disposable SQL Server under the nonqueued lock, pinned ruff and mypy with normalized baseline-versus-head diagnostics.
* [ ] P8 Changes, one independent-quality author review, state, handoff, commit with the privacy-safe identity.

## Scenarios (each becomes a regression)

* S1 (F1, enforced boundary) With a real `Ai` client whose endpoint is an actual TLS peer and a captured-readings quality task: the production `execute` path makes zero connections and sends zero bytes; the outcome is `suspended-before-dispatch` with the manual-route text; no provider hand-off and no allowance beyond the claim. Controlled suspension at the former final-check point plus a withdrawal and gate expiry committed by another process: still zero bytes, withdrawal never waits. Calling `Ai.evidence` directly inside the captured-readings context is refused before the meter and token. Control: the same TLS peer with a trickling (partial-receive) reader still completes an ordinary non-captured request, so zero is not a vacuous result.
* S2 (F1 composition) The API composition with a real `Ai` holds captured-readings tasks; a mock carrier declaring `sends_no_bytes` still works; a carrier that does not declare it is never given the data.
* S3 (F3) Fresh store and a legacy store (tasks, no schedule rows): a forecast leaves every `assistant_schedule` row, `assistant_tasks`, events, `incomplete` and `scan_cursor` identical; the following scan still adopts. With a persisted incomplete row the forecast leaves it untouched. SQLite and SQL Server.
* S4 (F2) A qualifying serviced task behind 120 newer manual tasks at the unchanged `ADOPT_ROWS`/`ADOPT_PAGES`: scan 1 is incomplete and visible, scan 2 (also after a restart) adopts it with no new autonomous call; no repeated prefix (each scan reads rows strictly after the stored cursor); an unrelated change is still enqueued once. A history longer than three scans completes in bounded scans. SQLite and SQL Server.
* S5 (F4) After enough same-bucket arrivals the cited rows leave every selected array while their `sensor_reading` rows remain unchanged; the flag says changed, `basis` names the bounded capture, nothing claims deletion. Real deletion and unavailable captures keep their existing results.

## Controls kept

Monitoring consent, human quality decisions, role denial, manual routes, finite attempts, tokens, expiry and freshness; synthetic data only; no real model call; no unmerged sibling import; Fluent 2, plain language and WCAG controls in the UI.

## Out of scope

Provenance architecture, a lease-enforcing egress proxy, permanent real-AI sensor grounding, rewriting C1-C8 or E1 evidence, publication, live walkthrough, #1292 and #184 integration.

## Stop rules

A failing selected test is not waived. Shared SQL lock busy: record blocked, do not queue. If a safe correction needs #1292 code, stop and report. Any materially different runtime, provenance or consent strategy needs a scoped owner decision.

## Amendment A1 (2026-11-09T10:30Z, after the one independent critique)

Critique: `.copilot-tracking/challenges/2026-11-09-issue-1288-e2-plan-critique.md` (Revise, five findings, none conflicts with a confirmed decision, all applied directly; no second critique).

* A1.1 Worker bypass (High, accepted): `agents/dispatch.py` `_bounded.call` sets the same captured-readings context when the task captured sensors, so the separate worker never hands readings to a real `Ai`. Test `handle` and a redelivery with a real `Ai` against the TLS peer.
* A1.2 Chat and direct calls (High, partly accepted): `chat_panel.py` contains no sensor or reading data path (searched), so no captured readings reach it. Free text pasted by a person cannot be classified without inferring provenance, which the owner excluded; the boundary is stated as covering assistant dispatch and the agents worker only, with free-text chat and direct `Ai` use disclosed as residual and an owner-decision item. A test records that `Ai` used outside the context is unchanged.
* A1.3 Cursor ordering (Medium, accepted): `dispatched` is rewritten on retry, so it is not a stable keyset. Phase one (no cursor) is the unchanged newest-first 100-row read. An incomplete slot then walks the immutable primary key `id` in pages from the stored cursor (`task_id`), adopting the first qualifying task; the walk covers each row once and terminates. Documented: after the first window the adopted task is the first qualifying by id, not necessarily the newest. Tests: retry during the walk, ties, restart, SQL Server `OFFSET/FETCH`-free keyset (`id > ?` with `ORDER BY id`).
* A1.4 Forecast release writes (Medium, accepted): `assessment` reaches `invalidate_changed` which writes release rows and events. A context-local read-only flag makes forecast assess without `change()`. Test compares release rows and event contents including a mismatched (would-be revoked) release.
* A1.5 Vacuous suspension test (Medium, accepted): the old-race reproduction runs only against unchanged source (logged). The new tests assert the refusal precedes every hook (zero `dispatch_check`, `reserve`, `_token` calls, zero connections and bytes), plus a positive control proving the TLS peer is reachable and the hook points are reachable on a non-captured call.
