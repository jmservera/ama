---
applyTo: '.copilot-tracking/changes/2026-11-13/435-capstone-deck-tooling-verify-1222-changes.md'
---

# Plan: verify Capstone deck tooling (Refs #435)

Research: ../../research/2026-11-13/435-capstone-deck-tooling-verify-1222-research.md
Details: ../../details/2026-11-13/435-capstone-deck-tooling-verify-1222-details.md

## Phases

* [ ] Phase 1: critique plan independently (before any command).
* [ ] Phase 2: scratch venv (system-site-packages, pip only), run Python and Node suites, capture exit codes to files in /tmp.
* [ ] Phase 3: compute SHA-256 for every receipt hash (raw and LF-normalised) with read-only Python; no rebuild.
* [ ] Phase 4: write changes.md with counts, matches, exit codes; remove /tmp/venv-*; confirm `git diff --check` and tracked tree untouched except .copilot-tracking.
* [ ] Phase 5: independent code-review, review.md, commit with Refs #435 and trailer.
