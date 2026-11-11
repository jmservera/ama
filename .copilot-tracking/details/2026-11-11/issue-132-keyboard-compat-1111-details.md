---
title: Issue 132 keyboard probe compatibility details
description: Phase details, exact edits and test proposal for the staff-job-pack-intake keyboard probe declaration (issue 132 follow-up)
ms.date: 2026-11-11
---

## Preconditions (checked at E4 admission, not now)

* Root supplies the exact private `HOME`, task-private interpreter and test-helper origins, and states E4 is admitted with a concrete safe delta.
* Worktree clean at the planning-candidate head; `origin/main` fetched and compared to the base.
* No private data, `.env` or default `ZF_DATA`. Install only a package whose absence fails a command; do not install the five projects blindly.

## Phase 1: failing regression

File: `src/api/tests/test_specialist_keyboard_check.py` (existing). Add `import re` and `from pathlib import Path`, import `EXPECTED_REGIONS` beside `NO_REGION_GAPS`, and add to `SpecialistKeyboardCheckHelpers`:

```python
    def test_staff_intake_screen_is_declared_and_unknown_screens_still_fail(self) -> None:
        self.assertEqual(region_failures("staff-job-pack-intake", []), [])
        self.assertTrue(region_failures("staff-job-pack-intake", [REGION]))
        self.assertTrue(region_failures("unlisted-screen", []))
        web = Path(__file__).parents[1] / "src/zava_forward/api/web"
        registered: set[str] = set()
        calls = 0
        for script in web.glob("*.js"):
            source = script.read_text()
            calls += len(re.findall(r"(?<!function )registerRoleScreen\(", source))
            registered |= set(re.findall(r'registerRoleScreen\(\{\s*id:\s*"([A-Za-z0-9_-]+)"', source))
        self.assertIn("staff-job-pack-intake", registered)
        self.assertEqual(len(registered), calls)
        self.assertEqual(registered - set(EXPECTED_REGIONS) - set(NO_REGION_GAPS), set())
```

The call count is compared with the number of ids parsed, so a registration in an unsupported form (single quotes, another property order, a loop) fails the test instead of escaping the guard. Expected on base: fails at the first assertion (undeclared-screen message) and would also fail the registration-drift assertion with `{'staff-job-pack-intake'}`. The `registered` guard reads only checked-in source, needs no browser, and fails closed for any future registered screen nobody declared. Line wrapping to the repository's ruff line length is the implementer's job.

Command, from `src/api`, after confirming the interpreter: `python -m unittest tests.test_specialist_keyboard_check -q` (or the form the existing workflow uses; the README guidance shows `python3 -m unittest discover -s tests -q`, narrowed here to the one module).

## Phase 2: repair

File: `src/api/checks/specialist_keyboard_browser_check.py`, `NO_REGION_GAPS` tuple (currently lines 56-62). Add one entry:

```python
        "finance-funding",
        "staff-job-pack-intake",
```

Keep the existing reason text: "fixture renders no evidence table for the selected home" is accurate (no work order issued). Do not touch `region_failures`, `EXPECTED_REGIONS`, `walk_screen`, `negative_controls`, imports or signatures. Do not add a skip, a wildcard or a prefix match.

Re-run the same unit module: all tests green, including the unknown-screen assertion.

## Phase 3: static and affected browser

* Static, on the two changed files only: `ruff check`, `ruff format --check` and `mypy` with the repository's pinned configuration for `src/api`. Use the project's existing commands; do not invent new tooling.
* Browser, E4 only, free lock, from `src/api`: `python -m checks.specialist_keyboard_browser_check` with a short `ZF_BROWSER_SCRATCH`, the existing pinned Chromium, and no network provider. Expected observations: for each of the seven roles an `OBS` line with `screen: 'staff-job-pack-intake'`, `regions: []`, `no_region_gap` set, handoff and reset keys present, and a PASS for "evidence regions match the declared fixture". The probe observes only that no evidence table rendered. It does not observe the empty-order text, and a per-order load error would also render no table, so the cause (no work orders) stays a source-derived statement and is not claimed as browser-confirmed. The README text says about 714 PASS lines; the new count is a consequence of seven extra walks and is not an acceptance figure.
* Outcomes: any table appears, any role fails a walk step, or the server returns an error from `/api/workorders`: stop, record the blocker and re-plan. Do not widen the gap or relax the predicate.

## Phase 4: evidence

Record the changes file, the before and after unit output, the browser observations for each of the seven roles, and the unchanged extension balance. One Review after implementation, per the RPI protocol. State what did not run.

## Not in scope

README edit unless root approves the conditional one-word change, new fixture or work-order seeding, product code, role or approval changes, `connected_home_browser_check.py`, changes to helper signatures, full suites, SQL, images, cloud.
