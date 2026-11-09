---
title: "Plan: #184 correction 1"
ms.date: 2026-11-08
---

Critique: executed once. Verdict: compatible; no conflict with confirmed
decisions (source-only, no Azure changes, simulator grants unchanged).

## Phases

* [x] 1. F1: a control refusal (`StreamError`) ends sending and never reuses
  cached homes; only a transient `HomeListError` reuses cached homes the current
  control still lists. Re-read cohort every slot when a control file is used.
* [x] 2. F3: add a `_watch` task to the receiver that polls the control file and
  sets the `HubReceiver` stop event on stop, invalid, changed cohort or expiry.
  Refuse a window shorter than 1 second instead of rounding up.
* [x] 3. F2: add `infra/live-receiver-job.bicep` (manual job, own UAMI, routing
  ready parameter default false, command, read-only control mount, SQL MSI env)
  and document the minimum grants in `infra/README.md`.
* [x] 4. Regression tests, then focused unit, ruff, mypy, Bicep and SQL checks
  with real exit codes.

Out of scope: any grant, deployment, device registration, send or model call.
