<!-- markdownlint-disable-file -->
# Research: PR 1295 main-provenance hash repair (2026-11-09)

* Task: `pr-1295-main-provenance-hash-repair`. `hve-core-all:rpi-agent`, Claude Sonnet 5.5, worktree `ama-demo-wt/pr1295-main-provenance-1109`, branch `docs/capstone-provenance-1295-1109` from `origin/main` `ad679b96b8c14f79623e0cc03dbf52d9d0fba99e` (tree `10dcf107794c1ccb556641745c323750de8168c0`).
* Research disposition: executed (coordinator brief, common rules, original C5 brief, C4 handoff, C4 Readiness closure, updater source, live checks on the clean tree).
* Planning Readiness: Ready.
* Lineage: a prospective continuation of the SAME C5 repair (fifth of five correction cycles, already consumed by the original C5 output of four dirty files). It creates no new cycle, no reset and no sixth cycle. The owner independently merged PR 1295 at head `5f1014` into `ad679b96b`; that merge is not reopened or overwritten. The old `pr-1295` worktree, its committed C5 records and its four dirty files are preserved untouched and read only as originals; no phase or record is fabricated or copied from them.

## Evidence (current tree, before any edit)

* `node docs/architecture/update-architecture.mjs --check` exits 1 with `Stale native source: docs/architecture/zava-forward-executive-architecture.excalidraw` (log `/tmp/ama-1295-mp/pre-update-check.log`, not committed).
* Cause: `docs/architecture/update-architecture.mjs` lines 87 to 90 hash the ENTIRE `infra/README.md` into each element's `customData.evidence`. Current `infra/README.md` sha256 is `be99190c627ea3678eabf9e33637e3c34be5695d01e8fbd0c7d8c87a3159399c`; both legacy excalidraw files still bind `07b3a8e3...` (2 hits executive, 4 technical). Main commit `4fcd1934f` (issue 144) changed the changes row near `infra/README.md:1333`; anchor line 1 is unchanged.
* `docs/capstone/source/diagrams/architecture/test-architecture.mjs` exits 1 only through its generator test (it invokes the updater `--check`); its SVG `data-native-sha256` test passes today because the SVGs still match the stale excalidraw bytes. After the excalidraw change the two legacy SVG hashes must follow.
* `build-architecture.mjs --check` exits 0 (capstone diagrams not stale; log `/tmp/ama-1295-mp/pre-build-check.log`). Capstone diagrams, catalog, receipt, PPTX, PDF, PNG, pitch, runbook, QX, financial and manifest files are not implicated.

## Scope boundary

Exactly four files: `docs/architecture/zava-forward-{executive,technical}-architecture.excalidraw` (evidence hash only) and the matching two `.svg` files (`data-native-sha256` only). Owner merge `5f1014` added issue 144 source and docs, not these hashes. If any other file proves necessary, STOP that finding and ledger it outside this zero-budget repair; no extension is approved.

## Not in scope

No render, rebuild, visual change, `control.json` wording, native or AT acceptance, runbook or QX edits, private data, Azure, models or global installs. This is pure documentation: no full gate (owner demo-targeted tier).
