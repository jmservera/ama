---
title: Resident chat routing implementation evidence
description: Original changes, validation and review handoff for the source-only fix
ms.date: 2026-10-31
---

Task ID and slug: resident-chat-routing. Implementation scope: P01 and P02;
P03 belongs to parent-owned Review/publication. Execution: Complete for P01/P02.
Plan and phase details under their dated 2026-10-31 resident-chat-routing paths.
Critique: one Complete / Revise, PC-001 and PC-002 applied to the ready plan.

## P01: Routing and copy

Implemented bounded ordered token/intent grammar after legacy exact matches.
Shared noun/own-case scaffolds accept status, receipt/missing documents, forms
and home/address questions without an unconsumed suffix. Typographic apostrophe
normalization is confined to the fallback. Four refusal examples retain the
original task-limit source and human help. Exclusions, specialist routes,
core answer facts and activation code are untouched.

Local judgment / PC-001 disposition: finite ordered grammar replaces the proposed
unordered vocabulary guard because complete single-request semantics matter.
No general parser, model, dependency or authority expansion is introduced.

## P02: Tests and validation

Added exactly three methods in existing `test_resident_chat_api.py`, a natural
question matrix and adversarial matrix, and extended the existing suffix/prefix
regressions to every new recognized question. Original tests are retained.
README documents finite recognition and its authority limits.

Baseline from `src/api`:
`PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_resident_chat_api test_resident_demo_api -q`.
Exit 0, 69 tests, no skips, 50.954 seconds. Expected failure-path application
logging appeared; the suite passed. Ruff 0.17.3 and mypy 2.4.1 are installed
(manifest 0.17.1 / 2.4.0). No dependency installation was needed.

Initial changed checks: four targeted tests exited 1 (two assertions) because
the new repair preservation row incorrectly used the protected-route helper,
which forbids optional advisor work. Repair's existing optional generated route
is intentional. Corrected the test to assert repair with AI off separately;
no production correction was required.
API Ruff lint and format passed; initial mypy exited 1 with 12 missing/untyped
import errors in unrelated API files. Pip reported the core/agents/API and Azure
Event Hub/IoT distributions absent. Restore the documented project dependencies
in an isolated session venv; do not suppress typing or alter manifests.

Restored missing distributions with pip into the session's external
`files/routing-venv` using `python3 -m venv` then
`python -m pip install --quiet -e 'src/core[sql,blob]' -e src/agents -e 'src/api[dev]'`.
Exit 0. This also restored pinned Ruff 0.17.1 and mypy 2.4.0.
No manifest change, shared-environment install, real service or secret was needed.

Final implementation validation from `src/api`, using that venv's Python:

| Command | Outcome |
| --- | --- |
| `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python -m unittest test_resident_chat_api test_resident_demo_api test_resident_chat_agenda test_resident_assistant_api -q` | Exit 0; 90 tests; no skips; 64.116 seconds |
| `python -m ruff check .` | Exit 0; all checks passed |
| `python -m ruff format --check .` | Exit 0; 67 files already formatted |
| `python -m mypy` | Exit 0; no issues in 126 source files |
| `git diff --check` from repository root | Exit 0 |

Validation covers both reported phrases, 49 natural question rows, 39 explicit
negative rows, every existing appended/prefixed/mixed request regression,
specialist precedence, own-record consent/access, agenda and fixed assistant
behavior. HTTP uses loopback and constructed data; configured-AI tests use
mock transport only. No tests were removed or skipped.

## Amendments, divergences and blockers

No approved-intent divergence. Current repository dated focused-tier policy
and explicit owner validation direction select lightweight checks, not a heavy
gate. No shared lock is acquired. No AI activation, real model calls, deployed
site requests, private dataset reads or infrastructure changes.

## Remaining work and Review handoff

P01/P02 and implementation validation are complete. Independent Review executed
once at `.copilot-tracking/reviews/logs/2026-10-31/resident-chat-routing-review.md`:
execution Complete, outcome Conformant, no material blockers. Independently
executed 3,485 routing assertions and verified all 28 original test methods
unchanged. RV-001 (Low) retains named human copy/live acceptance as a distinct
nonblocking follow-up. Original critique remains unchanged. Hosted/owner approval,
AI activation and resident release remain separate.

## P03: Publication preparation

Reviewed base remains `87bf629c630314f5be086697e322e1b0ec22277d` after fresh fetch.
Commit the source, documentation and original dated artifacts with the
GitHub-resolved local noreply identity and requested co-author trailer.
Focused checks must pass again on the clean committed candidate before push.
PR scope uses Refs #520 and Refs #563; no deployment or activation is authorized.

## P03: Publication outcome

Implementation and original RPI evidence committed as
`29b96698d3b5d4550de5f8cf86732aa50e44ce6f`, with authenticated repository-local
noreply author/committer and the requested Copilot trailer.
On that clean committed candidate, repeated the exact four-module focused
unittest command: exit 0, 90 tests, zero skips, 62.758 seconds. Repeated pinned
Ruff lint/format and mypy: all exit 0, 67 formatted files, 126 typed files.
`git diff --check` passed and worktree remained clean.

Fresh fetch advanced origin/main from the original reviewed base to
`9c67a399c62eb42f99ac46e1861b55526552c112` through PR #609. The initial
base-equality guard stopped before any push (exit 1). Read-only changed-path
inspection established browser-check, README, tooling and evidence changes;
chat routing, core answers and the selected unit modules were untouched.
Retained topic ancestry without rebasing, merging or rewriting history.

`git push -u origin HEAD` exited 0 without force.
`gh pr create --base main --head fix/resident-chat-routing` exited 0:
https://github.com/jmservera/ama/pull/611. Body includes all RPI artifact pointers,
focused-check evidence, unchanged AI/deployment boundaries, RV-001 qualification
and Refs #520 / Refs #563, with no issue-closing keyword.

This final evidence-only closeout updates current plan/state/publication facts
without modifying original critique, original Review or reviewed source/tests.
Repeat focused checks on its committed HEAD before the final ordinary push.
Hosted CI, owner merge approval and named resident-copy/live acceptance remain
pending; no deployment or AI activation was attempted.
