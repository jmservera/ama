---
title: Issue 440 post-1500 checkpoint details (0240)
description: Phase details, exact selectors and annex outline for the post-1500 provenance annex, Refs #440
ms.date: 2026-11-13
ms.topic: reference
---

## Status

Draft, prospective, not approved. Companion to [plan](../../plans/2026-11-13/issue-440-post1500-0240-plan.md).

## Exact pinned inputs (to re-verify in P1)

* Main `ad1a1722965e7943166e5d0018089b8d2dcd0316`, tree `f650b1ba936c7cd65442a4613eb43e071fb825df`.
* PR 1500 head `4961acbeca952f9e3f60a1c09905d4b7f8acce34`, hosted merge ref `f1a5ebccd271b600ec9fe6ed53ef19d79930130e`, base parent `c401e5d56446b5752e8d91af6a45f3f06269c4bd`.
* Hosted Source CI run `43351173623` (pull_request event, checked out as the merge ref). The rubric scorer run `43351173644` is a pull_request run at head `4961`; its contexts are part of the 19-context rollup but its checkout identity is not verified here. The post-merge `push` scorer run on the merge commit was in progress when read; identify its actual run id by query before citing, or state it as not yet observed.
* Document blobs: BRD `34d88395de86`, PRD `c788b917bafa`, proper-warm PRD `f7f9b7675e60`, ADR 0001 `d42fa5c4615f`, 0002 `cbe21530043f`, 0003 `d60645397b20`, 0004 `9406c2e747ce`, 0005 `4d610335a5a1`, 0006 `956da1a3b804`, 0007 `541e0f72dd2c`.

## P1 re-pin commands (read-only)

* `git fetch origin main`, `git rev-parse origin/main origin/main^{tree}`.
* `gh pr view 1500 --json state,mergeCommit,closingIssuesReferences,statusCheckRollup`, `gh issue view 83 --json state`, `gh issue view 440 --json state`.
* `gh run view 43351173623 --json jobs,headSha,event,conclusion` and, from the job log, only the `Ran N tests` and `OK (skipped=N)` lines, the checkout `refs/remotes/pull/1500/merge` line, and the specific named `... ok` or `... skipped` lines for each test the annex names (the funding-membership SQLite test, its `MssqlQueueMembership` skip in the API and core jobs, the two C4 baseline tests, `test_live_doc_links`). Aggregate counts alone do not support named outcomes; omit any named claim that cannot be re-read. Never paste raw log text.
* List the `push` runs for the merge commit (`gh run list --commit <sha>`) and record each run id, workflow and state; state absent or path-filtered Source CI as not success.
* `gh api repos/jmservera/ama/git/commits/f1a5ebccd271b600ec9fe6ed53ef19d79930130e --jq '.tree.sha,[.parents[].sha]'`.
* If the post-merge `push` scorer run has concluded, record its conclusion; otherwise state it as not yet observed.

## P2 annex outline (draft, ASCII, `*` lists, no em dash, no bold-prefix items)

* Heading: `## Post-1500 merged-main provenance checkpoint (2026-11-13, Refs #440 #149 #96)`.
* Opening paragraph: draft, local-only, not approved; not a repair or correction cycle; records the actual merge; not whole-product, human, AT, Azure, model or actual-SQL acceptance; the original final UX Review stays Partial; C4 independent assessment is a bounded publication Pass.
* Identities table (main, tree, PR head, merge ref, base).
* Classes table: A parent-source (`288b6a376`, eight lanes, input-equivalent only), B fresh final C4 (13, 21, 4, Ruff 0.17.1 lint and format 152, mypy 2.4.0 236, 7 author mutations as author evidence), C hosted (19 pull-request rollup contexts SUCCESS across Source CI, Capstone Rubric Scorer and the `rubric/score` status, kept apart from the verified Source CI merge-ref checkout; job table with counts 3148/403, 2966/629, 336, 321/1), D merged-main provenance (tree equality, 32 non-tracking files, document blobs).
* Document-qualified status table (blobs equal; no approval).
* Traceability delta: only the WCAG baseline tied-field row (PRD NFR-level accessibility context, nearest by inspection; no new requirement asserted); other rows reference the existing section unchanged.
* Reconciliation table: earlier statement, later fact, disposition (preserved, superseded, or qualified).
* Failure, manual and approval boundaries: constructed data, no consent or approval, manual paths remain, AI scripted, human decisions unclaimed.
* Backlog and holds: 233, scoped 96 (C4 of 5 spent, none inferred), 203, 184, other allowances not borrowed, #83 open, #440 final two criteria unticked.
* Recommendation (proposal): CONTINUE bounded; closures held; independent lanes listed.
* Process limits: what was not run (browser, AT, wholeAPI beyond hosted, full gate, local SQL Server, per-test SQL attribution), hosted limits (mutable image tag, non-verbose SQL step, path-filtered or absent push runs are not success), model label asserted without host attestation.

## Hosted claims allowed and forbidden

* Allowed: the named Source CI jobs concluded success on the verified merge-ref checkout whose tree equals merged main (other rollup contexts are reported as PR rollup successes only); counts and skips as read; the SQLite twin of the funding-membership regression printed `ok` in the core job; the C4 baseline tests printed `ok` in the API job.
* Forbidden: calling hosted results locally executed or fresh local counts; inferring the SQL Server job proved the membership twin or any named selector beyond module-level success; inferring browser role-walk, AT, WCAG, Finance, legal, live or Azure acceptance; reading hosted success as closure of any issue.

## Conditional focused observation (not planned, not recommended)

Only if root or the owner later requires per-test SQL Server attribution for the funding-membership regression.

* Selector: from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest -v test_mssqlstore.MssqlQueueMembership` with the marker environment the workflow uses, against a local disposable SQL Server container.
* Preconditions: separate named root admission; exact tree `f650b1ba...` clean; immutable image id recorded; local-only container, no Azure, provider or private data; evidence external; skips reported; no other selector.
* Why not now: repeats an unchanged-input module already hosted-passed at module level; SQL-sensitive tier; no defect or contradiction is known.

## P4 exact checks

* `git diff --check` over the change.
* ASCII and em dash scan of added lines in the pack and log (`grep -nP '[^\x00-\x7F]'` limited to added hunks).
* Relative-link review of added text; prefer no relative links in the annex as the earlier section did, except to the tracking records this task creates.
* From `src/core` (after the project is installed per repository rules, no `PYTHONPATH=mvp`): `python3 -m unittest tests.test_live_doc_links` (it reads the pack). This is not a wave observation.
* Not run: whole API or core, browser, SQL, Docker, image, scanner, model, provider, Azure, full gate, `--changed` gate.

## Stop rules for the later stage

* Stop and report precisely if main moved in a way that touches the pinned facts, if the hosted counts cannot be re-read, or if any check fails; do not open a correction cycle. A failing documentation check is fixed only within the annex; anything else is routed to its existing owner.
* No push, PR, merge or issue mutation without explicit publication admission. PR text is `Refs` only.
