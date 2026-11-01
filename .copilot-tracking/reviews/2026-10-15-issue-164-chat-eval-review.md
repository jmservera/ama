---
title: Issue 164 chat evaluation review
description: Single post-implementation review
ms.date: 2026-10-15
---

## Execution and outcome

Original Review executed once. Its earlier "conformant with open items" outcome
is superseded by the PR 307 fix-first direction and the critical gap accounting
below. Current acceptance outcome: blocked by an open critical grounding gap.
Boundary: src/core, src/agents, src/api web and docs.

## Checks

* Dependency rule, no `mvp/` code, no new SQL, no enablement, synthetic data only: pass.
* Refusal precedes any model call; role and case re-checked each turn: pass.
* Criteria needing owner decisions or evidence are unticked in the changes file: pass.

## Routed findings

* Critical: unsupported claims with a valid citation remain accepted; claim-level
  grounding requires later work. This blocks enablement, not just evidence
  sufficiency. No approval or semantic grounding claim is made.
* Lexical refusal and output action checks can over-/under-match and remain
  paraphrase-bypassable. The model's own refusal behaviour remains unmeasured;
  actual-model/held-out/human evidence and owner decisions are still required.

## PR 307 owner-directed fix evidence (P05-T01 to P05-T03)

This updates the existing evidence record for the requested fixes; it is not a
second independent Review, new critique, human sign-off or enablement approval.

* Normalized refusal input covers NFKC, format/zero-width characters, common
  Cyrillic/Greek confusables and whitespace. Need/want-to, mark-X-as-consented,
  named/titled contact targets and Unicode variants have golden/core/API coverage
  and refuse before the model is called.
* Stale assistant-history scenario now passes because no assistant turns are
  carried to the model; existing stored conversations are preserved. User
  follow-up questions remain untrusted and can contain stale/injected content.
* Seeded plain-prose approval/consent assertions, including obfuscated variants,
  are withheld with no citations and unchanged case data. The scenario is a real
  pass with no gap marker; this establishes only lexical guard behaviour.
* Unsupported-claim-with-valid-citation remains a critical known gap: 24
  scenarios, 61 turns, 23 passes, one gap with two failing assertions. Category
  totals do not count it as passed; report `passed` is false, CLI exits 1 and
  enablement is `fail`, `disabled`, listing the gap in `blocking_gaps`. An actual
  subprocess JSON CLI check confirmed this, not only an aggregate test.
* Full src suites: core 261, agents 70, api 459 (92 existing skips), orchestrator
  17, importer 39; all successful. Ruff check, ruff format --check and mypy pass
  for all five projects. Missing orchestrator/importer editable packages were
  restored using pip after initial import failures, then fully rerun.
* ADR 0006 dependency tests pass; no runtime dependencies, SQL schema, working
  data, deployment, inference calls or enablement changes. Synthetic fixtures
  only. Existing SQL/environment skips do not prove SQL integration.
* Plan/details/changes and reference index/log are reconciled. Source fix
  `2f6f73a190e82909dc1013af726fef9e990c0ebd` committed and pushed normally to
  `feat/src-chat-eval-164`; this delivery-record reconciliation follows on that
  same branch. No force push, main push or merge. Acceptance remains blocked by
  the explicitly reported critical grounding gap; nothing is enabled.

## PR 663 review follow-up (2026-11-01)

* Copilot finding on unsupported binding lookups for the disabled chat task
  was valid and fixed in both consumers; chat stays disabled and its release
  evidence stays incomplete. Focused assistant, release and continuity tests
  and ruff pass. SQL-backed cases skip locally; the src-api and mssql CI jobs
  must confirm.
