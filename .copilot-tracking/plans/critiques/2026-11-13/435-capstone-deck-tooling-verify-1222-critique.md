# Plan critique: 435 capstone verify-only

Reviewer: rubber-duck (independent, read-only), run before any test or script.
Verdict: Revise.

Findings (all applied directly in details.md "Revisions after critique"):

* Blocking: test-geometry.mjs and the export_diagrams test in test_conceptual_figures.py launch Chromium and may write under docs/; exclude and report unverified.
* Blocking: hash mapping omitted asset_catalog_sha256, native_helper_sha256 and historical_native; enforce per-field convention.
* Blocking: pytest-style files can pass with zero tests under unittest; run with pytest and require nonzero collection.
* Non-blocking: use venv python explicitly, disable pytest cache, compare git status before and after.
