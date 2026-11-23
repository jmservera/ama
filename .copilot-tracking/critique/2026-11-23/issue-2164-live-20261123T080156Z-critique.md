---
title: Critique for issue 2164 r6
ms.date: 2026-11-23
---

Executed once on the final candidate plan.

Verdict: proceed.

* Risk: widening refusal could break unbound Entra callers. Disposition: applied; unbound principals
  already fail closed (no roster row for the derived email), so behaviour is unchanged.
* Risk: JSON and SQL stores both feed `_current_staff`. Disposition: applied; the oid/tid check runs
  in `_gate` on the loaded row, backend-neutral, and tests run on both backends via DraftCases.
* Risk: src change forces the FULL tier. Disposition: recorded; the coordinator runs the gate, this
  worker runs targeted tests, mypy and ruff only and never `rpi-checks.py --all`.
* Live Azure proof is not applicable: sensor review drafts are default-off (`FLAG`) and not served
  in the demo apps. Recorded as unproven-for-demo.
