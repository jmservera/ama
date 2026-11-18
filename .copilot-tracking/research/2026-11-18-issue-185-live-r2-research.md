---
title: Research for issue 185 live device identity demo
date: 2026-11-18
---

Research disposition: executed (reuse of the earlier note `docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md`, which kept no raw output and was not independently re-queried).

Evidence read: issue 185 (two criteria ticked, two open), the existing note, `device_registry_azure.py` (X.509 thumbprints only). Hub `iot-cutover-test-rzsrg` in group `ama`: public access Disabled, so a throwaway Container Apps job is needed.

Open criteria to prove: credentials issued and stored without appearing in source or logs; teardown removes all simulated identities. Owner scope: symmetric Hub-generated keys, no X.509, no Key Vault rotation, demo only.

Planning Readiness: Ready.
