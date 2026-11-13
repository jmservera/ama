# Changes: 435 capstone verify-only run (Refs #435)

Base 74a93a137a983e0a87418e3321a6847ba9bcd278. No `docs/` or `tools/` edits; no rebuild. `git status --short --ignored` identical before and after the runs. Scratch venv `/tmp/venv-435cap` (system-site-packages, pip only, PyMuPDF 2.0 and pytest 9.1.0 from `tools/capstone/requirements.txt`) removed afterwards. Exit codes are the direct producer `$?`.

## Test suites

| Suite | Runner | Result | Exit |
| --- | --- | --- | --- |
| `tools/capstone/test_render_preview.py` | pytest | 10 passed | 0 |
| same file | `python -m unittest` | 0 tests collected (pytest-style, not accepted as a pass) | 5 |
| `history/cowork-main-presentation/test_build_assets.py` | pytest | 23 passed, 1 failed | 1 |
| `anc/test_measurement_provenance.py` | unittest | 13 OK | 0 |
| `anc/test_paper_tooling.py` | unittest | 14 OK | 0 |
| `anc/test_protocol_planning.py` | unittest | 10 OK | 0 |
| `anc/test_review_metrics.py` | unittest | 11 OK | 0 |
| `anc/test_conceptual_figures.py` | not run (launches Chromium via export_diagrams.mjs); 9 tests collected only | collect 0 | n/a |
| `source/diagrams/architecture/test-architecture.mjs` | node | 11 tests: 8 pass, 3 fail | 1 |
| `source/diagrams/architecture/test-geometry.mjs` | not run (playwright-core Chromium) | unverified | n/a |

### Failures (reported, not fixed; verify-only scope)

* `test_build_assets.py::test_given_current_native_deck_when_checked_then_cost_comparison_preserved`: `build_assets.py --check-only --check-pptx` against the committed `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` exits non-zero (stderr not captured by the test output).
* `test-architecture.mjs`: `native sources have unique editable elements and source-backed evidence` (line 77 hash mismatch), `all four editable views include the complete sensor chain...` (hash mismatch), and `the SVG and native derivatives match the explicit generator` (`build-architecture.mjs --check`: "Stale derivative: cxo-architecture.excalidraw"). The committed architecture derivatives are out of step with their generator or recorded hashes at this commit; deck-side hashes below still match.

## validation.json SHA-256 (all 10 verified fields match)

| Field | File | Match |
| --- | --- | --- |
| `package.candidate_sha256`, `linux_preview.source_sha256` | `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` | raw bytes |
| `linux_preview.pdf_sha256` | `docs/capstone/deck/zava-forward-cowork-v2-draft.pdf` | raw bytes |
| `package.baseline_sha256` | `docs/capstone/source/baseline.pptx` | raw bytes |
| `package.manifest_sha256` | `docs/capstone/source/slides.json` (brief's `slides.json`; none in `deck/`) | LF-canonical |
| `package.asset_catalog_sha256` | `docs/capstone/source/assets/catalog.json` | LF-canonical |
| `package.builder_sha256` | `tools/capstone/Invoke-Capstone.ps1` | LF-canonical |
| `package.native_helper_sha256` | `tools/cowork-native-recovery/Invoke-StoryReview.ps1` | LF-canonical |
| `pitch.speaker_script_sha256` | `docs/capstone/pitch/speaker-script.md` | LF-canonical |
| `pitch.questions_and_answers_sha256` | `docs/capstone/pitch/questions-and-answers.md` | LF-canonical |

(Files are LF, so raw and LF-canonical coincide for text.) `historical_native` hashes refer to a historical PowerPoint build with no committed artifact: unverifiable.

## Not verified

Browser-backed tests (geometry, conceptual figure export), native PowerPoint, human acceptance.
