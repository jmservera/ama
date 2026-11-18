# Plan: issue 350 live parity proof, re-run r2 (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src change; rpi-checks.py --all not run).
Research: [research](../research/2026-11-18-issue-350-live-r2-research.md). Details: [details](../details/2026-11-18-issue-350-live-r2-details.md). Critique: [critique](critiques/2026-11-18-issue-350-live-r2-critique.md).

## Phases

* [x] Phase 1: measure the ten criteria on the live demo (read-only) and retain raw output, screenshots and scripts.
* [x] Phase 2: add the research note, index row and log entry; record the per-criterion table in the changes record.
* [x] Phase 3: validate links and the diff, scan for secrets, delete temporary session files, review once, commit.

## Decisions

* Prove only what a read-only run can show; do not change Easy Auth, create a model release, seed the law store, enable the token store or write cases.
* Do not edit src. Defects found (time status 500, CSV mine versus list, anonymous browser API 302) become follow-ups.
