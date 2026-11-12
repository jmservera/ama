<!-- markdownlint-disable-file -->
# Plan: five synthetic demo homes in the demo runbook (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Research: [research](../../research/2026-11-12/five-home-script-134-1112-research.md). Details: [details](../../details/2026-11-12/five-home-script-134-1112-details.md). Critique: [critique](./five-home-script-134-1112-critique.md). Base `origin/main` `d288b2a893a5a934f4357bbc7be79fa94ab59580`. DOCUMENTATION ONLY.

## Objective

Give the owner a demo script that names the five owner-selected synthetic homes with traceable ids and direct Workbench links, and states the owner-selected simplified operating mode as a TARGET, without claiming implementation, activation, availability or spend.

## Scope

In scope: [runbook](../../../docs/capstone/demo/runbook.md) (frontmatter date and one new section), an index pointer in [the index](../../../docs/reference/README.md), a log entry, these tracking artifacts, and a machine-readable handoff in the coordinator session files folder.

Out of scope and unchanged: all source, tests, infrastructure and workflows; API routes, the AI guard, telemetry storage, permissions; the #184 design proposal and earlier plans, adverse reports and observed/blocked histories; the cowork runbook; issues, board and PRs; any run beyond the read-only local replay already done.

## Phases

* [x] Research (executed; Planning Readiness Ready)
* [x] Plan (this file)
* [x] One critique pass (execution and disposition recorded separately)
* [x] Implementation
* [x] One Review (author, not independent), then stop

## Tier

Docs tier (focused): link, Markdown, Git diff and source-provenance review only. No runtime, full gate or CI claim. Independent exact-head Readiness review and hosted CI remain required before any publication and are not claimed.

## Design stance

* Label the operating mode (cadence, five-home scan restriction, single-instance start/stop, manual analysis) as OWNER-SELECTED TARGET until implementation is verified, and the eight-hour limit as a later recommendation. The five ids are replay-selected by a stated mechanical rule, not owner-picked.
* Preserve old statements as dated history; the runbook currently contains none that conflict, so the new section states the supersession of the every-open-case scope as an owner selection in the target mode only.
* ASCII, `*` lists, no em dashes, no bold-prefix items.
* Preflight before live use: ids exist in the chosen build, state is open, sensors exist, cohort lists them. Fixture selection is not deployed acceptance.
* Links: documented employee origin with the exact route; sign-in required; no availability claim.
