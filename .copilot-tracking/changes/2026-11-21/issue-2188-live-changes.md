# Changes: issue 2188

Tier: FOCUSED (documentation only, no src/ or tools/ edit; full gate not run).

Files: docs/reference/research/issue-2188-live-gate-speed-2026-11-21.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry).

| Criterion | Status | Evidence / reason |
| --- | --- | --- |
| Wall time before and after on the same tree | Partly proven | API image build 80.7 s fresh vs 1.3 s cached on one tree and host. Full-gate pair unproven: needs two full gates; retained receipts differ in head, base and load |
| Receipt records retries | Unproven | Test-class retry not implemented; changing gate semantics needs an owner decision and the full tier |
| Verify rejects tampered evidence | Proven | 25 targeted tools.test_rpi_checks tests pass (tamper, shard, fresh, layer cache, full scope, rejects) |

Issue stays open: Refs #2188, no closing keyword. Throwaway docker tags removed.
