---
title: Issue 154 representative expiry changes
ms.date: 2026-11-01
---

* Added class `RepresentativeAuthorityBoundary` (4 tests) and `date`/`timedelta` imports to `src/core/tests/test_resident_preview.py`. No production code changed.
* Validation: `unittest` for the file 36 OK; ruff check, ruff format --check and mypy on `src/core` clean (pip-installed editable in a temporary venv).
* Divergence: none from the plan.

## Correction cycle (PR 712, 2026-11-01)

* `test_resident_preview.py`: the unconfirmed-authority test now iterates the supported non-Confirmed statuses (Unclear, Disputed, Revoked) instead of the unsupported `Pending`.
* The household-leak assertion now checks `2 Synthetic Row`, the address of the represented case SYN-C2.
* State and review artifacts record independent Review as pending.
