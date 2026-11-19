# Issue 117 live r3 critique (2026-11-18)

Executed once. Verdict: proceed.

* Finding: ticking the criterion on the synthetic scanner alone would overstate assurance. Disposition: applied; the criterion stays unticked and the note says why.
* Finding: changing `ZF_SCANNER` on the live demo app is a configuration change the owner did not authorise. Disposition: applied; not changed, listed as an owner follow-up.
* Finding: raw outputs must hold no secrets or tenant identifiers. Disposition: applied; probe redacts e-mail addresses and the FQDN is not retained.
