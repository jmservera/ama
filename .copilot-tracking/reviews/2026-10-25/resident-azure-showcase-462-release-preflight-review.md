# Issue 462 release preflight evidence: independent review (2026-10-25)

Reviewer: rubber-duck agent, one read-only execution after the evidence was written, recomputing
from the retained raw files. Outcome: request changes (1 High, 3 Medium); all four corrected in the
evidence artifact afterwards and not re-reviewed (one review per task). Original output, unaltered:

---

## Verdict: request changes

1. High: stop threshold of 38 leaves only 12 before the 50 cap, but the deployment reserve alone is
   about 11, so it did not preserve a lag reserve. Fix: threshold = 50 minus deployment reserve minus
   explicit lag reserve.
2. Medium: priced-component subtotal not reproducible (rows sum to 4.679 to 4.689, not 5.4; variant
   5.284 to 5.294, not 6.0; 100 percent reserve of 6.0 would be 12.0, not 11).
3. Medium: Method 1 is not a defensible bound (retrofit 10.30 is a day-to-day difference, demo app total
   spans 24 Oct). Rename it an over-inclusive scenario and rely on Method 2 for the proxy.
4. Medium: the 4.017 figure is the managed-environment privateendpoint resource; eight
   Microsoft.Network/privateEndpoints add 3.280; reconcile.

Recomputed: ungrouped 25.4677 equals ResourceId 25.4677; 24 Oct 19.0959; 25 Oct 6.3718; October MTD
303.7111; Method 1 components 12.4069 (15.4069 with reserve); Method 2 about 31.6625. No hard-ceiling
claim found.

---

## Disposition (coordinator session)

All four applied in the evidence artifact: threshold now 27.8 with 5 lag and 11 deployment reserve
(current 25.5 leaves about 2.3, a thin conditional release, not a clearance); table arithmetic
corrected with explicit contingency; Method 1 relabelled and excluded from gates; private endpoint
figures reconciled. Corrections were not re-reviewed.
