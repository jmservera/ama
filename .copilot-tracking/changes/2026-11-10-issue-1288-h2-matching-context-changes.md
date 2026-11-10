<!-- markdownlint-disable-file -->
# Changes and observation: issue 1288 H2 matching-context

Readback `date -u` 2026-11-10T00:25Z. Plan: `.copilot-tracking/plans/2026-11-10-issue-1288-h2-matching-context-plan.md` (one critique applied before observation). Verification only; E11 success, E12 and E13 unused. H0 and H1 records are unchanged and remain the historical a859 observations.

## Change manifest

* Ordinary merge of `origin/main` `ddeebd01694ddb46b456451d9ac6390347e51aaa` (accounting PR 1339) into this tracking-only branch, no conflict; `git diff origin/main HEAD` shows only `.copilot-tracking` paths, so product bytes equal pinned main. Merge commit `5d0460dd6c05312d0a905e69774d561c7ab8fc59` (tree `230c976d5ceaedea7515683f1746f685cc71d096`).
* New records: H2 research, plan (with amendment), details, critique, this changes file, review. No source, test, schema, workflow, config or shared-doc edit. The plan and critique timestamp readback was corrected from 00:24Z to the actual 00:22Z readback in a follow-up commit.

## Execution

* Holder inspected: no `fuser`/`lsof` holder, no running container. One `flock -n /tmp/ama-rpi-heavy.lock sql-run-h2.sh` at 2026-11-10T00:23:08Z, exit 0 (meta recorded dirty 2 = the two uncommitted timestamp-fix edits, tracking files only).
* Fresh owned loopback container (removed on exit; zero labelled containers remain), SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, image `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, Python 3.12.3, external venv built from the hash-locked requirements, editable core/agents/api; import identity proved to the worktree source paths.
* Harness `harness_h2_matching_context.py` sha256 `698c13ec5188f24e18d0d607331e1441beaf60e5b269fa83242bef4418f96ac4`; wrapper `sql-run-h2.sh` sha256 `68851d83f02127446b1d7c8c3d88ad5fee0b74fedff1dc832686df0f3a2940fe`.
* Process 1 (H2 alone on the fresh database): exit 0, Ran 1, OK, 0 skips. Process 2 (existing affected Quality MSSQL selectors): exit 0, Ran 30, OK, 1 skip (the SQLite-only cross-process withdrawal test, not waived), 29 ok. Selectors: the H0 list minus the H0, H2a and H2b harness tests.
* Raw (external) `logs-h2-matching-context-1110/sql-run/`: `h2.json` sha256 `1285e610f60ea9595b4de48a3af8de55eb4d4d872692352ef8bb328bebbc44e6`, `h2.stderr.txt` `78163f85005b...`, `existing.stderr.txt` `054d7af5b4f9...`; full list in `logs-h2-matching-context-1110/SHA256SUMS`.

## Observed result (H2 test)

* Prerequisites met: `fx-quality-evidence` active revision 1, first flag `review-suggested`, actionable, cited IDs non-empty, B and C runtime binding digest `b4791e0c22b1f1be` equal to the first provider's.
* B and C (new store, new connections, independent `CapturingProvider`, same `test-model` recipe and `release = store.release_context`, no `install`, no writes, no default `Ai`) read flag `review-suggested`, `display_state` `ready`, actionable, `release_denial` null, current release `fx-quality-evidence`; equal on cited IDs, ID/reading pairs, role projection (Quality Inspector and Retrofit Programme Manager allowed, others refused), task state and body hash. `b_differs_on` and `c_differs_on` are empty.
* All 11 `assistant_releases` rows (id, status, body hash, revision) were identical at all 47 recorded snapshots (before and after open_store, attach, construct, detail, release_reference and each sensors role call); `fx-quality-evidence` stayed active revision 1. No revoke occurred under the matching context.
* Provider counters: B and C 0 calls and 0 prompts before and after; the first provider served `proactive()` once (1 call) and its counters did not change during the observation. No stub peer in H2, so no byte claim is made for H2. 0 real provider, model or cloud calls.
* Existing 30 Quality MSSQL cases: 29 pass, 1 skip, no failure; the earlier H0 selectors that ran before H0 are the same set.

* Timestamp note: the readback preceding this record was 00:25:19Z; the first commit of this record carried 00:26Z in error, corrected here.
