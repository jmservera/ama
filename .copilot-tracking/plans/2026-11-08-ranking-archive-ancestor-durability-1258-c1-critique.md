---
title: Ranking archive ancestor durability 1258 correction 1 critique
description: One independent critique of the correction 1 plan and drafted diff, with dispositions
ms.date: 2026-11-08
---

Independent critique (rubber-duck agent, read-only), one execution, verdict Revise. Sequencing note, recorded honestly: the code and failing-first tests were drafted and the red run captured before this critique; the critique reviewed the plan together with that uncommitted diff. The critique is not repeated.

| ID | Severity given | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | `os.path.ismount` does not detect a same-filesystem bind mount, so host parents can still be synced and an unreadable one reports unconfirmed (the M1 symptom). | Accepted as a declared limitation, not fixed. The failure mode is fail-closed (extra sync or `committed_unconfirmed`), never a false confirmation. Parsing `/proc/self/mountinfo` is new platform-specific scope beyond the reported finding, which asks for the resolved-archive mount check. Reported for the owner. |
| PC-002 | Blocking | `realpath` discards the configured symlink path, so a symlink or its parent created by another party may be unsynced. | Rejected for this change with reason. `publish` creates directories with `makedirs` and never creates a symlink, so every entry this call creates is a real directory on the resolved chain. A symlink is operator provisioning. Recorded as a residual: durability of pre-existing operator symlinks is not asserted. |
| PC-003 | Non-blocking | An execute-only ancestor (for example a 0711 home) makes every publication unconfirmed. | Accepted and made explicit. This is the fail-closed reading of the first criterion and the cost of removing the permission inference. No silent skip. Owner acceptance of the deployment-permission tradeoff and a test with the real deployment permissions are open items. |
| PC-004 | Non-blocking | `ismount` treats a Btrfs subvolume root as a mount point and may stop before an unsynced enclosing entry. | Accepted as a declared limitation; supported filesystems are not enumerated in this change. Reported, not fixed. |

Also confirmed by the critique: the preserved red run supports H1 and the mocked M1 case, and the open-failure test already passed before the fix (it pins existing behavior, not a red case). No heavy gate was run.

Net plan effect: no change to scope or code. Limitations PC-001 to PC-004 are carried into the Changes and Review records as open residuals.
