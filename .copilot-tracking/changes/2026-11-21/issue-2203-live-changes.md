# Issue 2203 changes record

Refs #2203. Tier: FOCUSED (docs only, no src change). Hosted CI was not observed and `rpi-checks.py --all` was not run.

## Files changed

* `docs/capstone/demo/runbook.md`: new "Live Demo Status (2026-11-21)" section with Observed and Not verified columns; five-home section kept (a regression test parses its table) but relabelled as a superseded historical target; preflight and sensor fallback text updated for the 20-home cohort.
* `docs/reference/README.md`, `docs/reference/log.md`: index pointer and appended log entry.
* `docs/reference/research/issue-2203-runbook-live-2026-11-21.md` and `docs/reference/research/issue-2203-live-2026-11-21/`: evidence note, probe scripts, secret-free JSON results and screenshots.

## Validation

* `src/core` `tests.test_generated_dataset`: OK.
* `tests.test_home_sensors_tab`: 21 tests OK.
* Link and anchor check of the runbook: no missing links or bad anchors.
* Secret scan: one benign selector hit (`input[name=passwd]`); no credentials retained.
* Prose detector (sloptrim) was not found locally; scoring unavailable. No em dashes in the edited prose files.
* No throwaway Azure resources were created.

## Per-criterion table

| # | Criterion | Status | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Cohort, cadence, consent mix, resident checkbox, chat routing, charts, operator-triggered AI scope with dated status | Partly proven | Cohort, cadence, consent mix and charts observed live. Checkbox observed absent live (#2192 not deployed). Chat panel inventoried, no question sent. AI scope not re-read live (1288 r6 cited); forecast endpoint timed out. |
| 2 | Stale five-home table replaced or relabelled; links checked | Proven | Relabelled as historical; link check and `test_generated_dataset` pass. |
| 3 | Offline-sensor alert, role proof, hardening status | Partly proven | Documented. Live offline alert unproven (no stale home; local test only). Role observed as Retrofit Programme Manager; wrong-role denial unproven (one account). Hardening read from Azure: off or unset on most apps, enforced on agents app. |
| 4 | Honest Observed vs Not verified wording | Proven | Every status row has both columns. |
