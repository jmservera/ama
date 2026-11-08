<!-- markdownlint-disable-file -->
# Plan: fresh static review correction S01/S02 (issue 1204, pass 6)

Written 2026-11-05T23:18Z before implementation. Research: [.copilot-tracking/research/2026-11-05/coordinator-static-correction-s01-s02-1204-research.md](../../research/2026-11-05/coordinator-static-correction-s01-s02-1204-research.md). Details: [.copilot-tracking/details/2026-11-05/coordinator-static-correction-s01-s02-1204-details.md](../../details/2026-11-05/coordinator-static-correction-s01-s02-1204-details.md).

## Phases

* [ ] Phase 1: S01 admission rewrite plus launch cross-reference (agent file only).
* [ ] Phase 2: S02 handoff and step 6 HVE evidence clause (agent file only).
* [ ] Phase 3: focused checks (unittest with captured exit code, git diff --check, frontmatter, ASCII, links). No behavior rerun by order.
* [ ] Phase 4: changes record, process-incident record, single review, state, NEW commit (no amend).

## Constraints

Frontmatter and tools untouched; PR thresholds and 20-PR drain unchanged; no new rule section; no rebase; no push; no deletion.

## Critique (single, before implement)

Edits must stay inside existing bullets, with the launch and recount text pointing to the one admission rule. Pause conditions are all conjunctive (head proof, no live native, no unpublished work, preserved ledger) and Unknown keeps the slot. HVE clause conditional on behavior-bearing instruction changes. Verdict: proceed; no significant divergence from the supplied direction.
