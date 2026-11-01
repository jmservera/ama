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

const reviewerRole = "Contracts manager, independent of the person who issued or submitted the pack";
const wording = (value, fallback = "Unknown") => value === null || value === undefined || value === "" ? fallback : String(value);
const reference = (order) => `${wording(order.id)} v${wording(order.version)}`;
function packagePrerequisites(pkg, orders) {
  const capacity = pkg.capacity || [];
  const evidenced = capacity.length && capacity.every((row) => String(row.evidence_status || "").startsWith("Evidenced"));
  const active = orders.filter((order) => order.state !== "Withdrawn");
  const current = active.filter((order) => order.scope_version === pkg.scope_version);
  const bound = current.length && current.every((order) => !String(order.measures || "").startsWith("Unknown"));
  const binding = !orders.length ? "Unmet. No work order for this home."
    : !active.length ? "Unmet. Every work order for this home is withdrawn."
    : active.some((order) => order.scope_version === undefined || order.scope_version === null) ? "Unknown. Work-order scope version not supplied."
    : current.length !== active.length ? "Unmet. A work order is tied to an older package scope."
    : bound ? "Met on record" : "Unmet. Resident scope confirmation needed.";
  return [
    ["Scope recorded with a version", pkg.scope && pkg.scope_version ? `Met on record (scope v${pkg.scope_version})` : "Unmet", "Programme manager"],
    ["Contract or call-off reference recorded", pkg.contract_ref ? `Met on record (${pkg.contract_ref} v${wording(pkg.contract_version)})` : "Unmet", "Contracts manager"],
    ["Committed capacity evidenced for every contractor", evidenced ? "Met on record" : "Unmet or Unknown", "Contracts manager"],
    ["Consultation status confirmed", pkg.consultation_status === "complete" || pkg.consultation_status === "not_applicable" ? "Met on record" : "Unmet. Status is Unknown or applies.", "Legal or procurement authority"],
    ["Work order issued for the selected home with resident scope", binding, "Contracts manager"]
  ];
}
registerRoleScreen({
  id: "procurement-packages",
  title: "Package queue",
  roles: screenManagers,
  async load(c) {
    const signal = routeController.signal;
    const packages = await api("/api/packages", undefined, signal);
    const orders = await api(`/api/workorders?case=${encodeURIComponent(c.id)}`, undefined, signal);
    return { packages, orders };
  },
  render(c, extra) {
    const packages = extra?.packages || [];
    const orders = extra?.orders || [];
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view. It records no approval, issues no work order and books no visit. Readiness here is a draft only. Contract terms, capacity and delegations are Unknown unless a fixture or recorded evidence says so. Source: desk research, not observed behaviour."),
        h("p", {}, `Work orders shown are for home ${c.id} only.`)),
      screenPanel("Package queue",
        screenTable("Packages with period, scope, version and capacity",
          ["Package", "Period", "Scope and version", "Contract or call-off reference", "Contractor", "Offered", "Recorded committed", "In use", "Recorded headroom", "Capacity evidence status"],
          packages.flatMap((p) => (p.capacity?.length ? p.capacity : [{}]).map((cap) => [
            `${wording(p.id)}: ${wording(p.name)}`, `${wording(p.period_from)} to ${wording(p.period_to)}`,
            `${wording(p.scope)} (v${wording(p.scope_version)})`, `${wording(p.contract_ref)} v${wording(p.contract_version)}`,
            cap.contractor, cap.offered, cap.committed, cap.in_use, cap.headroom, wording(cap.evidence_status)])))),
      screenPanel("Work orders for this home",
        screenTable("Work-order references for the selected home",
          ["Work order", "Package", "Contractor", "State", "Scope"],
          orders.map((o) => [reference(o), o.package, o.contractor, o.state, o.scope]))),
      ...packages.map((p) => screenPanel(`Draft readiness: ${wording(p.id)}`,
        h("p", { role: "status" }, "Draft readiness only. This is not a release or approval."),
        screenTable(`Unmet prerequisites for ${wording(p.id)}`, ["Prerequisite", "State", "Next reviewer (role)"],
          packagePrerequisites(p, orders.filter((o) => o.package === p.id))),
        screenFields([["Next reviewer", reviewerRole], ["Named reviewer", "Unassigned. Contracts manager to name a person."]]))),
      screenPanel("Contractor submission and review",
        screenFields([["Contractor submission", "Recorded outside this screen; not shown here"],
          ["Acknowledgement", "A contractor acknowledgement is not acceptance"],
          ["Independent review and acceptance", "Separate step by a named reviewer; not available from this screen"]])));
  }
});

const jobPackChecklist = [
  "Resident notice or access arrangement confirmed",
  "Appointment outcome recorded",
  "Measures installed match the work-order scope",
  "Completion photographs",
  "Deviations from scope noted",
  "Handover documents and guarantees"
];
registerRoleScreen({
  id: "contractor-job-pack",
  title: "Job pack and evidence checklist",
  roles: ["Contractor"],
  async load(c) {
    return { orders: await api(`/api/workorders?case=${encodeURIComponent(c.id)}`, undefined, routeController.signal) };
  },
  render(c, extra) {
    const orders = extra?.orders || [];
    return h("div", {},
      screenPanel("What this screen does",
        h("p", {}, "Read-only job pack view. Nothing is submitted, accepted or booked from here, and it is not a provider portal. To submit or correct evidence, send it to your named contact."),
        h("p", {}, "Source: desk research hypothesis, not observed behaviour.")),
      screenPanel("Your job pack",
        screenTable("Your work orders for this home", ["Work order and version", "State", "Works", "Scope"],
          orders.map((o) => [reference(o), o.state, o.measures, o.scope])),
        screenFields([["Notice before visit", c.needs_notice ? "Needs notice" : "No extra notice needed"],
          ["Named contact", c.named_contact]]),
        h("p", {}, "The reason for any notice is not shared with contractors.")),
      screenPanel("Evidence checklist",
        screenTable("Evidence checklist for this job pack", ["Evidence item", "State on record"],
          jobPackChecklist.map((item) => [item, item === "Appointment outcome recorded" && orders.some((o) => (o.appointments || []).length)
            ? "Recorded on a work order" : "Unknown. Not assessed on this screen."]))),
      screenPanel("Submission and review are separate",
        screenFields([["Your submission", "Not recorded on this screen"],
          ["Acknowledgement", "Not recorded. An acknowledgement is not acceptance."],
          ["Independent review and acceptance", "Unknown. Review data is not available here. Done by someone other than you."],
          ["Next reviewer", reviewerRole]])));
  }
});
