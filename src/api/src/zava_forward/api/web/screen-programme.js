"use strict";

registerRoleScreen({
  id: "programme",
  title: "Programme coordination and returned work",
  roles: ["Retrofit Coordinator", ...screenManagers],
  render(c) {
    const handoff = c.handoff;
    return [
      screenPanel("Returned work and accountable ownership",
        screenFields([
          ["Current owner", c.owner], ["Current stage", c.stage],
          ["Handoff state", handoff?.status], ["Sender", handoff?.from_name],
          ["Proposed receiver", handoff?.proposed_receiver],
          ["Confirmed receiver", handoff?.confirmed_receiver],
          ["Chase owner", handoff?.chase_owner],
          ["Resident-update owner", screenPerson(c.resident_update?.owner_identity)],
          ["Resident-update purpose", c.resident_update?.purpose],
          ["Resident-update due", screenStamp(c.resident_update?.due_at)]
        ]),
        h("p", {}, "Sending, receipt and acceptance are different. The current owner keeps responsibility until the recorded handoff is accepted. Chase responsibility and the resident-update commitment stay separate."),
        screenTable("Returns for this home", ["From and to", "Return reason", "Sender", "Receiving owner", "Source", "Next action"],
          (c.returns || []).map((item) => [
            `${item.from_stage} to ${item.to_stage}`, item.reason, item.by,
            screenPerson(item.receiving_owner), item.source, item.next_action
          ]))),
      screenPanel("One home, independent work states",
        h("p", {}, `These states all belong to ${c.id}. They are not stages assembled from different example homes.`),
        screenTable("Independent states", ["Responsibility", "Recorded state, not permission to move on"], [
          ["Technical", `Design ${screenValue(c.technical?.design_version)}; ${(c.technical_missing || []).length} missing technical references or reviews`],
          ["Resident", (c.measure_decisions || []).map((m) => `${m.measure}: ${m.status}; ${m.readiness}`).join("; ") || "Unknown"],
          ["Delivery", c.stage],
          ["Quality", (c.quality || []).map((q) => `${q.measure}: ${q.state}`).join("; ") || "Unknown; no evidence supplied"],
          ["Finance", c.finance?.budget ? `${c.finance.budget.status} budget; not a payment decision` : "Unknown or not supplied for this role"],
          ["Funding", c.funding?.state || c.funding?.status || "Unknown"],
          ["Safety", (c.hazards || []).some((item) => !item.released) ? "Safety issue open; independent response continues" : "No open report supplied; not proof of safety"]
        ]),
        screenUnknown("Readiness is not established by this view. Missing or stale evidence remains blocking.", "Retrofit Coordinator", "Inspect each current scoped review and final check in the existing case workspace."),
        screenTable("Missing technical references and reviews", ["Item", "Responsible reviewer role"],
          (c.technical_missing || []).map((item) => [item.item, item.assigned_to])),
        (c.gate || []).length ? h("ul", {}, c.gate.map((reason) => h("li", {}, reason)))
          : h("p", {}, "No final-check reason supplied. This is not an independent authorization.")),
      screenPanel("Programme scope and lifecycle",
        h("p", {}, "The specialist queue is all permitted cases. Its reset restores the default first page and clears selection without changing any record. Use the existing coordinator workspace for region, stage and other scope filters; the overview supplies the programme funnel."),
        h("p", {}, h("a", { href: "#/coordinator" }, "Open existing coordinator scope filters")),
        h("p", {}, h("a", { href: "#/overview" }, "Open lifecycle and funnel overview")))
    ];
  }
});
