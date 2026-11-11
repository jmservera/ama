---
title: Issue 80 capacity page export controls, review
description: Native post-implementation review of the two Capacity page CSV anchors (not independent review)
ms.date: 2026-11-10
---

## Execution

* Review executed once after implement-done, by the implementing author (native self-review). It is not the independent exact-head review Root requires before publication, and no human or hosted approval is implied.
* Assessed boundary: `git diff` of `ops.js` and `capacity_browser_check.py` against the preparation baseline `181da535`, the changes record, the focused validation outputs and the browser run log `ROOT/phase80-capacity-exports-evidence-1110/browser-run1.log`.
* Outcome: OPEN FINDINGS (not conformant). Implementation matches the admitted scope; focused validation is incomplete because the one browser run failed at an unrelated route.

## Scope conformance

| Root requirement | Result | Evidence |
| --- | --- | --- |
| Exactly two native anchors near Packages and Work orders headings | Met | `ops.js:485-494`, `h2` then anchor paragraph then pager |
| Fixed existing routes, no API/core/permission/serializer/route/default/filter change | Met | diff touches only the two files; hrefs `/api/packages.csv`, `/api/workorders.csv` |
| Honest export breadth | Met | sentence "every package|work order you can see, not only the ones on this page"; run showed 20 rows on the page and 601 CSV rows |
| One-way read-only meaning | Met in text and observed | sentence "read-only copy; changes in it are not imported back"; check asserted no POST and unchanged URL |
| Keyboard semantics, non-colour cues | Met by construction and observed for activation | native `<a>`, Enter activated download; text label, existing `.btn` focus style |
| Withhold when misleading | Met by source reading only | `total ? link : null`; the empty scenario assertion did not run |
| No role grant, progress variant, new fields | Met | manager-only page unchanged |

## Web guideline findings (source fetched 2026-11-10, rules applied to changed web file)

```text
## src/api/src/zava_forward/api/web/ops.js

ops.js:485 - pass: native <a> with download for a file link, text label equals accessible name, no aria needed, .btn gives hover and :focus-visible, no transition: all
ops.js:488 - pass: copy in active voice, plain ASCII, numerals not needed
ops.js:490 - pass: empty state not broken, no control when total is 0
ops.js:494 - pass: same for work orders; heading order h1 > h2 unchanged
ops.js:485 - note: label uses sentence case, the fetched Title Case rule yields to the content standard and the existing "Download for Excel" links
```

Not assessed (no evidence): rendered layout, reflow, screen-reader output, target size in render, deployed behaviour. No conformance or acceptance claim.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| R1 | Medium | The one browser run of `capacity_browser_check.py` exited 1 at an unrelated `#/time` expectation (status text drifted after #1343). The new export assertions passed, but the empty-capacity scenario with the zero-anchor assertion and later scenarios were not executed. The check as a whole is not a pass. | Later user-selected work: Root decides whether to admit a separate repair of the `#/time` expectation and one re-run. Not repaired here; no re-run admitted. |
| R2 | Low | The seed has one package, so package breadth beyond a page is not exercised; only work orders (20 shown, 601 exported) show it. | Accept; label is source-true. |
| R3 | Low | Only the Retrofit Programme Manager role was exercised; Programme Support Officer shares `isManager` and `STAFF_GET` but was not run. | Accept; no role change made. |
| R4 | Low | Anchor label differs from the existing "Download for Excel" wording to keep the two accessible names distinct. | Accept as intentional; Root may prefer other wording. |
| R5 | Info | Attribution of R1 to #1343 is by source reading, not a baseline re-run. | Disclosed. |

## Routing and limits

* No transition back to Implement or a second Review in this task.
* Whole every-list criterion remains UNPROVEN. Progress variant, other registers and owner thresholds remain open. C2, C4 and #73 remain OPEN. This change creates no further allowance.
