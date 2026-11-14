# Review: #164 officer chat consent boundary (2026-11-14)

Execution: executed once. Outcome: conformant for the stated local scope; no material findings.

* Consent not `Given` (including empty or withdrawn) returns a deterministic `decision-rules` answer citing a `[Workflow rule]`, naming the manual case-card path, with 0 model calls and no case change.
* Out-of-scope refusals keep their own route; given and legacy (absent) states keep the existing path.
* Only allow-listed state names are echoed; guidance is ASCII, short sentences, no internal terms or status claims.
* Open: no real source of `ai_data_use_consent` exists yet, and an absent state is treated as legacy (owner decision). Live model, rendered browser, screen reader and staff comprehension are not evidenced. Focused tier, not the complete gate. #164 and #215 criteria are not closed by this change.
