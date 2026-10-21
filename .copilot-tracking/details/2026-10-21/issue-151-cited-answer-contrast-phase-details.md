<!-- markdownlint-disable-file -->
# RPI Phase Details: issue-151-cited-answer-contrast

## Metadata

* Task ID: issue-151-cited-answer-contrast; plan: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md
* Research: .copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md
* Test ownership: add one unit test method; remove none; max additions: one unit test, one browser helper and three scan states; canonical target style.css (no generated copy); semantic coverage is the axe mid-fade scan, the unit test is a regression guard on the cause.

## Phase Index

* P01 regression first; P02 fix; P03 reuse, docs, validation.

## P01: Regression first

### Context

Cause is the `button` background fade with instant text colour (research C2, C3). The check scan runs immediately after render (C5).

### Intent

Encode the cause in a unit guard and the symptom in a browser state, and prove both fail on current CSS.

### Boundaries

No axe changes; scan selector and rule tags unchanged; helper restores animations after each scan.

### Likely Targets

src/api/tests/test_regulatory_ux_check.py; src/api/checks/regulatory_ux_check.py (new helper called after the cited-answer scan).

### Dependencies

None.

### Validation Expectations

Unit test fails and the browser check fails with `color-contrast` on the submit button while the CSS is unfixed.

### Completion Evidence

Recorded failing output in the changes record.

### Unresolved Items

None.

### P01-T01: Unit regression

#### Context

style.css has a single `transition` rule for `button,.btn,.item,.tile`.

#### Intent

Parse style.css (path resolved from the test file location to `../src/zava_forward/api/web/style.css`); for every rule whose selector list includes `button` or `.btn`, assert `transition` and `transition-property` declarations contain none of `background-color`, `background`, `all`. Assert the parser found the border-color rule (non-empty match) so an empty parse fails.

#### Boundaries

Parse CSS text with a simple regex on rule blocks; no new dependency.

#### Likely Targets

src/api/tests/test_regulatory_ux_check.py.

#### Dependencies

None.

#### Validation Expectations

Fails on current CSS, passes after P02.

#### Completion Evidence

Test output.

#### Unresolved Items

None.

### P01-T02: Mid-fade browser state

#### Context

Only a paused in-flight transition reproduces the state deterministically (research C7).

#### Intent

Helper toggles the submit button disabled then enabled, waits two animation frames, pauses its animations at 35 and 50 percent, asserts computed background equals the brand colour rgb(11, 93, 107) and records the animated properties, runs the unchanged `scan`, then cancels the animations, restores disabled state and focus (the question field). Scope: submit button only.

#### Boundaries

Uses the real button and real `scan`; does not wait for transitions to finish; no axe rule changes; later keyboard states unaffected (full check must pass).

#### Likely Targets

src/api/checks/regulatory_ux_check.py near line 309.

#### Dependencies

P01-T01 not required.

#### Validation Expectations

Check fails on unfixed CSS with `color-contrast`; passes on fixed CSS.

#### Completion Evidence

Failing then passing run output.

#### Unresolved Items

None.

## P02: Fix

### Context

Research selected removing the background fade.

### Intent

Make the base transition rule explicit about what animates.

### Boundaries

Keep `--motion`, reduced-motion, `.item` and `.tile` border transitions and the border-color transition for buttons.

### Likely Targets

src/api/src/zava_forward/api/web/style.css line 191.

### Dependencies

P01.

### Validation Expectations

AC-2.

### Completion Evidence

Passing runs.

### Unresolved Items

None.

### P02-T01: CSS edit

#### Context

`button,.btn,.item,.tile{transition:background-color ...,border-color ...}`.

#### Intent

Split into `.item,.tile` (unchanged) and `button,.btn` (border-color only).

#### Boundaries

No token changes.

#### Likely Targets

style.css.

#### Dependencies

P01.

#### Validation Expectations

Unit and browser checks pass.

#### Completion Evidence

Diff and test output.

#### Unresolved Items

None.

## P03: Dependency reuse, docs and validation

### Context

Shared lockfiles must carry certifi 2026.10.19 (GHSA-6q48-6c7w-9gw2).

### Intent

Reuse exactly the named commit's four requirements files and validate.

### Boundaries

Only the four files; no tracking copied from that commit.

### Likely Targets

src/{api,core,importer,orchestrator}/requirements.txt; src/api/README.md.

### Dependencies

P02 for validation.

### Validation Expectations

AC-3, AC-2, ruff, mypy, format check, related unit modules, web-design-guidelines refresh and review.

### Completion Evidence

Command log in the changes record.

### Unresolved Items

None.

### P03-T01: Requirements files

#### Context

Current pins certifi 2026.7.22.

#### Intent

`git checkout a3257c71... -- <four files>`; verify a diff touches only certifi hash blocks.

#### Boundaries

No other pin.

#### Likely Targets

The four files.

#### Dependencies

None.

#### Validation Expectations

`git diff base -- file` limited to certifi lines.

#### Completion Evidence

Diff stat.

#### Unresolved Items

None.

### P03-T02: README and validation

#### Context

README lines about axe states.

#### Intent

Add one sentence describing the mid-fade state scan; run validation.

#### Boundaries

Do not claim conformance.

#### Likely Targets

src/api/README.md.

#### Dependencies

P02.

#### Validation Expectations

As above.

#### Completion Evidence

Results.

#### Unresolved Items

None.
