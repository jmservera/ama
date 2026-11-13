# Plan: verify src/orchestrator tests at 3b05143179

Research: [research](../../research/2026-11-13/115-orchestrator-verify-1143-research.md)
Details: [details](../../details/2026-11-13/115-orchestrator-verify-1143-details.md)

* [ ] P1 Independent critique of this plan (before any venv, test or script)
* [ ] P2 Initialize changes file, record implement-start
* [ ] P3 Create /tmp/venv-orch-1143, editable-install core, agents, importer, orchestrator, verify paths inside worktree
* [ ] P4 Run unit suite from src/orchestrator with env -u ZF_DATA -u ZF_TEST_MSSQL, PYTHONPATH=../core/tests, save log and true exit code
* [ ] P5 Record per-module counts, skips, log sha256, exit code in changes file; remove venv
* [ ] P6 Independent review, then commit with Refs #115, #144, #148
