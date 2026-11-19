---
title: Changes for issue 185 live proof
ms.date: 2026-11-18
---

Refs #185. Tier: FOCUSED (no `src/` change; documentation and tracking only). No `rpi-checks.py` run. Validation: Git diff review, link check by inspection, and live run output.

Changed: new evidence note `docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md`, index entry in `docs/reference/README.md`, entry in `docs/reference/log.md`.

Azure actions: temporary job `job-185-probe` and IoT Hub Registry Contributor role (both removed), three `SYN-185-*` SAS devices (deleted; hub statistics show 0 devices). Hub settings unchanged.

| Criterion | Status | Basis |
| --- | --- | --- |
| Approach decided with credential owner | Proven (already ticked) | Owner decision 2026-11-18: Hub-generated symmetric keys, no X.509 |
| One device identity and one stock home ID per home | Already ticked, not re-proven live | Earlier source tests |
| Credentials issued and stored without appearing in source or logs | Proven for the demo; durable storage unproven | Hub-generated keys, in-memory only, no key text in output or repository; Key Vault excluded by the owner |
| Teardown removes all simulated identities | Proven for the demo hub | Delete 204 x3, empty read-back, 0 devices in hub statistics |

Unmet beyond the demo: production credential ownership, durable secret storage, rotation, X.509, N-home scale, repository adapter for SAS.
