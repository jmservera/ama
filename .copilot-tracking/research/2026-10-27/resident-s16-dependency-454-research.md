---
title: Resident S16 dependency correction research
description: Focused evidence for PR 454 review thread 4390263899
ms.date: 2026-10-27
---

## Research Brief

Correct the draft backlog's S16/S15 ordering for the owner and PR reviewer.
Scope: the current PRD, active backlog/proposal tables and this dated RPI
evidence. Preserve historical assessment inputs and outcomes. Non-goals:
requirements approval, runtime work, routine activation and merge.
Output mode: convergence, preparing planning.

## Research Parameters

Focused posture, selected for the owner's bounded named-source correction.
Questions: where is S16 -> S15 specified; which active tables omit it; can
the edge coexist with independent urgent help and no OD-53 requirement?
Initial internal areas: PRD story/acceptance tables, draft backlog slice and
dependency tables, current unregistered proposal. External area: the named
GitHub review thread only. No external regulatory claim or new research.

## Extension Registry and Participation

Repository guidance and RPI phase skills apply. No web, accessibility,
security or requirements-authoring assessment is warranted for a dependency
transcription correction. Research stays inline because the trace is small
and continuous. Independent critique and final Review belong to later phases.
No interaction is needed: the owner specified the correction and validation.

## Direction Controls and Prior Knowledge

The existing branch is the requested open PR branch. A clean-worktree
`git pull --rebase` fast-forwarded c1c058f3, including the bot's latest.json.
Earlier RPI/requirements evidence is historical, not authority to mark approval.
Retain urgent help independent of the model, task-release gates and routine OFF.

## Research Cycle Log

Cycle 1 completed inline, in order:

1. Wider: searched `docs/` and tracking Markdown for all four item/story
   identifiers. Found the canonical PRD, active backlog/proposal and historical
   research/assessment inputs. Reflection: only active planning views need
   correction; old assessments must remain byte-preserved.
2. Deeper: mapped S13 -> RB-15, S15 -> RB-17 and S16 -> RB-18.
   The PRD already states S16 depends on S13/S15. Both the slice gate cell
   and combined dependency row omit RB-18 -> RB-17. Reflection: split the
   graph row and synchronize the narrative, preserving all prior conditions.
3. Contrarian: examined PRD S16 acceptance and S14, plus proposal R3/R4.
   A blanket "all help waits for R4 release" would contradict independent
   urgent help. OD-53 belongs to positive dispatch activation, not S15/S16.
   Reflection: explicitly exempt urgent help from the model/task-release
   dependency in the corrected descriptions. The proposal's grouped R4 row
   should state S16 follows S15 without making the human route wait.

## Evidence Log

* W1: https://github.com/jmservera/ama/pull/454#discussion_r4390263899,
  retrieved 2026-10-27. The one unresolved thread requests RB-18 -> RB-17.
* C1: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1126-1129`:
  S15 has an independent task-release gate; S16 explicitly depends on S13/S15;
  OD-53 is named for positive activation in S17.
* C2: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1149-1152`:
  S16 urgent help/referral works independently of the model.
* C3: `.copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md:91-94,123-125`:
  RB-18 gate wording and the shared RB-17/RB-18 graph row omit the edge.
  RB-19/RB-20 already retain their separate ordering and activation limits.
* C4: `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/resident-service-unregistered-proposal.md:704`:
  grouped R4 reconciliation lists task-release versus activation gates but
  does not spell out S16 -> S15.

## Findings, Alternatives and Decisions

Accept W1 and C1-C4 as sufficient documentary evidence. Correct the active
backlog in both tables and make the grouped proposal explicit. The PRD already
has the required edge and independent-help acceptance, so no PRD edit/version
bump or fresh full-PRD quality assessment is warranted. Historical inputs,
earlier FAIL outcomes and all unsigned/registration/acceptance gates stay intact.
Reject adding OD-53, removing task-release gates or blocking urgent help.
No remaining uncertainty affects this bounded correction. No further research
cycle is justified: all live tables and credible in-scope counter-evidence
have been checked.

## Planning Readiness

Ready. Research disposition: executed. All three questions have evidence
(ordering C1/C3, consistency C3/C4, independent help/no OD-53 C1/C2).
Artifact self-check: scope, extension provenance, cycle, evidence, alternatives,
decisions and readiness recorded. Parent continues to Plan automatically.
