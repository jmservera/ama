# Changes: Epic #123 verification (123-governance-learning-verify-1222)

Base 74a93a137a983e0a87418e3321a6847ba9bcd278. Tracking-only; no src/ or docs/ edits. Refs #123, #125, #126, #128, #129, #108.

## Method

* venv /tmp/venv-123-1222 (--system-site-packages, setuptools/wheel upgraded, editable --no-deps --no-build-isolation, PIP_NO_INDEX=1); removed after the run.
* Verified `zava_forward.{core,agents,api}.__path__[0]` under this worktree `src/<pkg>/src/`.
* Each module run as `env -u ZF_DATA -u ZF_TEST_MSSQL PYTHONPATH=<pkg tests + sibling tests> python -m unittest -v tests.<module>` from `src/<pkg>`; PYTHONDONTWRITEBYTECODE=1; no network, Docker, browser or LLM calls (api test_case_journey uses a local node DOM harness only).
* Critique (rubber-duck, Revise) added core test_governance (protocol, benefits, release gates); inventory is 19 core, 10 agents, 4 api.

## Per-module results (rc = true producer exit code; log = sha256 prefix of /tmp/v123-logs log)

| Module | rc | Ran | Skipped | Log sha256 (16) |
| --- | --- | --- | --- | --- |
| agents-test_ai_eval | 0 | 20 |  | 0b63c1e24d0d4460 |
| agents-test_chat_eval | 0 | 45 |  | 905b4b187b5496cc |
| agents-test_cohort_ai_eval | 0 | 5 |  | e00afe714638d94a |
| agents-test_cohort_manifest_draft | 0 | 11 |  | b52e401e1b94cdc8 |
| agents-test_cohort_ranking_eval | 0 | 20 |  | fe72b11b1d365abb |
| agents-test_eval_registry | 0 | 8 |  | d5cf216b7f57a2d7 |
| agents-test_gate_agreement | 0 | 7 |  | 8ee5eb38fea5752a |
| agents-test_paired_report_command.rerun | 0 | 21 |  | 27b4ecc659081b0f |
| agents-test_paired_trial | 0 | 10 |  | 628d32da7eeeffed |
| agents-test_regulatory_gates | 0 | 18 |  | 2466d02c32753a16 |
| api-test_accessibility_baseline | 0 | 13 |  | ba26f25a64595111 |
| api-test_assistant_release | 0 | 60 | 7 | 44aa074800645a3c |
| api-test_case_journey | 0 | 31 |  | 41248f1303bb9813 |
| api-test_production_ux_acceptance_protocol | 0 | 4 |  | bd3764c60f719949 |
| core-test_cohort_eval | 0 | 25 |  | 3854e196dd578891 |
| core-test_discovery_assistant_boundary | 0 | 11 |  | 10d20832691acc00 |
| core-test_discovery_assistant_demo | 0 | 14 |  | 7be4df6ed58ee580 |
| core-test_discovery_assistant_drafting | 0 | 8 |  | a39fbaf34e30b829 |
| core-test_discovery_assistant_evaluation | 0 | 8 |  | e50ef36fa8d6a7fc |
| core-test_discovery_flow | 0 | 6 |  | c5838dfb761a11e4 |
| core-test_discovery_register | 0 | 13 |  | bdfe2727d288e2e5 |
| core-test_gates | 0 | 22 |  | bc56ad16f15db9a8 |
| core-test_governance | 0 | 71 | 16 | 4acbd0f9f181ccab |
| core-test_journey_acceptance | 0 | 4 |  | 96e33d5a29d486d8 |
| core-test_journey_building | 0 | 6 |  | b86b013b9e0c4aae |
| core-test_journey_register | 0 | 7 |  | 988c22ea0703c04c |
| core-test_journey_store | 0 | 5 |  | e3f1e59e635b06b0 |
| core-test_journey_trace | 0 | 10 |  | 4e33486bed1aa3b5 |
| core-test_learning_test_bundles | 0 | 21 |  | 4fbf1783a035ad10 |
| core-test_paired_equity | 0 | 26 |  | 080a271d34c062b3 |
| core-test_rai_release | 0 | 6 |  | 5132010a44d4d4db |
| core-test_rai_release_invalidation | 0 | 6 |  | 05713c7f294fdf06 |
| core-test_resident_journey_design | 0 | 9 |  | 2bd27ce2eb9176f2 |

## Notes

* agents-test_paired_report_command: first parallel run hit the 170s timeout (rc 124, no result; first-run log sha256 prefix 98436c712fff44cc). Rerun alone with 400s timeout: rc 0, 21 tests OK in 124.7s, log sha256 27b4ecc659081b0fbad44eda2fa5aaa649d29a3cc233d5689705529ffa80e901. Cause is inferred to be parallel load (the standalone rerun passed); not independently proven.
* Skips (explicit): 16 in core test_governance, 'opt-in task-owned loopback SQL'; 7 in api test_assistant_release, 'needs disposable SQL Server (ZF_TEST_MSSQL=1)'. SQL-backed paths are therefore unverified here.
* Total tests across the 33 final module results: 551, 0 failures, 0 errors. Counts are per-module from the table.
* Scope: focused tier only, not the complete local gate; no hosted CI read; local freeze (no push/PR).
