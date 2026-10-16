<!-- markdownlint-disable-file -->
# RPI Phase Details: Historical climate source

Task ID: 178. Task slug: climate-source-178.
Plan: .copilot-tracking/plans/2026-10-16/climate-source-178-plan.md.
Research: .copilot-tracking/research/2026-10-16/climate-source-178-research.md.

<!-- rpi:phase id=P01 -->
## P01: Publish bounded offline evidence

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update source decision and acceptance audit

Target: docs/reference/research/iot-sensor-analytics-research-plan.md.
Preserve earlier dated findings and distinguish the historical-source issue
from the existing method research. Candidate product descriptions must remain
unverified investigation questions where no retrieved source supports them.
Do not state guessed coverage periods, resolution, OGL or humidity availability.
Record no external climate retrieval date and no actual observed bounds.
Evidence: issue owner comment and source/test declarations in C1-C4.
Completion: three explicit issue-criterion audit rows and exact missing packet.
Blocker: actual records/licence/owner confirmation unavailable.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Connect maintainer documentation

Targets: src/core/README.md, docs/reference/README.md,
docs/reference/log.md. Link the source decision from the existing generator
description; add a routing row and append a dated log entry.
Dependency: P01-T01. No memory or regulatory snapshot changes.
Completion: working relative links and accurate synthetic-only limitations.

P01 completion: both tasks complete. The source register and three unmet
criteria exist; index/core links added and log appended, with generator and
tests unchanged.

<!-- rpi:phase id=P02 -->
## P02: Validate and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validate and record review

Read the changed Markdown, inspect diff, check new relative links and
`git diff --check`. No new tools/dependencies. No application code changes:
tests, Ruff, mypy, app run and live-platform checks not applicable/not run.
Review exactly once; route unresolved source evidence as future work.
Completion: changes and review artifacts with honest criterion dispositions.

Validation complete: five new relative links/anchors resolve, log append
preserves its original prefix, diff whitespace passes and canonical change
scope is exactly four documents. One Review recorded: execution Complete,
outcome Not accepted for full issue delivery; RV-001 routed to later research.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit, push and create PR

Dependency: P02-T01. GitHub identity already resolved as login jmservera and
ID 8036360; construct repository-local noreply email. Stage only explicit task
paths, commit with required trailer, push without force and create PR against
main with Refs #178. Do not modify issue criteria. Verify remote commit/PR.
