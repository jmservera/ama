<!-- markdownlint-disable-file -->
# Research: PR 1295 failed authoring check and LibreOffice preview defects (2026-11-09)

* Task: `pr-1295-validation-correction` (parent `pr-1295-owner-reconcile`). Qualified native RPI agent, model Claude Sonnet 5.5, isolated worktree `docs/demo-recovery-pr1295-1109`.
* Research disposition: executed (new investigation of two defects the parent recorded but did not trace; parent evidence is reused only as a pointer, not as proof).
* Planning Readiness: Ready.
* Correction budget: five total scoped cycles (repository default 2026-11-09). This task plans one cycle; none spent beyond it.

## Identities (fetched at start)

| Item | SHA |
| --- | --- |
| Run HEAD (frozen start) | `53ff9757930242795d321626a0301f4a948449c7` (tree `9e84d7c5090697df1684323021c429699e70b5dd`) |
| Owner remote `origin/docs/capstone-cxo-story` | `0bcf55da1d516c82567e6eb44357343054c69b76` (unchanged) |
| `origin/main` (fresh fetch) | `76db469b16e7ac0ae862e8c9b19873fc66b04f0e` (`chore(rubric)` record on top of `9814cf6b2`, #1301) |
| Merge base HEAD / main | `b46a9ad9a9619db535368d1b2cbbddec8110e122` |

* Main moved from `9814cf6b2` to `76db469b1`; the new commit is a rubric score record. The previously reported main identity is therefore stale and is superseded here.

## Defect 1: `build-resident-journey.mjs --check` fails

Reproduction (scratch `/tmp/ama-pr1295-owner-val-2535257`, Node 24.21.0):

* On a `git archive` of fresh `origin/main` (`76db469b1`), `node docs/capstone/source/diagrams/discovery-journey/build-resident-journey.mjs --check` exits 1 with `Stale generated asset: resident-journey.excalidraw`: recorded locator `line 21`, sha256 `358b5ca0...`; current generated `line 33`, sha256 `825de34b...`, for `docs/reference/research/company/agent-request-challenge.md` (and its later anchors, for example 241 vs 253, 315 vs 327).
* The same failure was already recorded on `b671116d` and `292d0091a` (parent task). Those comparisons alone did not prove independence from the PR, so the whole-PR input set was traced.

Trace of inputs:

* The generator reads 22 locator inputs (all under `docs/`: the two case-study documents, the company, UX journey, sector and regulatory Markdown files). The excalidraw/SVG metadata embeds each file's line number and SHA-256.
* `git diff --name-only <merge-base> HEAD -- docs/reference docs/case_study_48_addendum.md docs/case_study_48_original.md` lists only `docs/reference/README.md` and `docs/reference/log.md`. Neither is a generator input. `git diff --name-only origin/main HEAD -- docs/reference docs/capstone/source/diagrams/discovery-journey` shows only knowledge-base differences that are main-newer or PR-only index entries, and nothing in the journey directory.
* The changed input is `agent-request-challenge.md`, last modified on main by `ecb28815b` (#1283, 2026-11-08), an ancestor of `b46a9ad9a`, the merge base, and of HEAD.
* Regenerating on main changes only `resident-journey.excalidraw` and `resident-journey.svg` (metadata locators and hashes); `resident-journey.png` bytes are unchanged, so the delivered slide image is not visually affected.

Classification: confirmed defect on current main, not introduced by this PR (no PR-modified file is a generator input, and the PR does not touch the journey directory). It is a source-to-asset staleness introduced by #1283 on main.

Decision: no source change in this PR. Smallest separate fix draft (for the coordinator, not filed): regenerate `resident-journey.excalidraw` and `.svg` with the existing generator, update their two catalog SHA-256 values (`source_native_sha256`, `source_sha256`; PNG unchanged), rebuild/verify the deck and refresh the receipt. It must be sequenced after or merged with PR 1295 because both edit `catalog.json`, `validation.json` and the delivered PPTX. Known-issue dedup: `gh issue list --state all` searches for the stale asset, the generator name and the input file returned no matching issue.

Affected publication gap: the README-listed regression `build-resident-journey.mjs --check` fails on main and on this branch, so the documented focused authoring regression set is not fully green until the fix lands. This is recorded, not waived.

## Defect 2: connectors cross heading text on pages 12/13 (LibreOffice preview)

Reproduction on current assets: the owner-selected preview (scratch `preview/`) rendered 55 PNGs; pages 12 and 13 were re-rendered at 200 dpi from the preview PDF and cropped. Fresh main has neither page: its `slides.json` has 54 slides, page 12 is a different slide, and `docs/capstone/source/diagrams/architecture/` does not exist on main, so the diagrams are PR/owner-introduced and the comparison with main is that the defect cannot occur there.

Findings (source obstacles in `build-architecture.mjs`, native `cxo-architecture.excalidraw`, `azure-architecture.excalidraw`):

* Page 12 (CxO view): the rectangle `application-boundary` (x 404 to 1572, y 12 to 812) has its left edge at x=404 and runs through `sensor-caption` ("HOME TELEMETRY / FINITE INTAKE + READ-ONLY ANALYSIS", x 30 to 950, y 590 to 616) and through `iot-hub` (x 290 to 500, with its title and body text). The line is a boundary edge, not an arrow; the visible symptom in the image is a vertical line through the word "INTAKE" and through the IoT Hub box. Existing geometry tests do not catch it: they check only newly authored arrows against text, image and service rectangles, and never check boundary/frame rectangle edges.
* Page 13 (Azure deployment): no arrow, line or rectangle edge intersects any text box (checked exactly and with an 8 px pad). With the pad, three dashed connectors (`deployment-production-target`, `deployment-queue-dependency`, `deployment-job-storage`) run horizontally at scene y 3040 to 3045 immediately under `deployment-options-label` (box y 3000 to 3039, 34 px text), a 1 px clearance from the text box and about 5 px on the 1600 px preview. The crop shows the dashed line below the heading without crossing glyphs. Classification: not a confirmed crossing; near-contact observation only, left unchanged and recorded. No other connector touches a heading on page 13.
* The geometry tests pass because (a) their wire check ignores arrows in `originalElementIds`, (b) it only protects text/image/service boxes against arrows with matching `frameId`, and (c) boundary rectangles are never tested. The text of the page 12 crossing is therefore a genuine PR-introduced geometry defect that the test contract does not cover.

Semantics preserved by any fix: the boundary is "logical application/data scope" (`text-equivalent.md`); devices and IoT Hub are device-side items; Event Hubs, the API telemetry service and Azure SQL telemetry remain inside it (owner layout, not changed). Dashed gated styling, node text, arrows, the 1600 x 850 canvas, 56 elements' ids and bindings stay.

## Candidate fixes for page 12 (evidence-ranked)

| Option | Result | Verdict |
| --- | --- | --- |
| End the boundary at y 578 above the telemetry band | API telemetry and SQL telemetry fall outside "application + controlled case data" | Rejected: changes meaning |
| Move the boundary left edge to include devices | The external inputs and devices become "inside" | Rejected: changes meaning |
| Shift or resize telemetry nodes to fit | Four inside nodes need about 1250 px against a 1168 px boundary at the 26 px font floor | Rejected: needs redesign |
| Replace the rectangle with one closed outline whose lower-left edge sits in the 30 px gap between Home sensors (right edge 260) and Azure IoT Hub (left edge 290), and move the caption from x 30 to x 290 | Home sensors and the external inputs stay outside; IoT Hub, Event Hubs, API telemetry and SQL telemetry stay inside as the owner's current membership implies; caption text, nodes, arrows and canvas unchanged | Selected |
| Same notch at x 515 (between IoT Hub and Event Hubs) | Caption cannot sit inside the boundary on one line without crossing arrow `sensor-quality-context` (vertical at x 1020, y 558 to 640); moving Event Hubs outside also alters the owner's membership | Rejected |
| Same notch at x 755 (outside: sensors, IoT Hub, Event Hubs) | Moves Event Hubs outside the application scope; owner-semantics change | Rejected |

Selected geometry (assumption for owner review): outline points (404,12), (1572,12), (1572,812), (275,812), (275,578), (404,578), back to (404,12). The notch edge at x 275 lies in the gap 260 to 290. The caption box becomes x 290 to 990 (measured text is about 640 units at 26 px, so it ends before the arrow at x 1020 and the 770 telemetry-service left edge is not involved). The outline is a native Excalidraw `line` so it stays editable; `application-boundary` keeps its id.

## Delivery chain (existing tooling)

* `build-architecture.mjs` writes `cxo-architecture.excalidraw` and `.svg` (and Azure derivatives; Azure sources do not change).
* `excalidraw render` (local `@excalidraw/cli` 0.3.0 with existing Chrome 155) writes the PNG at padding 0, scale 1.5, max 2400 x 1275, fonts-url none.
* `assets/catalog.json` pins native, SVG and PNG hashes (`cxo-architecture`); `text-equivalent.md` documents the layout; `Invoke-Capstone.ps1 -Action Build` and `Verify` regenerate and verify the deck, speaker script and Q&A; `validation.json` is the receipt regenerated from a successful Verify; `Test-SourceHashes.ps1` binds the four canonical sources and the delivered PPTX; delivered `docs/capstone/deck/*.pptx/.pdf` and `pitch/*.md` are the delivery copies.
* The PDF is produced by native Windows Render in the owner workflow; Linux only previews. The delivered PDF therefore cannot be regenerated honestly here and must be reconciled explicitly (see plan).

## Not established

* Native PowerPoint rendering, assistive technology, projector and human rehearsal.
* Whole 55 page visual inspection (only affected pages are re-inspected).
* Azure deployment, live IoT, model behaviour, #136, #184 and #1288 acceptance. The diagrams are source-model projections.
* A host-font missing glyph for "x" on page 46 does not authorize rewriting delivered text or installing fonts.
