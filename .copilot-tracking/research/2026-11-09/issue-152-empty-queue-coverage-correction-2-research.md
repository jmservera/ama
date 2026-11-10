<!-- markdownlint-disable-file -->

# Task Research: issue-152-empty-queue-coverage-correction-2

| Field | Value |
|---|---|
| Date | 2026-11-09 (written from 05:22 UTC, prospectively, before any source edit) |
| Researcher / agent | RPI Agent via rpi-research (inline; no delegated lanes) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-2-research.md |
| Parent | correction 1 (`...-correction-1-*`) and the original task; all preserved unchanged |

## Research Brief

* Topic: correction 2 of the partial #152 slice (`Refs #152`). The coordinator's focused gate on `06954540eaa3dade49ba6ad3239377430043445d` has an actual failed API suite (`/tmp/ama-g152-c1-1109/0024-project-api.log`, 2038 tests, 841s, 1 failure, 363 skips). That receipt stays intact and is not a pass.
* Purpose: fix only the demonstrated failure, `test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy`.
* Non-goals: weakening the audit or adding a bypass, behaviour change, a trusted metadata source, scope growth, WCAG/AC-034/043/live/user claims.
* Tier: focused. Posture: focused (supplied failure evidence, named target). Output mode: convergence. Heavy gates, browser, SQL, Docker not run by direction.

## Extension Registry

| Kind | Candidate | Decision |
|---|---|---|
| Instruction | AMA repository instructions | selected |
| Skill | web-design-guidelines | deferred to Implement (before web edit) and Review (refresh) |
| Specialist | RPI Researcher | skipped, inline |

## Wave 1 (Wider)

* C1 `src/api/src/zava_forward/api/web/app.js:462-463`: the comment I added in correction 1 contains the word `provenance`.
* C2 `src/api/tests/test_content_standard.py:10`: `BANNED` matches `gates, holds, provenance, traces, snapshots, envelopes` case-insensitively on every line of the audited files, comments included; `copy_violations` (lines 17-25) is explicitly a conservative lexical guard.
* C3 `src/api/tests/test_content_standard.py:11-12`: `ALLOWED` is a short list of exact identifiers; a prose comment is not one.
* C4 `/tmp/ama-g152-c1-1109/0024-project-api.log` lines ~3164-3179: the only failure is the audit reporting `(462, '// No authoritative runtime source of current fixture provenance exists...')` for `app.js`.
* C5 `docs/reference/research/ux/content-standard.md:25,86`: the standard bans these internal terms in the core flow and prescribes a lexical search of the named web files.
* Local reproduction at the candidate head: `python3 -m unittest tests.test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy` fails with the same line 462 violation.

## Wave 2 (Deeper)

* The word "fixture" and the rest of the comment are not banned; only `provenance` triggers. A grep of `app.js` for the banned family found only line 462 as a new violation (earlier hits are allowed identifiers).
* The comment is nonessential: the function name, the fixed unknown text and the README already say what is active. The README and the test file are not in `AUDITED_FILES`, so correction 1's documentation wording is unaffected.
* Behaviour independence: a comment change cannot alter executable behaviour; `node --check` and the queue test confirm.

## Wave 3 (Contrarian)

* Alternative A: add the comment text to `ALLOWED` or exclude comments from the audit. Rejected: weakens the guard and is a bypass, forbidden.
* Alternative B: keep a rephrased comment avoiding banned words (for example "no trusted runtime record of the current demonstration data exists"). Viable, but a comment that restates the README adds a maintenance claim; counter-evidence is the repository's instruction to comment only what needs clarification.
* Alternative C (selected): remove the comment. The "always unknown" intent is covered by the README and by `test_unverified_provenance_never_becomes_a_declared_gap`. Removal is the smallest change and cannot reintroduce a banned term.
* Risk: the test name in correction 1's test file contains `provenance`; the test file is not audited, and it is old evidence. Left alone.

## Parent Synthesis

| Item | Disposition | Evidence |
|---|---|---|
| Remove the comment at app.js:462-463 | accepted | C1, C2, Alt C |
| Rephrase instead | rejected (not needed; adds a restating comment) | Alt B |
| Weaken audit or allow-list | rejected | Alt A, caller constraint |
| Edit audit test or old evidence | rejected | scope |
| Regression check | the existing audit test is the check: it fails on the old comment (reproduced) and must pass after | C4 |

## Closeout Record

* Research disposition: executed (one cycle; saturated for a one-line defect).
* Planning Readiness: Ready. Selected approach: Alternative C. No full-tier trigger found (comment only).
