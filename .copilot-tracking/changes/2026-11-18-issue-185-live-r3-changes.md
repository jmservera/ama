---
title: Changes for issue 185 run 3
date: 2026-11-18
---

Docs and evidence only; no source edits, focused tier (documentation link and diff review). No rpi-checks run.

Changed: third-run section in `docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md`; new redacted retained `issue-185-live-device-identity-run3-log-2026-11-18.txt` and `...run3-operator-2026-11-18.txt`.

Azure: created and removed jobs `job-185c-probe`, `job-185d-probe`, two Registry Contributor assignments; 3 devices created and deleted by this run. Devices with the same ids seen later at 12:39 to 12:41Z belong to another concurrent worker (not deleted by me).

| Criterion | Status | Basis |
| --- | --- | --- |
| Approach decided with credential owner | Ticked before | Owner decision 2026-11-18 |
| One device identity per home and stock home ID | Ticked before; additionally proven live for 3 homes | Ids built with repository `sensor_key`, distinct per home |
| Credentials issued and stored without appearing in source or logs | Proven for demo (issuance, no leak, retained log, 0 key matches); "stored" = process memory only | Create 200 with Hub keys, send 204, wrong key 401. Durable store unproven: Key Vault excluded |
| Teardown removes all simulated identities | Proven for this run's identities (delete 204 and empty in-job read-back); hub-wide count 0 NOT shown | Shared hub: foreign devices with identical ids appeared after teardown |

Not proven: production ownership, rotation, durable storage, repeatable repository command (adapter is X.509 only), N-home scale, hub-wide zero count.
