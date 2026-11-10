<!-- markdownlint-disable-file -->
---
title: Issue 159 route-level validation receipts plan (prospective)
description: Prospective bounded plan for one metadata-only zero-call receipt on three authenticated HTTP 400 chat branches; awaits a frozen parent and a confirmed correction ledger
ms.date: 2026-11-09
---

## Task Metadata

* Task slug: issue-159-route-validation-receipts. Refs #159 only; no closing keyword.
* Research: .copilot-tracking/research/2026-11-09/issue-159-route-validation-receipts-research.md
* Phase details: .copilot-tracking/details/2026-11-09/issue-159-route-validation-receipts-details.md
* Critique: executed once on this final candidate (self-conducted, not independent). Artifact: .copilot-tracking/reviews/plans/2026-11-09/issue-159-route-validation-receipts-plan-critique.md. Verdict and dispositions are recorded there and not repeated.
* Status: PARTIAL preparation. Research and plan only. No Implement or Review phase exists and none is claimed.

## Entry gates (all required before any code)

* [ ] G1: parent PR 1313 local clean head frozen and qualified (currently d3810ffe48 with hosted `src-namespace` FAILURE; C4 native fix running). Never implement against the RED parent or correct it through this child.
* [ ] G2: ordinary integration of the qualified parent (or its merge to main) into this branch, preserving `server.py` intents, then a fresh research check of `_chat` and `chat_panel.py` against that exact base. No silent rebase.
* [ ] G3: coordinator or owner confirms the #159 correction ledger (research table) and that this initial implementation is a feature increment that consumes no correction cycle.
* [ ] G4: nonqueued resource admission for any shared heavy resource (SQL only if triggered, see Phase 3).

## Scope (approved, 7 Nov comment 6711077218)

* Three authenticated 400 branches: unstored-ask extra keys; stored ask extra keys; stored ask explicit `skill: null`.
* Each: keep the 400 and message, append exactly one metadata-only validation receipt, zero model calls, token usage unknown (`None`).
* Never retain the question, unknown field names or values, or invalid skill values. Valid turns still produce exactly one normal receipt; permission denial, foreign or missing thread and workflow fallback are unchanged.
* Excluded: anonymous 401 and no-actor policy, migration, UI, model activation, live call, cloud, deployment, credentials, private data, adjacent unreceipted 400s listed in the research, and any whole-#159 tick.

## Phases (prospective, unchecked)

* [ ] Phase 1 (core): add `ChatPanel.record_validation_refused(user, tid=None)` in src/core/src/zava_forward/core/chat_panel.py. It re-reads the user with `iso.current_user`; on `PermissionError` or `LookupError` it records the existing access-rejected receipt and re-raises. Otherwise stored (`tid` set) audits `_receipt(tid)` with outcome `rejected` as `chat.turn`; unstored audits `{"outcome":"rejected","model_calls":0}` as `chat.turn.unstored` with an empty target.
* [ ] Phase 2 (api): in `_chat`, call it before each of the three `ValueError` raises (unstored before the key check; stored for extra keys and for `skill: None`). Keep the existing messages and the generic 400 mapping.
* [ ] Phase 3 (tests, existing files): src/api/tests/test_chat_panel.py HTTP receipt-count tests with sensitive canaries for the three branches, a positive normal-turn control (+1 receipt, model call counted) and a removed-user control; one core test in src/core/tests/test_chat_panel.py for the helper. Red-before-green with the source change absent is shown by a negative control.
* [ ] Phase 4 (validation): owner demo-targeted tier. Run only the two test modules above plus the existing denial, foreign-thread and fallback tests in them, the repository's pinned ruff check and format on changed files, and the maintained API strict mypy and core mypy on changed files. Disposable SQL is used only if the audit seam or `sqlstore.py` changes; the plan does not change them, so none is planned. Record exact commands, counts, exits, skips and identities.
* [ ] Phase 5 (record and handoff): actual changes and review artifacts, local commit with the privacy-safe identity, handoff, proposed PR body using `Refs #159`.

## Decisions to settle in the first implementation turn

* D1 (planned default): permission denial takes precedence. For unstored-ask the key check moves behind the panel's user recheck, so a user removed between the role gate and the handler gets 403 with the existing access-rejected receipt, not 400.
* D2 (planned default): the unstored refusal target is empty, not the body `case_id`, so no unvalidated body content is retained.
* D3: the stored refusal reuses outcome `rejected`, matching the existing invalid-skill receipt, so no new outcome vocabulary or schema.

## Validation and budget notes

* Tier: owner-selected demo-targeted (2026-11-09). The 7 Nov comment and the repository security-sensitive rule ask for FULL; the coordinator brief replaces blanket full local gates for this demo push. This is flagged for the independent reviewer, not resolved here. Hosted CI and independent exact-head review stay mandatory.
* Correction budget: unknown spent (evidenced 1, possibly 2). Any correction after review needs issue-specific authorization; this plan grants none.

## Unmet after this slice (expected)

* Criterion 6 (named screen-reader and announcement acceptance), the anonymous 401 and no-actor tokenomics policy, adjacent unreceipted 400s, OD-51 cost. Whole #159 stays open.
