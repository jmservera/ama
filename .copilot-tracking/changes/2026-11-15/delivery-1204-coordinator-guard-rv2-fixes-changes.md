<!-- markdownlint-disable-file -->
# Changes: Resolve Validator Edge-Case Defects RV-001 through RV-003 (Issue #1204 Child Loop 2)

## Metadata

* Task ID: issue-1204-rv2-fixes
* Task slug: delivery-1204-coordinator-guard-rv2-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Execution status: Complete

## Opening Implementation State

* Interpreted implementation goal: Implement `P01-T01` and `P01-T02` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` to close `RV-001`..`RV-003` and `PC-001`..`PC-003`.
* Declared scope: Full child plan (`P01`, `P01-T01`, `P01-T02`)
* First ready item: `P01-T01`
* Active blockers: none

## Completed Work

### P01-T01: Governed Negation Binding, Table-Evidenced PR Blockers, Concurrent Lane Waits, and Linked Issue Cells (`tools/check-coordinator-handoff.py`)

* Replaced unanchored clause-anywhere negation checks with anchored suffix patterns (`PROHIBITION_SUFFIX_RE` and `HANDOFF_NEGATION_SUFFIX_RE`) matching governed verbs, coordinated claim list items, inline backtick code spans, and optional trailing determiners/prepositions/quotes directly before `match_start`, rejecting coordinated conjunction bypasses (`"Never skip verification and nothing changed."`, `"Cannot merge PR #1641 yet and waiting for stakeholder feedback."`, `"Never skip verification and always claim \"nothing changed\"..."`).
* Updated `check_agent_instructions` to evaluate every `"nothing changed"` and `"unverified blocker"` occurrence per clause via `re.finditer`.
* Added `_extract_verified_evidence_numbers` and expanded `CITED_BLOCKER_REF_RE` (`PR #<n>` / `pull request #<n>`) so `Waiting on #1641` and `Waiting on PR #1641` pass when `#1641` is recorded in a valid blocking row's GitHub `/issues/` or `/pull/` URL, valid Markdown link, or prose evidence, while still rejecting unlisted or URL-fragment `#999` bypasses.
* Added `GLOBAL_WAIT_OR_PAUSE_RE`, `CONCURRENT_LAUNCH_RE` (scoped to explicit `#<n>` or `rpi-<n>` targets), and `HOLD_PREPOSITION_SUFFIX_RE` via `_has_unnegated_concurrent_launch` so active concurrent launch progress (`"Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 next."`) passes without weakening rejection of global stalls (`"Waiting for stakeholder feedback before starting #1310."`, `"Check started at 12:00Z; waiting for stakeholder feedback."`).
* Added `_parse_issue_cell` enforcing single-issue bare `#?<digits>` or `[#?<digits>](target)` Issue column cells, rejecting multi-issue cells (`#1204, #1205`), `javascript:`/`data:` links, mismatched `/issues/9999` URLs, and invalid `#anchor` targets while preserving `row.issue_number` for bare self-reference rejection (`Blocked in #1288`).

### P01-T02: Regression Subtests and Focused Validation (`tools/test_check_coordinator_handoff.py`)

* Added regression `self.subTest` cases across existing test methods (`11` test methods total, zero net additions) covering coordinated-conjunction polarity bypasses in `.agent.md` and handoff prose, bare/qualified table-evidenced PR blocker citations, unlisted PR blocker rejection, concurrent active-launch lane waits vs `before starting #1310` and `started at 12:00Z` holds, and valid/invalid Markdown-linked Issue column IDs.

## Implementation-Time Plan and Detail Updates

* Local judgment: Included `launch\w*|start\w*|dispatch\w*|spawn\w*` in `_GOV_VERB` so `_is_claim_negated` also detects negated launch verbs (`"Never launching #1310..."`) inside `_has_unnegated_concurrent_launch`.

## Validation Record

* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> passed (`All checks passed!`)
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> passed (`2 files already formatted`)
* `python3 tools/check-coordinator-handoff.py` -> passed (`Coordinator handoff guard check passed (1 target(s), 0 violations).`)
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` -> passed (`Ran 11 tests in 0.149s - OK`)
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` -> passed (`Ran 33 tests in 3.072s - OK`)
* `git --no-pager diff --check` -> passed (0 whitespace/patch issues)
* `tools/rpi-checks.py` -> intentionally not executed per explicit Focused-tier instruction (`Do NOT run tools/rpi-checks.py`).

## Blockers and Remaining Work

* Blockers: none
* Remaining work: none (`P01`, `P01-T01`, `P01-T02` complete; ready for `Review`)

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
