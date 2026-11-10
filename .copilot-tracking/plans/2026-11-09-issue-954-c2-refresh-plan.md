# Plan: issue 954 C2 non-vacuous false-refresh proof (2026-11-09)

Task `issue-954-c2-refresh`; research `.copilot-tracking/research/2026-11-09-issue-954-c2-refresh-research.md`; details `.copilot-tracking/details/2026-11-09-issue-954-c2-refresh-details.md`.

Tier: owner-selected DEMO focused. Selected: checker self-tests and the new negative control, ONE synthetic Chromium run covering the negative control, 503 and 403 (one nonqueued admission on `/tmp/ama-rpi-heavy.lock`), `test_photo_availability`, Core `test_scenario_manifest` and `test_needs_inventory`, pinned Ruff 0.17.1 check and format. No `rpi-checks --all`, SQL, cloud, model, credential or global install.

## Phases

* [ ] Phase 1: commit research, plan, details, critique and the dated original-review qualification BEFORE any source edit or validation (this commit).
* [ ] Phase 2: edit only `src/api/checks/photo_flag_stale_browser_check.py`.
* [ ] Phase 3: lint/format, holder check, one nonqueued admission, unit selections; save commands, outputs, exits, tool versions and checker SHA before/after outside the repo.
* [ ] Phase 4: review against freshly fetched web guidelines; correct only reproduced defects within budget.
* [ ] Phase 5: changes, review, state, handoff; commit; freeze.

## Boundaries

* Checker only; product UI/API untouched.
* Budget: C2 of five total; three remain after C2; no reset or extra grant.
* Lock busy: stop heavy work, finish light checks, report unadmitted, never claim the browser passed; no wait, poll, sleep loop or kill of other holders.
* Old failures, C1 evidence and original review text are preserved; `Refs #954`; no acceptance tick.
