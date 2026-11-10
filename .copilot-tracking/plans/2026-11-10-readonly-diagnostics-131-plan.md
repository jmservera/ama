---
title: Issue 131 read-only diagnostics of independent REVISE findings plan
ms.date: 2026-11-10
task_id: 131-readonly-diagnostics-1110
---

## Objective

Reproduce, with the smallest owned synthetic fixtures, the two Medium independent findings (malformed inventory history can look valid; ambiguous identity and Unknown route omitted from refusal reasons) and attribute the configured typing and format failures to base or candidate. No product or test fix and no Source Correction grant. Research: [research](../research/2026-11-10-readonly-diagnostics-131-research.md). Details: [details](../details/2026-11-10-readonly-diagnostics-131-details.md).

## Phases

* [ ] Phase 1: Probe A and Probe B through the actual candidate module (two functional probes, JSON `Store` and SQLite `SqlStore`).
* [ ] Phase 2: One baseline comparison of configured mypy and `ruff format --check .` on an owned export of `fe59ef56a0084dd975fd7e5c342670bb8f788fb0` with the pinned tools.
* [ ] Phase 3: Re-run the unchanged candidate configured checks once for same-tool comparison and confirm candidate source equality with `7f8af9b`.
* [ ] Phase 4: Review once, commit only new RPI records, witness, owned scratch cleanup and handoff with a one-batch fix proposal for a future authority.

## Stop rules

* Stop and record a diagnostic if a probe cannot run, is not reproduced, or any witness event is refused. No blind retry, no backfill.
* Maximum two functional probes and one baseline comparison.
* No edit to the product source, tests, READMEs, configuration or the immutable original records. No candidate checkout or mutation, no other worktrees or venvs. No silencing, grep filtering of results, ignores, config excludes, `Any` casts or reformatting.
* Install only on a new missing-dependency failure into the owned venv.

## Success criteria

* Each finding is labelled confirmed, unreproduced or static-only with raw output, distinguishing the supported API path from corrupt-store injection.
* `TENURE_HOLD` is never released in any observation.
* Typing and format counts are stated as introduced or baseline only where the same pinned tool run on the base shows it.
* Product source stays byte-equal to the `7f8af9b` tree.
