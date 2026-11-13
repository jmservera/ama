# Details: 440-wave23-parent-integration-1222

## Phase 1 merge

`git merge --no-ff -m "<msg with trailer>" <14 shas>` from HEAD `74a93a137a`. Fall back to sequential merges if octopus refuses. Expected: no conflicts (0 overlapping paths of 112).

## Phase 2 verification

* `git diff --name-only 74a93a137a HEAD | grep -v '^.copilot-tracking/' | wc -l` is 0 after merge, before docs edits.
* Before merging, save per-child path lists from `git diff --name-only 74a93a137a <child>` (post-merge `HEAD...<child>` is empty). After merging, `git rev-parse HEAD:<path>` must equal `git rev-parse <child>:<path>` for every path; fail on any missing path; count 112.
* Final scope check: the staged diff against `74a93a137a` is allowlisted to the 112 child paths, the parent tracking records, and exactly `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md` and `docs/reference/log.md`; pack and log diffs show zero deleted lines (`git diff --numstat`).
* Each table row and limit is checked against the child changes and review records before commit; skips and exclusions are copied from them, not from the brief alone.
* `git diff --stat 74a93a137a HEAD -- src infra tools .github` empty.

## Phase 3 docs

* Section `## Waves 1105 and 1143 Multi-Package Local Demo Verification (2026-11-13, Refs #440)` appended to `docs/architecture/cutover-evidence-pack.md`: one table of 14 rows (child commit, issues, outcome, class, qualification, records), a limits list, no acceptance language.
* One index row in `docs/reference/README.md` after the Post-1507 row.
* One log entry appended to `docs/reference/log.md`.

## Phase 4 checks

Link and anchor resolution script over the three edited files and new section; non-ASCII scan of added lines; `git diff --check`.
