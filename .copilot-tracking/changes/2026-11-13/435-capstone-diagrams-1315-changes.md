# Changes: #435

* Regenerated with pure Node: `build-architecture.mjs` (2 .excalidraw + 4 .svg under docs/capstone/source/diagrams/architecture), `docs/architecture/update-architecture.mjs` (executive/technical .excalidraw) and `docs/architecture/annotate-previews.mjs` (their .svg native-hash tags). test-architecture.mjs now 11/11. The last two were required by the test and sit just outside the named surface (divergence, same generator chain). PNGs untouched.
* build_assets.py: PPTX slide 52 qualifier "proposed" replaced by "planning" and "assumed workload" (matches the 55-slide deck); help text says 55-slide. Slide numbers were not stale. USD 0.440576/home scenario checks unchanged.
* test_build_assets.py: 2 negative tests for the new slide 52 qualifiers. pytest 26/26.
* Not run: test-geometry.mjs (needs excalidraw CLI/Chromium), pwsh Test-SourceHashes.ps1 (pwsh unavailable). No validation.json-pinned input changed (slides.json, catalog.json, Invoke-Capstone.ps1, helper, deck untouched).
* Known stale: catalog.json derivative hashes (diagram svg/native); infra fixed-line anchors in build-architecture.mjs have drifted. Routed as follow-up.
* ruff: 7 pre-existing errors and format diffs identical to HEAD; none added.
