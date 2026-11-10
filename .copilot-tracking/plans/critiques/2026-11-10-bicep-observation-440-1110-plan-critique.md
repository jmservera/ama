<!-- markdownlint-disable-file -->
# Plan critique: Bicep public-simulation current-main observation (#440, 2026-11-10)

Single critique of the final candidate plan, executed once by the author (self-executed, not independent). Plan: [plan](../2026-11-10-bicep-observation-440-1110-plan.md).

## Verdict

Proceed with amendments B1 to B6 recorded in the plan and applied directly. No finding conflicts with a confirmed decision; no user decision needed.

## Findings

* Medium: the 19 hosted checks are PR-head metadata and Root-reported; do not present them as a result for the merge commit.
* Medium: the lock-busy exit 1 attempts, the old image and the three unwaived mypy errors must stay visible; no all-infra or all-process pass.
* Medium: seal wording must keep the retained-pair versus replaced-pair distinction and claim no cross-restart runtime test.
* Low: the image id is a manifest identity; the local candidate for #89 is not main; the NomUX and Bicep gates differ.
* Low: unique heading, index paragraph and log entry so the NomUX and CSV-learning records are neither included nor altered.
