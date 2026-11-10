<!-- markdownlint-disable-file -->
# Review: paired-equity anchor ID collision correction, 2026-11-08 (author review, one pass)

Changes: [changes](../../changes/2026-11-08/paired-equity-id-collision-123-changes.md). Plan: [plan](../../plans/2026-11-08/paired-equity-id-collision-123-plan.md). Refs #123, #440, #128.

Execution: author self-review, once. Outcome: CLEAN for the bounded correction, gate Pending. Not an independent assessment.

## Assessed

* The new finding was reproduced red with a real run before any production edit (status `pass` for a colliding anchor), then fixed minimally and verified green.
* Behavior preserved: existing tests pass, differing-ID failures and `_comparability` precedence retained; no ranking or policy change; flags unchanged.
* Limits: duplicate anchor IDs unrelated to the pair case are not guarded (critique IC-003, deliberate). Other malformed anchors (no `id`) are tolerated by `.get`, with ranker behaviour unchanged. Constructed diagnostics remain non-evidence of population fairness or real-model quality.
* No new defect confirmed beyond the reproduced one.

## Routing

* Open: fresh gate and partial receipt verification (this session, external); independent exact-head assessment and hosted checks (coordinator). Held: whole #123, #128, #440, AC073, human, legal, DPO, resident, AT, actual-model and Azure acceptance.
