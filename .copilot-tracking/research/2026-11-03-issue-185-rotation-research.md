# Issue 185 research, round 2 (2026-11-03)

Disposition: executed (delta only; builds on 2026-11-01 research).

* Merged PR #647 delivered plan/provision/teardown against fakes and the proposed decision. Nothing else merged for #185.
* Gap: the issue and ADR 0003 decision 6 require credential rotation; `device_identity.py` had no rotation path. The research plan states rotation is owner-run and rotated credentials must be covered by teardown.
* Remaining unmet criteria need the owner or live Azure: owner confirmation, live Key Vault issue/storage, live teardown.
* Slice chosen: offline `rotate()` (overlap, then revoke) in `src/core`. No security-sensitive infra, SQL or deployment touched; focused tier.

Planning Readiness: Ready.
