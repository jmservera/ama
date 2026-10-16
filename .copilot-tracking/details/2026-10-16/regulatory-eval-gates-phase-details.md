---
title: Regulatory evaluation phase details
description: Completion evidence for issue 216
ms.date: 2026-10-16
---

## P01-T01

Use an independently frozen expected bundle as oracle, not runtime retrieval or citations.
Check exact source/fact support, IDs, links/status/dates and nonempty coverage.
Freeze source IDs/text/metadata, permitted fact paths/values and expected kind.
Compare the complete closed-template envelope against rendering of that oracle,
detecting unsafe reply-only edits and changed escalation/owner sections, not
arbitrary entailment. Mutate both retrieval/output with extra sources/facts.
Include independently frozen card identities, links, cadence object/text/as-of
and answer as-of; none may escape visible-answer grading. Invalid outputs have
separate case IDs and cannot be counted as correct/supported in summary.
Count unsafe answers and false refusals separately. Empty or malformed outputs
must fail. No overall boolean pass. Provisional citation/refusal targets 1.0,
pending Juan Manuel Servera; recall baseline has no numeric threshold.

## P01-T02

Frozen development questions cover supported lookup, forbidden actions/legal
terms/future law, injection, absent/future/partial/changed sources and conflicts.
Offline runner constructs temporary law/case data and calls actual retrieval and
renderer. Generate 60,000 wholly fictional home IDs with explicit seeded rule
profiles. Report exact state matches plus independently specified alert-required
hazard recall. Separate stateless scale from SQL engine integration and live stock.
Ten profiles repeat 6,000 times: hazard elapsed hours 0/23/24/47/48/72,
missing awareness, future awareness, empty hazards and missing hazards.
Expected states: clear/clear/attention/attention/breach risk/breach risk/
unknown/unknown/not applicable/unknown. Automated decisions cycle recorded human
evidence/pending/missing evidence/explicit non-significant/absent list, each
12,000 times. Unit: home/rule/item, absent output counts as a miss.
Freeze seed 174, as-of 2026-10-16T12:00:00Z and fictional 48h/24h contract.
Freeze the item identity per profile: hazards/0 or automated_decisions/0 for
present items, collection names for missing/empty lists. Require exact expected
item and result, with no credit for unrelated/duplicate output. SQL also scopes
the selected output to its home and card.
No human trial data is synthesized into success.

## P02-T01

Read existing versioned monitoring config and last successful observation.
At the due boundary label out-of-cadence. Missing configuration/observation and
future clock are unknown. Failed observations never refresh success. Do not
instantiate a write service during reads or infer cadence from free-text metadata.
Expose per-source and card freshness from rule-card HTTP reads and chat cards,
render accessible text in the existing chat panel. No new public-facing design.
Any overdue source makes the card out-of-cadence; otherwise any unknown or empty
coverage makes it unknown; only all in-cadence yields in-cadence. Absent tables,
configuration or successful observation is unknown without writes. Future latest
attempt, including a failed attempt, is unknown. No alert eligibility changes.

## P03-T01

Mutation tests break citation IDs, quotes, metadata, facts, false refusals,
hazard output, empty evidence and comparison availability. Existing law/rule/chat
tests protect behavior. Run local HTTP server with synthetic SQLite fixture and
health response; no cloud or live calls. Update component READMEs and append the
reference log/index with per-criterion honest audit and exact commands.
Migrate regulatory_eval.py, regulatory_chat_results.json and the existing
test_regulatory_answers.py equality test together: remove aggregate assertion,
retain all 13 cases, 3/3 and 10/10 counts and structural comparison.
The new runner records the new report; the legacy report changes only its removed
aggregate field and schema version, verified by its retained equality test.

## P03-T02

One independent post-implementation RPI review; no repeated review loop.
Fix in-scope correctness/safety defects and rerun targeted checks or disclose
them as readiness blockers; only nonblocking/out-of-scope work is deferred.
Resolve authenticated GitHub identity, configure
repository-local privacy-safe email, commit with required coauthor trailer,
push topic branch and create main-targeted PR using only Refs #216.
Do not modify issue checkboxes or merge.
