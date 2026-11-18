<!-- markdownlint-disable-file -->
# Plan: issue #126 residual and unassessed-check source assessment

* Task: `issue-126-residual-source-assessment`; date 2026-11-17; mode automatic
* Research: `.copilot-tracking/research/2026-11-17/issue-126-residual-source-assessment-research.md` (Planning Readiness Ready)
* Phase details: `.copilot-tracking/details/2026-11-17/issue-126-residual-source-assessment-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-11-17/issue-126-residual-source-assessment-plan-critique.md`
* Validation tier: focused (read-only, evidence-only; no application, security control, permission, package, infrastructure, deployment, gate-semantics or runtime-instruction change)

## Objective

Produce a bounded current-source traceability and assessment table for the existing eleven residuals and eleven unassessed checks at HEAD `01baf8d3df86a28f754da8545d0e8f12012bf350`, preserving baseline versus current distinctions, with no approval, closure or main-acceptance claim.

## Boundary

* Writes: `.copilot-tracking/**` and the external evidence directory only. No application, tests, SQL, config, gate, agent or policy edits, no tick or closure of #126, no push or PR.
* No new human, real-model, cloud or paid activity; no synthesised signatures, thresholds or outcomes.
* Disposition vocabulary: `implemented/source-tested`, `deployed-observed` (= observed), `proposed`, `insufficient`, `independent-acceptance` (= independently accepted). Repository evidence alone never yields observed or independently accepted; both are listed as unavailable per row. Roles are proposed/inferred, never appointed (critique PC-001..PC-005 applied; see Critique Disposition).

## Critique Disposition

One critique executed 2026-11-17 (verdict Revise). Applied directly: PC-001 role labelling, PC-002 executed-and-passed test rule, PC-003 sanitised `env -i` execution, PC-004 separate version and EU applicability fields, PC-005 vocabulary mapping. No user decision required; no repeat critique.

## Phases

* [x] P01 Establish lineage, versions and import paths (done in Research; `git rev-parse` blobs recorded in table)
* [x] P02 Row evidence capture: for each of 22 IDs record baseline status/verdict/severity, code and test references (symbol plus line at HEAD), blob ids, version evidence, accountable role, disposition and missing-evidence/resume condition
  * [x] P02-T01 Residuals (11)
  * [x] P02-T02 Unassessed (11)
* [x] P03 Bounded verification: at most two test-command batches (core; api plus agents) using own-source `PYTHONPATH`, temp `ZF_DATA`, timeouts; record exact command, exit code and counts; map evidence ids to rows; unperformed items stated
* [x] P04 Assemble table and changes record; verify lineage facts (commit, tree, ancestry, blob ids, working-tree cleanliness of non-RPI paths)
* [x] P05 Single original Review restricted to the 22 rows (inline verifier evidence, lineage/fidelity, gaps)

## Dependencies and Order

P02 before P03 (the batches target referenced tests); P03 before P04 (results feed rows); P04 before P05. Witness events: plan-done, then changes artifact before implement-start, implement-done, review-done, commit-complete.

## Acceptance for this candidate (not the issue)

* All 22 IDs present exactly once, with every field non-empty or an explicit "none recorded"/"unperformed".
* Every code/test reference exists at HEAD (checked by a mechanical existence check).
* No row claims observed, independently accepted or closed; DOWNGRADED is not treated as closed.
* Test results reported as run, with unrun items listed.

## Follow-Up Items

* Qualified owner, DPO/Legal, Finance, real-model, witnessed restore and EU applicability evidence, per row resume conditions.
* Authorised publication of this candidate (not given).
