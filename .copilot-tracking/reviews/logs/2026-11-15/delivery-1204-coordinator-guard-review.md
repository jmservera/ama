<!-- markdownlint-disable-file -->
# Review: Prevent Unsupported Idle Ticks and Stale Coordinator Handoffs (Issue #1204)

## Scope and Evidence

* Task ID: issue-1204
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Coordinator instruction updates in .github/agents/ama-backlog-delivery-coordinator.agent.md, offline deterministic validator in tools/check-coordinator-handoff.py, focused `unittest` suite in tools/test_check_coordinator_handoff.py, step 6 HVE static/behavior assessment in .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md, and Focused validation tier (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, `test_rpi_phase_witness.py`, AMA Markdown/ASCII checks; `tools/rpi-checks.py` excluded per caller direction).
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py, tools/test_rpi_phase_witness.py

## Opening Review State

* Interpreted review goal: Verify once, from reconciled artifacts and implemented files, whether `P01` through `P03` satisfy Issue #1204 acceptance criteria (`AC-01` through `AC-06`), plan functional/non-functional requirements (`FR-01` through `FR-05`, `NFR-01`, `NFR-02`), and critique dispositions (`PC-001` through `PC-004`) without defects, regressions, or unrouted residual work.
* Review scope: full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, changes log, HVE assessment, and focused validation outputs are present and reconciled.
* Acceptance basis: Caller AC1 through AC4 (plan `AC-01` through `AC-06`), `FR-01` through `FR-05`, `NFR-01` through `NFR-02`, and `PC-001` through `PC-004` critique dispositions.
* First comparison boundary: Plan-to-change reconciliation across `P01-T01`, `P02-T01`, `P03-T01`, and `## Follow-Up Items`, paired with independent read-only logic verification of `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py`.
* Active read-only boundaries: This stage writes only `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` and does not mutate source files, research, plan, phase details, critique, or changes records.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-task review on 2026-11-15 across .github/agents/ama-backlog-delivery-coordinator.agent.md (`sha256: 6bca3f75f222a34d69f389ab82438a75004512fec82e070b12597f6c1d544f4d`), tools/check-coordinator-handoff.py (`sha256: 103774399dd1f371c32452e83962cbbbe09b0f747f688901f71118e3d` prefix `103774399dd1`), tools/test_check_coordinator_handoff.py (`sha256: 55a7fa0a7d5effbedee2ecd83f69bcbf823912842f14f28d815d3ae7133ef721`), reconciled RPI research/plan/details/critique/changes/HVE artifacts, Focused validation results, and an independent read-only `rubber-duck` logic audit.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01` (`P01-T01`) | `Coordinator Instructions Guard (`P01` / `P01-T01`)` | Partial | Five-category table, anti-idle/unverified-blocker rules, and live command refresh are present across all five coordinator sections, but the prescribed `--handoff` check omits `--expect-*`/`--open-issues` flags for write-time live cross-checking and `gh ... --limit 500`/`200` lacks an explicit pagination guard when saturated (`RV-002`). |
| `P02` (`P02-T01`) | `Deterministic Coordinator Handoff Validator (`P02` / `P02-T01`)` | Partial | CLI/library validator implements `check_agent_text` and `check_handoff_text`, but independent audit reproduced bypasses on trailing-clause negation (`"Nothing changed; do not launch anything"`), `"Waiting for ..."` phrasing, split classification tables after summary prose, uncited/absent blocker IDs (`ref_row is None`), nonexistent local `#anchor` targets (`RV-001`), and inverted agent-instruction rules (`RV-002`). |
| `P03` (`P03-T01`) | `Focused Unit Test Suite, Lint/Format Checks, and HVE Qualification (`P03` / `P03-T01`)` | Partial | `10` `unittest` methods, Ruff checks, `test_rpi_phase_witness.py`, and five-attribute HVE qualification ran and passed, but adversarial regression cases covering `RV-001` and `RV-002` were missing (`RV-003`). |
| `Follow-Up Items` | `tools/rpi-checks.py` static-check wiring kept out of scope | Reconciled | Mirrored in changes `## Follow-Up Items` and excluded from active `P01`-`P03` scope per caller prohibition on touching/running `tools/rpi-checks.py`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01` / `P01-T01` | .github/agents/ama-backlog-delivery-coordinator.agent.md | Added `### Issue-state classification table and live handoff refresh` and aligned `Liveness and stop decision`, `Recurring schedules`, `Stabilization checkpoints`, step 5 `Cover, in this order:`, and `Final report` for AC1-AC3. | Verified in `git diff .github/agents/ama-backlog-delivery-coordinator.agent.md`. | `git diff --check`, link check (`0` violations in `718` docs), ASCII/bullet check passed. | Reconciled with minor gap (`--expect-*` write-time flags and `--limit` saturation guard, `RV-002`) |
| `P02` / `P02-T01` | tools/check-coordinator-handoff.py | Implemented stdlib-only offline validator for coordinator instructions and handoff/status/checkpoint Markdown (`AC4`). | CLI self-check exited `0`. | `ruff check`, isolated `ruff check` + `ruff format --check`, `unittest` passed. | Defects found (`RV-001` summary/table/blocker bypasses; `RV-002` positive-only agent token match) |
| `P03` / `P03-T01` | tools/test_check_coordinator_handoff.py, .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md | Added `10` `unittest` methods with `subTest` matrices and five-attribute HVE static/behavior qualification. | `Ran 10 tests in 0.085s OK`; HVE record persisted. | `unittest`, `ruff check`, `ruff format --check`, `test_rpi_phase_witness.py` (`33` tests) passed. | Defect found (missing adversarial bypass tests and updated HVE coverage for `RV-001`/`RV-002`, `RV-003`) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P02-T01` (`CITED_BLOCKER_REF_RE` in tools/check-coordinator-handoff.py) | Scoped cited-blocker regex during implementation so `"before launching #1310"` was not misread as a blocker citation while keeping `waiting on #N` / `blocked on #N` / `paused on #N`. | Caught by unit test execution during `P03-T01`; ordinary local judgment requiring no user decision. | Recorded in .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md under `## Implementation-Time Plan and Detail Updates`. | Preserved `PC-001`..`PC-004`, though `ref_row is None` remained unhandled (`RV-001`). | Reconciled; remaining gap routed in `RV-001` |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` through `PC-004` from .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md are recorded in plan `## Critique Disposition` and honored (still-open stacked child/partial-delivery `merged` restriction, `1/8 (rpi-1204)` active-session parsing, fenced-block stripping, and step 6 HVE static/behavior qualification), subject to the clause-level negation and split-table refinements identified in `RV-001`.
* Material revisions: No scope, architectural, or user-decision divergence occurred during implementation; critique executed once and was not repeated.
* Dependent-work pause assessment: `P01` -> `P02` -> `P03` ran in declared dependency order with no early resumption.
* Justification assessment: Confirmed caller constraints (`Focused` tier, no `tools/rpi-checks.py`, no `git push`/PR) were preserved.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks | Caller explicitly prohibited running `tools/rpi-checks.py` in this Focused-tier slice, and gate-tool changes carry full-tier scrutiny under `#1294` | Follow-up gate-tooling issue/PR with full-tier gate validation | Open distinct follow-up (non-defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `check_handoff_text` allows bypasses via trailing-clause negation, `"Waiting for ..."` phrasing, split tables after summaries, unclassified cited blockers, and broken local `#anchor` blocker links

* Related scope: `P02-T01`
* Evidence: tools/check-coordinator-handoff.py (`NEGATION_GUARD_RE`, `WAITING_OR_PAUSE_RE`, `first_table_end`, `CITED_BLOCKER_REF_RE`, `_cell_has_valid_blocker_link`)
* Impact: (1) `NEGATION_GUARD_RE.search(line)` skips an entire line whenever any negation appears anywhere on the line, so `"Nothing changed; do not launch anything"` passes even with `ready to start` or unclassified issues; (2) `"Waiting for owner feedback"` misses `WAITING_OR_PAUSE_RE`; (3) `lineno < first_table_end` checks only the first classification table's end while aggregating rows from later tables placed *after* `"Nothing changed"`; (4) citing `Waiting on #999` where `#999` is absent from the classification table (`ref_row is None`) silently passes; and (5) local in-document `#nonexistent-anchor` blocker links pass without checking document heading slugs.
* Destination: `rpi-implement`
* Smallest useful next action: Scope negation checks to guard tokens immediately preceding each matched claim within the same clause, include `waiting\s+(?:on|for)\b` (and general waiting claims), require all classification tables needed to classify open issues to precede each summary line (`lineno > last_class_table_end` and evaluate pre-summary rows), flag `unverified-blocker-reference` when `ref_row is None`, and validate non-GitHub-fragment `#anchor` links against document heading slugs.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `check_agent_text` checks positive token presence without prohibition polarity, and coordinator handoff guidance omits `--expect-*` live flags and `--limit` saturation pagination

* Related scope: `P01-T01`, `P02-T01`
* Evidence: tools/check-coordinator-handoff.py (`check_agent_text`) and .github/agents/ama-backlog-delivery-coordinator.agent.md (`### Issue-state classification table and live handoff refresh`, `Recurring schedules`, step 5)
* Impact: An adversarial instruction edit such as `"always claim nothing changed when open issues are unclassified"` or `"pause on an unverified blocker"` satisfies substring token checks in `check_agent_text`; additionally, the prescribed `python3 tools/check-coordinator-handoff.py --handoff <path>` example omits `--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, `--expect-head`, `--expect-base`, and `--open-issues` needed to verify snapshot freshness against live command outputs, and `gh issue list --state open --limit 500` / `gh pr list --state open --limit 200` lacks an explicit pagination rule (`gh api --paginate`) if a backlog reaches `500` open issues or `200` open PRs.
* Destination: `rpi-implement`
* Smallest useful next action: Require prohibition polarity (`never` / `cannot` / `must not` / `forbid`) in `check_agent_text` for the unclassified-idle and unverified-blocker rules, and update .github/agents/ama-backlog-delivery-coordinator.agent.md to pass live `--expect-*` / `--open-issues` arguments at handoff write time and require full pagination (`gh api --paginate`) whenever `--limit 500` or `--limit 200` is saturated.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: `tools/test_check_coordinator_handoff.py` and step 6 HVE assessment omit adversarial regression coverage for `RV-001` and `RV-002`

* Related scope: `P03-T01`
* Evidence: tools/test_check_coordinator_handoff.py and .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md
* Impact: Without regression subtests for trailing-clause negation, `"Waiting for ..."`, split tables after summaries, absent cited blocker IDs, broken local `#anchor` blocker links, and polarity-inverted agent instructions, `RV-001` and `RV-002` passed the initial 10-test suite undetected.
* Destination: `rpi-implement`
* Smallest useful next action: Add deterministic `unittest` subtests for every `RV-001` and `RV-002` bypass vector in tools/test_check_coordinator_handoff.py and refresh the SHA-256-anchored HVE assessment after the child fix completes.

## Defects

* `RV-001` (`High`, destination `rpi-implement`): Clause-unscoped negation, `"Waiting for ..."` gap, split-table ordering, absent cited-blocker (`ref_row is None`), and broken local `#anchor` link bypasses in tools/check-coordinator-handoff.py.
* `RV-002` (`Medium`, destination `rpi-implement`): Polarity-insensitive guard check in `check_agent_text` and missing live `--expect-*` CLI flags / `--limit` saturation pagination guidance in .github/agents/ama-backlog-delivery-coordinator.agent.md.
* `RV-003` (`Medium`, destination `rpi-implement`): Missing adversarial unit-test regressions and refreshed HVE scenario evidence for `RV-001` and `RV-002` in tools/test_check_coordinator_handoff.py.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| `RV-001` | `rpi-implement` | Harden clause-scoped negation, waiting regex, pre-summary table completeness, absent cited-blocker rejection, and local `#anchor` verification in tools/check-coordinator-handoff.py | Bounded validator logic defect within approved plan direction |
| `RV-002` | `rpi-implement` | Enforce prohibition polarity in `check_agent_text` and add live `--expect-*` flags + saturated-limit pagination rule in .github/agents/ama-backlog-delivery-coordinator.agent.md | Bounded instruction/validator contract tightening |
| `RV-003` | `rpi-implement` | Add adversarial unit tests in tools/test_check_coordinator_handoff.py and refresh HVE assessment identity/scenarios | Bounded regression-test gap |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks under a separate gate-tooling PR validated with the full gate receipt.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none inside completed `issue-1204` loop (`RV-001`, `RV-002`, and `RV-003` routed to automatic child follow-up task `issue-1204-rv-fixes` before local commit)

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 tools/check-coordinator-handoff.py` | `.github/agents/ama-backlog-delivery-coordinator.agent.md` | Passed | `Coordinator handoff guard check passed (1 target(s), 0 violations).` (exit `0`) |
| `python3 -m unittest tools/test_check_coordinator_handoff.py -q` | `tools/test_check_coordinator_handoff.py` (`10` tests) | Passed | `Ran 10 tests in 0.085s - OK` (exit `0`) |
| `python3 -m unittest tools/test_rpi_phase_witness.py -q` | Adjacent `tools/` regression suite (`33` tests) | Passed | `Ran 33 tests in 3.315s - OK` (exit `0`) |
| `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | Repository Ruff config (`0.17.3`) | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | Isolated 100-char format check | Passed | `2 files already formatted` (exit `0`) |
| `git --no-pager diff --check` + Markdown link/ASCII checks | Changed agent Markdown and Python tools | Passed | `0` diff whitespace issues; `0` link violations across `718` docs; `0` non-ASCII chars |
| `python3 tools/rpi-checks.py` | Repository gate runner | Skipped | Explicitly prohibited by caller (`Do NOT run tools/rpi-checks.py`) |
| Hosted GitHub Actions CI | Unpushed local branch `fix/delivery-1204-coordinator-guard` | Skipped | Explicitly prohibited by caller (`Do not push or open a PR`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned `P01` through `P03` tasks executed completely and passed initial Focused validation, but independent read-only logic review reproduced concrete validator and instruction-check bypasses (`RV-001` High, `RV-002` Medium, `RV-003` Medium) that must be closed in a routed child implementation pass before freezing `HEAD` for coordinator review.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | `rpi-implement` | Resolve `RV-001`, `RV-002`, and `RV-003` in child task `issue-1204-rv-fixes` (`delivery-1204-coordinator-guard-rv-fixes`) |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks in a full-tier gate-tooling PR |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused tier passed (`10` unit tests, `33` phase-witness tests, `ruff check`, `ruff format --isolated --line-length 100 --check`, `git diff --check`, Markdown link/ASCII checks); `tools/rpi-checks.py` and hosted CI skipped per explicit caller instructions
* Blockers: none
