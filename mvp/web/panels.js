"use strict";
// Case panels for finance, grants, technical sign-offs and resident decisions. Plain words; every action is one record at a time.
const FIN_ROLES = ["Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"];
const money = (n) => `£${Number(n).toLocaleString("en-GB", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const caseApi = (id, part, body) => api(`/api/cases/${encodeURIComponent(id)}/${part}`, body);

function actForm(title, fields, run, label) {
  const inputs = fields.map(([name, text, opts]) => {
    const el = opts && opts.options
      ? h("select", { id: `f-${title}-${name}` }, opts.options.map((o) => h("option", { value: o }, o)))
      : h("input", { id: `f-${title}-${name}`, type: (opts && opts.type) || "text", maxlength: 300 });
    return [name, text, el];
  });
  const body = () => Object.fromEntries(inputs.map(([name, , el]) => [name, el.value]));
  return h("details", {}, h("summary", {}, title),
    inputs.map(([name, text, el]) => [h("label", { for: el.id }, text), el]),
    h("p", {}, h("button", { onclick: () => run(body()) }, label || title)));
}

function financePanel(c, id, refresh) {
  const f = c.finance;
  if (!FIN_ROLES.includes(me.user.role)) return null;
  const go = (action, extra) => refresh(() => caseApi(id, "finance", Object.assign({ action }, extra)));
  const fx = f || { budget: null, commitments: [], invoices: [] };
  const invoiceIds = fx.invoices.map((i) => i.id);
  const pick = (o) => Object.assign({ options: invoiceIds.length ? invoiceIds : [""] }, o);
  return h("section", { class: "card" }, h("h2", {}, "Budget, commitments and invoices"),
    h("p", { class: "muted" }, "This records what people decided. The system never pays anything. A different person must approve what you prepare."),
    h("p", {}, fx.budget ? `Budget ${money(fx.budget.amount)}: ${fx.budget.status.toLowerCase()}${fx.budget.approved_by ? ` by ${fx.budget.approved_by}` : ` (prepared by ${fx.budget.proposed_name})`}.` : "No budget recorded yet."),
    fx.commitments.length ? h("ul", {}, fx.commitments.map((m) => h("li", {}, `${m.id}: ${m.supplier}, ${m.measure}, ${money(m.amount)}, work order ${m.work_order}. ${m.status}${m.approved_by ? ` by ${m.approved_by}` : ` (raised by ${m.raised_name})`}.`))) : h("p", { class: "muted" }, "No commitments yet."),
    fx.invoices.length ? fx.invoices.map((i) => h("div", { class: "card" },
      h("strong", {}, `${i.id}: ${i.kind.toLowerCase()} ${i.ref} from ${i.supplier}. ${i.status}.`),
      h("div", { class: "muted" }, `Payment: ${i.payment_status}. ${i.disposition ? `Finance decision: ${i.disposition} (${i.disposition_by}).` : "No Finance decision yet."}${i.hold ? ` Payment paused: ${i.hold.reason}.` : ""}`),
      i.exceptions.length ? h("ul", {}, i.exceptions.map((e) => h("li", {}, `${e.line == null ? "Whole invoice" : `Line ${e.line + 1}`}: ${e.message}`))) : null)) : null,
    actForm("Propose a budget", [["amount", "Amount in pounds"], ["note", "Note"]], (b) => go("budget_propose", b), "Save proposed budget"),
    fx.budget && fx.budget.status === "Proposed" ? h("p", {}, h("button", { onclick: () => go("budget_approve") }, `Approve the budget as ${me.user.name}`)) : null,
    actForm("Raise a commitment", [["supplier", "Supplier"], ["contract", "Contract reference"], ["work_order", "Work order"], ["measure", "Measure"], ["amount", "Amount in pounds"], ["quantity", "Quantity"]], (b) => go("commit_raise", b), "Raise commitment"),
    actForm("Approve a commitment", [["id", "Commitment", { options: fx.commitments.filter((m) => m.status === "Raised").map((m) => m.id).concat([""]) }]], (b) => go("commit_approve", b), "Approve"),
    actForm("Record an invoice or valuation", [["kind", "Kind", { options: ["Invoice", "Valuation"] }], ["supplier", "Supplier"], ["work_order", "Work order"], ["ref", "Provider's reference"], ["measure", "Measure on the line"], ["quantity", "Quantity"], ["amount", "Line amount in pounds"], ["milestone_ref", "Accepted milestone evidence reference (leave blank if unknown)"]],
      (b) => go("invoice_receive", { kind: b.kind, supplier: b.supplier, work_order: b.work_order, ref: b.ref, lines: [{ measure: b.measure, quantity: b.quantity, amount: b.amount, milestone_ref: b.milestone_ref }] }), "Record invoice"),
    invoiceIds.length ? [
      actForm("Check an invoice against the commitment", [["id", "Invoice", pick()]], (b) => go("invoice_match", b), "Check now"),
      actForm("Pause payment on an invoice", [["id", "Invoice", pick()], ["reason", "Why"]], (b) => go("hold_place", b), "Pause payment"),
      actForm("Restart payment on an invoice", [["id", "Invoice", pick()], ["note", "Why it is restarted"]], (b) => go("hold_release", b), "Restart payment"),
      actForm("Finance decision", [["id", "Invoice", pick()], ["decision", "Decision", { options: ["Accept for payment", "Reject and return to provider", "Keep on hold"] }], ["note", "Note"]], (b) => go("disposition", b), "Record decision"),
      actForm("Note the payment status", [["id", "Invoice", pick()], ["status", "Status", { options: ["Not payable yet", "Awaiting payment run", "Paid outside this system"] }]], (b) => go("payment_status", b), "Save note"),
    ] : null);
}

function grantPanel(c, id, refresh) {
  if (!FIN_ROLES.includes(me.user.role)) return null;
  const grants = c.grants || [];
  const go = (action, extra) => refresh(() => caseApi(id, "grant", Object.assign({ action }, extra)));
  const ids = grants.map((g) => g.id);
  return h("section", { class: "card" }, h("h2", {}, "Grant stages"),
    h("p", { class: "muted" }, "Each stage is kept on its own with its evidence and who approved it. Grants are separate from invoices and payments."),
    grants.length ? grants.map((g) => h("div", {}, h("strong", {}, `${g.id}: ${g.scheme}. Now: ${g.state}.`),
      g.pending ? h("div", { class: "muted" }, `Waiting for approval: ${g.pending.to}, proposed by ${g.pending.name}. Evidence: ${g.pending.source}.`) : null,
      h("ul", {}, g.history.map((x) => h("li", {}, `${x.state}: ${x.source}. Proposed by ${x.proposed_by}, approved by ${x.approved_by}.${x.amount ? ` ${money(x.amount)}.` : ""}`))))) : h("p", { class: "muted" }, "No grant recorded."),
    actForm("Add a grant", [["scheme", "Scheme or funder"], ["source", "Evidence for the opportunity"]], (b) => go("grant_open", b), "Add grant"),
    ids.length ? [
      actForm("Propose the next stage", [["id", "Grant", { options: ids }], ["to", "Next stage", { options: ["Award", "Claimable", "Submitted", "Accepted", "Rejected", "Cash received"] }], ["source", "Evidence"], ["amount", "Amount in pounds (needed for cash received)"]], (b) => go("grant_propose", b), "Propose"),
      actForm("Approve a proposed stage", [["id", "Grant", { options: ids }]], (b) => go("grant_approve", b), "Approve"),
      actForm("Withdraw a proposal", [["id", "Grant", { options: ids }]], (b) => go("grant_withdraw", b), "Withdraw"),
    ] : null);
}

function technicalPanel(c, id, refresh) {
  const t = c.technical;
  const go = (action, extra) => refresh(() => caseApi(id, "technical", Object.assign({ action }, extra)));
  const TYPES = [["assessment", "Retrofit assessment"], ["design", "Design"], ["building", "Building and safety dependency"], ["coordination", "Coordination"]];
  return h("section", { class: "card" }, h("h2", {}, "Assessment and technical sign-offs"),
    !t ? h("p", { class: "muted" }, "No design recorded yet.") : [
      h("p", {}, `Design version ${t.design_version}, recorded by ${t.design_name}. The person who recorded the design cannot sign it off.`),
      h("table", {}, h("thead", {}, h("tr", {}, ["Sign-off", "State", "By", "Note"].map((x) => h("th", {}, x)))),
        h("tbody", {}, TYPES.map(([k, label]) => { const s = t.signoffs[k]; return h("tr", {}, h("td", {}, label), h("td", {}, s ? s.status : "Not given"), h("td", {}, s && s.by ? s.by : ""), h("td", {}, s ? (s.reason || s.note || "") : "")); }))),
      c.technical_missing.length ? [h("p", {}, "Still needed before this stage can pass:"), h("ul", {}, c.technical_missing.map((m) => h("li", {}, `${m.item}. For the ${m.assigned_to}.`)))] : h("p", {}, "Every sign-off and piece of evidence is in place."),
    ],
    !t ? actForm("Record the design", [["note", "What the design covers"]], (b) => go("design_submit", b), "Record design")
      : actForm("The design has changed", [["note", "What changed"], ["affects", "Which sign-offs this affects", { options: ["All that depend on the design", "design", "building", "coordination"] }]],
        (b) => go("design_change", { note: b.note, affects: b.affects.startsWith("All") ? undefined : [b.affects] }), "Record change"),
    t ? [
      actForm("Give a sign-off", [["type", "Which one", { options: TYPES.map((x) => x[0]) }], ["note", "Note"]], (b) => go("signoff_give", b), `Sign off as ${me.user.name}`),
      actForm("Send a sign-off back", [["type", "Which one", { options: TYPES.map((x) => x[0]) }], ["reason", "Why"]], (b) => go("signoff_return", b), "Send back"),
    ] : null);
}

function residentPanel(c, id, refresh) {
  const go = (action, extra) => refresh(() => caseApi(id, "resident", Object.assign({ action }, extra)));
  const measures = (c.measure_decisions || []);
  const reqs = c.service_requests || [];
  const staff = (me.staff || []).filter((s) => s.role !== "Contractor");
  const who = staff.map((s) => s.email);
  return h("section", { class: "card" }, h("h2", {}, "Decision for each measure"),
    h("p", { class: "muted" }, "These start as not recorded. Only write what the resident told you. Contact or access is never treated as a yes."),
    h("table", {}, h("thead", {}, h("tr", {}, ["Measure", "Their answer", "Versions"].map((x) => h("th", {}, x)))),
      h("tbody", {}, measures.map((m) => h("tr", {}, h("td", {}, m.measure), h("td", {}, m.status),
        h("td", {}, m.versions.map((v) => `v${v.version} ${v.status} (${v.answered_by}, recorded by ${v.recorded_by}${v.note ? `: ${v.note}` : ""})`).join("; ") || "None"))))),
    actForm("Record what the resident said", [["measure", "Measure", { options: measures.map((m) => m.measure) }], ["status", "Their answer", { options: ["Waiting", "Accepted", "Declined", "Paused", "Withdrawn"] }], ["answered_by", "Who said it", { options: ["The resident", "Their representative"] }], ["representative_ref", "Reference for the representative, if any"], ["note", "In their words (needed for declined, paused or withdrawn)"]], (b) => go("decision_record", b), "Save answer"),
    h("h2", {}, "Service requests and complaints"),
    reqs.length ? reqs.map((r) => h("div", {}, h("strong", {}, `${r.id}: ${r.route}. ${r.status}.`),
      h("div", { class: "muted" }, `${r.summary}. They want: ${r.desired_outcome}. Dealt with by ${r.service_owner}. Redress owner: ${r.redress_owner}. Contact needs: ${r.accessibility.join(", ")}. Representative: ${r.representative_ref}. Next update ${r.next_update}.`))) : h("p", { class: "muted" }, "None open."),
    actForm("Open a request or complaint", [["route", "Type", { options: ["Service request", "Complaint", "Repair", "Defect", "Hazard"] }], ["summary", "Short summary"], ["desired_outcome", "What the resident wants"], ["service_owner", "Who deals with it", { options: who }], ["redress_owner", "Who owns the redress", { options: who }], ["accessibility", "Contact need", { options: ["Unknown", "None", "Large print", "Phone only", "Plain language", "Interpreter", "Representative contact", "Safe route needed"] }], ["next_update", "Next update date", { type: "date" }]],
      (b) => go("service_open", Object.assign({}, b, { accessibility: [b.accessibility] })), "Open"),
    reqs.length ? [
      actForm("Update a request", [["id", "Request", { options: reqs.map((r) => r.id) }], ["status", "Status", { options: ["Open", "In progress", "Resolved"] }], ["next_update", "Next update date", { type: "date" }], ["note", "Note"]], (b) => go("service_update", b), "Save update"),
      actForm("Close a request", [["id", "Request", { options: reqs.map((r) => r.id) }], ["note", "Outcome for the resident"]], (b) => go("service_close", b), "Close"),
    ] : null);
}

async function financeQueueView() {
  let rows;
  try { rows = await api("/api/finance"); } catch (e) { return show(h("h1", {}, "Finance queue"), h("p", {}, e.message)); }
  show(h("h1", {}, "Finance queue"),
    h("p", { class: "muted" }, "Invoices with exceptions, paused payments or no check yet. A person decides each one. Nothing is paid from here."),
    rows.length ? h("table", {}, h("thead", {}, h("tr", {}, ["Home", "Invoice", "Supplier", "Status", "Exceptions", "Total"].map((x) => h("th", {}, x)))),
      h("tbody", {}, rows.map((r) => h("tr", {}, h("td", {}, h("a", { href: `#/case/${encodeURIComponent(r.case_id)}` }, r.address)), h("td", {}, `${r.invoice} ${r.ref}`),
        h("td", {}, r.supplier), h("td", {}, r.on_hold ? `${r.status}, payment paused` : r.status), h("td", {}, r.exceptions), h("td", {}, money(r.total)))))) : h("p", {}, "Nothing is waiting."));
}
