---
title: Resident assistant 469 changes
description: Implementation evidence, amendments and validation
ms.date: 2026-10-27
---

Task #469; automatic RPI Implement, full plan scope. Plan and phase details:
`.copilot-tracking/plans/2026-10-27/resident-assistant-469-plan.md`,
`.copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md`.

## P01 - Design and contracts

Design note written before source edits. Single critique executed; PC-002
applied, PC-001 rejected as contrary to current explicit owner direction.
No actual model or Azure calls permitted. Dependencies installed using pip in
external /tmp/ama-469-venv after missing zava_forward import. Initial branch
feat/resident-assistant was clean, matches parent at 55c239d9; no source changes
inherited. Parent fetched and unchanged.

## P02 - API and panel

Completed P01-T01/P02-T01/P02-T02. Core typed Topic/CaseProgress/Advice and
provider protocol, deterministic FakeProvider, optional disabled Azure adapter.
The adapter only exchanges topic enums, validates endpoint/deployment, refuses
redirects, bounds prompt/output/reply, reserves before credentials/transport,
checks expiry again after credentials and never retries/refunds.

POST /demo/assistant reuses fresh view authorization, origin/CSRF checks and
bounded body parsing. Strict one-key topic schema; generic explicit errors.
Independent assistant.js panel, one demo.js mount call and one script include;
two scoped CSS rules. No MAX_MAPPINGS or sibling behavior changed.
Component READMEs and knowledge-base index/log point to durable design.

## P03 - Validation and publication

Completed P03-T01 (four test/check files, no removals). Core focused 6 passed;
initial API focused 16 passed after correcting the test to refresh expired
CSRF before asserting expired session denial. Changed core ruff/mypy passed.
Changed API ruff/mypy passed after local typing/format corrections.
Local actual HTTP app started over constructed showcase fixtures and Chromium
completed six focused groups: keyboard/status/sources/notice; document/form help;
network failure/retry; delayed old response across logout/new resident; 320px
reflow/reduced motion; expired-session recovery/no JS errors/no external page
requests. Screenshots retained externally at /tmp/ama-469-browser/.
Desktop/mobile images inspected. Final results:

| Check | Result |
| --- | --- |
| core `python -m unittest discover -s tests -q` | 1378 run, OK, 186 skipped; 635.795s |
| API `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | 1083 run, OK, 308 skipped; 699.565s |
| final focused API `test_resident_demo_api test_resident_assistant_api test_resident_assistant_provider` | 54 passed, 29.526s |
| final focused core `test_resident_assistant` | 6 passed |
| changed Python ruff check | Pass: 2 core, 5 API/check files |
| changed Python mypy | Pass: 2 core, 5 API/check files |
| formatter check | Pass on 2 core and 4 API files; checks directory follows existing formatter exclusion |
| final local Chromium script | All six groups passed, including final panel source |
| node --check assistant.js and demo.js | Pass |
| git diff --check; protected resident_showcase.py unchanged | Pass |

Full discovery includes existing opt-in/integration skips, not full SQL/browser/
live acceptance. API discovery began before the final optional-adapter
expiry-during-token guard/test was added; final focused 54 tests, changed-file
lint/types and Chromium validate the final source. Core source was unchanged
during its full run. Full logs external: /tmp/ama-469-core-tests.log and
/tmp/ama-469-api-tests.log. No failures; existing negative-path exception output
and ResourceWarnings remain in those logs.

P03-T02 complete as validated implementation handoff, not publication.

Full long gate not run per current owner instruction; hosted CI,
rubric and owner review remain separate and unclaimed.

## Amendments and Divergences

No material divergence. Local topic choice rather than free-text chat is an
explicitly documented prototype boundary, not generated AI functionality.

## Remaining Work and Follow-ups

No implementation blockers or unchecked implementation tasks. One independent
Review and parent-owned commit/push/PR remain. Real-provider
activation, durable accounting and human/accessibility acceptance are future
owner-gated work.

## PR 474 P04 implementation addendum (2026-10-27, Refs #466)

Scope: only the three supplied review threads and focused regressions.
Research Ready; independent P04 critique Pass. Implementation starting with
provider/HTTP regressions, Account disclosure assertions and native focusable
busy submit. Existing unrelated untracked gate records remain untouched.
Original outcomes and findings above are preserved. No full gate or Azure.

P04-T01/T02/T03 complete: Account closed/hidden then open/visible assertions;
reserve moved inside existing normalization; guarded native `aria-disabled`
submit never moves focus. Added exactly two unit methods and existing browser
assertions, no files/removals. Before the fix both new regressions failed:
raw OSError and actual HTTP RemoteDisconnected. Afterward all 19 focused
provider/API tests and all three offline Chromium scripts (assistant, Account,
sensors) pass. Assistant checks include success/network/HTTP failure focus,
pending duplicate suppression, no focus stealing, logout/new-resident isolation,
320px/reduced motion and expired-session recovery. Full API discovery is running.
Initial lint found import spacing and one long test name; corrected without
behavior changes. SQL-backed browser runner is outside the no-secrets scope.

P04-T04 final validation: from src/api, the owner's exact PYTHONPATH with
`python3 -m unittest discover -s tests -q` in the existing installed
`/tmp/ama-469-venv` ran 1089 tests in 407.206s, OK (308 existing skips).
Log: external session `files/pr474-api-tests.log`. After import/test-name
formatting corrections, all 19 focused tests reran successfully; production
source did not change during full discovery. All three offline Chromium scripts
passed; ruff, format, mypy (four Python files), node syntax and diff checks pass.
Original five Markdown evidence prefixes verified byte-preserved. No material
divergence; P04-T04 completion clarified as implementation handoff rather than
unperformed publication. `git pull --no-rebase origin feat/resident-interactive`
reported already up to date at 9c0d71960b954ea607912840e8d804dfe888987e.
Ready for one independent P04 Review; no implementation blockers.
