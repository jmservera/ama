# Review: recommendation origin provenance (Refs #104, #164)

Date: 2026-11-14. Execution: executed once. Outcome: conformant for scope.

* Additive fields only; no change to ranking, approval or mutation paths.
* Origin derived from `source`, so held or fallback records cannot claim `generative_model`.
* Residual: ai_task records (briefing, draft) and the UI card renderer do not yet surface `origin`; follow-up for a later task. Independent human review and hosted CI remain required.
