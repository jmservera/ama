<!-- markdownlint-disable-file -->
# RPI Phase Details: AI consumption economics

## Metadata

* Task ID: 432
* Task slug: ai-metering-432
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md
* Evidence: research C4-C8; all source-only boundaries apply.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Extend existing ledger and compose dispatch | Complete |
| P02 | Semantic/regression evidence and documentation | Complete; publication gate pending after Review |

<!-- rpi:phase id=P01 -->
## P01: Financial ledger and source wiring

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend immutable assistant events

Assistants.transaction already provides SQLite BEGIN IMMEDIATE and SQL
SERIALIZABLE; assistant_events is immutable. Reuse those ports without changing
DDL. Each event has a safe kind/version and closed metadata payload. Reservations
are durable before provider dispatch, no automatic refund on ambiguous usage.
Owner/price policies must match model/configuration, currency, time and scope.
Finite ledger scan overflow denies admission, never silently truncates budgets.
Report monetary values as exact decimal strings; no floating-point money.
Billing absence or missing acceptance/quality/effort gives Unknown, not zero.
Tests cover concurrent reservations, unknown cached tokens, duplicates, token
overrun, expiry, request depth/calls and quality deterioration.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire model calls and reports

Ai.evidence and legacy _chat use one financial admission boundary, with request
metadata passed explicitly/scoped per call rather than mutable shared state.
Assistant model thread receives its own task identity; callbacks retain meter IDs.
Legacy result records and assistant review link to record IDs without case text.
Image dispatch without known maximum liability stops but document storage remains.
Real Ai without a supplied financial ledger denies; test doubles stay nonbillable.
API attaches ledger after existing assistant schema setup and extends manager-only
/api/ai/report. Independent resident accounting is reported separately/unjoined;
no stored procedure or deployment changed.

<!-- rpi:phase id=P02 -->
## P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Tests, guides and pitch

Two new test modules at most; no regression removals. Owned core semantic tests
use existing constructed SqlStore/assistant tables, no private dataset. API
composed tests use fake HTTP provider responses and authenticated local report.
Run caller's exact unittest/PYTHONPATH and Ruff commands from src/api.
Update component README, existing Tokenomics synthesis and pitch brief with
engineering results and source/evidence labels. Update knowledge index/log.
Do not rebuild any deck or claim a rehearsed pitch. Keep required human gates open.
After independent Review, commit original evidence, run complete external local
gate, fetch main and verify receipt immediately before push. Failure blocks
publication; no skip or cloud substitute.

## Final-candidate critique contract addendum

* PC-001: SHA-256 opaque root, attempt, output, budget and authority references.
  Immutable authority records intersect period and task budget IDs in one DB-time
  transaction. All reservations for a budget ID count across authority versions.
  Duplicate physical attempt is denied, never reauthorised. Depth starts at one;
  calls and depth admit at <= maximum, projected budget sum must be <= cap.
* PC-002: only schema ai-consumption-v1 under the dedicated ai-consumption task
  partition is read. New events are constructed from validated method arguments;
  unknown keys are not accepted. References are hashed, provider returned model
  is compared to the configured model and only its digest survives mismatch.
  Never export mixed historical output/review events.
* PC-003: an immutable call context carries root/attempt/capability/config/prompt.
  It is installed inside assistant provider threads, not inherited. Low-level Ai
  returns usage and meter ID; assistant shaping and chat usage retain cached tokens.
  Legacy run receipt uses a per-call local dictionary, not shared Ai state.
* PC-004: reserved but incomplete, unknown/malformed cached usage or any overrun
  is a sticky budget hold. Financial completion occurs at transport return,
  independently of proposal fencing; no automatic release or hold-clearing API.
  Known actual charge replaces reservation only when complete and within bounds;
  overrun records actual liability and alerts. Serialized ASCII request bytes
  conservatively bound textual input; any image has unknown liability and stops.
* PC-005: output hash links all attempts for a root; accept/edit-accept count once,
  verify/reject/templates/chat are not accepted proposals. SQL review joins occur
  in the review transaction. Legacy cross-save linking is best-effort only with
  explicit incomplete-join coverage; missing joins prohibit qualified economics.
* PC-006: immutable billing imports name exclusive UTC [start,end), currency,
  budget scope and SHA source/allocation references. Overlap/duplicate imports
  are rejected; correction is a later separate source delivery, not overwriting.
  Supplied synthetic records remain synthetic. Variance is absolute billed minus
  projected divided by billed (zero bill only reconciles with zero projection);
  tolerance is an explicit owner fraction. Missing complete allocation is Unknown.
  Monetary strings are finite nonnegative Decimal, never float or rounding down.
* PC-007: call-time cohort with as-of output review state, all attempt costs
  including failures included. Accepted proposal is an output, not a home.
  Financial ratio is billing/accepted; quality-qualified ratio additionally needs
  approved floor and matched observed denominators for critical misses,
  unsupported claims, overrides and reopened cases. Missing values are Unknown.
  Any worse rate versus baseline is Failure, even with a cheaper numerator.
  TCA token/hosting/review/correction/assurance/support are distinct; any missing
  component prevents total. Capacity hours are not cash without Finance evidence.
* PC-008: new modules core/tests/test_ai_consumption.py and
  api/tests/test_ai_consumption_api.py, <=35 parameterized methods, no removals.
  Semantic groups cover PC-001 budgets/races/replay; PC-002 privacy;
  PC-003 composed fake transport; PC-004 uncertainty/overrun;
  PC-005 review/joins; PC-006 billing; PC-007 quality/capacity.
  Existing test_assistants, test_ai_tasks, test_chat_model and full API discovery
  cover preservation. AC1 partial (resident/historical joins unmet), AC2 local
  engineered bounds, AC3 local deny/alerts, AC4 price-record mechanism but actual
  applicable price unmet, AC5 synthetic reconciliation only, AC6 report mechanism
  but real quality/cost unmet, AC7 capacity classification, AC8 paid batch unmet,
  AC9 pitch brief engineering/gap update (deck remains unchanged).
