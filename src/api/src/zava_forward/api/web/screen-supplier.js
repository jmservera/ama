"use strict";

registerRoleScreen({
  id: "supplier",
  title: "Supplier capacity and job evidence",
  roles: ["Contractor", ...screenManagers],
  async load() {
    const orders = await api("/api/workorders");
    const packages = me.user.role === "Contractor" ? null : await api("/api/packages");
    return { orders, packages };
  },
  render(c, data) {
    const orders = data.orders.filter((item) => item.case_id === c.id);
    if (me.user.role === "Contractor") {
      return [
        screenPanel("Assigned job pack",
          h("p", {}, "This is your existing restricted contractor view, not a provider portal or a new identity claim. No resident vulnerability reason is supplied."),
          screenFields([["Home", c.id], ["Works", c.measures], ["Named contact", c.named_contact],
            ["Practical notice", c.needs_notice ? "Needs notice; ask the named contact" : "No additional notice recorded"]]),
          screenTable("Assigned work orders for this home", ["Order", "Version", "Scope", "Recorded state", "Appointment state, not a new booking"],
            orders.map((item) => [item.id, item.version, item.scope, item.state, item.appointment_control?.status])),
          screenUnknown("Submission receipt, correction instructions and job-specific evidence checklist are not supplied in this restricted case read.", screenValue(c.named_contact) === "Unknown" ? "Contract manager" : c.named_contact, "Ask the named contact for the authorised job pack and correction checklist. Use the existing manual submission route.")),
        screenPanel("Submission is not acceptance",
          screenFields([["Provider submission", "Unknown"], ["Acknowledgement", "Unknown"],
            ["Independent quality review", "Unknown"], ["Acceptance", "Unknown"]]),
          h("p", {}, "A provider's submission or acknowledgement is never independent acceptance. Nothing is submitted, booked or self-approved here."))
      ];
    }
    return [
      screenPanel("Programme package queue",
        h("p", {}, "Programme-wide package evidence is separate from the selected home. A package is not proof this home has a work order. Recorded committed capacity is not usable unless its evidence is current."),
        screenTable("Packages, period and scope", ["Package", "Period", "Scope and version", "Call-off reference and version"],
          data.packages.map((item) => [
            `${item.id}: ${item.name}`, `${screenValue(item.period_from)} to ${screenValue(item.period_to)}`,
            `${screenValue(item.scope)}; v${screenValue(item.scope_version)}`,
            `${screenValue(item.contract_ref)}; v${screenValue(item.contract_version)}`
          ])),
        screenTable("Offered versus committed capacity", ["Package and supplier", "Offered", "Recorded committed", "Usable committed", "Evidence status", "Next reviewer"],
          data.packages.flatMap((item) => item.capacity.map((capacity) => [
            `${item.id}: ${capacity.contractor}`, capacity.offered, capacity.committed,
            capacity.usable_committed, capacity.evidence_status, "Contract manager"
          ])))),
      screenPanel("Selected-home order and review readiness",
        screenTable("Orders linked to this home", ["Order", "Version", "Scope", "State", "Appointment evidence"],
          orders.map((item) => [item.id, item.version, item.scope, item.state, item.appointment_control?.status])),
        screenUnknown("Draft readiness only. Contract, source, capacity, current resident choices and independent review must be checked.", "Contract manager", "Inspect unmet prerequisites with the named technical and resident-workflow reviewers before any existing authorised work-order process."),
        h("p", {}, "Provider submission and acknowledgement stay separate from independent quality review and acceptance. No booking, call-off, portal submission or self-approval occurs here."))
    ];
  }
});
