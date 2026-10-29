---
title: Progress lifecycle element-type correction research
description: Focused evidence for PR 540 malformed lifecycle correction
ms.date: 2026-10-29
---

## Research Brief

Task `progress-dashboard-533-correction3`, Refs #533, PR #540. Investigate
malformed history elements/actions and sibling closure/return elements so both
read endpoints retain unknown-date coverage rather than crashing or inventing
known lifecycle evidence. Audience: implementer and independent reviewer.
Output mode: convergence, preparing planning. Posture: focused, selected from
the owner's named function, reproduction and bounded audit.

## Direction Controls and Extensions

* Owner requests the complete RPI correction loop, local Conventional Commits,
  no push, no Azure, no force push and no closing keywords.
* Reuse `feat/progress-dashboard-533`; first `git pull --rebase` succeeded
  with no changes, and PR #540 remains open against main.
* Repository instructions govern source placement, synthetic-only evidence,
  package validation, retention and privacy-safe commit identity.
* RPI Research selected; subsequent RPI skills own their phases.
* Web design skills are not applicable: no web implementation or UI audit.
* Research specialists skipped: one tightly coupled parser/storage trace is
  clearer inline. Independent critique and final Review remain separate.
* Interaction unavailable; supplied scope is sufficient. No new legal,
  company, data-generation, schema or operational approval claims.

## Questions and Candidate Areas

1. Which element types crash or silently weaken lifecycle reconstruction?
2. Which sibling assumptions require guards without changing valid replay?
3. How can JSON/SQLite and the browser exercise the actual read contracts?

Inspect `src/api/src/zava_forward/api/progress.py`, its tests/checks, package
guides and previous correction evidence. No external research is required.

## Research Cycle Log

### Cycle 1: Wider

Opening evidence: the parser hashes `action` without a type guard and skips
non-dictionary history elements. Closures and returns already reject
non-dictionary elements before their `.get` calls. Reflection: inspect the
test fixture and persistence boundaries before selecting additional guards.

### Cycle 1: Deeper

C1: `src/api/src/zava_forward/api/progress.py:78` checks list containers and
closure/return dictionary elements, but not history dictionary elements.
C2: `src/api/src/zava_forward/api/progress.py:93` skips non-dictionaries and
non-synthetic rows together. The `action` membership at line 96 requires a
hashable value; even hashable non-strings silently contribute no evidence.
An inline Python reproduction confirmed null yields a known open lifecycle
and synthetic list/dictionary actions raise TypeError.

C3: `src/api/tests/test_progress_dashboard.py:304` already persists malformed
auxiliary evidence, opens a separate JSON/SQLite reader and checks both
endpoints' exact coverage/date-filter behavior. SqlStore's ordinary save runs
queue validation, so corrupt retained evidence is written to the constructed
SQLite case body directly, not passed through unrelated mutation validation.
Reflection: extend this single existing matrix across all three collections,
preserving a valid history around each malformed element to prove no silent
skip, and add synthetic-action cases to that same persistence harness.

### Cycle 1: Contrarian

C4: `src/api/src/zava_forward/api/progress.py:100` only replays labelled
synthetic history, while closure/return `event_type` uses equality and flags
use identity (`is True`); these safely ignore lists/mappings as non-transitions.
All timestamps pass through `observed` (`progress.py:56`), which safely rejects
non-string timestamps. No additional hashing, indexing or truth coercion of
elements exists within the function. Missing auxiliary collections default to
empty; missing/null synthetic action must instead be unknown.

C5: `src/api/tests/test_progress_dashboard.py:364` preserves empty/missing and
non-transition dictionary auxiliary evidence. Extend positive controls to
malformed timestamps/tags on non-transitions, legitimate synthetic narrative
actions and unlabelled dictionary history. Do not validate action type on
unlabelled dictionary rows: they are intentionally outside simulation replay.
Reject all non-dictionary history elements, including unlabelled/null ones.

C6: `src/api/checks/progress_browser_check.py:28` exercises real authenticated
reads, table/API equality, archive filtering and eleven axe states with a pinned
asset. `src/api/README.md:10` documents this bounded lifecycle contract.
The scenario manifest pins four other files, not these correction targets.
Reflection: no new schema, core change, browser source edit or pin update needed.
History container tests and auxiliary persistence tests are complementary;
keep their existing assertions, extend malformed primitive coverage.

## Alternatives and Current Decisions

* Selected: preflight every collection's element type and reject non-string
  actions only on synthetic rows before membership/replay. This is explicit,
  fail-closed and preserves intentional narrative handling (C1-C5).
* Rejected: catch TypeError, stringify actions or skip malformed rows. Those
  conceal incomplete evidence and can fabricate a known lifecycle.
* Rejected: validate arbitrary event tags/flags as strings/bools. Equality and
  identity already have safe defined behavior; broadened schema rules would
  change valid non-transition dictionary semantics without caller evidence.
* No unresolved implementation decision. Required validation may be blocked by
  shared-lock admission or dependencies; preserve actual results, never infer.
* Prior correction original evidence is retained. Session-history search found
  no additional matching recent session; checked repository evidence instead.

## Completion Self-Check

One inline Wider/Deeper/Contrarian cycle complete in order. All three questions
answered with C1-C6. Scope is covered; further sources are redundant for this
focused correction. No workers or external claims. Handoff: C1-C6, guard strategy,
existing persistence harness and no active blocker.

## Evidence, Decisions and Readiness

Research disposition: executed. Planning Readiness: Ready.
Only research and required workflow tracking are being written in this phase.
