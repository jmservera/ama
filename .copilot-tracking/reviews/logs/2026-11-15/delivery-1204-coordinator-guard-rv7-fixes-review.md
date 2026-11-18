<!-- markdownlint-disable-file -->
# Review: Resolve RV-001 through RV-006 Single-Subclause Hold Indexing, Independent Multi-Trigger Spans, Strict Capacity/Drain Anchors, Bare Self-URL Rejection, Tableless Blocker Checks, and Mixed Declared Session Matching (Issue #1204 Child Loop 7)

## Scope and Evidence

* Task ID: issue-1204-rv7-fixes
* Review date: 2026-11-15
* Review scope: Full task (`P01`: `P01-T01` through `P01-T02`)
* Assessed boundary: Issue #1204 acceptance criteria 1–4, routed parent review findings `RV-001`..`RV-006`, critique dispositions `PC-001`..`PC-004`, Focused validation tier (`unittest`, `ruff check`, `ruff format --check`), and HVE agent conformance (`test_rpi_phase_witness.py`).
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and independent read-only `rubber-duck` verification.

## Opening Review State

* Interpreted review goal: Verify complete closure of parent `RV-001`..`RV-006` and `PC-001`..`PC-004` without quadratic scaling paths, bypasses, false positives, or missing planned subtests.
* Review scope: Full task (`P01-T01`..`P01-T02`)
* Evidence readiness: Complete across plan, details, critique, changes record, Focused validation runs, and independent read-only subagent review.
* Acceptance basis: Issue #1204 acceptance criteria 1–4, `FR-01`..`FR-07`, `NFR-01`..`NFR-02`, and `PC-001`..`PC-004`.
* First comparison boundary: Plan-to-change reconciliation and adversarial edge-case verification of `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Active read-only boundaries: Write only this canonical review artifact; leave source, plan, details, critique, and changes artifacts untouched.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-15 across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and `rv7-fixes` RPI artifacts with independent read-only `rubber-duck` verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01-T01` | Single-subclause memoization, per-trigger wait clamping, capacity/drain anchors, bare self-URL rejection, tableless blocker guard, and mixed declared session coverage | Reconciled with residual defects | Parent `RV-004`..`RV-006` closed cleanly, but `_is_claim_negated_at` still slices `clause_raw` per match (`RV-001`), coordinated uncited blockers inside a single `Waiting on #1641 and stakeholder approval` trigger pass (`RV-002`), and the added tail `$` anchor rejects `"until the next check"` (`RV-003`). |
| `P01-T02` | `self.subTest` regression cases inside existing `11` test methods + Focused validation | Partially reconciled | `11` test methods pass (`0.526s`), but two subtests named in phase details (`until the next check` and backticked `` `rpi-1310-no-push` ``) were omitted (`RV-004`) and the changes log overstated the tracking-literal assertion scope as `tools/` rather than the two target files (`RV-005`). |
| `Follow-Up Items` | Dedicated gate-tooling PR to wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` | Reconciled | Outside Focused validation scope per `#1294`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `tools/check-coordinator-handoff.py` | Implemented `RV-001`..`RV-006` and `PC-001`..`PC-004` | Changes log + `git diff` | Focused checks pass; `RV-001`..`RV-003` defects remain | Defects found |
| `P01-T02` | `tools/test_check_coordinator_handoff.py` | Added `rv7` `self.subTest` cases inside `11` existing test methods | `Ran 11 tests in 0.526s` | `unittest`, `ruff check`, `ruff format --check` exit `0` | Missing two detail-specified subtests (`RV-004`) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` local refinements | Added `next_start` `endpos` bound on `BLOCKER_SPAN_STOP_RE.search` and tail `$` anchors on `SESSION_CAPACITY_WAIT_SPAN_RE` / `PR_DRAIN_WAIT_SPAN_RE` | Local judgment during `Implement` | Recorded in changes log, but tail `$` anchor inadvertently rejected `"until the next check"` specified in `PC-002` / phase details (`RV-003`) | `PC-002` explicitly required preserving `"until the next check"` | Regression against `PC-002` (`RV-003`) |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`, `PC-003`, and `PC-004` were preserved, while `PC-002`'s preservation of `"Waiting for a free worker session slot until the next check."` was broken by the over-strict tail `$` anchor added during `Implement` (`RV-003`).
* Material revisions: None requiring user input.
* Dependent-work pause assessment: No pause required.
* Justification assessment: Requires targeted code and subtest resolution in child loop 8.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation | Modifying gate tooling requires full-tier validation (`#1294`), whereas this task prohibits running `tools/rpi-checks.py` | Separate follow-up PR | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Per-Match Full-Clause Slice Copy in `_is_claim_negated_at` Reintroduces Quadratic Scaling on Prohibited Launch/Wait Clauses

* Related scope: `P01-T01` (`FR-01`, `NFR-01`)
* Evidence: `tools/check-coordinator-handoff.py` (`_is_claim_negated_at`) executes `clause_raw = idx.raw_text[ct.start : ct.end]` on every match inside any clause with `ct.prohibitions` non-empty (e.g., `"never " + "starting #1310 " * N`), copying the entire clause `K` times (`O(K * N)` memory and time; doubling `N` from `16,000` to `32,000` increases runtime `3.5x` from `0.22s` to `0.78s`).
* Impact: Violates strict `O(N)` scaling whenever a prohibition token governs many candidate matches in a single clause.
* Destination: `rpi-implement`
* Smallest useful next action: Pre-store `raw: str` once per `ClauseTokens` during `_build_clause_index` (or pass `idx.raw_text` with `ct.start` offset without slicing) so `_is_claim_negated_at` performs zero per-match clause string copies, and add a scaling subtest for `"never " + ("starting #1310 " * 4000)`.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Coordinated Uncited Blocker After `and`/`or`/`plus` Inside a Single Wait Trigger Is Masked by Earlier Verified Citation

* Related scope: `P01-T01` (`FR-02`)
* Evidence: `tools/check-coordinator-handoff.py` (`_extract_wait_and_blocker_spans`) treats `"Waiting on PR #1641 and stakeholder approval."` as a single trigger span with `span_refs = [("", 1641)]`, never flagging the coordinated uncited blocker `"stakeholder approval"` when `#1641` is verified.
* Impact: Allows an unverified human/external blocker to be conjoined onto a verified blocker under one `Waiting on` / `Blocked on` / `Paused on` verb without citing evidence for the second blocker.
* Destination: `rpi-implement`
* Smallest useful next action: Split `target_span` across coordinating blocker conjunctions (`(?:,\s*)?\b(?:and|or|plus|as\s+well\s+as)\b`) in `idx.span_masked_text`; when any non-first coordinated segment contains an explicit non-capacity blocker phrase (e.g. stakeholder/owner/human approval/sign-off/decision/feedback/input/clearance/permission/outage/upstream) without its own blocker reference (while still permitting shared single-subject suffixes such as `"PR #1641 review and merge"` or `"PR #1641 CI and status checks"`), set `has_uncited_wait = True`.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Over-Strict Tail `$` Anchor on `SESSION_CAPACITY_WAIT_SPAN_RE` Rejects Legitimate `"until the next check"` Capacity Waits

* Related scope: `P01-T01` (`FR-03`, `PC-002`)
* Evidence: `tools/check-coordinator-handoff.py` (`SESSION_CAPACITY_WAIT_SPAN_RE` / `PR_DRAIN_WAIT_SPAN_RE`) rejects `"Waiting for a free worker session slot until the next check."` at `1/1` session capacity with `unverified-blocker-pause`, contradicting `PC-002` and `P01-T02` phase details.
* Impact: Causes false-positive `unverified-blocker-pause` failures on legitimate coordinator capacity/drain wait summaries that mention the next scheduled check/tick/poll/window.
* Destination: `rpi-implement`
* Smallest useful next action: Permit bounded scheduling/timing tail qualifiers (such as `(?:until|before|for|pending)\s+(?:(?:a|an|the)\s+)?(?:next\s+)?(?:scheduled\s+)?(?:check|tick|run|poll|cycle|pass|window)`) in `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` while still rejecting arbitrary non-capacity blocker tails (`for external vendor`, `and owner approval`), and add the regression subtest.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Phase-Detail Specified Subtests (`until the next check` and Backticked `` `rpi-1310-no-push` ``) Omitted from Test Suite

* Related scope: `P01-T02` (`FR-07`, `PC-002`, `PC-004`)
* Evidence: `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md` (`P01-T02`) explicitly listed positive subtests for `"Waiting for a free worker session slot until the next check."` at `1/1` capacity and backticked session token `` `rpi-1310-no-push` `` (containing hold word `no`), neither of which was added to `tools/test_check_coordinator_handoff.py`.
* Impact: Leaves `PC-002` and `PC-004` regressions unguarded in unit tests.
* Destination: `rpi-implement`
* Smallest useful next action: Add both positive `self.subTest` assertions inside existing test methods in `tools/test_check_coordinator_handoff.py`.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: Changes Record Overstates Tracking-Directory Literal Check Scope as Entire `tools/` Directory

* Related scope: `P01-T02` (`NFR-02`)
* Evidence: `.copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-changes.md` states `"zero-literal tracking-directory check across tools/"`, whereas the validation snippet checked only the two Issue #1204 target files (`tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`) because unrelated pre-existing RPI witness tools legitimately parse tracking directories.
* Impact: Minor precision inaccuracy in validation prose.
* Destination: `rpi-implement`
* Smallest useful next action: Record the exact two-file scope (`tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`) in downstream changes/validation prose.

## Validation Assessment

* Required checks run:
  * `python3 tools/check-coordinator-handoff.py`: Passed (`0` violations).
  * `python3 -m unittest tools/test_check_coordinator_handoff.py -q`: Passed (`11` test methods in `0.526s`).
  * `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed.
  * `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed.
  * `python3 -m unittest tools/test_rpi_phase_witness.py -q`: Passed (`33` tests in `3.082s`).
* Skipped checks:
  * `python3 tools/rpi-checks.py`: Explicitly prohibited by user prompt (Focused validation tier).
* Residual testing risks: `RV-001`..`RV-004` require regression subtests in child loop 8.

## Outcome

* Outcome: Defects found
* Severity summary: `0` Critical, `3` High (`RV-001`..`RV-003`), `1` Medium (`RV-004`), `1` Low (`RV-005`).
* Open blockers: None preventing automatic child-task remediation.
* Handoff and routing summary: Route `RV-001`..`RV-005` into automatic child task `issue-1204-rv8-fixes` (`delivery-1204-coordinator-guard-rv8-fixes`).
