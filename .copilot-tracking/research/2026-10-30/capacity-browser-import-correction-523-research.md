---
title: Capacity browser import correction research
description: Correction cycle 1 for PR 577, Refs 523
ms.date: 2026-10-30
---

## Research Brief

Investigate the reported discovery-time Playwright dependency in the capacity
harness and tests. Audience: PR reviewers. Output mode: convergence. Focused
posture, selected from the explicitly bounded caller scope. Evidence root:
`.copilot-tracking/`. No application UX changes, Azure, sign-in, secrets, uv
or push. Research writes are restricted to evidence and workflow state.

## Research Parameters and Direction Controls

* Questions: Does browser-free discovery fail? Which imports must be deferred?
  Which existing regression pattern proves the runtime-only contract?
* Internal candidates: capacity harness/tests, regulatory import regression,
  API README, API project configuration and CI runtime installation.
* External sources: none needed for this internal import correction.
* Success: reproduce before editing; preserve scanner assertions and explicit
  missing-browser failure; validate full API discovery, Ruff/format and mypy.
* Owner explicitly requests all four RPI phases and a local commit on the
  existing active PR branch. No interactive clarification is necessary.

## Extension Registry and Prior Knowledge

Repository instructions and the RPI skills apply. Web-design skills are skipped:
this change touches Python dependency loading, not web UI. Research is inline
because this is one tightly coupled import trace. Existing parent state
`rpi-sessions/2026-10-30/capacity-work-orders-page-523-state.json` records completed
implementation, original Review and unresolved publication/live gates. Those
historical outcomes are preserved, not reclassified by this correction.

## Research Cycle 1

### Wider

The harness and test both import Playwright at module scope. API dependencies
place it in the dev extra only; the README promises browser-free discovery.
Reflection: the reported failure is plausible and needs isolated reproduction.

### Deeper

Blocked Playwright with a fresh-process `MetaPathFinder` and ran unittest
discovery for `test_capacity_browser_check.py` in the existing capacity dev
environment with the caller's source/test paths. Result: one loader error,
`ModuleNotFoundError` at harness line 22, before any scanner assertions ran.
The installed dev dependency therefore does not mask the reproduction.
Reflection: the reported defect is confirmed, not merely inferred.

### Contrarian

The regulatory harness already uses postponed annotations, TYPE_CHECKING for
Page, local runtime imports and a subprocess import blocker. Unlike adding
Playwright to runtime dependencies or skipping scanner tests, this preserves
browser-free tests and explicit failure when browser execution is requested.
The capacity check uses `expect` only inside `check`; browser types occur in
annotations. Import browser operations at the start of `check`, before server
or store access. A list-spec Mock can enforce the sole `evaluate` method
without importing a real Page.
Reflection: no wider dependency or UI change is needed.

### Parent Synthesis and Disposition

Accept lazy operations imports, type-only browser annotations and a fresh-process
regression that actually runs the scanner unit suite with Playwright denied.
Reject adding runtime dependencies or skips: both violate the README contract.
One focused cycle answers all material questions; another would repeat evidence.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `src/api/checks/capacity_browser_check.py:22` | Browser types and operations imported at module load. |
| C2 | `src/api/tests/test_capacity_browser_check.py:13` | Runtime Page import used only as mock spec. |
| C3 | `src/api/pyproject.toml:23` | Playwright is a dev-only dependency. |
| C4 | `src/api/README.md:4033` | Runtime-only discovery is a documented contract. |
| C5 | `src/api/tests/test_regulatory_ux_check.py:18` | Existing fresh-process import-blocker regression pattern. |
| C6 | `src/api/checks/regulatory_ux_check.py:3` | Existing postponed annotations/type-only Page prior art. |
| C7 | `src/api/checks/capacity_browser_check.py:169` | Browser operations are confined to check. |
| C8 | `.github/workflows/mvp-ci.yml:30` | Legacy CI installs distributions without dev extras. |

## Findings, Alternatives and Current Decisions

Q1 answered by the actual loader failure (C1-C2). Q2 answered by type-only
annotations and local operations imports (C6-C7). Q3 answered by the existing
subprocess pattern (C5), extended to execute rather than merely import the
capacity tests. Missing-browser execution must still raise explicitly.
No remaining implementation uncertainty. Full publication/live acceptance
remains separate from this local-only correction.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: three ordered inline waves complete; source and reproduction
evidence recorded; no external sources, source edits or unresolved decisions.
