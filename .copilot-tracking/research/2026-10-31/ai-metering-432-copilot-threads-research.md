---
title: AI metering Copilot threads research
description: Focused source investigation for five unresolved PR 602 threads
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Continue issue #432 on feat/ai-metering-432 / PR #602. Investigate shared
document-call limits, report input validation, and human rejection when financial
attribution is missing or capacity-held. Audience: implementer and independent
reviewer. Output mode: convergence preparing planning.

## Research Parameters and Direction Controls

Focused posture selected from the five named source failures. No paid inference,
private data, secrets, deployment, or unrelated UI changes. User explicitly
requests the entire RPI loop, tests/static checks, non-force push, and thread
resolution; CI is the gate and the full local gate must not be awaited.
Topic pull completed; origin/main merge reports already up to date, so no rubric
conflict required resolution. Preserve Refs #432 and original adverse evidence.

## Extension Registry and Participation

Repository project/branch/evidence guidance and rpi-research selected. Domain
sources: core/API READMEs, consumption ledger, assistant transaction contracts.
No external research or research delegation needed for this coupled source
trace. No interactive questions: explicit scope and outcomes are sufficient.
Prior artifacts are historical evidence, not current closure proof.

## Questions and Candidate Areas

1. How can document calls retain request root/call/depth admission?
2. Which shared helper validates timestamps and ranges independently of SQL?
3. How can missing output attribution allow rejection without resolving economics?
4. How can assistant rejection atomically repair missing output links?
5. How can capacity-held rejection persist and invalidate stale accepted economics?

## Research Cycle Log

### Cycle 1: Wider

PR reviewThreads retrieved with gh GraphQL on 2026-10-31. All five named
threads are unresolved. Initial source reads confirm fresh document roots,
SQL-only report validation, synchronous review intent before legacy save,
and consumption review inside authoritative assistant transactions.

### Cycle 1: Deeper

Consumption owns bounded append-only reads and review revisions; legacy domain
saves use a separate transaction. Existing API composed tests include missing
output-link injection but explicitly expect rejection to fail. Assistant
provider failures stay pending and do not create output links.

### Cycle 1: Contrarian

Acceptance must continue requiring linked output. Legacy rejection may write
an orphan intent/disposition, retaining unjoined_outputs until the original
link is repaired. Assistant rejection can create an ineligible link atomically
when absent. Capacity/malformed ledger reads must remain fail-closed for
dispatch, not human withdrawal: append a closed unresolved-review marker
without scanning in the authoritative transaction. Reports must exclude those
outputs from accepted counts and prohibit reconciliation even after scan
capacity becomes available; historical cutoffs before withdrawal stay intact.
Rejected alternatives: fresh request roots; swallowing arbitrary SQL errors;
marking missing economics resolved; truncating the ledger; relaxing MAX_EVENTS.
One focused cycle covers all questions; next sources are redundant.

## Evidence Log

* W1: https://github.com/jmservera/ama/pull/602#discussion_r4431875217
* W2: https://github.com/jmservera/ama/pull/602#discussion_r4431875235
* W3: https://github.com/jmservera/ama/pull/602#discussion_r4431875253
* W4: https://github.com/jmservera/ama/pull/602#discussion_r4431875268
* W5: https://github.com/jmservera/ama/pull/602#discussion_r4431875281

All W sources retrieved 2026-10-31 using authenticated read-only gh GraphQL.

* C1: src/core/src/zava_forward/core/ai.py:155 and :210, run preserves CURRENT
  but look_at unconditionally replaces it.
* C2: src/core/src/zava_forward/core/ai_consumption.py:68 and :798,
  timestamp and complete-exclusive-period validation are reusable.
* C3: src/core/src/zava_forward/core/ai_consumption.py:664 and :698,
  missing output gates both intent and disposition; :826 reporting counts
  missing root/output joins and pending review intents.
* C4: src/core/src/zava_forward/core/ai_tasks.py:375 and
  src/core/src/zava_forward/core/store.py:941, intent precedes domain save.
* C5: src/core/src/zava_forward/core/assistants.py:930 and :1068, pending
  provider errors have no link and review errors roll back task withdrawal.
* C6: src/core/src/zava_forward/core/ai_consumption.py:172, bounded scans
  raise DispatchHeld; :180 permits append-only closed metadata independently.
* C7: src/api/tests/test_ai_consumption_api.py:392 and :848, composed fixture
  covers both legacy stores, priority, assistant/provider, local HTTP routes.

## Alternatives and Decision State

Do not silently accept missing economics or relax provider dispatch limits.
Prefer existing ledger reconciliation and explicit unresolved financial state.

## Planning Readiness

Ready. Research disposition: executed, complete. All questions covered by
C1-C7 and W1-W5; no source edits in this phase. Parent proceeds to Plan.
