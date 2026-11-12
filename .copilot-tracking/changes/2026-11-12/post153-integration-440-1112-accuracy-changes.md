<!-- markdownlint-disable-file -->
# Changes: accuracy follow-up for the post-153 checkpoint (2026-11-12)

Task `post153-integration-440-1112-accuracy`; plan .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-accuracy-plan.md; base `8bfd52729048bc7c94b4d266188307f1d9bc213c`. Scope: full plan except the commit marker (P03-T02, open until the commit exists).

## Implementation evidence

* P01-T01 (five-id boundary): `docs/architecture/cutover-evidence-pack.md`, five-home paragraph. The sentence "No other public tracked file mentions the five ids" is replaced by the actual boundary (script scope, `git grep` at `8bfd52729` finding three files, one tracked historical record not reproduced, areas not searched, no deployment claim). Raw: `five-id-tracked-search.out`. Includes PC-006.
* P01-T02 (opening, counts, ordering): the section opening is qualified (tested pin `bbb1d20cc`, merged before the PR 1478 publication); an "Accuracy note" subsection is appended at the end of the file covering C1 to C4, the observed counts (20 and 7), the wrong 16 and 19, PC-007 not fully applied, the merge times and that the originals are unchanged. Raw: `merge-times-and-counts.out`.
* P01-T03 (F1): narrowed to the observed attributes and the unverified implicit-generic-role question; the ARIA 1.2 blanket statement is withdrawn; the sentence claiming possible AT ignoring is removed. No source touched.
* PC-001: the process-limits line about "all applied directly" is amended in place.
* P02-T01: `docs/reference/log.md` gets one appended entry (earlier entries unchanged). `docs/reference/README.md` index sentence corrected for the C3 ordering (PC-002), 2 lines.
* P02-T02 verification, all local and read-only:
  * `git status --short`: three modified docs and the new `-accuracy` files only.
  * `git diff --stat`: three files, 22 insertions, 6 deletions before the new artifacts; the six removed lines are the four corrected pack lines and two index lines.
  * Seven original tracking blobs equal the pre-change list `original-blobs-before.txt` (blob ids from `git ls-files -s`): `ORIGINALS_EQUAL`.
  * No removed line carried a count, pin or test result change; the 145/92 and `4074b44f3` statements were not removed.
  * Anchors and relative links in the added text reuse the existing section anchor; no new link target.

## Omissions and non-actions

* No test, node check or browser rerun; no web fetch of any ARIA standard; no private or `support/` read; no source, test, workflow, instruction or requirement edit.
* The original research, plan, critique (nine findings), changes, state, review and raw evidence are untouched and keep their errors.

## Remaining work

* P03-T02 commit; coordinator independent reassessment before any publication.
