"use strict";

const roleScreens = new Map();
const screenManagers = ["Retrofit Programme Manager", "Programme Support Officer"];
const screenValue = (value) => value === null || value === undefined || value === "" ? "Unknown" : String(value);
const screenPerson = (value) => typeof value === "string" ? screenValue(value) : screenValue(value?.name);
const screenStamp = (value) => {
  const date = value ? new Date(value) : null;
  return date && !Number.isNaN(date.getTime())
    ? new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "short" }).format(date)
    : "Unknown";
};
const screenFields = (rows) => h("dl", {}, rows.flatMap(([label, value]) => [
  h("dt", {}, label), h("dd", {}, screenValue(value))
]));
const screenPanel = (title, ...children) => h("section", { class: "card screen-record" },
  h("h2", {}, title), ...children);
const screenUnknown = (reason, owner, action) => h("div", { class: "blocked" },
  h("p", { class: "blocked-title" }, "Cannot confirm readiness"),
  screenFields([["Why it is blocked", reason], ["Owner", owner], ["Next action", action]]));
function screenTable(label, headings, rows) {
  return h("div", {},
    rows.length > 50 && h("p", { role: "status" }, `Showing the first 50 of ${rows.length} records. Open the case workspace to inspect the remaining evidence. This is not a complete readiness check.`),
    rows.length ? h("div", { class: "table-scroll", role: "region", "aria-label": label, tabindex: 0 },
      h("table", {}, h("caption", {}, label),
        h("thead", {}, h("tr", {}, headings.map((title) => h("th", { scope: "col" }, title)))),
        h("tbody", {}, rows.slice(0, 50).map((row) => h("tr", {}, row.map((value) => h("td", {}, screenValue(value))))))))
      : h("p", { class: "empty" }, "No records supplied. This does not establish readiness."));
}
function registerRoleScreen(screen) {
  if (roleScreens.has(screen.id)) throw new Error(`Duplicate specialist screen: ${screen.id}`);
  roleScreens.set(screen.id, screen);
}
function screenHref(id, caseId, page = 0) {
  const query = new URLSearchParams();
  if (id) query.set("screen", id);
  if (caseId) query.set("case", caseId);
  if (page) query.set("page", String(page));
  return `#/screens${query.size ? `?${query}` : ""}`;
}
async function roleScreensView() {
  const signal = routeController.signal;
  const query = new URLSearchParams(location.hash.split("?")[1] || "");
  const id = query.get("screen");
  const caseId = query.get("case");
  const rawPage = query.get("page") || "0";
  const page = Number(rawPage);
  const installed = [...roleScreens.values()].filter((screen) => screen.roles.includes(me.user.role));
  const screen = installed.find((item) => item.id === id);
  if (!/^\d+$/.test(rawPage) || !Number.isSafeInteger(page) || page > 100000) {
    return show(h("h1", {}, "Invalid screen page"), h("p", { role: "alert" }, "Choose a page from the queue."),
      h("a", { href: screenHref(id, caseId) }, "Reset screen view"));
  }
  if (id && !screen) {
    return show(h("h1", {}, "Screen unavailable"),
      h("p", { role: "alert" }, "This screen is not installed for your signed-in role. Your access has not changed."),
      h("a", { href: "#/screens" }, "Back to specialist screens"));
  }
  const menu = h("nav", { "aria-label": "Specialist screens", class: "screen-links" },
    installed.map((item) => h("a", { href: screenHref(item.id, caseId),
      "aria-current": item.id === id ? "page" : null }, item.title)));
  if (!screen) {
    return show(h("h1", {}, "Specialist screens"), menu,
      h("p", {}, installed.length
        ? "Choose a screen. Select a home explicitly; no case is selected automatically."
        : "No specialist screens are installed for your role on this branch. Use your existing work list."),
      h("a", { href: "#/" }, "Back to my work"));
  }
  show(h("h1", {}, screen.title), h("p", { role: "status", "aria-busy": "true" }, "Loading recorded evidence."));
  const data = await api(`/api/cases?view=all&limit=20&offset=${page * 20}`, undefined, signal);
  const c = caseId ? await api(`/api/cases/${encodeURIComponent(caseId)}`, undefined, signal) : null;
  const extra = c && screen.load ? await screen.load(c) : null;
  signal.throwIfAborted();
  const label = (row) => `${row.id}: ${row.address || "Address unknown"}. ${row.status || row.stage || "State unknown"}`;
  const queue = h("section", { "aria-labelledby": "screen-queue-heading" },
    h("h2", { id: "screen-queue-heading" }, "Choose a home"),
    h("p", {}, "All cases permitted to your signed-in role, including safety concerns. This is a bounded page, not a portfolio total."),
    h("p", { role: "status" }, `${data.items.length} records on page ${page + 1}; ${data.total} permitted cases.`),
    data.items.length ? h("ul", { class: "list" }, data.items.map((row) => h("li", {},
      h("a", { class: "item", href: screenHref(id, row.id, page),
        "aria-current": row.id === caseId ? "true" : null },
        h("div", {}, label(row),
          row.hazard && h("span", { class: "flag danger" }, "Safety issue open"),
          row.work && workSummary(row.work))))))
      : h("p", { class: "empty" }, "No cases on this page. Reset the view or return to your work list."),
    h("div", { class: "row" },
      page > 0 && h("a", { class: "btn alt", href: screenHref(id, caseId, page - 1) }, "Previous page"),
      (page + 1) * 20 < data.total && h("a", { class: "btn alt", href: screenHref(id, caseId, page + 1) }, "Next page"),
      h("a", { class: "btn alt", href: screenHref(id) }, "Reset screen view")));
  const selected = c ? h("section", { class: "screen-evidence", "aria-label": `Evidence for ${c.id}` },
    h("h2", {}, `Selected home ${c.id}`),
    h("p", {}, "Recorded evidence only. Missing, stale or withheld information cannot establish readiness. No message, approval or record change is made from this screen."),
    await screen.render(c, extra),
    h("p", {}, h("a", { href: `#/case/${encodeURIComponent(c.id)}` }, "Open existing case workspace")))
    : h("p", { class: "empty" }, "No home selected. Choose a home from this queue.");
  signal.throwIfAborted();
  workspaceStatus.textContent = `${me.user.role}. ${screen.title}. ${c ? `Selected home ${c.id}.` : "No home selected."}`;
  show(h("h1", {}, screen.title), menu,
    h("div", { class: "layout" }, h("aside", { class: "side" }, queue),
      h("div", { class: "main" }, selected)),
    h("a", { href: "#/" }, "Back to my work"));
}

const assetDate = (iso) => {
  const text = String(iso ?? "");
  const basic = /^(\d{4})(\d{2})(\d{2})$/.exec(text);
  if (basic) return Date.parse(`${basic[1]}-${basic[2]}-${basic[3]}T00:00:00Z`);
  const week = /^(\d{4})-?W(\d{2})(?:-?([1-7]))?$/.exec(text);
  if (week) {
    const jan4 = Date.UTC(+week[1], 0, 4);
    const monday = jan4 - ((new Date(jan4).getUTCDay() + 6) % 7) * 86400000;
    return monday + ((+week[2] - 1) * 7 + (+(week[3] || 1) - 1)) * 86400000;
  }
  return Date.parse(text);
};
const assetAgeDays = (iso) => {
  const then = iso ? assetDate(iso) : NaN;
  return Number.isNaN(then) ? "Unknown" : `${Math.max(0, Math.floor((Date.now() - then) / 86400000))} days old`;
};
const assetStatus = (c, q) => {
  const event = (c.stock_reconciliation_events || []).filter((e) => e.query_id === q.id).at(-1);
  return event ? `${event.status} (recorded by a named person)` : "Unresolved";
};
const assetInputs = [
  ["Capital budget", "Finance owner to name the budget source"],
  ["Investment priority", "Asset owner to name the priority basis"],
  ["Cost forecast", "Finance owner to supply a dated forecast"],
  ["Benefit baseline", "Programme owner to supply a measured baseline"],
  ["Phase gate evidence", "Programme manager to name the gate evidence"]
];
function assetCost(report) {
  const m = report?.consumption;
  const passed = m && m.quality_status === "Pass" && m.quality_qualified_cost && m.quality_qualified_cost !== "Unknown";
  return screenFields([
    ["Overall AI cost per accepted outcome", "Unknown. Other cost components are not complete and quality-qualified."],
    ["Token/API component per accepted proposal (component only)", passed ? `${m.quality_qualified_cost} ${screenValue(m.currency)}` : "Unknown"],
    ["Report period (UTC)", m?.period ? `${screenValue(m.period.start)} to ${screenValue(m.period.end)}, as of ${screenValue(m.period.as_of)}` : "Unknown"],
    ["Accepted-outcome denominator", screenValue(m?.denominator)],
    ["Quality floor", screenValue(m?.quality_status)],
    ["Value status", m?.cash_value && m.cash_value !== "Unknown" ? m.cash_value : "Unknown. No finance-defensible value is recorded."],
    ["Evidence class", screenValue(m?.evidence_label || m?.coverage)],
    ["Coverage", screenValue(m?.coverage)],
    ["Reading", "A token count is never shown as the cost of AI. Without a recorded price source and a passed quality floor, cost stays Unknown."]
  ]);
}
registerRoleScreen({
  id: "asset-board",
  title: "Asset and board view",
  roles: screenManagers,
  async load() {
    const signal = routeController.signal;
    const portfolio = await api("/api/cases?view=all&limit=1&offset=0", undefined, signal);
    const report = await api("/api/ai/report", undefined, signal).catch(() => null);
    return { portfolio, report };
  },
  render(c, extra) {
    const queries = c.stock_reconciliation || [];
    const owner = queries.find((q) => assetStatus(c, q) === "Unresolved")?.query_owner;
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view. It records no investment approval and changes no record. Budgets, priorities, forecasts and eligibility are Unknown unless a constructed fixture says so, and this page cannot confirm them. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Stock conflict comparison",
        screenTable("Stock source conflicts and source age",
          ["Query", "Field", "First source (value, ID, version, age)", "Compared source (value, ID, version, age)", "Status", "Resolution owner"],
          queries.map((q) => [q.id, q.field,
            `${q.left.value}, ${q.left.source_id} v${q.left.version}, ${assetAgeDays(q.left.date)}, ${q.left.validation_state}`,
            `${q.right.value}, ${q.right.source_id} v${q.right.version}, ${assetAgeDays(q.right.date)}, ${q.right.validation_state}`,
            assetStatus(c, q), screenPerson(q.query_owner)]))),
      screenPanel("Eligibility",
        screenFields([["Eligibility", "Unknown"],
          ["Resolution owner", owner ? screenPerson(owner) : "Unassigned. Programme manager to name an owner."],
          ["Next action", "Obtain source-authority review. Nothing here selects a winning source."]])),
      screenPanel("Missing investment inputs",
        screenTable("Investment inputs", ["Input", "State", "Resolution owner and action"],
          assetInputs.map(([name, action]) => [name, "Unknown", action]))),
      screenPanel("Benefits and phase gate",
        screenUnknown("No measured benefit or gate evidence is supplied for this home.", "Programme manager to name an owner", "Supply dated evidence before any gate is read as passed")),
      screenPanel("Portfolio scope (separate from this home)",
        screenFields([["Cases permitted to your role", extra?.portfolio?.total],
          ["Meaning", "A role-scoped count, not a stock, budget or programme total"]])),
      screenPanel("Ledger-wide AI cohort (all homes, not this home)", assetCost(extra?.report)));
  }
});

const financeRoles = ["Grants and Evidence Officer", ...screenManagers];
const financeMoney = (value) => typeof value === "number" && Number.isFinite(value)
  ? new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(value) : "Unknown";
const financeQty = (value) => typeof value === "number" && Number.isFinite(value) ? String(value) : "Unknown";
const financeChecked = (inv) => inv.status && inv.status !== "Received" && inv.status !== "Not checked";
function financeLineRows(f, inv) {
  const com = (f.commitments || []).find((m) => m.id === inv.commitment);
  const budget = f.budget;
  const budgetText = budget ? `${financeMoney(budget.amount)}, ${screenValue(budget.status)}` : "Unknown. No budget recorded.";
  const checked = financeChecked(inv);
  return (inv.lines || []).map((ln, i) => {
    const found = (inv.exceptions || []).filter((e) => e.line === i || e.line === null || e.line === undefined);
    const scope = !com ? "Unknown. No matched commitment."
      : String(com.measure).trim().toLowerCase() === String(ln.measure).trim().toLowerCase() ? "In scope" : `Not in scope (authorised: ${com.measure})`;
    const quantity = !com ? "Unknown. No matched commitment."
      : ln.quantity > com.quantity ? `Above authorised (${financeQty(ln.quantity)} of ${financeQty(com.quantity)})`
        : `Within authorised (${financeQty(ln.quantity)} of ${financeQty(com.quantity)})`;
    return [`Line ${i + 1}: ${screenValue(ln.measure)}`, `${financeQty(ln.quantity)} at ${financeMoney(ln.amount)}`,
      com ? `${com.id} (${screenValue(com.status)}), ${financeMoney(com.amount)}` : "Unknown. Not matched.",
      scope, quantity, budgetText,
      ln.milestone_ref ? `Reference ${ln.milestone_ref}` : "Unknown. No accepted milestone evidence.",
      !checked ? "Not checked yet. Exceptions are unknown."
        : found.length ? found.map((e) => e.message).join(" ") : "No exception found by the match. This is not a payment decision."];
  });
}
function financeInvoicePanel(c) {
  const f = c.finance || {};
  const invoices = f.invoices || [];
  if (!invoices.length) return screenPanel("Invoice line comparison",
    h("p", { class: "empty" }, "No invoices recorded for this home. This does not establish that nothing is owed."));
  return screenPanel("Invoice line comparison", ...invoices.map((inv) => h("div", {},
    h("h3", {}, `${inv.id}: ${screenValue(inv.kind)} ${screenValue(inv.ref)} from ${screenValue(inv.supplier)}`),
    screenFields([["Version and record", `${inv.id}, work order ${screenValue(inv.work_order)}, match status: ${screenValue(inv.status)}`],
      ["Payment hold", inv.hold ? `Paused by ${screenValue(inv.hold.name)}: ${screenValue(inv.hold.reason)}` : "No hold recorded"],
      ["Finance decision", inv.disposition ? `${inv.disposition}, recorded by ${screenValue(inv.disposition_by)}` : "No Finance decision recorded"],
      ["Payment status (a note of what Finance did elsewhere)", `${screenValue(inv.payment_status)}. This system never makes or releases a payment.`]]),
    screenTable(`Line comparison for ${inv.id}`,
      ["Invoice line", "Quantity and amount", "Commitment", "Scope", "Quantity check", "Budget", "Accepted milestone evidence", "Exception or unknown"],
      financeLineRows(f, inv)))));
}
const financeQueueRows = (queue) => queue.map((q) => [q.case_id, q.invoice, `${screenValue(q.supplier)}, ref ${screenValue(q.ref)}`,
  screenValue(q.status), `${q.exceptions ?? "Unknown"} exceptions`, q.on_hold ? "On hold" : "No hold", financeMoney(q.total)]);
registerRoleScreen({
  id: "finance-invoices",
  title: "Invoice queue",
  roles: financeRoles,
  async load() {
    const signal = routeController.signal;
    const queue = await api("/api/finance", undefined, signal).catch(() => null);
    const report = await api("/api/ai/report", undefined, signal).catch(() => null);
    return { queue, report };
  },
  render(c, extra) {
    const queue = Array.isArray(extra?.queue) ? extra.queue : null;
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view for the approver and payment officer. It makes no payment, approval or decision and changes no record. Use the existing case workspace to act. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only, except the queue below.`)),
      screenPanel("Invoices waiting for Finance (all homes your role can see)",
        queue ? screenTable("Invoices with exceptions, holds or not yet checked",
          ["Home", "Invoice", "Supplier and reference", "Status", "Exceptions", "Hold", "Invoice total"], financeQueueRows(queue))
          : h("p", { class: "empty" }, "Unknown. The queue could not be read for your role.")),
      financeInvoicePanel(c),
      screenPanel("AI economics (ledger-wide, all homes)", h("p", {}, "Design only. Usage must be reconciled to billing before any cost is read. Total Cost of AI is the sum of components, and any missing component keeps it Unknown. Booked-value status stays Unknown until Finance records a defensible value. No price, budget or target is set here (BRD OD-51 open)."),
        screenFields([["Usage reconciled to billing", "Unknown. No billing source is recorded."],
          ["Total Cost of AI components", "Unknown. Platform, licence, people and rework components are not supplied."]]),
        assetCost(extra?.report)));
  }
});

const fundingFieldRows = (draft) => Object.entries(draft.fields || {}).map(([id, row]) => {
  const issue = (draft.issues || []).filter((i) => i.field_id === id);
  const source = row.evidence?.source;
  return [id, row.effective_state || row.state, row.value === null || row.value === undefined ? "Unknown. No confirmed value." : JSON.stringify(row.value),
    source ? `${screenValue(source.id)} v${screenValue(source.version)} (${screenValue(source.kind)})` : "Unknown. No reviewed evidence bound.",
    issue.length ? issue.map((i) => `${i.status}: ${i.reason}`).join(" ") : "None recorded"];
});
function fundingDraftPanel(draft) {
  if (draft.status === "Unavailable") return screenPanel(`Field draft ${screenValue(draft.draft_id)}`,
    screenUnknown(draft.notice, "Document owner", "Recover the source document before reading this draft"));
  const conflicts = (draft.issues || []).filter((i) => i.status === "Conflict");
  return screenPanel(`Constructed field draft ${screenValue(draft.draft_id)}`,
    screenFields([["Template", `${screenValue(draft.template?.id ?? draft.template?.name ?? draft.schema_id)} (schema ${screenValue(draft.schema_id)} v${screenValue(draft.schema_version)})`],
      ["Funding route", draft.funding?.route ?? draft.funding?.scheme ?? "Unknown"],
      ["Rule references", (draft.rule_refs || []).length ? draft.rule_refs.map((r) => (typeof r === "string" ? r : r.id)).join(", ") : "Unknown. None supplied."],
      ["Conflicting source candidates", conflicts.length ? `${conflicts.length} field${conflicts.length === 1 ? "" : "s"}: ${conflicts.map((i) => i.field_id).join(", ")}. A person must review them. Nothing here picks a winning source.` : "None recorded"],
      ["Stale fields", (draft.stale_fields || []).length ? draft.stale_fields.join(", ") : "None recorded"],
      ["Reviewed ready", draft.reviewed_ready ? "Yes, as recorded by the reviewer" : "No. Held until a person reviews the evidence."],
      ["Approved rule validation", screenValue(draft.approved_rule_validation)],
      ["Unit and currency verification", screenValue(draft.unit_currency_verification)]]),
    screenTable(`Fields and reviewed evidence for ${draft.draft_id}`,
      ["Field", "State", "Value", "Reviewed evidence", "Issues"], fundingFieldRows(draft)),
    h("p", {}, screenValue(draft.notice)));
}
registerRoleScreen({
  id: "finance-funding",
  title: "Funding route and claim pack",
  roles: financeRoles,
  async load(c) {
    const signal = routeController.signal;
    const review = await api(`/api/cases/${encodeURIComponent(c.id)}/form-review`, undefined, signal).catch(() => null);
    const report = await api("/api/ai/report", undefined, signal).catch(() => null);
    return { review, report };
  },
  render(c, extra) {
    const funding = c.funding || {};
    const grants = c.grants || [];
    const drafts = Array.isArray(extra?.review?.drafts) ? extra.review.drafts : null;
    const holds = extra?.review?.decision_holds || [];
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view for the capital and grant preparer. It is a reviewed export or readiness view only. No submission, award, eligibility decision or payment is made or inferred. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Funding route",
        screenFields([["Route", funding.route], ["Status", funding.status], ["Reference", funding.reference],
          ["Eligibility", "Unknown. This page cannot confirm eligibility."]])),
      screenPanel("Grant stages",
        grants.length ? screenTable("Grant stages and approved evidence", ["Grant", "Scheme", "Stage now", "Waiting for approval", "Approved evidence"],
          grants.map((g) => [g.id, g.scheme, g.state,
            g.pending ? `${g.pending.to}, proposed by ${screenValue(g.pending.name)}. Evidence: ${screenValue(g.pending.source)}` : "Nothing waiting",
            (g.history || []).length ? g.history.map((x) => `${x.state}: ${screenValue(x.source)} (approved by ${screenValue(x.approved_by)}, ${screenValue(x.source_status)})`).join("; ") : "Unknown. No approved stage."]))
          : h("p", { class: "empty" }, "No grant recorded. This does not establish that no funding is available.")),
      drafts ? (drafts.length ? drafts.map(fundingDraftPanel)
        : screenPanel("Constructed field draft", h("p", { class: "empty" }, "No field draft recorded for this home. Template, fields and evidence are Unknown.")))
        : screenPanel("Constructed field draft", h("p", { class: "empty" }, "Unknown. The field review could not be read for your role.")),
      screenPanel("Readiness export",
        screenFields([["Claim pack readiness", drafts && drafts.some((d) => d.reviewed_ready) ? "A reviewer recorded ready on at least one draft. A person must still check and submit it outside this system." : "Not ready. No reviewed export exists."],
          ["Open decision holds", holds.length ? `${holds.length} recorded` : "None recorded"],
          ["Submission, award and payment", "Not recorded here. This screen never infers them."]])),
      screenPanel("AI economics (ledger-wide, all homes)", assetCost(extra?.report)));
  }
});
