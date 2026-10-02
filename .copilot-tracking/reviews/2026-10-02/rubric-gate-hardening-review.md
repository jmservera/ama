<!-- markdownlint-disable-file -->

# Review: rubric-gate-hardening

* Task: 2026-10-02-rubric-gate-hardening (child of 2026-10-02-rubric-gate-context-artifact)
* Changes record: .copilot-tracking/changes/2026-10-02/rubric-gate-hardening-changes.md
* Scope: `.github/rubric/scripts/gate.py`, `.github/rubric/scripts/prepare.py`, `test_gate.py`, `test_prepare.py`, `.github/workflows/rubric-score.md`, `.github/workflows/rubric-score.lock.yml`
* Mode: one pass, read-only, static. Reported validation (47 passed, 1 skipped under a pytest stub; compile 0 warnings) taken as given, not rerun. No GitHub run observed.

## Outcome

Conformant with findings. All seven targets are addressed; RG-002 and RG-009 are partially closed. No Medium or higher findings. The RG-010 change introduces one minor diff-quality regression for in-scope renames (RH-002).

## Target status

| Target | Status | Notes |
|--------|--------|-------|
| RV-005 | Closed | `clean_text` idempotent (ZWSP is not `\s`, guards use negative lookahead, truncation after insertion); `sanitize` escapes table and HTML; latest.json stores cleaned rationale and evidence; prompt marks baseline rationale and evidence untrusted. Residual autolink forms in RH-008. |
| RV-006 | Closed | Backslash, `GITHUB_WORKSPACE` prefix, leading `/`, `#L` and `:L` anchors, `normpath`; `.` maps to empty. Unknown absolute prefixes still fail safe (no match). |
| RV-009 | Closed (accepted divergence) | `persist-credentials: false` in `rubric_prepare` and `record_rubric_score` (lock L2003, L1833); token only in the `record` step env. Fail-closed on missing scripts not implemented, recorded as accepted. GHES note in RH-009. |
| RV-010 | Closed | (a) pre-step conditioned on `record_rubric_score.result == 'skipped'`; (b) `decide` failure sets `failure`; (c) distinct push-failure description; (d) sticky lookup filtered by `github-actions[bot]`; (e) skip path dismisses only bot `CHANGES_REQUESTED` reviews. Adjacent gaps in RH-004 to RH-007. |
| RG-002 | Partially closed | Tip-writes-scores range now uses `commit^1`; the tip's own edits and deletions are visible. Main-side commits missing from a not-up-to-date squash remain invisible (RH-003). |
| RG-009 | Partially closed | Decoding uses `surrogateescape` and `UnicodeDecodeError` is handled, but an in-scope non-UTF-8 path now fails in `fingerprint_files` with an uncaught `UnicodeEncodeError` (RH-001). |
| RG-010 | Closed with regression | Removed paths are stat-only and listed first; budget no longer consumed by oversize files. In-scope renames now render as full additions (RH-002). |

## Regression checks requested

* `clean_text` and evidence matching: no regression. `evaluate` matches `evidence_path(ref)` on the raw proposed evidence; `clean_text` is applied only when building latest.json. Stored evidence gains ZWSP only for paths containing `@`, `#<digit>`, `](`, `![` or `://`, which is informational (RH-011).
* RG-002 and normal post-merge pushes: no regression. Up-to-date squash merges match fingerprints, so `should_score` stays false and the range is unused. Merge commits are TREESAME to the PR parent for `latest.json`, so `git log -1 -- latest.json` returns the PR's gate commit, not `HEAD`, and the old range applies. The bot's own commits do not occur on `main` (record step is PR-only). `rubric_prepare` uses `fetch-depth: 0`, so `commit^1` resolves; a shallow clone would silently fall back to the empty `HEAD HEAD` range.
* `dismissReview` and other users: safe. The filter requires `review.user.login === 'github-actions[bot]'` and `state === 'CHANGES_REQUESTED'`. Unhandled API errors are RH-007.
* Push URL with token: `github.token` is auto-masked and not persisted to `.git/config`. Host is hard-coded to `github.com` (RH-009). `GITHUB_REPOSITORY` is `owner/repo` on GHES as well, so only the host is wrong.
* Conclusion pre-step needs: confirmed. Lock L1185-L1191 lists `rubric_prepare` and `record_rubric_score` in `conclusion.needs`, so both expressions resolve. The conclusion job itself is skipped when `agent` is skipped (unless a credit or activation guard fired), see RH-005.
* `if: always()` on Report initial status after checkout failure: `steps.decide.outcome` is `skipped`, so `failure` is posted with "Could not compute what changed". This fails closed and `github-script` does not need the checkout. The cancellation case is RH-004.

## Findings

### RH-001 Low: In-scope non-UTF-8 path still crashes with a traceback

* Location: `prepare.py` `fingerprint_files` (`relative.encode("utf-8")`); exception lists in `prepare.main` and `gate.main`
* Evidence: `tracked_files` now yields surrogate-escaped strings. `"\udcff".encode("utf-8")` raises `UnicodeEncodeError`, which neither `main` catches. The step still fails closed (status `failure` via Report initial status; gate falls back to the default FAILED report), but RG-009's "no traceback" goal is only met for out-of-scope paths. Filesystem and subprocess calls are fine because POSIX `fsencode` uses `surrogateescape`.
* Fix: `relative.encode("utf-8", "surrogateescape")` in `fingerprint_files`; catch `UnicodeError` rather than `UnicodeDecodeError` in both mains; add a Linux-only test with a Latin-1 filename.

### RH-002 Low: RG-010 change turns in-scope renames into full-file additions

* Location: `prepare.py` `write_context` (`present = changed_files - removed_files`; content diff pathspec `-- *present`)
* Evidence: for `docs/brds/a.md -> docs/brds/b.md`, `classify_changes` puts `a.md` in `removed` and `b.md` in `changed`. The content diff now limits the pathspec to `b.md`, so `-M` cannot pair it and the whole file is emitted as an addition, while `a.md` appears in the stat as deleted. Before the change both paths were in the pathspec and only the hunks were shown. This consumes the same budget RG-010 set out to protect.
* Fix: keep only removed paths that still exist in the working tree (oversize, symlink, non-regular) stat-only; pass removed paths that no longer exist (deletions, rename sources) to the content diff, where `-D` already suppresses deleted content and `-M` pairs renames. Add a rename-within-scope context test.

### RH-003 Low: Not-up-to-date squash still hides main-side changes (RG-002 residual)

* Location: `prepare.py` `diff_args` (non-PR branch)
* Evidence: after a squash merge `Q` of a PR that was behind `main`, `latest.json` holds the PR-tree fingerprints. The mismatch comes from main-side commits the PR lacked, but `Q^1..Q` shows only the PR's own changes. Artifacts changed only on the main side get no in-scope entries, so their criteria cannot move and their deletions stay invisible. The new range also reopens the PR's already-scored edits for rescoring on `main` (minor, more permissive). The added test covers a direct push, not this case.
* Fix: when a changed artifact has no in-scope entry in the range on a non-PR event, add an explicit reason and either fail closed or score with all of that artifact's files as changed; document "require branches to be up to date" as a precondition in the README.

### RH-004 Low: Report initial status runs on cancellation

* Location: `rubric-score.md` `rubric_prepare` Report initial status (`if: always() && ...`)
* Evidence: concurrency uses `cancel-in-progress: true`. A cancelled run still executes `always()` steps; `decide.outcome` is `cancelled` or `skipped`, so the step posts `failure` "Could not compute what changed". For same-SHA retriggers (`reopened`, `ready_for_review`) this can land on the current head and, on the skip path, override the new run's `success` until the next push.
* Fix: use `!cancelled() && github.event_name == 'pull_request'`, or return early when `DECIDE_OUTCOME === 'cancelled'`.

### RH-005 Low: Context or upload failure leaves `rubric/score` pending with no explanation

* Location: `rubric-score.md` `rubric_prepare` Prepare rubric context, Upload rubric context, Report initial status; lock `conclusion.if` L1192
* Evidence: when `decide` succeeds with `should_score=true` but context preparation or upload fails, Report initial status posts `pending`. `agent` is skipped because its need failed, so `conclusion` is skipped too (its condition requires `agent` not skipped), and the pre-step comment never fires. The PR stays blocked on a pending check with no comment.
* Fix: give the context and upload steps ids, pass their outcomes, and post `failure` with "Could not prepare scoring context" when either failed.

### RH-006 Low: A non-push failure in the record step can publish success

* Location: `rubric-score.md` Record score on the pull request branch; Publish verdict
* Evidence: under `bash -e`, a failing `cp`, `git commit` or `jq` ends the step without `push_failed` or `new_sha`. Publish verdict then treats the run as not blocked and can post `success` and APPROVE on `SCORED_SHA` while the branch lacks the new `latest.json`. Adjacent to RV-010(c); likely pre-existing.
* Fix: pass `RECORD_OUTCOME: ${{ steps.record.outcome }}` and treat `failure` as blocked with the push-failure description.

### RH-007 Low: Review dismissal errors fail the prepare job

* Location: `rubric-score.md` Report initial status, `dismissReview` loop
* Evidence: dismissal can return 403 or 422 when branch protection restricts who can dismiss reviews. The call is not wrapped, so `rubric_prepare` fails and the run shows red on a skip path that already posted `success`, and the stale review stays.
* Fix: wrap each `dismissReview` in `try`/`catch` and emit `core.warning`.

### RH-008 Low: `clean_text` leaves some GitHub autolinks

* Location: `gate.py` `clean_text`
* Evidence: GFM extended autolinks for `www.example.com`, and GitHub references such as `GH-123` and commit SHAs, still render in the sticky comment and in issues opened on `main`. Scheme URLs, Markdown links and images, mentions and `#123` are neutralised.
* Fix: insert ZWSP after `www` before `.` (`re.sub(r"(?i)\bwww\.", f"www{ZWSP}.", ...)`) and accept SHA and `GH-` references as low risk, or render rationale inside escaped code spans.

### RH-009 Info: Push URL hard-codes `github.com`

* Location: `rubric-score.md` Record step (`https://x-access-token:${PUSH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git`); lock L1895
* Evidence: the token is masked and not persisted. On GHES the push targets the wrong host and is reported as a push failure. The lock already derives `GH_HOST` from `GITHUB_SERVER_URL` elsewhere. The token also appears in the `git push` argv and is inherited by git hooks; acceptable on an ephemeral runner, but in the bootstrap path PR-head `gate.py` runs earlier in the same job and could plant a `.git/hooks/pre-push`.
* Fix: build the host from `${GITHUB_SERVER_URL#https://}`, or pass the token through `git -c http.extraheader="AUTHORIZATION: basic ..."` with `-c core.hooksPath=/dev/null`.

### RH-010 Info: Test and runtime evidence gaps

* Location: `test_prepare.py`, `test_gate.py`; workflow
* Evidence: no tests for RG-009 (non-UTF-8 path), the PPTX uncompressed bound, or in-scope rename diff output. Validation used a pytest stub, not real pytest (RG-008 carry-over). The workflow changes (dismissal, conclusion pre-step, token push) are unverified until a GitHub run.
* Fix: add the tests named in RH-001 and RH-002; run `uv run --with pytest pytest .github/rubric/scripts` when the host allows; check the first PR run for the status, comment and review lifecycle.

### RH-011 Info: Stored baseline text narrowed

* Location: `gate.py` `build_scores_file`
* Evidence: stored rationale is now capped at 300 characters (was 1000) and `change_reason` is not stored. Evidence paths can carry ZWSP for rare characters. This does not affect gate matching. `rubric_prepare` gains `pull-requests: write`, but the token is neither persisted nor exposed to the Python steps.
* Fix: none required; note the 300-character cap in the README if baseline rationale length matters.

## Routing

* RH-001, RH-002, RH-005, RH-006: follow-up, Implement (small, same files).
* RH-003: follow-up, Plan (choose fail-closed or open-artifact behaviour) plus README precondition.
* RH-004, RH-007: fix with the next workflow edit.
* RH-008 to RH-011: optional or informational.
