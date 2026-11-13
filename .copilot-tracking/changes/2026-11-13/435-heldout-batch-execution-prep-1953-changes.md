# Changes: #435 held-out batch live adapter (1953)

Status: implemented; no live call made.

* Added `src/agents/src/zava_forward/agents/heldout_aoai.py`: stdlib Azure OpenAI `Call` adapter, az CLI or managed-identity token, no redirects, no retries, fixed-message unchained errors, response-model prefix and cached-token checks (critique P5, P7).
* `heldout_batch.main`: `--endpoint`, `--deployment`, `--model`, `--auth`. Live needs all three plus a valid authorization (<= USD 5.00) and matching model before any token fetch; otherwise exit 2 or refusal. Injected provider unchanged. Module docstring updated.
* Added `src/agents/tests/test_heldout_aoai.py` (15 tests, mocked HTTP, subprocess and credential).
* README held-out section updated (owner pre-run checks, one live batch per authorization).

Validation (venv `/tmp/venv-435bp-1953`): `--dry-run` CLI completed offline; `--execute-live` without target exits 2. Agents suite 430 tests OK; `heldout_aoai.py` 100% line coverage; `ruff check`, `ruff format --check` and `mypy` clean.

Deferred follow-ups: durable spend ledger (P4), proposal content bound to freeze digest (P6).
