# Details 2244 live r4 (2026-11-23)

Phase 1: lawstore.py helper using `sys.tables`, `sys.tables.ledger_type_desc` and `sys.triggers` (same catalog views as `MssqlStore._schema_current`).
Phase 2: guard around the locked DDL block; `self.in_tran = False` stays set.
Phase 3: FakeDb-style stub connection in the existing test module recording whether `BEGIN IMMEDIATE` ran.
