# Issue 444 main lineage integration plan

Date: 2026-10-25. Research: ../../research/2026-10-25/issue444-main-lineage-integration-research.md. Details: ../../details/2026-10-25/issue444-main-lineage-integration-details.md.

## Phases

* [x] Phase 1: Independent critique of this plan (one execution), apply compatible findings before any merge.
* [ ] Phase 2: Merge origin/main (36996d70 or current) into the branch with a merge commit; resolve log.md keeping both sides.
* [ ] Phase 3: Fix only direct compatibility failures inside #444 scope; stop if a substantive shared auth change is required.
* [ ] Phase 4: Focused and full validation on the merged tree, plus exact-head browser check on a disposable port and data dir.
* [ ] Phase 5: Changes artifact, one independent Review of the integration, then the commit of evidence.
* [ ] Phase 6: Complete local gate on the clean head, new external dir, lock-timeout 14400, then official verify-receipt. Then push and open a DRAFT PR referencing #444 (no closing keyword).

## Acceptance

* History preserved: merge commit, no reset, amend, rebase or force-push.
* Original 2026-10-24 artifacts and reviews unchanged.
* Running services and /tmp/ama-444-preview-data untouched.
* All ordered RPI evidence is committed before the gate; no receipt-only commit.
