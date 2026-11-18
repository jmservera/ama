<!-- markdownlint-disable-file -->
# Phase Details: issue #126 historical batch A/B log retention correction

## P03-T02 Exact edits to `issue-126-residual-source-assessment-table.md`

* Line 332 final sentence: replace "Parent batch A/B logs were not retained at the original location, so test ids ... not for a passed result in a log." with wording that the logs were inaccessible to that confined worker, are retained, and that the new section below carries the qualified result. Keep the inline-verifier and reconstructed-verifier sentences verbatim. Keep the qualification that the follow-up checked test ids for existence in sources only; per-id log results were not verified by that follow-up and are not verified here (PC-001). Name the supplied copy paths and hashes separately from the coordinator-reported original path (PC-002).
* Append a section "Retention Correction (2026-11-17)" stating:
  * Superseded claim: line 332 earlier text and follow-up Review info finding 2 ("not retained at the original location").
  * Distinction: inaccessible-from-worker is not missing.
  * Directly observed by this worker: SHA-256 and final result lines of the two supplied copies; both match the hashes in the Commands Run section.
  * Coordinator-reported, not directly observed: both files at the original host-only path with matching hashes.
  * Historical results: A 251 tests, 18 skips, OK; B 270 tests, 67 skips, OK; historical, not new execution.
  * Unchanged: original inline verifier unrecovered; reconstructed verifier is a different helper with name-only/class-membership limitation; MAP1 qualifications, skipped SQL/telemetry coverage, evidence limits and RAI/human approval boundaries; no row disposition changes.

## Verification

* `sha256sum` on the two copies; final lines of each; relative-link check of new artifacts; `git diff --name-only` shows only `.copilot-tracking/`.
