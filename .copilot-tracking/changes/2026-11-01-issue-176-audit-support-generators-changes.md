<!-- markdownlint-disable-file -->
# Changes: issue 176 audit support generators (2026-11-01)

* `src/core/src/zava_forward/core/synthetic/determinism_audit.py`: adds `public-pack` and `stock-epc` replays, per-generator seed override, 16 or 64 hex revision pattern, unavailable listing when the support directory is missing.
* `src/core/tests/test_determinism_audit.py`: expects six generators; tests missing support directory and 16 hex revisions.
* `docs/reference/research/retrofit-synthetic-data/README.md`, `docs/reference/log.md`: documented.

Validation (focused tier): `test_determinism_audit` 10 OK; `ruff check`, `ruff format --check`, `mypy` clean on `src/core`. Heavy gate not run; CI is the evidence.
Divergence: none.

## Correction cycle 2026-11-01 (PR 703 review threads)

* Six Copilot threads on determinism_audit.py addressed: per-generator revision length (core 64, support 16), checkout-independent support directory (argument, ZF_SUPPORT_GENERATOR, cwd/module search), isolated subprocess replays, intrinsic windows for pack and EPC, per-generator FAIL with diagnostics instead of a crash, and key summary provenance (version, generator_revision) added and audited.
* Validation: ruff check, ruff format --check, mypy and src/core unit tests.
