---
title: Resident chat routing phase details
description: Completion contracts and evidence boundaries for the routing fix
ms.date: 2026-10-31
---

Task ID and slug: resident-chat-routing.
Plan: `.copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md`.
Readiness: Ready after direct PC-001/PC-002 disposition; original Revise retained.
Execution: P01/P02 complete; three added methods, 90 focused tests and pinned
Ruff/mypy pass. P03 remains parent-owned independent Review/publication.

<!-- phase:P01 -->
## P01: Routing and copy

<!-- task:P01-T01 -->
### P01-T01: Bounded natural question fallback

Research C1-C5: exact legacy grammar already owns many useful queries. Retain it.
Normalize typographic apostrophes only within the fallback. Require allowed
whole-message characters/terminal punctuation and an ordered per-topic
keyword/intent grammar consuming the entire message. Token sets and anchor
presence alone are insufficient. Documents/forms must require an explicit
receipt/missing/help intent rather than route arbitrary text containing nouns.
Status needs own case/retrofit plus progress/waiting/update/blocking intent.
Home needs own home/address plus recorded-location/information intent.
Existing exclusion and specialist code remains untouched. Unknown words and
mixed requests must fail closed, even without known forbidden words.
Completion: reported and natural question matrix maps to existing `Topic` values
or home without changing core answers or activation.

<!-- task:P01-T02 -->
### P01-T02: Useful refusal

Research C6: keep truthful reason and housing-officer next action. Add four
examples for case progress, documents, forms and home address. Keep source
"Assistant task limits", advisory notice and action prohibition.
Completion: unknown HTTP response names supported questions and manual help.

<!-- phase:P02 -->
## P02: Regression evidence and documentation

<!-- task:P02-T01 -->
### P02-T01: Existing test module

Add no more than three methods and shared matrices in `src/api/tests`.
Check exact rules answer/sources against explicit topic, constructed C-1/C-2
isolation, no actions, no callbacks and no advisor invocation.
Adversaries include cross-person queries, other case IDs, approval/decision/
booking/instruction requests, unknown suffixes, mixed categories and markup.
Append the natural matrix to the complete-recognized-message regressions so
newly recognized phrases inherit every existing suffix/prefix protection.
Include "How is my case going what is my case status", "How is my case going
my case" and corresponding repeated document/form/home anchors and questions,
using only admitted words. A full character check alone cannot reject them.
Keep all original tests and fake data. Real HTTP loopback is constructed local
evidence, not a deployed service or actual resident acceptance.

<!-- task:P02-T02 -->
### P02-T02: Focused checks and README

Document finite matching and task limitations in the existing resident-chat
section. Run the plan's exact unittest/Ruff/mypy commands from `src/api`.
Do not acquire/wait on the shared heavy lock. Capture failures before correction,
tool versions, commands, counts and exits in the changes artifact.
No web edit means browser/design-skill review is outside this change.

<!-- phase:P03 -->
## P03: Independent Review and publication

<!-- task:P03-T01 -->
### P03-T01: One independent Review

Fresh worker reviews the final diff and original plan/evidence. Allowed writes:
only `.copilot-tracking/reviews/logs/2026-10-31/resident-chat-routing-review.md`.
Record execution and outcome separately; do not fabricate human acceptance.
Findings route to later work, not another Review in this task. An unresolved
material acceptance finding blocks publication; nonblocking residuals require
explicit disposition. Never treat Review execution alone as approval.

<!-- task:P03-T02 -->
### P03-T02: Exact candidate publication

Use GitHub-resolved repository-local noreply author/committer identity and the
specified co-author trailer. Commit only scoped files and original RPI evidence,
fetch current main, verify focused checks against the committed clean candidate,
push `git push -u origin HEAD` without force and open a PR to main.
Body uses Refs #520 and Refs #563 and states no AI activation/deployment.
Hosted checks and owner merge decision remain outstanding, not bypassed.
