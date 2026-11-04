# Details: live sensors seed (#1072)

* Seed: `seed SYN-NE-001458-FLAT1 2026-11-05 30` (720 generated, 7 future-dated rows removed, 713 kept).
* Map: `map ZF-2025-0029 SYN-NE-001458-FLAT1` (rowversion +1; `unmap` reverses).
* View: `view id-resident-demo <client id>` applies the view and `verify_principal`.
* Verify: EXECUTE AS the resident principal; 1 of 522 rows with sensors, 0 foreign.
* Spec restore: no job spec change; template, configuration and identity read back identical.
