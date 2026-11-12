<!-- markdownlint-disable-file -->
# Research: #1402 cycle 2 post-parent integration (C2 of 3)

Date 2026-11-11. Branch `fix/aftercare-blank-state-1402-1111`, local HEAD `e8468bcc386dc9eb49763e490c9ae09a7f04e870` (tree `86869c0191620c2259aef6a12217bad9e17b4568`), C1 independently approved (report `files/independent-1402-c1-e8468-1111.json` in root session 38e61c82, read in full).

Research disposition: executed (git ancestry and diff inspection; the C1 research stays valid and is reused, not relabelled).

## Evidence

* Parent #1456 merged into main as squash `a3862eed4a324b13715eeebf0c98053d9079dec1` (2026-11-11T20:04:04Z); `origin/main` fetched equals it, tree `ab22886c8202b843de0afb233d3a2dc4c64178be`; its first parent is `ba65039c2177694bd3d9532d86dd494551fcc3de`.
* `git diff 2f7465c57 origin/main` on `aftercare_intake.py` and `test_aftercare_intake.py` is empty: the issue-owned files are byte-identical between the old parent topic and merged main, so the child commits should rebase without source conflict. Main's other 47 changed files are unrelated: tracking files plus `src/api/tests/test_permit_sql.py` and `.github/rubric/scores/latest.json` (corrected per critique CK-03).
* Owner decision: child now targets `main` directly, not the merged parent topic. Rebase only the three own unpushed commits (`6ac95f78b`, `3d59c1abe`, `e8468bcc3`) from `2f7465c57` onto `origin/main`. No push.
* C1 report provenance limits (preserved): only red-1/red-2 and green-1 have import hashes; later attempts have explicit paths and chronology only; original author review was non-independent and its store-test import failed (missing `dataset`); green-3 ran zero tests (exit 5); red-1 had author test bugs; lint-1 failed on a long line.
* Authority: C1 spent, C2 admitted only for integration and requalification, C3 unadmitted. No source or test correction authorised.

## Planning Readiness

Ready. Stop condition: any source or test conflict, or any new failure, stops publication pending explicit correction admission.
