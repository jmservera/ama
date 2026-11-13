# Details: 435 capstone verification

## Phase 2 commands

* `python3 -m venv --system-site-packages /tmp/venv-435cap`; `pip install --upgrade setuptools wheel`; install `tools/capstone/requirements.txt` (PyMuPDF, pytest) only if import fails; other packages only if a suite fails on a missing import, otherwise report blocked.
* Run each Python suite with `python3 -m unittest <file>` (brief) from the file's directory; pytest-style tests that unittest cannot collect are rerun with `pytest` and both recorded. Exit codes saved via `echo $? > /tmp/...rc` directly after the producer, output to file.
* Node: `node test-architecture.mjs`, `node test-geometry.mjs` in the architecture dir. Do not run build/export scripts. Suites must not write into the worktree; check `git status` after.
* Run with `PYTHONDONTWRITEBYTECODE=1`.

## Revisions after critique (verdict Revise, all accepted)

* Browser exclusions: `test-geometry.mjs` (launches Chromium via playwright-core) and the `export_diagrams.mjs` test in `test_conceptual_figures.py` (Chromium, writes under docs/) are NOT run; reported as unverified/blocked by the no-browser rule. Other tests in `test_conceptual_figures.py` run via pytest deselecting the browser test if separable.
* Pytest-style files (`test_render_preview.py`, `test_build_assets.py`) run with `/tmp/venv-435cap/bin/python -m pytest -p no:cacheprovider`; unittest is also tried but a zero-test unittest pass is not accepted; require nonzero collected counts.
* Use the venv's explicit python for pip/pytest; `PYTHONDONTWRITEBYTECODE=1`; compare `git status --short --ignored` before and after.
* Hash map adds `asset_catalog_sha256` -> `docs/capstone/source/assets/catalog.json` and `native_helper_sha256` -> `tools/cowork-native-recovery/Invoke-StoryReview.ps1`. Convention per Test-SourceHashes.ps1: the four source inputs (manifest, catalog, builder, native helper) use CRLF/CR->LF canonical text hash; `candidate_sha256`/`source_sha256`, PDF and baseline use raw bytes; pitch markdown hashes tried under both conventions with the matching one reported. `historical_native` hashes refer to a historical PowerPoint build and are reported unverifiable unless an artifact exists.

## Phase 3 mapping

See research Evidence. `deck/slides.json` from the brief is `source/slides.json`; `Invoke-Capstone.ps1` is under `tools/capstone/`; speaker script and Q&A are under `docs/capstone/pitch/`. Deviations are recorded.
