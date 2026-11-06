<!-- markdownlint-disable-file -->
# Changes: bounded evidence corrections (issue 1204)

* Source file unchanged: blob acefb44a4d254ede6d86413343127b763dec42cb. No frontmatter, tools, application or infrastructure edit.
* Added: research update, plan, details; sandbox 003 (run-state, design, test-log, run-index, test-review, model-id sidecar for run 002, mutant replay mapping, storage-proof-receipt, three manifests and two copy bundles raw-selected-68.tar.gz and raw-runs-002-003-preservation.tar.gz); behavior report 005; review; state. Private archive directory under ~/.local/share/ama/tracking-archives/ (outside the checkout).
* Commands: 25 native `copilot --model auto` children under strace (all exit 0); replay diffs; names-only hygiene scans; snapshot.py (inventory, archive, readback, restore, hash compare).
* Divergences: in-script tracked-blob check had a column bug (corrected by a separate check, both recorded); one wording fix in run-state.md after the run by a shell stream edit; M1 diff qualification recorded; designer returned 25 scenarios (over the 18 to 24 request) and flagged threshold-number leaks which the lead neutralised before use.
* Not done by design: no replacement, removal, move, pruning or normalization of any old member; no .gitattributes change; range `git diff --check origin/main..HEAD` remains OPEN; 97-unit repeat deferred until the final storage candidate; no controls repeat.
* Preserved: reports 003 and 004, sandboxes 001 and 002, grade-role deviation, cbebe refs, /tmp/h1204.
