# Plan: issue 954 composed-source browser validation (2026-11-09)

Task `issue-954-composed-browser`; research `.copilot-tracking/research/2026-11-09-issue-954-composed-browser-research.md`; details `.copilot-tracking/details/2026-11-09-issue-954-composed-browser-details.md`.

Tier: owner-selected DEMO focused. Selected check: ONE actual synthetic Chromium run of the unchanged typed checker, covering the 13 detector fixtures, the exact expected negative control, the real 503 and 403 quiet receipts, the actual false client-flag transition, the identity sentinel and no new photo request. No weaker fixture or assertion, no new test source or config.

Admission: one actual holder check (`fuser` on `/tmp/ama-rpi-heavy.lock`), then ONE nonqueued `flock -n -E 99` admission (99 distinguishes a lock conflict from a checker failure), with the `obs` directory created beforehand. Expected output: exactly 83 PASS lines and one expected control FAIL. If busy, record unadmitted and stop: no wait, poll, sleep loop, retry loop or kill.

## Phases

* [ ] Phase 1: commit research, plan, details and the one critique BEFORE the holder check and the run (this commit).
* [ ] Phase 2: record the checker SHA-256 and git blob before; holder check; one nonqueued admission with raw command, stdout, stderr, exit, time and observation receipts in a session-owned directory (`evidence-954-composed-browser`).
* [ ] Phase 3: record the checker SHA after, tool versions and the raw `MANIFEST.sha256`; classify the result against the plan. A failure is reported as failed, never waived.
* [ ] Phase 4: changes, one review, state; commit with the privacy email and trailer; freeze a clean records-only head whose tested source equals `271ea1440`.
* [ ] Phase 5: handoff `handoff-954-composed-browser.md`; no push or PR.

## Boundaries

* No source, test, config, product, API, UI, workflow or dependency change; checker SHA must be unchanged (`62030130...a6db`).
* No merge, rebase, amend, stash, force, push, PR, issue or board write. No `rpi-checks --all`, SQL, cloud, model, private data, live credential or global install.
* Budget: no correction cycle spent; C1, C2, C3 spent, two of five remain; no reset or grant. `Refs #954`.
* Earlier failures, reviews, C1 to C3 evidence stay unchanged. Functional f41 current-head qualification, one batched push and fresh hosted CI belong to the coordinator; no merge claim.
