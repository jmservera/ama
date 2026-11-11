# Details: issue 80 entrypoint follow-up

* Plan: `.copilot-tracking/plans/2026-11-10/issue-80-entrypoint-followup-1110-plan.md`
* Date: 2026-11-10

## Option 2 details (only if Root authorises)

* Site: `src/api/src/zava_forward/api/web/ops.js` `capacityView` show block, after `h("h2", {}, "Packages")` and inside the Work orders section after its `h2`.
* Anchor shape: `h("p", {}, h("a", { class: "btn alt", href: "/api/packages.csv", download: "packages.csv" }, "Download for Excel"), " The file is a read-only copy; changes in it are not imported back.")`, and the `workorders.csv` equivalent. Both match the sentence used at `web/ops.js:246`.
* Contract: no server, role, projection or retention change; `LIST_EXPORTS` already holds both paths (`server.py:172-173`).
* Validation if later admitted: `api/tests/test_list_export_api.py` targeted run; the populated-fixture browser observation repeated for the two selectors; web-guidelines review of the changed file. None run now.
* Evidence limit: a visible control does not prove correct rows, authorisation or source immutability.

## Optional re-observation (only if Root authorises)

Unobserved stages: `#/progress?report=progress`, `#/all?report=progress`, `#/case/ZF-1`. Use a driver that navigates with a full load or awaits `hashchange` re-render and checks the actual heading text from the page. Same admission and owned-data rules.
