<!-- markdownlint-disable-file -->
# RPI Plan Critique: Hazard and Safeguarding Clock and Named Owner

## Metadata

* Task ID: ux-76-hazard-clock-owner
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the remaining unchecked acceptance criterion of Issue #76 (`Hazard and safeguarding items show a clock and named owner`) across queue projections (`My cases today`, `All open cases` shared work queue, specialist role queues) and case card responses (`Store.detail` / `/api/cases/{id}`) with explicit statutory/operational clocks (failing closed when timestamps are missing) and non-blank named accountable owners (surfacing escalation owner and unassigned flag when unallocated); do not modify `src/api/src/zava_forward/api/web/role-screens.js`; preserve counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`) and existing regression suites (`test_taskqueues.py`, `test_role_screens.py`, `test_safety_panel_ux.py`, `test_resident_preview.py`); add at most two unit test files (`src/core/tests/test_hazard_safeguarding_clock_owner_76.py`, `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`, removals `none`); run focused-tier validation (`ruff check`, `ruff format --check`, `mypy`, `unittest` across `src/core` and `src/api`); commit locally with `Refs #76` and the Copilot trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md`, `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md`, `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/insights.py`, `src/core/src/zava_forward/core/export_fields.py`, `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/core/tests/test_taskqueues.py`, `src/core/tests/test_sqlqueues.py`, `src/core/tests/test_hazard_referral.py`, `src/core/tests/test_resident_preview.py`, `src/api/tests/test_role_screens.py`, `src/api/tests/test_safety_panel_ux.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_list_export_inventory.py`, `src/api/tests/test_role_endpoint_inventory.py`, and `src/api/checks/case_view_ux_browser_check.py`.
* Decisions, dependencies, and acceptance criteria considered: Issue #76 acceptance criterion (`Hazard and safeguarding items show a clock and named owner`), FR-1 through FR-6 in the plan candidate, research citations C1 through C18, receipt-is-not-acceptance ownership rule (`FR-003`), plain-language copy standard (`SA-003`), role-based default-deny projection (`PR-002`), and focused validation tier rules (`D4` / `#1294`).
* Assessment boundary: Evaluates completeness, internal consistency, and codebase contract compatibility of `P01` through `P04` and `P01-T01` through `P04-T01` against the supplied research and referenced source/test files. Does not execute runtime test suites or inspect external hosted CI runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / C4, C5, C11, C17, C18 | Partial | Clock states and fail-closed missing-timestamp states are well defined, but `P01-T01` places `destination` ahead of `sender` before acceptance (`PC-002`). |
| FR-2 / C2, C6, C7, C8, C9 | Partial | Queue blocker enrichment covers `app.js` and `roleScreensView`, but standalone safeguarding items trigger a `"Mismatch"` error in unmodified `role-screens.js` specialist safety screens (`PC-001`) and miss `SqlStore` roster/revision/overdue parity (`PC-003`). |
| FR-3 / C3, C10 | Partial | `Store.detail` enriches `d["hazards"]` and `d["safeguarding_items"]`, but omits standalone safeguarding projection compatibility with `role-screens.js` and `caseView` `openHaz` (`PC-001`), plus `projection.hold_notes` redaction on safeguarding free-text fields (`PC-004`). |
| FR-4 / C12, C13, C14 | Partial | Preserves unmodified `role-screens.js` and counted accessibility/export baselines, but omits `snapshot(s)` and `envelope(s)` from the banned-word list enforced by `test_content_standard.py` (`PC-004`). |
| FR-5, FR-6 / C15, C16 | Partial | Test file additions (`2`) and removals (`none`) honour caller limits, but Phase 4 omits the required local commit task with `Refs #76` and privacy-safe GitHub email (`PC-005`). |
| P01 / P01-T01 | Partial | Needs acceptance-gated direct-owner precedence (`PC-002`), `MEMBERSHIP_REVISION` bump, standalone safeguarding `overdue_tasks` coverage, and an explicit discriminator ignoring note-only `safeguarding={"note": ...}` fixtures (`PC-003`). |
| P01 / P01-T02 | Partial | Needs `Store._work_context` fallback to `self.staff`, `Store.counts`/`gate_reasons`/`status_line`/`focus` parity and safe owner lookups (`PC-003`), projected `d["hazards"]` + scalar `owner` backfill for unmodified `role-screens.js` (`PC-001`), and `projection.hold_notes` coverage for safeguarding free text (`PC-004`). |
| P02 / P02-T01 | Partial | Needs `caseView` `openHaz` safeguarding detection, deduplicated read-only rendering for projected standalone safeguarding items (`PC-001`), deterministic fallback `.safety-clock-owner` on raw `test_safety_panel_ux.py` fixtures, and full `CopyAudit` banned-word guardrails (`PC-004`). |
| P03 / P03-T01, P03-T02 | Partial | Needs assertions for unaccepted-referral `sender` ownership (`PC-002`), `safety-lead`/`hazard-triage` non-mismatch data shape (`PC-001`), `SqlStore` membership refresh (`PC-003`), and `can_see_reason` redaction on standalone safeguarding items (`PC-004`). |
| P04 / P04-T01 | Partial | Covers lint, format, typecheck, and unit suites, but omits `test_content_standard.py`, `test_sqlqueues.py`, `test_role_endpoint_inventory.py`, and the caller-required local Git commit step (`PC-005`). |

## Verdict

* Verdict: Revise
* Rationale: Five substantive, codebase-verified planning gaps (`PC-001` through `PC-005`, three High and two Medium) would cause standalone safeguarding items to render a `"Mismatch"` error in unmodified `role-screens.js` specialist safety screens, assign unaccepted referrals to `destination` instead of `sender` in violation of `FR-003`, leave `SqlStore` queue caching and `Store` helper methods out of parity, risk `CopyAudit` (`SA-003`) and `PR-002` redaction regressions, and omit the caller-required local commit step. Every finding is a direct planner correction resolved by current caller direction and codebase contracts; no user decision is required.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Standalone safeguarding items trigger a Mismatch error in unmodified role-screens.js specialist safety queues and miss open-safety hoisting in web/app.js

* Related IDs: FR-2, FR-3, FR-4, P01-T02, P02-T01, P03-T02, C7, C8, C9, C11
* Evidence: `src/api/src/zava_forward/api/web/role-screens.js` lines 818-885; `src/api/src/zava_forward/api/web/app.js` lines 1013, 1136, 1149, 1181-1200; `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` (`P01-T02`, `P02-T01`)
* Concern: `P01-T02` sets `row["hazard"] = True` (via `insights.has_hazard(c)`) for cases with open standalone safeguarding items while placing standalone safeguarding items only in `d["safeguarding_items"]` and leaving `d["hazards"]` populated solely from `c["hazards"]`. Because caller requirement #2 forbids modifying `role-screens.js`, `hazardQueue.summary` (`role-screens.js` line 875: `if (!c.hazards.length && row.hazard) return [flag([row.id, "Mismatch. The list flags a hazard but the case returns none. Open the home to check."])];`) will render a false `"Mismatch"` error in both the `Building safety referral queue` (`safety-lead`) and `Repairs and hazard triage` (`hazard-triage`) specialist role queues whenever a case has only a standalone safeguarding item. In addition, `hazardScreen` (`role-screens.js` line 836) iterates `c.hazards || []` (even though its own caption on line 842 promises every recorded hazard and safeguarding item is listed), `hazardFollowUp(h)` (`role-screens.js` lines 818-825) renders `"Owner: Unknown"` when an unreferred item omits scalar `h.owner`, and `caseView` (`web/app.js` line 1013: `const openHaz = (c.hazards || []).some(x => !x.released);`) fails to show the `"Safety issue open"` badge, `.blocked` state, or top-of-journey `safetyPanel` hoisting when only standalone safeguarding items are open.
* Impact: Standalone safeguarding items fail to display a clock or named owner in the two specialist safety role queues (`safety-lead` and `hazard-triage`), surface a false data-integrity mismatch banner instead, show `"Owner: Unknown"` on unallocated unreferred items in `role-screens.js`, and fail to hoist the safety panel on the case card.
* Smallest useful change: In `P01-T02` (`Store.detail`), backfill scalar `item["owner"] = enriched["named_owner"]` whenever `not item.get("owner")` on projected safety items (keeping `owner` a `str` scalar as required by `export_fields.status_inputs`), and project normalized standalone safeguarding items (with `category` defaulting to `"Safeguarding"`, `released` normalized to `bool`, `item_kind="safeguarding"`, `standalone_safeguarding=True`, plus full `clock_*` and owner metadata) into both `d["safeguarding_items"]` and `d["hazards"]` (appended after `c["hazards"]` so existing cases without standalone safeguarding retain identical `d["hazards"]` counts and mutation indices for `test_hazard_referral.py` and `case_view_ux_browser_check.py`). In `P02-T01` (`web/app.js`), compute `openHaz` across open `c.hazards` and open `c.safeguarding_items`, and deduplicate `standalone_safeguarding` items in `safetyPanel` so each standalone safeguarding item renders once as a read-only card without `hazard-refer`/`hazard-receive` index mutation forms.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T02`, `P02-T01`, and `P03-T02` in `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` and `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` specifying `d["hazards"]` standalone safeguarding projection, scalar `owner` backfill, `caseView` `openHaz` coverage, deduplicated read-only rendering in `safetyPanel`, and API/UI test assertions confirming `c["hazards"]` is non-empty and `"Unknown"`-free when `row["hazard"]` is `True`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Direct-owner precedence places unaccepted destination ahead of sender, violating FR-003 receipt-is-not-acceptance

* Related IDs: FR-1, P01-T01, P03-T01, C2, C4, C11
* Evidence: `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` (`P01-T01` Boundaries); `src/core/src/zava_forward/core/workflows.py` lines 406-447; `src/core/src/zava_forward/core/taskqueues.py` lines 37-40, 129-130, 212-213, 355; `src/api/src/zava_forward/api/web/role-screens.js` lines 818-822
* Concern: `P01-T01` specifies direct-owner resolution order as `accepted_by -> destination -> sender -> item.get("owner") -> item.get("named_owner")`. In `workflows.refer_hazard` (`workflows.py` lines 417-422), `destination` is populated as soon as a referral is sent (`sent_at`), before receipt (`received_at`) or acceptance (`accepted_at`). Under `taskqueues.DEFINITIONS["unowned"]` (`taskqueues.py` lines 37-40: a proposed receiver is not a confirmed owner and the sender retains chase responsibility until acceptance) and `hazard_clocks` (`taskqueues.py` line 355: `owner = _person(h.get("accepted_by")) or _person(h.get("sender"))`), `destination` does not own the item until `accepted_at` / `accepted_by` is recorded.
* Impact: Every sent or received-but-unaccepted referral would report `destination` as the allocated `named_owner` (`unassigned=False`), violating `FR-003` ("receipt is not acceptance") and contradicting `clock["owner"]` (`sender`) on the same safety panel and queue row.
* Smallest useful change: Change `P01-T01` direct-owner precedence to `accepted_by -> (destination only when item.get("accepted_at") is truthy) -> sender -> item.get("follow_up") -> item.get("owner") -> item.get("named_owner")`, and use unaccepted `destination` only as the first candidate for `escalation_owner` when no direct follow-up owner is recorded. Add an explicit test case in `P03-T01` asserting that a sent/received-but-unaccepted referral resolves `sender` as `named_owner` and does not promote `destination` before `accept_hazard`.
* Action owner: planning_parent
* Exact resolving evidence: Updated direct-owner precedence rule in `P01-T01` of `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` and `FR-1`/`P01` of `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md`, plus a sent-unaccepted referral assertion in `P03-T01`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Incomplete Store, SqlStore, and taskqueues parity for standalone safeguarding items, SQL staff-roster access, queue revision invalidation, and note-only fixture discrimination

* Related IDs: FR-2, FR-3, P01-T01, P01-T02, P03-T01, P04-T01, C2, C6, C7, C15
* Evidence: `src/core/src/zava_forward/core/taskqueues.py` lines 6, 102-158; `src/core/src/zava_forward/core/store.py` lines 164-179, 418-451, 605-608; `src/core/src/zava_forward/core/sqlstore.py` lines 777, 799-806, 976-980, 1507-1511; `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py` lines 104, 234; `src/core/tests/test_taskqueues.py` lines 173-186, 222-265; `src/core/tests/test_sqlqueues.py` lines 48-115
* Concern: Four tightly coupled backend contracts are underspecified across `P01-T01` and `P01-T02`:
  1. `Store._work_context(c, user, data, cases)` (`P01-T02`) passes `staff=data.get("staff", [])`, but `SqlStore._refresh_queue_membership` (`sqlstore.py` lines 799-803) builds a synthetic `data` dict containing only `"buildings"` and `"procurement"`, so `data.get("staff", [])` is always `[]` during SQL queue refreshes. Furthermore, `SqlStore._queue_fingerprint` (`sqlstore.py` line 777) caches `queue_blocked`/`queue_overdue`/`queue_unowned` keyed on `taskqueues.MEMBERSHIP_REVISION` (`taskqueues.py` line 6, currently `3`), which `P01-T01` does not increment.
  2. `P01-T01` Likely Targets and Expected Result mention `overdue_tasks(...)` and safeguarding overdue deadlines, yet `P01-T01` Boundaries omits `overdue_tasks(...)` rules. Adding standalone safeguarding recorded deadlines (`response_due_at`/`due_at` and `resident_update_due_at`) to `overdue_tasks` is required for `queue="overdue"`, whereas adding derived awareness-only target deadlines into `overdue_tasks` when `response_due_at` is absent would break existing `test_taskqueues.py` assertions (`lines 173-186, 222-265`).
  3. `P01-T02` updates `SqlStore._row` `hazard` via `insights.has_hazard(c)` (making `SqlStore.counts` count standalone safeguarding items via `SUM(hazard)`), but `P01-T02` Boundaries omits `Store.counts` (`store.py` line 450, still `any(not h["released"] for h in c["hazards"])`) and leaves raw `h["owner"]` / `h["category"]` lookups in `Store.gate_reasons`, `Store.status_line`, `Store.focus`, and `Store.require_safety_clear` that raise `KeyError` when unallocated items omit `"owner"` or `"category"`.
  4. `resident_preview_fixture.py` line 104 attaches `safeguarding=dict(note=f"{CANARY}-SAFEGUARDING-NOTE-{cid}")` to `SYN-C1`, `SYN-C2`, and `SYN-C3` as a privacy-canary note container, then calls `store.issue_work_order(...)` on `SYN-C1` and `SYN-C2` (`line 234`). `P01-T01` wording (`plus dict/list case.get("safeguarding") if structured as items`) lacks a concrete schema discriminator to prevent note-only `{"note": ...}` dicts from being treated as open safeguarding items.
* Impact: SQL queue refreshes miss the staff roster and serve stale cached `queue_*` flags on reopened databases; `Store.counts` diverges from `SqlStore.counts`; unallocated items without `"owner"` trigger `KeyError` in `Store.status_line`/`gate_reasons`/`focus`; standalone safeguarding items with overdue recorded deadlines miss `queue="overdue"`; or `test_resident_preview.py` / `test_resident_preview_api.py` break on `safeguarding={"note": ...}`.
* Smallest useful change:
  1. In `P01-T01`: increment `taskqueues.MEMBERSHIP_REVISION` from `3` to `4`; specify that `overdue_tasks(...)` evaluates recorded `response_due_at`/`due_at` and `resident_update_due_at` on open standalone safeguarding items (`safeguarding/{i}/...`) while keeping derived awareness-only operational clocks out of `overdue_tasks` when `response_due_at` is unrecorded; and define an explicit discriminator for `case.get("safeguarding")` dicts requiring at least one item-identifying key (`id`, `status`, `state`, `priority`, `category`, `kind`, `aware_at`, `raised_at`, `reported_at`, `response_due_at`, `due_at`, `owner`, `sender`, `destination`, `accepted_by`, `released`) so note-only `{"note": ...}` dicts are ignored.
  2. In `P01-T02`: pass `staff=data.get("staff") or list(self.staff.values())` in `Store._work_context`; update `Store.counts` to use `insights.has_hazard(c)`; and replace raw `h["owner"]` / `h["category"]` indexing in `Store.gate_reasons`, `Store.status_line`, `Store.focus`, and `Store.require_safety_clear` with safe lookups backed by resolved `named_owner` and default category.
  3. Include `test_sqlqueues.py` and `test_resident_preview_api.py` in `P04-T01` targeted checks.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, `P03-T01`, and `P04-T01` specifications in `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` and `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` incorporating all four parity and schema rules.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Incomplete CopyAudit (SA-003) banned-word list, unredacted standalone safeguarding free-text fields in projection.hold_notes, and raw fixture fallback in safetyPanel

* Related IDs: FR-3, FR-4, P01-T01, P01-T02, P02-T01, P03-T02, P04-T01, C12, C15
* Evidence: `src/api/tests/test_content_standard.py` line 14; `src/core/src/zava_forward/core/projection.py` lines 30-31, 135-145; `src/core/tests/test_hazard_referral.py` lines 598-627; `src/api/tests/test_safety_panel_ux.py` lines 25-39
* Concern:
  1. `test_content_standard.py` line 14 enforces `BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)` across every line of `web/app.js` (including comments and string literals), whereas `FR-4`, `P01-T01`, and `P02-T01` only name `gate`, `hold`, `provenance`, and `trace`, omitting `snapshot(s)` and `envelope(s)` (while `P01-T01` itself uses the word `snapshot` when describing clock evaluation).
  2. `projection.hold_notes` (`projection.py` lines 135-145) only redacts `NOTE_KEYS` plus `source`/`job` when `"category" in c and "released" in c`, and `reason`/`evidence` when `"actor" in c`. Standalone safeguarding items carrying free-text `summary` or `reason` (or missing normalized `category`/`released`) would bypass `NOTE_HELD` redaction for staff roles without `can_see_reason(user)` (`Retrofit Coordinator`, `Grants and Evidence Officer`, `Quality Inspector`, `Programme Support Officer`).
  3. `test_safety_panel_ux.py` lines 25-39 calls `safetyPanel({hazards}, "ZF-1", ...)` directly in Node with raw hazard dicts lacking `c.work` and pre-projected `clock_*`/`named_owner` fields; leaving client-side fallback ambiguous in `P02-T01` risks either omitting `.safety-clock-owner` on raw fixtures or rendering `undefined`.
* Impact: Introducing `snapshot(s)` or `envelope(s)` in `web/app.js` breaks `CopyAudit`; unredacted safeguarding `summary`/`reason`/`source`/`job` violates default-deny role projection (`PR-002`); and isolated `safetyPanel` calls risk missing or malformed clock/owner text.
* Smallest useful change:
  1. Update `FR-4`, `P01-T01`, and `P02-T01` to list the full banned pattern `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` across both UI copy and comments in `web/app.js`, and include `test_content_standard.py` and `test_role_endpoint_inventory.py` in `P04-T01`.
  2. In `P01-T02` (`projection.py`), ensure projected standalone safeguarding items always include `"category"` and `"released"` and update `hold_notes` to replace non-empty free-text `"summary"` and `"reason"` on safety/safeguarding items (`"category" in c and "released" in c` or `c.get("item_kind") == "safeguarding"`) with `NOTE_HELD` when `not can_see_reason(user)`, while keeping structured `clock_*` and owner fields visible to staff.
  3. In `P02-T01` (`web/app.js`), require `safetyPanel` to always render `.safety-clock-owner` by computing deterministic fallback clock and owner strings from raw item fields and `staff` whenever pre-projected `clock_label` / `named_owner` are absent.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-4`, `P01-T01`, `P01-T02`, `P02-T01`, `P03-T02`, and `P04-T01` in `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` and `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Phase 4 omits an executable task/step for the caller-required local commit with Refs #76, privacy-safe GitHub email, and Copilot trailer

* Related IDs: P04, P04-T01
* Evidence: `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` (`User Decisions and Requirements` vs `Phase 4: Validation`); `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` (`P04-T01`); `.github/copilot-instructions.md` (`Branch and Pull Request Workflow`)
* Concern: Caller requirement #6 explicitly requires creating a local commit with `Refs #76` and the Copilot `Co-authored-by` trailer without pushing, and repository instructions require configuring repository-local `user.email` as `{id}+{login}@users.noreply.github.com` from `gh api user` before committing. Although `User Decisions and Requirements` notes this requirement, the Phase Checklist (`P04`) and Phase Details (`P04-T01`) end after running lint, typecheck, and unit tests without any commit or diff-boundary verification task.
* Impact: Following the phase checklist and task details literally leaves workspace changes uncommitted at the end of implementation, failing caller requirement #6.
* Smallest useful change: Add `P04-T02` (or explicit final steps in `P04-T01` gated on green validation) to inspect `git status --short` and `git diff --name-status` (verifying `role-screens.js` is untouched, test removals `0`, new test files `<= 2`), resolve `{id}+{login}@users.noreply.github.com` via `gh api user`, set `git config --local user.email`, commit locally on `feat/76-hazard-clock-owner` with `Refs #76` and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, and confirm no `git push` is executed.
* Action owner: planning_parent
* Exact resolving evidence: Explicit local commit verification and commit step added to Phase 4 in `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` and `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md`.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Strong architectural reuse: Enriching `taskqueues.py` (`work["blockers"]` and `work["hazard_clocks"]`) plus `Store.detail` and `web/app.js` `workSummary` propagates clock and named-owner display across `My cases today`, `All open cases`, `roleScreensView` specialist role queues, and `/api/cases/{id}` without duplicating queue-ranking logic or touching `role-screens.js`.
* Regulatory and baseline discipline: Awaab's Law 24-hour emergency, 7-day investigation, and 14-day work-start thresholds, fail-closed missing-timestamp states, and explicit preservation of counted accessibility/form/export baseline tests (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`) are accurately grounded in repository evidence (`C12` through `C18`).
* Residual risk (accepted within focused-tier scope): Statutory 5-working-day written-summary and 12-week preventative-works clocks in later Awaab's Law phases are not separate stored timestamps on current synthetic hazard fixtures; surfacing recorded `response_due_at` / `resident_update_due_at` alongside deterministic 24h/7d/14d operational awareness clocks and fail-closed `awaiting_timestamp` states keeps timing claims transparent without inventing unrecorded statutory milestones.

## Questions or Blocking Evidence Gaps

* None. All five findings (`PC-001` through `PC-005`) are resolved deterministically by existing caller constraints and repository code contracts without requiring user input.

## Limitations

* Critique was conducted strictly by static inspection of the supplied research, plan, phase details, and repository source/test files without modifying files or executing test runners.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md` and `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md` directly to incorporate `PC-001` through `PC-005`, then finalize the plan for implementation without another critique pass.
* User response required: No
