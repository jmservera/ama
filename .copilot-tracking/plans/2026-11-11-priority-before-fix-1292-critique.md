# Critique: priority before-fix 1292 plan (2026-11-11)

One independent read-only rubber-duck critique over the research, plan and details. Verdict: Revise.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Historical evidence misstated: errors were schema-related (missing created_ord), and the native SQL log records ordering failures in four reload tests | Applied to research line 30 |
| 2 | Blocking | Verifier could overclassify a partial red | Applied: exact selector ids, counts, exit, MIXED label, per-method assertion identification (plan P5) |
| 3 | Blocking | Clean-worktree precondition false with untracked records | Applied: tracked-path equality plus untracked allowlist (plan P0) |
| 4 | Non-blocking | Prediction plausible not guaranteed; incremental method may fail at cold load | Applied (plan P5) |
| 5 | Non-blocking | Isolation and timing: sanitized env, sys.path inside each process, 1190 s budget reconciliation | Applied (plan P3) |

Compatibility of selected APIs, imports and OwnedMssql setup was judged compatible by inspection; native bootstrap remains an execution question. No tests-directory shadow package or conftest was found. Blob identities match. The 148-test pass belongs to an earlier source revision.
