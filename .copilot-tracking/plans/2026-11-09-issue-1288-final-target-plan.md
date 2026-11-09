<!-- markdownlint-disable-file -->
# Plan, research and details: #1288 final-target integration

Parent: issue-1288-main-integration (HEAD 2aa038043). Written and committed BEFORE the merge. Refs #1288 only.

## Research (executed, read-only)

* Fetched origin/main a04668ae94b5c2f38e6c55ed789db245e8c71d16. Commits beyond the previously integrated cd687abad: 3d23e8907 (#1329 docs checkpoint) and a04668ae9 (bot rubric score 78/100).
* `git diff cd687abad origin/main` outside additive tracking files: .github/rubric/scores/latest.json, docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md. No path under src, infra, tools or any pyproject.
* `git merge-tree --write-tree HEAD origin/main` is conflict free (tree 51bc2e2ec). Detection only.
* latest.json is trusted rubric score metadata, not an executable workflow or config input; it must not be edited.

## Plan

1. Commit this record. 2. Ordinary no-ff merge of origin/main; no rebase, force or code change. 3. Prove src, infra, tools, pyproject and workflow inputs are identical to 2aa038043 (git diff empty) and the all-path manifest equals main's delta. 4. No test reruns are warranted because executable inputs are byte-identical; the main-integration raw logs at 2aa038043 are reused and labelled historical-at-that-tree, not fresh. 5. Record changes and review, update a separate handoff.

Counters: E1-E7 spent, E8-E10 remain; unchanged-source integration consumes nothing. Real-provider route stays disabled; SQL remains historical.
