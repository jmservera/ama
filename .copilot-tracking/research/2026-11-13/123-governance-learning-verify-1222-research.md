# Research: Epic #123 governance verification (123-governance-learning-verify-1222)

Base: 74a93a137a983e0a87418e3321a6847ba9bcd278. Research disposition: executed (local listing only). Planning Readiness: Ready.

Required docs (case study original/addendum, knowledge-base README, memory) confirmed present; memory is context, not evidence.

## Test module inventory (repo-relative, under src/)

* core/tests: test_discovery_assistant_{boundary,demo,drafting,evaluation}, test_discovery_flow, test_discovery_register, test_gates, test_journey_{acceptance,building,register,store,trace}, test_learning_test_bundles, test_paired_equity, test_cohort_eval, test_rai_release, test_rai_release_invalidation, test_resident_journey_design
* agents/tests: test_ai_eval, test_chat_eval, test_cohort_ai_eval, test_cohort_manifest_draft, test_cohort_ranking_eval, test_eval_registry, test_gate_agreement, test_paired_report_command, test_paired_trial, test_regulatory_gates
* api/tests: test_accessibility_baseline, test_assistant_release, test_case_journey, test_production_ux_acceptance_protocol

Shared helpers: agents/tests/regulatory_gate_fixture.py, agents/tests/cohort_eval_fixture.py, api/tests/release_support.py. Cross-package imports mean api needs ../core/tests and ../agents/tests on PYTHONPATH (never mvp).

## Constraints

Tracking-only write surface; no src/ or docs/ edits; no network, Docker, browser, private data.
