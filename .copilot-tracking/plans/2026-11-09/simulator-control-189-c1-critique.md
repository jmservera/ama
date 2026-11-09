<!-- markdownlint-disable-file -->
# Issue 189 C1 critique (2026-11-09)

Execution: one rubber-duck pass on the final candidate plan, details and research (no repeat). Verdict: Revise. No significant or divergent user decision was needed; every finding is compatible with the owner brief and was applied directly to the details.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | `test_lookalike_paths_never_reach_the_control` expects 404 for administrator-only POSTs; the moved gate returns 403 first | Applied: lookalikes run as administrator plus staff for 404 and as administrator alone for 403, both with no mutation |
| 2 | Blocking | HTTP 403 could come from the module alone and not prove the server gate | Applied: a test patches `simulator_admin.handle` and asserts it is not called for an administrator-only POST (server denial with the standard message) |
| 3 | Blocking | `git restore` would keep the bypass expectation (it is in the committed head) | Applied: explicitly rewrite the `test_entra_authoritative` assertion so every destination is "needs a role with this authority" for administrator alone |
| 4 | Non-blocking | Browser "error" state only a manual state | Applied: add a deterministic failed Stop (`live_control.write` patched to raise `OSError` in the in-process server) asserting the alert and an unchanged control |
| 5 | Non-blocking | Stop submission only presence-checked | Applied: submit Stop in send, expired and invalid-window states and verify revision and resulting control |
