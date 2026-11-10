<!-- markdownlint-disable-file -->
# Phase details: PR 1295 main-provenance hash repair (2026-11-09)

* Phase 1: run `node docs/architecture/update-architecture.mjs` from the repository root. It rebuilds each legacy native source from the original artifact head `b671116d5` plus the extension scene, so only the `infra/README.md` evidence sha256 should change. Success: `--check` exit 0; `git diff --stat` shows two excalidraw files; every changed line is a 64-hex value on a `sha256` line.
* Phase 2: replace the old `data-native-sha256` value in each SVG with `sha256` of the new matching excalidraw file. No other SVG byte changes.
* Phase 3: compare old versus new by JSON property path (expected delta: only `elements[*].customData.evidence[*].sha256` where `path` is `infra/README.md`) and XML attribute (only `svg@data-native-sha256`). Mask 64-hex runs and require byte equality for the remaining text and geometry. PNG files and all other tracked paths must be unchanged (`git diff --name-only`).
* Stop rule: any need for another path, or a failing check not fixed by these hashes, is recorded as an out-of-budget finding and not repaired.
