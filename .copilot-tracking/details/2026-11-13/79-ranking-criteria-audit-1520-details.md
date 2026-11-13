---
title: Issue 79 ranking criteria audit details
ms.date: 2026-11-13
---

## Phase 1 details

* Proof standard: a criterion is proven only when merged code and a passing test cover every word of the literal checkbox, and no step in it is a human, policy or deployment act.
* Criterion 1 (determinism): `test_golden_snapshot_order_and_byte_identical_rerun`, `test_old_version_stays_loadable_and_reruns_identically`, `test_json_and_sql_snapshots_agree`, `test_ranking_module_has_no_clock`.
* Criterion 2 (versioned, hash-verified): `test_tampered_policy_is_refused`, `test_policy_missing_a_field_is_refused`, `test_old_version_stays_loadable_and_reruns_identically`, `test_list_header_carries_policy_hash_and_as_of`.
* Criterion 3 (owner signs): mechanism `ranking.signoff_problems`; the shipped policy is unsigned and pinned so. Human act, not provable by code.
* Criterion 4 (scheduled and retained): publish, verify and retention-by-no-delete are tested; `SCHEDULE` records the scheduler as not configured, owner and retention not set. Not proven.
* Record the missing paths named in the brief and the cohort-balancing title gap.
