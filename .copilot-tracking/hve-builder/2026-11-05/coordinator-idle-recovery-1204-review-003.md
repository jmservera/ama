<!-- markdownlint-disable-file -->
# Closure review 003: coordinator idle recovery (issue 1204)

Scope: `git diff HEAD -- .github/agents/ama-backlog-delivery-coordinator.agent.md` (14 insertions, 9 deletions, three hunks). Static review only.

## Verdict

Pass. No open High, Medium or Low finding.

## Closure evidence

* C1 closed (lines 333-337). The "merge at once" exception is gone. An append-only docs rebase now creates a new head that needs step 7/8 final exact-head selected-tier evidence, independent exact-head assessment and hosted checks before merge. This agrees with step 8 (lines 715-729: a rebase invalidates validation evidence and independent assessment; rebase only for a named reason) and with the "Never rebase a PR just to refresh a green head" bullet at line 331.
* C2 closed (lines 632-635). Step 5 now sends the PR back for a frozen local correction; the coordinator alone verifies, assesses and publishes; workers never push. This agrees with the worker-publication prohibition (lines 559-562) and step 6 (lines 647-648).
* C3 closed (lines 106-111). Open PRs at 16 to 20 admit no new issues. Above 20, no new issues and drain to 10 to 15 by repairing, reviewing and merging one at a time (rebase only under step 8). Existing-PR repair, correction and review continuations remain permitted at every count within the eight-total-live-session cap. This is consistent with the single-source admission rule (eight total live sessions, PRs and sessions counted separately, lines 96-105) and with the review-launch `ready` rule at line 122.

## Checks

* Whole-file grep for `merge at once`, `push the artifacts`, `launch nothing`, `previous head`, `green head`, `workers push` found no remaining stale exception or contradiction. The only push-related hits are the coordinator-owned publication statements and the `--force-with-lease` use in step 8, which is coordinator-owned.
* Frontmatter lines 1-5 are identical to HEAD.
* The file has no non-ASCII characters.
* The diff has no unrelated edits.

## Observations (not defects)

* Line 634 and the paragraph at lines 108-111 are wrapped unevenly (one long line). This is cosmetic only.
* The `/tmp` log paths in the tmux command at line 532 are pre-existing and outside this diff.

## Closure of M1/M2

Verdict: Pass. M1 and M2 are closed; no new contradiction found.

* M1 closed (line 668): the step 7 merge gate now requires a latest review verdict of "Pass for that exact head", which binds the verdict to the head and agrees with the exact-head checks at lines 664-667 and the C1 bullet at lines 333-337.
* M2 closed (lines 725-731): step 8 now reads "assess the resulting exact HEAD, and only then push with `--force-with-lease`", and "before any push of it" at line 731. A rebase no longer pushes before assessment. This agrees with the worker-publication prohibition and step 6 (assess, then push).
* No contradiction: hosted checks necessarily follow the push, and step 7 still requires them (lines 664-667) before merge, so the pre-push assessment and the post-push hosted checks are consecutive gates and not in conflict. The C1 bullet's "hosted checks before merge" remains accurate.
* Frontmatter lines 1-5 are unchanged from HEAD, the file has zero non-ASCII characters, and the diff shows only the two M1/M2 edits on top of the earlier C1-C3 hunks.
