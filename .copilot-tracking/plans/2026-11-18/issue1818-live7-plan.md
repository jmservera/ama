<!-- markdownlint-disable-file -->
# Issue 1818 live round 7: plan (Refs #1818)

Tier: focused. No `src/`, SQL schema, infra definition or deployment change in the repository; the live run uses existing demo resources and one temporary job.

* [x] Phase 1: research and reuse of rounds 1 to 6 (see research note).
* [x] Phase 2: bounded live send. Temporary job `job-demo-live7` from the existing `zava-forward-api:demo-1818live6` image, 3 homes x 3 slots = 9 messages (cumulative 54 of 200), then delete the job and temporary role assignments.
* [x] Phase 3: Playwright proof, desktop 1440x900: employee map cards for the three demo homes and resident `#sec-sensors`. Screenshots and card text held outside the repository under the evidence dir; ids redacted in the note.
* [x] Phase 4: research note under `docs/reference/research/`, index and log entries, per-criterion table in the changes record, review, one local commit.
