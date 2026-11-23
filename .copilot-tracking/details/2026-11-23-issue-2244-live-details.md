# Details 2244 live

P1: each helper returns True only when every expected object exists (sys.tables, sys.triggers, sys.indexes, COL_LENGTH, sys.columns). Non-ledger databases additionally require the three trigger names. Ledger databases require audit to be APPEND_ONLY_LEDGER_TABLE, else return False so the locked path raises its explicit error.
P2: fake `db.execute` recording statements.
