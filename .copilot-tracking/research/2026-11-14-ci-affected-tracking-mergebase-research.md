---
title: ci-affected tracking paths and merge-base diff research
ms.date: 2026-11-14
---

## Task

Refs #470. Task slug: ci-affected-tracking-mergebase. Research disposition: executed.

## Findings

* `select(files)` in `tools/ci-affected.py` returns `everything` for any path outside `src/` and `NAMESPACE_ONLY`, so `.copilot-tracking/**` (committed by every RPI PR) and docs widen CI to all projects plus mssql.
* `src-ci.yml` path filter watches only `docs/reference/research/retrofit-synthetic-data/**`, `docs/reference/research/chat-memory-dpia.md` and `docs/reference/research/ux/customer-journeys/residents.md` under `docs/`. Other docs Markdown is inert for CI.
* `changed_files` uses `base..head` (two-dot), which includes commits merged into base after the branch point.

## Decisions

* Skip `.copilot-tracking/` paths and inert `docs/**/*.md|.mdx` outside the watched paths. Non-Markdown docs, infra, workflows, `support/synthetic-data/`, `src/trivy.yaml`, unknown paths still select everything.
* Use `base...head`.

Planning Readiness: Ready. Validation tier: Focused (tool-only, no gate semantics weakening beyond the stated narrowing).
