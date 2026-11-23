# Research: #2164 r5 (2026-11-23)

Disposition: executed (re-verification). Planning Readiness: Ready.

* The fix 6a03928ccb (#2274) is an ancestor of HEAD 9dbfab6f56; `Assistants.authorize` (src/core/src/zava_forward/core/assistants.py:1507) re-reads the bound roster row and applies role, disabled, active, case_ids and areas.
* Tests re-run: src/api two #2164 tests OK; src/core `test_assistants_identity` 5 OK.
* Live, read-only: `ca-cutover-test-demo-api--0000055` (created 2026-11-23T03:25Z, 100% traffic), `ca-resident-demo--0000027`. Digest sha256:b628e067... is not traceable to a commit (ACR network-restricted), so deployed behaviour is circumstantial only.
* A live behavioural proof needs a roster edit on live data, a production change excluded by the owner decisions.
* Evidence note to extend: docs/reference/research/issue-2164-roster-scope-recheck-2026-11-22.md.
