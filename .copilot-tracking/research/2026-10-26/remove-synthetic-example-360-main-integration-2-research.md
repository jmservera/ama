# Research: second main integration for PR 459 (issue 360), documentation only

Date: 2026-10-26 (about 09:05Z), written before the merge. Local only; no Azure, SQL, Graph, secrets, install, Docker, browser, scan or gate.

## Evidence (read-only git inspection)
* Topic and remote head are both f3658ced (bot score commit over dfaaf85b). Worktree clean. Local identity is the repo-local noreply address.
* origin/main is acafc6ee (PR 460 merged). Against the topic merge base it adds 42 files: capstone deck, scientific-paper agent and tracking, thought-leadership material, rubric score/badge, and `docs/reference/log.md` (+207). No `src/` or `infra/` path.
* Trial merge (`git merge-tree`) conflicts in exactly two files:
  * `.github/rubric/scores/latest.json`: bot metadata. Topic side holds the score for commit dfaaf85b; main holds a later score for d852cf74 with different `infrastructure` and `capstone-deck` fingerprints.
  * `docs/reference/log.md`: both sides appended at the same tail position. Topic side adds two 2026-10-25 synthetic-case entries (9 lines); main adds 207 lines of entries.
* No running gate. A fix for the shared image-scan blocker is validated on another PR but not on main; this PR must not copy runner source or launch a gate before it lands.

## Decisions
* Normal merge of origin/main, no rebase, amend or force.
* `latest.json`: take main's file entirely. It is bot-owned, describes main's baseline, and this PR has no scoring intent; merging two scores would synthesise a score that no scorer produced.
* `log.md`: keep every entry of both parents; main's block first, then the two topic entries appended after, no entry edited or reordered internally. Intent is unambiguous so no stop condition applies.
* Earlier adverse reviews, correction record and the previous integration artifacts are not edited.
* Receipts 96232201, e2081c02, a98e1e08 and 46a1a06f are historical; none is current for the merged head.
