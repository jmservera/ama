---
title: Issue 350 feedback correction4 plan
description: Narrow runtime-compatible account and map JSON type validation
ms.date: 2026-10-23
---

Task ID: issue-350-demo-feedback-correction4.
Planning status: Bounded implementation and one Review completed. The owner
cleared the commit/gate sequencing blocker by authorizing a local-only commit
followed by one fresh full gate; publication remains blocked pending its exact
receipt and independent coordinator assessment. Task completion denotes loop
execution, not delivery acceptance.

## Executive Summary

Reject wrong JSON types for account name/email/provider and map
tiles/attribution without rejecting valid null tiles or empty contractor email.
Preserve all existing checks. The initial gate-before-commit attempt stopped at
the unchanged clean committed-HEAD prerequisite. The owner has authorized a
local-only commit followed by one fresh gate attempt; publication remains
blocked until exact receipt verification and independent coordinator
assessment.

## Sources

* Research: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction4-research.md
* Details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md
* Critique target: .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-correction4-plan-critique.md
* Changes target: .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-correction4-changes.md

## User Decisions and Requirements

* One ordered RPI loop; final owner-authorized correction, citing issue
  comment 6351734485 supplied in the request (not fetched).
* Only the two named tool files and this task's dated artifacts/state may change.
* Account fields must be strings; retain valid empty contractor email.
  Tiles must be null or string; attribution string. No content restrictions.
* Focused tests and targeted lint passed. The initial full-gate attempt stopped
  before checks because the candidate was dirty. Owner decision on 2026-10-23:
  authorize one local-only commit, then exactly one fresh unchanged full gate
  against b4d467cad84535ed106cffa1ae9aa303db7bfed2 with unique external output.
  Verify the receipt for that exact commit and base, then obtain independent
  coordinator assessment. No push before both pass; no further gate attempt if
  this one fails without new owner authorization.
* No Azure, tenant, network, credential or live-data actions; no fetch.

## Goals

Close the false-positive `me_contract` type gap while retaining runtime-compatible
empty/null values and all unrelated verdict behavior.

## Scope and Non-Goals

Canonical edits: `tools/check-demo-feedback.py`,
`tools/test_check_demo_feedback.py`. Generated targets: none. Removals: none.
No new helpers, dependencies, schema versions, provider allowlists or runtime
edits. No live/deployed/SQL/AI/human acceptance or original checkbox changes.

## Functional Requirements

* FR1: account name/email require `isinstance(value, str)`.
* FR2: keep existing nonempty provider and deployed trusted-proxy checks.
* FR3: map tiles accepts only None or str; attribution requires str.
* FR4: wrong types yield explicit FAIL diagnostics, never crash or PASS.

## Non-Functional Requirements

Preserve exact keys, role checks, navigation, work queues and other checker
paths. No implicit coercion. Cache-free tests and Ruff; no new dependencies.

## Acceptance Criteria

* Each field rejects every invalid JSON type using serialized synthetic fixtures
  for both staff and contractor; null tiles remains valid.
* Empty contractor email, empty attribution and other string contents introduce
  no unsupported content failure. Existing provider nonempty remains enforced.
* Focused suite and targeted Ruff checks pass on corrected source.
* Record the initial preflight refusal. Run the one owner-authorized fresh gate
  after the local-only commit and verify its exact-head receipt. If it fails,
  publication remains blocked and no further attempt is authorized here.
* One postimplementation Review preserves original adverse outcomes and routes
  residual work without another correction or Review cycle.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strict types and regressions

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add localized account and map type guards

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add focused JSON-type matrix and valid boundary tests

<!-- rpi:phase id=P02 -->
### [ ] P02: Validation and evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run corrected-source focused tests and targeted lint

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Attempt exactly one full gate and conditionally verify receipt

Attempt completed, not gate success: exit 1, `BLOCKED: Candidate has tracked
modifications or untracked inputs`. No checks ran, output/receipt not created,
verification unavailable. This remains historical and did not validate the
corrected candidate. Console preserved externally.

<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Commit locally and run the owner-authorized fresh gate

After persisting the owner's sequencing decision, commit the exact candidate
locally using the repository privacy-safe noreply identity. Do not push. Run
one fresh full gate against the current base with unique external output, then
verify the receipt against the exact candidate commit and base. If the gate or
receipt verification fails, stop without another attempt or publication.
The required `get_changed_files` tool is unavailable. The owner has authorized
a one-time `git diff --cached` review fallback for this isolated #350 commit.
Use it only to inspect staged content, then commit locally; no other diff
fallback is authorized.

<!-- rpi:phase id=P03 -->
### [x] P03: Review and handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute one Review and preserve publication blockers

One Review executed Complete; outcome Not accepted for publication.
RV-001 routes sequencing to owner/coordinator; RV-002 preserves independent
coordinator assessment as later work. No source correction or second Review.

## Test Ownership and Validation Lock

Primary implementer owns tests in the existing focused module; no test removal
or replacement. Maximum additions: eight test methods, parametrized with
subtests. Semantic coverage: staff/contractor, empty strings, null tiles.
Regression coverage: wrong JSON values None/list/object/bool/int/float for each
string field and all but None for tiles; every mutation must FAIL.
Every negative also checks the relevant account/map diagnostic; provider keeps
its existing generic account diagnostic. Every positive mutation explicitly
requires `me_contract` PASS, alongside overall/acceptance limitations. Positive
matrix includes empty and nonempty arbitrary strings in name/email/tiles/
attribution for both roles, null tiles, and existing provider-origin behavior.

Run existing `/tmp/fh350-venv/bin/python` with `PYTHONDONTWRITEBYTECODE=1` and
`-B -m unittest tools.test_check_demo_feedback -q`; if missing imports fail, only
then restore missing dependencies. Run Ruff 0.17.1 with `--no-cache`, isolated
E,F,W,B,BLE,I selection ignoring E501, plus isolated format `--check`.
Run `git diff --check` and inspect ignored status.

Use one external unique `/tmp` gate output; unchanged
`python3 tools/rpi-checks.py --all --base b4d467cad84535ed106cffa1ae9aa303db7bfed2 --out ...`.
Preserve console outside checkout even if preflight refuses output creation.
Do not edit during gate. If lock is reached, wait without interfering; use a
long lock timeout. The initial dirty-candidate attempt is already recorded. The
owner authorizes one new attempt after a local-only commit; verify only a
receipt actually emitted for that exact candidate. If it fails, do not retry,
push, or publish without new authorization.

## Critique Disposition

Exactly one independent final-candidate critique executed before source edits:
verdict Revise. Original critique is retained unchanged.

* PC-001 (High), rejected: the worker reports an execution-local prohibition
  on `/tmp` writes. That prohibition is not part of the primary caller's active
  instructions; the owner explicitly requires a unique `/tmp` gate output and
  points to preserved `/tmp` inputs. Do not substitute worker-local restrictions
  for this authorization. Retain external validation paths, existing interpreter
  and normal synthetic tempfile use. No source or gate bypass is authorized.
* PC-002 (Medium), applied directly: strengthen positive tests to require
  `me_contract` PASS per field/value for both roles including empty tiles; require
  field-contract diagnostics in negative tests. No user decision needed.
* Timing: correction4 source diff was empty at critique dispatch; this critique
  is genuinely preimplementation, unlike correction3. No second critique.

## Follow-Up Items

* After P02-T03 passes, obtain independent coordinator assessment of the exact
  committed candidate and receipt before any push. The owner authorized no push
  before both checks pass.
* Prior correction3 residual findings and all original issue #350 acceptance
  remain unchanged; this narrow task does not own them.

## Handoff

Source correction, focused validation and one Review are complete. The initial
full-gate preflight refusal remains recorded. The owner has resolved sequencing
by authorizing a local-only commit and one fresh full gate; that follow-up is
pending. Do not push before its exact receipt and independent coordinator
assessment pass.
No extra planner delegation: this compact single-trace change was drafted
directly; critique was the independent planning challenge.
