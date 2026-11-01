# Issue 470 remaining criteria plan (2026-11-01)

Research: [research](../research/2026-11-01-issue-470-gate-benchmark-research.md)

* [x] Phase 1: reconcile issue criteria against merged PRs 475, 584, 669.
* [x] Phase 2: decide scope. Deliver evidence documentation only; no code, because criterion 4 needs an owner-authorised full benchmark.
* [x] Phase 3: validate. Documentation-only; Git diff review.
* [ ] Deferred, owner-gated: run the comparable full `--jobs 1` and `--jobs 4` gate pair using the runnable commands (required `--base` and a new external `--out` per run) in [Measuring full-gate scheduling](../../src/README.md#measuring-full-gate-scheduling). Keep criterion 4 open unless both comparable full runs pass receipt verification and the parallel run admits more than one worker; only then record both times in a PR, tick it and close.

Critique: single pass, no conflicting advice; the one decision (do not run the heavy benchmark) follows the confirmed user tier instruction.
