<!-- markdownlint-disable-file -->
# Plan: #1288 ordinary main integration

Research: [research](../research/2026-11-09-issue-1288-main-integration-research.md). Details: [details](../details/2026-11-09-issue-1288-main-integration-details.md). Written and committed BEFORE the merge. Tier: owner-selected DEMO TARGETED (no blanket full gate, no rpi-checks --all, no scanners, images, browser or SQL campaign). Refs #1288 only.

## Phases

1. [ ] Commit research, plan and details before merging main.
2. [ ] Ordinary merge of fetched origin/main (cd687abad) into the run-owned branch (no rebase, amend, force or push). Preserve both source intents. Stop and record a blocker on any ambiguous intent conflict.
3. [ ] Inventory the actual merged delta and compare the source and config inputs (candidate versus main versus merged tree).
4. [ ] Run complete pinned profiles where affected: Core SDK-free (owned mktemp venv, `-e src/core[dev]` only) ruff check, ruff format --check and mypy; API SDK-enabled (core[sql,blob]) the same. Record exits. No casts, ignores, stubs or config relaxation.
5. [ ] Run targeted tests (existing only): merged ranking/Blob suites, Quality call-site dependencies, deadline, lane, consumption, inventory and assistants regressions as the details define. Capture raw logs, exits, counts and skips.
6. [ ] Decide any SQL dependency from the actual inputs; if one changed, record the exact selectors and use one non-queued `flock -n` admission, otherwise record the qualification and the reuse basis.
7. [ ] Original review of the merge, then write changes, review and state artifacts, then freeze a clean candidate.
8. [ ] Write handoff-1288-main-integration.md with identities, delta inventory, commands, counts, remaining AC and a proposed Refs body.

## Decision rules

* An unchanged-source integration does not consume E8. If a real new defect needs a productive correction, reproduce it, record E8 prospectively and keep the remaining count (E9, E10) accurate. No transport redesign.
* A missing mandatory check blocks the handoff. No cloud fallback.
* Reused historical results carry their commit identity and are labelled historical.
