# Critique: issue 1297 plan (single pass)

Verdict: proceed with amendments applied directly.

* Allowing a skip by reason alone would weaken execution: bind to exact class and reason per group. Applied.
* Zero skips and at least one ok test per class in the required step; integration=True keeps SQL_NOT_APPLICABLE the only tolerated skip there. Applied.
* A browser-only or infra-only changed selection must not leave the tolerated skips unexecuted: couple selection. Applied.
* ZF_RESIDENT_MSSQL classes remain an unwired gap: routed as follow-up, not changed here.
