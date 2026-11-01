---
title: Issue 223 human-review effectiveness review
ms.date: 2026-11-01
---

## Review execution

Executed once, self-review of the diff against the acceptance criteria. Independent human review is still required.

## Criteria

| Criterion | Status |
| --- | --- |
| Seeded critical defects detected and prevented from satisfying a controlled gate | Proven for scripted panels only |
| Reviewer, source and reason retained | Proven (real `review_ai` evidence plus source tag in reason) |
| Detection, corrections and effort reported against workflow-only scenario | Proven (scripted units) |
| Default acceptance and citation validity alone cannot pass | Proven for scripted baselines |
| Automation-bias test; reviewer authority and evidence defined (OQ-017) | Test included; authority provisional, OQ-017 not decided |

## Outcome

Partial. AC-070 as written needs competent human reviewers; not evidenced. PR uses `Refs #223`.

## PR review follow-up (2026-11-01)

Copilot review findings on edit completeness, ineffective-edit validation, source-hash retention and workflow effort comparability were fixed with tests; failing src-agents (eval registry) and src-core (provenance register) checks were fixed. Outcome above is unchanged.

Second follow-up: non-AI seeded runs, numeric-prefix edit collisions and unvalidated edited controls were fixed with tests. Outcome unchanged.

Third follow-up: repeated source labels (for example `Extra support: needed` and the adjustment text) no longer overwrite each other in the fact map, and a seeded defect is credited as corrected only when the gate's source-evidence check passes; regressions added. Outcome unchanged.

Fourth follow-up: a defect rejection or edit is credited only when its reason names the seeded topic and the source label of that discrepancy (an unrelated resolving citation no longer passes), and aliased repeated-label topics cite the original case label in findings; regressions added. Outcome unchanged.

## Follow-ups

1. Run an authorised human reviewer protocol once OQ-017 authority is decided.
2. Fold the seeded set into the #108 harness golden run and CI.
3. Replace scripted effort units with measured reviewer time.
