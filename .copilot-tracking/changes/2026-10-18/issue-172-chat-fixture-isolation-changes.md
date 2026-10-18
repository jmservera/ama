<!-- markdownlint-disable-file -->
# RPI Changes: issue-172-chat-fixture-isolation

## Metadata

* Task ID: 172
* Task slug: issue-172-chat-fixture-isolation
* Implementation date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-172-chat-fixture-isolation-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-172-chat-fixture-isolation-phase-details.md

## Execution Status

Completed implementation: P01/P02 within the full parent plan; P03 independent
Review and publication are later parent-owned work. Completed markers: P01,
P01-T01, P01-T02, P02, P02-T01. Remaining: P03/P03-T01 only.
Approved source boundary: public helper/test and directly related docs only.
First execution boundary: tests before helper. No engineering blocker.

## Execution Summary

Research actually executed and disproved the alleged baseline failure. Exactly
one independent critique executed: original Pass, zero findings. Implementation
and local verification now complete; original independent Review not yet run.

## Completed Work

### P01-T01: Failing-first coverage established

Changed `src/agents/tests/test_chat_fixture.py`: exact eligible thread-owner/action
coverage, separate eleven-perspective memory coverage, all-payload byte equality,
both-contractor active-target assertions, per-actor/action omission mutations and
invalid/self/mismatched/inactive target checks. Four test methods added, none
removed. No helper source change yet.

Executed the focused root command again: 15 tests, nine failing assertions/subtests.
Failures explicitly report the missing six contractor actor/action pairs, missing
kind and absence of required ValueError for no/expired/ineligible targets.
Existing baseline was green; this is intentional new-contract failing evidence.
P01-T01 complete; P01-T02 now dependency-ready.

### P01-T02: Explicit contractor actor denials

Changed `src/agents/tests/chat_fixture.py` only in isolation probe generation.
For each contractor persona, append read/list/search deny expectations targeting
the first active content-present thread owned by eligible non-contractor staff.
No valid target raises ValueError, rather than silently skipping required probes.
Focused suite now passes 15 tests, including six individual removal mutations,
invalid/self/mismatched/inactive targets and no/expired/ineligible target errors.
P01 and P01-T02 complete; source eligibility/lifecycle generators unchanged.

### P02-T01: Current public documentation and bounded validation

Updated agents README, dictionary, KB index and append-only log. Documented
eleven persona/memory perspectives versus seven eligible thread perspectives,
six explicit contractor actor denials, declarative limits and SN-08 remaining
partial with scope/volume approval unverified. No runtime or role mapping changed.
Original helper produces eight unchanged payload families and appended isolation
probes; existing `write()` computes the new aggregate hash for temporary output.
No tracked chat output/source hash exists to refresh. Public scenario source
hashes do not cover this helper; registry and frozen reports were left intact.

## Implementation-Time Plan and Detail Updates

None. No requirement or scope change, amendment or significant divergence.
Plan markers, details and handoff updated to completed P01/P02 and pending P03.

## Validation Record

| Check | Status | Evidence or reason |
| --- | --- | --- |
| System Python focused baseline | Failed, dependency unavailable | Three ModuleNotFoundError imports for zava_forward |
| Editable pip recovery | Passed | python3 -m venv .venv; .venv/bin/python -m pip install -q -e 'src/core[dev]' -e 'src/agents[dev]' -e src/api |
| Same focused baseline after install | Passed | 11 tests, no skips |
| Failing-first focused suite | Failed as intended | Same focused command: 15 tests, nine failure assertions/subtests identifying absent contractor matrix/kind and required target error |
| Focused suite after helper | Passed | 15 tests, no skips; root PYTHONPATH includes core/agents/API tests, .venv/bin/python -m unittest test_chat_fixture test_chat_provenance test_chat_fixture_roles -q |
| Focused plus public coupling | Passed | Same root prefix; modules test_chat_fixture test_chat_provenance test_chat_fixture_roles test_eval_registry test_synthetic_provenance test_scenario_manifest test_needs_inventory -q: 54 tests, no skips |
| Agents component CI discovery | Passed | cd src/agents; PYTHONPATH="$PWD/../core/tests" ../../.venv/bin/python -m unittest discover -s tests -q: 98 tests, no skips |
| Existing static lint | Passed | From src/agents: ../../.venv/bin/ruff check . |
| Existing format gate | Passed | From src/agents: ../../.venv/bin/ruff format --check .: 19 files already formatted |
| Existing type gate | Passed | From src/agents: ../../.venv/bin/mypy: no issues in 23 source files |
| Diff whitespace | Passed | git diff --check |
| Markdown/links | Passed, direct inspection | New relative links and anchors inspected; no repository-wide documentation build exists |
| Rename migration regression | Not applicable, not executed | No source path/import/migration metadata change; scoped public coupling tests selected instead |
| Live SQL/Azure/Graph/IAM/AI/browser/deployment | Not applicable, not executed | Public offline fixture/test-only change; no runtime/UI changed |
| Paid rubric, live personal data, notice/policy/volume approval | Prohibited/not executed | No authority or evidence invented |

Existing pyproject migration exemptions exclude this helper and fixture test
from format enforcement and ignore their mypy errors; lint has per-file rule
exemptions too. Passing component gates do not establish strict checks of exempt
files, accessibility acceptance, runtime enforcement or operational privacy.
Existing public source audit regressions deliberately retain three unresolved
historic external source entries; passing tests do not mean those were verified.

## Pre-Review Reconciliation

Ready. Plan markers and phase details match completed P01/P02; all required
implementation checks passed, completed-work evidence and handoff current.
P03/P03-T01 original independent Review remains unchecked and parent-owned.
No active engineering blocker. Approval/runtime follow-ups remain separate.

## Blockers

None for bounded engineering. Human policy/scope decisions remain separate.

## Remaining Work

Only parent P03/P03-T01 original Review/publication gate.

## Follow-Up Items

SN-08 approved scope/volume and runtime/human privacy/retention evidence remain
outside this fixture-only task, owned by owner/coordinator.

## Return-to-Caller State

Implement P01/P02 complete, review-ready. Original critique Pass preserved.
No amendment/divergence. Parent owns single original Review and publication
decision; this implementation result is not a self-awarded Review outcome.
