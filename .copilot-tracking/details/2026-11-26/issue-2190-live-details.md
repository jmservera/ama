# Details: issue 2190

Phase 1: wrap `self.wfile.write(body)` in the Slow handler in try/except (BrokenPipeError, ConnectionResetError). Validation: verbose run of the test shows no traceback; ruff format/check; mypy in src/api.
