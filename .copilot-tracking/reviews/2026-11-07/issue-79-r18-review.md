---
title: Issue 79 author Review, correction cycle 1 for the 357e842d assessment
ms.date: 2026-11-07
---

Author-only Review, executed once after implementation and checks. It is not an independent assessment. The original r17 Review is unchanged.

## Status

* Execution: Complete for the supplied boundary. Outcome: Conformant with residual work.
* Compared: research, plan with critique, details, changes, the independent findings JSON, the diff against `357e842d`.

## Findings

* RV-001 (info): finding 1 corrected. The selected policy is validated (key, version, hash) before sign-off for schedule, publish and exercise; a stale-hash signed policy is refused `policy_invalid` with no archive write. Verified by RED then GREEN.
* RV-002 (info): finding 2 corrected. A future latest date gives verify and schedule status `problem` with null window state, refuses non-exercise publish (existing `archive_unverified` code, specific message) and leaves exercise no-write and historical records healthy. The 9999-12-31 case now reports through the same single problem; the existing test still passes unchanged.
* RV-003 (info): finding 3 corrected. `blocked` schedule exits 2 for approval missing and unknown policy; due/current stay 0. The README states it. Scheduler callers that treated the shipped unsigned policy as exit 0 will now see 2, as the finding intended.
* RV-004 (Low, residual): the refusal code for a future date is `archive_unverified`, not a dedicated code, to preserve an existing test; consumers distinguish it by message. Route: later `rpi-plan` if a dedicated code is wanted.
* RV-005 (Low, residual): only the latest archived date is checked; the helper does not reject a future `published_on` itself. Route: #1231 helper lane / later research.
* RV-006 (info, evidence): GREEN attempt 1 failures and the one `sed` edit deviation are preserved in Changes; the tools' in-tree caches were removed individually after verification.
* RV-007 (Medium, gap): no FULL, independent exact-head assessment or hosted checks on this head; named policy-owner signoff and Legal retention remain outside this work.

## Validation

* 53 core tests and 15 API wiring tests OK; pinned Ruff check clean; mypy clean (268 files); `ruff format --check src` reports only pre-existing `src/check-container.py`. Logs under `/tmp/79-r18-1107/`.

## Routing

* Coordinator: merge this parent into the corrected child, then a new combined FULL, independent exact-head assessments, hosted checks and a new parent integration FULL.
