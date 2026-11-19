<!-- markdownlint-disable-file -->
# Task Research: issue #126 historical batch A/B log retention correction

## Status

* Phase: Research (opened 2026-11-17 after the coordinator launch record; opening text persisted before substantive research)
* Research disposition: executed (read-only inspection of the active table, earlier Review and follow-up records, and two supplied log copies)
* Planning Readiness: Ready (finalised after the findings below)
* Task: `issue-126-retention-correction`; state `.copilot-tracking/rpi-sessions/2026-11-17/issue-126-retention-correction-state.json`

## Scope and Lineage

* Start HEAD `66a2014a72b6b3652ec2d23f6f378cafacc41ed0` on `docs/rai-residual-source-assessment-126`. Declared parent topic `feat/demo-164-chat-grounding-provenance-0900` at `01baf8d3df86a28f754da8545d0e8f12012bf350` (PR 1641), not main. Any eventual child publication must declare this ancestry and target the parent topic; eventual main integration is separate. No rebase, retarget, push or PR here.
* Docs-only tracking correction. No source, test, gate, prompt, agent, skill, dependency or control file changes. Overall owner restart/demo delivery authority admits this finite correction; no human, privacy, RAI or approval gate is changed or claimed.
* Earlier adverse Reviews and historical research stay unchanged.

## Findings

* F1 (direct observation): the supplied copies `../evidence-retention-correction-1455/run/batchA.log` and `batchB.log` hash to `8fd8668b01bd4b624a26c464556d819b8a58ff3a81f772f869afcc9ba869e0cc` and `0235f289a27ca362c526de903685c07c200ca992d846f93de336536a7d7daee4`. These equal the hashes already recorded in the active table (batch A line 30; batch B alongside). Final lines: A `Ran 251 tests in 6.996s`, `OK (skipped=18)`; B `Ran 270 tests in 89.068s`, `OK (skipped=67)`.
* F2 (coordinator-reported, not directly observed): the coordinator found both files at the original host-only path `/mnt/tmp/ama-run-74bd1fe9-126-assess-20261117T1305/evidence-126-assess/run/` and verified the same hashes. This worker did not access that run root.
* F3 (defect): the active table (line 332) says the parent batch A/B logs "were not retained at the original location". That conflates inaccessible-to-the-confined-follow-up-worker with missing. The same wording appears in the earlier follow-up Review (info finding 2) and is historical; it is preserved and identified as superseded in new evidence only.
* F4 (unchanged limitation): the original inline verifier checks (69 path:line, 44 symbols, 38 blobs, 27 test ids) remain unrecovered. The reconstructed verifier is a different helper with a name-only/class-membership limitation. The supplied logs do not recover it.
* F5: the logs are historical executions from the earlier assessment, not newly executed tests. They do not change MAP-01 semantic qualifications, skipped SQL/telemetry coverage or any row disposition.

## Planning Readiness

Ready: one in-place sentence correction of the active table, plus a dated provenance clarification in the table and the new changes record.
