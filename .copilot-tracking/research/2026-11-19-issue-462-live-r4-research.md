---
title: Issue 462 live r4 research
ms.date: 2026-11-19
---

## Scope

Session `rpi-462-live`, task `issue-462-live-r4`. Owner decisions 2026-11-18: synthetic demo, desktop only, live Azure authorised in `ama`. Refs #462.

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Criterion status (from the 2026-11-18 r3 note and the live issue)

* Criterion 1 (RPI artifacts, threat model): proven by earlier notes; original October independent review not re-derived.
* Criterion 2 (#444/#455 resolved, failed rubric resolved): the first unmet criterion. r3 left it unmet because review thread `discussion_r4372517587` (High) on PR #455 is unresolved and its fix on main was never checked.

## Finding

Read-only `gh api graphql` on PR #455 confirms the thread is unresolved and not outdated: `resident_preview.py` line 509 compares `dataset_marker.get("fixture_id") != fixture_meta.get("id")`. When both identifiers are absent or null, `None != None` is false, so `safe_start` accepts an incompletely marked dataset/fixture pair. Main (HEAD 06188c533) still has the code; `test_refuses_unmarked_or_mismatched_files` covers only a mismatched string id, not missing or null.

## Decision

Implement the reviewer's fix in `src/core` (non-empty string identifiers required before comparing) with regression tests for missing and null identifiers. Source change in `src/core` takes the FULL tier classification; per the owner brief the full `--all` gate is not run, and the limit is recorded in the changes note.
