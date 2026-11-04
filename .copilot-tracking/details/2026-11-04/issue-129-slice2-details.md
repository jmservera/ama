# Issue 129 slice 2 details

* Bundles table mirrors the protocol; O16 is in two bundles and is only a key in atlas_ids, so effort is counted per run, not per opportunity.
* compare_bundle requires both arms on each case and all target-zero counts; any nonzero count sets stop and lists breaches.
* Output carries the constructed-case evidence label, capacity note and assistance-not-available note.
