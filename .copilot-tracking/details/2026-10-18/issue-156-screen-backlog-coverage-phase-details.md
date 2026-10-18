---
title: Issue 156 screen backlog coverage phase details
description: Bounded execution and evidence expectations for each plan task
ms.date: 2026-10-18
---

Task ID: `issue-156-screen-backlog-coverage`.
Base/source: `2ca6d1c48bb95b65e6c349fe508e99c00a74efbe`.

## P01-T01: Snapshot and traces

Source C1-C5/W1-W2 in the new research. REST fetched with pagination includes
all issue states and excludes PR objects; 184 matches supplied 500-limit export.
Snapshot retrieval complete before 2026-10-18T04:13:45Z. Preserve exact all-state
IDs and open/closed states in grouped membership rows and individual traces.
Use exclusive classification:

* includes-screen: explicit visible interaction/content/state or screen impact;
  encompasses planned, delivered and cross-cutting patterns, not just new pages.
* no-screen: inspected scope prescribes backend/data/tests/research/docs/infra,
  not an additional application screen. Does not deny dependencies on screens.
* epic-covered: sixteen aggregate epics routed to feature classifications;
  "covered" means inventory routing, not delivery/acceptance.
* unknown: #121/#125/#126/#127/#187/#189/#213/#222 lack a declared screen versus
  report/CLI/manual route. Each needs a precise role/surface choice, not an
  unreviewed residual or inferred approval.

Known screens: 74, 57 open/17 closed. No-screen: 86, 59 open/27 closed.
Epics: 16 open. Unknown: eight, seven open/one closed.
Use one trace row per issue; exact section links can be shared through Markdown
reference definitions. Issue acceptance criteria are check provenance and may
remain unexecuted. For reused T/C rows name exact row and partial match;
H/E never become current design acceptance. For missing feature flow, use
NOT SUPPLIED rather than a broad architecture/PRD link masquerading as a flow.

## P01-T02: KB integration

Insert continuation in existing synthesis, preserving original fifteen rows,
decision register and G156 record. Update earlier present-tense unknown coverage
sentence with a dated pointer, retain historical findings. Update existing index
entry and append dated log. Existing ms.date already 2026-10-18; retain date.

## P02-T01: Checks

Temporary/session script extracts new classification IDs from Markdown and
compares against independently loaded REST/export IDs and the frozen expected
membership in Research. Require zero per-issue classification mismatches, exact
trace-ID/includes-screen set equality (zero missing/extra), no duplicate or
overlapping IDs, exact eight-unknown set and sixteen evidenced epic routes.
Count states, classes,
unique trace rows, missing-field sentinels and all named edge cases. Resolve all
introduced local Markdown files/anchors and table shape; check H/E git objects
at exact pins, original T/C rows/register/gate and all prior tracking bytes
against base; `git diff --check`.
No repository-wide documentation build exists; inspect actual workflow/tool
definitions rather than assume CI success. No added tooling or dependencies.

## P02-T02: Original Review

Fresh independent agent activates rpi-review, reads user boundary, exact candidate
diff, plan/details/research and check evidence; writes only designated original
Review. It independently reconciles complete membership/classification and trace
sets against accessible source projection/bodies, including the four
count-preserving critique disagreements, plus representative named edge cases.
Temporary source evidence path is recorded in Research; remove after review.
No second/amended Review, no self-Pass.
If Not accepted, preserve locally, commit freeze and stop for coordinator routing.

## P03-T01 and P03-T02: Finalization

Changes record captures actual diff/checks, critique dispositions, divergences,
remaining gaps and original Review. Persist state immediately before and after
phase transitions. Fresh `gh api user` id/login builds repository-local privacy-safe
author/committer email; commit own docs and all new artifacts, Copilot trailer.
Accepted Review permits ordinary push and main PR with Refs #156, not closure.
Do not modify issue ACs, boards or merged #400 records.
