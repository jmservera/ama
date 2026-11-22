# Critique: issue 2204 combinations plan (2026-11-22), executed once

Verdict: approve with direct dispositions.

* Do not modify Kat Larsson's existing roster row (correct already); use a temporary row for the test account and delete it in `finally`. Applied.
* A temporary row must carry a synthetic identity only; never reuse Kat's email or code. Applied.
* Entra tokens lag role changes (seen on 2026-11-22): wait and verify `app_roles` before probing. Applied.
* The AIRestart gate cannot be separated by a non-mutating probe and a drill is not allowed; claim it only through `/api/me` `rule_roles`. Applied.
* Exec rate limit (429, 600 s): minimise exec calls; one for insert, one for delete and verify. Applied.
