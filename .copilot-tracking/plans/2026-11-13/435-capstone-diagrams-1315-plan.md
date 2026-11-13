# Plan: #435 diagram and asset-test repair

1. Run `node build-architecture.mjs` to regenerate the 4 .excalidraw/.svg derivatives; verify `test-architecture.mjs` 11/11. PNGs untouched.
2. In build_assets.py, remove the stale `"proposed"` qualifier from the PPTX slide 52 requirement (deck text no longer says it), keep all figures including USD 0.440576/home and "planning/secondary price/unknown/not run" qualifiers; fix help text to 55-slide. The slides.json B25 check keeps "proposed".
3. Run pytest test_build_assets.py (24/24), ruff check/format --check on build_assets.py, validation.json SHA-256 recheck, git diff --check.
Out of scope: deck pptx/pdf, slides.json, validation.json, PNGs.
Alternative rejected: editing the deck (out of scope).

## Critique (rubber-duck, executed once) - verdict Revise; dispositions
* Replace "proposed" with present qualifiers "planning scenario" and "assumed workload" and add a negative test: ACCEPTED.
* Catalog hashes (docs/capstone/source/assets/catalog.json) go stale after regeneration: REJECTED for this task. catalog.json is outside the owned surface and validation.json pins its hash (asset_catalog_sha256) which must stay unchanged per the brief; routed as follow-up needing owner re-baseline decision.
* Fixed-line infra anchors in build-architecture.mjs have drifted: REJECTED here (generator and infra out of owned surface); routed as follow-up.
* PNGs preserved: ACCEPTED (verify untouched).
