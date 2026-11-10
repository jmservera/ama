---
title: Issue 89 current main adoption critique
ms.date: 2026-11-10
---

## Execution and verdict

* One critique of the final candidate plan, authored by the same agent (not independent). Verdict: Proceed; amendments applied directly, none conflicts with a confirmed decision.

## Findings

* PC-001 Core `pyproject.toml` changed; the old SQL result is not carried over. Applied: run focused 36 SQL once if exact qualification fails; it fails, so run.
* PC-002 Mypy may import the Registry SDK. Applied: install the pinned dev dependency into the own environment only after an actual failure and record it.
* PC-003 A clean textual merge may still break manifests. Applied: `test_scenario_manifest` and TOML parsing after merge.
* PC-004 Skips are not passes; any browser or SQL refusal (busy lock) is reported as unrun, not passed.
* PC-005 Witness order: unique-key validation in its own call before each marker, each marker a separate call, literal 40-hex HEAD obtained in one call before commit-complete.
