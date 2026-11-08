---
title: Issue 1231 author review (author-only, after changes and light checks)
ms.date: 2026-11-06
---

## Execution

Review executed 2026-11-06 after the implementation and light checks, by the implementing author, once. It is not independent. Assessed boundary: the working-tree diff on head `748526484e76dd8d0c2751bbc6c6be146aeeda63` (helper, three test/README files) against issue #1231 acceptance criteria. No human-review box is ticked; independent exact-head assessment, FULL receipt and publication are pending.

## Criteria

* Prospective Research, Plan and details committed before edits: yes (`748526484e76`, 04:41:59Z). Research flags a material-looking hard-link qualification and a guard refinement rather than hiding them.
* Deterministic regression on the real defect: met for the runner reproduction and the helper threads (RED `'2026-10-11' != '2026-10-10'`, `FileNotFoundError`).
* One record, truthful publisher, `already_published` loser, no shared-stage `FileNotFoundError`: met in GREEN.
* Finished record versus delayed contender: covered; note the old helper failed it with `FileNotFoundError`, so overwrite is still not demonstrated anywhere.
* Ownership-safe cleanup: covered, including a real failed link (injected `PermissionError` replaces the link; the stage is removed, foreign files kept). The injected error is the only non-real element and is limited to the failure path under test.
* Sequential bytes, filename, idempotence: covered; verify, policy, freshness, retention, approvals untouched (API wiring 12 tests OK).
* Separate processes: four spawned processes pass; not a forced interleaving and RED on the old helper did not fail it. Local POSIX filesystem only.
* FULL and independent assessment: pending, not satisfied.

## Findings

* Medium (open, routed to owner/deployment): hard links are now required on the archive directory; no production archive mount is defined and an SMB-style mount would refuse to publish. Needs an explicit decision before such a mount is used.
* Low (open, for assessor): the no-delete source scan was narrowed to allow the single owned-stage `os.unlink`. Behavioural tests protect records.
* Low (open): a crash between stage creation and cleanup leaves an unreferenced hidden `.tmp` stage; it is ignored by `verify` and never reused, but is not auto-removed (removing foreign files is out of scope).
* Low (limitation): Windows, network filesystems, rate and production unmeasured; one process-level test is a stress, not a proof.

## Outcome

Author-only: conformant with the focused light evidence and with the three open qualifications above. Not a conformance, FULL, independent or publication outcome. No further Review in this task; routed items are for later user-selected work.
