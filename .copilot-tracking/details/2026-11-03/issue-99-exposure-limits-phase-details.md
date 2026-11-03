<!-- markdownlint-disable-file -->

# Phase details: issue-99-exposure-limits

## Phase 1

`record_limits(approval, envelope, tolerances)` validates a complete approval record, a non-negative finite envelope with currency and period, and tolerances limited to the six RULE-012 dimensions. `assess(limits, exposure)` returns Held when no limits exist, Breach or Unknown with the signal "Pause for human decision", or "No pause signal" when within every limit. The notice states it never approves, resumes or contains activity.

## Phase 2

Tests use synthetic values labelled as not company figures: held without inputs, validation failures, within limits, envelope breach, tolerance breach, missing or mismatched exposure.

## Phase 3

Append a log entry; no index change (no knowledge-base file added).
