<!-- markdownlint-disable-file -->
# RPI Plan: Offline demo-feedback acceptance harness (Refs #350)

## Task Metadata

* Task ID: issue-350-demo-feedback-harness
* Task slug: issue-350-demo-feedback-harness
* Planning status: ready
* Plan date: 2026-10-22
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-harness-plan-critique.md

## Executive Summary

The plan adds one deterministic, offline checker, `tools/check-demo-feedback.py`, and one focused test module. The checker reads one explicitly supplied JSON evidence bundle and reports `pass`, `fail`, `blocked` or `not-run` for each measurable prerequisite of the owner-feedback minimum: immutable image identity, the role-scoped `/api/me` contract, persisted synthetic case write and reload, bounded real-AI evidence versus template output, and the 980-case programme versus 60,000-home stock distinction. Research found no existing check that validates supplied deployed evidence (the browser checks start local password-auth servers), so the gap is real. Runtime schemas are imported from the installed packages, not copied.

The harness is not deployed acceptance. Fixture evidence caps the overall verdict at `blocked`; redirects, 401/403 and asset existence are never success; #349, #360 and all original #350 acceptance criteria remain unmet.

### User Decisions and Requirements Highlights

* Build only a narrow new checker, and only because prior art cannot do this; consequence: two new files and no shared-file edits.
* Offline by default from explicit synthetic evidence; consequence: no network, env credentials, private data, writes or AI activation.
* Never count denial or redirect as functional success; consequence: those statuses in a positive slot fail the check.

### What You May Not Know

* The new test module is not discovered by the unchanged gate (only `tools/test_rpi_checks.py` is in its matrix), so it is run directly and recorded; the full gate runs unchanged on the committed candidate.
* A write followed by a fresh read does not prove persistence; the evidence must record a restart between them.
* `/api/cases?view=all` totals open cases only, so the 980 comparison is stated as open permitted cases.
* Contact outcomes are held for roles without a recorded need, so write/reload evidence for such roles is blocked, not passed.

### Unresolved Decisions or Blockers

* Live capture procedure, spend-bound evidence and the fixed administrator account: blocked on #349/#360 and have no runtime field; reported `not-run`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Run research, plan, implement, review in order through installed skills; commit dated issue350 artifacts (user prompt 2026-10-22).
* Prior art first; build `tools/check-demo-feedback.py` and `tools/test_check_demo_feedback.py` only if existing harness cannot do it (user prompt).
* Distinguish pass/fail/blocked/not-run; never count redirect, auth denial or source-asset existence as authorized functional success (user prompt).
* Cover image identity, real role-scoped `/api/me`, persisted synthetic write/reload, real bounded-AI vs template/mock (user prompt).
* Reuse actual runtime schemas; no invented API shapes, real writes, AI activation, implicit credentials, private data or network; no broad catches or success-shaped fallback (user prompt).
* Keep 60,000 homes and 980 operational cases distinct (user prompt).
* Ownership limited to the two new tools files and own tracking files; no edits to API/web/core/infra, `tools/rpi-checks.py`, workflows, KB index/log, addendum or parity matrix (user prompt).
* No closing keywords; PR uses `Refs #350`; draft PR to main; no merge (user prompt).
* Validate focused tests and the existing full gate (long lock timeout, new external output, official receipt verification) before push; pip, installed packages, no `PYTHONPATH=mvp`; repo-local privacy email; Conventional Commits with Copilot trailer (user prompt).

## Goals

* Provide a reusable deterministic offline verifier for the minimum owner-feedback prerequisites.
* Make absence of evidence visible as `blocked` or `not-run`, never success.
* Keep original #350 acceptance unmet unless literally proven by reviewed evidence.

## Scope and Non-Goals

### In Scope

* `tools/check-demo-feedback.py` and `tools/test_check_demo_feedback.py`.
* Dated research, plan, details, critique, changes and review artifacts for issue 350.
* Focused tests, the unchanged complete gate and receipt verification, a draft PR.

### Non-Goals

* Live or authenticated execution, Azure/tenant/RBAC/staff/ingress changes, deployments, paid inference, credentials.
* Changes to API, web, core, infra, `tools/rpi-checks.py`, workflows, KB index/log, addendum, parity matrix.
* Claiming #349, #360 or any #350 criterion complete; merging.

## Functional Requirements

* CLI `check-demo-feedback.py [--evidence FILE] [--expect-image-digest sha256:HEX] [--expect-role ROLE] [--expect-programme-cases N] [--format json|text]`; default expected programme cases 980.
  * Observable acceptance criteria: with no `--evidence` every check is `not-run`, overall `not-run`, exit 3; no file or network access occurs and no runtime package is imported.
* Report has `schema_version`, `offline_only: true`, `evidence_origin`, per-check `{id, status, reason}`, and an overall verdict; exit 1 `fail`, 2 `blocked`, 3 `not-run`; exit 0 is reserved for an overall `pass` that this slice cannot reach, and the report states `acceptance: not-accepted`.
  * Observable acceptance criteria: fixture-origin evidence never yields overall `pass`; because `spend_bound` and `admin_account` are always `not-run` gaps, overall `pass` is unreachable in this slice for any origin and the report lists them under `gaps`.
* `image_identity`: reference must be `<name>@sha256:<64 hex>`; tag-only fails; supplied expected digest must match; no image evidence is `not-run`, expected digest without evidence is `blocked`.
* `me_contract`: status 200 and body matches `projection.me_payload` shape plus `account{name,email,provider}`, `map{tiles,attribution}`, `navigation` equal to `workbench.navigation(user)`, and `work_queues` equal to `taskqueues.contract(ranking.CURRENT)` for non-contractors; role in `STAFF_ROLES` or `CONTRACTOR` and equal to `--expect-role` when given; contractors have empty counts and staff and no `work_queues`; non-contractors have integer `counts.mine`, `counts.hazards`, `counts.open` and a `staff` list of objects with string `email` and `role`; deployed-capture requires provider `trusted-proxy`.
  * Observable acceptance criteria: 3xx, 401, 403 or non-200 status fails with a denial-is-not-success reason.
* Self-declared fields (`origin`, `synthetic`, `restart_between_write_and_read`, `image.reference`) are bundle-schema fields owned by this harness, not runtime responses; the report lists them under `self_declared` and they cannot raise any verdict above `blocked` on their own.
* `case_write_reload`: evidence of before detail, `POST /api/cases/{id}/call` response, after-restart detail and before/after `/api/audit-check` reports; pass needs synthetic marker, write 200, contacts +1 whose outcome equals the request outcome stripped and truncated to 80 characters (as `log_call` stores it) and the channel, restart marker true, ledger intact with more entries and a changed head; held outcome is `blocked`; missing restart marker is `blocked`.
* `ai_evidence`: the slot holds the bare record returned by `POST /api/ai/priority` (a `GET` `{recommendation}` wrapper is rejected as the wrong shape); `source` and `fallback_reason` are the discriminators because `mode == "ai"` also appears on template fallback. The record has HTTP 200, `source == "ai"`, non-empty `model`, `validated` true, no `fallback_reason`, `mode == "ai"`, release with non-empty `id`, `version`, `digest`, numeric `latency_ms`, status `Proposed`, label `AI suggestion, not approved`, non-quarantined, `release_denied` false, `epoch_current` true, and every item with non-empty `cites`; `source == "template"` or workflow-only fails with the template/mock reason.
* `baseline_distinction`: programme total from `/api/cases?view=all` must equal the expected 980; a value equal to 60,000, or evidence claiming stock homes as cases, fails; missing is `not-run`.
* `spend_bound` and administrator-account evidence: always `not-run` (no runtime field).

## Non-Functional Requirements

* Determinism and offline operation.
  * Objective threshold or evaluation condition: identical input yields byte-identical output; no socket, subprocess or environment-credential use.
  * Observable acceptance criteria: tests assert JSON output stability and that only the supplied path is read.
* Safety of input handling.
  * Objective threshold or evaluation condition: evidence file at most 1 MiB, regular file, valid UTF-8 JSON object; specific exceptions only.
  * Observable acceptance criteria: oversized, missing, malformed or non-object input yields a clear `blocked` report, never a pass or traceback.
* Quality gates.
  * Objective threshold or evaluation condition: `ruff check` (version recorded) on the two files from the isolated venv, focused unittest, and a test asserting by AST that the script has no bare or `Exception` handlers; full gate and receipt verify on the exact head.
  * Observable acceptance criteria: receipt verification succeeds against current `origin/main`.

## Acceptance Criteria

* New tests cover pass, fail, blocked and not-run for each check and the overall cap for fixtures.
* Fixtures are built from the real runtime builders (`me_payload`, `navigation`, `taskqueues.contract`, ledger report) rather than hand-copied shapes.
* Fixtures never present a redirect, denial or asset existence as success.
* Only the two tools files and dated tracking artifacts changed; no closing keyword; draft PR states offline and unmet #349/#360/#350 criteria with exact head, receipt path and hash.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                 |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md                 |
| Phase details                    | .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md      |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-harness-plan-critique.md |
| Relevant research                | .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md          |
| Changes-record role              | .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-harness-changes.md is created by implementation |
| Planning execution and readiness | Complete; ready after critique disposition                                                 |
| Continuation context             | Confirmed automatic RPI Agent continues to Implement                                       |

## Sources

* .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md: evidence C1-C16, W1, W2 and decisions.
* src/README.md local RPI gate section: gate commands and `--extra-test` limits.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement the checker

* Intent: deterministic offline checker with the contract above.
* Dependencies: installed `src/core` and `src/api` packages in a venv.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Evidence loading, report model and CLI

* Requirement and evidence: Functional requirements 1-2; NFR input safety; C15.
* Expected result: bounded loader, four-state report, exit codes, JSON/text output.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Image, `/api/me`, case write/reload, AI and baseline checks

* Requirement and evidence: Functional requirements 3-8; C5-C14, W1, W2.
* Expected result: each check follows the plan's state rules and imports runtime constants and builders.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused tests

* Intent: prove every state and the fixture cap using runtime-built fixtures.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Unittest module with synthetic fixtures

* Requirement and evidence: Acceptance criteria 1-3.
* Expected result: `tools/test_check_demo_feedback.py` passes under the installed packages; no network or credentials.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md

<!-- rpi:phase id=P03 -->
### [ ] P03: Validate and publish

* Intent: Ruff and focused tests, review, committed candidate, unchanged complete gate, receipt, draft PR.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Validation, gate and draft PR

* Requirement and evidence: Non-functional quality gates; C15.
* Expected result: focused tests and Ruff pass; gate receipt verifies; draft PR with exact head, receipt and hash; not merged.
* Detail section: P03-T01 in .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md

## Dependencies

* Installed `zava_forward` core and api packages (pip, isolated venv): schemas are imported.
* Host heavy lock `/tmp/ama-rpi-heavy.lock`: serializes the full gate; use a long lock timeout.

## Critique Disposition

| Critique run and finding (single critique, verdict Revise, all direct) | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (High) AI slot ambiguous | resolved | Slot is the bare POST record; GET wrapper rejected; `source`/`fallback_reason` discriminate |
| PC-002 (High) overall verdict contradiction | resolved | Overall pass unreachable by design; exit 0 reserved; `acceptance: not-accepted` |
| PC-003 (Medium) self-declared markers | resolved | Listed as `self_declared`; cannot raise a verdict above blocked |
| PC-004 (Medium) outcome truncation, held outcome, counts/staff | resolved | 80-char truncation rule, held outcome blocked, counts/staff shape added |
| PC-005 (Medium) Ruff/AST/test invocation | resolved | Ruff version recorded; AST test for broad handlers; direct unittest recorded |
| PC-006 (Low) import timing | resolved | Lazy import only with evidence; failure is whole-run blocked |
| PC-007 (Low) disposition pending | resolved | This table |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-harness-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
