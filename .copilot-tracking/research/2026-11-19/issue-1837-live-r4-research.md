# Issue 1837 live research, pass 4, 2026-11-19

Base `7ea3a1ff6`. Builds on the dated records of 2026-11-18 and 2026-11-19 and on `docs/reference/research/issue-1837-live-demo-evidence-2026-11-19.md`.

## Findings

* Criteria 1, 3 and 4 are proven on source or locally (see that note). Source on main already contains the fix for the transport defect (#1878) and the stylesheet and axe fix (#2110).
* The only functional criterion not proven live is 2 (valid writes retained). Live probe 2026-11-19: unauthenticated POST to `/api/cases/ZF-1/resident` on `ca-cutover-test-demo-api` returns HTTP 401 for both urlencoded and JSON bodies, so it does not show whether the deployed revision `0000033` (created 2026-11-18T22:39Z) parses form bodies. An authenticated live write needs a redeploy from main, a production change the owner excluded.
* Criteria 5 (independent exact-head review, hosted CI) and 6 (external full receipt) need a human, a push or the forbidden `rpi-checks.py --all`.
* Planning Readiness: Ready, no buildable criterion remains.
