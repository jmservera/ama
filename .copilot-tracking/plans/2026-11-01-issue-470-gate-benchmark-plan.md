# Issue 470 remaining criteria plan (2026-11-01)

Research: [research](../research/2026-11-01-issue-470-gate-benchmark-research.md)

* [x] Phase 1: reconcile issue criteria against merged PRs 475, 584, 669.
* [x] Phase 2: decide scope. Deliver evidence documentation only; no code, because criterion 4 needs an owner-authorised full benchmark.
* [x] Phase 3: validate. Documentation-only; Git diff review.
* [ ] Deferred, owner-gated: run `python3 tools/rpi-checks.py --all --jobs 1` and `--jobs 4` on the same base and host, record both times in a PR. Then tick criterion 4 and close.

Critique: single pass, no conflicting advice; the one decision (do not run the heavy benchmark) follows the confirmed user tier instruction.
