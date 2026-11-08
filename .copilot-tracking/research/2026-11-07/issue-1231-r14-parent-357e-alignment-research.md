# Research: issue 1231 R14 alignment onto frozen parent 357e842d

Date: 2026-11-07. Disposition: executed (git evidence). Planning readiness: Ready.

## Evidence

* Child HEAD fd6a5cf9ccd3f35d10b5a042db19d0c0bd96acc2, clean ignored-inclusive. Preserved ref backup/issue-1231-fd6a-pre-r14-align.
* Parent gate satisfied: tmux rpi-79 absent, its log reports a completed clean outcome (exit 0), parent worktree ignored-inclusive status empty, HEAD 357e842d064296d4764f087f7a39006cc702f4ee (tree 1d3f6ef1), rebased on main 0f420dc9514db22081cb48fa733267d9d33a0d24, which is its ancestor. Origin/main fetched at 09:57 is 0f420dc9.
* Parent's own rebase left the old snapshot 11fb73f45 as the common ranking base. `git diff 11fb73f45 357e842d` in src is only main's #891 chat and browser-check changes plus the rubric score.
* The earlier child rebase onto an older parent conflicted in intermediate ranking commits. `git merge-tree --write-tree --merge-base=11fb73f45 HEAD 357e842d` is clean (tree df407596 before this record commit) and changes the child in src only by the 5 #891 files.

## Approach

Two-parent merge (HEAD, 357e842d) using that clean tree. No manual source resolution; #1231 fixes and #891 changes both kept.

## Limits

Old receipts (g1231 r4, r7 failed, r9, r11, r13; g79 r14, r16, r17) do not cover the new head. FULL gate admitted only under the coordinator conditions. Author review is not independent.
