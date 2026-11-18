<!-- markdownlint-disable-file -->
# Review: PR #1745 Cycle-2 Rebase of Issue #1288 onto `origin/feat/demo-164-chat-grounding-provenance-0900`

## Scope and Evidence

* Task ID: quality-1288-sensor-ai-2142-c2
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P02`, `P02-T01`)
* Assessed boundary: Rebase of `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf` -> `4df840df3`, followed by Cycle-2 seam-test commit `23926a772`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `5f50fc238` (`5f50fc238f78e37e31baaed87f5d1eb81943cf14`); conflict resolution in `src/core/src/zava_forward/core/chat_case_answers.py` (`_sensor(r: Reply)`); auto-merge integrity in `src/core/src/zava_forward/core/chat_panel.py`; focused seam unit coverage in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`); `PC-001` and `PC-002` critique dispositions; `-p`-scoped test execution discipline and bare `mypy`/`ruff` checks in `src/core` and `src/api`; fresh `vercel-labs/web-interface-guidelines` review of rebased `web/ops.js`, `web/assistants.js`, and `web/chat.js`; privacy-safe git identity and local-only (unpushed) commit state. Hosted GitHub Actions CI is outside the local unpushed boundary.
* Plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md; .copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-review.md; `git diff 5f50fc238..HEAD -- src/` across all 13 modified/added source and test files; `mypy` and `ruff` outputs in `src/core` (`328` files) and `src/api` (`280` files); `-p`-scoped `unittest` suites across `src/core`, `src/agents`, and `src/api`; fresh `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` inspection of rebased `ops.js`, `assistants.js`, and `chat.js`.

## Opening Review State

* Interpreted review goal: Confirm with read-only source authority that `feat/quality-1288-sensor-ai-2142` sits cleanly atop `5f50fc238`, preserves both Issue #1288's `sensor.conflict` refusal + `sensor.source` provenance and upstream `#157`/`#164`'s `sensor.detail` + `_damp(r)` fallback without citation pollution, satisfies `PC-001` and `PC-002`, passes all focused `-p` test and static checks, and leaves zero defects in scope.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready — `c2-research.md`, `c2-plan.md`, `c2-phase-details.md`, `c2-plan-critique.md`, `c2-changes.md`, and committed git tree (`23926a772` on `4df840df3` on `5f50fc238`) are present and reconciled.
* Acceptance basis: Caller Cycle-2 prompt requirements, `c2-plan.md` acceptance criteria, `PC-001` and `PC-002` critique dispositions, and `.github/copilot-instructions.md` (`focused` validation tier, Web Development Guidance, privacy-safe noreply commit author/committer, no push).
* First comparison boundary: `git diff 5f50fc238..HEAD -- src/` and `c2-changes.md` against `c2-plan.md` `## Phase Checklist` (`P01-T01`, `P02-T01`) and `## Critique Disposition`.
* Active read-only boundaries: This review creates only `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md` (followed by parent state transition and tracking closeout commit) and does not mutate production code, tests, research, plan, phase details, critique, or changes artifacts.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary read-only verification on 2026-11-14 across all Cycle-2 RPI artifacts, `git diff 5f50fc238..HEAD -- src/` (`13` files, `+737 / -42`), rebased `web/{ops.js,assistants.js,chat.js}` against freshly fetched `vercel-labs/web-interface-guidelines`, and recorded static and `-p` test outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | Rebased `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and Resolved `_sensor(r: Reply)` | Reconciled | Checked `[x]` in `c2-plan.md`, marked `completed` in `c2-phase-details.md`, and verified against commit `4df840df3` (`git merge-base` equals `5f50fc238f78e37e31baaed87f5d1eb81943cf14`). |
| `P02` (`P02-T01`) | Added `DomainAnswerTests` Seam Coverage and Verified `-p` Test Suites | Reconciled | Checked `[x]` in `c2-plan.md`, marked `completed` in `c2-phase-details.md`, and verified against commit `23926a772` (`src/core/tests/test_chat_case_answers.py` + pre-review `.copilot-tracking/` artifacts). |
| `## Follow-Up Items` | Carried-forward parent Cycle-1 follow-ups (`styles.css` `#employee-chat-question` target-size and `quality_sensors_browser_check.py` seeded conflict case) | Reconciled | Mirrored identically in `c2-plan.md` and `c2-changes.md` outside active `P01`–`P02` acceptance claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py` (clean auto-merge), `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` | Rebased `a2a39b2cf` onto `5f50fc238` (`4df840df3`) with privacy-safe git identity (`8036360+jmservera@users.noreply.github.com`); resolved `_sensor(r)` so `conflict = r.fact("sensor.conflict")` runs first under `if not cite:` (returning early without calling `r.fact("sensor.detail")`), `not cite and not conflict` emits `sensor.detail` when present and delegates to `return _damp(r)`, and clean `cite` emits `Reading source:` citing `sensor.source`. | Commit `4df840df3`; `git diff 5f50fc238..HEAD -- src/core/src/zava_forward/core/` | Passed (`mypy`, `ruff check .`, `ruff format --check .` in `src/core` and `src/api`) | Reconciled |
| `P02-T01` | `src/core/tests/test_chat_case_answers.py` | Added two strict-typed (`-> None`) seam test methods to `DomainAnswerTests` (`1` test file modified, `0` deletions, `2` additions) covering `answer()`, `ChatPanel._rules_answer(..., skill="funding-evidence")`, and `ChatPanel._source_kind(...)` across conflict, non-conflict `_damp(r)` fallback, and clean `sensor.source` regimes, and committed `Implement` outputs locally (`23926a772`) ahead of `Review`. | Commit `23926a772`; `src/core/tests/test_chat_case_answers.py` diff | Passed (`12` tests in `test_chat_case_answers.py`, `60` in `test_chat_panel.py`, `4` in `test_sensor_view_conflicts.py`, `6` in `test_regulatory_chat_case_domain_grounding.py`, `14` in `test_quality_sensor_grounding.py`, `19` in `test_quality_sensors_correlation.py`, `191` in `test_quality_sensors.py`, `11` in `test_sensor_staleness_ui_badge.py`, `29` in `test_content_standard.py`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` in `c2-phase-details.md` | Replaced placeholder skill name `"resident-communications"` with registered `assistants.REGISTRY` lens `"funding-evidence"` and aligned `ChatPanel._source_kind` expectations (`"decision-rule"` for `hazards.*`, `sensor.conflict`, `sensor.source`; `"case-record"` for `sensor.detail`, `sensor.0.state`, `sensor.latest.citation`; `"workflow-rule"` for `workflow/domain-boundary`). | `src/core/src/zava_forward/core/chat_panel.py` (`skill_sources`, `ChatPanel._source_kind`); local judgment / immediately relevant current-state update requiring no user decision. | Reconciled across `c2-phase-details.md`, `c2-changes.md`, and `src/core/tests/test_chat_case_answers.py`. | Non-material; preserves `PC-002` critique disposition without needing re-planning or a second critique. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Both findings from `.copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan-critique.md` (`PC-001` [Medium] separating the pre-review `Implement` commit from the post-`Review` tracking closeout commit, and `PC-002` [Low] testing `ChatPanel._rules_answer` under a non-general skill lens plus `ChatPanel._source_kind`) were resolved in `c2-plan.md` and `c2-phase-details.md` before implementation and verified in `23926a772`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Compliant — single-pass critique completed and resolved before `P01` and `P02` ran.
* Justification assessment: Fully supported by commit ancestry (`5f50fc238` -> `4df840df3` -> `23926a772`) and passing `-p` test suites across `src/core`, `src/agents`, and `src/api`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` (`#employee-chat-question` `target-size` `partiallyObscured` at 720px viewport height in `checks.employee_chat_browser_check`) | Pre-existing `origin/main` global employee-chat CSS layout issue carried forward from parent Cycle 1 (`quality-1288-sensor-ai-2142`), outside Cycle-2 rebase conflict scope. | Distinct UX/CSS follow-up task (`styles.css` + `checks.employee_chat_browser_check`) | Open `follow-up-only` item (`RV-001`); kept outside active `P01`–`P02` defect scope. |
| Add seeded conflicting-reading scenario to `src/api/checks/quality_sensors_browser_check.py` asserting `[data-sensor-conflict]`, `[data-flag-conflict]`, and `[data-flag-sources]` under pinned `axe-core` 4.10.3 | Optional browser harness enhancement carried forward from parent Cycle 1; unit, API grounding, and UI-to-snapshot correlation suites already cover conflict states end to end. | Distinct browser-harness follow-up task (`src/api/checks/quality_sensors_browser_check.py`) | Open `follow-up-only` enhancement (`RV-002`); kept outside active `P01`–`P02` defect scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Web Interface Guidelines Audit (`web-design-guidelines`)

Rules freshly fetched from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and checked against all rebased web files in `5f50fc238..HEAD`:

```text
## src/api/src/zava_forward/api/web/ops.js

✓ pass

## src/api/src/zava_forward/api/web/assistants.js

✓ pass

## src/api/src/zava_forward/api/web/chat.js

✓ pass
```

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Carried-forward pre-existing `#employee-chat-question` `target-size` (`partiallyObscured`) CSS issue at 720px viewport height

* Related scope: Plan `## Follow-Up Items` (carried forward from parent task `quality-1288-sensor-ai-2142`)
* Evidence: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md (`## Follow-Up Items`); .copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-review.md (`RV-001`); `src/api/src/zava_forward/api/web/styles.css`.
* Impact: Unchanged by the Cycle-2 rebase onto `5f50fc238`; does not affect `_sensor(r)`, `ChatPanel._rules_answer`, or Quality sensor/review-flag panels, and remains a clean standalone CSS follow-up.
* Destination: follow_up
* Smallest useful next action: Adjust `#employee-chat` vertical flex/max-height spacing at `720px` height in `src/api/src/zava_forward/api/web/styles.css` in a dedicated UX follow-up and verify `python3 -m checks.employee_chat_browser_check`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Carried-forward optional live conflicting-reading scenario in `checks.quality_sensors_browser_check`

* Related scope: Plan `## Follow-Up Items` (carried forward from parent task `quality-1288-sensor-ai-2142`)
* Evidence: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md (`## Follow-Up Items`); `src/api/checks/quality_sensors_browser_check.py`; `src/api/tests/test_quality_sensor_grounding.py`; `src/api/tests/test_quality_sensors_correlation.py`.
* Impact: Non-blocking defense-in-depth improvement; conflict handling is already verified across `src/core` unit tests and `src/api` grounding/correlation suites.
* Destination: follow_up
* Smallest useful next action: Add one seeded conflicting-reading case to `src/api/checks/quality_sensors_browser_check.py` asserting `[data-sensor-conflict]`, `[data-flag-conflict]`, and `[data-flag-sources]` under pinned `axe-core` 4.10.3.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` | Dedicated UX/CSS follow-up in `src/api/src/zava_forward/api/web/styles.css` | Carried-forward pre-existing `origin/main` 720px employee-chat CSS layout item outside Issue #1288 / Cycle-2 rebase scope |
| `RV-002` | `follow_up` | Dedicated browser-harness follow-up in `src/api/checks/quality_sensors_browser_check.py` | Carried-forward optional defense-in-depth browser scenario outside Cycle-2 rebase scope |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Dedicated UX/CSS follow-up in `src/api/src/zava_forward/api/web/styles.css` for 720px `#employee-chat-question` target-size clearance.
* `RV-002`: Dedicated browser-harness enhancement in `src/api/checks/quality_sensors_browser_check.py` for live conflicting-reading DOM assertions.

## Blockers and Remaining Work

* Blockers: None locally (hosted GitHub Actions CI on PR #1745 awaits owner push, as pushing is explicitly prohibited in this session).
* Remaining active work: None (`P01`, `P01-T01`, `P02`, and `P02-T01` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `Success: no issues found in 328 source files`; `All checks passed!`; `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_domain_questions.py' -q` | `src/core` (caller-listed selector) | Skipped (`0` matching files) | `Ran 0 tests` (`NO TESTS RAN` on Python 3.12 because domain tests on `5f50fc238` reside in `test_chat_case_answers.py` and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py`) |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_case_answers.py' -q` | `src/core` | Passed | `Ran 12 tests in 0.004s OK` (includes both new Cycle-2 seam tests) |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_panel.py' -q` | `src/core` | Passed | `Ran 60 tests in 14.549s OK` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_sensor_view_conflicts.py' -q` | `src/core` | Passed | `Ran 4 tests in 0.515s OK` |
| `PYTHONPATH=../core/src:src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat_case_domain_grounding.py' -q` | `src/agents` | Passed | `Ran 6 tests in 0.002s OK` |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `Success: no issues found in 280 source files`; `All checks passed!`; `196 files already formatted` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensor_grounding.py' -q` | `src/api` | Passed | `Ran 14 tests in 13.687s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensors_correlation.py' -q` | `src/api` | Passed | `Ran 19 tests in 21.608s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensors.py' -q` | `src/api` | Passed | `Ran 191 tests in 140.560s OK (skipped=94)` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_sensor_staleness_ui_badge.py' -q` | `src/api` | Passed | `Ran 11 tests in 0.001s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_content_standard.py' -q` | `src/api` | Passed | `Ran 29 tests in 0.238s OK` |
| `vercel-labs/web-interface-guidelines` fresh check | `src/api/src/zava_forward/api/web/{ops,assistants,chat}.js` | Passed | `ops.js` ✓ pass, `assistants.js` ✓ pass, `chat.js` ✓ pass |
| Hosted GitHub Actions CI (`PR #1745`) | `feat/quality-1288-sensor-ai-2142` | Unavailable | Unobserved locally because caller prohibited pushing (`Do NOT push`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: `feat/quality-1288-sensor-ai-2142` is cleanly rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), `_sensor(r: Reply)` in `src/core/src/zava_forward/core/chat_case_answers.py` preserves both Issue #1288's `sensor.conflict` refusal + `sensor.source` grounding and `#157`/`#164`'s `sensor.detail` + `_damp(r)` fallback with zero citation pollution, `PC-001` and `PC-002` are fully satisfied, all `-p`-scoped unit/integration suites and bare `mypy`/`ruff` static checks pass across `src/core`, `src/agents`, and `src/api`, and only non-blocking carried-forward follow-ups (`RV-001`, `RV-002`) remain outside scope.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up | Optional user selection of `RV-001` (`styles.css` 720px employee-chat target-size) or `RV-002` (`quality_sensors_browser_check.py` seeded conflict case) at post-Review checkpoint |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier complete (`mypy`, `ruff check .`, `ruff format --check .` in `src/core` and `src/api`; `-p`-scoped `unittest` suites across `src/core`, `src/agents`, and `src/api`; fresh `web-design-guidelines` pass on `ops.js`, `assistants.js`, `chat.js`); hosted CI unobserved (branch unpushed per caller instruction)
* Blockers: None
