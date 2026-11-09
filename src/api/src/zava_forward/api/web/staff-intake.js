"use strict";
// Staff-mediated synthetic job pack intake (issue 132). Shares h, api and the role screen helpers with role-screens.js.
// Existing signed-in staff key in what a worker confirmed. This is not a provider portal and never accepts work.
const intakeRoles = ["Retrofit Coordinator", "Resident Liaison Officer", "Building Safety Liaison", "Grants and Evidence Officer",
  "Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer"];
const intakeStamp = (value) => screenStamp(value);

function intakeField(id, label, control, hint) {
  return h("div", { class: "field" }, h("label", { for: id }, label), control, hint && h("p", { id: `${id}-hint`, class: "hint" }, hint));
}

const intakeNotices = new Map();

function intakeForm(label, fields, submitLabel, task, rerender) {
  const feedback = h("p", { role: "alert", class: "err", hidden: true });
  const form = h("form", { "aria-label": label, autocomplete: "off", novalidate: true,
    onsubmit: async (event) => {
      event.preventDefault();
      feedback.hidden = true;
      const send = form.querySelector("button[type=submit]");
      send.disabled = true;
      try {
        await task(new FormData(form));
        await rerender();
      } catch (error) {
        send.disabled = false;
        feedback.textContent = `${error.message || "This could not be saved."} Check the entries and try again.`;
        feedback.hidden = false;
        feedback.scrollIntoView?.({ block: "nearest" });
      }
    } }, fields, h("button", { type: "submit", class: "btn" }, submitLabel), feedback);
  return form;
}

function intakeReceipt(order, receipt, rerender) {
  const rows = [
    ["Measure and checklist", `${receipt.measure}, ${receipt.checklist_version}`],
    ["Confirmed by the worker", receipt.confirmed_by],
    ["Keyed in by", receipt.recorded_by],
    ["Captured", `${intakeStamp(receipt.captured_at)} (${receipt.mode})`],
    ["Evidence status", receipt.status],
    ["Acknowledged by", receipt.acknowledgement ? `${receipt.acknowledgement.by}, ${intakeStamp(receipt.acknowledgement.at)}` : "Not yet acknowledged"],
    ["Accepted", receipt.accepted ? "Accepted by an independent reviewer" : "No. Acknowledging a receipt is not acceptance."],
    ["Independent review", receipt.review.state],
    ["You may review this", receipt.review.you_may_review ? "Yes, if you have a quality role" : receipt.review.blocker],
  ];
  const notes = Object.entries(receipt.original_notes).map(([label, text]) => [label, text]);
  const corrections = receipt.corrections.map((c) => [c.label, `${c.note} (worker ${c.confirmed_by}, ${intakeStamp(c.at)})`]);
  const ack = !receipt.acknowledgement && receipt.quality_state === "Submitted"
    ? intakeForm("Acknowledge receipt", [h("p", {}, "Acknowledging records that you have the evidence. It does not review or accept the work.")],
      "Acknowledge receipt", () => api(`/api/workorders/${encodeURIComponent(order)}/field-acknowledge`, { record: receipt.record }), rerender)
    : null;
  const fix = !receipt.acknowledgement && receipt.quality_state === "Submitted"
    ? h("details", {}, h("summary", {}, "Record a worker correction"),
      intakeForm("Worker correction", [
        intakeField(`fix-label-${receipt.record}`, "Check being corrected",
          h("select", { id: `fix-label-${receipt.record}`, name: "label", required: true },
            Object.keys(receipt.original_notes).map((label) => h("option", { value: label }, label)))),
        intakeField(`fix-note-${receipt.record}`, "Corrected note, in the worker's words",
          h("textarea", { id: `fix-note-${receipt.record}`, name: "note", maxlength: 200, rows: 2, required: true })),
        intakeField(`fix-by-${receipt.record}`, "Worker's name",
          h("input", { id: `fix-by-${receipt.record}`, name: "confirmed_by", value: receipt.confirmed_by, maxlength: 80, autocomplete: "off", spellcheck: "false" })),
        h("div", { class: "field" }, h("input", { type: "checkbox", id: `fix-ok-${receipt.record}`, name: "confirmed" }),
          h("label", { for: `fix-ok-${receipt.record}` }, "The worker confirms this correction is their own")),
      ], "Record correction", (data) => api(`/api/workorders/${encodeURIComponent(order)}/field-correct`, {
        record: receipt.record, label: data.get("label"), note: data.get("note"),
        confirmed_by: data.get("confirmed_by"), confirmed: data.get("confirmed") === "on" }), rerender))
    : null;
  return h("article", { class: "card", "aria-label": `Receipt ${receipt.capture_ref}` },
    h("h4", {}, `Receipt ${receipt.capture_ref}`),
    screenFields(rows),
    screenTable("Worker's original notes, kept as written", ["Check", "Note"], notes),
    corrections.length ? screenTable("Worker corrections, added after the original", ["Check", "Correction"], corrections) : null,
    h("p", {}, "Original notes are never overwritten. A correction is added beside them."),
    ack, fix);
}

function intakeCapture(order, pack, rerender) {
  const ref = `SYN-${(globalThis.crypto?.randomUUID?.() || String(Date.now())).slice(0, 24)}`;
  const measure = h("select", { id: "intake-measure", name: "measure" },
    pack.measures.map((m) => h("option", { value: m }, m)));
  const notes = h("div", { id: "intake-notes" });
  const paint = () => {
    notes.replaceChildren(...pack.checklists[measure.value].items.map((label, i) => intakeField(`intake-note-${i}`, label,
      h("textarea", { id: `intake-note-${i}`, name: `note-${i}`, rows: 2, maxlength: 200, required: true, "data-label": label }))));
  };
  measure.addEventListener("change", paint);
  paint();
  const offline = h("input", { type: "checkbox", id: "intake-offline", name: "offline" });
  return intakeForm("Record the worker's evidence", [
    h("p", {}, `Checklist ${pack.checklists[pack.measures[0]]?.version || "unknown"}. Use the worker's own words, up to 200 characters a check.`),
    intakeField("intake-measure", "Measure", measure),
    notes,
    intakeField("intake-worker", "Worker's name", h("input", { id: "intake-worker", name: "confirmed_by", maxlength: 80, autocomplete: "off", spellcheck: "false" }),
      "The person who did the work, not you."),
    h("div", { class: "field" }, h("input", { type: "checkbox", id: "intake-confirmed", name: "confirmed" }),
      h("label", { for: "intake-confirmed" }, "The worker confirms these notes are their own")),
    h("div", { class: "field" }, offline, h("label", { for: "intake-offline" }, "These were written down offline earlier")),
    intakeField("intake-captured", "Time captured, if offline", h("input", { id: "intake-captured", name: "captured_at", type: "datetime-local" })),
  ], "Record worker evidence", async (data) => {
    const items = {};
    notes.querySelectorAll("textarea").forEach((area) => { items[area.dataset.label] = area.value; });
    const result = await api(`/api/workorders/${encodeURIComponent(order)}/field-capture`, {
      measure: measure.value, notes: items, confirmed_by: data.get("confirmed_by"), confirmed: data.get("confirmed") === "on",
      capture_ref: ref, pack_digest: pack.pack_digest,
      mode: data.get("offline") === "on" ? "offline" : "online",
      captured_at: data.get("offline") === "on" ? data.get("captured_at") : undefined });
    if (result.outcome === "duplicate") intakeNotices.set(order, "This evidence was already recorded. The existing receipt is shown and nothing was added.");
  }, rerender);
}

function intakeOrder(data, orderId, rerender) {
  const pack = data.pack;
  const status = h("p", { role: "status", "aria-live": "polite" });
  const notice = intakeNotices.get(orderId);
  intakeNotices.delete(orderId);
  if (notice) setTimeout(() => { status.textContent = notice; }, 0);
  return h("section", { class: "card", "aria-label": `Work order ${orderId}` },
    h("h3", {}, `Work order ${orderId}`),
    status,
    screenFields([["Scope", `${pack.scope} (version ${pack.scope_version})`], ["Design version", pack.design_version],
      ["Access", pack.access], ["Named contact", pack.named_contact], ["Appointment state", pack.state],
      ["Ready to start", pack.ready ? "Yes" : pack.not_ready_reason]]),
    pack.ready ? intakeCapture(orderId, pack, rerender)
      : h("p", { role: "status" }, "Evidence cannot be recorded until the scope, design version and appointment are confirmed."),
    h("h4", {}, "Receipts and independent review"),
    data.receipts.length ? data.receipts.map((r) => intakeReceipt(orderId, r, rerender))
      : h("p", { class: "empty" }, "No worker evidence recorded for this order yet."),
    screenTable("If the visit does not happen", ["Event", "Outcome", "Effect on the resident", "Next step"],
      data.recovery.map((r) => [r.event, r.outcome, r.resident_effect, r.next_step])),
    screenFields([["Escalation owner", data.escalation.owner], ["Escalation role", data.escalation.role],
      ["Escalation contact", data.escalation.contact],
      ["Effect", "A concern does not change the work order. Only the contract manager issues a new version."]]),
    h("p", {}, data.boundaries.acceptance), h("p", {}, data.boundaries.consent));
}

registerRoleScreen({
  id: "staff-job-pack-intake",
  title: "Job pack and worker evidence intake",
  roles: intakeRoles,
  async load(c) {
    const orders = await api(`/api/workorders?case=${encodeURIComponent(c.id)}`, undefined, routeController.signal);
    const details = await Promise.all(orders.map((o) => api(`/api/workorders/${encodeURIComponent(o.id)}/field-intake`, undefined, routeController.signal)
      .then((data) => ({ id: o.id, data }), (error) => ({ id: o.id, error }))));
    return { details };
  },
  render(c, extra) {
    const details = extra?.details || [];
    const rerender = () => roleScreensView();
    return h("div", {},
      screenPanel("What this screen does",
        h("p", {}, "Staff open a synthetic job pack and key in evidence the worker has confirmed. It is not a provider portal and gives no one new access."),
        h("p", {}, "It records evidence only. It never accepts work, gives a contract instruction or records resident consent."),
        h("p", {}, "Synthetic demonstration data. Named quality, legal and accessibility review are separate.")),
      details.length ? details.map((d) => d.error
        ? screenPanel(`Work order ${d.id}`, h("p", { role: "alert" }, `This order could not be read: ${d.error.message}`))
        : intakeOrder(d.data, d.id, rerender))
        : screenPanel("Work orders", h("p", { class: "empty" }, "No work order has been issued for this home.")));
  }
});
