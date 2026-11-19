# Critique: issue 1840 live plan (one pass)

Date: 2026-11-18. Executed once on the final candidate plan.

Verdict: approve with direct dispositions.

* Finding 1 (applied): do not recreate `old_image_sql_probe.py` from the issue prose. Reconstruction would produce a file unrelated to pin `510fd90f` and false assurance. Plan records a blocker instead.
* Finding 2 (applied): changes record must carry a per-criterion table marking every criterion unproven, with the precise reason.
* Finding 3 (applied): tier. No source change, so the focused tier applies; the issue's full-tier default is noted as applying once the fix lands. `rpi-checks.py --all` is not run.
* Finding 4 (applied): demo Azure authority does not make an offline fixture defect provable live; record that explicitly.

No conflict with confirmed owner decisions. No user decision required.
