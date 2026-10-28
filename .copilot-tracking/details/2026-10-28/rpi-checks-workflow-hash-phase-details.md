---
title: Local gate workflow pin correction phase details
description: Bounded completion evidence for the two planned phases
ms.date: 2026-10-28
---

Task: rpi-checks-workflow-hash. Initial readiness: research Complete / Ready.
No unresolved choices; owner explicitly requested all phases and publication.

<!-- P01 -->
## P01: Correct and validate

<!-- P01-T01 -->
### P01-T01: Extend the existing test

Within test_matrix_drift_and_unreviewed_extra_commands_refuse, assert the
pin key set equals WORKFLOWS and real repository digest equality for each
workflow. Keep existing unreviewed-selector assertions. Patch fixture pins
to fixture bytes for a positive preflight, then mutate and restore each
fixture file and assert its exact drift failure. Mock only versions/tool
identity in the unit test, never in the real preflight. Verify red on the
existing deployment pin before changing production code.

<!-- P01-T02 -->
### P01-T02: Refresh and exercise

Replace only the stale deployment literal. Run
python3 -B -m unittest tools.test_rpi_checks -q. Invoke Runner.preflight()
directly with actual tools and the candidate as snapshot, new external
output and no mocked probes; explicitly fail if runner.failures is nonempty.
This is preflight evidence only, not a gate receipt. Check existing
Ruff 0.17.1 and strict mypy 2.4.0 contracts if available; an actual
missing-dependency failure precedes any install.

P01 completion: existing test extended, stale real pin failed before refresh,
all 30 runner tests passed after correction, real preflight passed all probes
and five pins. Canonical Ruff lint/format and strict mypy passed. Missing
Ruff was restored in an external venv; no dependency manifests changed.
No remaining implementation items; P02 is review/publication only.

<!-- P02 -->
## P02: Review and publication

<!-- P02-T01 -->
### P02-T01: Original independent Review

One fresh reviewer assesses source diff, test behavior, research/policy
justification and validation evidence. Preserve execution, outcome, scope
and any findings without rerunning Review; route findings to later work.

<!-- P02-T02 -->
### P02-T02: Clean candidate and gated publication

Resolve gh api user and configure repository-local noreply email for both
author/committer. Include Refs #500 and requested Copilot trailer.
Commit original evidence before complete --all gate, external to checkout.
Any new commit or base/tool/input movement invalidates the gate. Fetch main
and verify the authoritative receipt against the current origin/main just
before push. Independent exact-head assessment is distinct from original
Review; it must not rewrite that Review outcome. Never claim hosted/human
approval. If required validation blocks, retain evidence and do not push.
