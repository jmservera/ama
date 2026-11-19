<!-- markdownlint-disable-file -->
# Phase Details: Resolve Validator Edge-Case Defects RV-001 through RV-003 (Issue #1204 Child Loop 2)

## Metadata

* Task ID: issue-1204-rv2-fixes
* Task slug: delivery-1204-coordinator-guard-rv2-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Governed Negation Binding, Table-Evidenced PR Blockers, Concurrent Lane Waits, and Regression Subtests

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update `tools/check-coordinator-handoff.py` for `RV-001`, `RV-002`, and `RV-003`

#### Purpose

Close coordinated-conjunction negation bypasses while supporting valid coordinator table-evidenced PR blocker references, concurrent active-launch lane-wait reporting, and Markdown-linked Issue column IDs.

#### Context

1. Anchored prohibition suffix (`_is_claim_negated` and `check_agent_instructions`, `RV-001`, `PC-001`):
   * Match `PROHIBITION_SUFFIX_RE` (for agent instructions) and `HANDOFF_NEGATION_SUFFIX_RE` (for handoff prose) against `trailing_clause` anchored at `\s*$`, handling literal `` `[^`]*` `` code spans, inflected verbs (`repeat\w*`, `claim\w*`, `report\w*`, `emit\w*`, `say\w*`, `stat\w*`, `writ\w*`, `assert\w*`, `paus\w*(?:\s+on)?`, `wait\w*(?:\s+(?:on|for))?`, `cop(?:y|ied|ying)`, `carr(?:y|ied|ying)\s+over`, `cach\w*`, `be`, `rel(?:y|ied|ying)\s+on(?:\s+`[^`]*`)?(?:\s+(?:counts?|shas?|sessions?|snapshots?))?`), coordinated claim list items, and optional trailing determiners/prepositions/quotes (`on`, `for`, `a`, `an`, `the`, `any`, `global`, `["'`]`) right before `match_start`.
   * Scan all `"nothing changed"` and `"unverified blocker"` occurrences in each clause via `re.finditer` in `check_agent_instructions`.
2. Table-evidenced PR blocker lookup (`_validate_section`, `RV-002`, `PC-002`):
   * Include optional `PR`/`pull request` qualifiers in `CITED_BLOCKER_REF_RE`.
   * Build `verified_blocker_evidence_nums: set[int]` from valid blocking rows (`active session`, or `human-blocked`/`dependency-blocked` with `has_valid_blocker_link=True`) using GitHub `/issues/(\d+)` and `/pull/(\d+)` URL/link-target matches plus URL/link-stripped `ISSUE_REF_RE` prose matches (excluding self `row.issue_number` and broken anchors).
   * Check `classified_by_num` first, then `verified_blocker_evidence_nums`.
3. Global wait/pause vs concurrent active-launch lane wait (`_validate_section`, `RV-002`, `PC-002`):
   * Guard `GLOBAL_WAIT_OR_PAUSE_RE` with `not _is_claim_negated(line, m.start())` and cover `before`/`until`/`prior to`/`instead of` stall forms.
   * Require `#<n>` or `rpi-<n>` delivery targets in `CONCURRENT_LAUNCH_RE` (`\b(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\s+(?:tmux\s+session\s+|worker\s+|session\s+|issue\s+)?(?:#\d+\b|`?rpi-\d+[A-Za-z0-9_.-]*`?)`) not preceded on the same clause by `before|until|without|instead of|prior to` or negation.
4. Single-issue Markdown-linked Issue column IDs (`_parse_issue_cell`, `RV-003`, `PC-003`):
   * Accept only `^\s*#?(\d+)\s*$` or `^\s*\[([^\]]+)\]\(([^)\s]+)\)\s*$` with `#?(\d+)` label, rejecting multi-issue cells, `javascript:`/`data:` schemes, mismatched `/issues/<other>` URLs, and invalid `#anchor` targets.

#### Likely Targets

* tools/check-coordinator-handoff.py

#### Dependencies

* none

#### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0`

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Lock regression subtests for every `RV-001`..`RV-003` edge case and synchronize artifact metadata before Review.

#### Context

* Extend `test_agent_instruction_guard_rejects_missing_contracts` with `"Never skip verification and always claim \"nothing changed\" while open issues remain unclassified."`.
* Extend `test_valid_active_and_multi_role_stacked_handoffs_pass` with Markdown-linked Issue IDs (`[#1204](https://github.com/jmservera/ama/issues/1204)`) and concurrent active-launch lane-wait prose (`"Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 next."`).
* Extend `test_valid_waiting_and_idle_summaries_pass_when_all_open_issues_classified` with table-evidenced PR blocker prose (`"Waiting on #1641 for parent PR merge."` when `#1302 | dependency-blocked | PR #1641` is in the table).
* Extend `test_adversarial_rv001_handoff_bypasses_rejected` with `"Never skip verification and nothing changed."` and `"Launched rpi-1204; pausing tick on #1288."` / `"Waiting for stakeholder feedback before starting #1310."`.

#### Likely Targets

* tools/test_check_coordinator_handoff.py

#### Dependencies

* `P01-T01`

#### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0`
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` exits `0` (`11` tests)
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` exits `0`
* `git --no-pager diff --check` exits `0`
