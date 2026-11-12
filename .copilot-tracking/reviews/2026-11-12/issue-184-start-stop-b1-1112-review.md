<!-- markdownlint-disable-file -->
# #184 stage B1 start/stop retry enforcement: original author Review (2026-11-12)

Execution: ONE Review by the authoring session, once, after implementation. It is NOT independent; the coordinator's independent exact-head review remains required before any publication. No second Review is run in this task.

Boundary: the diff of `live_simulator.py`, `live_control.py` (docstring), `test_live_simulator.py`, `test_live_control.py` against the [plan](../../plans/2026-11-12/issue-184-start-stop-b1-1112-plan.md), [critique](../../plans/2026-11-12/issue-184-start-stop-b1-1112-critique.md) and [changes](../../changes/2026-11-12/issue-184-start-stop-b1-1112-changes.md).

## Outcome

Candidate complete for the admitted single-instance B1 read/revalidation; no blocking defect found by the author. Not a conformance, acceptance or approval statement.

| Check | Result |
| --- | --- |
| Control revalidated before every actual send attempt including retries, after pacing and backoff | Implemented and tested |
| Stop, expiry, over-window, unreadable or corrupt control, removed home, gate error each prevent later sends | Tested (unit and through `main`) |
| Defaults without a control file unchanged; open gate identical to no gate | Tested; existing 65 tests still pass |
| Rate, batch, retry and backoff semantics preserved | Held (open-gate equivalence test) |
| No remote cancellation or instantaneous termination claimed | Held; in-flight send is not interrupted |
| Out of scope untouched (schema, SQL, Bicep, guard, B2, D1 to D6) | Held |

## Open items and limits

* Author review only; independence is absent.
* Single process: another replica is not fenced (B2 deferred, not approved). A stop written between the per-attempt read and the send still lets that one attempt through; a send already handed to the sink is not recalled.
* Per-process attempt cap (proposal row) not implemented, not admitted.
* A home removed from the store (as opposed to the control cohort) mid-slot is not rechecked per attempt.
* Per-attempt read adds a small local file read; bounded by cohort cap 100 and the rate limit.
* The stream-chronology discrepancy stays Medium and qualified; unknown historical balances remain unknown; no live Hub, timing or cost behavior was observed.
* No hosted CI applies to this local-only candidate; the complete gate was not run (behavior-preserving, non-deployment, no infra or permission change; classification: focused tier, basis recorded here, doubt resolved by the coordinator's review).

## Routing

Later work, user-selected only: independent exact-head review, then owner decisions on B2, attempt cap and live handoffs. Nothing returns to Implement or Review in this task.
