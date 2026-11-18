<!-- markdownlint-disable-file -->
# Changes: issue #126 historical batch A/B log retention correction

* Task: `issue-126-retention-correction`; date 2026-11-17; plan `.copilot-tracking/plans/2026-11-17/issue-126-retention-correction-plan.md`
* Status: Implement complete (record written before the table edit; results below).

## Planned change

* In place: `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md` line 332 final sentence and one appended dated section "Retention Correction (2026-11-17)".
* New dated issue126 retention-correction artifacts only otherwise. No non-tracking path.

## Superseded claims (history preserved, not rewritten)

* Active table line 332 earlier text: "Parent batch A/B logs were not retained at the original location".
* `.copilot-tracking/reviews/logs/2026-11-17/issue-126-restart-followup-review.md` info finding 2 repeats the same wording. That Review and the restart-follow-up changes record stay unchanged; this record identifies the claim as superseded.

## Results

* Table edited in place: line 332 final sentence corrected (inaccessible to the confined worker, not lost) and a dated "Retention Correction (2026-11-17)" section added before "Unchanged boundary". The only remaining "not retained at the original" text is the quoted superseded claim.
* Direct observations: `sha256sum` of the supplied copies matched `8fd8668b...e0cc` (A) and `0235f289...d7daee4` (B), equal to the table's recorded hashes; final lines A `Ran 251 tests`, `OK (skipped=18)`; B `Ran 270 tests`, `OK (skipped=67)`. External copies: `/mnt/tmp/ama-run-81a96abb-126-20261117T1332/evidence-retention-correction-1455/run/`.
* Coordinator-reported only: original-path readback; not directly observed.
* `git diff --name-only` outside `.copilot-tracking/`: none. Tracking diff: one modified table, new retention-correction research, plan, details, critique, changes and state files.
* No test, browser, SQL, Docker, scanner or gate run. Prose detector: no detector found in `tools/`; scoring unavailable, not claimed. HVE static/behavior checks not applicable (research documentation only). No web edits or accessibility claim.
* Unchanged: inline verifier unrecovered; reconstructed verifier limitation; MAP-01 qualifications; skipped SQL/telemetry coverage; RAI/human approval boundaries; per-id log verification not performed.
