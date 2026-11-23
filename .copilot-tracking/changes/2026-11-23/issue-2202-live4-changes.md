# Changes: issue 2202 live4 (2026-11-23)

Tier: focused (tools/ only, no src/ change). No push, no Azure write. Ruff format and check pass; `python3 -m unittest tools.test_demo_preflight` runs 10 tests, OK.

Files:

* tools/demo_preflight.py: `check_deployment` (digest and hardening value only), agents app, wired into `collect`
* tools/test_demo_preflight.py: three tests (digest and hardening gate, query scope, default coverage)
* docs/reference/research/issue-2202-live-receipt-2026-11-23.md and its preflight.txt, docs/reference/README.md, docs/reference/log.md

## Per-criterion table (#2202)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Images rebuilt from main and rolled | Unproven | digests differ across API, simulator, receiver; registry firewalled; no build commit readable |
| Revisions Running and Healthy; hardening enforced; rollback noted; agents difference explained | Proven (rollback not exercised) | preflight.txt: 8 workloads enforced, API 0000055 and resident 0000028 Healthy |
| Owner demo checks | Not re-run | earlier proofs in issue-2202-live-deploy-2026-11-22.md; half of homes unproven |
| Live receipt and log entry | Proven | receipt note and log entry |
