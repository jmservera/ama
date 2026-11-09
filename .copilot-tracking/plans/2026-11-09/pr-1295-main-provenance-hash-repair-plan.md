<!-- markdownlint-disable-file -->
# Plan: PR 1295 main-provenance hash repair (2026-11-09)

* Task `pr-1295-main-provenance-hash-repair`; research `.copilot-tracking/research/2026-11-09/pr-1295-main-provenance-hash-repair-research.md`; details `.copilot-tracking/details/2026-11-09/pr-1295-main-provenance-hash-repair-phase-details.md`.
- [x] Phase 1: regenerate the two legacy excalidraw files with `update-architecture.mjs` (no flag), then confirm `--check` exits 0 and `git diff` touches only evidence hashes.
- [x] Phase 2: set `data-native-sha256` in the two legacy SVGs to the new excalidraw sha256, changing nothing else.
- [x] Phase 3: prove metadata-only delta (JSON property delta, XML attribute delta, masked byte equality for text and geometry, PNG byte invariance) and run bounded checks: updater `--check`, `build-architecture --check`, `test-architecture.mjs`, `test-geometry.mjs` if Chrome is available, `git diff --check`, diff path inventory (exactly four product files).
- [x] Phase 4: record changes, authored review (once), state and handoff.
