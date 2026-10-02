<!-- markdownlint-disable-file -->

# Review: rubric-gate-change-detection

* Task ID: 2026-10-02-rubric-gate-change-detection (child of 2026-10-02-rubric-score-gate)
* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-change-detection-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-gate-change-detection-changes.md
* Parent review: .copilot-tracking/reviews/2026-10-02/rubric-score-gate-review.md (targets RV-001, RV-003 README part, RV-004, RV-012 docs part)
* Scope: .github/rubric/scripts/prepare.py, gate.py, test_gate.py, test_prepare.py; .github/workflows/rubric-score.md and .lock.yml; .github/rubric/README.md
* Mode: one pass, read only. No files other than this review were changed. Tests were not rerun; the changes log reports 28 passing cases run against a minimal pytest stub, and `gh aw compile` with 0 warnings.

## Outcome

Conformant with findings.

FR-1 to FR-5 and AC-1 to AC-4 are met. RV-001 is closed for the cases it named: deletion, rename out of scope, and growth past `max_file_bytes`, on pull request and push paths, including squash, merge-commit and rebase merges. RV-004 is closed. The README parts of RV-003 and RV-012 are mostly corrected. One Medium residual (RG-001) leaves a related way to hide evidence. The other findings are Low and cover documentation accuracy, how blind the calibration run is, and test gaps.

## Verified

* Deletion, PR path: `diff_args` uses `origin/main...HEAD`. `classify_changes` adds `D` paths and in-scope rename sources to `removed`. These are unioned after the `artifact["files"]` intersection (CC-002), so an artifact whose files were all removed stays in `changed_artifacts`, because a `None` fingerprint is not equal to the previous fingerprint. `test_given_pr_deleting_scored_file_when_gated_then_drop_counts` exercises this through `gate.evaluate`.
* Deletion, push path: the base is the last commit on `HEAD` that wrote `latest.json`. `test_given_direct_push_deleting_scored_file_when_computed_then_removed_detected` covers this.
* Rename out of scope: the source becomes removed and the out-of-scope target is ignored. This is unit-tested in `classify_changes` only (see RG-008).
* Oversize growth: an in-scope `M` entry for a file in `oversize` moves to `removed` through `hidden` (CC-004). The fingerprint also changes because the file leaves `files`. The logic is correct but untested (RG-008).
* Squash merge: the squash commit writes `latest.json`, so the range is `HEAD HEAD`. Its fingerprints were computed on the PR head tree, which equals the squash tree when the PR is up to date, so the run correctly skips. Merge commit: `git log -1 -- latest.json` follows the TREESAME parent to the bot commit on the PR branch, and the bot tree equals the merge tree when the PR is up to date, so the run skips. Rebase merge: the replayed bot commit is the tip. See RG-002 for PRs that were not up to date and for direct pushes.
* Bot `latest.json` commit: the path is outside every artifact glob, so it never enters `changed_files`. The push uses `GITHUB_TOKEN` and does not retrigger. It is the correct anchor for non-PR ranges.
* Force cannot alter the baseline: `gate.main` writes `latest.json` only when `not args.force`. The record step is guarded by `github.event_name == 'pull_request'`, and `FORCE` comes only from `github.event.inputs.force`, which is empty on PR and push events. Publish returns before any issue is created when `decision.calibration` is set. The lock declares the `force` input (L77) and binds `FORCE` at all three call sites.
* Issues are limited to `refs/heads/main`: `if (decision.calibration || context.ref !== 'refs/heads/main') return;` runs before `issues.create`, and only on the non-PR branch.
* `git ls-files` in the agent job after `restore_base_github_folders.sh`: the restore changes only `.github/` (and `.agents`, `AGENTS.md`). The index still reflects the PR head after `checkout_pr_branch`, and every active and planned artifact glob lives outside `.github/`. File lists and fingerprints therefore match `rubric_prepare`. The `.github/`-based `instrument_changed` and `scores_file_changed` values in the agent context still come from the restored tree, which is the existing RV-002 issue and not new.
* `git hash-object -- <path>`: by default it applies the path's attributes and autocrlf conversion, so CRLF checkouts hash the same as the blob. When a path is missing on both sides, both ids are `""` and the result is unchanged. When hashing fails, the result is "differs", which errs towards scoring.
* `-z` parsing: `R`/`C` entries consume three tokens and all others consume two. Similarity suffixes such as `R100` are handled through `[0]`. The trailing NUL stops the loop. `-C` is not passed, so `C` cannot occur. Status `T` falls into the else branch (see RG-001).
* Unchanged-PR skip path: fingerprints are built from `git ls-files`, sorted, so the set and order are deterministic. No new trigger was added to `should_score`. Fingerprint values may differ from the previous `Path.glob` implementation only for untracked files, which do not exist in CI. `main` holds the manual seed, so the first run is bootstrap regardless. No regression found.
* Fail closed: an unresolvable range with changed artifacts outside bootstrap or force raises `RuntimeError`, which becomes `EXIT_ERROR`. This also closes most of RV-007.
* `**/` semantics: `(?:.*/)?` matches zero or more directories, and `match` with `\Z` anchors both ends. The parametrised tests cover nested, sibling-prefix and single-level cases.
* Gate: `allowed = present | removed` only for decreases. `test_given_increase_citing_removed_file_when_evaluated_then_baseline_kept` covers the increase case.

## Findings

### RG-001 Medium: Replacing a scored file with a symlink, or otherwise making it unscorable, still hides evidence

* Location: `.github/rubric/scripts/prepare.py` `classify_changes` (else branch) and `compute_state` (`changed_files |= present & set(artifact["files"])`)
* Evidence: `match_files` drops symlinks and non-regular files. A commit that replaces `docs/brds/x.md` with a symlink appears as `T docs/brds/x.md`. `classify_changes` puts it in `changed`, but it is not in `artifact["files"]`, so the intersection drops it, and it is never added to `removed`. The fingerprint changes and the agent runs, but no move can cite the path, so scores carry forward. This is the same failure mode as RV-001 through a path the fix did not generalise.
* Fix: treat any in-scope diff path that is not in the artifact's current `files` as removed: `removed |= {p for p in changed if p not in files}`. This makes the separate `oversize` set redundant. Add a test.
* Routing: follow-up, Implement (small).

### RG-002 Low: Non-PR range is empty when the scores commit is the tip but the tree has moved

* Location: `prepare.py` `diff_args` (non-PR branch)
* Evidence: when `HEAD` itself writes `latest.json`, the range is `HEAD HEAD` and `entries == []`. This happens with a squash merge of a PR that was not up to date, or a direct push that edits `latest.json` together with artifacts. If fingerprints still differ, `changed_artifacts` is non-empty but `changed_files` is empty, so the agent runs and the gate reverts every move. A deletion in that commit is therefore invisible on `main`. Branch protection (require up to date) and trust in `main` pushers limit the impact.
* Fix: when a changed artifact has no in-scope diff entry, widen the base to `<commit>^1`, or fail closed with an explicit reason. Alternatively, anchor on the `commit` recorded in `latest.json` when it is an ancestor of `HEAD`.
* Routing: follow-up.

### RG-003 Low: The calibration run is not blind to the baseline

* Location: `prepare.py` `write_context` (`baseline.total`, `baseline.sections` kept in force mode); `.github/rubric/README.md` Day-to-Day Use ("without seeing the baseline"); workflow prompt ("baseline scores are withheld")
* Evidence: only per-criterion baseline scores are withheld. The total and the section totals stay in `context.json`, and the agent can `cat .github/rubric/scores/latest.json` or `git show` it. Anchoring remains possible, which weakens the variance measurement that RV-004 was meant to unblock.
* Fix: in force mode, set `baseline` to `{}` in the context. Either state in the README and prompt that the file is still readable, or remove `latest.json` from the agent workspace in a force-only pre-agent step and tell the agent not to read it.
* Routing: follow-up (README wording can be fixed now).

### RG-004 Low: Repeated force dispatches cancel each other

* Location: `.github/workflows/rubric-score.md` `concurrency` (lock L84-L86); README Day-to-Day Use
* Evidence: the workflow-level group is `rubric-score-workflow_dispatch-<ref>` with `cancel-in-progress: true`. `job-discriminator` does not appear in the workflow-level group in the lock. The README tells the owner to run force "two or three times". If those runs overlap, every run except the last is cancelled.
* Fix: tell the owner in the README to wait for each run to finish, or add `github.run_id` to the group when `event_name == 'workflow_dispatch'`.
* Routing: fix with the next README or workflow edit.

### RG-005 Low: README live-criteria statement omits the instrument-change exception

* Location: README What It Does ("They keep their baseline until one of those changes, except in bootstrap and calibration runs")
* Evidence: `instrument_changed` opens all 20 criteria. A PR that changes an instrument file together with a BRD can move B1 to B5 and C2 by citing the BRD. This is the residual of RV-003(e). The live set in `rubric.json` (B1 to B5, C2) matches the README.
* Fix: add the instrument-change exception to the README, or close live criteria unless a deck or pitch artifact is in `changed_artifacts` (RV-003 follow-up).
* Routing: README now, code with the RV-003 follow-up.

### RG-006 Low: README overstates issue creation on `main`

* Location: README Day-to-Day Use ("A regression or a scoring failure on `main` opens an issue")
* Evidence: the gate job runs only when the agent called `record_rubric_score`. `report-failure-as-issue: false` is set, and the conclusion pre-step is PR-only. An agent failure or timeout on `main` therefore opens no issue. Only invalid decisions produced by the gate do.
* Fix: reword to "a regression, or an invalid scorecard", or add a non-PR branch to the conclusion pre-step that opens an issue.
* Routing: README now.

### RG-007 Low: Prompt guidance for reading deleted files does not fit the PR range

* Location: workflow prompt Inputs step 3; `prepare.py` `write_context` (`diff_range`)
* Evidence: "`<base>` is the first commit in `diff_range`" does not fit a PR, where `diff_range` is the single token `origin/main...HEAD`. Running `git show origin/main...HEAD:path` fails, so the agent has to guess `origin/main`.
* Fix: emit `diff_base` (the merge-base SHA for PRs, the scores commit otherwise) in the context and reference it in the prompt.
* Routing: follow-up.

### RG-008 Low: Change-detection tests miss oversize, rename-out end to end and merge styles

* Location: `.github/rubric/scripts/test_prepare.py`
* Evidence: no test covers a file growing past `max_file_bytes` (FR-1, CC-004), a rename out of scope through `compute_state`, a type change (RG-001), or non-PR base resolution after a squash or merge commit. Validation ran against a minimal pytest stub rather than real pytest, so `parametrize` and fixture semantics were not independently confirmed.
* Fix: add temporary-repo tests for oversize (set `max_file_bytes` low in the copied registry), rename out, symlink replacement and a squash-style tip commit. Rerun with real pytest (`uv run --with pytest pytest .github/rubric/scripts`) when the host allows.
* Routing: follow-up (pairs with RG-001 and RG-002).

### RG-009 Low: Non-UTF-8 paths crash `prepare.py` with a traceback

* Location: `prepare.py` `tracked_files`, `parse_name_status`
* Evidence: `.decode("utf-8")` on raw `-z` output raises `UnicodeDecodeError`, which `main()` does not catch. The step still fails closed, but `rubric/score` gets no explanation (compounds RV-010b).
* Fix: decode with `errors="surrogateescape"`, or add `UnicodeDecodeError` to the handled exceptions.
* Routing: follow-up.

### RG-010 Low: Oversize file diffs can consume the whole context diff budget

* Location: `prepare.py` `write_context` (`git diff -M -D ... -- changed_files`, truncated at `MAX_DIFF_BYTES`)
* Evidence: hidden oversize files are in `changed_files`, so their full textual diff is included. A file over 2 MB can fill the 400 KB budget and silently truncate the diffs of the other changed files.
* Fix: exclude `removed_files` from the content diff and append `git diff --stat` for them, or put them last in the pathspec.
* Routing: follow-up.

## Parent finding status

| Parent | Status |
|--------|--------|
| RV-001 | Closed for deletion, rename out and oversize, on PR and push. Residual variant RG-001, edge case RG-002 |
| RV-003 | README part corrected. RG-005 residual. Code part remains a follow-up |
| RV-004 | Closed. RG-003 and RG-004 limit calibration quality |
| RV-012 | Docs part closed (credit cap, setup PR run, model pinned twice). RG-006 is a separate README inaccuracy |
| RV-007 | Largely closed by fail-closed range resolution (not a target) |

## Routing summary

| Finding | Severity | Routing |
|---------|----------|---------|
| RG-001 | Medium | Follow-up, Implement |
| RG-002 | Low | Follow-up |
| RG-003 | Low | Follow-up (README wording now) |
| RG-004 | Low | Next README or workflow edit |
| RG-005 | Low | README now, code with RV-003 |
| RG-006 | Low | README now |
| RG-007 | Low | Follow-up |
| RG-008 | Low | Follow-up with RG-001 and RG-002 |
| RG-009 | Low | Follow-up |
| RG-010 | Low | Follow-up |

## Pending live validation

* `job-discriminator` semantics in gh-aw v0.89.21 (RG-004).
* RV-002: setup PR behaviour after the `.github` restore. The README asserts a bootstrap run, which is still unconfirmed.
