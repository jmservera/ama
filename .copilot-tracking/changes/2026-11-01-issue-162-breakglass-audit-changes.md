# Changes: issue 162 break-glass audit purpose (2026-11-01)

* `src/core/src/zava_forward/core/chat_isolation.py`: refused break-glass audit detail now includes the redacted purpose.
* `src/api/tests/test_chat_isolation.py`: asserts purpose, target and policy reference on every break-glass audit entry, and no content key.
* `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`, `src/core/README.md`: proposed OD-46 options (not decided), log entry, README pointer.

Validation: `tests.test_chat_isolation` 32 tests OK; ruff check clean for src/core and src/api; mypy clean for both. `ruff format --check` fails for the two touched Python files, identically on unmodified main (pre-existing); not reformatted to keep scope tight.

## Copilot review follow-up (PR 650, 2026-11-01)

* `src/api/tests/test_chat_isolation.py`: adds a refusal whose purpose contains a synthetic email and asserts the exact masked purpose, actor and target, and a non-empty purpose on every entry.
* `docs/reference/research/chat-memory-dpia.md`: option A now states counts only (no ids) and that the expiry is advisory, not an enforced grant.

Validation: `tests.test_chat_isolation` 32 tests OK; ruff check clean.
