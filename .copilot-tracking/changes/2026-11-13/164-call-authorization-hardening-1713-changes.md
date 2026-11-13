# Changes: 164 call authorization hardening

* `chat_eval.py`: strict UTC `expires_at`/`now`, finite budget, validated owner/counts, `projected_spend`/`used_spend` vs `max_budget`; new `CallLedger`, `AuthorizedModel` (fail-closed gate, reserve before dispatch, kept on failure); `Run(model=)`.
* `test_chat_eval.py`: fixtures moved to UTC timestamps; added inf/NaN/bool/zzz/naive/offset, budget exceeded, gated dispatch, shared ledger, failed-dispatch and blocked-Run tests.
* Validation: 403 agents tests OK; ruff check, ruff format --check, mypy clean. Divergence: none. Provider-enforced output limits remain an owner-approved actual-model follow-up.
