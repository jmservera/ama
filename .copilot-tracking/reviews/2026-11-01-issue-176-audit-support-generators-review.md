<!-- markdownlint-disable-file -->
# Review: issue 176 audit support generators (2026-11-01)

Execution: executed once after implementation. Outcome: Conformant for the delivered slice; criteria 1 and 2 remain unmet overall.

* Scope matches the plan; no Azure, private data, mvp/ or prototype/ changes.
* Tests sit outside the package; pip only.
* Residual (routed to later work): the original stock register generator and pinned OSM inputs are absent, so universal byte replay and complete manifest coverage cannot be proven. Pack seed override exists because seed 7 fails the pack generator's own validation.
* Human approval of the refresh policy remains outstanding and is not claimed.

## Correction cycle 2026-11-01 (PR 703 review threads)

* Six Copilot threads on determinism_audit.py addressed: per-generator revision length (core 64, support 16), checkout-independent support directory (argument, ZF_SUPPORT_GENERATOR, cwd/module search), isolated subprocess replays, intrinsic windows for pack and EPC, per-generator FAIL with diagnostics instead of a crash, and key summary provenance (version, generator_revision) added and audited.
* Validation: ruff check, ruff format --check, mypy and src/core unit tests.
