# Details

* Phase 1: git cherry-pick -x both SHAs in order; stop on conflict.
* Phase 2: find the inventory generator in tools/; regenerate only if the audit test reports drift. Tests run from a /tmp venv installed with pip (removed before commit).
* Phase 3: resolve relative Markdown links in added lines; scan added lines for secret patterns, expect 0 hits.
* Phase 4: repo-local noreply email, Co-authored-by trailer, git status empty, git diff --check clean.
* Critique corrections: baseline BASE=34b11967b; run the actual inventory checker (not just unit tests); commit the 1531 tracking files in a final commit.
