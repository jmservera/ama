# Issue 86 formal-complaints parent re-alignment: plan and details

Scope: jmservera/ama#86 only, `Refs #86`. Research: `.copilot-tracking/research/2026-11-07/issue-86-formal-complaints-realignment-research.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-86-formal-complaints-realignment-critique.md`. Dated 2026-11-07.

Validation tier: FULL for final publication (adapter persistence and access boundaries). This turn runs only focused unit, strict mypy and Ruff checks. No gate, SQL, browser, image or scanner is started; #1231 holds the only heavy lane.

## Phases

* [x] 1. Research and prospective critique, committed before any rebase.
* [ ] 2. Parent gate: wait at most 15 minutes for rpi-81 to be absent and the parent worktree clean; pin the parent HEAD twice. If not met, write a no-alignment record and stop.
* [ ] 3. Backup the actual pre-rebase HEAD (the commit of these records, which sits on `6ff492adf9d897c81ae666e71696f5a10ed1573d`) as local branch `issue86-pre-realign-1107`, keep `6ff492adf` reachable as a tag-free ref `issue86-frozen-6ff492a`, and enumerate the replay range `c5edb320..HEAD`. Expected: the 6 original child commits plus this 2026-11-07 records commit. Stop if it differs.
* [ ] 4. Recheck parent ref, parent worktree and `origin/main` immediately before and after; stop if either moved. `git rebase --onto <pinned parent> c5edb320ad10d3d73bb985bfb82b2d0bee94381a`. `c5edb320` is not an ancestor of the new parent; it is the correct old boundary. No automatic merge fallback (it could retain rewritten parent history); a conflict with unclear intent stops. Resolve only genuine conflicts, minimally. Never drop a child patch, never touch the parent worktree or branch.
* [ ] 5. Equivalence: `git range-diff c5edb320..backup pinned-parent..new-head`; inspect every non-identical patch and treat skipped commits or unexplained differences as a stop. Compare the slice diff against the parent before and after (blob equality is informative only, since the parent may legitimately change neighbouring code). Verify ancestry of the parent and `origin/main`, and the replay completed.
* [ ] 6. Focused checks at the aligned head: strict mypy, `ruff check .`, `ruff format --check .`, `test_resident_decisions` and any parent-changed test that touches resident decisions or `Store`; import origin proven.
* [ ] 7. Write the alignment and author-review record from actual results; commit with the gh-derived repo-local identity.

## Details

* Scratch `/mnt/ama-gates/restart-1107-86-align/`; `PYTHONDONTWRITEBYTECODE=1`; R3 core venv tools read-only; `PYTHONPATH=src:tests` plus a `zava_forward.core.__file__` print.
* A dirty, moving or ambiguous parent, or a conflict with unclear intent, is a stop with exact evidence.

## Out of scope

New features, runtime changes, web, #144 files, parent edits, retargeting PR 1243, any publication.
