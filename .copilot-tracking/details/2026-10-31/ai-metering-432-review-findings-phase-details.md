<!-- markdownlint-disable-file -->
# Phase Details: Routed AI metering implementation

* Task: 432-review-findings; parent 432; date 2026-10-31.
* Original contracts and Review remain evidence, not rewritten verdicts.

## P01

Immutable review events carry monotonically increasing output revision and an
optional intent ID. Latest eligible revision as of cutoff determines acceptance.
Review intents commit before non-atomic legacy saves; a completed authoritative
review link supersedes earlier intents for that output. Pending intent without
completion explicitly blocks economic ratios. Same-action replay is idempotent.
Currency invariants are checked at authority, price and admission boundaries;
all intersecting held/unknown liabilities are checked before physical dispatch.

## P02

Use ledger review_intent(output, action) before legacy domain save and
review(output, action, intent=...) afterward. Existing already-reviewed records
may retry only a pending financial link matching their authoritative action;
do not reapply content/domain edits or change a reviewed action silently.
SQL assistant review remains inside its existing authoritative transaction.
Tests exercise the actual adapters and interrupted saves using only constructed
SQLite/loopback transport, with no credentials, private data or paid call.

## P03

Original Review remains Complete / Defects found. Corrections/tests are later
implementation evidence, not independent closure or human approval. A fresh
full gate/receipt is required for the final source/evidence commit and current
main base; unresolved prerequisite failures block publication.

Source preparation is complete: 26 core and nine API composition methods;
requested full API discovery passes 1,439 tests with 320 opt-in skips, and
component Ruff/format/types pass. P03 completion means preparing the committed
candidate, not executing a gate against dirty evidence. Its fresh external
receipt and PR remain the authoritative subsequent publication evidence.
