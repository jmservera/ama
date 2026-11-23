# Plan: live smoke 0000055 / 0000027 (issue 2237)

## Critique (executed once)

Verdict: proceed. Findings applied: record the revision names before and after the probes (traffic can change mid-run); repeat `/api/retention` in a burst so one 200 is not over-read; treat a probe failure as a fail row, not a retry-until-green; assert no credential text in saved output.

## Phases

1. Phase 1: read revision state with az. 2. Phase 2: one Playwright probe for the employee (sign-in, retention burst, chat thread POST, map with sensor items, start-up health via revision state and /healthz) and one for the resident (login, Sensors chart). 3. Phase 3: write the evidence note, README index row and log entry. No src edits; no Azure change.
