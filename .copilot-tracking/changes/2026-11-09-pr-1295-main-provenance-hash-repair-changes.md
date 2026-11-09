<!-- markdownlint-disable-file -->
# Changes: PR 1295 main-provenance hash repair (2026-11-09)

Base `ad679b96b8c14f79623e0cc03dbf52d9d0fba99e`. Plan phases 1 to 3 complete; no divergence from plan except one self-corrected miss (below).

## Product files (exactly four)

* `docs/architecture/zava-forward-executive-architecture.excalidraw`: 2 `customData.evidence[*].sha256` values for `infra/README.md`, `07b3a8e3...` to `be99190c...`.
* `docs/architecture/zava-forward-technical-architecture.excalidraw`: 4 such values, same change.
* `docs/architecture/zava-forward-executive-architecture.svg` and `...technical-architecture.svg`: native-source sha256 in both `data-native-sha256` and the `zava-native-source` metadata element (executive `08bf04b2...` to `a9e10d19...`, technical `e219216c...` to `cea1bd8c...`).

## Evidence (scratch `/tmp/ama-1295-mp`, not committed)

* Before: `update-architecture.mjs --check` exit 1 (`Stale native source`); `test-architecture.mjs` exit 1 via its generator test; `build-architecture.mjs --check` exit 0.
* Regeneration: `update-architecture.mjs` exit 0 (executive 57 retained plus 38 new elements, technical 194 plus 42, unchanged counts).
* Self-corrected miss: the first SVG edit changed only the attribute; the second `zava-native-source` metadata hash was found by the delta script and fixed. `annotate-previews.mjs` run on a scratch copy is byte-identical to the final SVGs.
* JSON property delta: 2 (executive) and 4 (technical) changes, all at `elements[*].customData.evidence[*].sha256` with `path` `infra/README.md`. XML delta: two hash values per SVG. Masked (64-hex) bytes equal for all four files, so text and geometry are unchanged. No PNG or other path changed (`git diff --name-only` lists four files).
* After: `update-architecture.mjs --check` 0, `build-architecture.mjs --check` 0, `test-architecture.mjs` 11 of 11 pass, `git diff --check` 0.
* Not run: `test-geometry.mjs` (exit 1, `which excalidraw` fails; CLI not installed and global installs are out of scope), capstone `Verify`/`Test-SourceHashes` (no `pwsh`; no capstone file references these legacy diagrams and none changed), Python tests (no source change), full gate, private data, Azure, models.
* The four result files are byte-identical to the preserved dirty files in the old `pr-1295` worktree (compared with `cmp`, read only).
