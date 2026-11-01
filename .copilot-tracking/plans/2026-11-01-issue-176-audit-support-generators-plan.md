<!-- markdownlint-disable-file -->
# Plan: issue 176 audit support generators (2026-11-01)

Research: `.copilot-tracking/research/2026-11-01-issue-176-audit-support-generators-research.md`

## Phases

* [x] 1. Extend `determinism_audit.py` with `public-pack` and `stock-epc` generators loaded from `support/.../generator`; report them unavailable (not passed) when the directory is absent.
* [x] 2. Accept `sha256:` plus 16 or 64 hex characters as revision; keep truncated or oversize values failing.
* [x] 3. Update tests in `src/core/tests/test_determinism_audit.py`.
* [x] 4. Update the retrofit synthetic data README and `docs/reference/log.md`.
* [x] 5. Focused validation: unit tests, ruff check, ruff format --check, mypy on `src/core`.

## Critique (single pass)

Verdict: proceed. Risk: generic module names (`zf_*`) on `sys.path`; mitigated by reusing the same insertion the existing test uses and removing the path afterwards. No Azure, no private data: a fictional register is written to a temporary directory.

## Correction cycle 2026-11-01 (PR 703 review threads)

* Six Copilot threads on determinism_audit.py addressed: per-generator revision length (core 64, support 16), checkout-independent support directory (argument, ZF_SUPPORT_GENERATOR, cwd/module search), isolated subprocess replays, intrinsic windows for pack and EPC, per-generator FAIL with diagnostics instead of a crash, and key summary provenance (version, generator_revision) added and audited.
* Validation: ruff check, ruff format --check, mypy and src/core unit tests.
