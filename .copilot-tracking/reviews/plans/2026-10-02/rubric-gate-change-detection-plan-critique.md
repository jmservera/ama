<!-- markdownlint-disable-file -->

# Plan Critique: rubric-gate-change-detection

* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-change-detection-plan.md
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-score-gate-review.md (RV-001, RV-003, RV-004, RV-012)
* Code read: .github/rubric/scripts/prepare.py, gate.py, test_gate.py; .github/rubric/artifacts.json; .github/workflows/rubric-score.md; .github/rubric/README.md
* Mode: one pass, read-only

## Verdict

**Pass with changes.** The direction is right and the scope is proportionate, but FR-1 as written does not close RV-001 for push events, can be undone by the existing `changed_files &= artifact_files` line, and does not say how excludes and oversize files interact with the diff. Force mode cannot change the baseline today, but the plan should make that explicit and fix a concurrency side effect. The acceptance tests exercise `evaluate()` and parsing, not the `compute_state()` path the bug lives in. All findings can be applied by the planner directly.

## Findings

### CC-001 High: Push events have no defined diff base, so RV-001 stays open on `main`

* Evidence: on `push` and `workflow_dispatch`, `BASE_REF` is `HEAD` (rubric-score.md L46, L57, L105) and `branch_changes` is `None` (prepare.py L163). FR-1 says "baseline commit to HEAD when resolvable" without defining the commit or the fallback. `latest.json.commit` is the PR head SHA before the bot's score commit; after a squash merge, and once the branch is deleted, that SHA is not on any fetched ref, so it is usually unresolvable. A direct push to `main` that deletes a BRD then reverts every drop and opens no regression issue.
* Fix: resolve the base for non-PR events as `git log -1 --format=%H {base_ref} -- .github/rubric/scores/latest.json` (the commit on the trusted ref that last wrote the baseline; works for merge, squash and rebase merges because the baseline tree equals that commit's tree under the up-to-date branch rule). Diff that commit to `HEAD` with `--name-status -M`. When no such commit exists and the baseline is not bootstrap, fail closed with `EXIT_ERROR` and a logged reason instead of silently omitting removals. Record in the plan that PR events keep `base...HEAD`, which is merge-strategy independent.
* Planner can apply directly: yes.

### CC-002 Medium: Removed paths are dropped by the existing artifact-file intersection

* Evidence: prepare.py L165 `changed_files &= artifact_files` keeps only paths present in the head tree. FR-1 adds removed paths "to that artifact's changed files" but does not say they survive this line. An implementation that unions before L165 reproduces RV-001.
* Fix: compute `removed_files` separately and union it after the intersection: `changed_files = (changed_files & artifact_files) | removed_files`. Also add the owning artifact id to `changed_artifacts` when only removals occur (the fingerprint already changes, but state it so the open-criteria set is correct when an artifact loses every file and `fingerprint` becomes `None`).
* Planner can apply directly: yes.

### CC-003 Medium: Exclude globs and matcher parity are unspecified

* Evidence: FR-1 matches diff paths against include globs only. `match_files` uses `Path.glob` for includes (`*` does not cross `/`) and `fnmatch` for excludes (`*` crosses `/`). FR-2 defines only `**/`. If the diff matcher is looser than `Path.glob` (for example `docs/capstone/deck/*.pptx` matching `deck/old/x.pptx`), paths never scored become "removed"; if excludes are skipped, a move into an excluded folder is handled inconsistently.
* Fix: one `glob_match(path, include, exclude)` used for both diff paths and the head tree filter: segment-wise `*` and `?` not crossing `/`, `**` as zero or more segments, exclude applied with the same rules the tree uses today. Classify each `--name-status` row as: `D` old path counts if it matched (include and not exclude); `R` old path counts if it matched, new path follows the normal tree rule (so in-scope to excluded or out-of-scope moves count as removal; in-scope to in-scope counts both; out-of-scope to in-scope is an addition only); `M`/`A` unchanged. Add a parity test asserting `glob_match` agrees with `Path.glob` for every active and planned pattern in artifacts.json over a fixture tree.
* Planner can apply directly: yes.

### CC-004 Medium: Oversize handling can flag files that never changed

* Evidence: FR-1 adds "oversize skipped files" to changed and removed without a diff condition. A file already over `max_file_bytes` on `main` is skipped on both sides; counting it as removed on every PR lets any open criterion move by citing it.
* Fix: count an oversize path only when it is also in the diff path set (PR or CC-001 base) or was under the limit at the base commit (`git cat-file -s {base}:{path}`). Log it as `oversize` in context so the agent can explain the drop.
* Planner can apply directly: yes.

### CC-005 Medium: Tests do not exercise the defect path

* Evidence: AC-1 calls `evaluate()` with a removed path in `changed`, which already passes today because `evaluate()` accepts any listed path. AC-2 covers parsing and `**/` only. RV-001 lives in `compute_state()`.
* Fix: add `test_prepare.py` cases on a temporary git repository (fixture with `main` holding a workflow-sourced `latest.json` and a feature branch): delete in scope; rename in scope to in scope; rename in scope to out of scope; move into an excluded path; all files of an artifact deleted; oversize growth versus already oversize; non-ASCII path; push event resolving the base via the last `latest.json` commit (CC-001), including after a squash-style single commit; push with no resolvable base fails closed. Assert `changed_files`, `removed_files`, `changed_artifacts` and `open_criteria`. Add one end-to-end gate test feeding `compute_state()` output into `evaluate()` for a deletion that must fail the gate. Add force tests (CC-006). Keep pytest, matching test_gate.py, and note the RV-011 divergence.
* Planner can apply directly: yes.

### CC-006 Medium: Force mode must be explicitly non-writing and must not cancel main runs

* Evidence: today a dispatch run cannot write the baseline because the record step is `pull_request` only (rubric-score.md L176) and statuses need `PR_NUMBER`. The plan relies on that implicitly. The concurrency group `github.event.pull_request.number || github.ref` with `cancel-in-progress: true` means a forced dispatch on `main` cancels an in-flight push run on `main` (or is cancelled by one), losing a regression issue.
* Fix: in `gate.py --force`, never write `latest.json` (write `calibration.json` or only the report), set `calibration: true` and `passed: null` in decision.json, and have the Publish step return after the job summary when `calibration` is true. Read `force` only when `github.event_name == 'workflow_dispatch'`, pass it through an `env:` variable, not inline `${{ }}` in the script body. Change the concurrency group to `rubric-score-${{ github.event.pull_request.number || format('{0}-{1}', github.event_name, github.ref) }}`. Add tests: forced `decide` on an unchanged tree sets `should_score`; forced gate produces no `latest.json` and no pass or fail.
* Planner can apply directly: yes.

### CC-007 Low: Force plumbing and agent context are underspecified

* Evidence: `prepare.py` runs in three places (rubric_prepare decide, pre-agent context, gate via `compute_state`). FR-4 names prepare and gate but not each call site. "Score from scratch" is undermined when context.json still carries baseline scores and rationale, and the prompt's live-criteria rule says keep the baseline.
* Fix: list all three call sites in P02-T01. In force mode set `bootstrap`-like `force: true` in context, omit baseline criteria and rationale, and add one prompt line: in a calibration run, score every criterion from evidence, including live criteria as readiness, without reference to a baseline.
* Planner can apply directly: yes.

### CC-008 Low: Git path quoting will break matching for non-ASCII or special paths

* Evidence: `git diff --name-status` quotes paths with octal escapes under the default `core.quotepath`.
* Fix: use `git diff --name-status -M -z` and split on `\0` (rename rows carry two paths). Covered by the non-ASCII test in CC-005.
* Planner can apply directly: yes.

### CC-009 Low: Deletions can exhaust the 400 KB diff budget

* Evidence: FR-3 puts removed paths in `changes.diff`; a deleted large BRD emits its full preimage and truncates later hunks at `MAX_DIFF_BYTES`.
* Fix: generate the diff with `-M -D` (`--irreversible-delete`) so deletions show as headers only, and tell the agent to read removed content with `git show {base}:{path}`, which its bash allowlist already permits.
* Planner can apply directly: yes.

### CC-010 Low: Removed paths can justify score increases

* Evidence: the evidence rule accepts any cited changed path for any direction of change. A removed file cannot evidence an improvement.
* Fix: in `evaluate()`, accept an increase only if at least one cited path is in `changed_files - removed_files`; removed paths justify decreases only. Pass `removed_files` into `evaluate()` and add a test.
* Planner can apply directly: yes (small, aligned with G1).

### CC-011 Low: README acceptance criterion omits the new behaviour

* Evidence: AC-4 lists RV-003 and RV-012 corrections but not force mode, main-only issues or removal handling. README Day-to-Day still says any push regression "opens an issue".
* Fix: extend AC-4: document the `force` input (calibration, report only, no baseline write, no issues), issues only for non-forced runs on `refs/heads/main`, and that deleting, moving out of scope or oversizing a scored file counts as a change that can lower the score. Also state that the fix takes effect for pull requests only after it merges, because the gate loads scripts from `main`.
* Planner can apply directly: yes.

## Coverage of the Requested Questions

| Question | Covered by plan | Gap |
|----------|-----------------|-----|
| Renames within scope, source versus destination | Partly (source added) | CC-003 classification |
| Exclude globs | No | CC-003 |
| Artifact entirely removed | Implicit | CC-002 |
| Push without resolvable base, squash merges | No | CC-001 |
| Force mode changing the baseline | Implicitly safe | CC-006 make explicit, concurrency |
| Test adequacy | Weak | CC-005 |

## Dependencies and Notes

* RV-002 remains open: if the agent workspace `.github/` differs from the PR head, `removed_files` in the agent context may disagree with the gate. The gate recomputes state, so pass or fail stays correct; only agent awareness is at risk.
* Severity counts: High 1, Medium 5, Low 5.
