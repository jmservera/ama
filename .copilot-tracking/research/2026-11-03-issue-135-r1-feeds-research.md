# Research: issue 135 round 1, exception queue feeds

Date: 2026-11-03. Disposition: executed (short). Planning Readiness: Ready.

## Already delivered

* PR 666 (merged) added `exception_queue.py`, 10 tests and a README section: core register, scoped queue, audited recovery request, outage banner. Its review listed unmet work: store, API and UI wiring, producers, owner approval of role names and runbooks.
* #80, #84 and #122 delivered rows to fix, conflict display and continuity earlier (PRs 382, 398, 431, 269 and others); not redone.

## Evidence for the next slice

* Nothing populates the queue. AI task records (`ai_tasks.finish`, `add_record`) already keep `fallback_reason`, `mode`, `source` and `status` (`Quarantined`); `taskqueues.overdue_tasks` already yields overdue tasks with `owner` `Unknown`.
* API wiring needs role mapping for named staff (open owner question) and store persistence in three backends, which is a larger and access-sensitive slice.

## Chosen slice

Read-only feeds in core (`exception_feeds.py`) that turn failed AI runs and ownerless overdue tasks into queue items, idempotently, with no change to source records. Pure Python, no store, SQL, infrastructure or deployment change; focused tier.

## Stacked slices after this

1. Importer failure and integration producers (needs importer quarantine record shape).
2. Store persistence and read-only API with role mapping (security-sensitive, needs owner approval of role names).
3. Staff UI (Fluent 2, WCAG, plain language) with outage banner and AI-unavailable manual path.
