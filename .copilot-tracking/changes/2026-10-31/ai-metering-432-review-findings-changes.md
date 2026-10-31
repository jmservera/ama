<!-- markdownlint-disable-file -->
# Routed Implementation: AI metering Review findings

## Identity and Accepted Direction

* Task: 432-review-findings; parent task 432.
* Date: 2026-10-31.
* Original Review: .copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-review.md.
* Original plan/details and PC-001..008 contracts are reused; no new decision,
  deployment, paid call, repeated critique or repeated Review is authorised.
* Original Review execution Complete / outcome Defects found remains unchanged.
  This later implementation records corrections and tests, not review closure.

## Required Corrections

* RV-001: append immutable review revisions; preserve idempotency and latest
  disposition at the report as-of cutoff, including human withdrawal.
* RV-002: shared held/unknown budget liabilities govern the post-token
  pre-network check, not only original reservation.
* RV-003: unresolved shared currencies cannot admit conflicting authority or
  later price registration; admission checks remain fail closed.
* RV-004: durable pre-save review intent makes lost legacy review links visible
  and blocks economics; retry can recover the link from authoritative review.
* RV-005: parameterized actual assistant/legacy/priority/chat/worker/fence
  compositions cover identity/cached usage/output eligibility and failures,
  within the original two-module/35-method cap.

## Execution and Validation

P01 complete: 26 core methods pass, with complete core Ruff check/format and
strict mypy (170 files). New tests cover shared post-token holds, interrupted
review attribution/replay, deferred-price currency order and historical
acceptance withdrawal. An initial new collection inference type error was
fixed explicitly; its adverse result is retained here.

P02 complete: only ai_tasks.py, store.py and test_ai_consumption_api.py changed
within its delegated boundary. Legacy and priority JSON/SQL reviews commit
pre-save intents and recover matching authoritative dispositions without
reapplying content/domain edits. Interrupted saves/output/review links remain
visibly incomplete and do not qualify economics.

Actual loopback compositions cover metered assistant withdrawal, post-token
denial with zero later dispatch, legacy/priority recovery, chat ineligibility
and cached/identity provenance, worker failure/revocation/stale-fence settlement.
The phase returned 76 passing focused/regression tests and a final nine-method
API run; complete core/API Ruff/format and standard API mypy passed. Two narrow
import suppressions document the agents package's missing py.typed boundary.
The original two-module limit remains: 26 core + nine API = 35 new methods.

P03 final requested discovery, documentation reconciliation and publication
gate remain pending. These are correction/test observations, not independent
closure or a replacement Review verdict.
Original discovery/static successes do not resolve these findings.
Final requested checks and the complete external publication gate remain required.
Original adverse evidence and all operational RV-006 gaps are preserved.
