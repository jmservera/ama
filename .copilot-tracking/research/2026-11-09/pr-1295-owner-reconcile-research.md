<!-- markdownlint-disable-file -->
# Research: PR 1295 owner-head reconciliation (2026-11-09)

* Task: `pr-1295-owner-reconcile` (parent `pr-1295-cxo-story-validation`, grandparent `pr-1295-cxo-story-recovery`).
* Research disposition: executed (new investigation; the prior validation research covers the old 54-slide head only and is not reused as proof).
* Planning Readiness: Ready.

## Identities (fetched before research)

| Item | SHA |
| --- | --- |
| Run branch `docs/demo-recovery-pr1295-1109` HEAD | `1d831ab3da49a8aa12320b1ac7540d9f1a7ce558` |
| Owner remote `origin/docs/capstone-cxo-story` | `0bcf55da1d516c82567e6eb44357343054c69b76` |
| Old PR head (recovery parent) | `b671116d571b76ebbbc9e277a791e67f781609cd` |
| Owner commit | `292d0091a` docs(architecture): add IoT telemetry and resident deployment views (author and committer `jmservera`) |
| `origin/main` | `b46a9ad9a9619db535368d1b2cbbddec8110e122` |

* Remote head is `0bcf55da1` = merge of `b46a9ad9a` (main, #1299) into `292d0091a`; first parent is the owner commit on top of `b671116d`.
* `b671116d` is an ancestor of the run HEAD and of the remote head, so the run branch and owner remote share the old PR head as merge base; the run branch only adds 12 `.copilot-tracking` files (recovery and validation evidence).
* `git merge-tree --write-tree HEAD origin/docs/capstone-cxo-story` completes with exit 0 and no conflicted path (read-only dry run). The two sides touch disjoint paths.

## Owner-only scope (`b671116d..292d0091a`, 48 files, +19373/-2322)

* Deck: 54 to 55 slides. New `S11A` "Azure connects home evidence to owned action." at physical page 13; `slides.json` schema 2 (`part_number`, `baseline_number`, `insertion`); original pages 13-54 move to 14-55 with codes unchanged. Page 12 (CxO concept) is enlarged and carries an IoT/telemetry addition. Delivery PPTX 3619820 -> 4718352 bytes, PDF 3057936 -> 4217911 bytes.
* Diagrams: CxO, full Azure, core, and new `azure-deployment` (SVG/PNG) projections, plus technical/executive architecture under `docs/architecture/`; generator `build-architecture.mjs`, `export-reference.mjs`, `update-architecture.mjs`, `annotate-previews.mjs`; new `test-geometry.mjs`; extended `test-architecture.mjs`; `text-equivalent.md`.
* Authoring tooling: `tools/capstone/Invoke-Capstone.ps1` (+316), `Test-CostStatus.ps1`, new `Test-DeckInsertion.ps1`, `test_render_preview.py` (+38), `Invoke-StoryReview.ps1`.
* Contracts and docs: `assets/catalog.json`, `validation.json` (receipt), capstone READMEs, `speaker-script.md` (now 24:30 narration plus 5:30 reserve), `questions-and-answers.md`, `review-2026-11-08-cxo.md` (+201, owner local review and corrections), `THIRD-PARTY-NOTICES`, `skills-lock.json`, vendored `.agents/skills/excalidraw`, KB `README.md` and `log.md` entries.
* Claimed final deliveries (owner review text): PPTX SHA-256 `7cf5abf9...bc64`, PDF `09de4170...cc`, 303 package members, 108 fixed actions, 32 native-shape checks, 14 diagram checks. These are owner claims; this run must recompute them.

## Main-side scope (`b671116d` merge base to `b46a9ad9a`)

Main drift is `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, issue 1297 sensor MSSQL tracking and review records; no deck or diagram path. Taken only through the clean merge; the run executes no `rpi-checks`.

## Commands and prerequisites (current component README, `docs/capstone/source/README.md` at remote head)

* Build, Test-NativeShapes, Test-SourceHashes (`-SemanticOnly` then default), Test-DeckInsertion (needs a built candidate), Test-CostStatus, Verify, Linux preview and `pytest tools/capstone/test_render_preview.py`.
* Node checks: `build-resident-journey.mjs --check`, `build-architecture.mjs --check`, `docs/architecture/update-architecture.mjs --check`, `node --test test-architecture.mjs test-geometry.mjs` (needs `EXCALIDRAW_BROWSER_PATH`).
* Prerequisites present: isolated pwsh 7.6.9, Node v24.21.0, Python 3.12.3, `/usr/bin/google-chrome`, Playwright Chromium 1248, LibreOffice, `pdftoppm`. The `excalidraw` CLI is not on PATH; install only if a selected command fails for that actual reason, and only isolated.
* PowerShell `Invoke-Capstone.ps1` authoring logic and the JS generator/tests changed, so focused tests are required; documentation-only edits need none.

## Boundaries and gaps carried forward (checkpoint inputs, not acceptance)

* The deployment and CxO views show Bicep/source-coded structure and gated options; a diagram inventory is not Azure deployment, live IoT, model or resident-access proof. #136 resource coverage and the merged transport/UI/model chain of #184 and #1288 remain unproven; those issues are referenced, never closed.
* Native PowerPoint, AT/keyboard, projector and human rehearsal remain unverified on Linux; LibreOffice render is a preview.
* Draft/funding/approval caveats and financial arithmetic are untouched; owner statement of unchanged cost slides must be confirmed by the cost/hash checks.
* PR 1301 (issue 1294) must merge first; publication is outside this run.

## Decision

Merge the current owner remote locally (merge commit, no rebase), preserve both histories, then validate the merged tree against the actual commands above. No source, deck, diagram or financial edit is planned. If a check fails on the unchanged owner tree, reproduce it, record it and propose the smallest fix without applying it unless it is a tightly coupled correction with evidence.
