# Changes: issue #175 source retrieval dates (2026-11-02)

* docs/reference/research/retrofit-synthetic-data/provenance-register.json: retrieval_date 2026-10-01 and owner-decision basis for SRC-CENSUS-TS054, SRC-IMD-2025, SRC-ONS-BOUNDARIES; header note updated.
* src/core/tests/test_synthetic_provenance.py: audit expects only `SRC-ONS-BOUNDARIES:provisional_attribution`; dates and basis asserted.
* docs/reference/research/retrofit-synthetic-data/README.md, data-dictionary.md, src/core/README.md: stale "dates missing" statements corrected; criterion stays unmet.
* docs/reference/log.md: appended entry.

Validation: `unittest tests.test_synthetic_provenance` 12 tests OK (venv with `pip install -e src/core`, PYTHONDONTWRITEBYTECODE=1). Divergences: none.
