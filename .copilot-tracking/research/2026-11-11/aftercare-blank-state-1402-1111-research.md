<!-- markdownlint-disable-file -->
# Research: aftercare blank stored state (issue 1402, cycle 1 of 3)

Date: 2026-11-11. Branch `fix/aftercare-blank-state-1402-1111`, base `2f7465c57dee4d341ac2340a9e303d387a6e103e` (independently approved parent #1401 topic `fix/aftercare-numeric-order-1401-1111`). PR 1400 merge `64c3f9191a2ffa97ef2dc07245422333ad4d6585` is an ancestor (verified). `origin/main` is `ba65039c2177694bd3d9532d86dd494551fcc3de`; the parent is not merged and is not assumed to be.

Authority: owner grant, public comment 6801517952 on #1402, up to three scoped cycles; root admits C1 only (this is 1 of 3). C2/C3 are unadmitted. Inherited #133/#89/D5 spent history is not reset. Synthetic bounded demo only.

Research disposition: executed (source read and call-path trace; no external research needed).

## Evidence

* `src/core/src/zava_forward/core/aftercare_intake.py` `_parse(text)`: `if text is None or not text.strip(): return _blank()`. Empty or whitespace-only existing text is treated as a fresh register.
* `StateStore.read()` contract returns `str | None`; `None` means absent. `FileStateStore.read()` returns `None` only on `FileNotFoundError`; an existing empty file returns `""`.
* `AftercareService` reads via `_parse(self.store.read())` (read path) and `_parse(text)` inside `store.update` mutators (write path). With a blank existing file, a read returns an empty register and the next write replaces the file, destroying the bytes and restarting identifiers (`AC-001`).
* Existing refusal pattern: invalid JSON or schema raises `StateInvalid`; `handle()` maps `StateInvalid` to 503 "left unchanged"; the mutator raising leaves stored text unchanged (`FileStateStore.update` writes only after the mutator returns).
* Existing test `test_aftercare_intake.py` bad-state subtests (about lines 255-285) assert refusal and unchanged bytes for bad documents; blank documents are not in that list.
* Adapter path: `DocumentStateStore` (`aftercare_store.py`) returns `_canon(value)`, which is `None` or `json.dumps(...)`; it can never return blank text, so the changed `_parse` branch is unreachable through the supported runtime adapters. A raw blank JSON document is not claimed to be handled there (out of scope per issue). The adapters' MSSQL behaviour is unchanged, so no SQL test is needed or admitted; SQLite results must not be read as SQL Server evidence.

## Root cause and smallest fix

`_parse` conflates absent (`None`, legitimate) with present-but-blank. Fix: `if text is None: return _blank()`; blank or whitespace text falls through to `json.loads`, which raises `JSONDecodeError` and the existing `StateInvalid` mapping applies, so bytes are preserved. No new helper or message.

## Planning Readiness

Ready. Unknowns: none blocking. Limits: standalone `FileStateStore` only; connected-runtime raw blank JSON adapter behaviour is not claimed.
