<!-- markdownlint-disable-file -->
---
title: Rubric Model Pilot Plan
description: One-run-per-model comparison within the approved USD 10 allowance
ms.date: 2026-10-24
---

## User Requests

* Continue suggested work item 2: compare cheaper models with approved budget.
* Approved choice: USD 10 pilot, one run per model, report only.

## Scope and Dependencies

Follow repository instructions, Python/Markdown conventions and existing
rubric contracts. Preserve the presentation branch, Office lock file, source
scorer, baseline, model and remote state. Use the existing virtual environment,
Copilot CLI and production prepare/adapter/gate functions. No new production
dependency or billable retry. Research is recorded in
.copilot-tracking/research/2026-10-24/rubric-model-pilot-research.md.

<!-- rpi:phase id=P01 -->
## Freeze and Prepare

<!-- parallelizable: false -->
* [x] Record one source SHA and frozen input manifest.
* [x] Create isolated baseline-hidden read-only scoring inputs.
* [x] Verify local runner and output validation without inference.

<!-- rpi:phase id=P02 -->
## Execute Pilot

<!-- parallelizable: false -->
* [x] Sonnet 5: one explicitly pinned invocation.
* [x] Haiku 4.5: one explicitly pinned invocation if budget permits.
* [x] GPT-6 Luna: one explicitly pinned invocation if budget permits.
* [x] Retain usage and timing, including errors; do not silently substitute.

<!-- rpi:phase id=P03 -->
## Review and Discover

<!-- parallelizable: false -->
* [x] Validate full scorecards and compare all 20 criterion values.
* [x] Record local gate decisions, measured cost/time and validity.
* [x] Document limits, recommendation and next-work choices.

## Acceptance

At most one assessment invocation per named model; aggregate pilot spending
within the approved allowance with soft-limit headroom. Report unavailable or
invalid results honestly. No live score submission, production change,
commit, push or workflow dispatch. Planning details and deviations belong to
.copilot-tracking/details/2026-10-24/rubric-model-pilot-details.md and
.copilot-tracking/plans/logs/2026-10-24/rubric-model-pilot-log.md.

<!-- rpi:phase id=P04 -->
## Native Submission Extension (2026-10-24)

The owner explicitly approved one additional native-MCP invocation each for
Haiku 4.5 and GPT-6 Luna, using the USD 9.61368924 remaining within the original
USD 10 total. This supersedes the original no-further-invocations boundary for
these two invocations only. Original results and invalid cards remain intact.

<!-- parallelizable: false -->
* [x] Verify pinned runtime blobs and actual stdio/HTTP regressions: 7 passed.
* [x] Prepare generated-schema MCP servers with isolated local append files.
* [x] Run one Haiku invocation; preserve tool rejections/corrections and usage.
* [x] Run one Luna invocation if cumulative usage remains within allowance.
* [x] Validate exactly-one appended cards through the unchanged strict gate.
* [x] Record native transport limitations, complete costs and recommendations.

No output-handler jobs, GitHub writes, score publication, production changes,
fallback or repeated assessment invocation are authorized. A rejected MCP call
may be corrected within its single invocation only if nothing was appended.
