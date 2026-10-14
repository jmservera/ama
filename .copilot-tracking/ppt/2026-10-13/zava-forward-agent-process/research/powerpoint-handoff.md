<!-- markdownlint-disable-file -->
---
title: Agent process diagram handoff to PowerPoint Builder
ms.date: 2026-10-13
status: Supplied content and bounded update contract
---

## Task and supplied content

The owner asked: generate a nice diagram showing how the agents fit into the
process, how they are used, when they work proactively and how they improve the
process, then hand it to the PowerPoint agent for the capstone deck.

The parent has completed topic/source investigation and authored the diagram.
This is not a new research request. Use supplied content; do not launch a fresh
RPI research workflow or additional topic experts. Use the powerpoint skill
and a minimal PowerPoint Subagent execution lane for deck build/validation.

Repository/worktree: /home/azureuser/source/ama-wt-zava-challenge
Branch: docs/draft-experiment-closure; continuing open PR #68.
Working root: .copilot-tracking/ppt/2026-10-13/zava-forward-agent-process/
Immutable starting copy: slide-deck/source.pptx, 21 slides, 13.333 x 7.5.
Canonical delivery to be replaced by the parent only after validation:
docs/capstone/deck/zava-forward-executive-draft.pptx
Output: slide-deck/zava-forward-executive-draft.pptx
Report: changes/powerpoint-agent-result.md

Ready-to-use illustration:
* docs/capstone/deck/agents-in-retrofit-process.svg (editable vector source)
* docs/capstone/deck/agents-in-retrofit-process.png (3200 x 1800)
* research/diagram-contract.json (all five capabilities, labels, authority,
  source references and measured text geometry)

Style reference and reproducible prior content:
.copilot-tracking/ppt/2026-10-11/zava-forward-executive-draft/content/
Cream #F7F2E7, forest #183A31/#173F35, moss #D5E2D4, gold #E5B96A.
The diagram uses the existing visual palette. Avoid a whole-deck redesign.
Existing slide 12 distinguishes closed-set supplied-source selection from
cited generation and must be retained, including its notes and caveats.

## Required deck update

Add exactly ONE diagram slide immediately AFTER existing slide 12 and before
existing CFO slide 13. New slide number 13; final deck 22 slides. Do not replace
or discard existing slides. Use the canonical current deck/source.pptx, not an
older unpublished working deck. Preserve existing slides, masters, layouts,
logos, shapes, notes and image relationships; only renumber visible footer
counters on moved slides if needed. No other narrative rewriting.

Author new content YAML before building. A PNG placement is acceptable, with
accessible alt description and a complete text equivalent in speaker notes.
If creating native shapes improves readability, retain exact semantic content
and source/authority boundaries. Avoid content-extra script bypasses. A safe
staging copy with one inserted blank slide, followed by --source/--slides 13,
is acceptable; never --template a partial update. Verify original 21 plus the
one intended added slide, and make slide 13 titled "Five assists. One controlled
journey." with explicit proposed-design status.

Use a short 45-60-second suggested talk track, not a claimed timed rehearsal.
Speaker notes must explain:
* Stock: explain sourced candidates; proactively flag new conflicts/missing
  facts. Data owners verify; Assets approves policy. AI does not rank or change
  queues. Measure reconciliation effort/critical conflicts and viability.
* Assessment: sourced survey/design pack; changed/stale evidence goes to named
  review. Assessor and coordinator sign independently. No invented site facts.
  Measure returns/rework and assessment-to-ready time.
* Grant/funding: source-linked draft; changed terms/missing evidence go to
  Finance. Rules calculate eligibility/totals; Finance validates, approves and
  submits. It spans planning through later claim/cash; award is not receipt.
  Measure pack rework, first-time acceptance and time-to-claim.
* Contractor/resident coordination: draft updates and committed-capacity slot
  suggestions; unaccepted handoffs and missed updates create owned review.
  Resident chooses measures; Programme/contract authority releases/instructs.
  No automatic messages, inferred consent or autonomous scheduling.
  Measure coordination effort, failed visits and unowned handoffs.
* Quality: assemble evidence and raise missing/conflicting evidence for
  independent QA. Flags never clear holds, accept work or close defects.
  Measure evidence rework and missed critical defects.
* "Proactive" is a PROPOSED permitted event/scheduled task after deterministic
  eligibility checks, not evidence that all watchers are deployed. Only
  registered/source-permitted tasks, proposals/raise-only flags to owned human
  queues; source/version changes stale dependent review. Rule-only/manual path
  remains available on model failure or inappropriate task.
* Workflow core owns identity/field rights, versions, deterministic gates,
  human approvals, audit, retries/manual recovery. It is not a sixth supervisor
  agent. Any hazard goes directly to human safety service; model output cannot
  suppress intake or change its separate clocks.
* Intended improvements are hypotheses. Compare rules/manual with assisted
  work on paired cases, count preparation/review/correction effort, critical
  errors, latency/cost and uncertainty. Current live inference is narrow
  feasibility, not proof of every capability, calibrated quality or value.

Evidence to cite in notes (all repository-local, no new legal claims):
* docs/case_study_48_addendum.md, Digital Foundation / Where Agents Fit /
  Agentic Architecture Brief / Decision 1 in Application Design.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md, AI Model Selection
  and Evaluation Harness / Bounded-Agent Orchestration Pattern.
* docs/reference/research/company/agent-request-challenge.md, Summary and each
  capability's value test.
* docs/reference/research/gap-analysis-next-build.md, Draft Experiment Closure:
  #58 features/source are not automatically in the current deployment.

## Execution and validation constraints

NO uv: company policy. Reuse existing dependencies with
PYTHONPATH=/home/azureuser/.copilot/session-state/1e0d58ea-7ea9-4c65-93b7-66c89c481468/files/zava-script-libs
python3 ...
Skill scripts:
/home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/experimental/powerpoint/scripts/
LibreOffice and pdftoppm are available. Use direct Python scripts, not a
wrapper which installs uv. Do not install dependencies unless a chosen
command fails for a missing module. Existing PNG eliminates cairosvg need.

All writes/builds/exports/logs stay in working root. Do NOT modify canonical
PPTX, documents, protected case/memory/regulatory snapshots or live services.
No Azure/M365 calls, Git commit/push, PR edits/merge, resource teardown or
unnecessary agents. The parent owns publication and outside-root docs.

Validate new slide and both neighbors (12,13,14), plus all-slide notes/count
and preserved original content. Export fresh PDF/JPG and inspect actual images
for clipping, crowding, footer/logo collisions and readability. Use available
native view/vision. Do not call missing SDK/model setup a Passed vision lane.
Record executed checks and explicit Deferred/Unavailable lanes distinctly.

Check the changed contribution against full capstone rubric, especially
A1/A3/A6/A7 and B1/B2/B6/B7: readable one idea, bounded autonomy, source labels,
proposal/deployment distinction, value tests and human approval clarity.
No invented score, simulated staff validation or panel-ready declaration.

Return status complete/partial/blocked, output path and slide count, source and
output SHA256, changed-slide/neighbor images, exact validation findings and
execution log. No success without a usable persistent output.
