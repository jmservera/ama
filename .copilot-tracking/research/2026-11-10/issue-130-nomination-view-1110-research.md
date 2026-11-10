---
title: Issue 130 nomination read-only view research
description: Original research for the read-only employee nomination view (issue 130), opened before source research
ms.date: 2026-11-10
---

## Status

Research disposition: executed. Planning Readiness: Ready.

Chronology note: the first witness call was an argument error (`--repo` must be the worktree path; no event written). Seq 2 `research-open` was refused (no research artifact named in state). Seq 3 `research-open` succeeded after a stub of this file and the state pointer existed; the stub was then replaced by this content. Both earlier attempts are preserved in the evidence log. Substantive source research began after seq 3.

## Scope and identity

* Task: initial, previously undelivered, read-only employee nomination view. Not a correction of historical #130; issue-wide correction balance is UNKNOWN. No post-review source correction batch is authorised.
* Base: `4244e84e763e6e01dd6012fcb9b650dae8d58e9d`, branch `feat/demo-nomination-view-130-1110`, declared target `feat/demo-nomination-ui-parent-81-1110`.
* Inputs read: admission issue JSON, merged lineage JSON (#509, #859, #1037, #1153: record-level, follow-up and review work, not a UI), the 130 section of the static source screen, `docs/reference/memory.md`, and the web guideline source (fetched 2026-11-10).

## Gap verification in this source

* `src/api/src/zava_forward/api/web/app.js:1065` defines the Resident tab as `[residentPanel, call, write, affectedChallengePanel]`. A search of `app.js`, `panels.js` and `role-screens.js` for `nominat` finds only an unrelated journey label (`role-screens.js:479`, "No screen shows a source account yet"). No renderer consumes `nomination_records` or `follow_up`. The gap is confirmed and not already implemented.
* Only other consumer: `src/core/.../taskqueues.py:171` builds work-queue items from `nomination_records` (server side, not this tab).

## Existing server contract (consumed unchanged)

* `Store.detail()` (`store.py:466-478`) adds `follow_up` to each record through `followup_view`, then removes `nomination_records` and `tenure_reports` for users without `challenge_references_visible`. `projection.py:187` also removes them for roles without appointment-evidence rights. API test `test_resident_api.py:352-364` already proves the denial. The web layer treats an absent key as role-denied and renders nothing.
* Record shape (`resident_decisions.py:943-1023`): `id`, `version`, `kind`, `original{reported_subject_ref, account, source, channel, recorded_by, at}`, `identity_status`, `support_needs`, `risk_flags` (all "Unknown" at intake), `owner`, `acknowledgement{reference, recorded_by, at, delivery: "Not verified by this system"}`, `next_update`, `non_digital_route`, `review_status`, `corrections[{version, reported_subject_ref, account, source, channel, recorded_by, at, challenge}]`, `reviews[{record_version, outcome, rationale, evidence_ref, competing_evidence_versions, reviewer, at, stale_from_version?}]`.
* `follow_up` (`resident_decisions.py:314-340`): `route_ready`, `missing[]`, `next_update_overdue` (true, false or "Unknown"), `re_review_pending`, `review_current`, `review_owner`, `not_inferred[]`.
* A review is current only when the last review's `record_version` equals the record `version`; a correction stamps `stale_from_version` on earlier reviews and keeps them.
* Legacy records can lack owner, acknowledgement, route, reviews or corrections; the projection already reports these as `missing`.

## Safety and authority boundaries

* The view shows only these server-authorised fields. Unknown support, risk or identity stays "Unknown", never "None". A recorded review is a staff record of a supplied outcome, not an approval, eligibility decision or resident consent.
* OD-41 does not block the constructed exercise demonstrator; OD-42 blocks operational real-resident use. Actual resident participation and representative authority stay unapproved. The view makes no contact, referral, assignment, eligibility or model call and adds no mutation, API, store or schema.
* Acknowledgement text must state delivery is unverified (the server field says "Not verified by this system").

## Implementation options

| Option | Result |
| --- | --- |
| A. New `nominationPanel(c)` in `panels.js` next to `residentPanel` and `affectedChallengePanel`, composed in the Resident tab at `app.js:1065` | Selected. Smallest hunk, follows existing patterns, no backend change. |
| B. Extend `residentPanel` | Rejected. It is already large and returns early on `resident_readiness`. |
| C. New role screen in `role-screens.js` | Rejected. The brief scopes the Resident tab. |

## Overlap declaration

* Parent #81 worktree: no `app.js` or `panels.js` changes.
* The #111 worktree touches `ops.js` only; the #148 worktree has `app.js` hunks near lines 466 and 821, away from 1065. No overlap with this plan's one-line `app.js:1065` hunk or the new `panels.js` function. No implementation dependency on unpublished work is admitted.

## Validation facts discovered

* No registered browser recipe or manifest hash references `panels.js`, `app.js` or the resident-tab checks (`workbench-manifest.json` holds navigation, not file hashes; `challenge_browser_check.py` is documented in `src/api/README.md` only). A manifest-hash update is therefore expected to be not applicable; re-verify at implementation.
* Existing patterns: node `vm` renderer tests (`tests/test_resident_service_screen.py`, `tests/test_finance_exposure_screen.py`) and Playwright checks reusing `ResidentApi` (`checks/challenge_browser_check.py`).
* The copy audit `tests/test_content_standard.py` bans the words gate, hold, provenance, trace, snapshot and envelope in `app.js` and `panels.js` copy.
* Baseline before edits (private venv with pinned versions): API `test_resident_api` 20 tests OK (1 skipped); Core `test_resident_decisions` 371 tests OK (132 skipped).
* Guideline source `vercel-labs/web-interface-guidelines/main/command.md` fetched in full on 2026-11-10.

## Planning Readiness

Ready. No unresolved dependency; no backend change planned.
