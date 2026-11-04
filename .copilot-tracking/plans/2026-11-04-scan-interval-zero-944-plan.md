---
title: Plan for #944
ms.date: 2026-11-04
---

* Slice: single slice, whole issue.
* Phase 1: in `Assistants.forecast`, raise a plain-language `ValueError` when `scan_interval <= 0`, before the division. The forecast is read-only and staff-only, so refusing is the manual-path-safe behaviour; ordinary case work is unaffected.
* Phase 2: add a test for 0 and a negative value.
* Validation tier: focused (no security, infrastructure, SQL schema or deployment change). Gate not run.
* Critique: executed once, inline. Compatible finding applied: refuse (not silently skip) so the operator sees why; keep the check narrow rather than gating on `limits.valid`, which would change existing forecast behaviour for other invalid settings.
* Details: [details](../details/2026-11-04-scan-interval-zero-944-details.md).
