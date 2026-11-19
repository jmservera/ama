# Research: issue #126 live run 2 (2026-11-19)

Refs #126. Synthetic DEMO, desktop only. Research disposition: reused plus re-executed tests. Planning Readiness: Ready.

* Prior run `issue-126-live` (committed on main) found no criterion needing new code; evidence at `docs/reference/research/issue-126-live-2026-11-19.md`.
* Unticked criteria (6): protocol/DPIA/lawful basis approval (named human); track 22 findings with dispositions (engineering in `governance.py` `_rai_view`, tests pass; live dispositions need claims recorded by humans); fresh current-source assessment (assessment run, not code); qualified owner acceptance (human); real AI/SQL/Azure contract (SQL tests opt-in, skipped).
* Re-run today: `src/core` `test_governance` 88 OK, 18 skipped (opt-in SQL, no MSSQL variable set); `src/api` `test_governance_evidence_api` 10 OK.
* Finding: no unticked criterion is both demo-provable and unbuilt. Writing SQL tests against a throwaway Azure SQL would be SQL/infrastructure scope (FULL tier) and was not started.
