# Issue 2254 verify-fixed research (2026-11-22)

Disposition: opened. Main already holds the fix (1be6940b90, merged in a6c0910c97, #2258). Open question: does the live demo API now show equal tile, map and list counts? Plan: re-run the prior read-only probe against ca-cutover-test-demo-api, compare revision and image, then run the local regression test on this head.

Result: executed. Live probe on revision ca-cutover-test-demo-api--0000053 (image sha256:065628c9...): tile 23, map 23, list 23; no case in map-not-list or list-not-map. Evidence: docs/reference/research/issue-2254-verify-2026-11-22/ (probe, result JSON, screenshot). Planning Readiness: Ready (verify-only, no source change needed).
