# Changes: #107 F1-F4 (1531)

* `ai_consumption.py`: `IDENTITY_CHARS = 80`; oversized str maps to sentinel; `_SECRET` anchored prefixes plus 32+ hex/unbroken runs; price-register model admission limited to 80 and rejects secret shapes.
* `assistants.py`: typed `Limits.__init__`, `sanitize_identity`, `shape_result`; identity fields validated on raw value (no pre-truncation).
* `ai.py`: deployment uses the shared limit.
* Tests: `test_assistants_identity.py` (secret shapes, accepted names incl. task-summarisation-v1, 80/81 boundary), `test_ai_consumption_api.py` roundtrip expectations.
* Divergence: none. The brief's `/tmp/venv-*` was deleted by another process mid-run; used `/tmp/ama-107-c1-1531-env` instead.
* Validation: ruff check/format clean; mypy core/agents/api 0 errors; core and agents full unittest discover pass; api pass (api 2966 OK).
