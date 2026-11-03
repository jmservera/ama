---
title: Issue 125 round 1 research
ms.date: 2026-11-03
---

Disposition: executed. Planning Readiness: Ready.

## Delivered so far (merged PRs and code)

* Merged PRs mentioning #125 (#291, #389, #401, #409, #614, #692) are contextual only; none implements the assistant. Closure audit comment (2026-10-31, #614) records all three criteria unmet and no new ticks.
* `grep` of `src/` finds no discovery-assistant, readiness-gate or tool-allowlist code (2026-11-03).
* Source: `docs/brds/retrofit-flow-discovery-brief.md` sections Proposed Assistant Concept, Authority and Safety Boundary, Readiness Before Writing the Agent, Evaluation Criteria.

## Constraints from sources

* An agent definition may be drafted as a design hypothesis but must not be connected to company data or described as approved until ten readiness items are met.
* Read-only, low autonomy; forbidden actions listed (source writes, lifecycle progress, consent inference, hazard diagnosis, PAS 2035 output, scheduling, payment, grant decisions, ranking, presenting inferred cause as validated).
* Deterministic code calculates; any model only drafts source-linked summaries. Manual analysis and export must remain possible.

## Smallest coherent slice (slice 1 of a stack)

Pure `discovery_assistant_boundary` module: readiness gate over ten items that yields at most "ready for owner decision", plus default-deny read-only tool allowlist. No store, model, company data or infrastructure, so the focused tier applies.

## Later slices (not delivered)

1. Human nomination of the discovery owner and readiness evidence (human, outside code).
2. Deterministic duration and reconciliation functions with tests on synthetic data (readiness item 7).
3. Read-only analytical-store tool wiring and access-denial evidence (SQL and security: gate needed).
4. Comparison against manual analysis and conventional reporting on approved data (criterion 3).
