# Changes issue-222-live3

Refs #222. Tier FOCUSED (docs only, no src change; rpi-checks --all not run).

## Files

* docs/reference/research/cohort-evaluation-live-r3-2026-11-18.md (new)
* docs/reference/research/evaluation/cohort-eval-live-r3-2026-11-18/ (new retained output and probe)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/rpi-sessions/2026-11-18/issue-222-live-state.json overwritten at the mandated path; the previous content is in git history.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Paired cohorts vs expected-outcome manifest | Proven (synthetic, draft manifest) | unittest-raw.txt, baseline outputs |
| Seeded defects detected | Proven (4/4 ranking, 3/3 AI) | ranking-defects.txt, ai-biased.txt |
| Counts, errors, review burden, uncertainty reconcile | Proven (fixture) | per-cohort rows |
| Small or missing samples insufficient | Proven | ranking-baseline.txt |
| Unapproved thresholds block activation | Proven | activation allowed False x4 |
| Owner approval of cohorts, fields, thresholds (OQ-018) | UNPROVEN: needs named-human approval; synthetic is not fairness evidence; demo waives DPO/Legal | note section "Why the last criterion stays unticked" |

## Validation

* agents cohort tests 36 OK; core test_cohort_eval 36 OK.
* Live read-only probe: revision 0000032, policy 200, snapshot 200 (443 entries, no cohort fields). No Azure resource created.
