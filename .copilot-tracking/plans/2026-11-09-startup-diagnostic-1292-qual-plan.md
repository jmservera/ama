---
title: Issue 1292 startup diagnostic record qualification plan
ms.date: 2026-11-09
task_id: 1292-startup-diagnostic-qual-1109
---

## Task metadata

* Research `.copilot-tracking/research/2026-11-09-startup-diagnostic-1292-qual-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-startup-diagnostic-1292-qual-details.md`. Critique `.copilot-tracking/plans/2026-11-09-startup-diagnostic-1292-qual-critique.md`.
* Branch `test/demo-startup-diagnostic-1292-1109`, frozen `59accfa1ca9be77f2e98faf5ef862deba76cf941`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`. Preserve the base; do not merge or rebase `origin/main`, stack, push, open a PR or close anything. Refs #1292 only.

## Requirements

* Add one new dated qualification (changes record) addressing only RQ-1..RQ-4, the observer-safety wording and provenance. It supersedes, with date and without backdating, the timing overclaims in the original changes, review and external handoff.
* Original authored records, raw evidence and original handoff remain unchanged byte for byte (verified by blob equality and `sha256sum -c`).
* No source, harness or test edit; no run of any test, suite, SQL, browser, stress, model or cloud action; no cleanup. Validation: diff, link and ASCII review plus read-only git and hash checks.
* Provenance to record where genuinely obtainable: head, tree, base, unchanged `src infra tools .github pyproject.toml` diff, 8aea86f8 ancestry, record blob hashes, 29-member raw manifest verification and manifest hash. State unavailable FR1 claims explicitly.

## Phases and criteria

* QC-1 R2 reworded as a proposed, unperformed diagnostic; neither condition has been established as necessary or sufficient.
* QC-2 3.05-3.25 s upper bound, backfill wrapper 1.10-1.17 s, 1.80-2.03 s non-COMMIT-duration, no return event, waiter possibly in an earlier migration, 1.6x heuristic only.
* QC-3 5 s SQLite busy timeout distinct from `errors == []` plus `elapsed < 20.0`; no proved deadline defect.
* QC-4 unittest durations versus process wallclocks; all under 180 s.
* QC-5 recorder claim limited to no observed observer error.
* QC-6 provenance and unavailable claims. The raw manifest proves member integrity against itself only; no trusted original manifest hash exists, so only its present hash and the 29 member matches are recorded, with that limit stated. Original records and the external handoff are compared with baseline sha256 values captured before and after.
* QC-7 counters (E5 not spent, one productive correction remains, H1-H4 unknown) and unchanged originals.
* Order: commit research, plan, details, critique and state first; then write the qualification; then one authored Review; then update state; commit. Branch is local only.
