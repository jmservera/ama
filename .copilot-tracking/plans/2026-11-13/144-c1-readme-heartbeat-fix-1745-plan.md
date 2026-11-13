---
title: "#144 C1 README heartbeat fix plan"
ms.date: 2026-11-13
---

## Phases

* [ ] P1 Update the infra/README.md "Worker and job images" row and the heartbeat sentence, regenerate the cutover inventory.
* [ ] P2 Rewrite the margin test from production constants; bound replace_worker.
* [ ] P3 Run test_container_contract, test_bicep_policy, test_cutover_audit, src/agents tests, ruff, mypy in /tmp/venv-144c1-1745.
* [ ] P4 Review once, commit locally, no push.

Details: [details](../../details/2026-11-13/144-c1-readme-heartbeat-fix-1745-details.md)
