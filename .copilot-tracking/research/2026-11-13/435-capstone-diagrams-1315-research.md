# Research: #435 Capstone diagram and asset-test repair

Disposition: executed. Planning Readiness: Ready.

Findings (read-only diagnosis):
* test-architecture.mjs fails 3 of 11 because build-architecture.mjs --check reports `Stale derivative: cxo-architecture.excalidraw`. The generator embeds SHA-256 of source files (src/, infra/, docs) that changed since #1295; regeneration with the pure Node generator (no Chromium; it writes only .excalidraw and .svg) fixes it.
* PNGs are not produced by build-architecture.mjs (export-reference.mjs is separate); PNGs left untouched.
* test_build_assets.py 1 failure: build_assets.py --check-pptx raises `PPTX slide 52: missing ... ['proposed']`. Slide numbers are unchanged (slide 6/11/21/32/36/52 verified in the 55-slide deck; S18 is on slide 22, B25 on slide 52, so the renumbering hypothesis was wrong). Slide 52 now reads "Observe, then assume ... Live gates: not run" and no longer contains the word "proposed".
* The USD 0.440576/home scenario stays on slides 21 and 52 and labelled planning scenario/assumed workload (Owner Q7).
* build_assets.py help text still says 54-slide.

Evidence boundary: deck, PDF, slides.json, validation.json are not modified.
