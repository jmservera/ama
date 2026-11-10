---
title: Issue 130 nomination read-only view plan details
description: Phase details for the read-only nomination section (issue 130)
ms.date: 2026-11-10
---

## Phase 1: renderer and composition

Files: `src/api/src/zava_forward/api/web/panels.js` (new function placed after `residentPanel`), `src/api/src/zava_forward/api/web/app.js:1065` (insert `nominationPanel(c)` after `residentPanel(c, id, refresh)`).

`nominationPanel(c)`:

* Authorised means the server supplied `c.challenge_targets` or an array `c.nomination_records` (store.py:472-479 and projection.py:187-190 remove them together for denied roles). Return `null` when neither is present (role-denied). When authorised and the records key is absent or empty (records are created lazily), show the empty state.
* Identity objects (owner, recorded_by, reviewer) render through a helper that shows `name` (and role when present) and falls back to "Unknown"; objects are never stringified. Review outcome text is shown in full, for example "Accepted for human eligibility review", with the fixed note "A recorded review is a staff record, not an approval or an eligibility decision."
* `section.card#nominations` `aria-labelledby` heading `h2` "Nominations and self-referrals". Lead text: "Read only. This view records what was supplied. It does not contact a resident, decide eligibility, change priority or assign an owner." Empty list: "No nomination or self-referral is recorded for this home."
* One native `details` per record (first five open) with a `summary` of record id, kind, version, review status. Inside: `h3`-free `dl` groups under `h3` "Original supplied account" and, per correction, `h3` "Corrected account, version N (competing evidence; the original is kept)". Fields: Unverified subject reference, Account, Source, Channel, Recorded by, Recorded at.
* "Follow-up" group: Named owner, Next update (date, "Overdue" / "Not overdue" / "Unknown"), Staffed non-digital route, Acknowledgement reference with "Delivery unverified" text, Identity status, Support needs, Risk flags (server value, fallback "Unknown"), Missing items from `follow_up.missing`, plus `follow_up.review_owner` and `follow_up.not_inferred` as "This view does not infer: ..." (fallback "Unknown").
* "Human review" group: each review with outcome, reasons, evidence reference, reviewer, time, versions of competing evidence, and a word label Current or Stale as defined in the plan; empty means "No human review recorded."; `re_review_pending` adds "Correction awaiting human re-review."
* All values are set as text nodes through the existing `h()` helper; long values use `overflow-wrap:anywhere` through an existing class if available, otherwise a minimal inline style-free approach (no new CSS unless needed).
* Copy avoids banned words (gate, hold, provenance, trace, snapshot, envelope).

## Phase 2: node renderer test

`src/api/tests/test_nomination_screen.py` loads `panels.js` in a node `vm` with a minimal DOM stub and asserts text for: original plus correction plus stale review; current reviewed version; legacy record missing owner, acknowledgement, route and fields; no records; role-denied (absent key returns null); markup in supplied text stays text; unknown support and risk never rendered as None.

## Phase 3: browser check

`src/api/checks/nomination_browser_check.py` reuses `ResidentApi`, builds records through the real authorised HTTP routes (record, correct, review by an independent staff user), builds records in this order: record, independent review, then correction (stale review and re-review pending asserted), then a second independent review (current asserted), then logs in as the resident-workflow user and a denied role, opens `#/case/ZF-1?tab=resident`, asserts literal text, Tab and Enter/Space keyboard use of the summary, no non-GET requests while viewing, axe scan (existing pinned hash), reduced motion, 320/1280 reflow, server case state unchanged. Browser launch only under the heavy-resource lock, loopback only.

## Phase 4: validation and review

Run the focused commands in the plan, including the existing `challenge_browser_check.py` as an impacted check, rendered target-size assertions for summary controls in the new browser check, and an authorised-empty-case assertion, write the changes record and a single Review.

## Dependencies

None unpublished. No backend, Core, SQL or dependency manifest edits.
