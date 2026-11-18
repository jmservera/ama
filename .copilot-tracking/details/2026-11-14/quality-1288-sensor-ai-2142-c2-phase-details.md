<!-- markdownlint-disable-file -->
# RPI Phase Details: PR #1745 Cycle-2 Rebase of Issue #1288 onto `origin/feat/demo-164-chat-grounding-provenance-0900`

## Metadata

* Task ID: quality-1288-sensor-ai-2142-c2
* Task slug: quality-1288-sensor-ai-2142-c2
* Parent task ID: quality-1288-sensor-ai-2142
* Related plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md, .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md, .github/copilot-instructions.md

## Phase Index

| Phase ID | Name                                                                               | Status  | Detail sections |
|----------|------------------------------------------------------------------------------------|---------|-----------------|
| P01      | Rebase `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and Resolve `_sensor(r)` | completed | P01, P01-T01    |
| P02      | Seam Unit Test, Focused `-p` Verification, and Local Cycle-2 Commit                | completed | P02, P02-T01    |

## Test Ownership and Validation Lock

* Canonical test target modified in Cycle-2: `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`), maximum `1` test file modified, exact test removals: `none` (`0`), maximum additions: `2` strict-typed (`-> None`) test methods covering semantic `_sensor(r)` conflict refusal vs `_damp(r)` non-conflict delegation and `sensor.source` clean-reading provenance.
* Preserved Cycle-1 test targets carried across rebase unchanged: `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py`, `src/api/tests/test_sensor_staleness_ui_badge.py`.
* Generated targets modified: `none`.
* Validation commands (strictly `-p`-scoped for `unittest discover`):
  1. `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
  2. `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_domain_questions.py' -q` (caller-listed command; expected `0` tests because domain tests live in `test_chat_case_answers.py` and `src/agents`)
  3. `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_case_answers.py' -q`
  4. `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_panel.py' -q`
  5. `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_sensor_view_conflicts.py' -q`
  6. `cd src/agents && PYTHONPATH=../core/src:src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat_case_domain_grounding.py' -q`
  7. `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
  8. `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src python3 -m unittest discover -s tests -p 'test_quality_sensor_grounding.py' -q`
  9. `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src python3 -m unittest discover -s tests -p 'test_quality_sensors_correlation.py' -q`
  10. `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src python3 -m unittest discover -s tests -p 'test_quality_sensors.py' -q`
  11. `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src python3 -m unittest discover -s tests -p 'test_sensor_staleness_ui_badge.py' -q`
  12. `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src python3 -m unittest discover -s tests -p 'test_content_standard.py' -q`

<!-- rpi:phase id=P01 -->
## P01: Rebase `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and Resolve `_sensor(r)` Conflict

### Context

Research evidence `C1`–`C5` proves `feat/quality-1288-sensor-ai-2142` has a single commit (`a2a39b2cf`) above merge-base `f5f76b6cc`, while `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) has 11 commits above `f5f76b6cc` (including `2b1d40db0`, PR `#1734`). `git merge-tree --write-tree 5f50fc238 a2a39b2cf` confirms `src/core/src/zava_forward/core/chat_case_answers.py` is the sole conflicting file and `src/core/src/zava_forward/core/chat_panel.py` auto-merges cleanly.

### Intent

Rebase `a2a39b2cf` directly onto `5f50fc238` using the authenticated GitHub noreply identity and resolve `_sensor(r: Reply)` in `chat_case_answers.py` so Issue #1288's `sensor.conflict` early return and `sensor.source` line coexist cleanly with `2b1d40db0`'s `sensor.detail` + `return _damp(r)` fallback.

### Boundaries

* Included: Local git config (`user.name`, `user.email`), tracked parent state pre-rebase restoration and post-rebase update, `git rebase 5f50fc238`, and conflict resolution in `src/core/src/zava_forward/core/chat_case_answers.py`.
* Excluded: Remote `git push`, modifying `sensor_view.py`, `assistants.py`, `sensor_badges.py`, or `src/api/src/zava_forward/api/web/*.js`.

### Likely Targets

* `src/core/src/zava_forward/core/chat_case_answers.py`: Resolve `_sensor(r: Reply)` conflict while keeping `sensor_facts(view)` (`sensor.detail` fallback, `sensor.conflict`, `sensor.source`) and all `2b1d40db0` domain functions (`_domain_head`, `_domain_close`, `_claim`, `_pas2035`, `_damp`, `DOMAIN_BOUNDARY`, `ORIGIN_RULE`, `RULES_FIRST`, `ANSWERS`).
* `src/core/src/zava_forward/core/chat_panel.py`: Verify auto-merged result retains `"sensor.source"` and `"sensor.conflict"` in `SENSOR_RULE_PATHS` alongside `RULES_FIRST`, `RULES_SOURCE_ROOTS`, and `skill_sources` `common`.

### Dependencies

* None.

### Validation Expectations

* `git rebase` finishes with `0` remaining conflicts, `git merge-base 5f50fc238 HEAD` equals `5f50fc238f78e37e31baaed87f5d1eb81943cf14`, and `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` passes in `src/core`.

### Completion Evidence

* Rebased commit on `feat/quality-1288-sensor-ai-2142` sits directly on `5f50fc238` and contains all 19 files from `a2a39b2cf` with `chat_case_answers.py` cleanly reconciled.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local privacy-safe git identity, rebase `a2a39b2cf` onto `5f50fc238`, and resolve `chat_case_answers.py`

#### Context

1. `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` is tracked in `a2a39b2cf` and was updated at child-loop intake; restoring it to `HEAD` before running `git rebase 5f50fc238` ensures a clean tracked working tree during rebase, after which the child-lineage `next_action` update is re-applied (`Research Trap 5`). Untracked `*-c2-*` files under `.copilot-tracking/` do not collide with any upstream commit.
2. In `chat_case_answers.py`, `sensor_facts(view)` sets `put("sensor.detail", view.get("detail") or view.get("conflict_notice"))` and `put("sensor.conflict", view.get("conflict_notice"))` (`C3`). Consequently, inside `_sensor(r: Reply)` under `if not cite:`, `conflict = r.fact("sensor.conflict")` MUST run before `detail = r.fact("sensor.detail")` so conflict replies cite `{case_id}/sensor.conflict` (`decision-rule`) rather than `{case_id}/sensor.detail` (`case-record`) and never emit `"No retained sensor reading is shown for this case."` (`C8`).

#### Intent

Complete the rebase onto `5f50fc238` with exact `_sensor(r: Reply)` semantics and privacy-safe commit metadata.

#### Boundaries

* Included: `git config --local`, `git rebase 5f50fc238`, `src/core/src/zava_forward/core/chat_case_answers.py`.
* Excluded: Any remote git operation (`git push`).

#### Likely Targets

* `src/core/src/zava_forward/core/chat_case_answers.py`:
  * Keep `sensor_facts(view)` additions (`put("sensor.detail", view.get("detail") or view.get("conflict_notice"))`, `put("sensor.conflict", view.get("conflict_notice"))`, and `put("sensor.source", grounding.get("source_text"))` inside `if values:`).
  * Resolve `_sensor(r: Reply)` to:
    ```python
    def _sensor(r: Reply) -> None:
        cite = r.fact("sensor.latest.citation")
        if not cite:
            conflict = r.fact("sensor.conflict")
            if conflict:
                r.say(
                    "Retained sensor readings conflict, so no single value is selected. "
                    + conflict
                    + " Use the ordinary quality check, or ask the quality team to inspect the home."
                )
                if r.fact("sensor.not_retained"):
                    r.say(r.facts["sensor.not_retained"])
                if r.fact("stage"):
                    r.say(f"Case stage: {r.facts['stage']}.")
                return
            detail = r.fact("sensor.detail")
            if detail:
                r.say(f"No retained sensor reading is shown for this case. {detail}")
            return _damp(r)
        temperature = r.fact("sensor.latest.temperature_c")
        humidity = r.fact("sensor.latest.humidity_pct")
        observed = r.fact("sensor.latest.observed_at")
        r.say(
            f"Latest retained reading [{cite}]: temperature_c {temperature} degC, "
            f"humidity_pct {humidity} %RH (relative humidity), observed {observed}."
        )
        if r.fact("sensor.source"):
            r.say(f"Reading source: {r.facts['sensor.source']}")
        for path in ("sensor.freshness", "sensor.health", "sensor.watch", "sensor.thresholds"):
            if r.fact(path):
                r.say(r.facts[path])
        if r.fact("sensor.not_retained"):
            r.say(r.facts["sensor.not_retained"])
        r.say("These readings are synthetic and not calibrated. A person decides any action.")
    ```
  * Stage `src/core/src/zava_forward/core/chat_case_answers.py` and continue rebase (`GIT_EDITOR=true git rebase --continue`), then re-apply the parent state `next_action` pointer in `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json`.

#### Dependencies

* None.

#### Validation Expectations

* Inspect `git log --oneline -n 3`, `git show --stat HEAD`, and `chat_panel.py` + `chat_case_answers.py` around merged hunks.

#### Completion Evidence

* `HEAD` parent is `5f50fc238`, no conflict markers exist anywhere, and `chat_case_answers.py` + `chat_panel.py` contain both `#1288` and `#157`/`#164` hunks intact.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Seam Unit Test, Focused `-p` Verification, and Local Cycle-2 Commit

### Context

Research evidence `C6`–`C8` shows that on `5f50fc238`, `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` and `CaseDomainGroundingTests` in `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` test `#157`/`#164` domain answers (`_damp`, `_claim`, `_pas2035`), while `src/api/tests/test_quality_sensor_grounding.py` tests Issue #1288 full-stack chat/sensor grounding. Adding a direct unit test in `DomainAnswerTests` inside `src/core/tests/test_chat_case_answers.py` verifies the exact Cycle-2 conflict-resolution seam in `src/core` itself.

### Intent

Add focused seam unit coverage in `src/core/tests/test_chat_case_answers.py` (including `ChatPanel._rules_answer` under a non-general skill lens and `ChatPanel._source_kind`), run every required static and `-p` unit/correlation check across `src/core`, `src/agents`, and `src/api`, reconcile pre-review `Implement` RPI artifacts, and create the `Implement` local commit on `feat/quality-1288-sensor-ai-2142` before `Review` without pushing.

### Boundaries

* Included: `src/core/tests/test_chat_case_answers.py`, `-p` test runs and bare `mypy`/`ruff` runs, pre-review `.copilot-tracking/` Cycle-2 artifacts (`research`, `plan`, `phase-details`, `plan-critique`, `changes`, `state.json`), and local `git commit` with `Refs #1288` and Copilot trailer.
* Excluded: Unscoped `unittest discover -s tests` without `-p`, editing other test files, creating `c2-review.md` inside `Implement` (owned by subsequent `rpi-review` phase and its tracking closeout commit), or pushing to remote.

### Likely Targets

* `src/core/tests/test_chat_case_answers.py`: Add strict-typed (`-> None`) seam test(s) in `DomainAnswerTests`.
* `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md`, `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md`, `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md`, `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-c2-state.json`, and `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json`.

### Dependencies

* `P01`.

### Validation Expectations

* All 12 commands in `## Test Ownership and Validation Lock` pass with exit code `0`.

### Completion Evidence

* Passing static and `-p` test outputs recorded in `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md`, plan/detail markers reconciled (`[x]` / `completed`), and `Implement` local commit created on `feat/quality-1288-sensor-ai-2142` ready for `rpi-review` without pushing.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `DomainAnswerTests` seam test in `test_chat_case_answers.py`, run `-p` tests and `mypy`/`ruff`, and commit `Implement` artifacts locally

#### Context

`DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` currently has two tests (`test_sensor_answer_cites_documents_only_when_survey_is_listed` and `test_claim_without_grants_keeps_the_domain_footer`). Adding up to two strict-typed (`-> None`) test methods in `DomainAnswerTests` directly exercises both `chat_case_answers.answer()` and `ChatPanel._rules_answer(..., skill="funding-evidence")` + `ChatPanel._source_kind(...)`:
1. `sensor_facts(conflict_view)` + `case_facts(detail)` -> `answer("ZF-1", "What are the sensor readings?", facts)` and `ChatPanel._rules_answer(..., skill="funding-evidence")` emit `"Retained sensor readings conflict, so no single value is selected."`, cite `"ZF-1/sensor.conflict"` (`source_kind == "decision-rule"`), omit `"ZF-1/sensor.detail"`, omit `"No retained sensor reading is shown"`, and omit `cca.DOMAIN_BOUNDARY` / `_damp` fallback.
2. Non-conflict `not cite` with `sensor.detail` (`"Monitoring consent is declined; no values are shown."`) + damp hazard / `sensor_review_drafts` -> emits `"No retained sensor reading is shown for this case. Monitoring consent is declined; no values are shown."` AND delegates to `_damp(r)` (`"[Origin: decision_rule]"`, `"ZF-1/hazards.0.category"` as `"decision-rule"`, `"ZF-1/sensor.0.state"` as `"case-record"`, and `cca.DOMAIN_BOUNDARY` / `"workflow/domain-boundary"` as `"workflow-rule"`), even under `skill="funding-evidence"` via `skill_sources` `common` (`"sensor"`) + `RULES_SOURCE_ROOTS["sensor"] = ("hazards",)`.
3. Clean `cite` with `sensor.source` -> emits `"Reading source: "` and cites `"ZF-1/sensor.source"` with `source_kind == "decision-rule"`.

#### Intent

Prove the merged `_sensor(r)` and `ChatPanel._rules_answer` contract at unit level in `src/core`, run all focused `-p` checks and `mypy`/`ruff` checks, and commit `Implement` outputs locally cleanly before `Review`.

#### Boundaries

* Included: `src/core/tests/test_chat_case_answers.py` (`<= 2` new `-> None` test methods, `0` deletions), validation runs, and the pre-review `Implement` local commit (`Refs #1288` + Copilot trailer).
* Excluded: Remote push; unscoped test discovery; `c2-review.md` creation (performed in `Review`).

#### Likely Targets

* `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`).
* `.copilot-tracking/` Cycle-2 files.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* Execute all commands listed in `## Test Ownership and Validation Lock` and verify non-zero test counts on `test_chat_case_answers.py`, `test_chat_panel.py`, `test_sensor_view_conflicts.py`, `test_regulatory_chat_case_domain_grounding.py`, `test_quality_sensor_grounding.py`, `test_quality_sensors_correlation.py`, `test_quality_sensors.py`, `test_sensor_staleness_ui_badge.py`, and `test_content_standard.py` (while also running the caller's literal `-p 'test_chat_domain_questions.py'` command and recording that the domain tests actually live in `test_chat_case_answers.py` and `test_regulatory_chat_case_domain_grounding.py`).

#### Completion Evidence

* Exit code `0` on `mypy`, `ruff check .`, `ruff format --check .` in `src/core` and `src/api`, exit code `0` on all `-p` test commands, and clean `git status --short` on `feat/quality-1288-sensor-ai-2142` ahead of `5f50fc238` without pushing.

#### Unresolved Items

* None.
