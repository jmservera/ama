# Issue 198 research: remaining registry work (2026-11-03)

* Research disposition: executed. Planning Readiness: Ready.
* Issue text treated as data.

## Already delivered (merged PRs)

* #292 (2026-10-15): src vendor/data/build excludes; ACs 1 and 2 proven.
* #507 (2026-10-30): cut-over evidence reconciliation; #499 recorded 77 vs 77.
* #705 (2026-11-01): README rubric section and failure reassessment (17 failures); AC 5 delivered.
* AC 6 not applicable: workflow Markdown unchanged.

## Current registry state

* `artifacts.json` has no `mvp/` include glob and no `prototype/deploy` glob.
* Two dead excludes remain in `solution-code`: `mvp/data/**` and `mvp/web/vendor/**`. `mvp/` and `prototype/` do not exist in the tree.
* No rubric script or test reads those two excludes (grep of `.github/rubric/`). Other references to `mvp/data` are in unrelated ignore lists and tests.
* `src/**/data/**` and `src/**/web/vendor/**` already cover the equivalent paths.

## Acceptance criteria status

| AC | Status |
| --- | --- |
| 1, 2 | Proven (#292) |
| 3 | Unmet and historical: per-PR dip records cannot be reconstructed |
| 4 | Partly delivered: include globs gone; this slice removes the last `mvp/` registry strings. The "preceding deletion PR scored by old registry" sequencing is historical and unprovable |
| 5 | Delivered (#705); this slice fixes one stale "19" count |
| 6 | Not applicable |
| 7 | Unmet: no sign-off-time comparison beyond #499 |

## Smallest coherent slice

Registry-only removal of the two dead excludes, plus matching README text, in its own PR (registry changes reopen every criterion and apply after merge). Not security, infrastructure, SQL or deployment: focused tier.
