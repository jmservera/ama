---
title: Issue 212 implementation evidence
description: Changes and validation for the approved bounded plan
ms.date: 2026-10-16
---

## Scope

Full issue-212-plan, P01 and P02. Implementation started after one critique
and direct dispositions. No source approvals or private dataset reads.

## P01

P01-T01/T02/T03 complete. New rule_card_check bindings are immutable and
visible before human approval. Existing seeds remain unchanged drafts.
The typed engine has two finite predicates, exact citation/status gating,
code-owned UTC arithmetic, no hold/message/AI writes, atomic check/alert/
checkpoint transactions, stable data keys and minute schedule keys.
Per-home alert grouping ranks clock then harm, attention is throttled per
home/card/step/item without suppressing checks or breach escalation.
Owner-only acknowledgement/outcome and retained classifications are exposed
through authenticated role-scoped API routes. Case mutations evaluate after
commit; the bounded schedule entry point revisits SQL facts.

Immediately relevant refinements: use a transaction-allocated check sequence
to identify the latest whole snapshot, not timestamp ties or latest individual
items. Old advisories disappear on newer clear/empty evidence; unresolved
breaches survive holds and changing evidence. A separate availability/coverage
status prevents empty or stale results appearing as a compliance conclusion.
Independent adapter concurrency and failed-checkpoint recovery are tested.

P02-T01 complete: tests remain in core/tests and api/tests. The existing
role endpoint inventory covers new routes. Core/API READMEs and knowledge
README/log record contracts and limits. No production code outside src.

## Validation

Initial full suites: core 413 tests passed; API 538 tests passed, 105
environment-dependent skips. Final targeted rerun after snapshot/coverage
refinement: core 33 tests and API 30 tests passed. Both whole-project ruff
checks and mypy passed (core 84 files, API 43). Final adapter-shape and
acceptance evidence reconciliation completed before the single Review.
Final core engine/card tests: 34 passed, including SQL Server DDL-shape and
independent SQLite adapter concurrency. Final combined API law/approval/
inventory/hazard/alert tests: 67 passed, 16 environment-dependent skips.
After the final independent-release evidence guard, core 34/API 5 tests
passed again, as did both full-project ruff and mypy checks.
Both new typed source/test format checks and git diff --check passed.
The nine-row acceptance audit is in src/core/README.md. Criterion 7 is
explicitly partial end-to-end; all live, staff and legal gates remain unmet.
P02-T02 complete; P02-T03 publication follows the one Review.

Commands ran from the project directories using /tmp/zf164/bin/python,
ruff and mypy, with absolute per-project test PYTHONPATH. Missing local
distributions were installed with pip --no-deps; a missing setuptools build
backend was restored with pip after the explicit failure. No uv or cloud
acceptance run. Existing core fixture file ResourceWarnings were observed,
not changed. Full-suite logs are session artifacts, not repository files.

## Remaining gates

Operational legal approval, real staff trial, UI and live SQL/Azure evidence
are not supplied and will remain explicitly unmet.

## Review handoff

Ready for one Review of P01 and P02-T01/T02. No known unaddressed local
implementation defect. P02-T03 is the explicitly authorized publication
step after Review, with no further source implementation intended.
