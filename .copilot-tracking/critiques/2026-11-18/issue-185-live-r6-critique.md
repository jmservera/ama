---
title: Issue 185 live r6 critique
ms.date: 2026-11-18
---

Executed once. Verdict: proceed with amendments, all applied directly.

* C1: Starting SAS identities DISABLED means the adapter issues no usable credential; the activation and storage step stays outside. Amendment: state this in the module docstring and in the criterion table; do not claim durable storage.
* C2: Never read keys: discard the create response; tests must fail if a key reaches a return value, `RegistryError`, `repr` or `caplog`.
* C3: Hub-wide count is not proof of teardown on a shared hub; use run-unique ids and the per-id read-back plus `list_run`.
* C4: Process note, adverse: a draft of the source edit was applied before the `implement-start` witness call. It was reverted (`git checkout src`, patch kept outside the repository) and reapplied after the changes file and witness, so the witness order is restored; the premature edit is recorded here and in the changes record.
* C5: FULL tier applies; not claimed satisfied.
