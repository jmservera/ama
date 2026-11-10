<!-- markdownlint-disable-file -->
# Critique: keyboard probe correction C1 (2026-11-10)

Execution: one rubber-duck critique of the final candidate plan. Verdict: three blocking design issues, all compatible with the confirmed decisions, applied directly (no user decision needed).

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Minimum-one region expectation lets single-region removal stay green | Applied: expectations become exact per-screen counts taken from the preserved observation (resident-choice 4, hazard-triage 3, asset-board 2, programme-queue 3, technical-queue 5, safety-lead 3, data-operator 2, contractor-job-pack 1) with a single-region-removal negative |
| 2 | Focus measure accepts transparent outline or unrelated shadow | Applied: measured visible means outline-style not none, outline width at least 2px, and non-transparent outline colour, or a non-none box-shadow; negatives remove the indicator and make it transparent |
| 3 | Combined status negative cannot prove each attribute asserted | Applied: independent negatives remove role, aria-live and aria-atomic one at a time, each keeping correct text, each must fail the walk status assertion |

Residual: exact counts are tied to the constructed fixture and fail loudly on change (intended).
