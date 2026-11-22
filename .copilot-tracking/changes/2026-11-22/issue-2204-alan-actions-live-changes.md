---
title: Issue 2204 Alan actions live, changes
ms.date: 2026-11-22
---

Status: implementation complete. No `src/` change; focused tier (documentation and live evidence only). Never pushed.

## Changes

* Evidence under `.copilot-tracking/evidence/2026-11-22/issue-2204-alan-actions-live/`: `alan_probe.py`, `live_alan_actions.py`, `live-alan-actions.json`, `run.log`, two screenshots (emails masked).
* New note `docs/reference/research/issue-2204-rule-actions-owner-live-2026-11-22.md`; index entry in `docs/reference/README.md`; entry appended to `docs/reference/log.md`.
* The shared state file `issue-2204-live-state.json` of the earlier task of that name was replaced by this task's state (history in Git).

## Live changes (demo, reversible)

* Entra app-role assignments changed during the run: the main test account to Programme Manager plus RuleAuthor, Alan Steiner to RuleOwner plus Programme Manager. Both restored (test account Programme Manager only, Alan RuleOwner only) and verified through Graph.
* One synthetic exercise card `exercise-rules-alan-2204` persists (append-only table): version 1 untouched draft (origin not established, an aborted first attempt is the only candidate), version 2 taken through draft, approved, active, held, active, held, retired.
* Divergence: a first script run started concurrently with the `implement-start` witness call and was refused at sign-in by a script loop defect; no card action came from it as far as established. Fixed and rerun after the witness succeeded.

## Per-criterion table

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Proven (all-roles note plus this run for RuleAuthor and RuleOwner) | research note |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven (403 on RuleOwner propose, author approve and activate; credential literal scan clean) | `live-alan-actions.json` |
| 3 | Evidence recorded | Proven | note, index, log, evidence folder |

## Rule actions (goal)

| Action | Result |
| --- | --- |
| approve | Proven live, 200, state approved |
| activate | Proven live, 200, state active |
| hold | Proven live, 200, state held |
| release | Proven live, 200, state active |
| retire | Proven live, 200, state retired |

Not ticked on GitHub: ticking is left to the owner after merge. MFA did not block Alan; the blocker was a RuleOwner-only identity being refused for lacking a staff role.
