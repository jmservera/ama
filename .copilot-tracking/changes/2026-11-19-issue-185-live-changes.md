# Changes: issue 185 live proof

Files: docs/reference/research/issue-185-live-20261119-2026-11-19.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry), evidence under .copilot-tracking/evidence/2026-11-19/issue-185-live/. No src change.
Tier: FOCUSED; checks: git diff review, link review. Azure: throwaway hub iot-thr185-30198 created, used, deleted and verified; no demo resource changed.

| Criterion | Proven? | Basis |
| --- | --- | --- |
| 1 Approach with credential owner | Ticked already | not re-tested |
| 2 One identity per home | Ticked already | re-observed live |
| 3 Credentials issued and stored without appearing in source or logs | Unproven (issuance partly proven) | issuance keys never in log; no durable store exists; Key Vault store is FULL-tier design |
| 4 Teardown removes all simulated identities | Unproven for demo (proven on throwaway hub registry) | demo hub private; throwaway hub zero residual by two reads |
