---
title: Ranking current-main stabilization checkpoint 440 plan
description: Plan for the scoped issue 440 current-main stabilization checkpoint after the ranking publication integration merged to main
ms.date: 2026-11-08
---

## Scope and tier

Task `440-ranking-main-stabilization-checkpoint`. Worktree `/home/azureuser/source/ama-wt/checkpoint-ranking-main-440`, branch `docs/ranking-main-stabilization-440`, declared PR target `main`, start HEAD `a80acadaa1b7d96a10e71b246e297bc2825d3de5`. Local frozen handoff only; no push, PR, merge, issue write or tick.

Tier FOCUSED. Rationale: documentation and tracking records only (cutover pack append, index, log, RPI records); no production code, deployment, infrastructure, SQL or security-policy change. If a check shows a defect that needs executable change, stop and return a narrowly evidenced requirement through the coordinator. Do not downgrade or silently upgrade the tier.

Research source: `.copilot-tracking/research/2026-11-08-ranking-main-stabilization-440-research.md` (disposition executed, Planning Readiness Ready).

## Phase 1. Planned local observations (before canonical edits)

Resource preconditions, each checked immediately before use and stopping on failure: `/tmp/ama-rpi-heavy.lock` has no holder, no competing test or gate process, `/mnt` free space at least 2 GB, scratch directory `/mnt/ama-gates/ranking-main-440-1108` absent before creation (refuse a collision, never delete). All scratch, pip and cache output goes under it with `PYTHONDONTWRITEBYTECODE=1`; pip only; no other environment is touched.

* [x] 1.1 Create a venv in the scratch directory. Export the committed tree with `git archive HEAD src | tar -x -C $S/export` so pip builds out of tree and leaves no `build/` or `*.egg-info` in the checkout (PC-001). Install `$S/export/src/core`, `$S/export/src/agents` and `$S/export/src/api` non-editable, so the installed packages are tested, then `pip check`. Immediately afterwards require `git status --short --ignored` to show 0 lines and record it.
* [x] 1.2 Prove import identity: print `zava_forward.core.__file__`, `ranking_publication.__file__`, `ranking_publication_runner.__file__` and the api server module location, require them under the venv `site-packages` and not under `src/`.
* [x] 1.3 Core selectors, run from `src/core` with `PYTHONPATH=tests`: `python -m unittest discover -s tests -p "test_ranking_publication*.py" -q`. Planned classes present in source: `PublicationTests`, `ConcurrentWriterTests`, `SignoffTests`, runner `PublishTests`, `ConcurrentPublishTests`, `ScheduleAndVerifyTests`, `MalformedArchivedDateTests`, `CliAndStoreTests`, `AssessmentFindingTests`, `StorageAndDuplicateFindingTests`, `AssessmentCycle1Tests`.
* [x] 1.4 API selectors, run from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`: `python -m unittest discover -s tests -p "test_ranking_*.py" -q`. Planned files present in source: `test_ranking_policy.py`, `test_ranking_publication_wiring.py`, `test_ranking_scale.py`. Record any SQL-class skip as a skip, not a pass of SQL. All three selectors run with `ZF_DATA=$S/data/zavaforward.json` (absent under scratch) and `HOME=$S/home`, so the private default dataset is never read (PC-004); stop if a selector touches a path outside `$S` and the worktree. Check `df` before and after the venv install and before the API run, stopping below 2 GB (PC-007).
* [x] 1.5 Agents selector, run from `src/agents` with `PYTHONPATH=../core/tests`: `python -m unittest discover -s tests -p "test_cohort_ranking_eval.py" -q`.
* [x] 1.6 Preserve the first failure of any selector exactly; a command written wrongly is reported as such and rerun once with the corrected form, keeping both logs. No test or source change.
* [x] 1.7 Record every command, exit, test count, skip and the exact environment and source identity. These are installed-package local observations at `a80acada`, source-qualified, and not a full gate.

## Phase 2. Traceability and comparison work (read-only)

* [x] 2.1 Join document-qualified requirements and decisions to source and tests: PRD PR-006, PR-007, PR-008, FR-012 with AC-015, AC-040, FR-054 with AC-073, ADR 0002 decision 4 (Proposed), ADR 0003, ADR 0006; BRD general ranking statements only.
* [x] 2.2 Confirm the HTTP boundary by test evidence: non-manager 403 for snapshot, status and publish, manager success, 409 `committed_unconfirmed`, ArchiveStorageError mapping and the audit entries; cite the passing selector, not static reading only.
* [x] 2.3 Reconcile the ADR 0002 implementation-status row for decision 4 against source. It is a dated 2026-10-08 historical snapshot that already says it is not the current status, so record it as dated history with the current contract in `src/core/README.md`; make no ADR edit.
* [x] 2.4 Compare every observation against open owners 79, 1231, 1258, 1259, 81, 86, 107 and the other open ranking issue search results. Record explicitly if no new defect is confirmed. A new proposal needs a smallest repro, severity, requirement trace, regression-test need and independent RPI owner, and is returned through the coordinator without implementation.
* [x] 2.5 Record the failed serialized `gh pr diff` (300-file cap) exactly as the coordinator reported it and never present it as successful; the 308-path paginated equivalence and byte-equal Git diff are coordinator reports, not re-run here, and are classified not observed in this session (PC-003). Carry the original socket-path preflight refusal and the prior R35 and adverse records by workspace-relative path as retained, unedited history, and report the refusal as a refusal and not a pass (PC-002).
* [x] 2.6 Classify evidence as local observed (this session), local observed historical source-qualified (receipt `ac0f29f9`), Azure observed (none), implemented unverified, deferred, blocked and unknown.

## Phase 3. Canonical edits (only after the planning commit)

* [x] 3.1 Append to `docs/architecture/cutover-evidence-pack.md` one new dated section after the last existing section, titled with the 2026-11-08 date and `Refs #440 #79 #1231`, no closing keyword. Contents: the retained socket-path preflight refusal and prior R35 and adverse records by path, pins, document identities, source and receipt identity with the main-versus-candidate qualification, actual commands and results, traceability table, boundary findings, existing owners, exclusions, classifications, recommendation (continue, fix or proposed pivot) and exact gates and resume points.
* [x] 3.2 Add one paragraph to `docs/reference/README.md` after the nearest existing cutover-pack paragraph and append one entry to `docs/reference/log.md`. Do not rewrite earlier text.
* [x] 3.3 Keep records ASCII, frontmatter on new records, no H1, `*` lists, no em dashes, and plain-text workspace-relative paths in tracking records (no Markdown links in them, which broke a prior helper).

## Phase 4. Focused validation (after edits, before Changes)

* [x] 4.1 `git diff --check`, ASCII scan of added lines, zero removed lines in the three canonical files, unique new pack heading, new relative link and anchor targets resolve, frontmatter and JSON parse of new records, ignored-inclusive status.
* [x] 4.1b Scan added lines and the commit messages for closing keywords (including negated forms) and for approval wording applied to 79, 1231 or 440; the pack text must use `Refs` only (PC-006).
* [x] 4.2 Existing documentation or tracking tests covering touched paths: `python -m pytest tools/test_tracking_retention.py -p no:cacheprovider --basetemp=$S/pt` using system Python if pytest is importable; otherwise record not applicable with the reason (PC-007).
* [ ] 4.3 After the FINAL commit of all records (PC-005), run `python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <origin/main sha> --out /mnt/ama-gates/ranking-main-440-1108/gate` with stdin `/dev/null` in the foreground, then `--verify-receipt <receipt> --base <same sha> --required-scope partial`. Stop, without retry, if selection differs from the expected groups preflight, namespace and static, if main moved, if the lock is held or if disk falls below 2 GB. A tool refusal is reported as a refusal.
* [x] 4.4 Fresh pins immediately before the final record: `origin/main`, HEAD, tree and BRD, PRD and ADR blobs.

## Phase 5. Changes, Review and handoff

* [x] 5.1 Write the Changes record from actual diffs and command logs.
* [x] 5.2 One author Review in a later completed turn after checks, using the `rpi-review` skill; record execution separately from outcome; it is not independent assessment.
* [ ] 5.3 One state JSON write and plan ticks after Review, then one final commit. Fresh `gh api user` identity, repository-local noreply for author and committer, Conventional message with the Copilot trailer, no amend, explicit staging paths.

## Commit sequence

1. Planning commit of the research, plan, details and critique records before any canonical edit.
2. Canonical edit commit (pack, index, log).
3. Final commit of Changes, Review, state and plan ticks. Decision (PC-005): the focused gate runs last, on the final frozen head, with its output and the receipt kept external. The tracked records name the planned gate and its prerequisites but do not embed its result; the result, receipt path and sha256 go in the external handoff and the final response. Any later commit invalidates the receipt, which is then historical for its head, and a changed head needs its own verify run.

## Critique Disposition

One independent critique executed (verdict Revise, 2 High, 4 Medium, 1 Low, no Critical), recorded in `.copilot-tracking/plans/2026-11-08-ranking-main-stabilization-440-critique.md`. All seven findings are compatible and applied directly; none conflicts with a confirmed user decision and none needs a user decision.

* PC-001 applied: out-of-tree export and install, ignored-inclusive status check (1.1).
* PC-002 applied: retained socket-path preflight refusal and R35 and adverse records (2.5, 3.1).
* PC-003 applied: failed `gh pr diff` recorded as failed, equivalence not observed (2.5).
* PC-004 applied: scratch `ZF_DATA` and `HOME` for all selectors (1.4).
* PC-005 applied: gate runs last at the final head, result kept external (Commit sequence, 4.3).
* PC-006 applied: closing-keyword and approval-wording scan (4.1b).
* PC-007 applied: disk checks and pytest fallback (1.4, 4.2).

## Follow-Up Items

* Existing owners stay as they are: 1258 (archive ancestor durability), 1259 (unusable archive path), 1231 (parent topic merged), 79 (epic).
* Current-main full gate at a later main, and 1231, 79 and 440 closure remain outside this checkpoint.
* Policy owner sign-off, thresholds, first rule order, retention, deployed scheduling, crash and cross-UID behaviour, live model, Azure and acceptance testing remain unproven.
