# Plan critique: #107 (107-ai-telemetry-1045)

Executed once by an independent `rubber-duck` subagent, read-only, before any venv, test or probe. Verdict: reject (as first drafted).

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Probe called `Consumption` directly and bypassed `shape_result` and task envelopes | Applied: probe also drives `assistants.shape_result` for all five `REGISTRY` capabilities with sentinel-laden provider results (text, extra usage keys, model, extra fields) and inspects envelopes. Full `Assistants.execute` end-to-end on a SQL store is out of the 7-minute budget and is recorded as a residual gap, not claimed |
| 2 | Blocking | Hashed ids and refusal could give false passes | Applied: probe asserts sentinels were present at the input boundary, that completion succeeded with nonzero tokens and an accepted proposal, then scans; refusal cases are reported separately |
| 3 | Blocking | Chat stub may never meter | Applied: chat uses a `ModelReply` with usage and asserts the model ran; if no meter is created the probe reports "receipt only, no ledger event" rather than claiming ledger coverage |
| 4 | Blocking | Chat audits omitted | Applied: probe scans `store` audit entries for `chat.turn`/`chat.answer` details and receipts, including limit-fallback |
| 5 | Non-blocking | Model mismatch confounds attribution | Applied: clean matching-model scenario with `eligible=True`; sentinel model tested separately |

Required decision from the user: none; all findings are compatible with confirmed direction. Critique is not repeated.
