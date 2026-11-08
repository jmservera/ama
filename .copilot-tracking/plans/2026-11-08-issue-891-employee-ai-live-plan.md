---
title: Issue 891 employee AI live observation plan and details
description: Bounded plan for attestation, one guarded employee chat ask and stop rules
ms.date: 2026-11-08
---

* [x] Warm `/healthz`; obtain tid/oid from the token endpoint using in-process credential reads; stop at the first distinct failure.
* [x] Sign in through `/.auth/login/aad`, apply the strict identity predicate (`checks.employee_acceptance_check.probe`) before each action.
* [x] One synthetic ask with no case or resident detail; record statuses, booleans and non-sensitive receipt fields only.

Stop rules: no replay, no app or Entra change, no ledger reset, no MFA bypass, no screenshots, HAR or trace; zero billable calls if admission or authority is absent.

Critique: single-pass author self-critique (bounded, read-only continuation). Compatible findings: use the maintained predicate, not `/api/me`; hold scripts and outputs outside the repository; require a model receipt before any AI claim.
