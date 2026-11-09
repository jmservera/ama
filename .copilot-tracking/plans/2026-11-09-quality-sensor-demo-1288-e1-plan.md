---
title: Quality sensor demo 1288 E1 plan
ms.date: 2026-11-09
---

Written 2026-11-09T08:50Z after the E1 research and before any E1 source edit. Refs #1288, #107. No closing claim. Owner-selected demo-targeted validation (no full gate). E1 is the first of up to five additional authorised cycles (4 remain after it).

## Phases

* [ ] P1 Reproduce: add focused regressions F1-F6 and run them against unchanged source; record which fail. A hypothesis that does not fail is recorded as not reproduced and not fixed.
* [ ] P2 F2/F1 control plane: gate-aware control triggers (SQLite and SQL Server, in-place upgrade), changed-only `configure()` writes.
* [ ] P3 F1 transport: chunked, deadline-bounded sends; non-bytes bodies fail closed; foreign provider policy; API wiring declares the real transport.
* [ ] P4 F3 manual request never rewrites the Quality slot. F4 bounded adoption with explicit incomplete marker. F5 durable `seen` evidence digest and migration.
* [ ] P5 F6 unknown comparison and UI wording (`assistants.js`).
* [ ] P6 Browser check (AC7) with isolated Playwright and axe, after verifying absence.
* [ ] P7 Validation: SQLite/loopback suites, real disposable SQL Server (zero skips) under the nonqueued heavy lock, ruff and type checks that already exist.
* [ ] P8 Changes, one author Review, state, handoff, commit with privacy-safe identity.

## Scenarios (each becomes a regression that fails before its fix)

* S1 (F2) With a live gate row for a home, a direct `UPDATE`, `DELETE` or `INSERT` of that home's control is rejected and consent stays granted; for another home it commits; after the gate is released or expired it commits. SQLite and SQL Server.
* S2 (F1) A fake transport that blocks inside a send beyond the send-by time is interrupted by the bound and no further bytes leave; a body larger than one chunk is re-checked per chunk; a provider that neither honours the gate nor declares `sends_no_bytes` is never given captured readings (outcome `suspended-before-dispatch`, manual route, no call, no allowance beyond the claim); the API composition reports the real `Ai` transport as fenced.
* S3 (F3) Proactive A serviced, manual B for a different exact capture, then reading C in the same bucket: a scan enqueues nothing; also with B pending and completed, after a service restart and after a release or epoch change.
* S4 (F4) More than five newer manual and other-release tasks precede a serviced task for a change-only capability: the serviced task is found and the current change is enqueued once; when the cap is reached the slot is `incomplete-history` and the current work is enqueued once, not hidden; a restart repeats neither.
* S5 (F5) After three stale-before-claim replacements, readings that keep changing across several quiet intervals create no recovery task and no new task rows; after one unchanged quiet interval (and across restart) recovery creates one task.
* S6 (F6) With the current sensor read failing, consent-withheld, and a real removal: failing and withheld give `unknown` and null newer count; the real removal still reports missing and changed.

## Controls kept

Monitoring consent, human quality decisions, role denial, manual routes, finite attempts, tokens, expiry and freshness, no real model call, synthetic data only, no unmerged sibling import.

## Out of scope

Rewriting C1-C7 or C8, publication, live walkthrough, production hardening, #1292 and #184 integration.

## Stop rules

Any selected test that fails is not waived. If SQL Server is busy under the shared lock, record blocked and do not queue. At most this one E1 correction; residual High findings are reported, not hidden.

## Amendment A1 (after the independent critique, 2026-11-09T09:05Z, still before any E1 source edit)

Critique: [challenges/2026-11-09-issue-1288-e1-plan-critique.md](../challenges/2026-11-09-issue-1288-e1-plan-critique.md). Changes to the plan:

* S2: sends use an explicit partial-send loop with remaining time recomputed before each `sock.send`; the timeout is restored in `finally`; the API provider lambda resolves `store.ai` once and refuses an active gate for a non-honouring object.
* S3: also a scan between manual B and reading C with a persistent gap; `_due` never lets an exact manual task re-occupy a serviced Quality slot.
* S4: a reached cap writes `incomplete-history`, which blocks autonomous work and is reported by `scan()`; it does not enqueue (supersedes "treated as changed").
* S5: `replaced` resets and replacement/pause decisions are bound to the slot's own task; forecast uses `observe=False`; a hard resume after `COALESCE_MAX` keeps work from starving.
* S1: add the two-connection ordering test (writer open, then gate request) on both stores.
