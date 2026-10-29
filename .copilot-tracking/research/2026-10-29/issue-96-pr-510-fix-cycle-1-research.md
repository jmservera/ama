---
title: Issue 96 PR 510 fix cycle 1 research
description: Focused evidence for report-local source freshness caching
ms.date: 2026-10-29
---

## Research Brief

Refs #96; PR #510 fix cycle 1. Reduce duplicate source reads and hashes
inside each working form report without reusing freshness across reports.
Audience: implementation and independent review. Output mode: convergence.
Trusted evidence root: `.copilot-tracking/research/2026-10-29/`.

## Research Parameters

Focused posture, selected from the named source target and supplied finding.
Internal candidates: `src/core/src/zava_forward/core/form_review.py`,
`src/core/tests/test_form_review.py`, staging fixtures and core guide.
No external research is required for this internal optimization.
Questions: where is freshness computed; what identifies an exact source;
how can tests distinguish within-report reuse from cross-request caching?

## Direction Controls

User explicitly requests all four RPI phases, local commit only, no push,
no Azure, source under `src/`, tests outside the installed package, Refs only,
no hand-edit of `latest.json`. Preserve original RPI/review outcomes.
`git pull --rebase` completed first: already up to date. Clean topic branch
`docs/finance-96` matches open PR #510 targeting main. Initial HEAD:
`71196fb800699311c7fa377d598996cd4854ada8`.

## Extension Registry and Provenance

Repository instructions supply source/test layout, branch, identity and
publication gates. RPI skills supply phase evidence, one independent critique
and one independent Review. Inline research is appropriate for this small,
continuous trace; no independent research lane is needed.
UI/security/architecture skills are not relevant to the bounded backend fix.

## User Participation and Research Decisions

Intake is complete; no clarification is necessary. The full-loop request
explicitly authorizes each phase in this bounded manual run; it does not
start an open-ended automatic follow-up session.

## Research Cycle Log

Cycle 1, all waves inline:

1. Wider: traced `_report`, its view/action callers, staging evidence and the
   JSON/SQLite fixture. Both callers hold the store lock. Reflection: isolate
   the optimization in `_report`; do not share with candidate review.
2. Deeper: `_current` checks clean metadata, exact version/hash/kind and actual
   bytes. `_visible` checks historical permissions/scan status but does not read
   bytes. Reflection: memoize the boolean by all four source attributes, not
   by field, locator or document ID alone.
3. Contrarian: evaluated stale-schema short-circuiting, false results,
   distinct snapshots of one document and changed bytes without new metadata.
   Reflection: preserve schema short-circuit behavior, cache false as well as
   true, and create the dictionary anew inside every `_report` invocation.
   Global/request-wide caches would incorrectly broaden the lifetime.

Parent synthesis: accept C1-C4. No further cycle is justified: the bounded
trace answers every question; regression execution belongs to implementation.

## Evidence Log

* C1: `src/core/src/zava_forward/core/form_review.py:108-116` reads/hashes
  bytes per `_current` call; `:173-201` calls it once per sourced field.
* C2: `src/core/src/zava_forward/core/form_review.py:285-296` and `:320-360`
  call reports under locks; candidate verification remains independent.
* C3: `src/core/src/zava_forward/core/forms.py:427-434` supplies source ID,
  integer version, content hash and kind. Locator is field-specific, not
  source freshness. `src/core/src/zava_forward/core/doc_controls.py:151-154`
  confirms clean-source checking does not read source bytes.
* C4: `src/core/tests/test_form_review.py:20-96,182-207,281-312` provides
  JSON/SQLite fixtures and existing source/schema/visibility regressions.
  `src/core/tests/test_form_staging.py:20-75` supplies schema and batch helpers.

## Findings Mapped to Questions and Evidence

Where: C1/C2 prove redundant byte reads within the lock.
Identity: C3 supports `(id, version, content_sha256, kind)`.
Lifetime/test: C4 supports two fields anchored to one staged document;
spy on `docstore.get`, then return changed bytes on a later report.
Exercise both read-only view and diagnose action, plus exact-key separation
and reuse of negative freshness results.

## Alternatives and Decision State

Selected: a local typed tuple-to-bool dictionary inside `_report`.
Rejected: ID-only keys conflate snapshots; `setdefault` with an eager
`_current` argument still rereads; global/store/request caches outlive a report.
No change to `_current`, `_candidate`, scan visibility or schema semantics.

## Open Questions, Risks, and Residual Uncertainty

Do not weaken clean-source visibility, schema staleness or source identity.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Self-check: all questions mapped to C1-C4; no external claims or new dependency.
No research blockers. Historical finance acceptance and review findings remain
outside this narrowly scoped performance correction.
