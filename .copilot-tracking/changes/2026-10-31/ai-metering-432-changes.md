<!-- markdownlint-disable-file -->
# RPI Changes: AI consumption economics

## Metadata

* Task ID: 432
* Date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md

## Execution Status

P01/P02 source, documentation and local unit/static validation are complete.
Original Review and the separate post-Review publication gate remain pending.
Approved writes are src and directly related evidence/docs only.

## Execution Summary

One critique executed Revise; eight compatible corrections applied as explicit
identity/privacy/admission/billing/quality/test contracts. Original verdict retained.
No deployment, credential, private-data, paid model or Azure action is authorised.

## Completed Work

* Closed ai-consumption-v1 events in the existing immutable assistant ledger.
  Serialized admission intersects durable call/depth/token/currency budgets,
  preserves unknown liabilities and emits workflow-only owned alerts.
* Core text transport, explicit worker/thread contexts, assistant/legacy
  output-review links and chat cached usage/receipt IDs use the same meter.
  Image liability remains unknown and denies dispatch without blocking storage.
* Manager-only existing AI report adds billing-led economics, human-accepted
  denominator, quality regression gates, distinct TCA and capacity-not-cash.
* Two new test modules contain 30 methods: 24 core semantics and six composed
  fake-loopback HTTP/API tests. No UI, deployment or mvp code changes.
* Component guides, Tokenomics synthesis, pitch brief, index/log and dated
  official price retrieval metadata preserve remaining financial evidence gaps.

## Implementation-Time Plan and Detail Updates

Critique addendum supplies deterministic contracts without approving live inputs.
Implementation hardened production rejection of synthetic prices, pre-network
expiry/stale checks after credential acquisition, cross-currency budget reuse,
visible zero-dispatch alerts and exact derived charges (up to 30 decimals).
Synthetic price provenance also remains labelled synthetic when a supplied
invoice claims otherwise; the existing billing-source test covers that mixture.
These are compatible corrections, not live authority or new scope.

Main advanced from 5666bd33e1827670e5c07e3e3063bbbe989b59d3 to
368d3bb8d0a9ad2dc221be6cf108b5cf2a8fa7cd through merged #423 while implementing.
Its transport/infrastructure work does not change the cost-ledger source.
The full gate requires current-main ancestry. Local merge f8cd4ced integrates
that base on the topic, preserving history and all original research/critique
evidence. Its sole index conflict retained both workstreams and the newer date;
all previous log entries and the new #432 entry are preserved.

## Validation Record

External validation venv uses pip-installed editable distributions and declared
dev/runtime pins; no uv or global dependency modification.

* Core: 24 semantic tests pass; complete Ruff check/format and strict mypy
  (170 source files) pass.
* Agents: complete Ruff check/format and strict mypy (24 source files) pass;
  existing dispatch/chat regression run passed 21 tests.
* API: six fake-loopback HTTP/composition tests pass; complete Ruff check/format
  and strict mypy (124 source files) pass after restoring missing SDK packages.
* Initial requested full API discovery: 1374 tests, two missing azure.eventhub
  module errors and 320 opt-in skips. It began before the final corrections;
  preserve this adverse result, not a final-candidate success.
* Earlier hashing-bound, fixture/type and event-schema failures were corrected;
  focused existing API regression rerun passed 106 tests with one opt-in skip.
* Exact requested full discovery rerun passed: 1436 tests in 574.076 seconds,
  320 opt-in integration skips (1116 executed). Command from src/api:
  `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`.
  Complete external gate pending after original Review.
  The synthetic-provenance-only correction was made during discovery and has
  a fresh passing 24-test core and six-test API exercise; discovery is not an
  exact-head receipt. The mandatory gate must assess the final committed head.
  No changed UI; new UI Playwright exercise is inapplicable. The full gate still
  requires actual existing Chromium checks and owned local SQL/scanner evidence.

Execution generates ignored Python/tool caches, editable metadata and blinded
synthetic answer-key files. Preserve them without reading, pruning or moving
unknown existing inputs. Publication will use a task-owned external clean clone
of the final commit, with the same topic/base and a fresh external full receipt.
No existing main/other worktree or historical tracking data is modified by that
isolation; ignored working data is not copied into the candidate.

## Pre-Review Reconciliation

Source, docs, plan markers, details and requested semantic/static/discovery
results reconcile. P01/P02 are complete; the full gate is explicitly scheduled
after original Review and final evidence commit, not silently marked passing.
No source divergence, unknown test failure or generated UI target remains.
Operational evidence remains unmet; no original review outcome claimed yet.

## Blockers and Follow-Up Items

OD-51, actual applicable pricing/billing, held-out spend and live financial
acceptance remain unavailable. Resident financial join remains explicitly partial.

## Return-to-Caller State

Automatic full-loop implementation complete; independent original Review is
next, then evidence commit, full gate/verification and authorised Refs #432 PR.
