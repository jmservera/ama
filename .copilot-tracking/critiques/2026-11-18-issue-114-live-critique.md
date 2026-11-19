# Critique: issue 114 live plan (single worker pass, 2026-11-18)

Verdict: proceed.

* Risk: ticking C1 on the strength of local tests only. Disposition: accepted as the owner said to tick if tests on main prove it; the deployed-image gap is stated as an adverse finding and C1 is marked proven for main, unproven for the deployed image.
* Risk: C3 asks for a throwaway server. Disposition: Azure SQL point-in-time restore cannot target another server; the drill restores to a throwaway database on the same server and states the limit.
* Risk: the 30-minute run wrote about 400 synthetic call-log rows to the live demo ledger. Disposition: authorised synthetic demo, disclosed.
* Risk: another worker used the same server concurrently. Disposition: disclosed as a confounder for DTU peaks and restore duration.
