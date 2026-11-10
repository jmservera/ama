---
title: Issue 130 process D2 plan
description: Plan for a source-unchanged, metadata-only process-disposition continuation of issue 130
ms.date: 2026-11-10
---

## Objective

Add new, dated process-disposition documentation for the existing read-only nomination view candidate `eb64413236cd0bc0aacc76ac3a89825ba43a9d19`, in a fresh strictly witnessed chain. No product, test, checker, configuration, regular documentation, package, manifest or image file changes. No claim that the old product code is implemented anew.

## Distinctions to preserve

* Original implementation and its original observations: seven successful boundaries, two refused calls (seq 2 research-open, seq 8 commit-complete) retried despite the STOP instruction, one unrecorded wrong-`--repo` call. Original `verify` exit 1, qualified.
* D1: read-only diagnosis, no repository write.
* D2: this plan, its research, details, critique, changes, review and state, at their actual times.

## Phases

1. Research (done after research-open, seq 2): identities, hashes, authority limits. Research file `issue-130-process-d2-1110-research.md`.
2. Plan: this file, with `details` and `critique`. The plan hash observed at plan-done must stay identical through the freeze.
3. Implement (metadata only): write one process-disposition changes record `issue-130-process-d2-1110-changes.md` and record verification output. The changes file is created before implement-start, as the helper requires. Verification is factual, not new implementation:
   * branch, head and base checks; clean status before writes
   * git tree id equality of `src`, `infra`, `tools`, `.github`, `docs` against eb644; empty `git diff eb644 -- . ':!.copilot-tracking'`
   * blob equality of all seven original tracking files and unchanged original external records
   * strict all-level JSON key uniqueness of the new state file and the new events
   * `node --check` of `panels.js` and `app.js` as the one small existing source verification (command, output and exit recorded). No tests, browser, SQL or gate runs.
   * documentation review of the new files against Markdown conventions
4. Review (after implement-done): author review, same agent, disclosed as not independent. One execution. Findings are reported and are not corrected inside this task.
5. Commit and freeze: stage only the new D2 tracking files, repository-local privacy-safe identity, Copilot trailer, `Refs #130` and `Refs #81`, no closing keyword. Then `commit-complete --claim-commit <actual HEAD>` and `verify`, with actual exit and hash.

## Witness contract for a source-unchanged implementation phase

The helper requires only a non-empty `changes` artifact listed in state at implement-start and implement-done. The implementation phase here is the writing of process-disposition metadata, so `implement-start` and `implement-done` will observe empty `dirty_source` and only tracking-artifact dirt. No event is labelled as product implementation. An empty `dirty_source` at both events is expected and is not evidence of a product edit.

## Stop rules

* Any refused helper event stops the chain at once. The command, exit and log are preserved and returned as a hold. No retry, repaired chain, new helper or unsupported stop.
* A failed required verification is a hold, not permission to fix source, tests or helper.
* Any unexpected tracked or untracked change outside the allowed new D2 files holds the work with no stash, reset, commit or move.
* The state file and the events are checked for duplicate JSON keys at all levels before every event.

## Allowed writes

Only new files under `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}` with `issue-130-process-d2-1110` names and the new critique path. Plus external ROOT files `phase130-process-d2-evidence-1110` and `handoff-130-process-d2-1110.md`.

## Non-goals

No source correction batch, no D3, no parent or main adoption, no rebase, no push, PR, merge, issue or board change, no publication, no human or real-resident approval claim, no OD-41/42 change.
