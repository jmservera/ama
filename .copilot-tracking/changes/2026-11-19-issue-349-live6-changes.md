# Changes

Files: research note r6, `docs/reference/README.md` index row, `docs/reference/log.md` entry, evidence dir live6. No `src/` change; focused tier (docs only). No Azure call, nothing created.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Unproven: needs Application Administrator; Graph denied |
| 2 | Credential in private vault, nothing published | Proven for the demo (r5) |
| 3 | Audience and callback use registration | Partly proven (r5) |
| 4 | Roster reconciled in VNet | Unproven, not applicable to the demo |
| 5 | Sign-in, logout, wrong-role, unknown-staff denial | Test account proven (r5); wrong-role live blocked by host DNS; code-level denial covered by unit tests |
| 6 | Anonymous 401, forged headers, positive request | Proven with a qualification (r5) |
