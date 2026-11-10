<!-- markdownlint-disable-file -->
# Plan critique: nomination and UX integration wave checkpoint (#440, 2026-11-10)

Single critique of the final candidate plan, executed once by the author (self-executed, not independent). Plan: [plan](../2026-11-10-nomination-ux-main-440-1110-plan.md). No significant or divergent issue needs a user decision; compatible findings are applied directly as amendments A1 to A6 in the plan.

## Verdict

Proceed with amendments. No finding conflicts with a confirmed decision.

## Findings

* A1 (Medium): the hosted "19 checks SUCCESS" and "MERGEABLE" facts are PR-head metadata, while commit-scoped runs for `65c2ab9d9` showed only 7 runs, one still in progress. The record must label them current-metadata, never a result for the merge commit.
* A2 (Medium): Root's #1384 wording (current exhaustion proven 4, missing-global 2, whole browser not green) is Root-supplied; the issue body only says the red-before is not yet instrumented. The record must attribute it to Root's later diagnostic, not claim this task reproduced it, and must not state the whole workspace browser check is green.
* A3 (Medium): #1383 shows a rubric scorer FAILED comment for `901fea60e`. Later rubric-only commits on `main` do not prove recovery. The record states the incident is OPEN and recovery unproven by a later overall SUCCESS alone, with no invented closure.
* A4 (Low): the 5-empty and 2-populated split of the 21 empty-queue lines was not re-derived by Root; the record must repeat that, not state the split as observed.
* A5 (Low): the nomination browser output contains law-store-unavailable, 503 and disconnect lines while passing; the record must not say zero server errors.
* A6 (Low): the old CSV-learning record may land first; this record must use a unique heading, unique index paragraph and unique log entry and say it neither includes nor republishes that record, with any later append-only conflict resolved by Root preserving both entries.

## Disposition

All six are applied directly to the plan constraints; no re-critique and no user question. No other change to the phase structure.
