# Issue 444 current-main integration (round 3) research

Date: 2026-10-25. Task slug: issue444-main-ea5577b2-integration. Parent: issue444-rebase-readiness (artifacts and its Conformant-with-Low review preserved).

## Scope

Existing owner-authorised #444 loopback-only synthetic read-only resident preview only, independent of unaccepted #441. No provider, real accounts or data, Azure/SQL/Graph, deploy, AI spend, messages, uploads, consent or production-resident work.

## Evidence (read-only inspection, worktree clean)

* Local HEAD ab07351acf692f348994ca06533c990dac3a1f33 (base 0245944a, historical gate and receipt 22f8df49... apply to it only). Remote PR head 9c896630107156f8bb82b49c7730931ec97d8d3b adds one bot commit `chore(rubric): record score 73/100`; `git diff ab07351a origin/<branch>` is .github/rubric/scores/latest.json only (9 additions, 9 deletions). Hosted rubric/score SUCCESS.
* origin/main ea5577b2ed0e051161a83813daa63d86e4613c7a adds #458 OSM demo basemap docs: infra/README.md (+1), src/api/README.md (+3), docs/reference/log.md (+6), rubric score files. No Python source.
* PR 455 is draft, CONFLICTING, closingIssuesReferences empty. Body is stale: head 6878d6ec, base 36996d70, and uses the wording "does not close it" which contains a closing keyword pattern; it must say only `Refs #444`.
* `git merge-tree` of the remote head with main: conflicts in docs/reference/log.md (both append) and .github/rubric/scores/latest.json (bot metadata); src/api/README.md auto-merges (both sections kept).
* Latest original review: Conformant with one Low follow-up: grants file re-read per request, but dataset, case and representative-authority data load once, so authority edits in the dataset need a restart. Keep explicit; not fixed here (no source refactors authorised).
* Shared heavy lock held by #360 gate PID 1090343; do not interrupt. Services 8350, 8444, 8445 return 200 and are old snapshots; HTTP 200 is not acceptance. They are not touched.
* web-interface-guidelines refetched 2026-10-25 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (8,055 bytes) for the web-file review.

## Intent per conflict

* log.md: keep every main entry, then the #444 entry (append-only).
* latest.json: rubric metadata only. The remote bot score 73/100 (commit 9c896630) was computed on the prior head and is preserved as historical evidence in the changes artifact; the rebased tree takes main's file. The bot re-scores on synchronize. No source churn is made to influence it.
* README files: auto-merge, verify both sides present.

## Rebase necessity

Required: PR is CONFLICTING and a merge would add a second integration merge. Coordinator authorised a run-owned rebase and `--force-with-lease` only if necessary; it is, and the lease pins 9c896630.

## Planning readiness

Ready. Disposition: executed.
