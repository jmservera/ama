# Issue 441 research: accept the resident portal ADR (2026-11-04)

Research disposition: executed. Planning Readiness: Ready.

## Already delivered (merged PRs referencing #441)

* #442 integrated BRD, PRD, addendum, UX and the unregistered proposal (id null).
* #454, #686, #726, #766, #881, #463: PRD backlog readiness, closure evidence, rechecks, owner disposition packet, demo disclaimer, isolated showcase.
* Issue criteria 1 to 4, 6 to 8 are ticked. Criteria 5 (FR-044/AC-084 disposition) and 9 (publication gates and independent review) are unmet.
* Do not redo: requirement integration, hashes, workload formulas.

## Findings

* Native registry is `docs/adrs/0001` to `0006`; the proposal was left `id: null` because the allocator and `docs/planning/adrs` expectations could not be reconciled. The next native number is 0007; the repository convention is a hand-numbered file in `docs/adrs/` (ADR 0006 precedent).
* The owner decision of 2026-11-04 accepts the ADR; this is the legitimate allocation authority.
* The proposal is 907 lines inside `.copilot-tracking/` with hash-bearing custody evidence; it must stay intact as history. The decision of record belongs in `docs/adrs/`.
* Diagram assets (Excalidraw, SVG, PNG) exist only under tracking; copy byte-identically to `docs/architecture/`.
* Stale statements ("unregistered", "id null", "registration UNMET") exist in BRD line 56, PRD lines 121 and 1358, architecture README and reference README row.
* Open decisions inside the ADR: none for the exercise choice. OD-52 to OD-55 (owners, routine-automation approval, identity and privacy model, targets) remain open and are listed in the ADR.
* The 2026-11-04 issue comment allows a demo-only routine exception on synthetic data; it is not an OD-53 approval.

## Slice

One docs PR: ADR 0007 (Accepted), assets, pointer updates, log entry. No code, so the focused tier applies; no security, infrastructure, SQL or deployment change.
