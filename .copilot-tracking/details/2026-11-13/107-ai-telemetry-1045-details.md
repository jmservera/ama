# Details: #107 AI telemetry raw-content exclusion (107-ai-telemetry-1045)

## Probe design (script under /tmp, hash recorded in changes file)

* Sentinels: `SENTINEL_RAW_CASE_NOTE_991`, `SENTINEL_RESIDENT_MSG_992`, `SENTINEL_DOC_BODY_993`.
* Ledger: reuse `Port` from `test_ai_consumption` with a temp sqlite file. For each capability in `assistants.REGISTRY` (five assistants): add price, authorize, `reserve` with `CallContext` whose ids are `reference(sentinel)`, `complete` with a usage dict carrying extra sentinel-valued keys and a sentinel model string (expect refusal or drop), `output(root, <sentinel proposal id>)`, `review(... "accept")`.
* Dump every ledger record plus `report()` JSON; assert no sentinel substring and that `by_capability` attributes tokens per assistant and per accepted proposal.
* Chat: `ChatPanel` with a stub model (as `test_chat_panel` setUp) asked a sentinel question; also an over-limit sentinel question for the limit-fallback path; scan returned `consumption` receipts and any ledger records for sentinels.
* Exit code captured directly from the python process (`$?`), not a pipeline.

## Commands (after critique)

`python3 -m venv /tmp/venv-107-1045`; pip upgrade `setuptools wheel` offline-first; `pip install --no-build-isolation --no-deps -e src/core -e src/agents`; verify `zava_forward.core.__file__`; `python -m unittest -v test_ai_consumption test_chat_panel` from `src/core/tests` with `PYTHONPATH` unset except the tests directory-relative imports; then the probe.

## Success

Both suites pass with recorded counts, probe reports zero sentinel hits, 14 hashes match, `git diff --check` and `git status --short` clean after commit.
