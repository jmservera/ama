<!-- markdownlint-disable-file -->
# Review: resident-showcase-azure-deploy-462

Date: 2026-11-17. One review pass by the worker (not an independent reviewer; independent exact-head assessment
stays with the coordinator). Boundary: the Azure deploy of main 488c5a0c8 plus the documentation diff.

| Check | Result |
|---|---|
| Image-only change, other metadata unchanged | Pass (projected diff showed only image) |
| Registry state restored | Pass after manual correction; defect in the trap script recorded (wrong JSON field) |
| No SQL, secret, role, tenant, employee app or SKU change | Pass (no such command run; SQL Standard 10 read back) |
| Real HTTPS login to correct synthetic home | Pass |
| Wrong password and unknown email identical message; CSRF; forged session; staff routes; sign-out | Pass |
| Credentials never printed or committed; fake-email screenshot deleted | Pass |
| `infra/tests` resident and hosting tests | Pass (36 and 16 tests) |
| Cost admission | Partial: RG-only USD 85.39 vs cap 700; all-in forecast unknown |

Findings, routed to later work:

* R-01 Medium: replica was still running at readback (scale-to-zero cooldown); confirm 0 later.
* R-02 Low: password-in-response was not asserted separately; server stores only a verifier.
* R-03 Low: the push script's rule removal should read `ipAddressOrRange`; fix before reuse.
* R-04: desktop only, no whole-WCAG, human, legal or production acceptance; #444/#455 criterion not addressed here.

Outcome: conformant for the deploy-and-verify scope with the open items above; correction cycles used: 0.
