---
title: Issue 1288 E1 plan critique
ms.date: 2026-11-09
---

Critique executed once by an independent read-only rubber-duck agent at 2026-11-09T08:58Z over the E1 research, plan and details and current source. Verdict: Revise (6 High, 1 Medium reported as 5 High, 2 Medium by content). It is not repeated. Dispositions are applied directly to the plan and details (amendment A1) because none conflicts with an owner decision.

| # | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | High | TLS `sendall` re-arms its timeout per partial send, so a chunk can outlive the deadline. | Accepted. Own partial-send loop: recompute remaining time before every `sock.send`, restore the original timeout (including `None`) in `finally`. Test a trickling peer and response read. TLS is covered on the loopback plain socket only, stated as a limit. |
| 2 | High | F3: skipping manual `_occupy` is not enough; `_due` returns true for an existing exact manual task and the proactive `_enqueue` then occupies it. | Accepted. For `quality-evidence`, when the slot is serviced and the exact task is not the slot's own task, `_due` returns false. Test a scan between manual B and reading C with a persistent gap. |
| 3 | High | F4: forcing an autonomous call at the cap can duplicate hidden same-bucket history and treats unknown history as change. | Accepted. A reached cap writes an explicit `incomplete-history` marker that blocks autonomous work for that case and capability (manual route unaffected) and `scan()` reports it. It never counts as changed and never enqueues. Plan scenario S4 changed accordingly. |
| 4 | High | F5: a claim resets `replaced` for the whole case and `_replaceable`/`_paused` ignore slot ownership. | Accepted. Resets and replacement or pause decisions apply only when the slot task is the task concerned. Test overlapping old and new claims. |
| 5 | Medium | F5: sampled signatures cannot prove uninterrupted quiet; the forecast calls `_due` and would mutate debounce state. | Accepted. The forecast passes `observe=False`. Sampled quiet (a change and revert between scans) is a stated residual, not claimed closed. |
| 6 | High | F2: tests do not prove transactional ordering; SQL Server `THROW` differs from SQLite. | Accepted. Add a two-connection ordering test (open withdrawing writer, then gate request) beside the committed-gate test, run on both stores, and verify rollback, trigger upgrade and unchanged-home configure on the real SQL Server. |
| 7 | Medium | F1: bind the capability check to the provider actually called. | Accepted. The API lambda resolves `store.ai` once and refuses when a dispatch gate is active and that object does not honour it. |

## Residuals kept after the critique

* A thread or process suspended between the last in-process check and the kernel send for longer than the margin cannot be excluded in userland.
* Sampled quiet detection can miss a change that reverts between scans.
* TLS behaviour is unit-bounded on a plain loopback socket, not proven with a real TLS peer.
