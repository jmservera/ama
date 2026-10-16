---
title: CI infra test dependency correction research
description: Focused investigation of PR 357 infra discovery failure
ms.date: 2026-10-16
---

## Brief and boundaries

Refs #138. Repair PR 357 on its existing branch, preserving pipeline-control
assertions and production dependencies. User explicitly requests research,
planning, implementation, review, commit and push. No Azure operations,
private datasets, retired-layout changes or issue checkbox updates.
Posture: focused, based on the supplied reproducible failure.
Output: convergence; root is `.copilot-tracking/research/2026-10-16/`.
Repository instructions and ADR 0006 apply. Domain specialists are skipped:
this is one small continuous dependency trace, handled inline.

## Questions and evidence

* C1: `infra/tests/test_pipeline.py:20` imports PyYAML unconditionally.
* C2: `.github/workflows/mvp-validation.yml:43` discovers every infra test
  without first installing PyYAML.
* C3: `.github/workflows/src-ci.yml:172` already installs `PyYAML==6.0.3`
  immediately before infra discovery.
* C4: `infra/README.md:253` documents the pin for focused pipeline tests,
  but the complete quality-gate recipe omits it.
* C5: `infra/tests/test_pipeline.py:118` retains negative workflow-control
  mutations, while the CI wiring assertion covers only source CI.

## Research cycle

1. Wider: inspected both CI discovery consumers, documentation, open PR,
   issue acceptance and upstream ancestry. Main is one commit ahead.
2. Deeper: a new isolated Python 3.12 venv with only
   `pip install -e src/core -e src/agents -e src/api` reproduces
   `ModuleNotFoundError: No module named 'yaml'` during
   `python -m unittest discover -s infra/tests -q`: 131 tests, one error.
3. Contrarian: a standard-library YAML subset parser would add bespoke
   parsing risk and could weaken structural controls. Skipping on ImportError
   would hide removed controls. The existing pinned test-only install is
   simpler and explicitly authorized. Production dependency changes rejected.

## Decision and readiness

Select the existing `PyYAML==6.0.3` pin in the specific validate infra-test
step. Assert both CI consumers install it before discovery and mutation-test
removal of that installation. Keep all pipeline-control mutations.
Merge origin/main first and preserve both append-only log entries.
Research disposition: executed. Planning Readiness: Ready.
No additional cycle needed: the failure and both relevant consumers are
identified. All six live Azure/OIDC acceptance criteria remain unmet.
