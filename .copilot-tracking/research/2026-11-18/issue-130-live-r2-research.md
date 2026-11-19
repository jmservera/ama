# Issue 130 live r2 research

Refs #130. Synthetic desktop demo, live Azure authorised (rg ama, cap USD 700). Task: re-prove nomination, self-referral, acknowledgement and challenge routes on the deployed demo.

Disposition: executed. Prior run (issue-130-live, merged in #1948) was blocked by a 403 identity defect on writes; this run rechecks the deployed image and retries writes.

Planning Readiness: Ready (evidence-only unless a src change is needed; src change would require STOP and FULL tier report).

## Findings

* Deployed image `ca-cutover-test-demo-api` revision 0000031 is still digest `sha256:5368f4e4...e17e5fb`, unchanged since the prior run.
* Rerun of `probe1.py` (raw: `.copilot-tracking/evidence/2026-11-18/issue-130-live-r2/probe1.out.txt`): reads 200; all four valid-shaped writes 403 "Reload your current staff identity before recording this step."; representative fields 400; 0 records; stage unchanged.
* Cause: `resident_decisions._operation` line 1112 compares `actor` with `_person(store, user.get("email"))`. Fixing needs `src/core` change, a redeploy and the FULL tier (security-sensitive identity control). Out of scope per brief: STOP and report.
* Offline: 19 core and 9 api nomination tests OK (retained in evidence dir).
* Only unticked criterion: authorized human representative evidence; excluded for demo.
