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

P03 source validation, documentation reconciliation and final-candidate
preparation are complete. The full exact-head publication gate must execute
after this evidence is committed. These are correction/test observations,
not independent closure or a replacement Review verdict.

## Current-Base and Documentation Reconciliation

Main advanced to a75bbdffa51ae34b1fcf779250f1f553d566ee93 through #558
without changing cost/runtime source. Its capstone move makes the older brief
historical and generated Q&A source-manifest-owned. Non-rewriting topic merge
3c15ebfb retained both index entries and log histories, restored the archived
brief to byte-identical main, and routes source-only drafting through the
existing Tokenomics synthesis/current source guide. No historical source,
generated deck/question bank, actual financial figure or approval is rewritten.

Core/API guidance now explains latest/as-of withdrawal, shared dispatch holds,
deferred currencies, durable pending review joins and matching retry recovery.
An append-only knowledge log entry records the prospective correction. Original
research, critique, implementation changes and independent Review hashes remain
unchanged, verified with an external preservation manifest.

## Final Local Validation

* Core: 26 tests; complete Ruff check/format and mypy (170 files) pass.
* Agents: 21 existing dispatch/chat tests; complete Ruff check/format and mypy
  (24 files) pass.
* API: complete Ruff check/format and mypy (124 files) pass. From src/api,
  the exact requested PYTHONPATH discovery passes 1,439 tests in 731.668s,
  with 320 opt-in skips; log /tmp/ai432-api-corrected-final.log. The required
  full gate must independently exercise its actual SQL/browser groups.
* Local SQL driver libraries and Chromium headless startup/evaluation were
  checked successfully. These prerequisite probes are not actual SQL semantics
  or application UI acceptance; the mandatory full gate still owns those checks.

Git publication identity was checked on task-owned first-parent commits. An
initial identity probe incorrectly included upstream commits; corrected task-only
selection confirms privacy-safe author/committer values without displaying emails.
No existing commit was amended.
Changed documentation introduces no missing relative file targets. A whole-file
check also found 19 inherited missing occurrences in the index/append-only log;
comparison with current main distinguishes these from the new links, and does
not rewrite historical log entries or unrelated presentation content.

## Candidate and Publication Boundary

P03 is reconciled to final source/evidence preparation, not a claim that an
uncommitted candidate passed the full gate. The repository requires committing
implementation and original evidence first, then running and verifying a fresh
external receipt at that exact HEAD/current main base. Committed state is this
pre-publication snapshot; the final external receipt and PR are the publication
evidence. No passing receipt, hosted approval or independent correction closure
is claimed here. Original adverse evidence and operational RV-006 gaps remain.

## Publication Gate Attempt: Blocked

Final committed candidate a9fa353ae798da1712970679c967b73d708f06e4 was
fast-forwarded into the clean task-owned external clone
/tmp/ama-ai-metering-432-publish-2026-10-31-a. Its tracked/untracked/ignored
input checks were empty; fetched main remained
a75bbdffa51ae34b1fcf779250f1f553d566ee93.

Command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 600 --base a75bbdffa51ae34b1fcf779250f1f553d566ee93 --out /tmp/ama-ai-metering-432-final-gate-2026-10-31-a`.
It exited 1 with `BLOCKED: Global heavy-resource lock timeout`. No Runner
group started and no receipt was produced. The failed attempt's external
directory/log are preserved; log /tmp/ai432-final-gate-run.log.

Read-only lock metadata identifies python3 PID 2927070 as the WRITE holder of
/tmp/ama-rpi-heavy.lock; flock PIDs 2931030 and 2953505 were waiting on that
holder. No foreign process, output, container, dataset or worktree was touched.
The attempt used a 600-second wait; the current src/README.md shared-resource
policy requires nonqueued admission, no duplicate/waiting gates or release
polling, and a later explicit coordination event before retry. No further
gate is queued or launched.

Publication is blocked, not passed: actual full SQL/browser/container/scanner
groups and exact-head receipt verification remain unexecuted. Push/PR have
not occurred. On a later explicit coordination event with ownership free,
reconcile freshly fetched main, fast-forward the clean clone to the new final
evidence commit, run the full gate with --lock-timeout 0 and a new external
directory, then fetch/verify immediately before authorised push/Refs #432 PR.
This failure record changes candidate identity and requires a new gate; the
earlier requested source tests/static checks are unchanged-source evidence.
