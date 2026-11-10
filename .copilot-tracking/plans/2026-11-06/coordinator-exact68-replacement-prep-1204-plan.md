---
title: Plan for exact-68 replacement preparation (issue 1204)
ms.date: 2026-11-06
---

Research: [research](../../research/2026-11-06/coordinator-exact68-replacement-prep-1204-research.md). Details: [details](../../details/2026-11-06/coordinator-exact68-replacement-prep-1204-details.md).

## Phases

* [x] Phase 1: prospective Research, Plan, details and a PENDING exact-68 journal with restore map (this commit, intent only).
* [ ] Phase 2: freeze the clean head, then external-only full snapshot, inventory, readback, 68 restore with actual modes, protected checks. No repository writes.
* [ ] Phase 3 (later, root-authorized only, not in this task): replace exactly the 68 transcripts with the tracked bundle C reference, new journal, final 97-unit repeat, range check, dedicated post-removal Review.

## Constraints

* Only the 68 paths in manifest SHA-256 643fb9ad... are ever eligible. `exit-codes.json`, report 005, originals, adverse records, source blob acefb44a, refs, `/tmp/h1204` and all unselected files stay intact.
* No normalization, suppression, gitattributes change, deletion or prune in this task.
* Review gate: Phase 2 results are consumed by root; the dedicated Review runs after any actual replacement.
