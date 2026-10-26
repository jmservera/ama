---
title: Resident Azure release 462 - plan (2026-10-26)
description: Release plan and the minimal source change. Written after the interim deployment.
ms.date: 2026-10-26
---

This plan was recorded after the interim ungated deployment, not before it. It reflects the steps that were executed under the owner and coordinator decisions.

1. Write the two vault secrets with `resident_demo_secrets.py` (expiry 2026-10-31T23:59Z).
2. Push the scanned image by digest using the temporary ACR route, then restore the registry exactly.
3. Deploy `infra/resident-demo.bicep` with `--no-ingress`, apply the view, principal, grants and allowlist through a per-execution ARM `/start` of `job-cutover-test-init`, counts only.
4. Open ingress for at most 60 minutes, run the checks that need no password, then close.
5. Source change: raise `MAX_MAPPINGS` from 25 to 1000 (core, SQL reader message, SQL comment, README, tests use the constant).

Bound rationale: 1000 is above the 980 cases in the current data and keeps the fail-closed refusal and the `fetchmany(MAX_MAPPINGS + 2)` read bound. It is a documented demo bound, not a scale target.
