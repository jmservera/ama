---
title: Bicep quality gates 139 changes
description: Offline implementation and validation evidence
ms.date: 2026-10-16
---

## Scope and current state

Full plan P01/P02. Implementation complete. One critique completed and PC-001
applied directly. No significant divergence, deployment or private-data access.
Existing lint configuration and guards reused.

## Dependency restoration

Baseline main build passed with az Bicep 0.48.1. Baseline full infra suite ran
67 tests with two import errors because source distributions were absent.
Created `/tmp/ama-139-venv` and pip installed `--no-deps -e src/core -e src/agents
-e src/api -e src/orchestrator`. Ruff probe then failed (module absent);
pip installation is eligible. No uv or private dataset involved.

## P01: Controls and CI

Expanded the existing compiled policy tests with presence-sensitive service
inventories, actual endpoint/connection/DNS wiring, SQL and local-auth controls,
purge/soft-delete/RBAC, exact unconditional audit policies and positive bounds.
Exhaustive profile/public/purge, edge and pilot matrices reuse named guards.
Six mutation tests call the same clean-template assertions on copied compiled
templates; temporary unused-parameter source proves both build/lint fail.

Enabled the existing core linter explicitly without relaxing any selected
error rule. Added all-entry-point build/lint, required full infra suite and
scoped ruff inside existing source namespace job; infra paths now trigger it.
No existing job/check identity changed and legacy workflow is untouched.

Small safe Bicep fixes: audit retention minValue(1); governance built-in policy
IDs now tenantResourceId rather than invalid subscription-prefixed strings.
The all-file build initially failed use-resource-id-functions on both
governance assignments. This is a directly related current-state correction;
no change to policy enforcement or Defender defaults, no scope divergence.

## P02: Validation and delivery

Validation commands (all final results exit 0):

```bash
for file in infra/*.bicep infra/modules/*.bicep; do
  az bicep build --file "$file" --stdout > /dev/null && az bicep lint --file "$file" || exit
done
REQUIRE_AZ_BICEP=1 /tmp/ama-139-venv/bin/python -m unittest discover -s infra/tests -q
/tmp/ama-139-venv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py
/tmp/ama-139-venv/bin/ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py
git diff --check
```

Full infra suite: 86 tests, no skips. Bicep 0.48.1; Ruff 0.17.1 installed via
pip after missing-tool probe. Instrumented same-assertion helper count: 129
compiled mutation cases initially rejected; two additional disabled-policy
mutations added before Review (final count recorded below).
Temporary unused-parameter probe additionally rejects both build and lint.
Final full-suite rerun after DNS parent and disabled-policy assertions: 86
tests, no skips, exit 0; scoped Ruff check/format and diff check exit 0.
Final mutation coverage is 131 compiled cases (129 counted plus two passing
disabled-policy cases), with no altered source files or Azure calls.

Implementation-time failures were corrected, not hidden: initial unformatted
test had Ruff long-line/zip diagnostics; formatting plus strict zip and split
strings corrected these. First mutation run exposed the guard parameter's
compiled expression yielding a value object (not a literal dict), and
subTest suppression inside an assertion helper. Replaced the whole value
object and moved contextual messages outside the helper's failure path.
Full suite then passed. Subsequent all-file builds/lints passed.

Read-only invariant checks compared workflow name, job IDs and explicit check
names against HEAD: identical. Verified log starts with exact HEAD content
(append only); updated index routes to existing infra guide. No new knowledge
synthesis or regulatory claim. README records both Bicep gaps and live limits.

One Review complete: outcome Residual work, no in-scope defects; RV-001/RV-002
route live acceptance and owner retention/locking outside this slice.
Commit/push/PR authorized by caller after Review. No blockers.

## Publication

Code/evidence commit `bfef987` pushed normally to
`feat/bicep-quality-gates-139`. PR https://github.com/jmservera/ama/pull/333 targets
main and is open. Its body contains Refs #139, no closing keywords;
`closingIssuesReferences` is empty. Verified author and committer email:
`8036360+jmservera@users.noreply.github.com`, with required Copilot trailer.
Hosted MVP validation and source CI checks started; no merge attempted.
This delivery-evidence update is a normal subsequent commit, not an amendment
or history rewrite. One-shot manual parent session stops after publication;
the offline task is complete and the two review residuals remain separate.

## Residual work

Owner locking/legal retention, actual ARM rejection messages, private networking
and optional edge live acceptance remain unverified. Pipeline #138 excluded.
