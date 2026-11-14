---
title: ci-affected tracking paths and merge-base diff review
ms.date: 2026-11-14
---

## Review

Execution: executed once. Outcome: conformant, no open findings.

* Inert set limited to `.copilot-tracking/` and docs `.md`/`.mdx` outside the three CI-watched paths; infra, workflows, `support/synthetic-data/`, `src/trivy.yaml` and unknown paths still select everything (tested).
* Three-dot diff confirmed in code and by mock test.
* Residual risk: docs Markdown excluded from CI paths filter semantics matches `src-ci.yml` `paths`. Hosted CI for the exact head not yet observed; coordinator review and push pending.
* Focused tier: local unittest and ruff passed; no full gate claimed.

## Cycle 1 validation

* Focused tier. Lint, format and both unit suites pass locally from the repository root, with no code change needed.
* Not run: full gate and hosted CI for the exact head; push pending the coordinator.
