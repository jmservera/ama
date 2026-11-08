---
title: Issue 1231 author review r2 (owner-approved hard-link contract)
ms.date: 2026-11-06
---

## Execution

Executed once by the implementing author after the changes and the checks above; not independent, no human-review box ticked. Boundary: head `a5bf43d4d` plus the two test edits, against the owner-approved contract.

## Assessment

* Atomic hard link required, fail closed: met by reading and tests. Only `FileExistsError` is handled; any other `OSError` propagates and the runner reports `publish_failed`. Both new tests cover the unsupported-filesystem errno.
* No publication on failure, no unsafe overwrite, no silent fallback: met (no record, foreign files byte-identical, later publish succeeds).
* Truthful winner, immutable existing records, owned-only cleanup: covered by the R1 tests, re-run green here.
* Owner decision scope: recorded as limited to the quoted compatibility contract. It does not approve any mount, deployment, retention, legal or policy step, or publication.

## Findings and qualifications

* Low (open): the new tests are characterization tests; they passed before and after, so they prove no new fix. R1's open owner question is now resolved by the owner, but R1 records were not edited and still show it as open at their time.
* Low (open): the refusal text "Check the archive location and rerun." does not name hard links. Left unchanged to avoid churn; a later user-selected item.
* Low (open, from R1): crash-orphaned hidden stage files are not auto-removed; overwrite of a finished record is still not demonstrated.
* Limitation: errno injection only; light evidence with newer tool versions than pinned.

## Outcome

Author-only: conformant with the owner contract on light evidence. FULL, independent feature review and publication are PENDING. No further Review in this task.
