<!-- markdownlint-disable-file -->

# Review: rubric-gate-symlink-tests

* Task ID: 2026-10-02-rubric-gate-symlink-tests (child of 2026-10-02-rubric-gate-change-detection)
* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-symlink-tests-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-gate-symlink-tests-changes.md
* Target findings: RG-001, RG-008 in .copilot-tracking/reviews/2026-10-02/rubric-gate-change-detection-review.md
* Scope: unstaged diff of `.github/rubric/scripts/prepare.py` and `test_prepare.py` against the staged previous version; `gate.py` `evaluate` read for consumer semantics
* Mode: one pass, read-only (no source edits)

## Outcome

Conformant with findings.

RG-001 is closed in code. FR-1 and AC-2 are met. RG-008 is closed for coverage, with one Low residual: the symlink case passes silently instead of skipping, it did not execute on this host, and no CI runs it.

## Verification

### RG-001 (classify_changes, compute_state)

`classify_changes` now gathers every touched path (both sides of `R`, `target or path` otherwise), filters by `in_scope`, and splits by membership in the artifact's current `files`. `compute_state` passes `artifact["files"]`, so `present` is already scorable and the old `& set(artifact["files"])` is correctly dropped.

| Case | Diff entry | Result | Correct |
|------|-----------|--------|---------|
| Symlink or type change | `T b.md` | b.md not in `files` (symlinks excluded by `match_files`), so removed | Yes (the RG-001 gap) |
| Delete | `D b.md` | removed | Yes |
| Rename out of scope | `R b.md archive/b.md` | source removed, target filtered by `in_scope` | Yes |
| Rename within scope | `R b.md c.md` | source removed, target changed | Yes |
| Oversize growth | `M b.md` | not in `files`, so removed (old `oversize` set no longer needed) | Yes |
| Modified, still scorable | `M a.md` | changed, not removed | Yes |
| Out-of-scope path | any | dropped by `in_scope` | Yes |
| Excluded path | any | dropped by `in_scope` exclude | Yes |

* Cross-artifact union: scorability depends only on `in_scope`, symlink status and the shared `max_file_bytes`, so a path cannot be scorable for one artifact and unscorable for another. `gate.evaluate` computes `present = changed - removed`, so the union stays consistent.
* Gate semantics are unchanged: removed paths still justify decreases only (`allowed = present | removed` only when the score drops).
* The `entries is None` fallback (bootstrap or force) is unchanged and records no removed files. That is acceptable because the gate skips the comparison in those modes.

### RG-008 (tests)

* Discrimination against the previous implementation:
  * `test_given_type_change_to_unscorable_when_classified_then_removed` fails against the old code: the old 4th parameter was `oversize`, `T` went to `changed`, and the method returned `({b.md}, set())`. This is the unit-level regression guard for RG-001.
  * The `hide_by_symlink` parameter fails against the old code on symlink-capable hosts only.
  * Rename within scope, `hide_by_deleting`, `hide_by_renaming_out`, `hide_by_growing` and both merge-style cases pass against the old code too. That is expected because they close the coverage gaps RG-008 listed (oversize, rename out end to end, merge-commit and squash base resolution) rather than detect RG-001.
* pytest validity: `parametrize` with a tuple of argnames and with function objects is valid. `tmp_path` before a parametrized argument is valid. The merge test's `--squash` path commits explicitly, and `--no-ff --no-edit` avoids an editor prompt.
* Fixture: `make_repo` lowers `max_file_bytes` to 1000 through the copied registry and computes the baseline fingerprint with the same limit, so `hide_by_growing` exercises the size path end to end.
* Count: 20 cases in `test_prepare.py` plus 16 in `test_gate.py` gives 36, which matches the changes log.

## Findings

### RS-001 Low: Symlink case passes silently instead of skipping, did not run here, and no CI runs it

* Location: `.github/rubric/scripts/test_prepare.py` `test_given_pr_hiding_scored_file_when_computed_then_path_is_removed` (`return  # symlinks unavailable on this host`); changes log Validation ("it runs on Linux CI")
* Evidence: a bare `return` is reported as a pass, not a skip. On this host, `Path.symlink_to` raises `WinError 1314` (checked during review), so the 36 reported passes include a symlink case that asserted nothing. No workflow under `.github/` runs pytest, so the "runs on Linux CI" claim has no support. The only executed check for RG-001 is the `T` unit test.
* Fix: replace the `return` with `pytest.skip("symlinks unavailable on this host")`. Correct the changes log statement. Run `uv run --with pytest pytest .github/rubric/scripts` once on Linux or WSL, or add a CI step that runs it.

### RS-002 Low: Validation still relies on a pytest stub

* Location: changes log Validation
* Evidence: the RG-008 residual remains. Real pytest has not run, so fixture injection, parametrize ids and skip reporting are confirmed only by inspection. The inspection found no invalid usage.
* Fix: same run as RS-001.

### RS-003 Info: Newly added unscorable in-scope paths are labelled removed

* Location: `prepare.py` `classify_changes`
* Evidence: an `A` entry for a new symlink or oversize file in scope lands in `removed_files` even though it was never scored. The gate admits removed paths only to justify decreases, so this does not create a way to raise scores. The docstring wording ("removed or unscorable") already covers it.
* Fix: none required. Optionally rename the state key to `unscorable_files` when RV-series wording is next revised.

### RS-004 Info: `match_files` oversize return value is now unused

* Location: `prepare.py` `match_files`; callers use `_oversize` and `_`
* Evidence: after the RG-001 generalisation, no caller consumes the second value. The warning log still has diagnostic value.
* Fix: optional cleanup. Return only `matched` and keep the warning.

## Routing

| ID | Severity | Routing |
|----|----------|---------|
| RS-001 | Low | Follow-up, Implement (one-line test fix and log correction), then a real pytest run |
| RS-002 | Low | Pairs with RS-001 |
| RS-003 | Info | No action |
| RS-004 | Info | Optional cleanup with the next `prepare.py` edit |

RG-001: closed. RG-008: closed for coverage, with the residual tracked as RS-001 and RS-002.
