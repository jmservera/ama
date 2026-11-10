<!-- markdownlint-disable-file -->
# Details: Issue 134 walkthrough plan (2026-11-10)

Plan: [plan](../plans/2026-11-10-walkthrough-plan-134-1110-plan.md). Matrix and AC mapping live in the [research](../research/2026-11-10-walkthrough-plan-134-1110-research.md); this file gives the executable specifics.

## P0 preflight (exact)

1. `git status --short`, `git branch --show-current`, `git rev-parse HEAD HEAD^{tree}` recorded; Root states the main/rebase decision (none in this planning phase).
2. External venv (for example `/tmp/z134-venv`), `pip install -e` each of `src/core`, `src/agents`, `src/api`, `src/orchestrator`, `src/importer` from this worktree (Playwright/Chromium already present); `zava_forward.api` is a namespace package, so assert concrete modules instead, for example `python -c "import zava_forward.api.server as m; print(m.__file__)"` (confirm the module name at P0), and one core module, each under the worktree.
3. `flock -n /tmp/ama-rpi-heavy.lock true` succeeds (non-queued); otherwise stop.
4. Output and scratch paths at most 58 bytes (`/tmp/z134-<n>`).

## P1 rows to fill (one evidence record per row, per element)

For each row 1 to 11 in the research matrix record: command, log path, observed assertion names, and a verdict among `observed`, `partial`, `not-covered`, `deferred-no-role`. Record separately, for each screen, whether the run asserted: (a) entry reachable by keyboard, (b) evidence region reachable by Tab and labelled, (c) endpoint text exists, (d) recovery link or message exists, (e) handoff owner text, (f) status text (`#workspace-status` or `role=status`), (g) non-colour state wording. Anything not asserted by the existing check is `not-covered`, not inferred.

Run mapping:

| Check | Rows informed | AC informed |
| --- | --- | --- |
| `workbench_browser_check` | 2, 3, 5, 8 (own queue, reset, projection) and all roles' navigation | AC-034, AC-036 |
| `role_screens 226` | 1 | AC-040 |
| `role_screens 230` | 2, 3 | AC-036, AC-043 |
| `role_screens 231`, `231p` | 4 | AC-040 (rationale) |
| `role_screens 231q`, `231qp` | 9 | AC-042 |
| `role_screens 232`, `232s` | 5 | AC-035, AC-037 |
| `safety_screens_browser_check` | 6 | AC-035, AC-038 |
| `procurement_screens_browser_check` | 7, 8 | AC-039 |
| `finance_screens_browser_check` | 10 | AC-042 |
| `data_operator_browser_check` | 11 | AC-040 |
| `progress_browser_check` | 2 (context) | AC-041 (partial) |
| `home_case_browser_check` | 3 | AC-043 (context only) |

AC-041: add `python -m checks.progress_browser_check` to P1 and map its actual partial coverage (filtered progress summary, PM role); no full pass is inferred; record what denominator, as-of and filter-impact text it does not assert, then Deferred with reason or propose P2.

## P2 candidate probes (each needs Root scope admission; none authorised)

* Keyboard-only perspective walk: owned synthetic server, the eight fixture logins; for each perspective with a served screen, press Tab and Enter only from the specialist-screens link to a selected home's labelled evidence region (focusable table regions), then the Reset screen view link, then reselect a home (reset clears selection, role-screens.js lines 99 to 105); owner and handoff text is asserted as text inside the labelled region, not as a focus target; assert visible focus on each reached link or region; a negative control that a removed recovery link fails.
* Status announcement: assert the `#workspace-status` element's live-region attributes and its text transitions on screen and home selection, and the loading `role=status`, for each registered screen. This is browser DOM evidence only and is labelled so; it is not assistive-technology or screen-reader acceptance.
* AC-035 reassignment preserving the commitment and AC-037 second-measure non-inheritance, only if the constructed fixture already holds the data; otherwise record Deferred, do not extend fixtures.
* AC-041: only if the existing overview exposes denominator and filter-impact text; otherwise Deferred.
* Perspectives without login roles (1, 7, 11) are exercised only through existing manager fixtures and labelled proxy.

## P3 edits (if evidence exists)

* `src/core/src/zava_forward/core/perspective_walkthroughs.py`: evidence lists and reasons only; `ELEMENTS` and allowed statuses unchanged.
* `src/core/src/zava_forward/core/journey_acceptance.py`: reasons and evidence lists; statuses stay partial or deferred. The validator allows no pass; a pass needs a separately Root-admitted model change, not part of this plan.
* `docs/reference/research/ux/zava-forward-prototype-profile-review.md`, `docs/reference/log.md`, index if a file is added.
* Keep core tests green: `test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_scenario_manifest.py`.

## Reporting

Raw logs, matrix and the draft issue comment (criteria still unticked, `Refs #134`) go to an external folder and the PR body; use `Closes #134` only if the reviewed evidence proves every criterion, which this plan does not expect.

## Known limits recorded now

Planning-only; no check was run; matrix cells derive from registries, docstrings and selected greps; Web Interface Guidelines were fetched in full but not applied to any file; `ZF_AXE_JS` availability unknown; browser checks have no hosted CI reference found.
