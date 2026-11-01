# Plan: #216 evaluation gates

1. Add `authorise_model_run(authority, request, now)` to `regulatory_gates.py`: denies unless authority has owner, finite positive call/token/budget limits and a future expiry, and the request fits; returns a decision dict, never grants spend.
2. Add unit tests in `src/agents/tests/test_regulatory_gates.py` (no authority, expired, over limit, within limit, non-finite).
3. Add a README note under the #216 section.
4. Validate: unit tests, ruff check, ruff format --check, mypy for `src/agents`.
5. Critique (single, self): compatible; no model call added; scope tight. Verdict: proceed.
6. PR uses `Refs #216` naming unmet criteria.
