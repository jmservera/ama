<!-- markdownlint-disable-file -->
# Plan critique: 441-c9-links-formulas-review-1848

Execution: independent `rubber-duck` agent, one pass, before any code. Verdict: Complete, Revise (nine findings).

| # | Severity | Finding | Direct disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Freshness fails with untracked tracking files | Accepted: pin `origin/main` SHA; require tracked tree and `docs/`, `src/` clean; tracking artifacts reported separately |
| 2 | Blocking | Proposed ADR ambiguous | Accepted: the unregistered proposal under `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/` is the ADR; ADR 0007 is unrelated; include in lint, links, hashes, review |
| 3 | Blocking | Some of the 30 custody inputs were not copied | Accepted: report matched, mismatched and not-archived separately |
| 4 | Blocking | Prior link method ignored anchors and images | Accepted: re-run the new method on the pre-#1519 parent blobs and label new-method-only findings unclassified |
| 5 | Blocking | Lint baseline optional, counts hide differences | Accepted: compare normalized individual diagnostics with the same tool and config on the pre-#1519 parent blobs; otherwise mark unproven |
| 6 | Blocking | Review scope excludes BRD/PRD/proposal bytes | Accepted: review prompt names exact hashes and includes those files; publication gates stay explicitly unmet |
| 7 | Non-blocking | Definition-aware traceability | Accepted: parse actual BRD and PRD definition formats; verify mapping namespaces |
| 8 | Non-blocking | Formula table is 12 rows x 3 | Accepted: verify all 12 rows against unrounded recomputation |
| 9 | Non-blocking | Verifier lacks fixtures | Accepted: small unittest file with positive and negative cases for slug, links, rounding |

No advice conflicts with a confirmed decision. No significant divergence needing a user decision.
