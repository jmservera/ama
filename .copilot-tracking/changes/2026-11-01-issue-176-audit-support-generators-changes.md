<!-- markdownlint-disable-file -->
# Changes: issue 176 audit support generators (2026-11-01)

* `src/core/src/zava_forward/core/synthetic/determinism_audit.py`: adds `public-pack` and `stock-epc` replays, per-generator seed override, 16 or 64 hex revision pattern, unavailable listing when the support directory is missing.
* `src/core/tests/test_determinism_audit.py`: expects six generators; tests missing support directory and 16 hex revisions.
* `docs/reference/research/retrofit-synthetic-data/README.md`, `docs/reference/log.md`: documented.

Validation (focused tier): `test_determinism_audit` 10 OK; `ruff check`, `ruff format --check`, `mypy` clean on `src/core`. Heavy gate not run; CI is the evidence.
Divergence: none.
