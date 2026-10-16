---
title: CI infra dependency correction details
description: Evidence and completion expectations for the bounded correction
ms.date: 2026-10-16
---

Task: 138-ci-pyyaml. Parent: cicd-deploy-pipeline-138.

## P01

* P01-T01: Current worktree initially clean; branch matches open PR 357.
  Main contains one new commit. Merge without rewriting history; if the log
  conflicts, keep complete entries from both sides without rewriting either.
* P01-T02: Match source CI's existing `PyYAML==6.0.3` immediately before
  the validate infra test command. Assert both consumers install before
  discovery. Exercise dependency removal on deep-copied workflow documents.
  Preserve every existing unsafe workflow-control mutation.
* P01-T03: Complete quality-gate recipe currently omits the dependency.
  Document test-only scope and isolated-venv reproduction followed by explicit
  pinned prerequisite. Update existing reference routing and append log.

## P02

* P02-T01: Fresh `/tmp/ama-138-clean-e18c47d4` venv already reproduces one
  import error across 131 discovered tests. Install pinned test dependency
  there, rerun exact discovery, and run pipeline-targeted mutations plus
  Ruff/format and helper mypy. Existing pipeline test launches the installed
  API with synthetic data; do not read private data.
* P02-T02: One review assesses only this correction and integration diff.
  Record any unexecuted checks, no live claims, and all six unmet issue criteria.
* P02-T03: Resolve GitHub identity, use repository-local privacy-safe email,
  include required coauthor trailer, commit and push without force.
  Update existing PR rather than opening a duplicate. Do not merge PR or
  mark issue criteria complete.
