"use strict";
// Case panels for finance, grants, technical sign-offs and resident decisions. Plain words; every action is one record at a time.
const FIN_ROLES = ["Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"];
const money = (n) => `£${Number(n).toLocaleString("en-GB", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const caseApi = (id, part, body) => api(`/api/cases/${encodeURIComponent(id)}/${part}`, body);

function actForm(title, fields, run, label) {
  const inputs = fields.map(([name, text, opts]) => {
    const el = opts && opts.options
      ? h("select", { id: `f-${title}-${name}`, name, autocomplete: "off" }, opts.options.map((o) => h("option", { value: o }, o)))
      : h("input", { id: `f-${title}-${name}`, name, autocomplete: "off", type: (opts && opts.type) || "text", maxlength: 300 });
    return [name, text, el];
  });
  const body = () => Object.fromEntries(inputs.map(([name, , el]) => [name, el.value]));
  return h("details", {}, h("summary", {}, title),
    inputs.flatMap(([name, text, el]) => [h("label", { for: el.id }, text), el]),
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

function stockPanel(c) {
  const queries = c.stock_reconciliation || [];
  const assertion = (label, value) => h("section", {},
    h("h4", {}, label),
    h("dl", {}, ["value", "source_id", "date", "version", "validation_state"].flatMap((key) =>
      [h("dt", {}, key.replaceAll("_", " ")), h("dd", {}, String(value[key]))])));
  return h("section", { class: "card", "aria-labelledby": "stock-heading" },
    h("h2", { id: "stock-heading" }, "Stock source comparisons"),
    h("p", {}, "Competing evidence stays visible. No source is selected automatically; a named person owns each query."),
    queries.length ? queries.map((q) => h("section", {},
      h("h3", {}, `${q.id}: ${q.field}. ${q.status}`),
      h("p", {}, `Query owner: ${q.query_owner.name}, ${q.query_owner.role}.`),
      h("div", { class: "grid" }, assertion("First source", q.left), assertion("Compared source", q.right)),
      h("p", {}, `Authority: ${q.authority}. Resolution: ${q.resolution}. Eligibility: ${q.eligibility}.`),
      ...(c.stock_reconciliation_events || []).filter((e) => e.query_id === q.id).map((e) =>
        h("p", {}, `${e.id}: ${e.status}, recorded by ${e.recorded_by.name} (${e.recorded_by.role}) at ${e.at}. Reason: ${e.reason}. Evidence: ${e.evidence || "Not supplied"}.`)))) :
      h("p", {}, "No comparison recorded. Source authority and eligibility are Unknown."));
}

function technicalPanel(c, id, refresh) {
  const t = c.technical;
  const go = (action, extra) => refresh(() => caseApi(id, "technical", Object.assign({ action }, extra)));
  const TYPES = [["assessment", "Retrofit assessment"], ["design", "Design"], ["building", "Building and safety dependency"], ["coordination", "Coordination"]];
  return h("section", { class: "card" }, h("h2", {}, "Assessment and technical sign-offs"),
    !t ? h("p", { class: "muted" }, "No design recorded yet.") : [
      h("p", {}, `Design version ${t.design_version}, recorded by ${t.design_name}. The person who recorded the design cannot sign it off.`),
      h("p", {}, "Technical sign-off is a named human professional decision, never an AI approval. Role membership alone does not attest competence."),
      h("table", {}, h("thead", {}, h("tr", {}, ["Sign-off", "State", "Design version", "By", "Note"].map((x) => h("th", { scope: "col" }, x)))),
        h("tbody", {}, TYPES.map(([k, label]) => { const s = t.signoffs[k]; return h("tr", {}, h("td", {}, label), h("td", {}, s ? s.status : "Not given"), h("td", {}, s && s.version ? String(s.version) : "Not given"), h("td", {}, s && s.by ? s.by : ""), h("td", {}, s ? (s.reason || s.note || "") : "")); }))),
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
  if (c.resident_readiness) {
    return h("section", { class: "card" }, h("h2", {}, "Decision for each measure"),
      c.resident_readiness.map((m) => h("p", {}, `${m.measure}: ${m.flag}`)));
  }
  const recordForm = (...args) => c.can_record_resident ? actForm(...args) : null;
  const go = (action, extra) => refresh(() => {
    const body = Object.assign({ action }, extra);
    for (const key of ["context_revision", "design_version", "review_decision_version"]) {
      if (body[key] !== undefined) body[key] = Number(body[key]);
    }
    return caseApi(id, "resident", body);
  });
  const measures = (c.measure_decisions || []);
  const reqs = c.service_requests || [];
  const residentRoles = ["Resident Liaison Officer", "Retrofit Coordinator", "Retrofit Programme Manager", "Programme Support Officer"];
  const staff = (me.staff || []).filter((s) => residentRoles.includes(s.role));
  const who = staff.map((s) => s.email);
  const update = c.resident_update;
  const stamp = (value) => {
    const date = value ? new Date(value) : null;
    return date && !Number.isNaN(date.getTime())
      ? new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "short" }).format(date)
      : "Unknown";
  };
  const named = (owner) => owner?.name || "Unknown";
  const residentForm = (key, title, fields, action, build = (body) => body, label = title) => {
    if (!residentRoles.includes(me.user.role)) return null;
    const status = h("p", { id: `${key}-feedback`, role: "status", "aria-live": "polite", tabindex: -1 });
    const inputs = fields.map(([name, label, options]) => {
      const attrs = { id: `${key}-${name}`, name, autocomplete: "off", "aria-describedby": `${key}-feedback` };
      const input = options ? h("select", attrs, options.map((o) => h("option", { value: o }, o)))
        : h("input", { ...attrs, type: name === "due_at" ? "datetime-local" : name === "next_update" ? "date" : name === "review_decision_version" ? "number" : "text", maxlength: 300 });
      return { name, label, input };
    });
    const button = h("button", { type: "submit" }, label);
    const form = h("form", { oninput: () => { form.dataset.unsaved = "true"; }, onsubmit: async (event) => {
      event.preventDefault();
      button.disabled = true;
      status.textContent = "Recording";
      let dispatched = false;
      try {
        const body = Object.fromEntries(inputs.map(({ name, input }) => [name, input.value]));
        const payload = JSON.stringify({ action, ...build(body) });
        dispatched = true;
        const response = await fetch(`/api/cases/${encodeURIComponent(id)}/resident`, {
          method: "POST", headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" },
          body: payload
        });
        const result = await response.json();
        if (!response.ok) {
          status.textContent = result.error || "Could not record this step. Reload to check its history.";
          status.focus();
          if (result.outcome !== "committed") button.disabled = false;
          return;
        }
        delete form.dataset.unsaved;
        await refresh(async () => {});
      } catch (error) {
        status.textContent = dispatched
          ? "Confirmation is unavailable. Reload and check the history before another action."
          : "Check the date and time before recording this step.";
        if (!dispatched) button.disabled = false;
        status.focus();
      }
    } }, inputs.flatMap(({ label, input }) => [h("label", { for: input.id }, label), input]), status, button);
    return h("details", {}, h("summary", {}, title), form);
  };
  const serviceForm = (key, title, fields, action, build = (body) => body, label = title) =>
    residentForm(key, title, fields.map(([name, text, opts]) => [name, text, opts?.options]), action, build, label);
  return h("section", { class: "card" }, h("h2", {}, "Decision for each measure"),
    h("p", { class: "muted" }, "These start as not recorded. Only write what the resident told you. Contact or access is never treated as a yes."),
    !c.can_record_resident ? h("p", {}, "Read-only resident decisions. Neighbourhood, Resident Engagement and Retrofit coordination staff record supplied answers.") : null,
    h("table", {}, h("thead", {}, h("tr", {}, ["Measure", "Their answer", "Versions"].map((x) => h("th", {}, x)))),
      h("tbody", {}, measures.map((m) => h("tr", {}, h("td", {}, `${m.measure}: ${m.context ? `scope ${m.context.scope}, revision ${m.context.revision}, design ${m.context.design_version}` : "Current scope not recorded"}`), h("td", {}, `${m.status}. ${m.readiness}`),
        h("td", {}, m.versions.map((v) => `v${v.version} ${v.status} (${v.answered_by}, recorded by ${v.recorded_by}${v.note ? `: ${v.note}` : ""})`).join("; ") || "None"))))),
    recordForm("Record the measure scope", [["measure", "Measure", { options: ["", ...measures.map((m) => m.measure)] }], ["scope", "Exact scope reference"], ["design_version", "Current technical design version", { type: "number" }], ["source", "Supplied scope source reference"]], (b) => go("scope_record", b), "Record scope"),
    recordForm("Record what the resident said", [["measure", "Measure", { options: ["", ...measures.map((m) => m.measure)] }], ["context_revision", "Current scope revision", { type: "number" }], ["status", "Their supplied answer", { options: ["", "Waiting", "Accepted", "Declined", "Paused", "Withdrawn"] }], ["answered_by", "Who said it", { options: ["", "The resident", "Their representative"] }], ["source", "Supplied answer source reference"], ["representative_ref", "Reference for the representative, if any"], ["review_ref", "Human review evidence if restarting after a pause or withdrawal"], ["note", "In their words (needed for declined, paused or withdrawn)"]], (b) => go("decision_record", b), "Save supplied answer"),
    h("h3", {}, "Representative authority"),
    h("p", { class: "muted" }, "A person confirms authority with the resident. Scheduling or interpreting is not authority for works consent. A changed safe contact, expired, disputed or unclear authority stops representative steps. Nothing is sent here. Retention is five years from first recorded resident contact, including withdrawn or expired records."),
    recordForm("Confirm the safe contact reference", [["safe_contact_ref", "Resident-confirmed safe contact reference"], ["source", "Supplied confirmation source"]], (b) => go("safe_contact_record", b), "Record confirmation"),
    recordForm("Record representative authority", [["measure", "Measure", { options: ["", ...measures.map((m) => m.measure)] }], ["context_revision", "Current scope revision", { type: "number" }], ["representative_ref", "Representative reference"], ["status", "Authority status", { options: ["", "Confirmed", "Unclear", "Disputed", "Revoked"] }], ["task", "Evidenced task", { options: ["", "Receive information", "Communicate", "Attend", "Works decision"] }], ["authority_date", "Authority evidence date", { type: "date" }], ["review_date", "Review due date (authority held from this date)", { type: "date" }], ["safe_contact_ref", "Current safe contact reference"], ["source", "Authority evidence reference"], ["resident_wishes", "Resident's own stated wishes"]],
      (b) => go("representative_record", Object.assign({}, b, { tasks: [b.task] })), "Record authority version"),
    recordForm("Check a representative task", [["measure", "Measure", { options: ["", ...measures.map((m) => m.measure)] }], ["context_revision", "Current scope revision", { type: "number" }], ["representative_ref", "Representative reference"], ["task", "Task", { options: ["", "Receive information", "Communicate", "Attend", "Works decision"] }]], (b) => go("disclosure_check", b), "Check only; nothing sent"),
    h("h2", {}, "Resident-update commitment"),
    h("p", {}, "A commitment is not a message. Nothing is sent or marked received here. Handoffs do not clear or reassign it."),
    update ? h("p", {}, `${update.status || "Unknown"}: ${update.purpose || "Unknown purpose"}. Owner: ${named(update.owner_identity)}. Due: ${stamp(update.due_at)}. Basis: ${update.basis || "Unknown"}. Safe route reference: ${update.safe_contact_ref || "Unknown"}. Status date: ${stamp(update.at)}. Original date: ${stamp(update.opened_at)}. Version ${update.version || 0}.`) : h("p", {}, "No commitment recorded."),
    residentForm("ru-record", "Record or reassign update commitment", [
      ["purpose", "Update purpose or linked issue"], ["owner", "Named update owner", who],
      ["due_at", "Human-selected due date"], ["basis", "Basis for the due date"],
      ["safe_contact_ref", "Safe contact reference (blank means Unknown)"],
      ["status", "Commitment status", ["Outstanding", "Proposed"]]
    ], "update_record", (body) => ({ ...body, expected_version: update?.version || 0,
      due_at: body.due_at ? new Date(body.due_at).toISOString() : "" })),
    h("h2", {}, "Service requests and complaints"),
    h("p", {}, "Response closure is separate from remedy completion, defects, charge queries, package completion, handover and finance."),
    reqs.length ? reqs.map((r) => h("div", {}, h("strong", {}, `${r.id}: ${r.route}. ${r.status}.`),
      h("div", { class: "muted" }, `${r.summary || "Unknown"}. They want: ${r.desired_outcome || "Unknown"}. Dealt with by ${r.service_owner}. Redress owner: ${r.redress_owner}. Contact needs: ${(r.accessibility || ["Unknown"]).join(", ")}. Representative: ${r.representative_ref || "Unknown"}. Next update ${r.next_update || "Unknown"}.`),
      h("p", {}, `Response: ${r.status}. Owner: ${named(r.status_owner)}. Status date: ${stamp(r.status_at)}. Original date: ${stamp(r.opened_at)}.`),
      h("p", {}, `Remedy: ${r.remedy?.status || "Unknown"}. Owner: ${named(r.remedy?.owner)}. Status date: ${stamp(r.remedy?.at)}. Original date: ${stamp(r.remedy?.opened_at)}. Age band: Unknown (Housing/Complaints have not configured bands).`),
      r.remedy?.version ? residentForm(`remedy-${r.id}`, `Record remedy progress for ${r.id}`, [
        ["status", "Remedy status", ["Open", "In progress", "Resolved", "Closed"]],
        ["owner", "Reassign remedy owner (blank keeps current owner)", ["", ...who]],
        ["note", "Supplied progress or reopening evidence"]
      ], "remedy_update", (body) => ({ ...body, id: r.id, expected_version: r.remedy.version }))
        : residentForm(`remedy-${r.id}`, `Confirm legacy remedy responsibility for ${r.id}`, [
          ["owner", "Named remedy owner", who], ["basis", "Supplied responsibility basis"]
        ], "remedy_confirm", (body) => ({ ...body, id: r.id, expected_version: 0 })),
      r.status === "Closed" ? residentForm(`response-${r.id}`, `Reopen response for ${r.id}`, [
        ["note", "Why the response is reopened"]
      ], "service_reopen", (body) => ({ ...body, id: r.id, expected_version: r.version || 0 })) : null
    )) : h("p", { class: "muted" }, "No requests recorded."),
    serviceForm("request-open", "Open a request or complaint", [["route", "Type", { options: ["Service request", "Complaint", "Repair", "Defect", "Hazard", "Charge query", "Household dispute"] }], ["summary", "Short summary"], ["desired_outcome", "What the resident wants"], ["service_owner", "Who deals with it", { options: who }], ["redress_owner", "Who owns the redress", { options: who }], ["accessibility", "Contact need", { options: ["Unknown", "None", "Large print", "Phone only", "Plain language", "Interpreter", "Representative contact", "Safe route needed"] }], ["next_update", "Next update date", { type: "date" }]],
      "service_open", (b) => ({ ...b, accessibility: [b.accessibility] }), "Open"),
    h("p", { class: "muted" }, "Ask your named officer for independent human review or the association's formal complaints route, including by phone or an accessible non-digital route. Recording a request here does not send it to a live complaints service, change works choices, stop urgent repairs or sanction future engagement."),
    serviceForm("review-open", "Request independent human review", [["review_measure", "Contested measure", { options: ["", ...measures.map((m) => m.measure)] }], ["review_decision_version", "Contested decision version", { type: "number" }], ["review_reference", "Review evidence reference"], ["summary", "Short summary"], ["desired_outcome", "What the resident wants"], ["service_owner", "Request handler", { options: who }], ["redress_owner", "Independent reviewer", { options: who }], ["next_update", "Next update date", { type: "date" }]], "service_open", (b) => ({ ...b, route: "Independent review", review_decision_version: Number(b.review_decision_version) }), "Record review request"),
    reqs.length ? [
      serviceForm("request-update", "Update a request", [["id", "Request", { options: reqs.map((r) => r.id) }], ["status", "Status", { options: ["Open", "In progress", "Resolved"] }], ["next_update", "Next update date", { type: "date" }], ["note", "Note"]], "service_update", (b) => b, "Save update"),
      serviceForm("request-close", "Close a request response", [["id", "Request", { options: reqs.map((r) => r.id) }], ["note", "Response outcome (remedy stays separate)"]], "service_close", (b) => b, "Close response"),
    ] : null);
}

async function financeQueueView() {
  let rows;
  try { rows = await api("/api/finance"); } catch (e) { if (e.name === "AbortError" || !me) return; return show(h("h1", {}, "Finance queue"), h("p", {}, e.message)); }
  show(h("h1", {}, "Finance queue"),
    h("p", { class: "muted" }, "Invoices with exceptions, paused payments or no check yet. A person decides each one. Nothing is paid from here."),
    rows.length ? h("table", {}, h("thead", {}, h("tr", {}, ["Home", "Invoice", "Supplier", "Status", "Exceptions", "Total"].map((x) => h("th", {}, x)))),
      h("tbody", {}, rows.map((r) => h("tr", {}, h("td", {}, h("a", { href: `#/case/${encodeURIComponent(r.case_id)}` }, r.address)), h("td", {}, `${r.invoice} ${r.ref}`),
        h("td", {}, r.supplier), h("td", {}, r.on_hold ? `${r.status}, payment paused` : r.status), h("td", {}, r.exceptions), h("td", {}, money(r.total)))))) : h("p", {}, "Nothing is waiting."));
}
