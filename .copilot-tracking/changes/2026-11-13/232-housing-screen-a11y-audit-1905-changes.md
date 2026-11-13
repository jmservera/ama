---
title: Issue 232 housing screen accessibility audit changes
ms.date: 2026-11-13
---

## Outcome

Audit only: no source, test, workflow or issue change. All listed automated checks passed on 2026-11-13 at the branch head before this commit, in pip venv `/tmp/venv-232-1905` (removed before commit; editable `src/core`, `src/agents`, `src/api`, `playwright==1.64.0`, Chromium 1248 from the existing Playwright cache). The #232 criterion is not ticked here: automated synthetic evidence does not establish WCAG 2.2 conformance or assistive-technology acceptance, and only the issue owner can tick it.

Environment from `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests`, `ZF_BROWSER_TESTS=1`, `ZF_AXE_JS=/tmp/axepk/package/axe.min.js` (SHA-256 `880970c0...8a68bb`, matches the pinned axe-core 4.10.3 hash in the check; the check itself asserts it).

## Results

Exit statuses of the three browser checks were observed in the session shell (the raw logs hold PASS lines, not exit codes); the unit log records `exit 0`.

| Check | Command | Result |
| --- | --- | --- |
| Unit and static | `python -m unittest test_accessibility_baseline test_role_screens test_role_screens_conformance test_specialist_keyboard_check test_resident_choice_screen test_resident_service_screen -v` | 54 tests OK, 0 skipped |
| Role screen 232 (resident choice, pause, update commitment) | `flock -w 600 /tmp/ama-rpi-heavy.lock python -m checks.role_screens_browser_check 232` | exit 0, 42 PASS, 0 FAIL, 0 SKIP |
| Role screen 232s (service issue, contact needs, safe route) | same with `232s` | exit 0, 41 PASS, 0 FAIL, 0 SKIP |
| Specialist keyboard walk | `python -m checks.specialist_keyboard_browser_check` | exit 0, 805 PASS lines, 15 negative mutations rejected, 22 declared no-table gaps |

## Automated evidence by criterion element

* Keyboard navigation: `232` Tab reaches all three table regions (Measure choices by version, Measures paused or withdrawn, Service requests and contact needs); `232s` reaches Service issues and contact needs; native keyboard focus is visible; the specialist walk (Tab, Shift+Tab, Enter) reaches the Specialist screens entry, screens, evidence regions, handoff and Reset links with measured focus visibility and `#workspace-status` role=status, aria-live=polite, aria-atomic=true.
* Textual state meaning: both stories pass "choice, issue and commitment state is stated in text" (paused or withdrawn by the resident, linked update commitment, state and meaning), no write controls in the reader view and no contact links or actions.
* axe-core 4.10.3 on `main`: `232` and `232s` each report no violations and an empty incomplete list.
* Static WCAG 2.2 baseline tests pass (language, zoom, text and non-text contrast, two-tone focus, 24px targets, status regions, table captions and headers, no drag-only interaction).

## Coverage limits

* axe scanned `main` of two synthetic scenarios at the checked viewport only; it is not a full-page, all-state or all-width scan.
* In the specialist keyboard walk, `resident-service-issues` for all four roles that serve it (Resident Liaison Officer, Programme Support Officer, Retrofit Coordinator, Retrofit Programme Manager) is a declared no-evidence-table gap on that fixture, not a table-navigation pass. Table keyboard reach for that screen rests on story `232s`.
* The data is constructed synthetic data; role selection is not authentication, resident or human acceptance.

## Honest residual (not evidenced)

* No screen reader (NVDA, JAWS, VoiceOver, TalkBack) output, voice control, switch access or magnification/reflow testing by people; DOM status text is not assistive-technology output.
* No review of resident-facing wording comprehension or human accessibility validation; validation belongs to #155.
* Chromium only; no cross-browser run.
* WCAG 2.2 conformance is not claimed; automated tools cover only part of the criteria.

## Review and gates

Tier: Focused (documentation-only tracking record plus local checks). Hosted CI for the exact head is not observed here and the branch is not pushed.
