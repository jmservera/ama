"use strict";

registerRoleScreen({
  id: "finance-evidence",
  title: "Finance and grant readiness",
  roles: ["Grants and Evidence Officer", ...screenManagers],
  render(c) {
    const finance = c.finance;
    const cash = (value) => typeof value === "number" && Number.isFinite(value)
      ? new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(value) : "Unknown";
    return [
      screenPanel("Budget and commitment comparison",
        h("p", {}, "Readiness evidence only. A recorded or reviewed amount is not a payment, grant submission, award or spending approval from this view."),
        screenFields([["Budget amount", cash(finance?.budget?.amount)], ["Budget status", finance?.budget?.status],
          ["Budget approver", finance?.budget?.approved_by]]),
        screenTable("Commitment evidence", ["Reference", "Work order", "Measure and scope", "Version", "Quantity", "Amount", "Status"],
          (finance?.commitments || []).map((item) => [
            item.id, item.work_order, item.measure, item.version, item.quantity, cash(item.amount), item.status
          ]))),
      screenPanel("Invoice line evidence and exceptions",
        screenTable("Invoice lines", ["Invoice and work order", "Measure", "Version", "Quantity", "Amount", "Matched commitment", "Accepted milestone reference", "Recorded exceptions"],
          (finance?.invoices || []).flatMap((invoice) => (invoice.lines || []).map((line, index) => [
            `${invoice.id}; ${invoice.work_order}`, line.measure, line.version,
            line.quantity, cash(line.amount), invoice.commitment,
            line.milestone_ref,
            (invoice.exceptions || []).filter((item) => item.line === null || item.line === index)
              .map((item) => item.message).join("; ") || "No check result supplied; not acceptance"
          ]))),
        screenUnknown("Line scope/version, budget and independently accepted milestone evidence must be verified; missing inputs cannot pass a check.", "Grants and Evidence Officer", "Inspect the exact invoice, commitment and independent evidence in the existing case workspace. A different authorised person reviews what you prepare.")),
      screenPanel("Funding route and constructed field draft",
        screenFields([["Recorded funding route", c.funding?.route], ["Funding status", c.funding?.status],
          ["Template/version source", "Unknown; no template contract supplied"],
          ["Reviewed evidence", c.funding?.approved_by || "Unknown; no reviewer evidence supplied"]]),
        h("p", {}, "Constructed field draft, not reviewed: EPC source comparison. No candidate is selected automatically and no field is submitted."),
        screenTable("Conflicting source candidates", ["Field", "First candidate and source/version/date", "Second candidate and source/version/date", "Query owner", "Disposition"],
          (c.stock_reconciliation || []).map((item) => [
            item.field,
            `${screenValue(item.left?.value)}; ${screenValue(item.left?.source_id)}; v${screenValue(item.left?.version)}; ${screenValue(item.left?.date)}`,
            `${screenValue(item.right?.value)}; ${screenValue(item.right?.source_id)}; v${screenValue(item.right?.version)}; ${screenValue(item.right?.date)}`,
            screenPerson(item.query_owner), item.status
          ])),
        h("p", {}, "Draft field value: Unknown until the named reviewer resolves the conflicting evidence. Safe endpoint: this readiness view, not a reviewed export or external submission.")),
      screenPanel("AI economics - design only",
        h("p", {}, "Draft economics requirements remain proposals. No price, budget or target is set here. Missing prices and billing inputs mean Unknown; token counts alone are not Total Cost of AI."),
        screenTable("AI cost and value evidence", ["Component", "Evidence status"], [
          ["Usage reconciled to billing", "Unknown"], ["Reviewed price source and period", "Unknown"],
          ["Inference and retries", "Unknown"], ["Platform, storage, energy and capital", "Unknown"],
          ["Software and licensing", "Unknown"], ["Labour, human review and process change", "Unknown"],
          ["Total Cost of AI", "Unknown"], ["Accepted outcome denominator", "Unknown"],
          ["Quality floor and result", "Unknown"], ["Cost per accepted outcome", "Unknown"],
          ["Booked-value destination and status", "Unknown; no booked value evidenced"]
        ]),
        screenUnknown("No billing reconciliation, reviewed tariff or accepted-outcome evidence is supplied.", "Finance", "Reconcile the source records and total cost components before making a cost or value claim."))
    ];
  }
});
