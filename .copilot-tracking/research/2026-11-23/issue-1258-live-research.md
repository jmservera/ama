# Issue 1258 research 2026-11-23

Disposition: executed (re-verification on head 342fad401d). Planning Readiness: Ready. Only AC5 of #1258 is unticked; AC1-4 re-checked by tests and a mutation.

Evidence: 146 tests OK across four ranking modules; mutation (parent fsync loop neutralised) failed 12 tests, source restored (no src diff). Live: ca-cutover-test-demo-api--0000054 (Healthy) and ca-resident-demo--0000026 are the latest revisions; the API has no ranking-archive env setting, so the archive path is not exercised live (local filesystem fix, mock proof only).
