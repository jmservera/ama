<!-- markdownlint-disable-file -->
# Asset and board evidence class: research (2026-11-03)

Task: `issue-226-evidence-class`. Refs #226. Disposition: executed (code and PR review).

## Prior delivery (merged)

* #639 screen, #710 cross-home queue, #771 phase check table, #800 browser check, #823 AI-unavailable state. Criteria 1, 2, 3 and 6 are covered in code and unit tests; criteria 4 and 5 and the tokenomics criterion (design only) need human validation (#155, #151, #150).
* Closed #491 superseded.

## Gap found

* `assetCost` in `role-screens.js` showed `evidence_label || coverage` as "Evidence class", so a report with no label displayed coverage (for example "complete") as if it were an evidence class. It also showed the quality-qualified cost component with no evidence class. The tokenomics criterion requires cost shown with its evidence class.
* The panel is shared with the Finance screens.

## Planning Readiness

Ready. Slice: evidence class reads Unknown without a label; cost component hidden without one. Web only; not security, infrastructure, SQL or deployment, so tier is focused.

Web guideline source fetched 2026-11-03 (first 6000 characters only; the remainder was not retrieved).
