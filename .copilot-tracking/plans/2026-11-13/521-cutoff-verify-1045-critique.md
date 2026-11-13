# 521 plan critique (rubber-duck, independent)

Verdict: Revise. Findings, all applied directly (see details file amendments):

* PC-001 research lacked inventory: research file was a stub; now filled with file:line inventory. Applied.
* PC-002 SQL test omitted: add test_resident_showcase_sql.py with ZF_TEST_MSSQL unset; DB behaviour unverified. Applied.
* PC-003 az bicep build and worktree writes: record bicep-dependent tests as skipped/blocked; avoid bytecode, clean egg-info. Applied.
* PC-004 exit/provenance gates: Python >=3.12, both package origins, immediate status capture, zero tests or setup failure = blocked. Applied.
