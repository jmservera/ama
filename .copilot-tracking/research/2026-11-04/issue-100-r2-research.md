# Research: issue 100 r2 per-capability AI economics

Disposition: reused (r1 research, 2026-11-03) plus executed source check. Planning Readiness: Ready.

Delivered (evidence: gh PR 911 merged 2026-11-03; children #101, #102, #103 closed; #134 open): overview, charts, progress report, packs, AI consumption ledger (#432) and the asset-board usage, alerts and components panel. r1 follow-up 1: the BRD management view is per capability (docs/brds/agentic-retrofit-programme-brd.md, Required Management Views; FR-052 AC-102), but `report()` in src/core ai_consumption.py returned ledger-wide figures only.

Slice: add a read-only table on the asset board over the `by_capability` dict that main already reports. Per-capability cost stays Unknown: billing is period-wide, so no capability cost can be proven. Not touched: limits and prices (OD-51 open), no approval or consent action, no SQL, infra, auth or deployment change. Focused tier.

Unmet: #440 checkpoint, children closed or deferred (#134 open), live evidence, limit values, per-capability cost and quality floor.
