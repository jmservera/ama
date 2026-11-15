<!-- markdownlint-disable-file -->
# RPI Phase Details: Reconcile feat/demo-233-same-home-tensions-0825 with origin/main

## Metadata

* Task ID: pr-1639-feat-233-merge-origin-main
* Task slug: feat-233-merge-origin-main
* Related plan: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md, docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Initiate merge and reconcile `src/core` conflicts | ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Reconcile `src/api` web, endpoint-inventory, and README conflicts | ready | P02, P02-T01, P02-T02 |
| P03 | Verify scenario manifest, run focused validation suite, and stage frozen merge candidate | ready | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Initiate merge and reconcile `src/core` conflicts

### Context

Research (`C1`, `C5`-`C10`, `C12`, `C14`) confirmed that merging `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) into `feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`) produces 6 conflicts in `src/core`. Four of those (`job_pack.py`, `staff_intake.py`, `projection.py`, `test_job_pack.py`) plus `src/core/README.md` stem from parallel implementations of Issue `#132` (`#1682`/`#1725` on `HEAD` and `#1666` on `origin/main`), alongside `#76` (`safeguarding_items` redaction in `projection.py` and `accountable_owner` in `store.py`) and `#82` (`GateError` `rules` argument in `store.py`).

### Intent

Start the no-commit merge and resolve all 6 `src/core` conflicts additively so every helper, field, redaction rule, audit action, and `GateError` rule works across both branches' test suites.

### Boundaries

* Included: `git merge --no-commit origin/main`, `src/core/src/zava_forward/core/job_pack.py`, `src/core/src/zava_forward/core/staff_intake.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/store.py`, `src/core/tests/test_job_pack.py`, and `src/core/README.md`.
* Excluded: Non-conflicting `src/core` files, `src/api` conflicts (owned by `P02`), and running `tools/rpi-checks.py`.

### Likely Targets

* src/core/src/zava_forward/core/job_pack.py: Retain `import re`, `NON_INSTRUCTION_NOTICE`, `INSTRUCTION_CLAIMS`, `_PLACEHOLDER_WORDS`, `_ROLE_WORDS`, `_NAME_ALLOWED`, `ADVISORY_NOTE`, `named_owner`, `assert_advisory`, `reject_instruction_claim`, and unified `escalation`.
* src/core/src/zava_forward/core/staff_intake.py: Combine `_valid_contact`, `_configured_owner`, `route_escalation`, `escalation_destination`, `escalation_options`, `_view_escalation`, `_read_dependency`, staff-directory role check, dual `escalations`/`field_escalations` storage, and dual `field_escalation_raised`/`field_escalation_routed` audit entries.
* src/core/src/zava_forward/core/projection.py: Combine `safeguarding_items` stripping with unified advisory escalation `summary` holding (`NOTE_HELD`) that skips overwriting `note` and `contract_notice`.
* src/core/src/zava_forward/core/store.py: Combine `taskqueues.accountable_owner(active.get("owner"))` and `[gates.BOOKING_RULES["safety"]]` in `require_safety_clear`.
* src/core/tests/test_job_pack.py: Retain all 5 test methods from both branches.
* src/core/README.md: Reconcile `field-escalate` documentation prose.

### Dependencies

* None.

### Validation Expectations

* `PYTHONPATH=src:tests /usr/bin/python3 -m unittest discover -s tests -q` in `src/core` passes completely.
* `/home/azureuser/.local/bin/mypy src tests` and `/home/azureuser/.local/bin/ruff check src tests` in `src/core` pass cleanly.

### Completion Evidence

* Zero unmerged index entries under `src/core/` (`git ls-files -u -- src/core` empty) and passing `src/core` unit tests, `mypy`, and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Start no-commit merge and verify the 10-file conflict boundary

#### Context

`git merge-tree --write-tree HEAD origin/main` identified the exact 10 conflicting paths (`C1`). Starting `git merge --no-commit origin/main` establishes `MERGE_HEAD` while leaving `.copilot-tracking/` untracked files intact.

#### Intent

Initiate the git merge in the worktree and confirm the unmerged index list matches the 10 expected files with no unexpected auto-merge regressions.

#### Boundaries

* Included: Running `git merge --no-commit origin/main` and inspecting `git status --short` / `git ls-files -u`.
* Excluded: Committing or modifying non-conflicting files.

#### Likely Targets

* .git/worktrees/feat-233-same-home-tensions-0825/MERGE_HEAD: Created by `git merge --no-commit origin/main`.

#### Dependencies

* None.

#### Validation Expectations

* `git diff --name-only --diff-filter=U` lists the exact 10 expected files.

#### Completion Evidence

* Active `MERGE_HEAD` pointing to `45cd2bd00a593d28208f5b99053d854ababb5484` and verified 10-file conflict list.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile `job_pack.py`, `staff_intake.py`, `projection.py`, and `test_job_pack.py`

#### Context

Research (`C6`, `C7`, `C8`, `C10`, `C12`) mapped every subtle contract requirement across `test_job_pack.py`, `test_fieldwork_variation_owner_guard.py`, `test_staff_intake_api.py`, and `test_safeguarding_detail_boundary.py`:

* In `job_pack.py`: keep `import re`; retain `NON_INSTRUCTION_NOTICE`, `INSTRUCTION_CLAIMS`, `_PLACEHOLDER_WORDS`, `_ROLE_WORDS`, `_NAME_ALLOWED`, and `ADVISORY_NOTE`; keep `named_owner`, `assert_advisory`, and `reject_instruction_claim` (raising `ValueError` for any non-`None`, non-`False`, non-`""` value on `INSTRUCTION_CLAIMS`, including integer `0`); in `escalation()`, validate `kind` and `owner = named_owner(owner_name, owner_role)`, stamp `contract_instruction=False`, `is_contract_instruction=False`, `acts_as_contract_instruction=False`, `note=ADVISORY_NOTE`, `contract_notice=NON_INSTRUCTION_NOTICE`, call `assert_advisory(out)`, and return `out`.
* In `staff_intake.py`:
  * `escalation_destination()` returns `owner`, `role`, `contact`, `configured=assigned`, `owner_assigned=assigned`, `owner_status`, `advisory_only=True`, `contract_instruction=False`, `is_contract_instruction=False`, `acts_as_contract_instruction=False`, and `note=job_pack.NON_INSTRUCTION_NOTICE`.
  * `route_escalation()` sets `out["owner"]["contact"] = contact` **only when `contact` is non-empty**, preserving exact `{"name": OWNER, "role": ROLE}` equality when explicit owner arguments are supplied without configured contact (`test_fieldwork_variation_owner_guard.py`) while populating `"contact"` when env vars are configured (`test_staff_intake_api.py`).
  * `_view_escalation(e, user)` projects an escalation record for staff intake while explicitly preserving `acts_as_contract_instruction`, `is_contract_instruction`, `contract_notice`, `raised_by_email`, and `raised_at` alongside `#1666` fields (`id`, `case_id`, `work_order_id`, `kind`, `escalation_kind`, `summary`, `owner`, `named_owner`, `owner_role`, `contract_instruction`, `note`, `routed_by`, `routed_at`) and applying `projection.hold_notes` when `user` lacks `need_to_know`.
  * `escalate()` validates `_staff_only`, dict `body`, `job_pack.reject_instruction_claim(body)`, string checks on `named_owner`/`owner_role`/`kind`/`summary` (treating explicit `"named_owner": None` or `""` when `owner_role` is supplied, or `"named_owner" in body and body["named_owner"] is None`, as an explicit missing owner rather than falling back to env defaults), `_pack(store, user, wid)`, open case and non-`Withdrawn` work order, `route_escalation(...)`, and — when `store._quality_staff()` is non-empty and the resolved `owner["name"]` matches a staff-directory member whose directory roles do not include `owner["role"]` — rejects the role mismatch with `ValueError` (preserving `Pam Lead` role enforcement in `test_fieldwork_variation_owner_guard.py` without rejecting configured/external owners in `test_staff_intake_api.py`). Inside `with _read_dependency(store, user), store._quality_operation(user, w["case_id"]) as (c, actor):`, build unified `rec` (including `id`, `case_id`, `named_owner`, `owner_role`, `escalation_kind`, `routed_by`, `routed_at`, `raised_by_email`, `raised_at`, plus all `routed` keys), append distinct copies (`dict(rec)`) to both `c.setdefault("escalations", [])` and `c.setdefault("field_escalations", [])`, emit both `field_escalation_raised` (including `acts_as_contract_instruction=False`) and `field_escalation_routed` audit records, and return the combined response dictionary containing `"escalation": _view_escalation(rec, user)` alongside `HEAD`'s top-level keys (`ok=True`, `work_order_id`, `case_id`, and projected escalation fields as expected by `HEAD` callers).
  * `view()` exposes `"escalation": escalation_destination()`, `escalation_options`, unified `boundaries` (`contract_instruction=False`, `is_contract_instruction=False`, `acts_as_contract_instruction=False`, `advisory_only=True`, `instruction_notice`, `acceptance`, `consent`), and deduplicated `escalations` (and `field_escalations` compatibility list if read by `HEAD` callers) across `c.get("escalations", [])` and `c.get("field_escalations", [])` keyed by `id` when present or fallback tuple `(work_order_id, kind or escalation_kind, routed_at or raised_at, summary)` when `id` is absent, projected via `_view_escalation(e, user)`.
* In `projection.py`: keep `c.pop("safeguarding_items", None)` in `hold_notes` and `d.pop("safeguarding_items", None)` in `redact_staff_detail`; keep safeguarding-category redaction on `d.get("hazards", [])`; in `hold_notes`, detect advisory escalation dicts via `(c.get("contract_instruction") is False or "acts_as_contract_instruction" in c) and "summary" in c and ("kind" in c or "escalation_kind" in c)`, replace non-empty `summary` with `NOTE_HELD`, and skip `k in ("note", "contract_notice")` when iterating `NOTE_KEYS`.
* In `test_job_pack.py`: retain all 5 unit test methods from `HEAD` and `origin/main`.

#### Intent

Resolve `job_pack.py`, `staff_intake.py`, `projection.py`, and `test_job_pack.py` so every `#132` and `#76` invariant from both branches holds simultaneously.

#### Boundaries

* Included: `job_pack.py`, `staff_intake.py`, `projection.py`, and `test_job_pack.py` (test removals: `none`; max new test additions: `2`, `0` needed when combined 5 methods cover all branches).
* Excluded: Rewriting `test_fieldwork_variation_owner_guard.py` or `test_staff_intake_api.py`.

#### Likely Targets

* src/core/src/zava_forward/core/job_pack.py: Conflict resolution for `#132` helpers and record keys.
* src/core/src/zava_forward/core/staff_intake.py: Conflict resolution for `#132` routing, directory check, persistence, view, and audit records.
* src/core/src/zava_forward/core/projection.py: Conflict resolution for `#76` `safeguarding_items` stripping and `#132` escalation `summary` holding.
* src/core/tests/test_job_pack.py: Conflict resolution preserving all 5 test methods.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_job_pack.py` passes in `src/core`; `test_fieldwork_variation_owner_guard.py`, `test_staff_intake_api.py`, and `test_safeguarding_detail_boundary.py` pass once `P02` resolves `src/api`.

#### Completion Evidence

* Staged `job_pack.py`, `staff_intake.py`, `projection.py`, and `test_job_pack.py` with zero conflict markers and green `test_job_pack.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Reconcile `store.py` and `src/core/README.md`

#### Context

Research (`C5`, `C9`) confirmed `store.py` has a single conflict hunk in `require_safety_clear`, where `HEAD` (`#1692`) formats `taskqueues.accountable_owner(active.get("owner"))` and `origin/main` (`#1667`) passes `[gates.BOOKING_RULES["safety"]]` as the second argument to `GateError`. `src/core/README.md` has a single prose conflict describing `field-escalate`.

#### Intent

Combine the accountable-owner safety stop message with `[gates.BOOKING_RULES["safety"]]` in `store.py`, reconcile `src/core/README.md`, and stage both files.

#### Boundaries

* Included: `src/core/src/zava_forward/core/store.py` and `src/core/README.md`.
* Excluded: Non-conflicting methods in `store.py`.

#### Likely Targets

* src/core/src/zava_forward/core/store.py: `require_safety_clear` conflict block.
* src/core/README.md: `#132` `field-escalate` bullet description.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Full `src/core` unittest discovery, `mypy`, and `ruff` pass with zero errors.

#### Completion Evidence

* All 6 `src/core` conflicted files resolved, staged (`git add`), and passing `src/core` unit/type/lint checks.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Reconcile `src/api` web, endpoint-inventory, and README conflicts

### Context

Research (`C2`-`C5`, `C11`-`C13`) confirmed 4 conflicts in `src/api`: `web/app.js`, `web/staff-intake.js`, `tests/test_role_endpoint_inventory.py`, and `src/api/README.md`. AMA Repository Instructions require loading `web-design-guidelines` and fetching its current source URL before editing web files, while preserving Fluent 2 semantics, WCAG 2.2 AA baseline counters (`sites == 9` for `aria-invalid`, `tables == 14` for `h("table", {})`), and plain-language `BLOCKED_WORDS` compliance in `staff-intake.js`.

### Intent

Load and fetch `web-design-guidelines`, resolve `app.js`, `staff-intake.js`, `test_role_endpoint_inventory.py`, and `src/api/README.md` with zero dropped functionality or accessibility regressions, and stage all 4 files.

### Boundaries

* Included: Loading `web-design-guidelines` and fetching live guidelines; editing and staging `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/staff-intake.js`, `src/api/tests/test_role_endpoint_inventory.py`, and `src/api/README.md`.
* Excluded: Unrelated visual redesigns, adding `aria-invalid` or raw `<table>` elements outside `screenTable`, or altering other role screens.

### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Render both `work.hazard_clocks` (`clock_text` + `accountable_owner`) and `(work.safeguarding_clocks || [])` in `workSummary(work)`.
* src/api/src/zava_forward/api/web/staff-intake.js: Reconcile `intakeNotInstruction`, `intakeEscalate(order, options, rerender, escalation)`, and `intakeOrder` with per-order input IDs, `Owner status` row, optional configured-owner fallback, and fail-closed `screenTable` without un-owned `BLOCKED_WORDS`.
* src/api/tests/test_role_endpoint_inventory.py: Union `POST_ENDPOINTS` (`field-escalate` + `/api/exceptions/recovery`).
* src/api/README.md: Reconcile `field-escalate` route documentation.

### Dependencies

* P01.

### Validation Expectations

* Targeted worktree-isolated `src/api` tests (`PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests /usr/bin/python3 -m unittest tests.test_fieldwork_variation_owner_guard tests.test_staff_intake_api tests.test_workbench_hazard_clock_owner tests.test_safeguarding_clock_a11y tests.test_safeguarding_detail_boundary tests.test_role_endpoint_inventory tests.test_accessibility_baseline tests.test_epic149_form_error_summary_associations tests.test_content_standard -q`) all pass.

### Completion Evidence

* `git ls-files -u` is completely empty across the repository and targeted `src/api` tests pass.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Fetch `web-design-guidelines` and reconcile `web/app.js` and `web/staff-intake.js`

#### Context

* AMA Web Development Guidance mandates loading `web-design-guidelines` and fetching its live rules before making web edits.
* In `app.js` (`C2`), `workSummary(work)` needs null-safe `(work.hazard_clocks || []).map(...)` (which prefixes `clock.clock_text` and `Accountable owner: ${clock.accountable_owner || "Building Safety lead (escalation owner)"}.`) followed immediately by `origin/main`'s `(work.safeguarding_clocks || []).map(...)` (`<p class="safeguarding-clock">`).
* In `staff-intake.js` (`C3`, `C11`, `C12`, `C13`), `StaffIntakeEscalationScreen` in `test_fieldwork_variation_owner_guard.py` mounts `staff-intake.js` in Node `vm`, clicks the `Raise a variation or concern` form (`aria-label === "Raise a variation or concern"`), checks that `named_owner` and `owner_role` inputs exist and have `required` when `owner_assigned` is not true, submits `kind`, `summary`, `named_owner`, `owner_role`, and checks that the re-rendered `screenTable("Variations and escalations raised", ...)` displays `"No - not a contract instruction"` when `acts_as_contract_instruction === false && contract_instruction === false` and `"Unknown - check with the contract manager"` otherwise. Meanwhile `#1666` adds unique per-order element IDs (`esc-${order}-kind`, `esc-${order}-summary`, `esc-${order}-owner`, `esc-${order}-role`), optional owner fields when `escalation?.owner_assigned` is `true`, and null-safe `data.escalation?.owner_status` (rendering `["Owner status", data.escalation.owner_status]` when `data.escalation?.owner_status` is present) in `screenFields`. Helper copy must avoid `test_content_standard.py` `BLOCKED_WORDS` (`cannot`, `refused`, etc.).

#### Intent

Apply Web Interface Guidelines and reconcile `app.js` and `staff-intake.js` so all Node-VM, accessibility baseline, and plain-language tests pass.

#### Boundaries

* Included: Activating `web-design-guidelines`, fetching its current rules, and resolving `app.js` and `staff-intake.js`.
* Excluded: Changing CSS or unrelated JS files.

#### Likely Targets

* src/api/src/zava_forward/api/web/app.js: `workSummary` clock paragraphs.
* src/api/src/zava_forward/api/web/staff-intake.js: `intakeNotInstruction`, `intakeEscalate`, and `intakeOrder`.

#### Dependencies

* P01.

#### Validation Expectations

* `test_workbench_hazard_clock_owner.py`, `test_safeguarding_clock_a11y.py`, `test_fieldwork_variation_owner_guard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, and `test_content_standard.py` all pass.

#### Completion Evidence

* Staged `app.js` and `staff-intake.js` passing all web, WCAG, and content-standard tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile `tests/test_role_endpoint_inventory.py` and `src/api/README.md`

#### Context

`POST_ENDPOINTS` in `src/api/tests/test_role_endpoint_inventory.py` (`C4`) needs `("/api/workorders/WO-0001/field-escalate", {})` once alongside `HEAD`'s `("/api/exceptions/recovery", {})` (`#1757`). `src/api/README.md` (`C5`) needs concise combined prose for `POST /api/workorders/{id}/field-escalate`.

#### Intent

Resolve and stage `test_role_endpoint_inventory.py` and `src/api/README.md`.

#### Boundaries

* Included: `src/api/tests/test_role_endpoint_inventory.py` (test removals: `none`; additions: `0` beyond merging both branches' endpoint entries) and `src/api/README.md`.
* Excluded: Modifying `server.py` route tables.

#### Likely Targets

* src/api/tests/test_role_endpoint_inventory.py: `POST_ENDPOINTS` list.
* src/api/README.md: `field-escalate` route documentation.

#### Dependencies

* P02-T01.

#### Validation Expectations

* `test_role_endpoint_inventory.py` passes completely against `server.py`.

#### Completion Evidence

* All 10 merge conflicts resolved and staged (`git ls-files -u` empty).

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Verify scenario manifest, run focused validation suite, and stage frozen merge candidate

### Context

Research (`C15`, `C16`) confirmed `scenario_manifest.py` tracks SHA-256 digests of 4 files (`workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, `test_workbench.py`), none of which changed on `HEAD` or `origin/main` since merge-base. Focused validation requires full worktree-isolated `src/core` and `src/api` unittest suites, `mypy`, `ruff check`, and `ruff format --check` (without running `tools/rpi-checks.py`). Repository rules require local privacy-safe `user.email` via `gh api user` and forbid `.copilot-tracking/` paths or negated closing keywords in commit messages. Staging the resolved merge files plus this task's `feat-233-merge-origin-main-*` tracking files at the end of `P03-T02` hands a clean frozen candidate to `rpi-review`, which writes `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md` before the parent loop finalizes the single local two-parent merge commit without pushing.

### Intent

Confirm manifest digest integrity, run the complete worktree-isolated Focused validation tier, configure and verify privacy-safe git identity, finalize the changes log, and stage the clean frozen merge candidate for `rpi-review`.

### Boundaries

* Included: `scenario-manifest.json` verification (and update only if a tracked digest changed), worktree-isolated `src/core` and `src/api` unit tests, `mypy`, `ruff check`, `ruff format --check`, local git config + `GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT` verification, `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md`, and task-scoped `git add` on `MERGE_HEAD`.
* Excluded: `tools/rpi-checks.py`, premature `git commit` prior to `rpi-review`, staging unrelated `.copilot-tracking/` files, and `git push`.

### Likely Targets

* docs/reference/research/retrofit-synthetic-data/scenario-manifest.json: Verified read-only unless a tracked file digest changed.
* .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md: Implementation record.
* .copilot-tracking/rpi-sessions/2026-11-15/feat-233-merge-origin-main-state.json: Updated phase state.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONPATH=src:tests /usr/bin/python3 -m unittest discover -s tests -q` in `src/core` exits `0` (including `test_scenario_manifest.py` and `test_generator_determinism_matrix.py`).
* `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests /usr/bin/python3 -m unittest discover -s tests -q` in `src/api` exits `0` (including `test_role_endpoint_inventory.py`).
* `MYPYPATH=src /home/azureuser/.local/bin/mypy src tests` in `src/core` and `MYPYPATH=src:../core/src:../agents/src /home/azureuser/.local/bin/mypy src tests` in `src/api` exit `0`.
* `/home/azureuser/.local/bin/ruff check src tests` and `/home/azureuser/.local/bin/ruff format --check src tests` in `src/core` and `src/api` exit `0`.
* `git diff --cached --check` exits `0` and conflict-marker regex scan returns `0` matches.

### Completion Evidence

* Active `MERGE_HEAD` (`45cd2bd00a593d28208f5b99053d854ababb5484`) with zero unmerged index entries, clean `git diff --cached --check`, verified noreply `GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT`, and reconciled `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md` staged and ready for `rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Verify `scenario-manifest.json` and execute worktree-isolated `src/core` + `src/api` unit tests, `mypy`, and `ruff`

#### Context

Focused validation ensures both resolved conflicts and auto-merged files (`server.py`, `governance.py`, `taskqueues.py`, `workflows.py`, `test_taskqueues.py`) integrate with zero regressions across unit tests, type annotations, and formatting/lint rules using worktree-local `PYTHONPATH` and `MYPYPATH` so shared user site-packages cannot mask local edits.

#### Intent

Verify `scenario-manifest.json` recipe SHA-256 digests and execute all required worktree-isolated Focused-tier checks across `src/core` and `src/api`.

#### Boundaries

* Included: Running `test_scenario_manifest.py`, `test_generator_determinism_matrix.py`, `test_role_endpoint_inventory.py`, full worktree-isolated `src/core` (`PYTHONPATH=src:tests`) and `src/api` (`PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests`) unittest discovery, worktree-isolated `mypy` (`MYPYPATH=src` in `src/core` and `MYPYPATH=src:../core/src:../agents/src` in `src/api`), `ruff check src tests`, `ruff format --check src tests`, `git diff --cached --check`, and conflict-marker regex verification.
* Excluded: `tools/rpi-checks.py` and mutating shared `pip install -e` installs.

#### Likely Targets

* src/core: Unit tests, `mypy`, `ruff check`, `ruff format --check`.
* src/api: Unit tests, `mypy`, `ruff check`, `ruff format --check`.

#### Dependencies

* P01, P02.

#### Validation Expectations

* Every test runner, `mypy` invocation, `ruff` check, and `git diff --cached --check` exits `0`.

#### Completion Evidence

* Recorded command exit codes and counts in `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Configure privacy-safe git identity, finalize changes record, and stage frozen merge candidate for `rpi-review`

#### Context

AMA Branch and Pull Request Workflow instructions require resolving `{id}+{login}@users.noreply.github.com` from `gh api user` and configuring `git config --local user.email` (plus `user.name` if unset), verified with `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. Keeping `MERGE_HEAD` staged at the close of `rpi-implement` (staging only resolved merge files and this task's `feat-233-merge-origin-main-*` tracking files) allows `rpi-review` to inspect the exact frozen candidate, write `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md`, and hand back to the parent RPI loop to stage the review/state files and execute the single `git commit` (`Refs #233`, zero closing keywords even negated, zero `.copilot-tracking/` strings in the commit message, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`) with no `--amend` and no `git push`.

#### Intent

Set and verify privacy-safe local git author/committer identity, reconcile `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md` and plan checklist markers, and stage the clean frozen merge candidate for `rpi-review`.

#### Boundaries

* Included: `gh api user`, `git config --local user.email` (and `user.name` if unset), `git var GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT` verification, completing `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md`, and task-scoped `git add` of resolved merge files plus `feat-233-merge-origin-main-*` `.copilot-tracking/` artifacts.
* Excluded: Premature `git commit` before `rpi-review`, staging unrelated `.copilot-tracking/` files, and `git push`.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md: Recorded implementation evidence.
* .copilot-tracking/rpi-sessions/2026-11-15/feat-233-merge-origin-main-state.json: Updated phase state.

#### Dependencies

* P03-T01.

#### Validation Expectations

* `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both show `{id}+{login}@users.noreply.github.com`; `git ls-files -u` is empty; `git diff --cached --check` exits `0`.

#### Completion Evidence

* Clean staged `MERGE_HEAD` frozen candidate and reconciled `changes`, `plan`, `details`, and `state` artifacts ready for `rpi-review` and post-review local merge commit.

#### Unresolved Items

* None.
