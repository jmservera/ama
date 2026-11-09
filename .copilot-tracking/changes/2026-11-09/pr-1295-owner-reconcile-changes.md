<!-- markdownlint-disable-file -->
# Changes: PR 1295 owner-head reconciliation (2026-11-09)

Plan: [plan](../../plans/2026-11-09/pr-1295-owner-reconcile-plan.md). Order executed: research, plan/details, critique, merge, validation, review.

## Repository changes

* Commit `ab2be0780` adds the four prospective records (research, plan, details, plan critique).
* Merge commit `0fad69e4c94cec033b09b76372311d6d2a5ce512` (`git merge --no-ff`, parents `ab2be0780` and owner head `0bcf55da1`), tree `1b41d88a7502f22753f10c1e38c1c4e3a33815db`. No conflict; no rebase, reset or force. No source, deck, diagram, financial or KB edit by this run; `git diff --name-status origin/docs/capstone-cxo-story <merge>` lists only 16 `A` entries, all under `.copilot-tracking/` (12 recovery/validation records plus 4 reconcile records), none modified or deleted.
* Ancestry: `292d0091a`, `0bcf55da1`, `b46a9ad9a`, `b671116d5`, `399e31ac1` and `1d831ab3d` are all ancestors of the merge.

## Targeted validation (scratch `/tmp/ama-pr1295-owner-val-2535257`, not committed; tracked tree stayed clean)

Versions: pwsh 7.6.9 (isolated), Node v24.21.0, Python 3.12.3 (scratch venv), Chrome 155.0.8059.39, `@excalidraw/cli` 0.3.0 (isolated install under the scratch directory only after `which excalidraw` failed), LibreOffice 24.2.7.2.

| Check | Exit | Result |
| --- | --- | --- |
| Build | 0 | 55 slides and notes; PPTX SHA-256 `7cf5abf93936aaa3b676c766479e91327a79c1746215a3a837be37b906acbc64` equals delivered |
| Verify (build copy) and Verify (delivered PPTX copy) | 0, 0 | 55 slides and notes, assets, navigation, timing and protected cost evidence verified |
| Test-NativeShapes | 0 | 32 checks |
| Test-SourceHashes `-SemanticOnly` and default | 0, 0 | four bindings, exact delivery hash |
| Test-DeckInsertion | 0 | position 13, all 108 original actions retained, deployment notes/alt-text chain |
| Test-CostStatus | 0 | six pages, four negative mutations denied |
| pytest `test_render_preview.py` | 0 | 10 passed (old head had 9) |
| `build-architecture.mjs --check` | 0 | CxO and Azure sources/SVG verified |
| `update-architecture.mjs --check` | 0 | executive 57 retained + 38 new; technical 194 retained + 42 new |
| `node --test test-architecture.mjs test-geometry.mjs` | 0 | 14 pass, 0 fail, 0 skipped |
| `build-resident-journey.mjs --check` | 1 | Stale `resident-journey.excalidraw`: line anchor 21 vs 33 for `agent-request-challenge.md` |
| Linux preview (`render_preview`) | 0 | 55 PNGs, 108 destinations and hit regions verified; human_acceptance false |

* Receipt/delivery hashes: delivered PDF `09de4170ed89a845da9ffd61bc36e211a770f4d96944952e795e649187cf14cc`, speaker script `35dc5c30...d10a`, Q&A `5e600549...538a` equal `validation.json`. All 52 hashed asset-catalog entries (PNG, SVG, native source) match the files.
* Misuse disclosed: the first delivered-deck Verify ran on an empty output directory and exited 1 (needs an existing candidate); rerun with the delivered copy exited 0. The first `node --test` run exited 1 because the `excalidraw` CLI was missing; rerun passed after the isolated install.
* Journey failure is pre-existing: the same command fails on `b671116d` and `292d0091a` extracted to scratch; the file `agent-request-challenge.md` has its heading at line 33 since #1283 while the asset records 21. Not part of owner work or this PR's changed paths (journey source is unchanged since #558); not fixed here. Smallest proposed fix, for the coordinator: regenerate the journey derivative with the generator (no flag) in a separate change and rebind hashes if the catalog binds it; not applied.
* Preview comparison: regenerated preview PDF bytes differ from the delivered PDF (`b0ccb698...7188` vs `09de4170...`; embedded creation time). At 40 dpi 54 of 55 pages are pixel-identical; page 46 (B18) differs only in the "x" glyph of "No silent mock fallback", which this host renders as a missing-glyph box (font fallback); extracted text is identical. Environment difference, not a source mismatch; delivered PDF left unchanged.
* Visual inspection of pages 12 and 13 in the LibreOffice preview: legible; connector lines cross heading text near "HOME TELEMETRY / FINITE INTAKE" (page 12) and the gated-options heading (page 13). The geometry test passes, so this is a visual checkpoint input for the owner, not changed.

## Not run or not established

Native PowerPoint, AT/keyboard, projector and human rehearsal; Azure, live IoT, model or resident-access behaviour; Build-vs-delivery pixel comparison on native renderer; `rpi-checks`. Pages 14-55 were not individually inspected beyond hashes and text/page parity checks.

## Main drift

`origin/main` advanced during the run to `9814cf6b2` (#1301, `docs(validation): streamline local checks while preserving coverage`). It touches no capstone/architecture/tools path; `git merge-tree` of main into the merge commit is clean (exit 0). Not merged by this run (owner direction: merge the owner remote only).
