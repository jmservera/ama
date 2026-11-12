<!-- markdownlint-disable-file -->
# RPI Plan Critique: accuracy follow-up for the post-153 checkpoint (2026-11-12)

## Metadata

* Task ID: post153-integration-440-1112-accuracy
* Critique date: 2026-11-12
* Plan: .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-accuracy-plan.md
* Phase details: .copilot-tracking/details/2026-11-12/post153-integration-440-1112-accuracy-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only correction of exactly four claims (C1 to C4); originals byte-preserved; no source, test or workflow edit; no new issues; counts 145/92 and pin 4074b44f3 unchanged.
* Research and evidence considered: .copilot-tracking/research/2026-11-12/post153-integration-440-1112-accuracy-research.md; original research, critique and plan named post153-integration-440-1112-*; docs/architecture/cutover-evidence-pack.md lines 7478-7543; docs/reference/README.md lines 1419-1424; docs/reference/log.md lines 11567-11571.
* Decisions, dependencies, and acceptance criteria considered: plan FR-1..FR-4, AC-1..AC-4, P01..P03.
* Assessment boundary: independent read-only git and gh checks at HEAD 8bfd52729. External raw evidence files were not read. No standard was fetched.

Independent verification results:

* C1: `git grep -l` of the five ids over HEAD returns three files (pack, runbook.md, .copilot-tracking/research/2026-11-12/five-home-script-134-1112-research.md); over 4074b44f3 it returns the runbook and that research file (the pack section is not yet there). Confirmed.
* C3: `gh pr view` mergedAt: 1470 = 2026-11-12T17:38:13Z, 1475 = 17:46:55Z, 1478 = 18:00:25Z. 088e8c3c0 is an ancestor of 4074b44f3 and bbb1d20cc is an ancestor of 088e8c3c0. Confirmed.
* C2: `git show --name-only` counts under `.copilot-tracking`: 088e8c3c0 = 20, 38d3ed187 = 7. Same via first-parent diff. Confirmed.
* C4: confirmed as unfetched-standard claim at pack line 7530.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-1 / C1 | Covered, with a gap | Boundary text is right; line 7513 also needs the "limits" tail kept consistent (PC-006). |
| FR-2 / C2 | Partial | Count belongs only to the original research and critique; but pack line 7542 repeats "all applied directly" (PC-001). |
| FR-3 / C3 | Partial | Plan fixes the pack opening only; the same ordering claim is repeated in README and log (PC-002, PC-003). |
| FR-4 / C4 | Partial | Pack F1 fixed; log entry repeats "role-less `pre` elements" (PC-004). |
| AC-1..AC-4 | Partial | AC-1 uses `git diff --name-only` which omits untracked files; AC-3 forbids the lines that PC-001 needs (PC-005). |
| Scope constraints | Covered | No source, test, workflow or issue edit; counts and pin untouched. |

## Verdict

* Verdict: Revise
* Rationale: the four named corrections are evidence-backed and correct, but the plan would leave verifiable copies of C3 (README, log) and a related false statement about the critique outcome (pack Process limits) uncorrected, and its mechanisms for finding them (grep for the corrected phrases) would miss them. All fixes are direct planner corrections inside the stated scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Pack "Process limits" repeats the PC-007 claim that the C2 correction was fully applied

* Related IDs: C2, FR-2, AC-3, P01-T02
* Evidence: docs/architecture/cutover-evidence-pack.md:7542 ("one independent read-only critique (verdict Revise, nine findings, all applied directly)"); original critique PC-007 asked for a reproduced count; original research line 31 still says 16 and the critique table line 26 says 19.
* Concern: the sentence is false in the same way the plan admits (PC-007 not fully applied). The plan puts that admission only in the appended note and AC-3 limits the pack diff to four places, so the unqualified sentence would remain.
* Impact: the pack would contain a contradiction between line 7542 and the new note.
* Smallest useful change: add a fifth targeted edit to line 7542, replacing "all applied directly" with "eight applied; PC-007 (tracking-file count) was not fully applied, see the accuracy note", and add this line to AC-3.
* Action owner: planning parent
* Exact resolving evidence: `git diff` shows line 7542 changed and the string "all applied directly" absent from the pack section; AC-3 text lists it.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: docs/reference/README.md repeats the C3 ordering claim and the plan defaults to leaving it unchanged

* Related IDs: C3, FR-3, P02-T01
* Evidence: docs/reference/README.md:1421-1422 ("It covers merged PR 1470 ... and PR 1475 ... on `main` `4074b44f3`, which the previous checkpoint excluded"); P02-T01 says leave it unchanged "unless its text repeats a corrected claim (check by grep)".
* Concern: both PRs merged before PR 1478 (17:38:13Z, 17:46:55Z vs 18:00:25Z), so "the previous checkpoint excluded" them as merged inputs is wrong in the same way as C3; what is true is that the tested wave (pin bbb1d20cc) predated them. The suggested grep keys (the phrases in the plan's own list) would not match "previous checkpoint excluded" if the planner greps for "later-merged" or "after the previous"; it only matches if it greps "previous checkpoint". Also, the README pointer would be left claiming the wrong ordering.
* Impact: the index, which agents read first, carries a wrong statement the follow-up claims to correct.
* Smallest useful change: edit that one sentence to "whose merges followed the historical tested pin `bbb1d20cc` and preceded the PR 1478 publication, and which the 281-test wave did not cover"; list README in AC-1 as a touched file; specify the grep pattern `previous checkpoint|previous #440|later-merged` across docs/reference/README.md and docs/reference/log.md.
* Action owner: planning parent
* Exact resolving evidence: `git diff docs/reference/README.md` shows only that sentence changed; grep for the pattern in the post-153 paragraph returns nothing wrong.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: log entry of 2026-11-12 repeats C3; the log is append-only so the plan must say how it is corrected

* Related IDs: C3, FR-3, P02-T01
* Evidence: docs/reference/log.md:11569 ("both excluded by the previous checkpoint"); plan P02-T01 only says to append one entry.
* Concern: the earlier entry cannot be edited, and the plan does not state that the new entry must explicitly correct it.
* Impact: the log would keep a wrong statement with no pointer to the correction.
* Smallest useful change: specify the new log entry content: corrects the ordering (merge times, tested pin), the tracking counts 20 and 7, the five-id boundary and the F1 wording, states originals and the earlier entry are preserved, and links the pack accuracy note.
* Action owner: planning parent
* Exact resolving evidence: the appended entry at the end of docs/reference/log.md contains the four corrections; `git diff` on the log shows additions only (no deleted or altered lines).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: log entry also repeats the C4 "role-less" characterisation

* Related IDs: C4, FR-4
* Evidence: docs/reference/log.md:11569 ("role-less `pre` elements with `aria-label`"); the research says native elements carry implicit roles and the generic-role question is unverified.
* Concern: "role-less" is the same imprecision as the withdrawn ARIA claim; the plan's FR-4 covers only pack F1. README line 1423 ("one static accessibility concern") is acceptable.
* Impact: an append-only line would keep the overbroad wording unless the new entry replaces it.
* Smallest useful change: include in the new log entry that the concern is narrowed to "`pre` with `aria-label` and `tabindex` and no explicit role; implicit-role name exposure unverified".
* Action owner: planning parent
* Exact resolving evidence: new log entry contains that wording; no new text uses "role-less" or "ARIA 1.2 prohibits".
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: acceptance criteria cannot detect the untracked, README and extra-line edits

* Related IDs: AC-1, AC-3, AC-4
* Evidence: plan AC-1 (`git diff --name-only 8bfd52729`), AC-3 (four places); at this moment the three accuracy files are untracked (`git status --short`).
* Concern: `git diff --name-only` omits untracked files, so new `-accuracy` files are not checked until committed; AC-3 enumerates places and would reject PC-001's edit; AC-1 omits README. AC-4 says "the commit is the only new commit" but AC-1 is checked before the commit.
* Impact: verification could pass or fail for the wrong reason.
* Smallest useful change: state AC-1 as `git diff --name-only 8bfd52729 HEAD` after the commit plus `git status --short` clean before it; amend AC-3 to the revised list (five-home paragraph, opening, F1, Process-limits sentence, appended note); name README sentence as in-scope.
* Action owner: planning parent
* Exact resolving evidence: commit file list equals pack, log, README and new `-accuracy` files only; `git diff -U0` on the pack shows hunks only at those places.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: C1 boundary wording must not overreach the git grep scope

* Related IDs: C1, FR-1, P01-T01
* Evidence: phase details P01-T01 ("git grep over tracked files at `8bfd52729`"); `git grep` over 4074b44f3 gives the same two non-pack files; the pack section itself adds the third at HEAD.
* Concern: the search covers tracked files only (ignored and untracked files, support/ and external folders are outside it), and the sentence at line 7513 also says "the generator replay ... was not read" which remains true. The new sentence should name the commit, the ids searched and that the record exists at the 4074b44f3 pin as well.
* Impact: avoids a replacement sentence that is itself over-broad.
* Smallest useful change: word FR-1 as "a search of tracked files at `4074b44f3` finds the five ids only in `runbook.md` and one historical tracking record; untracked, ignored and `support/` files were not searched".
* Action owner: planning parent
* Exact resolving evidence: replacement sentence names the commit and the unsearched areas.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Facts C1 to C4 independently reproduced; narrow scope, originals preserved, no source edit, counts and pin held.
* Residual: earlier pack sections (for example line 7399, "Unmerged PR 1470 and PR 1475", written when the PRs were already merged by 18:00Z) are inconsistent with the C3 facts. Earlier sections are out of scope by the plan; the accuracy note should mention it in one clause rather than edit it. This is an accepted-by-scope risk, not a finding.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* External raw evidence, the original-blobs-before.txt file and the original review were not read. No fetched standard; C4 was assessed only on repository evidence.

## Recommended Next Action

* Highest-impact finding: PC-001 (and PC-002 for the index)
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-006 directly in the plan and phase details, then finalize without another critique.
* User response required: no

## Relevant Artifacts

| Path | Description |
| --- | --- |
| .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-accuracy-plan.md | Plan under critique |
| .copilot-tracking/details/2026-11-12/post153-integration-440-1112-accuracy-phase-details.md | Phase details under critique |
| .copilot-tracking/research/2026-11-12/post153-integration-440-1112-accuracy-research.md | Accuracy research |

## Next Steps

* Standalone critique, verdict Revise: the planning parent applies the planner-owned corrections via `/rpi-plan` or directly; no user action is required.
