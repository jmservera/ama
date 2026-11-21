# Details 2026-11-21

Phase 1: wrap `self._row(json.loads(body))` in try/except (KeyError, TypeError, ValueError, IndexError) and `continue`.
Phase 2: test in the existing sqlstore test file that inserts a body `{"id": "legacy"}` and reopens the store.
