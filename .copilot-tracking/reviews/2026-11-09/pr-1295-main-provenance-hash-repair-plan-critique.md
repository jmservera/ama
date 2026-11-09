<!-- markdownlint-disable-file -->
# Plan critique (single pass): PR 1295 main-provenance hash repair

* Execution: executed once on the final candidate plan. Verdict: Approve with direct dispositions.
* Finding 1: the updater regenerates from `b671116d5`, so confirm the result differs from the current file only in hashes, not trust it. Applied: Phase 3 mandates property delta and masked byte equality.
* Finding 2: regeneration must not run from a dirty tree or write other files. Applied: the worktree is clean and Phase 3 inventories paths.
* Finding 3: the SVG test passes today, so SVG hashes are only due after the excalidraw change. Applied: Phase 2 follows Phase 1 and is verified by `test-architecture.mjs`.
* No conflict with a confirmed owner decision; no user decision required. No second critique will run.
