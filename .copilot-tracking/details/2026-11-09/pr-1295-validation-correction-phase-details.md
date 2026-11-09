<!-- markdownlint-disable-file -->
# Phase details: PR 1295 validation correction (2026-11-09)

Plan: [.copilot-tracking/plans/2026-11-09/pr-1295-validation-correction-plan.md](../../plans/2026-11-09/pr-1295-validation-correction-plan.md). Environment: scratch `/tmp/ama-pr1295-owner-val-2535257` (pwsh 7.6.9 at `~/.local/ama-tools/powershell/7.6.9/pwsh`, Node 24.21.0, Python venv, `excal/node_modules/.bin/excalidraw`, `EXCALIDRAW_BROWSER_PATH=/usr/bin/google-chrome`, LibreOffice 24.2.7.2).

## Phase 1: failing regression

* File `docs/capstone/source/diagrams/architecture/test-geometry.mjs`: add a test over the two capstone drawings (`cxo-architecture`, `azure-architecture`; the older `docs/architecture` drawings have inherited crossings and are out of scope). Collect outline elements: rectangles that own no `customData.container` text and every `line`. Build segments (rectangle edges; line points). Fail when a segment intersects any text box (reuse the existing `intersects` helper, which insets boxes by 1).
* Expect failures before the fix: `application-boundary` against `sensor-caption`, `iot-hub-title` and `iot-hub-body`.
* Command: `node --test docs/capstone/source/diagrams/architecture/test-geometry.mjs` with the scratch `excalidraw` on PATH and `EXCALIDRAW_BROWSER_PATH` set.

## Phase 2: source fix

* `build-architecture.mjs`: add `outline(id, points, colour, evidence)` creating an Excalidraw `line` (closed, last point equal to first, `backgroundColor` transparent, `polygon: true`, no bindings); export it from `scene`. In `cxo()` replace the `application-boundary` rectangle with `outline` using (404,12), (1572,12), (1572,812), (275,812), (275,578), (404,578), (404,12); set `sensor-caption` to x 290, width 700. Keep the id so `validate()` and tests that name it stay valid.
* `node build-architecture.mjs` (no flag) to write the CxO and Azure derivatives; confirm Azure outputs unchanged by `git diff --stat`.
* PNG: `excalidraw render cxo-architecture.excalidraw --out <scratch>/cxo.png --padding 0 --scale 1.5 --max-width 2400 --max-height 1275 --fonts-url none --browser-path /usr/bin/google-chrome`, then copy to `cxo-architecture.png`; check 2400 x 1275 and view it.
* If the Excalidraw CLI rejects or mis-renders the line, fall back to a two-rectangle-free alternative only with a new critique-free note recorded in changes (cycle 2); do not hand-edit the PNG.

## Phase 3: contract and delivery set

* `assets/catalog.json` `cxo-architecture`: `source_native_sha256`, `source_sha256`, `sha256` from the new files.
* `text-equivalent.md`: one sentence describing that Home sensors sit outside the outline notch and IoT Hub, Event Hubs, telemetry service and history store inside; confirm the rendering command text is unchanged.
* `pwsh Invoke-Capstone.ps1 -Action Build -RepoRoot <repo> -OutputDir <scratch>/build2` then `-Action Verify`; `python -m tools.capstone.render_preview --input <build2 pptx> --output-dir <scratch>/preview2`.
* Copy PPTX, PDF, `pitch/speaker-script.md` and `pitch/questions-and-answers.md` to the delivery paths when their bytes differ; update `validation.json` `package.candidate_sha256`, `package.asset_catalog_sha256`, `linux_preview.source_sha256` and `linux_preview.pdf_sha256` from the reports, check counts unchanged.

## Phase 4: validation

* Run the targeted list from the plan; record command, exit code, counts and skips in the changes record.
* View `preview2/slides/slide-012.png`, `slide-013.png` and `slide-038.png`; crop page 12 at 200 dpi for the telemetry band.
* Compare preview PNGs against the prior preview for unchanged pages to show which pages differ (expect page 12 only, plus metadata).

## Phase 5: review, state and commit

* Review record under `.copilot-tracking/reviews/logs/2026-11-09/`; changes under `.copilot-tracking/changes/2026-11-09/`; state under `.copilot-tracking/rpi-sessions/2026-11-09/`.
* Local identity: `git config --local user.email 8036360+jmservera@users.noreply.github.com`, name `jmservera`.
