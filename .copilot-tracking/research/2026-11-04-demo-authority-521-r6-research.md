# Research: demo authority 521 r6 (2026-11-04)

Disposition: executed. Planning Readiness: Ready.

## Already delivered (merged)

* #590 and #690: source extension to end of January 2027 (core, SQL, helpers, docs, tests).
* #742: live SQL window moved to 2027-02-01T00:00 and 522 rows renewed (2026-11-01); app revision 0000005, expiry 2027-01-31T23:59:59Z.
* #877: owner decision 2026-11-03 moved the single source (`resident-demo.json`) to exclusive 2028-01-01T00:00Z; tests and cost note (USD177 vs USD700 cap).

## Conflict flagged

The task confirmation names exclusive end 2027-02-01T00Z. Main holds 2028-01-01T00Z under the newer-merged owner decision of 2026-11-03. Reverting the source would undo that decision without owner evidence, so source is unchanged. The live window already equals 2027-02-01.

## Live read-only evidence (2026-11-04)

* `ca-resident-demo--0000008` Running, Healthy, min 0 max 1, `ZF_DEMO_EXPIRES_AT` 2027-01-31T23:59:00Z.
* Eight jobs all Manual. External curl to the app returned no response (no sign-in check run).
* SQL constraint not re-probed (would need a job execution).

## Acceptance criteria status

1. Consistency across code/SQL/helper/docs/tests: merged evidence exists; independent exact-head review not shown. Unmet by this slice.
2. Cost estimate and cap: recorded (README). Met.
3. Rotation plan documented: met.
4. Live apply with owner confirmation, verified and recorded: the confirmed 2027-02-01 value is live and read-only verified today; the 2028-01-01 value is not live and not confirmed. Partly met.
