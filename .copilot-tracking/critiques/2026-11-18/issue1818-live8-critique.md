<!-- markdownlint-disable-file -->
# Issue 1818 live8 critique (single pass)

Verdict: proceed with amendments.

* C1 Do not carry the held commit's research, plan or log artifacts: applied (source and infra text only).
* C2 Wider grant: the fix adds `INSERT` on `dbo.sensor_register` to the receiver. Applied: grant is the narrowest that works; the risk is documented in the note as a deploy-time, human-approved change.
* C3 The live walkthrough criterion must not be claimed from this commit: applied; it rests on round 7 evidence of the deployed demo image, not this branch.
* C4 FULL gate blocked by the heavy lock: applied; reported as outstanding, not simulated.
