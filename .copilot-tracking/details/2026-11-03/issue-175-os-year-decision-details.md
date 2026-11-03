# Details: issue 175 OS attribution year decision

* Phase 1: provenance-register.json, SRC-ONS-BOUNDARIES attribution ends "database right 2026"; new external_use_status "OS copyright year 2026 is an owner decision (2026-11-03); to confirm before external use"; rules text and verification updated.
* Phase 2: src/core/tests/test_synthetic_provenance.py (two tests); data-dictionary.md audit table and prose; src/core/README.md; docs/reference/README.md; docs/reference/log.md.
* Phase 3: PYTHONPATH=src python3 -m unittest tests.test_synthetic_provenance (12 OK); ruff; mypy --cache-dir=/tmp/mypy-175.
