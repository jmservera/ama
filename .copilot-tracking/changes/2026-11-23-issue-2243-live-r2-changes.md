---
title: Issue 2243 live changes r2
---

Changes: added the research note, probe folder, README index entry and log entry. No source change; tier focused. Hosted CI not observed (nothing pushed).

| Criterion | Status | Basis |
| --- | --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven | `expires_at()` on main; label moved off "exercise has ended" |
| Add a test | Proven | `test_expiry_follows_zf_demo_expires_at_and_fails_closed`; 70 tests OK |
| Rebuild and roll the resident image | Proven for a roll, unproven for commit | Revision 0000026 at 100%; registry firewalled |
| Resident chat answers with the model within budget caps | Unproven, owner-gated | `usage_limit` on both questions; private SQL ledger expiry needs owner action |
