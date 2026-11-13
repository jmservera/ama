<!-- markdownlint-disable-file -->
# Integration details

## Phase 1

* `git cherry-pick -x eb1e5e7d6 86ca9878f`; abort and record a blocker on any conflict.
* Success: file sets disjoint, no conflict markers.

## Phase 2

* `git diff --check 1db0c4462..HEAD` returns 0.
* Resolve every relative Markdown link in added files; grep for token, key, password, connection-string patterns.

## Phase 3

* Changes artifact lists commits, checks and results.
* One review, findings recorded; clean tree, trailer present, no `/tmp/venv-*`.

## Critique corrections

* Preflight: HEAD is `1db0c4462`, no `.git/CHERRY_PICK_HEAD`, only this task's artifacts untracked.
* Rerun diff, link and secret checks over the final complete diff including the changes artifact.
* Blocking review findings are fixed and rechecked before commit.
