# Issue 222 live demo plan details

Phase 1: from `src/agents`, run `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_cohort_ranking_eval tests.test_cohort_ai_eval tests.test_cohort_manifest_draft`. Expect OK and seven blockers.

Phase 2: research note states head SHA, command, result, table of six criteria, and why OQ-018 approval is unproven (owner decisions exclude DPO and Legal; #1905, #1906). Index row and log entry added.

Phase 3: changes record with proven/unproven table; review once; commit with trailers and repo-local noreply email.

Non-applicability: mypy, ruff and the web checks do not apply (no source or web change); no Azure action so the live apps and Event Hub are untouched and no throwaway resource exists.
