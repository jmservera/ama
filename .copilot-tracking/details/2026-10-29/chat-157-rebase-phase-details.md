---
title: Chat 157 rebase phase details
ms.date: 2026-10-29
---

Task ID: 503-chat-157-rebase-2026-10-29.

<!-- rpi:phase id=P01 -->
## P01: Rebase and compose

<!-- rpi:task id=P01-T01 -->
### P01-T01

Run git rebase origin/main (authorized history rewrite). Resolve each replayed
commit, including rubric-only commits that become empty; preserve historical
artifacts. Main copy for .github/rubric and scenario-manifest.json. Both log
and README contributions must remain. Complete when main is ancestor and
there are no unmerged entries. New RPI evidence is initially untracked.
Freeze fetched base 3e742ef13e45cb9de0590cbb5cb33e4996f5112e and old
head 2931b7f1e3158f273e5b99ad73b828af1e88eab0. Compare final ancestry,
main-owned bytes and both documentation contributions to those references.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Compose branch actor_role into main's paired writer and extracted _refer.
Copied messages use original actor_role or empty legacy provenance, not inbox
owner role. Receipt uses actual acting user role. Keep SQL upper sequence bound
and finite JSON snapshot read unchanged. Core existing regulatory tests cover
bounded reads/referral; add at most two tests only for missing integration
coverage. No tests removed. No broad regulatory file replacement is sufficient.
Allowed additions if missing, both in core/tests/test_regulatory_chat.py:
test_regulatory_writers_preserve_actor_roles (paired/receipt/copied roles);
test_legacy_referral_keeps_unknown_actor_role (empty legacy provenance).

<!-- rpi:phase id=P02 -->
## P02: Validate

<!-- rpi:task id=P02-T01 -->
### P02-T01

/tmp/mv exists but importing zava_forward failed. Install existing core, agents,
API dev distributions editable before validation. Avoid foreign private data.
Record interpreter and resolved package source paths.
Install while holding `flock -n /tmp/ama-rpi-heavy.lock`; contention blocks
setup, without polling, bypassing or mutating a foreign environment.
Verify installed imports without PYTHONPATH as well as requested source paths.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Run from project folders, PYTHONPATH=src:tests plus sibling src/tests.
Core: test_chat_panel, test_chatthreads, test_chat_memory, test_chat_privacy,
test_regulatory_chat, test_regulatory_usage, test_scenario_manifest,
test_dependency_rule. Agents: test_chat_model, test_chat_eval, test_chat_fixture,
test_chat_provenance. API: test_chat_panel, test_chat_isolation,
test_chat_fixture_roles, test_regulatory_chat_api, role endpoint inventory.
Actual module names confirmed before execution. Run all three packages' Ruff
check/check-format and mypy; core/API required. Also isolated lint for changed
regulatory UX harness. Do not run full API unless shared lock is acquired and
held during execution. Full gate/SQL/browser/deployment acceptance is not
inferred from this focused integration.
Exact commands from each folder: `/tmp/mv/bin/ruff check .`,
`/tmp/mv/bin/ruff format --check .`, `/tmp/mv/bin/mypy`.
Tests: `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests
/tmp/mv/bin/python -m unittest <selectors> -q`, using modules above and
test_dependency_rule for agents/API; API role module is test_role_endpoint_inventory.
Main's RegulatoryTests.test_json_usage_snapshot_excludes_append_crossing_byte_limit
and test_usage_reads_only_bounded_audit_metadata_and_survives_restart cover
bounded reads; test_conflict_automatically_routes_exact_pair_once_per_stored_turn
covers referral, test_regulatory_usage covers offline receipts.
Chatthreads restart/migration tests cover roles and unknown legacy storage;
chat_panel role-switch tests cover accounting/history composition.
Optional full API discovery requires held nonblocking exact shared lock
/tmp/ama-rpi-heavy.lock throughout. Contention means not run, no waiting.

<!-- rpi:phase id=P03 -->
## P03: Review and persist

<!-- rpi:task id=P03-T01 -->
### P03-T01

Reconcile plan/details/changes and run exactly one independent Review against
the resolved diff and evidence. Route any Review findings to later work, do not
cycle back within this task. Resolve authenticated account with gh api user,
set repository-local noreply email for author/committer, commit with Conventional
Commit and requested trailer. Do not push. Record no-Azure boundary and that
fresh hosted CI/remote mergeability cannot be verified without coordinator.
Acceptance-invalidating Review findings block ready handoff. Preserve original
adverse outcome; nonblocking follow-ups need explicit rationale and owner.

## Current Execution State

P01-T01/P01-T02 and P02-T01/P02-T02 complete, with changes evidence reconciled.
P01/P02 complete. Both named additions implemented; no tests removed.
Core focused 123 tests pass without skips; agents focused 49 plus regulatory
24 pass without skips; API focused 101 pass with one opt-in browser skip.
Full API separately admitted and held the shared lock: 1,324 tests, exit 0,
318 skips, 469.210s. Skips are not SQL/browser/live acceptance.
Ruff check/check-format/mypy passed for core, agents and API.
P03-T01 complete: single independent Review executed Complete / Residual work,
implementation Conformant; 5faa132970904d15ef159b328efdad802eb5fd67 locally
commits reviewed implementation and evidence. Identity/trailer/Refs, clean
status, main ancestry and main-owned bytes verified. Original Review retained.
RV-001 persistence fulfilled; RV-002/003 remain distinct follow-ups.
No implementation source edits are planned after Review. Coordinator owns
fresh publication gate, exact-head assessment and hosted/human acceptance.
