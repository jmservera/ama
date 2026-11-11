<!-- markdownlint-disable-file -->
# Changes: issue-144-permit-sql-e4-impl-1111

Date: 2026-11-11. Continuation of the same E4. Refs #144 only. Direct-only local qualification.

## Added

* `src/api/tests/test_permit_sql.py`: seven-method `MssqlPermitBoundary` (flag `ZF_TEST_MSSQL=1`, SQLGuard in `setUpClass`), strict local runtime fixture factory, holder/observer lock harness with LIFO cleanup (observer close, holder rollback, holder close, join), ID-conflict first and root-conflict last subTests. sha256 `a5fdab0b66740e67366d06e8749a690a850fa78c5ec8042b9557340d7ab51c0a`.

## Executed (external evidence under `144-permit-sql-e4-impl-1111/logs`, immutable `NN-name.out/.err/.exit`)

| Step | Exit | Result |
| --- | --- | --- |
| 00 identity | 0 | HEAD 1b11c2ecd, tree 53fbebda; only the new module untracked |
| 02 probes (core, setuptools, ruff, mypy) | 1,1,1,1 | Missing-dependency need demonstrated |
| 03 runtime wheel-only download, hashed requirements | 1 | BLOCKED: `paho-mqtt==1.6.1` has no wheel (only 2.0.0rc2..2.2.0); sdist fallback and pin weakening forbidden |
| 04 tool wheels (setuptools 80.9.0, wheel 0.45.1, ruff 0.17.1, mypy 2.4.0) | 0 | Downloaded; hashes in `receipts/wheelhouse-tools.sha256` |
| 05 ruff offline install | 0 | Tool-only, venv V |
| 06/07 ruff check, format on first draft | 1,1 | Four E501 plus format diff; preserved |
| 08-10 ruff format apply, check, format check (new log names) | 0,0,0 | Pass |

## Not executed (blocked by step 03)

Runtime/editable installs, mypy, 15 SQLite selectors, seven-skip run, heavy-lock admission, container, real SQL, N1/N2 controls. No container was created, no SQL connection was made, no lock was taken.

## Divergences

* Style-only authoring correction within the new module after ruff diagnostics (permitted by the admission); original diagnostics retained.
