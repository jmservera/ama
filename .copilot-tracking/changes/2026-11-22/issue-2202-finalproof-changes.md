# Changes: issue 2202 final live proof

Documentation and evidence only; no src change (focused tier, no rpi-checks --all). Refs #2202. No Azure resource created or changed; nothing pushed.

## Files

* docs/reference/research/issue-2202-finalproof-2026-11-22.md (note)
* docs/reference/research/issue-2202-finalproof-2026-11-22/ (probes, JSON results, az-state.txt, screens)
* docs/reference/README.md (index), docs/reference/log.md (entry)
* .copilot-tracking research, plan, details, critique, changes, review, state

## Per-criterion proven or unproven

| Criterion (#2202) | Status |
| --- | --- |
| Images rebuilt and rolled (API, resident, simulator, receiver) | Partly proven: API 0053 and resident 0025 new digests; jobs not rebuilt here, source commit not derivable |
| Revisions Running and Healthy; hardening enforced; rollback noted; agents app difference | Partly proven: Running, Healthy, enforced on API and agents; rollback not exercised and old revisions not retained; resident has no variable |
| Sensor charts | Proven (resident chart) |
| Map gauges | Partly proven (map loads, 443 markers; gauges not inspected) |
| Consent checkbox | Unproven on 0025 (proven on 0024 in earlier note) |
| Chat routing | Proven |
| Half of homes with readings | Unproven in this pass (earlier 2191 series cited) |
| Live receipt and log entry | Proven |

Requested checks: 10 employee asks 3.09 to 5.37 s pass; UI first ask 7.2 s pass; map, xlsx, resident chart, safety count 23, handoff waiting, AI hold label pass. Generative answer not provable (suspension and resident ledger).
