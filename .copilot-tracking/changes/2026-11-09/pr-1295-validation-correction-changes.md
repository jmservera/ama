# Changes: pr-1295-validation-correction

Parent: pr-1295-owner-reconcile. Frozen start 53ff97579. Fresh origin/main 76db469b1 (read 2026-11-09). Owner remote 0bcf55da1 unchanged. Correction cycle 1 of 5 used.

## Defect 1: resident-journey --check (classified, no source change)

* Reproduced on a `git archive` of fresh main 76db469b1 and on this branch: `Stale generated asset: resident-journey.excalidraw` (heading line 21 recorded, 33 current for `agent-request-challenge.md`).
* The generator reads 22 locator inputs under `docs/`. This PR changes only `docs/reference/README.md` and `log.md`, neither is an input. The input changed on main by `ecb28815b` (#1283), an ancestor of the merge-base `b46a9ad9a`. Verdict: confirmed main defect, not PR-introduced. No journey source changed here.
* Local result now: `build-resident-journey.mjs --check` exit 1 (recorded, not waived). Publication gap: that README-listed check stays red until the separate fix lands.
* Separate fix draft (not applied): regenerate `resident-journey.excalidraw` and `.svg` with the existing generator (PNG is byte-identical), update the two catalog hashes, rebuild the deck and receipt. Acceptance: `--check` exit 0, Build/Verify green, no layout or text change. Dependency: sequence with PR 1295 because `catalog.json`, `validation.json` and the PPTX collide. No existing open issue found by `gh issue` search on the heading and generator names.

## Defect 2: page 12 and 13 connector/heading overlap

* Page 12 (CxO): the `application-boundary` rectangle left edge cut `sensor-caption` and the IoT Hub node. Geometry tests ignored boundary rectangles. Confirmed, PR-introduced (main has no such page).
* Page 13 (Azure deployment): no crossing; three dashed arrows run about 1 px under `deployment-options-label`. Near contact only, left unchanged and recorded.
* Inherited `docs/architecture` executive/technical drawings have older crossings: out of scope.

## Files changed

* `build-architecture.mjs`: new closed `outline` line primitive; `application-boundary` is an L-notched polygon; `sensor-caption` moved to x=290 (width 765); `sensor-quality-context` arrow rerouted to x=1070.
* `test-geometry.mjs`: new test "capstone boundary outlines never cut through label or node text" (failed before the fix with `application-boundary -> sensor-caption/iot-hub-title/iot-hub-body`).
* `test-architecture.mjs`: `line` allowed only for `application-boundary`, closed and `polygon`.
* `cxo-architecture.{excalidraw,svg,png}` regenerated (PNG 2400x1275 with the existing CLI settings; old-source render reproduced the old PNG hash, so rendering is deterministic). `text-equivalent.md` describes the notch.
* `assets/catalog.json`: three `cxo-architecture` hashes. `validation.json`: candidate, catalog, PDF and both pitch hashes; `visually_inspected_pages` narrowed to 12 and 13 with a scope note. Delivered PPTX, PDF and two pitch files (candidate hash line only) replaced.
* Deck: sha256 343d133a252010d9de61ee064141e81d93f6a5e9a9f0efe915f50947e50cbb1a (was 7cf5abf9). PDF b8ec7712c834a3ac04e5d1f9b5aecb1bf3ecfc900933e8f7172fa93ddc803d27 (was 09de4170), a LibreOffice 24.2.7.2 Linux preview, not native rendering.

## Validation (isolated scratch, exits)

| Command | Exit | Result |
| --- | --- | --- |
| Invoke-Capstone Build | 0 | 55 slides, notes, 108 navigation actions, 303 members |
| Invoke-Capstone Verify (delivered copies) | 0 | same |
| render_preview | 0 | 55 images, 108 jumps verified |
| Test-NativeShapes | 0 | 32 checks |
| Test-SourceHashes (semantic and default) | 0 | pass |
| Test-DeckInsertion | 0 | pass |
| Test-CostStatus | 0 | pass |
| pytest test_render_preview.py | 0 | 10 passed |
| build-architecture.mjs --check | 0 | pass |
| update-architecture.mjs --check | 0 | pass |
| node --test architecture + geometry | 0 | 15 pass, 0 fail (was 14) |
| build-resident-journey.mjs --check | 1 | expected main defect |

Skipped: rpi-checks --all (owner-directed), native PowerPoint, AT, projector, rehearsal.

## Visual coverage

Pages 12 and 13 viewed from the new preview, plus the CxO PNG; page 12 shows no outline or connector through text. Not a whole-55-page inspection. Unchanged-page comparison and the previous aligned-page counts were not reproduced; the receipt says so. Host font glyph difference on page 46 is untouched.

## Remaining

Native PowerPoint, AT, projector and rehearsal unverified. #136, #184, #1288 Refs only. Owner review of the notch assumption (Home sensors outside, IoT Hub through SQL history inside the logical boundary).
