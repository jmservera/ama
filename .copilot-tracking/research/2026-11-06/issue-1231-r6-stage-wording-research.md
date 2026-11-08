---
title: Issue 1231 research r6 (retained-stage wording accuracy)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 starting 14:11Z as the first call of a serial Research, Plan, Details, critique sequence, before any edit, test or check in this continuation. Same original session b353a2c9. All earlier records, including the R5 files, are preserved unchanged. The R5 records are qualified here as follows. Their Research, Plan and Details files were created in one parallel batch (13:56:02.874 to .948Z), not as serial phases. They did precede the planning commit (13:57:22Z), the rebase (13:57:30Z), the first test (13:58:06Z) and the first source edit (13:58:33Z). The R5 author Review and final state were created in parallel at 14:00:14Z. The estimated clock times written inside the R5 files stay as recorded. The R4 FULL receipt for `b7f6186` stays historical and invalid for this lineage.

## Brief

* Topic: two wording sites assert that a retained staging file is always a hard-link alias of the archived record. Decide whether that is accurate and what conservative wording is needed.
* Scope: `ranking_publication.py` module docstring, `ranking_publication_runner.py` warning text, `src/core/README.md` only if it makes the same claim. Non-goals: outcomes, return keys, error handling, dates, audit, storage contract, new tests of constant text.
* Posture: focused (bounded internal task, named sources). Delegation: none, inline waves.
* Extensions: repository instructions (ASCII, no em dashes), `docs` conventions. No domain skills needed (not web work).
* Intake: head `e5486018168b0cccb281e06be2fc156934a8bb2b`, tree `831f520a1bc1ebf24c26afaeab4fc51d9b756014`, ignored-inclusive status empty. Parent #79 local `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5` (ancestor). Target stays the parent. `origin/main` last verified `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (provenance only, no fetch).
* Source of the defect: coordinator root assessment `1231-r5-root-assessment-r67.md` (one Low wording defect). Verified independently below.

## Wave 1 (wider)

* Candidate claim sites found by searching `alias` and `stage_retained` across `src/`: helper docstring line 13, runner warning line 358, README line 23 (retention note), Store log at `store.py:271`.
* `README.md:23` mentions `stage_retained` and `stage_not_removed` but makes no alias claim (grep of the file shows only unrelated "alias" lines at 1202 onward).
* Store log line prints only the stage name and makes no alias claim.

## Wave 2 (deeper)

* C1 `src/core/src/zava_forward/core/ranking_publication.py:100-112`: after the primary action, `_remove(stage)` runs; a failed removal sets `outcome["stage_retained"] = os.path.basename(stage)` for both the committed and the loser outcomes.
* C2 Same file, publish body: the winner executes `os.link(stage, record)`, so its stage shares the record inode (true alias). A loser's `os.link` fails with `FileExistsError`, so its stage was never linked and holds the loser's own bytes, which can carry a different `published_on` than the winning record.
* C3 `ranking_publication.py:13` states unconditionally "a hard-link alias of the record that an operator removes". True only for the committed outcome; false for a loser.
* C4 `ranking_publication_runner.py:352-361`: the same warning text is shown for `written` true and false, and says "It is a hard-link alias of the record and must not be edited." The instruction not to edit is still sound as a conservative caution; the alias assertion is not.
* C5 `src/core/tests/test_ranking_publication.py:307-352` (loser with failed cleanup) and `test_ranking_publication_runner.py:223` already exercise the loser and committed retained-stage cases, asserting returned keys and statuses, not the prose.

## Wave 3 (contrarian)

* Could the loser's stage be harmless to edit, so the whole "do not edit" advice be dropped? Not needed; the safest operator action is unchanged (check permissions, remove by hand). Dropping the caution would change behavior guidance beyond the wording defect.
* Could the alias claim be true for the loser after all? No: C2, the loser never links; its stage is a separate inode.
* Should the runner branch on `written`? That adds behavior and a new text path; the brief says conservative wording, no new abstraction. Rejected.
* Is a README change necessary? README line 23 has no alias claim, so no.

## Synthesis

* Accepted: replace both assertions with conditional wording ("may share the archived record's bytes and inode, so do not edit it before checking"), keep the remove-by-hand action.
* Rejected: branching on `written`, new tests of constant text, README edit, helper behavior change.
* Deferred: none.
* Risks: wording only; existing tests assert keys and statuses not text, so no test update is expected. A check that the runner message test (if any) matches text must be run.
* Research disposition `executed`; Planning Readiness `Ready`.
