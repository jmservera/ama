<!-- markdownlint-disable-file -->
# Changes: Resolve Coordinator Handoff Guard Review Defects RV-001 through RV-003 (Issue #1204 Child Loop)

## Metadata

* Task ID: issue-1204-rv-fixes
* Task slug: delivery-1204-coordinator-guard-rv-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Execution status: Complete

## Opening Implementation State

* Interpreted implementation goal: Implement `P01-T01` and `P01-T02` to close routed parent review defects `RV-001`, `RV-002`, and `RV-003` along with critique dispositions `PC-001` through `PC-004` while keeping the original parent review log untouched.
* Declared scope: Full child plan (`P01`, `P01-T01`, `P01-T02`)
* First ready item: `P01-T01`
* Active blockers: none

## Completed Work

### P01-T01: Validator Bypass Hardening and Coordinator Write-Time / Pagination Guidance (`RV-001`, `RV-002`)

* Updated `tools/check-coordinator-handoff.py`:
  * Replaced whole-line `NEGATION_GUARD_RE.search(line)` skipping with clause-scoped `_is_claim_negated(line, match_start)` evaluated per match across `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, and `CITED_BLOCKER_REF_RE`, masking inline backtick punctuation and preserving CLI `--flag` tokens (`--state`, `--limit`).
  * Expanded `WAITING_OR_PAUSE_RE` and `CITED_BLOCKER_REF_RE` to cover general `waiting on` / `waiting for` phrases, enforced pre-summary completeness across all classification tables (`lineno <= last_table_end` -> `summary-before-classification-table`), and validated unnegated `CITED_BLOCKER_REF_RE` blocker references even on standalone non-idle/non-waiting summary lines (`Summary: blocked on #999`), flagging `unverified-blocker-reference` when `ref_row is None`, non-blocking, or missing a verified blocker link.
  * Added `_inspect_blocker_links` with document-wide `valid_heading_slugs`, `GITHUB_FRAGMENT_ANCHOR_RE` (`#issuecomment-`, `#pullrequestreview-`, `#discussion_r`), `broken-blocker-anchor` emission, `MD_LINK_RE`/`URL_RE` span stripping before `ISSUE_REF_RE`, and tightened `ISSUE_REF_RE` (`(?![A-Za-z0-9_-])`) so digit-prefixed broken anchors (`#999-nonexistent`) never fall through.
  * Added `_iter_normalized_prose_clauses` in `check_agent_instructions` to verify prohibition-governed polarity across ~80-column wrapped sentences, reject single-section or global affirmative polarity inversions (`inverted-guard-polarity`), require `--expect-open-issues`, `--open-issues`, and `gh api --paginate` in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and accept `gh api --paginate .../issues` and `.../pulls` provenance in `_validate_section`.
* Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md`:
  * Prescribed write-time live expectation flags (`--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, `--expect-head`, `--expect-base`, `--open-issues`) alongside offline `--handoff <path>` structural validation.
  * Documented PR-excluding `gh api --paginate` saturation handling (`select(.pull_request == null)` when `--limit 500` returns `500` items, and `/pulls` pagination when `--limit 200` returns `200` items), cross-referenced across `Liveness and stop decision`, `Stabilization checkpoints`, and step 5.

### P01-T02: Adversarial Regression Tests, HVE Refresh, and Focused Validation (`RV-003`)

* Extended `tools/test_check_coordinator_handoff.py` (`11` test methods total, `<= 12` ceiling, `0` removals):
  * Added global and single-section polarity-inversion subtests plus `--expect-open-issues` and `gh api --paginate` contract subtests to `test_agent_instruction_guard_rejects_missing_contracts`.
  * Added `test_adversarial_rv001_handoff_bypasses_rejected` exercising later-clause/colon/comma negation bypasses, CLI `--state`/`--limit` preservation, general `Waiting for ...` phrases, split classification tables after `"Nothing changed"`, absent and standalone cited blockers (`Waiting on #999`, `Summary: blocked on #999`), broken and digit-prefixed `#anchor` links vs valid `#blocker-ledger` headings, and `gh api --paginate` provenance.
* Refreshed `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` with current `.github/agents/ama-backlog-delivery-coordinator.agent.md` SHA-256 (`cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`, 1155 lines) while retaining superseded parent SHA-256 (`6bca3f75f222a34d69f389ab82438a75004512fec82e070b12597f6c1d544f4d`) lineage and adding adversarial scenario `S-07`.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01`): Evaluated `CLAUSE_SPLIT_RE` over the full masked line up to `match_start` (`sep_m.end() <= match_start`) rather than slicing `line[:match_start]` prior to regex matching so comma-clause lookaheads see the claim token starting at `match_start` (catching `"Cannot merge PR #1641 yet, waiting for stakeholder feedback."` while preserving compound VP negations such as `'must never claim "nothing changed" or pause on an unverified blocker'`). No plan scope or acceptance change required.

## Validation Record

* `python3 tools/check-coordinator-handoff.py`: Pass (`Coordinator handoff guard check passed (1 target(s), 0 violations).`, exit `0`).
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`: Pass (`Ran 11 tests`, `OK`, exit `0`).
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Pass (`All checks passed!`, exit `0`).
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Pass (`2 files already formatted`, exit `0`).
* `python3 -m unittest tools/test_rpi_phase_witness.py -q`: Pass (`Ran 33 tests`, `OK`, exit `0`).
* `git --no-pager diff --check`, Markdown link/bullet-style audit, plain-ASCII (`ord(c) <= 127`) check on `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and zero-tracking-reference check on production files: Pass (exit `0`).
* `python3 tools/rpi-checks.py`: Intentionally skipped per explicit caller Focused-tier instruction (`Do NOT run tools/rpi-checks.py`).

## Blockers and Remaining Work

* Blockers: none
* Remaining work: none (`P01`, `P01-T01`, and `P01-T02` complete; ready for child `rpi-review`)

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks in a separate gate-tooling PR validated under the full gate tier (`#1294`).
