# Plan critique: sensor checkpoint correction C2 (2026-11-10)

Executed once on the final candidate plan by the author (self-executed, not independent). Verdict: proceed with the amendments below, applied directly.

* C1. Adding a green-looking claim: the text must not state the C2 chain outcome. Applied: the outcome stays external.
* C2. Overwritten exit 64 output: do not invent its content. Applied: record the command history and the sha256 captured at the time only.
* C3. Main is ahead: do not merge for appearance. Applied: prove `src`, `infra` and `tools` equality; disclose `.github/rubric/scores/latest.json` as generated data that differs.
* C4. Validators: the schema helper is local and not a repository tool; do not call it canonical. Applied.
* C5. A refused marker must not be used to discover missing inputs. Applied: preflight first, stop on failure.
* C6. Do not edit original text. Applied: additions only; the process sentence keeps its words and gains a label and a clarification.

No conflict with a confirmed Root decision; no significant or divergent issue needs a user decision.
