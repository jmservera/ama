---
title: Issue 79 ranking criteria audit changes
ms.date: 2026-11-13
---

## Summary

Documentation-only audit of the four acceptance criteria of issue #79 (`Programme ranking, cohort balancing and transparent rationale`) against `origin/main` at `0893bbcdb`. No source, issue or remote was changed. Issue text was read with `gh issue view 79` on 2026-11-13.

## Path corrections to the brief

* `test_ranking.py` does not exist. Ranking tests are `src/api/tests/test_ranking_policy.py`, `test_ranking_scale.py`, `test_ranking_publication_wiring.py` and `src/core/tests/test_ranking_publication.py`, `test_ranking_publication_runner.py`, `test_ranking_archive_blob.py`.
* `src/api/src/zava_forward/api/web/programme.js` does not exist. The programme screen is `role-screens.js`, exercised by `src/api/tests/test_programme_screen.py`.

## Test runs (venv `/tmp/venv-79-1520`, `--system-site-packages`)

| Command (directory) | Result |
| --- | --- |
| `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_ranking_policy tests.test_ranking_scale tests.test_ranking_publication_wiring tests.test_programme_screen` (`src/api`) | 83 tests OK |
| `PYTHONPATH=tests python -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner tests.test_ranking_archive_blob` (`src/core`) | 136 tests OK |

## Per-criterion proof table

| Criterion (literal) | Issue box | Audit result | Code and test evidence | Residual |
| --- | --- | --- | --- | --- |
| Same data and policy version give the same order | `[x]` | Proven, bounded to the same data and the same verified policy content | ``ranking.py` has no clock (`test_ranking_module_has_no_clock`); fixed tie-break ending in case id; `test_golden_snapshot_order_and_byte_identical_rerun`; `test_old_version_stays_loadable_and_reruns_identically`; `test_json_and_sql_snapshots_agree`; `test_ranking_scale.py` (`test_same_order_for_any_input_order_byte_identical`, `test_ties_break_on_case_id`) | A version label alone does not pin content (see next row) |
| Policy file changes are versioned and hash-verified | `[x]` | Proven as worded for hash verification, tamper refusal and multi-version registry; version-bump enforcement is not enforced | `ranking.load_policy` and `policy_hash` refuse a mismatched `content_hash`; duplicate versions refused in `load_registry`; `test_tampered_policy_is_refused`; `test_policy_missing_a_field_is_refused`; `test_old_version_stays_loadable_and_reruns_identically`; `test_list_header_carries_policy_hash_and_as_of` | `load_policy` checks a self-declared hash. Content edited with a recomputed hash under the same version is accepted; no test or gate forces a new version. Candidate follow-up, not a blocker for the ticked box |
| Named policy owner signs the first rule order | `[ ]` | Not proven. Human act outstanding | `ranking.signoff_problems` and `is_signed` read a recorded sign-off; `test_shipped_policy_loads_with_owner_and_status_unchanged` pins `owner: "to be named"` and "Draft rule order, not yet signed off"; `test_unsigned_policy_publication_is_recorded_in_audit_and_response` | A named owner and a dated signed `ranking-v2` (or later) file bound to `rule_order_hash` are needed. Code cannot prove a person approved; leave unticked |
| Ranking snapshot publication is scheduled and retained (ADR 0002 deviation) | `[ ]` | Not proven. Publish, verify and archive are delivered; schedule and retention are not | `ranking_publication.publish`, `verify` and `overdue` and the manager-only publish route are tested (`test_ranking_publication*.py`, `test_ranking_publication_wiring.py`, blob archive tests). `test_module_has_no_clock_and_no_delete` is module-level source evidence only. `SCHEDULE` states runner "deployment scheduler (not yet configured)", owner "to be named", retention "not set" | A configured deployment scheduler, a named schedule owner and a Legal-set retention period are outstanding; these are deployment and policy decisions |

## Conclusion

* The two ticked boxes are supported by merged code and passing tests, with the stated boundaries.
* The two unticked boxes must stay unticked. Both depend on human or policy decisions (named owner sign-off; scheduler, owner and retention period) that merged code and tests cannot prove.
* The issue title mentions cohort balancing; `ranking.py` has no cohort-balancing logic and no acceptance criterion covers it. Flagged for the owner, not changed.
* No contradiction found with the issue's own "Existing delivery and status" text.

## Evidence pointers

* Research: `.copilot-tracking/research/2026-11-13/79-ranking-criteria-audit-1520-research.md`
* Plan: `.copilot-tracking/plans/2026-11-13/79-ranking-criteria-audit-1520-plan.md`
* Critique: `.copilot-tracking/critiques/2026-11-13/79-ranking-criteria-audit-1520-critique.md`
