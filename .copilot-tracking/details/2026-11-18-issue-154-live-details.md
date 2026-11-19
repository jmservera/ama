---
title: Phase details for #154 live proof
ms.date: 2026-11-18
---

* Phase 1 evidence: `live_proof.py` and `rep_probe.py` read credentials at runtime, mask emails and write JSON and PNG files; no Azure resource is created.
* Phase 2: one index row and one log entry; no earlier log entry is edited.
* Phase 3 checks: relative-link resolution in the new note, `git diff --check`, grep of the evidence folder for the credential values (without printing them), 53 local API tests.
* Exit: per-criterion proven/unproven table present in the research note and the changes record.
