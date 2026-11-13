# Plan critique: 164-chat-grounding-criteria-1652

Executed once by an independent `rubber-duck` agent. Verdict: proceed with amendments. No user decision required; none conflicts with the owner brief.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Blocking: `call_authorization` is overstated as fail-closed. Local check confirmed `max_budget=inf` and `expires_at="zzz"` both return `within-limit` (the expiry is a lexical string comparison, no ISO parse; spend is not compared with budget). Existing tests do not cover these. | Applied: record as a code-level limitation in criterion 3. |
| 2 | Registration and disabled state are delivered; the accountable individual is `UNKNOWN`. | Applied: split the criterion 2 clauses. |
| 3 | "Disabled" has a demo-only exception: `authorizes_live` is true when the owner-approved demo switch and demo profile are both set (`ai_registry.py`, `demo_activation_honoured`). | Applied: qualify every disabled statement. |
| 4 | Avoid global negatives; scripted report records zero actual-model calls for that report only. | Applied: wording scoped to inspected evidence. |
