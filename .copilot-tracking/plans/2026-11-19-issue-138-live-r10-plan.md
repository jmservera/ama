# Issue 138 r10 plan and critique (2026-11-19)

Scope: criterion 6 repository half. Add tools/check-repo-secrets.py (stdlib, scans git-tracked files for high-confidence secret patterns, exact path+rule allowlist for synthetic test fixtures) and tools/test_check_repo_secrets.py. No src change, no workflow change: FOCUSED tier.

Critique (single pass, verdict proceed): risk of false positives is handled by an exact allowlist of the four known synthetic fixtures; wiring into src-ci.yml is excluded because a workflow edit takes the FULL tier and is routed as follow-up; the workflow-log half of criterion 6 stays unproven without a hosted run.
