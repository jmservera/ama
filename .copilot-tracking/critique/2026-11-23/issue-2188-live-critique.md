# Issue 2188 live critique (2026-11-23)

Executed once on the final-candidate plan. Verdict: proceed.

* Risk: Trivy DB lock contention under concurrent scans. Disposition: applied directly; scans serialised with `trivy_lock`.
* Risk: writer starvation or deadlock between `mssql` (all slots) and images (one slot). Disposition: images never wait on anything while holding a slot except the Trivy lock, which is leaf-level, so progress is guaranteed; mssql acquires slots under a gate mutex so two acquirers cannot interleave.
* Risk: weakening gate semantics. Disposition: no; same commands and receipt, only scheduling changes.
* Tier: the tool is a gate tool; scheduling change only, no permission/security control change. Classified focused with targeted tests, since the change touches no `src/` code; owner forbids rpi-checks.py --all.
