<!-- markdownlint-disable-file -->
# Issue 107 R1 model bounds: details

* `MODEL_CALLS_PER_ATTEMPT = 1`, `AGENT_DEPTH = 1`, `ATTEMPT_CEILING = 3` (the existing `Limits` attempts upper bound, now named).
* `model_bounds(limits=None)` returns `calls_per_attempt`, `max_attempts`, `max_calls_per_request`, `max_agent_depth`, `tools` (0) and `attempt_ceiling`; invalid or absent limits use `Limits.DEFAULTS`.
* `Assistants.registry` adds `model_bounds` to each assistant on both the SQL and non-SQL paths; no controlled-domain access, no new endpoint, no role change. Contractors and unknown roles are still refused before the view.
* Tests: `src/api/tests/test_assistants.py` (3 new), `src/agents/tests/test_dispatch.py` (1 new).
* Human approval, resident consent, manual path and AI-unavailable behaviour are unchanged; the statement is read-only metadata.
