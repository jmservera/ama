<!-- markdownlint-disable-file -->
# Research and validation record: keyboard probe C4 (2026-11-10)

Disposition: executed (read-only source and evidence inspection). Planning Readiness: Ready. Parent: C3. This file is also the technical audit qualification linked from `src/api/README.md`.

## Why C4

Hosted rubric score on PR 1414 was 77 against trusted main 78 (native scoring run 42864188813). Only criterion B6 (written communication) fell, from 4 to 3. The scorer found that `src/api/README.md` lines 4147-4172 cite opaque non-repository session paths and process jargon that serve authors, not feature users. This is a genuine readability defect. It is not permission to lower the baseline or change the scorer, workflow or rubric. C4 rewrites the live README section in plain language and keeps the audit detail here.

## Observed source and checks (bounded synthetic observations, not acceptance)

* Observed source head: `cb01c33c42ceef31ee699649ecceedadc487945d` (C2). Four validated blobs, still identical on the C4 base `7b31e2d8`: probe `e8b7d9f1...`, probe test `228a5390...`, `journey_acceptance.py` `e3466b6e...`, `perspective_walkthroughs.py` `f1828b2e...`.
* Pinned ruff 0.17.1 and mypy 2.4.0 clean on those files; helper tests 6 OK; core register tests 16 OK; one browser run on owned synthetic data: exit 0, 714 printed PASS lines, 15 deliberate mutations rejected, 15 declared no-table walks. The 714 is printed lines, not 714 criteria. Not rerun in C4.
* Limits: fixture roles are not authentication; DOM status text is not assistive-technology output; endpoint and handoff wording is text presence only; five screens have no table on the fixture; Asset, Procurement and Auditor have no login role; the first listed home stands in for every home; the entry target has a focus assertion but no mutation. Whole #134, AC-034 to AC-043, human and assistive-technology acceptance remain unmet. #1401 and #1402 are untouched.

## Execution records (all retained, none edited or waived)

Evidence directories sit in the owner's session `files` directory, full path `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/` (not in the repository): `phase134-walkthrough-plan-evidence-1110`, `phase134-keyboard-c1-evidence-1110`, `phase134-keyboard-c2-evidence-1110`, `134-keyboard-c2-evidence-1110` (C2 logs), `phase134-keyboard-c3-evidence-1110`, `phase134-keyboard-c4-evidence-1110`; handoffs `handoff-134-keyboard-c2-1110.md`, `handoff-134-keyboard-c3-1110.md`; the retained hosted score comment `pr1414-score-comments-2078.json`.

* Original chain: 8 records, verify exit 1, QUALIFIED (a marker refused at sequence 7, then accepted at 8).
* C1 chain: 9 records, verify exit 1, QUALIFIED (implement-start at sequence 4 refused).
* C2 chain: 8 records, verify exit 1, QUALIFIED. Launch (seq 1) refused for a missing `--brief`. Plan-done (seq 4) refused because a state update ran from the wrong directory and the preflight failure was hidden by piping through `tee`, so the marker was emitted after a failed preflight. Markers from seq 5 carry the note "missing observed predecessor: plan-done". Plan-done was deliberately not re-recorded.
* C3 chain: 7 records, all ok, verify exit 0. Timing caveat: verify reports that the state file changed after each observation, and that the changes file changed after implement-start (skeleton, then finalized). The C3 review file was written just before implement-done, which C4 corrects by creating the review only after a successful implement-done.
* C4 chain: see the C4 handoff; no post-commit result is recorded in any committed file.
* Counter: C1 to C4 spent; one of this probe's five corrections remains.
