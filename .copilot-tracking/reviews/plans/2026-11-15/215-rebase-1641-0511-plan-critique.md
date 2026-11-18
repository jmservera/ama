<!-- markdownlint-disable-file -->
# RPI Plan Critique: Rebase #215 regulatory alerts and home chat suites onto PR #1641

## Metadata

* Task ID: 215-rebase-1641-0511
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  1. Rebase unmerged `#215` regulatory alerts and home chat WCAG 2.2 AA, role matrix, consent-boundary, and provenance commits (`a3a9030be..d273b99d6`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`, PR #1641), skipping commits already merged upstream (`a3a9030be..680ca9a87` squash-merged as `c42fceed7`, #1576).
  2. Run the 8 `#215` test suites in `src/api/tests`: `test_regulatory_a11y_cues.py`, `test_alert_chat_role_wcag_plain_matrix.py`, `test_alert_chat_end_to_end_stabilization_215.py`, `test_alert_chat_provenance_audit_contract_215.py`, `test_alert_chat_unblock_visit_grounding_215.py`, `test_alert_chat_visit_consent_boundary_215.py`, `test_alert_chat_doubt_held_parity_215.py`, and `test_alert_chat_owner_clock_safe_action_215.py`.
  3. Run `ruff check src/api/tests` and `mypy` inside `src/api`.
  4. Commit updated `.copilot-tracking/` rebase review artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave a clean frozen worktree (`git status --short` empty), and do not push.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/215-rebase-1641-0511-research.md, .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md, .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md, .github/copilot-instructions.md
* Decisions, dependencies, and acceptance criteria considered: `git rebase --onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87` to skip the 10 squash-merged `#1576` commits and replay the 12 unmerged commits (`799909e72..d273b99d6`); preservation of PR #1641 `RULES_FIRST` routing, `workflow/*` citations, `SOURCE_LABELS`, and `chat.js` accessibility/provenance contracts without editing `chat.js` or `style.css`; focused validation tier under `.github/copilot-instructions.md`; privacy-safe `{id}+{login}@users.noreply.github.com` repository-local git identity; Copilot `Co-authored-by` trailer; no `git push`; runtime prohibition on writing to `/tmp` or external temporary directories.
* Assessment boundary: Evaluates plan completeness, execution feasibility, contract-preservation soundness, validation lock coverage, and git/environment hygiene solely from the supplied artifacts and repository/runtime rules without running mutating commands or inspecting source files outside the supplied artifacts.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / C1-C3 / P01-T01 (Rebase `680ca9a87..d273b99d6` onto `d8cb35d25`) | Partial | Commit-range math (`10` squash-merged in `c42fceed7` + `12` unmerged in `680ca9a87..d273b99d6` = `22` commits from `0578458d4`) and privacy-safe `git config --local user.email` are sound, but `P01-T01` hardcodes replacement phrasing for `RULES[VISIT_CONSENT]` without checking verbatim substring assertions on `d8cb35d25` (`PC-002`). |
| Research Contrarian Wave / NFR / P01-T02 (Editable package isolation) | Partial | Correctly avoids mutating shared `~/.local` editable links, but hardcodes `/tmp/venv-215-0600` (prohibited by the runtime no-`/tmp` rule) and relies on `venv --system-site-packages`, which disables `~/.local` user site-packages where third-party runtime/type packages may reside (`PC-001`). |
| Caller Req 2 / C4, C6, C7 / P02-T01 (8 named `#215` suites + contract reconciliation) | Covered | All 11 unmerged `#215` test modules and all 8 caller-named suite filenames (including the 2 thin alias modules `test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py`) are mapped cleanly to `d8cb35d25` contracts while retaining non-`RULES_FIRST` coverage for `generative-grounded`, `decision-rules-fallback`, and `withheld`. |
| Caller Req 3 / NFR / P02-T02 (`ruff check src/api/tests` and `mypy` inside `src/api`) | Partial | Both required commands and sibling `#164`/`#215` regression suites are locked, subject to fixing the workspace-local virtualenv path and `~/.local` package visibility (`PC-001`). |
| Caller Req 4 / P03, P03-T01 (Commit `.copilot-tracking/` artifacts with trailer, clean frozen worktree, no push) | Partial | Trailer, privacy-safe email, empty `git status --short`, and no-push boundary are explicit, but `P03-T01` runs `rpi-review` before committing reconciled `src/` changes and cleans up the temporary venv after commit rather than before review/staging (`PC-001`, `PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: The rebase ancestry (`--onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87`), `#164`/`#215` contract reconciliation strategy, and 8-suite + `ruff` + `mypy` validation scope are well-grounded, but three planner-direct execution adjustments are needed before implementation: replacing the prohibited `/tmp` virtualenv path and accounting for `venv` disabling `~/.local` user site-packages (`PC-001`), preserving `d8cb35d25`'s exact tested phrases in `RULES[VISIT_CONSENT]` during conflict resolution (`PC-002`), and cleaning the scratch venv / committing reconciled `src/` edits before `rpi-review` (`PC-003`). None requires user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Temporary virtualenv path uses prohibited `/tmp` directory and `venv --system-site-packages` excludes `~/.local` dependencies

* Related IDs: Non-Functional Requirements, Test Ownership and Validation Lock, Dependencies, Research Contrarian Wave, P01, P01-T02, P02-T02, P03, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md, .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md, .copilot-tracking/research/2026-11-15/215-rebase-1641-0511-research.md
* Concern: First, the plan and phase details mandate creating and running `/tmp/venv-215-0600`, which directly conflicts with the runtime constraint prohibiting any writes to `/tmp` or `/var/tmp` and requiring scratch files inside the project directory. Second, `P01-T02` creates the virtualenv with `python3 -m venv --system-site-packages` and installs `src/{core,agents,api}` using `--no-build-isolation --no-deps`; standard Python `venv` sets `ENABLE_USER_SITE = False` even with `--system-site-packages`, hiding `~/.local/lib/pythonX.Y/site-packages` where user-installed build backends, runtime dependencies (`fastapi`, `pydantic`, `httpx`), or `mypy` packages may live alongside `/home/azureuser/.local/bin/mypy`.
* Impact: Implementing `P01-T02` and `P02-T02` as written either violates the `/tmp` write prohibition / sandbox policy or fails with missing build/runtime modules during `pip install --no-build-isolation --no-deps`, `unittest`, or `mypy`; conversely, switching ad hoc to an in-worktree venv without updating cleanup timing risks staging venv files or leaving plan-vs-implementation drift.
* Smallest useful change: Replace `/tmp/venv-215-0600` across the plan and phase details with a workspace-relative scratch virtualenv (for example `.venv-215-0600`), specify adding a tail fallback `.pth` file (for example `zzz_user_site_fallback.pth` pointing to `~/.local/lib/pythonX.Y/site-packages`) inside `.venv-215-0600`'s `site-packages` if third-party dependencies reside in `~/.local` so local editable `src/{core,agents,api}` resolve ahead of stale `~/.local` `zava_forward` links without mutating `~/.local`, and delete `.venv-215-0600` immediately after `P02-T02` validation passes (before `P03-T01` review and staging).
* Action owner: Planning parent
* Exact resolving evidence: Updated .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md and .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md contain zero `/tmp/` references, lock `.venv-215-0600` with verified local `zava_forward.*` + third-party dependency imports in `P01-T02`, and delete `.venv-215-0600` at the end of `P02-T02` before `P03-T01`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `P01-T01` hardcodes `RULES[VISIT_CONSENT]` wording without guarding verbatim phrases asserted by `d8cb35d25` tests

* Related IDs: Functional Requirements, C5, P01-T01, P02-T02
* Evidence: .copilot-tracking/research/2026-11-15/215-rebase-1641-0511-research.md, .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md
* Concern: Research `C5` paraphrases `d8cb35d25`'s `RULES[VISIT_CONSENT]` rather than quoting its exact text or the exact assertions in `src/core/tests/test_chat_case_answers.py` and `src/api/tests/test_chat_panel.py`. `P01-T01` prescribes `"confirm the resident's consent and access"`, replacing the contiguous phrase `"resident consent"` in the confirmation clause if upstream PR #1641 tests assert exact substrings on `RULES[VISIT_CONSENT]`.
* Impact: If `test_chat_case_answers.py` or `test_chat_panel.py` on `d8cb35d25` checks a verbatim substring of PR #1641's `RULES[VISIT_CONSENT]`, baking an unverified rewrite into rebased commit `83957d33e` during `P01-T01` causes avoidable regression failures in `P02-T02`.
* Smallest useful change: Clarify `P01-T01` in .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md to inspect `d8cb35d25`'s verbatim `RULES[VISIT_CONSENT]` and `src/core/tests/test_chat_case_answers.py` during conflict resolution and extend `d8cb35d25`'s existing text minimally (preserving tested substrings such as `"resident consent"` and `"case consent control"` while adding explicit resident consent-and-access confirmation before a non-emergency visit and excluding `UnblockTests.BANNED` terms).
* Action owner: Planning parent
* Exact resolving evidence: `P01-T01` in .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md requires inspecting `d8cb35d25`'s verbatim `RULES[VISIT_CONSENT]` and `test_chat_case_answers.py` and preserving tested upstream phrases when adding `"and access"` confirmation wording.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: `P03-T01` orders `rpi-review` before committing reconciled `src/` changes, preventing `review.md` from citing an immutable implementation commit SHA

* Related IDs: Caller Req 4, Functional Requirements, P02-T02, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md, .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md, .github/copilot-instructions.md
* Concern: `P03-T01` runs `rpi-review` and writes `.copilot-tracking/reviews/logs/2026-11-15/215-rebase-1641-0511-review.md` before staging and committing the reconciled test modules alongside `.copilot-tracking/` artifacts, yet lists "Final commit SHA" under `P03-T01` completion evidence. A single post-review commit cannot record its own SHA inside `review.md`, and running `rpi-review` against uncommitted `src/` edits reduces audit traceability.
* Impact: `215-rebase-1641-0511-review.md` cannot reference the committed SHA of the reconciled `#215` code/tests unless `src/` reconciliation is committed at the end of `P02-T02` and `.copilot-tracking/` review/tracking artifacts are committed in `P03-T01`.
* Smallest useful change: Update `P02-T02` and `P03-T01` so `P02-T02` removes `.venv-215-0600` and commits the validated `src/` test reconciliation and alias modules locally (with privacy-safe git identity and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), and `P03-T01` runs `rpi-review` against that committed `HEAD` and commits the finalized `2026-11-15` `.copilot-tracking/` artifacts with the same trailer, leaving `git status --short` empty without pushing.
* Action owner: Planning parent
* Exact resolving evidence: Updated `P02-T02` and `P03-T01` in .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md and .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md separate the validated `src/` reconciliation commit before `rpi-review` from the final `.copilot-tracking/` review/state commit after `rpi-review`, both carrying the Copilot trailer with no `git push`.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Commit-ancestry scoping (`--onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87`) cleanly skips the 10 squash-merged `#1576` commits (`a3a9030be..680ca9a87` == `c42fceed7`) while preserving all 12 unmerged `#215` commits (`799909e72..d273b99d6`).
* Contract reconciliation preserves every `#215` behavioral guarantee rather than dropping assertions: `unblock`/visit prompts verify PR #1641's stronger `RULES_FIRST` deterministic path (`decision-rules`, `workflow/*` + `ZF-4/*` citations, zero model calls, zero record mutation), while non-`RULES_FIRST` prompts (`"review what is blocking it"`, `"Please summarise this case"`) retain full coverage of `generative-grounded`, `decision-rules-fallback`, and `withheld` (including consent-assumption withholding).
* Thin alias modules (`test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py`) satisfy the caller's exact 8-suite test selector without renaming or deleting `test_epic215_*` modules; residual risk that full `unittest discover` runs those stateless unit tests under both module names is low and consistent with existing `src/api/tests/test_alert_chat_keyboard_provenance.py`.
* Non-goals appropriately exclude live browser/screen-reader and staff comprehension sign-off and leave `chat.js` and `style.css` untouched at `d8cb35d25`.

## Questions or Blocking Evidence Gaps

* None. All three findings are planner-direct adjustments resolvable without user input or additional research.

## Limitations

* This critique assessed only the supplied `.copilot-tracking/` research, plan, phase-details artifacts, caller requirements, and `.github/copilot-instructions.md` without executing git, test, linter, or source-inspection commands outside the supplied inputs.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Revise .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md and .copilot-tracking/details/2026-11-15/215-rebase-1641-0511-phase-details.md directly to address `PC-001`, `PC-002`, and `PC-003`, then finalize the plan and proceed to `rpi-implement` without another critique pass.
* User response required: No
