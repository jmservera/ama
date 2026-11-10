<!-- markdownlint-disable-file -->
# Details: issue 1383 operational retry

Plan: [plan](../plans/2026-11-10-issue-1383-operational-retry-1110-plan.md).

## Phase 1

* File `.github/rubric/README.md`, append to the end of the existing run 42812941091 subsection (after the "Remaining uncertainty" list), plain ASCII.
* Text states: the original D1 witness chain recorded six `ok` boundaries and a last `commit-complete` event that was refused because the caller passed the non-hex string `HEAD` as the commit claim; the original evidence and commit `5c8a856c2dbee53d1aa8f7030524afa9569e7451` are kept unchanged; a separately recorded prospective operational retry (2026-11-10) did not repair or append to that chain and is a local observational record, not host or model attestation. The incident diagnosis and its limits are unchanged.

## Phase 2

* Changes record lists exact files; one self-review; commit identity from `gh api user`; Copilot trailer.
* Final marker: `git rev-parse HEAD` in one call, inspect, then a separate call passing the literal 40-hex SHA.
