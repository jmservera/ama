---
title: Issue 2201 live4 critique, 2026-11-22
---

Verdict: approve with direct dispositions. Executed once.

* Risk: counting 12:00 as a standing-config success. Disposition: state that it ran with `--seconds 240`; report the standing-config streak as two and not current.
* Risk: attributing the failures to the batch setting or to SQL saturation. Disposition: label as inference; the 13:30 failure with unchanged settings and 100 percent DTU in succeeded windows rule out a proven cause.
* Risk: opening the workspace network to read logs. Disposition: rejected; it is a production change the owner excluded. Record the refusal.
* Risk: naming operators. Disposition: describe the starter as scheduler or signed-in operator principal; do not record identities.
* No source change; focused tier, no gate run.
