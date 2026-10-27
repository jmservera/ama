"use strict";

registerRoleScreen({
  id: "asset",
  title: "Asset and investment evidence",
  roles: screenManagers,
  render(c) {
    const age = (value) => {
      const time = value ? Date.parse(value) : NaN;
      if (!Number.isFinite(time)) return "Unknown";
      const days = Math.floor((Date.now() - time) / 86400000);
      return days < 0 ? "Future-dated; verify source" : `${new Intl.NumberFormat("en-GB").format(days)} days at this lookup; not a freshness decision`;
    };
    const source = (item) => `${screenValue(item?.value)}; ${screenValue(item?.source_id)}; version ${screenValue(item?.version)}; date ${screenValue(item?.date)}; age ${age(item?.date)}; ${screenValue(item?.validation_state)}`;
    return [
      screenPanel("Scope and evidence boundary",
        h("p", {}, `This is selected-home evidence for ${c.id}, viewed through your existing programme role. It is not a provisioned Asset Executive or Board identity and does not approve investment.`),
        screenFields([["Portfolio scope", "Unknown; one selected home is not an investment cohort"],
          ["Selected home", c.id], ["Area", c.home?.area], ["Tenure", c.home?.tenure]]),
        h("p", {}, h("a", { href: "#/overview" }, "Open existing programme overview, not an investment forecast"))),
      screenPanel("Stock conflicts and eligibility",
        screenTable("Stock source comparison", ["Field", "First source and age", "Compared source and age", "Resolution owner", "Eligibility"],
          (c.stock_reconciliation || []).map((item) => [
            item.field, source(item.left), source(item.right), screenPerson(item.query_owner), item.eligibility
          ])),
        screenUnknown("Unresolved stock authority and investment eligibility remain Unknown.", "Asset evidence reviewer with the named stock-query owner", "Resolve the exact source conflict and evidence the eligibility decision before using this home in an investment cohort.")),
      screenPanel("Missing investment inputs and phase decisions",
        screenTable("Investment evidence", ["Input", "Current evidence class and state"], [
          ["Budget and affordability", "Unknown; no investment budget fixture supplied"],
          ["Investment priority", "Unknown; work-list order is not investment authority"],
          ["Delivery forecast and committed resources", "Unknown"],
          ["Whole-life costs and displaced maintenance", "Unknown"],
          ["Benefit baseline, counterfactual and observed outcome", "Unknown; no validated benefit"],
          ["Phase decision and named approval evidence", "Unknown; no investment approval"]
        ])),
      screenPanel("AI outcome economics - design only",
        screenTable("Cost, quality and value together", ["Cost per accepted outcome", "Quality floor and achieved result", "Booked-value status", "Evidence class"], [
          ["Unknown", "Unknown", "Unknown; no booked value evidenced", "Design proposal; unmeasured"]
        ]),
        h("p", {}, "Total Cost of AI includes inference, platform, software, licences, labour, review and process change. A token-only figure is never the cost of AI. Finance must reconcile billing, reviewed prices, accepted outcomes and value before an investment claim."))
    ];
  }
});
