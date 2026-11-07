<!-- markdownlint-disable-file -->
# Plan: coordinator current-source intake (issue 1204, pass 5)

Written 2026-11-05T22:51Z before any implementation edit. Research: [.copilot-tracking/research/2026-11-05/coordinator-current-source-intake-1204-research.md](../../research/2026-11-05/coordinator-current-source-intake-1204-research.md). Details: [.copilot-tracking/details/2026-11-05/coordinator-current-source-intake-1204-details.md](../../details/2026-11-05/coordinator-current-source-intake-1204-details.md).

## Phases

* [ ] Phase 1: three bounded edits to the agent file (G1 retained-candidate capacity, G2 schedule provenance, G3 activity-handoff premise).
* [ ] Phase 2: contained HVE behavior tests under Auto-profile child runs with independent grading, including negative controls.
* [ ] Phase 3: focused checks at the final head.
* [ ] Phase 4: single RPI review, state, commit.

## Constraints

Frontmatter lines 1-5 unchanged; no new rule section; cross-reference the single admission source; no schedule or live mutation; no heavy gate; no push.

## Critique (single, final candidate)

Self-critique recorded before implement, no extra repeat: edits stay minimal; G1 must not double count (an open PR with a live session or frozen candidate is one unit); G2 must not claim live prompt text; G3 keeps the `--help` gate and the legacy `--apply` prohibition. Verdict: proceed, no significant divergence.
