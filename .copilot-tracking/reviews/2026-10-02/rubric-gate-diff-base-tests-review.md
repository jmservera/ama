<!-- markdownlint-disable-file -->

# Review: rubric-gate-diff-base-tests

* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-diff-base-tests-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-gate-diff-base-tests-changes.md
* Targets: RC-001, RC-002 in .copilot-tracking/reviews/2026-10-02/rubric-gate-calibration-context-review.md
* Scope: `.github/rubric/scripts/test_prepare.py` (`make_repo`, lines 244-279), `.github/rubric/scripts/prepare.py` (`diff_args`, `write_context` `diff_base`)
* Mode: one pass, read only, static analysis (no test run in this review)

## Outcome

Conformant with findings. RC-001 is closed. RC-002 is partially closed: the push test guards against `HEAD` but not against `HEAD^`, because the last commit that wrote `latest.json` is exactly `HEAD^` in the fixture.

## Target Disposition

| ID | Disposition | Evidence |
|---|---|---|
| RC-001 | Closed | PR test (line 244) records `expected` as the pre-branch `main` SHA, commits on `feature`, then advances `main` with `docs/other.md` before returning to `feature`. `merge-base main HEAD` returns `expected`; `main` tip is a different SHA, so a `rev-parse <base_ref>` implementation fails the assertion. A `HEAD` implementation also fails. |
| RC-002 | Partially closed, see RT-001 | Push test (line 265) asserts `diff_base` equals the baseline commit. Against `HEAD`: `diff_base` mismatches and `git diff HEAD HEAD` is empty so `removed_files` is `[]`; fails. Against `HEAD^`: `HEAD^` is the baseline commit and `diff HEAD^ HEAD` contains the deletion; passes. |

## Mutation Check

| Wrong implementation | PR test | Push test |
|---|---|---|
| `diff_base` = base ref tip (`main`) | Fails (tip moved) | n/a |
| `diff_base` = `HEAD` | Fails | Fails (SHA and empty `removed_files`) |
| `diff_base` = `HEAD^` / `diff_args` = `HEAD^ HEAD` | Passes (one feature commit, so `HEAD^` equals the merge base; see note) | Passes (not detected) |
| `diff_base` = literal `diff_args[0]` for PR (`main...HEAD`) | Fails | n/a |

Note on PR row 3: with one feature commit, `HEAD^` on `feature` equals the merge base, so a PR implementation hard-coded to `HEAD^` would also pass. This is outside the requested mutation set and lower risk because the PR branch explicitly calls `merge-base`; folded into RT-001's fix as optional.

## Findings

### RT-001 Medium: Push test cannot distinguish the last scores commit from `HEAD^`

* Location: `.github/rubric/scripts/test_prepare.py` `test_given_direct_push_when_context_written_then_diff_base_is_last_scores_commit` (line 265)
* Evidence: `make_repo` ends with the `baseline` commit that writes `latest.json`; the test adds exactly one commit. So `git log -1 -- latest.json` and `HEAD^` are the same SHA, and both `diff_base` and `removed_files` assertions hold for a `HEAD^` regression. This is the multi-commit direct-push and squash-after-several-pushes case `diff_args` exists to cover.
* Fix: after `git commit -m "delete on main"`, add a second unrelated commit on `main` (for example write `docs/other.md`, `git add .`, `git commit -m "later push"`). Keep `expected` as the baseline SHA. Then `HEAD^` is the delete commit, `diff HEAD^ HEAD` misses the deletion, and both assertions fail for the regression. Optionally add a second `feature` commit in the PR test so `HEAD^` there is not the merge base either.

### RT-002 Info: Output directory sits inside the repo working tree

* Location: lines 259 and 274 (also pre-existing line 238); `make_repo(tmp_path)` uses `tmp_path` as the repo root and `write_context` writes to `tmp_path / "out"`.
* Evidence: Not flaky as written. `compute_state` runs before `out/` exists, `match_files` uses `git ls-files` (tracked only), and the diff and `merge-base` calls operate on commits, so the untracked `out/` cannot change any asserted value. It would matter only if a later `git add .` or a working-tree scan ran after `write_context`.
* Fix: optional. Use `make_repo(tmp_path / "repo")` with `out` at `tmp_path / "out"` to keep the fixture hermetic.

### RT-003 Info: Windows line endings do not affect these assertions

* Location: `make_repo` and the PR test `write_text` calls.
* Evidence: `Path.write_text` translates `\n` to `\r\n` on Windows and Git may warn under `core.autocrlf`, but warnings go to captured stderr and do not change the exit code. Fingerprints in `make_repo` and `compute_state` are both taken from the same working-tree bytes, `differs_from_base` compares object ids, and the asserted values are commit SHAs and paths. `rev-parse` output is `.strip()`ped. No line-ending risk.
* Fix: none.

### RT-004 Info: Host Git configuration can break `make_repo`

* Location: `make_repo` (line 27), pre-existing.
* Evidence: Commits inherit global config. A developer with `commit.gpgsign=true` or a commit hook in `core.hooksPath` would see `CalledProcessError`. `git init -b` needs Git 2.28 or later. Not introduced by this change.
* Fix: optional. Add `git config commit.gpgsign false` in `make_repo`, or pass `-c commit.gpgsign=false` in the `git` helper.

## Validity

* Both tests are valid pytest: `tmp_path` fixture, plain `assert` on tuples, no stub-only constructs, and they follow the existing Arrange/Act/Assert layout.
* The inline `subprocess.run([... "rev-parse", "HEAD"] ...)` duplicates across the two tests because the module `git` helper returns `None`. Acceptable; not raised as a finding.
* Reported 38 passed, 1 skipped (symlink) under a minimal stub. A real pytest run (RS-002) remains pending and is still required before closing.

## Routing

| ID | Severity | Route |
|---|---|---|
| RT-001 | Medium | Follow-up, Implement (one extra commit in push test; optional in PR test) |
| RT-002 | Info | Optional cleanup |
| RT-003 | Info | None |
| RT-004 | Info | Optional hardening |
| RS-002 | Carried | Real pytest run |
