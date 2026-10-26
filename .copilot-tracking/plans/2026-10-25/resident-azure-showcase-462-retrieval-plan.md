# Plan: private demo-password retrieval proposal (issue 462)

Written 2026-10-25 after `research/2026-10-25/resident-azure-showcase-462-retrieval-research.md`, before critique. Refs #462. Proposal only: no source change, no cloud action, no push.

## Phases

1. Reduce the research to a decision between A (new private client, retrieve from vault) and C (owner-chosen password, vault holds verifier and session key only).
2. Write the proposal with exact approval wording, role, duration, cost, audit exposure, cleanup, residual risk and what stays unproven.
3. One independent critique of the proposal (once). Apply compatible findings and record the outcome.
4. Local commit with the privacy-safe identity and trailer. No push. Report.

## Acceptance

* Facts and hypotheses separated; no secret, personal identity, token or credential written.
* No claim of verified headroom; the USD 50 cumulative incremental cap is not reset; authority ends 2026-10-26T12:00Z; group `ama` only.
* Open corrections kept separate: Medium proxy-shared limiter and Low email-equality finding block deployment.
