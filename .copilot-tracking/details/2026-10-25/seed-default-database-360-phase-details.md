# Phase details: default database path correction (issue 360)

1. `factory.py` helper plus `open_store` refactor (about 6 lines).
2. `seed_merge.py`: resolve path from the original env; set `ZF_SQLITE` only for sqlite.
3. Tests in `src/core/tests/test_seed_merge.py` (CLI default path, state-only, explicit wins, helper equivalence, MSSQL passthrough).
4. One-sentence README note. Changes and review records for this correction.
