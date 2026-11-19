---
title: Issue 216 live changes
ms.date: 2026-11-18
---

Tier: FOCUSED (documentation and evidence only; no `src/` change). Refs #216.

## Files

* Added `docs/reference/research/eval-gates-live-216-2026-11-18.md` (research note).
* Added `docs/reference/research/eval-gates-live-216-2026-11-18/` (authorization, declared cases, scripts, `report-live.json` rules-only run, `report-model-container.json` model run).
* Updated `docs/reference/README.md` (index) and appended `docs/reference/log.md`.
* Added RPI research, critique, plan, details, changes, review and state records.

## Per-criterion status (#216)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set | Partly proven (demo) | Refusals 10 of 10; model-path citations 7 of 7 (95% interval 0.646 to 1.0); model reached on only 9 of 30 turns (demo meter, 20 calls per day); strict graded pass 7 of 10 (G05 ambiguous, G06 and G10 rules fallbacks, U01 scorer too strict) |
| Production-only items (named Legal and Compliance owners, independent grader, larger set, regulatory rule-card citations) | Unproven | Not demo-provable; the regulatory chat needs a role the test account lacks and is not a model |
| Other issue criteria | Already ticked | Not re-proven |

## Validation

* `python3 docs/reference/research/eval-gates-live-216-2026-11-18/scripts/score_inner.py` over the saved raw output reproduces the table.
* Markdown, link and `git diff` review. `rpi-checks.py --all` not run (no `src/` change).
* Spend: about 12 to 13 calls in a lost first run, 20 on the deployed endpoint and 9 in the container run, above the 45 declared; disclosed in the research note. No Azure resource created; no throwaway threads left.
