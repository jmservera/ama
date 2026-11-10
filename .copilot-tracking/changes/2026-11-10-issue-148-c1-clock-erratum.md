<!-- markdownlint-disable-file -->
# Erratum: unobserved "Readback" times in the original issue 148 records

Additive correction C1. The original files below are unchanged and keep their original outcomes and the coordinator's adverse finding. Plan: [C1 plan](../plans/2026-11-10-issue-148-c1-clock-plan.md).

## Withdrawn claims

Each "Readback" time below was not observed at the moment of writing and is withdrawn. No replacement time is offered.

| Original file | Claimed time | Status |
| --- | --- | --- |
| [research](../research/2026-11-10-issue-148-four-images-research.md) | 2026-11-10T01:21Z | Withdrawn, unobserved |
| [plan](../plans/2026-11-10-issue-148-four-images-plan.md) | 2026-11-10T01:30Z | Withdrawn, unobserved |
| [details](../details/2026-11-10-issue-148-four-images-details.md) | 2026-11-10T01:30Z | Withdrawn, unobserved |
| [critique](../plans/critiques/2026-11-10-issue-148-four-images-critique.md) | 2026-11-10T01:33Z | Withdrawn, unobserved, later than the commit holding it |
| [changes](2026-11-10-issue-148-four-images-changes.md) | 2026-11-10T01:45Z | Withdrawn, unobserved, later than the commit holding it |
| [review](../reviews/2026-11-10-issue-148-four-images-review.md) | 2026-11-10T01:47Z | Withdrawn, unobserved, later than the commit holding it |

## Commit provenance only (not phase times)

| Commit | Author and committer time |
| --- | --- |
| `c9fa753f31f4983142c88cc5875c1f9e04042090` (prospective records) | 2026-11-10T01:22:25+00:00 |
| `d305d0f90512fe448caf99b8520811660c2305cb` (implementation and later records) | 2026-11-10T01:23:47+00:00 |

These are Git commit timestamps. They do not date when research, plan, critique, implementation or review actually ran; no exact phase wall time was captured.

## Ancestry

`git merge-base --is-ancestor c9fa753f3 d305d0f90` succeeded, so the prospective plan commit precedes the source commit by ancestry. The original plan, details, critique and research are in `c9fa753f3`; the source change is only in `d305d0f90`.

## Product unchanged

Targeted results at `d305d0f90` (112 orchestrator tests, zero skips, Ruff, format, mypy) apply only because the product tree is identical; none were rerun in C1.
