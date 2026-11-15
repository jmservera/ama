<!-- markdownlint-disable-file -->
# RPI Phase Details: Resolve Coordinator Handoff Guard Review Defects RV-001 through RV-003 (Issue #1204 Child Loop)

## Metadata

* Task ID: issue-1204-rv-fixes
* Task slug: delivery-1204-coordinator-guard-rv-fixes
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md
* Evidence sources: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Coordinator Handoff Validator, Instruction Hardening, and Adversarial Regression Suite | ready | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Coordinator Handoff Validator, Instruction Hardening, and Adversarial Regression Suite

### Context

Parent review `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` verified overall structure for Issue #1204 (`AC1`-`AC4`) and routed three defects (`RV-001`, `RV-002`, `RV-003`) to `rpi-implement`.

### Intent

Close all bypasses reproduced during parent review without expanding scope outside the three Issue #1204 implementation targets and the HVE qualification record.

### Boundaries

* Included: `tools/check-coordinator-handoff.py`, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/test_check_coordinator_handoff.py`, `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`
* Excluded: Parent review/critique artifacts, `tools/rpi-checks.py`, git push, and PR creation

### Likely Targets

* tools/check-coordinator-handoff.py: Clause-scoped negation, expanded waiting regex, pre-summary table completeness, absent cited-blocker check, local `#anchor` heading check, and polarity-aware agent rule checks
* .github/agents/ama-backlog-delivery-coordinator.agent.md: Write-time `--expect-*`/`--open-issues` flags on `--handoff` validation and saturated-limit `gh api --paginate` requirement
* tools/test_check_coordinator_handoff.py: Adversarial regression subtests for `RV-001` and `RV-002`
* .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md: Updated SHA-256 and expanded behavioral scenarios

### Dependencies

* none

### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0`
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` exits `0`
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` exits `0`

### Completion Evidence

* Updated files, passing command outputs, and refreshed HVE SHA-256 recorded in `.copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-changes.md`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `tools/check-coordinator-handoff.py` and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`RV-001`, `RV-002`)

#### Context

1. In `tools/check-coordinator-handoff.py`:
   * `_is_claim_negated(line: str, match_start: int) -> bool`: split `line[:match_start]` only at `[;.!?:]` or whitespace-bounded `\s+--\s+` (never bare `--`, preserving CLI flags like `--state` and `--limit`, and with no cross-clause bullet-prefix carryover so `"Do not launch: nothing changed"` is never masked) and check `NEGATION_GUARD_RE` only in the trailing clause segment immediately preceding `match_start`. Evaluate `_is_claim_negated` per match across `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, and `CITED_BLOCKER_REF_RE` (`PC-002`).
   * Expand `WAITING_OR_PAUSE_RE` to match `\bwaiting\s+(?:on|for)\b` and expand `CITED_BLOCKER_REF_RE` to include `waiting\s+(?:on|for)`.
   * Pre-summary table ordering and completeness: require all issue-state classification tables in the section to end before any idle/waiting/pause summary line (`any(tbl.end_line > lineno for tbl in class_tables)` -> emit `summary-before-classification-table`).
   * Standalone and absent cited-blocker validation (`PC-002`): evaluate unnegated `CITED_BLOCKER_REF_RE` matches on every prose line (even when `is_idle` and `is_waiting_or_pause` are `False`, e.g., `"Summary: blocked on #999"`), flagging `unverified-blocker-reference` when `ref_row is None`, when `ref_row.state` is outside `{"active session", "human-blocked", "dependency-blocked"}`, or when `ref_row.state in LINK_REQUIRED_CATEGORIES` lacks `has_valid_blocker_link`.
   * Local `#anchor` blocker link validation in `_has_non_bare_self_link`, `_extract_classification_tables`, and `_validate_section` (`PC-002`): compute `valid_heading_slugs: frozenset[str]` across the handoff document; accept `#issuecomment-\d+`, `#pullrequestreview-\d+`, and `#discussion_r\d+` as GitHub fragments, require any other `#<slug>` Markdown link target to exist in `valid_heading_slugs` (emitting `broken-blocker-anchor` in `_validate_section` when invalid), strip `MD_LINK_RE` spans before bare `ISSUE_REF_RE` matching, and tighten `ISSUE_REF_RE` with `(?![A-Za-z0-9_-])` so `[bad](#999-nonexistent)` never falls through to `#999`.
   * Polarity-aware `check_agent_instructions` (`PC-001`): preserve `check_agent_instructions(agent_path: Path, root: Path | None = None) -> list[str]`, normalize wrapped ~80-column paragraph/bullet clauses by splitting `unfenced_body` on `\n\s*\n` and `[.;!?]` and collapsing internal `\s+` to `" "`, require at least one prohibition-governed clause (`never|cannot|must\s+not|do\s+not|forbid\w*|prohibit\w*`) for `"nothing changed"` + `"unclassified"` and for `"unverified blocker"`, reject any unnegated affirmative clause pairing `"nothing changed"` with `"unclassified"` (outside `"permitted only when ... zero open issues unclassified"`) or pairing pause/wait verbs with `"unverified blocker"`, and require `--expect-open-issues`, `--open-issues`, and `gh api --paginate` in `unfenced_body`.
   * Saturated-limit provenance support in `_validate_section` (`PC-003`): accept `gh api --paginate` issue/PR provenance alongside `gh issue list` and `gh pr list`.
2. In `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`PC-003`):
   * Update the prescribed validator invocation in `### Issue-state classification table and live handoff refresh` to pass live `--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, `--expect-head`, `--expect-base`, and `--open-issues` flags when validating freshly written notes.
   * Specify PR-excluding `gh api --paginate` saturation handling (`gh api --paginate 'repos/{owner}/{repo}/issues?state=open&per_page=100' --jq '.[] | select(.pull_request == null)'` when `--limit 500` returns `500` items, and `gh api --paginate 'repos/{owner}/{repo}/pulls?state=open&per_page=100'` when `--limit 200` returns `200` items), cross-referenced from `Liveness and stop decision`, `Stabilization checkpoints`, and step 5.

#### Intent

Close every validator and coordinator-instruction gap identified in `RV-001` and `RV-002`.

#### Boundaries

* Included: `tools/check-coordinator-handoff.py` and `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* Excluded: Unrelated coordinator sections and other `tools/` scripts

#### Likely Targets

* tools/check-coordinator-handoff.py: Validator functions `check_agent_text`, `_cell_has_valid_blocker_link`, `_validate_handoff_section`, `check_handoff_text`
* .github/agents/ama-backlog-delivery-coordinator.agent.md: `Liveness and stop decision` and `### Issue-state classification table and live handoff refresh`

#### Dependencies

* none

#### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0`
* `git --no-pager diff --check` exits `0`

#### Completion Evidence

* Clean diff and zero-violation self-check on `.github/agents/ama-backlog-delivery-coordinator.agent.md`.

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Extend `tools/test_check_coordinator_handoff.py`, Refresh HVE Assessment, and Run Focused Validation (`RV-003`)

#### Context

Add adversarial regression cases in `tools/test_check_coordinator_handoff.py` covering every `RV-001` and `RV-002` bypass reproduced during parent review, refresh `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` with the new SHA-256 and expanded behavioral scenarios, and re-run all Focused checks.

#### Intent

Prove deterministic fail-closed behavior across all `RV-001`/`RV-002` bypass vectors and keep step 6 HVE static/behavior evidence current for the exact frozen file hash.

#### Boundaries

* Included: `tools/test_check_coordinator_handoff.py` and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`
* Excluded: Modifying parent review log `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md`

#### Likely Targets

* tools/test_check_coordinator_handoff.py: Extend `test_agent_instruction_guard_rejects_missing_contracts` with polarity-inversion and `--expect-*`/`--paginate` mutations, and add `test_adversarial_rv001_handoff_bypasses_rejected`
* .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md: Refresh SHA-256 while retaining superseded parent SHA-256 (`6bca3f75f222a34d69f389ab82438a75004512fec82e070b12597f6c1d544f4d`) lineage and expanded scenario matrix

#### Dependencies

* `P01-T01`

#### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0`
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` exits `0`
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` exits `0`
* `git --no-pager diff --check`, Markdown link/bullet-style check, and plain-ASCII (`ord(c) <= 127`) check on `.github/agents/ama-backlog-delivery-coordinator.agent.md` exit `0`

#### Completion Evidence

* Passing unit, lint, format, link, and ASCII checks plus updated SHA-256 in HVE assessment.

#### Unresolved Items

* none
