# Critique: issue 2254 run 5 (2026-11-23)

Executed once on the final candidate. Verdict: proceed.

* Risk: a test that passes by luck of fixture data. Amendment: pick open case ids and assert the specific ids are absent from the list, not only the totals.
* Risk: the test passes without the fix. Amendment: revert the `hazard` repair temporarily and show failure (done in implement).
* Scope: test-only; no src change, so the focused tier applies and rpi-checks --all is not run.
Executed once. Verdict: proceed with one amendment.

* Amended: do not add `decision` to the repaired columns. `page_cases` already bypasses the cached `decision` column because consent authority can expire without a row write, and `resident_status` depends on current context, so repairing it could rewrite rows on every start. Repair `support`, `days` and `fstatus` only; they are pure functions of the body.
* Risk: a legacy body that breaks `_row` is already skipped by the existing try/except.
* Risk: the repair issues an UPDATE only for rows that disagree, so a consistent database is untouched.
* Tier: this changes `src`, so the FULL tier applies by classification; the coordinator runs the gate and `rpi-checks.py --all` is not run here.
