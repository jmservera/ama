---
title: Issue 1204 exact schedule prompts changes
description: Changes record for the coordinator schedule prompt persistence continuation
ms.date: 2026-11-17
---

## Changed source

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`, Recurring schedules section only: provenance bullet extended; Startup and restart bullet; Honest limit bullet; new "Approved prompt snapshots (2026-11-17)" subsection with the delivery (historical id 5) and cleanup (historical id 2) bodies verbatim in `text` fences. 35 insertions, 1 deletion (the provenance bullet's last line, reworded to continue).

## Validation (FOCUSED)

* Extracted fenced blocks equal the approved strings: delivery True (2601 chars, SHA-256 4b27fc53ce297391b95d2197f11830e34c19514f5e294c49be63b3ff8f6fd25f), cleanup True (617 chars, SHA-256 fa5c65209141c539609c298d9783367cd9d05e96b46e88e5f7f768313c137a3b). Result file: external evidence `equality-result.txt`.
* No non-ASCII added; frontmatter and `tools`/model untouched; only one tracked source changed (full status checked, untracked are issue-owned `.copilot-tracking` artifacts).
* Full, browser, SQL and hosted gates not run (owner-approved prompt-only exception); hosted checks and independent review remain coordinator-owned before merge.

## HVE

Mode improve. Author classification Medium; the independent Review judged it Major, which supersedes it. Behavior gate: not satisfied-and-skipped; `hve-builder-tester` not run, behavior verdict Not available, HVE outcome Deferred (see review). No native scheduling behavior is claimed or simulated. Static review: the original Review (Revise).

## Post-review corrections (unreviewed)

F1 (delivery match requires current cleanup handle), F2 (zero/two repair only while authorized), F3 (dated provenance wording) applied after the Review. Equality re-verified: both blocks True; final diff 43 insertions, 4 deletions; no non-ASCII added.

## Divergences

None from plan. Critique findings PC-001 (exactly-one only while authorized) applied in the bullet.
