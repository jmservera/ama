<!-- markdownlint-disable-file -->
---
title: Fabric PR 558 correction phase details
description: Evidence boundaries and task completion expectations
ms.date: 2026-10-30
---

## Metadata

Task ID: 558-review-threads; slug: fabric-review-threads-558.
Plan: .copilot-tracking/plans/2026-10-30/fabric-review-threads-558-plan.md.
Research: .copilot-tracking/research/2026-10-30/fabric-review-threads-558-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete; ready for Review | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct evidence and navigation

Intent: repair statements without destroying dated original evidence.
Boundary: no application, infrastructure behavior, spending or deck edits.
Dependency: C1-C8/W1-W4 and one critique.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Append research qualifications and maintain assessment/KB

Targets: original 2026-10-29 data lane, infrastructure/governance lane and parent
research; docs/reference/research/microsoft-fabric-fit-assessment.md;
docs/reference/README.md and docs/reference/log.md.
Append dated qualifications to original research, naming original erroneous
claims and their corrected current reading, rather than rewriting the evidence
rows. Parent qualification must cover C9, Q5 economics, selected recommendation,
decision-changing test and implementation funding gate.
The maintained KB is updated in place and dated October30. Keep original
October29 product-source boundary distinct from new scoped source rechecks.
SQL comparison includes potential ongoing idle compute at the configured
minimum, independent of snapshot/log CPU/IO, and an authorized post-trial
verification of source change-feed cleanup, baseline settings and actual pause.
Do not claim W2 currently documents an automatic setting change: current
retrieval did not establish it.
Completion: claims trace to sources, original research bytes are prefixes,
index/log reflect material maintained assessment changes.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Repair historical evidence tables

Targets: fabric-rebase-558-review.md and fabric-rebase-558-plan-critique.md under
reviews/logs/2026-10-30 and reviews/plans/2026-10-30.
Change only Markdown destinations, not labels, outcomes or assessment text.
Tracking root is three directories up; repository root is four.
Completion: 24 and four links resolve and destination-stripped files are
identical to HEAD.

<!-- rpi:phase id=P02 -->
## P02: Validate, disposition and hand off

Dependency: P01. Validation evidence stays local/external or in dated changes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Checks and thread outcomes

Run from repository root with PYTHONDONTWRITEBYTECODE=1:
`python3 docs/capstone/pitch/cowork-main-presentation/build_assets.py --check-only --check-pptx docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`
and `python3 -m pytest docs/capstone/pitch/cowork-main-presentation/test_build_assets.py -q`
with external cache disabled. Only restore/install dependencies after an actual
missing-dependency failure. These checks cover current costs/source/native pages,
not the absent receipt. No new tests or verifier implementation.
Inspect changed/new Markdown links and anchors, exact historical prefixes,
destination-only repairs, ASCII additions, cadence arithmetic and git diff.
Changes table has eight actual unresolved database IDs and comment URLs,
status fixed or needs owner question, and exact correction/question.
Owner question requests exact commit/package containing source/validation.json,
its four canonical inputs, source guide, verifier and delivered deck to bind.
LF checkout policy is available, but no receipt or digest is fabricated.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile and prepare Review/local-closeout handoff

Reconcile all implementation markers, evidence and remaining boundaries before
Review. Completion means a ready handoff, not an already-executed Review/commit.
Fresh independent reviewer activates rpi-review, writes only its dated Review.
Review execution/outcome are separate and unresolved items routed later.
After Review, parent finishes the authorized local commit with authenticated
privacy-safe author/committer and exact Copilot trailer. Do not edit remote PR,
resolve remote comments, push, merge, or run cloud work.
Parent closeout requires recorded Review and local commit; missing receipt
remains explicit. Implementation completion evidence: all eight thread rows,
83 passing local links and source-preservation checks, successful existing
verifier and 24 regressions; changes/state/plan carry the same remaining limits.
Full publication gate, hosted/human acceptance and push remain coordinator-owned.
