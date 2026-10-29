<!-- markdownlint-disable-file -->
# RPI Phase Details: Compact case view

Task ID: 552. Task slug: case-view-ux-552. Date: 2026-10-29.
Plan: .copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md.
Research: .copilot-tracking/research/2026-10-29/case-view-ux-552-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Local execution complete; Review Partial / Residual work | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Compact case UI

Context: six-step native workspace currently puts full blocker reasons inside
step links and isolates horizontally scrolling tabs above unbounded panels.
Boundaries: web-only presentation; backend rules and independent safety stay.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Capture baseline and reuse deck icons

Use the existing synthetic server harness and same constructed long/multiple
blocker fixture for pre/post metrics. Record all step heights at desktop and
narrow widths and screenshots externally. Extract image11, image6, image12,
image13, image14, image15 from slide 4 into web journey icon files; record
SHA-256 provenance, source deck and step mapping. No icon redraw or dependency.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Compact blockers and attach tabs

Keep all journey state rules (closed overrides blockers; unknown stage never
invents current; earlier unconfirmed funding/resident steps not done).
Add short blocked status plus a first-reason summary rendered on one line.
Keep full every-blocker reason/owner/action in native `popover=auto` content,
controlled by a real button with popovertarget. Do not nest controls inside
journey links. Keep content safely rendered by h(), not HTML strings.
Use unique summary/step disclosure IDs. Use token spacing; decorative PNGs
have alt="", aria-hidden and dimensions. Restore wrapping without truncating
step names or tab labels.

PC-001: Constrain open popovers to viewport inline/block space, wrap long
words and allow a focusable keyboard/touch scrolling path. Full missing-field
fallbacks remain explicit. Enlarged text is allowed to increase collapsed
heights; default-size height ceilings must not cause enlarged-text clipping.

Move tablist into the case workspace ahead of the panels. Expose tabs to
keyboard without a scroll-region wrapper. Give the active panel a named,
focusable native scrolling area, bounded by viewport-relative maximum height.
Inactive panels remain hidden and mounted; all existing URL and manual tab
activation logic remains. Fallback unenhanced listed panels stay unbounded.

<!-- rpi:phase id=P02 -->
## P02: Evidence and independent Review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validate and document

Use `/tmp/mv/bin/python`, explicit current src roots and existing tests.
Run test_case_journey, test_workspace_scripts, test_design_system,
test_accessibility_baseline and test_content_standard in one runner.
Run `node --check` on changed JS. Browser callback uses the existing real
loopback server; block external requests; use synthetic route overlays only
for long blocker fixture, not a replacement page. Assert loaded PNGs, complete
labels, height thresholds, single-line summaries, full details and owner/action,
keyboard Enter/Space/Escape, touch tap/light dismiss, manual tabs/Home/End,
URL/back, retained inputs, panel scroll with stationary tabs, no page overflow,
reduced motion and no JS errors. Capture 1280/390/320 screenshots and JSON.
Record exact commands, success/failure, artifacts and limitations in changes.

PC-001: Open multiple very long blockers at 320px/short viewport and 200% root
text, scroll the focusable popover by keyboard and touch, and verify the last
reason/owner/action is actually visible, not merely in textContent.
PC-002: Block the workspace script, then separately inject an enhancement
exception after layout mutation. Require all listed panels, no inner-scroll
bounds/tab UI, reachable safety and usable ordinary controls. Deliberate
injected errors are recorded separately from unexpected page errors.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and commit locally

Refresh guidelines, inspect changed web files against all fetched rules, then
one fresh independent rpi-review with pointer-first evidence. Preserve original
critique and Review even if adverse; do not loop Review. Record required
human/live/full publication gates as unperformed, never accepted implicitly.
Commit with authenticated GitHub privacy-safe local identity and Copilot trailer.
No push, no PR creation, no az, no rubric score writes.

## Completion Evidence

P01 complete: exact icon bytes checked, measured baseline captured, compact
labels/popovers/attached wrapping tabs implemented. Fourth browser iteration
passed default-size, 200% text, keyboard/touch and both fallback scenarios.
Final assertion-expanded run passed at /tmp/case-552-ui-complete-20261029.
Chromium 156.0.8078.4/Playwright 1.64.0; 54 unittest tests, Node syntax,
Ruff and focused mypy passed. Independent Review executed Partial / Residual
work; RV-001 external-evidence access routes to a distinct later research action.
No source defects identified, no repeated Review. Source and original evidence
committed locally as e130e33f with Refs #552, no push. All task execution markers
complete; independent rendered acceptance remains open under RV-001.
No significant unanswered decisions; original critique retained.
