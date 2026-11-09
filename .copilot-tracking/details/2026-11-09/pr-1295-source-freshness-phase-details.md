<!-- markdownlint-disable-file -->
# Phase details: PR 1295 source freshness (2026-11-09)

Plan: [.copilot-tracking/plans/2026-11-09/pr-1295-source-freshness-plan.md](../../plans/2026-11-09/pr-1295-source-freshness-plan.md). Environment: scratch `/tmp/ama-pr1295-c2`, reusing the C1 tool environment in `/tmp/ama-pr1295-owner-val-2535257` (pwsh 7.6.9, Node, Python venv, local `excalidraw` CLI, Chrome).

## Phase 1

* `sha256sum` of: discovery-journey `.excalidraw`, `.svg`, `.png`; `assets/catalog.json`; delivered PPTX and PDF; `validation.json`; both pitch files. Save to `/tmp/ama-pr1295-c2/before.sha`.

## Phase 2

* `node docs/capstone/source/diagrams/discovery-journey/build-resident-journey.mjs` (no flag).
* Structural proof: parse before/after native JSON; delete `customData` evidence `line`, `sha256`, `localLink` fields; the rest must be deep-equal. Compare SVG with its `<metadata>` line removed byte-for-byte.
* PNG: `excalidraw render resident-journey.excalidraw --out <scratch>/journey.png --padding 0 --scale 1.5 --max-width 2400 --max-height 840 --fonts-url none --browser-path /usr/bin/google-chrome`; compare sha256 with the catalog PNG hash.

## Phase 3

* Edit only `source_sha256` and `source_native_sha256` of `resident-journey` in `catalog.json` (plus `sha256` only if the PNG differs).
* `pwsh Invoke-Capstone.ps1 -Action Build -RepoRoot <repo> -OutputDir <scratch>/build` then `-Action Verify`; regenerate the preview with `python -m tools.capstone.render_preview`. Update delivered PPTX/PDF/pitch/`validation.json` only if their bytes or recorded hashes change.

## Phase 4

* Commands as listed in the plan (README "focused authoring regression set"). Pages 12 and 13: node geometry test over `cxo-architecture` and `azure-architecture`, and view the preview images.
