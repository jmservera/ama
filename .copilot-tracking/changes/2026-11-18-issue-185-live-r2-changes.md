---
title: Changes for issue 185 live device identity demo
date: 2026-11-18
---

Docs and evidence only; no source edits, focused tier (documentation link and diff review). No rpi-checks run.

Changed: `docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md` (second-run section) and new `docs/reference/research/issue-185-live-device-identity-run2-log-2026-11-18.txt` (redacted job output, 0 key matches).

Azure: created and removed job `job-185b-probe` and a Registry Contributor role assignment; three devices created and deleted; hub device count 0 afterwards.

| Criterion | Status | Basis |
| --- | --- | --- |
| Approach decided with credential owner | Ticked before | Owner decision 2026-11-18: Hub-generated symmetric keys, no X.509 |
| One device identity per home and stock home ID | Ticked before, not re-proven | Source tests; run encodes home slot in device id |
| Credentials issued and stored without appearing in source or logs | Proven for demo (issuance, no leak in retained log); "stored" = memory only | Create 200 with Hub keys, sends 204, wrong key 401, 0 key matches in log. Durable storage unproven: Key Vault excluded by owner |
| Teardown removes all simulated identities | Proven for demo | Delete 204 x3, read-back 404, `show-stats` 0 devices, job and role removed |

Not proven: production ownership, rotation, durable storage, repeatable repository command (adapter supports X.509 only), N-home scale.
