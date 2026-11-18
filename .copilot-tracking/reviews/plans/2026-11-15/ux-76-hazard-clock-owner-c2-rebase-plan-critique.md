<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #76 C2 Rebase Continuation onto `#1641` (`36aeddae3`)

## Metadata

* Task ID: issue-76-c2-rebase
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  1. Write `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md`.
  2. Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) and rebase the `#76` branch in `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` (`feat/ux-76-hazard-clock-owner` for `PR #1768`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`, stashing and restoring the untracked `2026-11-15` `c2-rebase` tracking files across the rebase and preserving BOTH `#116` (`PR #1766`) and `#215` (`PR #1773`) changes on `#1641` AND `#76` (`PR #1768` hazard/safeguarding clock and named owner + SQL Server row-order invariant fix `8f8d85342`).
  3. Write `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md` and `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`.
  4. Run focused validation (`unittest discover -s tests -p "test_*case_workbench*.py" -q && ruff check . && ruff format --check . && mypy` in both `src/core` and `src/api`) plus real `#76`, `#116`, and `#215` unit suites.
  5. Commit all changes and `.copilot-tracking/` artifacts (`git status --short` clean) with `Refs #76` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without `git push`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-research.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md, .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md, .copilot-tracking/rpi-sessions/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-state.json, .github/copilot-instructions.md, and read-only `git merge-tree` inspection of `36aeddae345426fdf8ee53565fef1540979de967` vs `6e9eb39de..941806d9d`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1`, `FR-2`, `FR-3`, `NFR-1`, `NFR-2`, `AC-1` through `AC-4`, research findings `C1` through `C8`, focused-tier validation policy, privacy-safe noreply Git identity, Copilot trailer, and no-push rule.
* Assessment boundary: Evaluates target commit ancestry, rebase stash/restore hygiene, 3-way conflict boundaries across `#116` (`243764945`), `#215` (`36aeddae3`), and `#76` (`6e9eb39de`, `8f8d85342`, `941806d9d`), raw safeguarding cross-feature visibility (`#116` + `#76`), validation selector coverage, and caller-specified artifact output paths without mutating plan sources during critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1 / C1, C2 / P01-T01 (Rebase onto latest `#1641` tip and stash/restore tracking files) | Partial | `git merge-tree --write-tree 36aeddae3 941806d9d` confirms the conflict set against `36aeddae3` is identical to `243764945` (strictly `projection.py` 1 hunk and `store.py` 6 hunks in Commit 1 `6e9eb39de`, with `8f8d85342` SQL Server row-order fix and `941806d9d` replaying cleanly and `#215`'s `chat_case_answers.py` + 13 API test files untouched), but `plan.md` and `phase-details.md` still pin the earlier `#1641` tip `243764945ea8f5b292eed0b73ea034b91c3b6e5f` and omit explicit `git stash push -u` / `git stash pop` of untracked `2026-11-15` `c2-rebase` tracking files across the rebase (`PC-001`). |
| FR-2, AC-1 / C4, C5 / P01-T01 (`store.py` lossless merge) | Covered | AST comparison confirms zero semantic function overlap in `src/core/src/zava_forward/core/store.py`; resolving the 6 `ruff format`-wrapped safety hunks preserves both `#116` AI/document store methods and `#76` safety clock/owner methods. |
| FR-3, AC-2 / C3, C6, C7 / P01-T02 (`projection.py` unified `#116` + `#76` raw safeguarding visibility) | Covered | Container-aware holding on `safeguarding_items` and `safeguarding` (matching `SAFEGUARDING_ITEM_KEYS` without mutating passive note-only `{"note": "..."}` canaries or `documents[*]["summary"]`) plus high-sensitivity safety `summary` path classification in `_is_high_sensitivity_path` and 1 regression test in `test_hazard_safeguarding_clock_owner_76.py` cleanly closes the cross-feature seam. |
| NFR-1, AC-3 / C8 / P02-T01 (Focused validation + targeted suites) | Partial | Runs both literal caller step-4 commands (`-p "test_*case_workbench*.py"` + `ruff` + `mypy`) and `#76` + `#116` suites, and should also include `#215` alert owner/clock API test verification (`test_alert_chat_owner_clock_safe_action_215.py`) now that `#215` (`PR #1773`) is in upstream `36aeddae3` (`PC-001`). |
| NFR-2, AC-4 / P02-T02 (Artifact paths and clean local `Refs #76` commit closeout) | Partial | Privacy-safe `user.email`, `Refs #76`, Copilot trailer, clean `git status --short`, and no-push boundary are sound, but `P02-T02` in `phase-details.md` names `.copilot-tracking/reviews/logs/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` whereas caller Required Step 3 explicitly specifies `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: Conflict analysis (`projection.py` + `store.py`), SQL Server row-order invariant preservation (`8f8d85342`), and the `#116` + `#76` raw safeguarding visibility fix (`P01-T02`) are accurate and verified, including against upstream commit `36aeddae3` (`PR #1773` / `#215`). Two direct planner corrections are required before implementation: advancing the pinned `#1641` target SHA from `243764945` to `36aeddae345426fdf8ee53565fef1540979de967` with explicit untracked-file stash/restore across rebase and `#215` alert-owner/clock suite verification (`PC-001`), and aligning the review artifact path to caller Required Step 3's `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` (`PC-002`). Neither requires user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Target `#1641` parent SHA in `plan.md` and `phase-details.md` predates `PR #1773` (`36aeddae3`, `#215`) and omits explicit stash/restore of untracked `c2-rebase` artifacts across rebase

* Related IDs: FR-1, NFR-1, NFR-2, AC-1, AC-3, P01, P01-T01, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md, .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md
* Concern: Between the initial `c2-rebase` draft and execution, `origin/feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) advanced by one commit from `243764945ea8f5b292eed0b73ea034b91c3b6e5f` (`PR #1766`, `#116`) to `36aeddae345426fdf8ee53565fef1540979de967` (`PR #1773`, `#215` regulatory alerts, home chat, and visit consent boundary suites). `P01-T01` instructs implementation to check `243764945...` and pause if the remote tip changed, omits stashing/restoring the untracked `2026-11-15` `c2-rebase` tracking files across `git rebase`, and omits running `#215` alert owner/clock tests (`test_alert_chat_owner_clock_safe_action_215.py` / `test_alert_chat_visit_consent_boundary_215.py`) in `P02-T01`.
* Impact: Executing `P01-T01` verbatim against `243764945...` would trigger a false-positive SHA mismatch pause instead of rebasing onto `36aeddae345426fdf8ee53565fef1540979de967` as explicitly requested by the caller, and would leave `#215` preservation and alert-owner/clock cross-feature compatibility unverified in `P02-T01`.
* Smallest useful change: Update `plan.md` and `phase-details.md` to pin `36aeddae345426fdf8ee53565fef1540979de967` (`PR #1772` `#154` + `PR #1766` `#116` + `PR #1773` `#215`), stash (`git stash push -u`) and restore (`git stash pop`) the untracked `2026-11-15` `c2-rebase` tracking files across `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, explicitly preserve `#116`, `#215`, and `#76` (including `8f8d85342` SQL Server row-order invariant fix), and add `#215` API alert/chat boundary test modules (`test_alert_chat_owner_clock_safe_action_215.py`, `test_alert_chat_visit_consent_boundary_215.py`) to `P02-T01`.
* Action owner: planning_parent
* Exact resolving evidence: Updated .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md and .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md reference `36aeddae345426fdf8ee53565fef1540979de967`, stash/restore untracked `c2-rebase` files in `P01-T01`, and verify `#215` suites alongside `#76` + `#116` in `P02-T01`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P02-T02` review output path in `phase-details.md` differs from caller Required Step 3 path

* Related IDs: AC-4, P02-T02
* Evidence: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md
* Concern: `P02-T02` in `phase-details.md` writes `.copilot-tracking/reviews/logs/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`, whereas caller Required Step 3 explicitly instructs writing `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`.
* Impact: Writing only under `reviews/logs/2026-11-15/` would miss the exact file path specified in Required Step 3.
* Smallest useful change: Update `P02-T02` in `phase-details.md` (and `artifact_paths.review` in `ux-76-hazard-clock-owner-c2-rebase-state.json` during `Review`) to use the caller-specified path `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`, and keep `.copilot-tracking/` path strings out of the commit message body per `rpi-implement` production-reference hygiene.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T02` in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md specifies `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Identical 2-file rebase conflict footprint verified against `36aeddae3`: `git merge-tree --write-tree 36aeddae3 941806d9d` confirms `PR #1773` (`#215`) adds zero new conflicts beyond `projection.py` (1 hunk) and `store.py` (6 `ruff format` hunks) in Commit 1 (`6e9eb39de`), while Commit 2 (`8f8d85342` SQL Server row-order invariant fix) and Commit 3 (`941806d9d`) replay conflict-free.
* Cross-feature `#116` + `#76` visibility hardening (`P01-T02`): Extending `projection.hold_notes` and `_is_high_sensitivity_path` to raw standalone safeguarding dicts (`SAFEGUARDING_ITEM_KEYS`) ensures `#116`'s raw-case `project_case_visibility` and `withheld_scope_values` withhold private safeguarding text for non-reason staff roles without disturbing passive note-only `{"note": "..."}` canaries or `documents[*]["summary"]`.
* Accepted residual risk: Live SQL Server container parity (`ZF_TEST_MSSQL=1`) runs in hosted GitHub Actions CI after owner/coordinator-authorized push (`Do NOT git push` honored locally).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique performed strictly read-only against supplied `.copilot-tracking/` artifacts and Git commit objects (`08c36e4dc`, `243764945`, `36aeddae3`, `6e9eb39de`, `8f8d85342`, `941806d9d`) without modifying plan sources or running mutating Git commands.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply `PC-001` and `PC-002` directly to .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md and .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md, finalize planning status, and transition directly to `rpi-implement` (`P01-T01`) without repeating critique.
* User response required: No
