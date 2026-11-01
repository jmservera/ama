# Changes: #175 source provenance

* `provenance-register.json`: confirmed OGL v3.0 licence and attribution for SRC-CENSUS-TS054, SRC-IMD-2025, SRC-ONS-BOUNDARIES; retrieval dates left null.
* `src/core/tests/test_synthetic_provenance.py`: strict audit now expects only missing retrieval dates.
* `data-dictionary.md` audit table and `docs/reference/log.md` updated.
* Validation: test_synthetic_provenance (12) and test_needs_inventory (11) pass; ruff check, ruff format --check and mypy clean for src/core.

## Review-thread amendments (PR #648)

* SRC-ONS-BOUNDARIES attribution now carries both required ONS statements (ONS source statement and OS copyright/database-right); the OS year stays `[year to confirm]`, so the strict audit reports `provisional_attribution` until verified. Licence confirmed against the ONS digital-boundaries guidance.
* Test now asserts exactly four audit issues and adds provisional licence and attribution mutations.
* `docs/reference/README.md` index row and dictionary criterion row reconciled with the register.
