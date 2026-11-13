# Plan: 164 call authorization hardening

* [ ] 1. Harden `call_authorization`: strict UTC `expires_at`/`now`, `math.isfinite` budget, `projected_spend`/`used_spend` vs `max_budget`.
* [ ] 2. Add `AuthorizedModel` wrapper (fail-closed gate before each dispatch, metering) and `Run(provider=, authorization=, now=)`.
* [ ] 3. Tests in `src/agents/tests/test_chat_eval.py`; update fixtures to UTC timestamps.
* [ ] 4. Run agents tests, ruff check, ruff format --check, mypy in `/tmp/venv-164f-1713`.

Details: `.copilot-tracking/details/2026-11-13/164-call-authorization-hardening-1713-details.md`
