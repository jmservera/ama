# Critique: issue 1288 merged-main SQL contract verification plan

Critique read-back `date -u` 2026-11-09T23:23:43Z, before any SQL observation. One independent critique (`rubber-duck` agent, read-only) of the committed research, plan and details at commit `6072bddac`. One critique only; it is not repeated. Verdict: Revise (three blocking, two non-blocking). All findings are compatible with the plan and are applied directly; none conflicts with a confirmed owner decision and none needs a user decision.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | The selected churn test does not restart a service or re-read flag IDs, so C-A restart persistence was claimed beyond its evidence. | Accepted. Add harness H0: after a proactive Quality proposal exists, read the sensor view (reading and sensor IDs), the flag and its cited IDs; build a SECOND `Assistants` over a NEW `MssqlStore` (restart); re-read through the manager and a non-authorised role; compare sets of IDs and the flag. Add the existing restart tests `MssqlCursor.test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts` and `MssqlManualAndProactive.test_a_completed_manual_request_after_a_restart_does_not_allow_another_call` as named evidence. State that the churn test name does not prove restart of IDs. |
| 2 | Calling `ticket.send_fence()` directly does not touch the AI, meter, token or socket, so zero-send counters would be vacuous. | Accepted. Split. H2a: direct `fence_send` observes only the transaction contract (committed event, fresh connection) and claims nothing about counters. H2b: exercise the real `Ai.evidence` path through the lane request with the existing counted TLS peer and counting meter whose `before` hook (the former final-check position) waits, bounded, until the SQL clock passes the authority expiry; the transport fence then refuses. Expected, per the existing process test: meter reserved/checked and token each 1 (the fence follows them), peer accepts 0, bytes 0, envelope `suspended-before-dispatch`. |
| 3 | An expiry refusal could pass for another reason (suspension, release denial, expired lease). | Accepted. Use the SQL Server clock (`service.now`), lease 60 s so the lease outlives the authority expiry, assert no suspension row, and assert the committed event reason text equals the expiry reason (`Operator authority/allowance has expired.`) with the attempt still `reserved`, not `sending`. |
| 4 | The harness class inherits lane tests whose subprocess opens SQLite. | Accepted. Select ONLY the harness methods by explicit test id; no inherited lane test is run on SQL Server. |
| 5 | Physical slot reacquisition is an in-process semaphore, not a database readback. | Accepted. Test it locally and label it as in-process; durable attempt and allowance state is read separately through a fresh raw connection. |

## Residual risks recorded before observation

* The harness reuses `Lane` fixtures that build their simulation lane store as SQLite by design; only the working store is SQL Server. This is stated in the evidence; it is not a SQL lane-store proof.
* A harness error attributable to the fixture is classified inconclusive, never a pass.
* The clock for the expiry wait is the SQL Server clock, the same source `Assistants.now` uses.
