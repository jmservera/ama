<!-- markdownlint-disable-file -->
# Review: Issue #163 Model Provider Data-Handling and Region Position Contract

## Scope and Evidence

* Task ID: issue-163-chat-privacy-region
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Enforced model provider data-handling and region position contract across `src/core` (`chat_provider_position.py`, `chat_privacy.py`, `regulatory_privacy.py`), `src/api` (`/api/chat/status`), canonical privacy/DPIA and KB documentation (`docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md`), deterministic unit tests, and focused validation while preserving human DPO/Legal gating on `D1`–`D8`.
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md; `git diff` across `feat/demo-164-chat-grounding-provenance-0900..feat/chat-163-privacy-region` working tree; independent read-only review lens.

## Opening Review State

* Interpreted review goal: Verify that the completed `P01`–`P03` implementation satisfies all caller objectives, synthesized requirements, acceptance criteria, and resolved critique dispositions (`PC-001` through `PC-005`) while preserving the human DPO/Legal approval boundary on Issue #163 criterion 2.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Plan, phase details, plan critique, research, and reconciled changes record are present and current.
* Acceptance basis: Plan functional/non-functional requirements, acceptance criteria, critique dispositions `PC-001` through `PC-005`, and focused validation evidence.
* First comparison boundary: Compare `P01`–`P03` plan markers and critique dispositions against actual source, test, and documentation diffs without modifying implementation or prior RPI artifacts.
* Active read-only boundaries: Write authority limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md` (and parent RPI session state JSON on handoff); zero source, test, doc, or prior-artifact edits permitted.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across `P01`, `P02`, and `P03`, comparing `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md`, `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md`, `.copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md`, and the working-tree diff via direct inspection and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Enforceable Provider Data-Handling and Region Contract | Partial | Core module, residency/SKU/training/transfer gates, and `/api/chat/status` wiring exist, but `RV-001` through `RV-004` identify edge-case defects in actual-mode unapproved retention, omitted-`env` `build_foundry_query` evaluation, ASCII `1..36500` `CHAT_RETENTION_DAYS` bounds, and unverified modified abuse-monitoring retention claims. |
| `P02` (`P02-T01`, `P02-T02`) | Canonical Privacy, DPIA, and Knowledge-Base Documentation | Partial | `docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` record the contract while keeping `D1`–`D8` `"Not recorded"`, but `RV-005` notes overbroad no-echo wording for `ChatPrivacy.decision()` in `src/core/README.md` and trailing EOF blank lines in `log.md` and `chat-memory-dpia.md`. |
| `P03` (`P03-T01`, `P03-T02`) | Deterministic Unit Tests and Focused Validation | Partial | 13 new tests in `test_chat_provider_position.py` plus additions in `test_chat_privacy.py` and `test_chat_dpia_record.py` pass alongside `ruff` and strict `mypy`, but `RV-005` notes `changes.md` inaccuracies (`PRIMARY_UK_REGION` constant name and missing direct HTTP `/api/chat/status` `provider_position` test assertion). |
| `Follow-Up Items` | Named human DPO and Legal sign-off on `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` | Reconciled | Remains outside active `Pxx` engineering scope under `Refs #163` with named DPO and Legal ownership. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/chat_provider_position.py | Implemented typed residency constants (`uksouth` + EEA `EU_DATA_ZONE_REGIONS`), SKU checks, zero-training enforcement, content-filtering and abuse-monitoring disclosures, `CHAT_TRANSFER_REF` gating, and placeholder/synthetic ref validation. | Module passes strict `mypy` and `ruff`, but `RV-004` flags `default_sample_retention_days: 0` / `human_review_possible: False` when `CHAT_ABUSE_MONITORING_MODIFIED_REF` is unverified. | Passed (`test_chat_provider_position.py`, `ruff`, `mypy`) | Defect `RV-004` |
| `P01-T02` | src/core/src/zava_forward/core/chat_privacy.py, src/core/src/zava_forward/core/regulatory_privacy.py, src/api/src/zava_forward/api/server.py | Wired `chat_provider_position` into `ChatPrivacy`, `regulatory_privacy.readiness_report`, `regulatory_privacy.build_foundry_query`, and `GET /api/chat/status`. | `RV-001` flags `ZF_DATA_PROCESSING=actual` allowing non-`SYNTH-*` env refs to activate approval and retention while `DPO_LEGAL_APPROVED` (`dpo_legal_approved`) is `False`; `RV-002` flags `build_foundry_query(..., env=None)` substituting `{}` instead of `os.environ`; `RV-003` flags `days.isdigit()` missing `.isascii()` and `<= 36500`. | Passed existing tests, `ruff`, `mypy`; edge cases reproduced in review | Defects `RV-001`, `RV-002`, `RV-003` |
| `P02-T01` | docs/reference/research/chat-memory-dpia.md | Documented UK South / EU data-zone residency matrix, zero-training rule, content-filtering vs 30-day abuse-monitoring disclosures, transfer prohibition, and pre-approval retention gate while keeping `D1`–`D8` `"Not recorded"`. | `test_chat_dpia_record.py` passed; trailing blank line at EOF flagged in `RV-005`. | Passed `test_chat_dpia_record.py`; `git diff --check` flagged EOF blank line | Minor hygiene `RV-005` |
| `P02-T02` | src/core/README.md, docs/reference/README.md, docs/reference/log.md | Documented `chat_provider_position.py` and updated KB index and append-only log. | `src/core/README.md` includes `ChatPrivacy.decision()` in its no-echo sentence even though `decision()["refs"]` returns raw approval refs (`RV-005`); `docs/reference/log.md` has a trailing EOF blank line. | Diff review and `git diff --check` | Minor doc defect `RV-005` |
| `P03-T01` | src/core/tests/test_chat_provider_position.py, src/core/tests/test_chat_privacy.py, src/core/tests/test_chat_dpia_record.py | Added 13 unit tests in `test_chat_provider_position.py` and 2 tests across `test_chat_privacy.py` and `test_chat_dpia_record.py`. | Tests pass, but lack assertions for omitted-`env` `build_foundry_query`, non-ASCII/`>36500` `CHAT_RETENTION_DAYS`, `ZF_DATA_PROCESSING=actual` pre-DPO-signoff refusal on arbitrary refs, and HTTP `GET /api/chat/status` `provider_position` payload (`RV-001`–`RV-003`, `RV-005`). | Passed (`285` core privacy/regulatory tests) | Test gap in `RV-001`–`RV-003`, `RV-005` |
| `P03-T02` | .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md, .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md | Executed focused unit suites across `src/core`, `src/agents`, and `src/api` plus `ruff` and strict `mypy`. | Commands passed and were recorded; `changes.md` misnamed `PRIMARY_REGION` as `PRIMARY_UK_REGION` (`RV-005`). | Passed (`677` tests, `ruff`, `mypy`) | Reconciled subject to `RV-005` |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03`, `P03-T02` validation phrasing | Scoped `unittest` wording to focused chat, memory, privacy, DPIA, regulatory, content-standard, and dependency-rule suites across `src/core`, `src/agents`, and `src/api` alongside full `ruff` and `mypy`. | Unfiltered `/usr/bin/python3 -m unittest discover` in `src/core` without an editable `pip install -e ".[dev]"` virtualenv fails in 3 unrelated host-packaging/SDK suites (`test_discovery_assistant_demo`, `test_learning_test_bundles`, `test_device_registry_azure`) and 1 unrelated parent-branch error (`test_challenge_no_retaliation_220`). Caller specified the Focused validation tier. | Synchronized across `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md`, `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md`, and `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md`. | Not needed (preserves caller's Focused validation tier). | Justified and reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` through `PC-004` in `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md` were implemented as specified. `PC-005` (`regulatory_privacy.build_foundry_query` provider check) was implemented for explicit `Mapping` arguments, but `RV-002` found that omitted `env=None` substitutes `{}` instead of reading ambient `os.environ`.
* Material revisions: None altered architecture or user-confirmed scope.
* Dependent-work pause assessment: No improper early resumption occurred.
* Justification assessment: Focused validation scoping is justified by caller instructions and host environment facts; open defects `RV-001` through `RV-005` fit the accepted architecture and route directly to a follow-up `rpi-implement` / child RPI cycle.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention | Repository legal/regulatory rules and Issue #163 criterion 2 reserve lawful-basis, staff-notice, DPIA, and retention approval to named human DPO and Legal owners. | Owner: Named human DPO and Legal | Open distinct governance follow-up (`Refs #163`); properly kept outside engineering `Pxx` claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `ChatPrivacy.decision()` permits approval and retention in `ZF_DATA_PROCESSING=actual` mode when non-synthetic reference strings are supplied despite `dpo_legal_approved=False`

* Related scope: `P01-T02`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/chat_privacy.py` (`ChatPrivacy.decision` and `ChatPrivacy._require`) rejects `SYNTH-*` and demo references under `ZF_DATA_PROCESSING=actual`, but accepts arbitrary non-synthetic reference strings (for example `"DPIA-2026-99"` and `"RET-2026-99"`) and sets `approved=True` and `retention_days=30` while repository-level `DPO_LEGAL_APPROVED` (`dpo_legal_approved`) remains `False` (`D1`–`D8` `"Not recorded"`).
* Impact: Live personal-data mode (`ZF_DATA_PROCESSING=actual`) could activate chat/memory storage and a retention period via environment strings alone before named human DPO and Legal sign-off is recorded in the repository, weakening the Issue #163 human gate ("no retention period is set before approval").
* Destination: `rpi-implement`
* Smallest useful next action: Gate `ZF_DATA_PROCESSING=actual` approval and retention in `ChatPrivacy.decision()` / `_require()` on an explicit `DPO_LEGAL_APPROVED` repository constant (`False` until `D1`–`D8` are recorded by DPO/Legal) while keeping `constructed` fixture behavior unchanged, and add a unit test reproducing refusal with non-synthetic refs in `actual` mode.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `regulatory_privacy.build_foundry_query` ignores ambient `os.environ` when `env` is omitted

* Related scope: `P01-T02`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_privacy.py` (`build_foundry_query`) calls `evaluate_provider_position(env if isinstance(env, Mapping) else {})`. When a caller omits `env` (`env=None`), `isinstance(None, Mapping)` evaluates to `False` and passes `{}` instead of `None` (`os.environ`), permitting query construction even when ambient `CHAT_PROVIDER_REGION="eastus"` or `CHAT_PROVIDER_TRAINING="true"` is set.
* Impact: Partial gap in `PC-005` fail-closed enforcement for callers invoking `build_foundry_query` with the default `env=None`.
* Destination: `rpi-implement`
* Smallest useful next action: Pass `None` through to `evaluate_provider_position(None)` when `env is None` (falling back to `{}` only for non-`None`, non-`Mapping` inputs), align `readiness_report(env=None)` similarly if `None` is passed, and add a `unittest.mock.patch.dict(os.environ, ...)` regression test.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: `ChatPrivacy.decision()` `CHAT_RETENTION_DAYS` validation omits `.isascii()` and the `1..36500` upper bound

* Related scope: `P01-T02`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/chat_privacy.py` (`ChatPrivacy.decision`) evaluates `days.isdigit() and int(days) > 0`. In Python, superscript digits such as `"\u00b2"` satisfy `.isdigit()` and raise `ValueError` in `int(days)`, non-ASCII decimal digits such as `"\u0663\u0660"` are accepted, and values above `36500` (such as `"36501"`) are accepted despite the plan Functional Requirement specifying ASCII digits in `1..36500`.
* Impact: Unhandled `ValueError` on superscript Unicode characters and acceptance of out-of-range or non-ASCII retention day strings.
* Destination: `rpi-implement`
* Smallest useful next action: Validate `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` before `int(days)` conversion in `ChatPrivacy.decision()`, and add deterministic unit tests covering `"\u00b2"`, `"\u0663\u0660"`, `"0"`, and `"36501"`.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Unverified `CHAT_ABUSE_MONITORING_MODIFIED_REF` flips abuse-monitoring retention days to `0` and `human_review_possible` to `False`

* Related scope: `P01-T01`, `P02-T01`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/chat_provider_position.py` (`evaluate_provider_position`) sets `mode="modified_recorded_unverified"` when `CHAT_ABUSE_MONITORING_MODIFIED_REF` is present, yet reports `default_sample_retention_days: 0` and `human_review_possible: False` solely from an unverified environment reference string.
* Impact: Overstates operational privacy assurance before Microsoft's Modified Abuse Monitoring approval is verified on the subscription by DPO/Legal.
* Destination: `rpi-implement`
* Smallest useful next action: Keep `default_sample_retention_days: 30` (the platform default) and keep `human_review_possible: True` whenever `mode` is unverified (recording `modified_abuse_monitoring_recorded: True` without claiming verified zero-day retention or disabled human review), updating matching assertions and `chat-memory-dpia.md` wording if needed.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: `src/core/README.md` no-echo overstatement, missing HTTP `/api/chat/status` `provider_position` assertion, and EOF whitespace hygiene

* Related scope: `P02-T01`, `P02-T02`, `P03-T01`
* Evidence: `src/core/README.md` includes `ChatPrivacy.decision()` in its no-echo claim even though `decision()["refs"]` intentionally returns raw `refs`; `test_chat_provider_position.py` tests `ChatPrivacy.decision()["provider_position"]` directly without an HTTP `GET /api/chat/status` check; and `git diff --check` reports trailing blank lines at EOF in `docs/reference/log.md` and `docs/reference/research/chat-memory-dpia.md`.
* Impact: Documentation inaccuracy, missing HTTP endpoint regression assertion for `/api/chat/status`, and whitespace diff warnings.
* Destination: `rpi-implement`
* Smallest useful next action: Narrow the no-echo sentence in `src/core/README.md` to `provider_position` and `regulatory_privacy.readiness_report()`, add an HTTP `/api/chat/status` `provider_position` test assertion, and trim trailing EOF blank lines in `docs/reference/log.md` and `docs/reference/research/chat-memory-dpia.md` so `git diff --check` exits `0`.

## Defects

* `RV-001` (High, destination: `rpi-implement`)
* `RV-002` (High, destination: `rpi-implement`)
* `RV-003` (Medium, destination: `rpi-implement`)
* `RV-004` (Medium, destination: `rpi-implement`)
* `RV-005` (Low, destination: `rpi-implement`)

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c2`) | Implementation defect in `ZF_DATA_PROCESSING=actual` pre-DPO-approval gating |
| `RV-002` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c2`) | Implementation defect in `build_foundry_query` default `env=None` handling |
| `RV-003` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c2`) | Implementation defect in `CHAT_RETENTION_DAYS` ASCII and `1..36500` bounds check |
| `RV-004` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c2`) | Implementation defect overstating unverified modified abuse-monitoring fields |
| `RV-005` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c2`) | Documentation precision, HTTP `/api/chat/status` test assertion, and EOF whitespace cleanup |

Later implementation of a routed finding does not require this Cycle 1 Review record to be rewritten.

## Residual Work

* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention (Owner: human DPO and Legal; tracked under `Refs #163` criterion 2).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None inside Cycle 1 (`P01` through `P03` executed; routed defects `RV-001` through `RV-005` move to Cycle 2 child task `issue-163-chat-privacy-region-c2`).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src:tests python3 -m unittest tests/test_chat_*.py tests/test_regulatory_*.py tests/test_sensor_privacy.py -q` | `src/core` (`14` modules, `285` tests) | Passed | `Ran 285 tests in 123.445s — OK (skipped=1)` |
| `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest discover -s tests -p "test_*chat*.py" -q` | `src/agents` (`124` tests) | Passed | `Ran 124 tests in 16.149s — OK` |
| `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest ... -q` | `src/api` (`9` chat/privacy/content-standard modules, `239` tests) | Passed | `Ran 165 tests — OK (skipped=1)` + `Ran 74 tests — OK` |
| `test_dependency_rule.py` + `tools/rename-zava-tests.py` | `src/core`, `src/api`, `tools/` (`29` tests) | Passed | `2` + `2` + `25` tests `OK` |
| `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` | `src/core` (`363` files) and `src/api` (`300` files) | Passed | `0` lint, format, or strict `mypy` issues |
| `python3 tools/rpi-checks.py --all` | Repository-wide complete gate | Skipped | Explicitly skipped per caller Focused-tier instruction (`do not run tools/rpi-checks.py --all`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned phases `P01` through `P03` executed and passed focused validation, `ruff`, and strict `mypy`, but independent post-implementation review identified two High defects (`RV-001`, `RV-002`), two Medium defects (`RV-003`, `RV-004`), and one Low hygiene/documentation gap (`RV-005`) that must be resolved in a bounded Cycle 2 remediation before freezing the `Refs #163` commit.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` (`RV-001` through `RV-005`) | Child automatic RPI task `issue-163-chat-privacy-region-c2` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct governance follow-up | Named human DPO and Legal review of `D1`–`D8` (`Refs #163` criterion 2) |

* Execution status: Complete
* Outcome: Defects found (`0 Critical, 2 High, 2 Medium, 1 Low`)
* Validation coverage: `677` targeted unit/regression tests passed across `src/core`, `src/agents`, `src/api`, and `tools/`; `ruff check`, `ruff format --check`, and `mypy` passed across `src/core` and `src/api`; `tools/rpi-checks.py --all` skipped per caller constraint
* Blockers: none
