---
title: CI infra test dependency correction changes
description: Implementation and validation evidence for PR 357
ms.date: 2026-10-16
---

Task: 138-ci-pyyaml. Scope: full approved correction plan.

## P01 integration and repair

Implementation started after one critique and recorded disposition.
Source-only clean-venv discovery reproduces missing PyYAML (131 tests,
one import error). No production dependency changes authorized.
Merged origin/main at `dbe9ffd`, preserving both append-only histories without
conflict. No rebasing, force push or retired-layout changes.

The validate infra-test run block now installs `PyYAML==6.0.3` before discovery.
Both actual CI documents are tested for that prerequisite in the executing
step, and deep-copy mutations reject deletion, unpinning and late installation
for each. No original pipeline-control assertions or mutations were removed.
The full infra recipe documents the test-only prerequisite and exact baseline
comparison; reference routing and append-only log updated. P01 complete.

## P02 validation and publication

The same Python 3.12 isolated venv passes the exact discovery command after
installing only `PyYAML==6.0.3`: 156 tests, no skips. A second complete run
with `REQUIRE_AZ_BICEP=1` and absolute core/agents fixture paths also passes.
The suite includes six new dependency-install mutations, existing pipeline
control mutations, fake deployment orchestration and real local API probes.
The installed API runs with a temporary constructed empty fixture; health 200
and all three authentication denials pass. No private working data read.

After the baseline/fixed comparison, Ruff and mypy were missing. Installed
the existing CI pins `ruff==0.17.1` and `mypy==2.4.0` in the test venv.
Targeted Ruff/format for pipeline script/tests and strict pipeline helper
mypy pass. Git diff whitespace check passes.

No dependency manifests, production code, SQL, Dockerfiles or Azure controls
changed. No new image builds or live Azure/OIDC acceptance is claimed.
P02-T01 complete. One Review completed: Residual work only for inherited
live acceptance, no correction defect found. Seven workflow test methods pass
separately, including both original unsafe-control and new dependency mutations.
Programmatic checks confirm all prior branch/upstream log entries retained
verbatim and no retired-layout or production manifest edits.
P02-T02 complete; publication remains.
