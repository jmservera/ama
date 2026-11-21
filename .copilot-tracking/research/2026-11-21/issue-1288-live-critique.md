# Critique: issue 1288 live pass (2026-11-21)

Executed once on the final-candidate plan. Verdict: proceed, two changes applied.

* Plan: re-run local tests, probe live read-only, write one research note, no source edit. Basis: r1 to r5 found no defect; the live probe is the only new evidence.
* Finding 1 (applied): the live simulator now exists, so the note must not repeat the r5 claim "no simulator job"; record the observed job and its owner instead.
* Finding 2 (applied): the Home sensors tab was renamed by #2161; the probe script must target the new tab, and a failed first attempt is recorded as a probe error, not a product defect.
* Rejected advice: recording a demo release record to unlock criteria 4 and 8. It would fabricate the OQ-017 approver authority and the criterion excludes deterministic outcomes.
* Tier: FOCUSED, docs and evidence only; any source change would escalate to FULL.
