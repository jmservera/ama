---
title: Issue 131 inherited correction batch for the household inventory primitive (plan)
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Objective

One inherited correction batch, authorized by the Root brief after the dated D2 audit, for the two introduced Medium findings of the independent assessment 8f0786 (confirmed by D1) and the three introduced Core typing errors and one format difference. It consumes one cycle of the issue 131 allowance (proved minimum before: at least 1; conservative proved minimum after: 0; no fresh five, reset, second cycle or self-retry). It is not a new initial slice, grants no hold release or human authority and keeps the manual, unverified, caller-supplied boundaries of the inventory, digest, version and provenance.

Research: [2026-11-10-inherited-repair-131-research.md](../research/2026-11-10-inherited-repair-131-research.md). Details: [2026-11-10-inherited-repair-131-details.md](../details/2026-11-10-inherited-repair-131-details.md). Critique: [2026-11-10-inherited-repair-131-critique.md](2026-11-10-inherited-repair-131-critique.md).

## Phases

1. Prospective changes record and state path registered; `implement-start` witness event; source is clean until then.
2. Adopt current `origin/main` by an ordinary merge after the marker (not rebase, reset or amend); qualify the composed baseline: targeted Core and API resident tests and configured Core mypy and format.
3. Write the two regression tests first and show them failing on the unfixed module (red); then implement the validator and the new reasons (green).
4. Fix the three typing errors and the format difference in the test file with real types.
5. Minimal bounded Core README sentence; focused tests, configured full Core Ruff check, format check and mypy including the new test code; Core and API resident selectors.
6. Review once (authored), commit RPI records and source with privacy-safe identity and the Copilot trailer, witness `commit-complete`, freeze the handoff.

## Scope

Only `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py` and one bounded sentence in `src/core/README.md`, plus the new RPI records. No endpoint, SQL schema, UI, role, shared store or adapter, authority model, roster, Legal interpretation, attestation or hold release. No issue 1360, 132 or 233 change. No browser, SQL Server, cloud, model, provider or private data; MSSQL is not run and not claimed.

## Validation (owner demo focused tier)

* The two new regressions fail on the old module and pass on the new one, on the JSON `Store` and the inherited SQLite `SqlStore`.
* Core `test_resident_decisions.py` and API `test_resident_api.py` selectors, plus the other Core and API resident selectors that import the module.
* Configured Core `ruff check .`, `ruff format --check .` and `mypy` with no selectors (pinned mypy 2.4.0 and Ruff 0.17.1) in the owned venv; the baseline `fe59` was clean, the candidate had three errors and one format difference.
* No blanket `--changed` or full gate. The owner DEMO override applies; the classification is a mixed focused tier because the change is persistence-facing but carries no schema, deployment, dependency or security-control change, and the verdict stays local until Root's independent exact-head assessment.
