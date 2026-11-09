# Plan: issue 954 C1 checker detector correction (2026-11-09)

Task `issue-954-c1-detector`; research `.copilot-tracking/research/2026-11-09-issue-954-c1-detector-research.md`; details `.copilot-tracking/details/2026-11-09-issue-954-c1-detector-details.md`.

Tier: owner-selected DEMO targeted. Selected: ruff check/format, the browser checker for 503 and 403 (one nonqueued admission), `test_photo_availability`, Core `test_scenario_manifest` (8) and `test_needs_inventory` (11). No `rpi-checks --all`, SQL, cloud, model or credential.

## Phases

* [ ] Phase 1: commit research, plan, details and critique BEFORE any checker edit (this commit).
* [ ] Phase 2: edit only `src/api/checks/photo_flag_stale_browser_check.py`: replace the disruptive detector and add an in-checker detector self-test.
* [ ] Phase 3: lint and format, one nonqueued holder check, then one browser admission covering the self-test, 503 and 403; then the three unit selections. Raw logs and exits stay outside the repo.
* [ ] Phase 4: review the checker against freshly fetched web guidelines, record outcome; correct only reproduced defects within budget.
* [ ] Phase 5: changes, review, state, handoff; commit; freeze.

## Boundaries

* Checker only. No `app.js`, `index.html` or API change.
* Budget: C1 uses one cycle after the source edit; four remain. No reset or extra grant.
* If the heavy lock is busy: pause immediately and report; no loop, sleep, retry waiter or bypass.
* Old failures and the original ordering are preserved unchanged.
* `Refs #954`; no acceptance tick.
