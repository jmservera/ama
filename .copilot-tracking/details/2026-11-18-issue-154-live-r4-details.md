---
title: Details for #154 live round 4
ms.date: 2026-11-18
---

## Loader contract

* File: absolute, regular, non-symlink, at most 64 KiB, JSON array of at most 20 objects.
* Each object requires `case_id`, `email`, `representative_ref`, `measure`, `tasks`, `valid_from`, `expires_at` (explicit UTC ISO strings); unknown keys are rejected; `revoked` optional boolean.
* `expires_at` is mandatory (expiry as recorded), must be after `valid_from` and not later than `rs.AUTHORITY_END`.
* Each grant passes `rs.admit_representative_grant`; any failure raises `ShowcaseConfigError` with no value echoed.
* Grants carry no secret; the representative signs in with the showcase password verifier already configured, as for residents.
* No outbound contact, no new network or Azure access.
