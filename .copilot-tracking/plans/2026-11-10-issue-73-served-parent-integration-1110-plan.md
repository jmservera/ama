---
title: Issue 73 served parent integration of child 1357 with current main - plan
ms.date: 2026-11-10
---

## Scope

* Integrate pinned origin/main 4244e84e763e6e01dd6012fcb9b650dae8d58e9d into parent b0af68a3 with one ordinary merge (no squash, rebase, amend or force). Preserve main's discovery-demo CLI and the child's import-transfer CLI, scoped register, rollback/idempotency and optional-driver typing override.
* Not in scope: features, source relaxations, role or eligibility decisions, settings, workflows, protection, cloud or real AI, #111/#132/siblings, correction balance changes.
* Tier: owner DEMO TARGETED (not full, not --changed).

## Phases

* [ ] P1 Plan, details, one critique, record plan-done witness event.
* [ ] P2 Open the changes record, record implement-start, then merge main (only after P2 start). Resolve only real conflicts; none predicted.
* [ ] P3 Targeted validation V1-V9 on the merged tree, raw logs in /tmp/issue73-1110-scratch/logs.
* [ ] P4 Docs: append one docs/reference/log.md entry (append-only); no other doc change unless validation shows drift.
* [ ] P5 record implement-done, one Review, record review-done, commit with privacy-safe email, record commit-complete with the actual head.
* [ ] P6 Handoff at ROOT/handoff-73-served-parent-integration-1110.md with witness verify. No push, no PR.

## Validation matrix (details file holds exact commands)

* V1 Core: discovery demo tests, import refusals, exception register/queue/feeds, sqlstore and governance suites with JSON/SQLite restart and idempotency.
* V2 Importer: full discover (79 baseline) including CLI parser/transfer regressions.
* V3 API: exception register, register screen, role screens, workspace scripts, workbench.
* V4 CLI regressions: `python -m zava_forward.core` (version), `discovery-demo` (exit 0), extra argument (exit 2), importer stage/transfer help and refusal story.
* V5 Disposable MSSQL projection tests under the nonqueued heavy lock, own labelled container.
* V6 Served scoped browser story: synthetic data, explicit ZF_DATA, SQLite and JSON, Playwright.
* V7 Lint/type: ruff check, ruff format --check and mypy for core, importer and api (full venv), plus importer and core in the driver-absent venv.
* V8 Driver-absent proof: `import mssql_python` fails in the nosql venv, Importer mypy and 79 tests pass there.
* V9 Dependency-rule tests in core, importer, api; witness verify at the end.

## Stop rules

* A new source defect (not an integration resolution) stops implementation and is returned as evidence and scope. A refused witness event stops the run.
