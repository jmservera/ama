---
title: Issue 350 feedback checker correction 5 changes
description: Red-first JSON overflow and exact schema-version correction evidence
ms.date: 2026-10-23
---

## Scope and Opening State

Task ID: issue-350-demo-feedback-correction5.
Approved plan: .copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md.
Details: .copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md.
Full correction implementation scope P01/P02; P03 Review/local commit follows.
One preimplementation independent critique is complete; PC-001 applied,
PC-002 rejected with reason in plan. No source changes before that critique.
No material divergence, amendment or new scope decision.

## P01-T01: Red-First Regressions

Added five test methods without removals. Raw overflow matrix: three tokens
across latency, unchecked rank and nested unchecked list/dict payload. Schema
matrix: True, False, 1.0 and 2; normal supported integer is separate.
Finite fraction/large exponent/underflow/negative controls plus numeric-looking
strings retain field scope. Strengthened invalid-input helper with no-runtime
sentinel, per-check BLOCKED diagnostics and offline/gap assertions.

Before any checker edits, ran:
`PYTHONDONTWRITEBYTECODE=1 /tmp/fh350-venv/bin/python -B -m unittest
tools.test_check_demo_feedback.InputSafety.test_exponent_overflow_is_blocked_before_runtime
tools.test_check_demo_feedback.InputSafety.test_schema_version_requires_supported_integer_type -q`.
Exit 1, 2 methods, 13 failing subtests in 0.012s.
Nine overflow and True/1.0 cases wrongly reached runtime; False and 2 already
blocked but lacked the new explicit integer diagnostic. These are distinct
assertion failures, not 13 newly discovered input-acceptance bugs.
Full red console retained in session files/correction5-red.log.

## P01-T02: Minimal Loader Correction

Implemented after red evidence in tools/check-demo-feedback.py:
typed parse_finite_float(str) -> float converts and rejects non-finite numbers
using math.isfinite; json.loads invokes it globally alongside parse_constant.
Existing ValueError handler gives invalid-JSON BLOCKED without new catch.
Schema version exact int type and supported value are checked together, with
an explicit integer diagnostic. Module documentation states both constraints.
Large integers, finite floats and existing component rules remain untouched.

## P02-T01: Local Validation

Initial green run: 77 tests passed in 0.222s. Ruff lint passed; format check
requested one array-literal layout change in the test module. Applied the
existing Ruff formatter to the two named tools: one changed, one unchanged.
This is ordinary local formatting judgment, not a design amendment.

Final local source validation after formatting, all exit 0:

* `PYTHONDONTWRITEBYTECODE=1 /tmp/fh350-venv/bin/python -B -m unittest tools.test_check_demo_feedback -q`:
  77 tests passed in 0.238s.
* `/tmp/fh350-venv/bin/ruff check --isolated --no-cache --select E,F,W,B,BLE,I --ignore E501 tools/check-demo-feedback.py tools/test_check_demo_feedback.py`:
  All checks passed (Ruff 0.17.1).
* `/tmp/fh350-venv/bin/ruff format --isolated --no-cache --check tools/check-demo-feedback.py tools/test_check_demo_feedback.py`:
  2 files already formatted.
* `git diff --check`: passed. Code diff inspected; only the two named tools.
* `git status --short --untracked-files=all --ignored`: only expected tool edits
  and new correction5 artifacts; no ignored inputs.

Final console: session files/correction5-local-checks.log. Earlier green:
session files/correction5-green.log. No dependencies installed, no private
datasets read, no network/AI/SQL operations invoked by checker tests.
Full gate and receipt verification deliberately not run under this request.
Earlier receipt covers the supplied old head only.

## Plan Reconciliation Before Review

P01/P02 markers now complete, details retain the same implementation/validation
contract, and P03 Review/local commit remain pending. No unrelated plan markers
or earlier evidence changed. No implementation divergence, new requirement,
significant amendment, unresolved in-scope finding or source blocker.

## P03: Review and Atomic Local Commit Handoff

One postimplementation local RPI Review executed Complete. Outcome Conformant
for the bounded correction; no in-scope findings, no repeat Review. RV-001
routes new exact-head full gate/official receipt and subsequent independent
assessment to coordinator. Prior adverse outcomes remain untouched.

gh api user returned id 8036360/login jmservera. Repository-local user.email
configured to 8036360+jmservera@users.noreply.github.com; both author and
committer explicitly use it. Local commit includes only the two named tools
and seven correction5 artifacts, Conventional Commits/Refs #350 and required
Copilot coauthor trailer. The host lacks get_changed_files; staged content is
inspected with bounded git diff --cached rather than claiming unavailable
tool execution. This is a host-tool substitution, not a source-scope change.

Final checklist/state is prepared for inclusion atomically with the correction.
The successful containing commit object is commit-execution evidence; no
commit SHA is guessed in an artifact that must itself be committed. If commit
fails, this closeout does not establish a completed local handoff.
Owner explicitly requested stop, so session stops after the local commit;
no follow-up task is started.

Red console SHA-256:
8eb4f2fc516984df419b5e090f754bf0098d9e880b7039cd7ca779b78dde8a8a.
Final local-check console SHA-256:
02b89bc3697224cad2c96cd577698af39e555b0ef50b02475bb2c068fbbcf147.
Both retained under the session files directory named above.

No SQL durability, deployed acceptance, actual AI execution, issue acceptance,
criteria ticks, push, PR update, amend, merge or full-gate execution occurred.
No source blocker remains; publication evidence remains outside this task.
