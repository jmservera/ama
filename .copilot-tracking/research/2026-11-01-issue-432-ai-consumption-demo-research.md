# Research: #432 AI consumption metering, demo slice

Date: 2026-11-01. Branch `feat/ai-consumption-metering`. Mode: automatic. Research disposition: executed. Planning Readiness: Ready.

## Findings

* Source-only metering was merged in #602 (`src/core/.../ai_consumption.py`, `Consumption` ledger; API report in `src/api`, README `#ai-consumption-report-432`; 30 core tests, API tests). It already covers: call attribution joins, atomic per-request call/depth bound, token/money/expiry/unknown-price/liability dispatch holds with owner reference, dated price metadata, billing reconciliation with tolerance, billing-led cost per human-accepted proposal beside quality, capacity-not-cash, and a pitch drafting insert (`docs/reference/resources/ai-tokenomics.md`).
* The official price retrieval (2026-10-31) has no numerical rates, so cost stays Unknown.
* Issue #432 is open. Criteria needing external evidence and not provable by code: real Azure billing reconciliation, OD-51 owner decisions, owner spend authority for the held-out batch, deck placement.
* Gap for a demo: no single credential-free, runnable walk-through shows the behaviours (Unknown cost, unknown-price hold, loop stop, synthetic-labelled report) in one place.

## Decision

Deliver a small credential-free demo module in `src/core` (`ai_consumption_demo`, run with `python -m`) on a constructed temporary SQLite ledger, labelled synthetic, with tests outside the package. No new code in `mvp/` or `prototype/`. No claim of paid inference, billing or acceptance; PR uses `Refs #432`.

## Evidence

* `docs/reference/resources/ai-tokenomics.md` (source-only extension, criteria table)
* `docs/brds/agentic-retrofit-programme-brd.md` NFR-012, FR-052, AC-100 to AC-103, OD-51
* `src/core/tests/test_ai_consumption.py` (constructed port pattern)
