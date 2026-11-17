---
title: Issue 1204 exact schedule prompts research
description: Research for the prompt-persistence continuation of issue 1204 (coordinator recurring schedules)
ms.date: 2026-11-17
---

## Status

Research disposition: executed (bounded). Planning Readiness: Ready.

## Scope

Latest owner scope (2026-11-17): place the exact currently approved live delivery and cleanup prompt bodies inline in the existing Recurring schedules section of `.github/agents/ama-backlog-delivery-coordinator.agent.md`, with a short startup/restart clarification of the existing schedule rules. One bounded prospective continuation of open issue #1204. PR #1813 is an earlier merged PR into the unmerged AI parent #1641; its nine recorded corrections and adverse/Deferred history are preserved, not rewritten. The broader next-action-map/helper/refill redesign is a separate follow-up.

## Evidence

* Source boundary: only the coordinator agent file plus issue-owned RPI/HVE evidence. No tools or model frontmatter, general instructions, code, CI, security, permission or validation-policy change.
* Current Recurring schedules section (lines 190-218 at main 17119a81) already requires versioned snapshots in run evidence, create-verify-stop replacement, read-back of exactly one active delivery and one cleanup, and states live prompts are condensed equivalents, not byte-identical. It has no inline prompt bodies and no restart rule.
* Approved live prompts: evidence-1204-refill/approved-live-prompts.json, observed 2026-11-17 by live manage_schedule list read-back. Delivery historical runtime id 5 (10m, 2601 chars) and cleanup historical id 2 (1h, 617 chars). The delivery prompt ends with "Keep hourly cleanup #2 active and follow its retention contract."
* CLI limit: schedules are session schedules (`/every [interval] [prompt...]`) needing a running coordinator session. `/restart` restores supported live sessions but schedule recovery is not documented as guaranteed. No storage path or API is claimed.

## Decisions

* Embed both prompts verbatim in fenced `text` blocks, labelled approved snapshots with historical ids.
* Add a Startup and restart paragraph that restates existing rules: list live schedules first, keep matching active recurrences, create only missing authorized ones, cleanup first, substitute only the newly observed cleanup handle for "#2" when instantiating the delivery prompt, verify exactly one of each, honour pause, completed scope, authority/expiry, blockers and retention. IDs are runtime handles.
* Update the Provenance bullet so it no longer contradicts the new snapshots.
* HVE classification candidate: Medium (verbatim copy plus clarification of existing lifecycle; no new action, permission or gate). Behavior gate satisfied-and-skipped, to be re-judged at review.

## Remaining acceptance

Original #1204 acceptance beyond this prompt-persistence delta is not asserted met here; use Refs #1204.
