---
title: Research for #1847 nomination bootstrap isolation (live demo run)
ms.date: 2026-11-23
---
# Research (#1847)

Disposition: executed. Planning Readiness: Ready.

* Issue criteria 4 and 5 are ticked; 1, 2, 3 and 6 are open. Closure audit 2026-11-19 and three earlier re-runs exist.
* Fresh probes on head b11b8259bd (source, editable, noneditable layouts; both orders) show supported layouts share `ConflictError`, `GateError`, `Store` and patch-target identity and the foreign layout is rejected explicitly. No bootstrap defect found.
* The issue is test-harness only; live revisions ca-cutover-test-demo-api--0000054 and ca-resident-demo--0000026 confirmed read-only, no Azure change.
* Only gap: criterion 6 (full gate receipt), forbidden for this worker and owner-gated.
* Evidence: docs/reference/research/nomination-bootstrap-isolation-rerun-1847-2026-11-23.md
