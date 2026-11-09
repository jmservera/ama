---
title: Issue 86 formal-complaints adapter details (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Plan: `.copilot-tracking/plans/2026-11-06/issue-86-formal-complaints-adapter-plan.md`.

## Phase 1: tests

File `src/core/tests/test_resident_decisions.py`, class `JsonResidentDecisions` (inherited by `SqlResidentDecisions`). Add helper `SyntheticReceiver(mode)` recording calls; modes `ack`, `raise`, `malformed`. Install with `self.store.complaints_receiver = receiver`. Reuse `request()`, `review_body()`, `scope()`, `authority()`, `tenure()`, `answer()`. Run only these tests, expecting failure before Phase 2.

## Phase 2: source

1. `src/core/src/zava_forward/core/complaints_route.py`: constants `STATUSES = ("Unconfigured", "Failed", "Acknowledged")`, `ENVELOPE_KEYS`, `UnconfiguredReceiver.submit` raising `NotConfigured`, `receiver_from_env`, `build_envelope(case, req, attempt)`, `parse_acknowledgement(value)` (dict with non-empty str `receipt_ref` up to 100 characters; optional ISO `received_at`; else `ValueError`).
2. `resident_decisions.py`: add `service_forward` to `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`; implement `_res_service_forward`; add `formal_route` defaults to `followup_view`.
3. Handler order: locate request; `_version`; closed/route/already-acknowledged checks; authority; independent-reviewer recheck; `resident_request_ref`; if validating return; build envelope; call receiver inside try; classify; append attempt; audit detail names request id and status only.

## Phase 3

Add a short README section in `src/core/README.md` stating the boundary, default unconfigured, no real sending, and limits. Focused command: `cd src/core && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests python3 -m unittest test_resident_decisions -q`, plus the `src/api` resident tests if the install allows. Write Changes and Review artifacts, then commit.
