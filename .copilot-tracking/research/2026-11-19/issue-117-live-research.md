# Research: issue 117 live demo, first unmet criterion. Refs #117.

Unmet criterion: "Uploads are scanned before availability" (the retention criterion is ticked).
Prior evidence: docs/reference/research/issue-117-live-r3-closure-2026-11-18.md and the r4 changes (EICAR in the local scanner, merged at HEAD).
Planning readiness: Ready (disposition reused; no new investigation needed).
Finding: order of operations (scan before the record is appended) and the local scanner are proven offline and live. The only gap is a real engine on the demo app path: it needs ZF_SCANNER=defender on ca-cutover-test-demo-api, and the demo storage firewall denies this identity.
Owner decisions allow live Azure but no production changes and name no demo-config change, so the setting is not changed here.
