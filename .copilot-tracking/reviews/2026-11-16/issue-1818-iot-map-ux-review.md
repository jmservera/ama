---
title: Issue 1818 review
date: 2026-11-16
task_id: issue-1818
---

## Execution

One independent `code-review` pass over the working-tree diff (executed once, not repeated).

## Outcome

Conformant with the FOCUSED tier after one fix. No material finding remains open.

## Findings

* Medium, fixed: `Assistants.map_sensors` authorised every mapped point (up to 500, two queries
  each) before the 100-home cap applied. It now authorises at most `HOME_CAP` homes and marks the
  rest `not-loaded`. `test_map_sensors` re-run: 13 tests pass.

## Routed follow-ups

* Batch the per-case authorisation into one scope check (efficiency, not correctness).
* Re-run `checks.map_fullscreen_browser_check` on a quiet host; this host showed timing flakes that
  also affect the baseline commit.
* Live Azure IoT Hub walkthrough criterion stays unticked (separate live transport record).

## Boundary

Local candidate only. Hosted CI, the complete local gate and human approvals did not run.
