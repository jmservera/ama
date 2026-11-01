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
  const overview = screen.overview ? await screen.overview(signal) : null;
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
      h("div", { class: "main" }, overview, selected)),
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

const programmeScopes = [
  ["default", "Returned and handed-off work (default)"],
  ["returned", "Returned work only"],
  ["handoff", "Pending handoffs only"],
  ["blocked", "Blocked work"],
  ["all", "All permitted cases on this page"]
];
const programmeIn = (row, scope) => {
  const work = row.work || {};
  const queues = work.queues || [];
  if (scope === "returned") return Boolean(work.returned);
  if (scope === "handoff") return queues.includes("unowned");
  if (scope === "blocked") return queues.includes("blocked");
  if (scope === "all") return true;
  return Boolean(work.returned) || queues.includes("unowned");
};
const programmeRow = (row) => {
  const work = row.work || {};
  const sent = work.handoff?.sender;
  return [
    `${row.id}: ${row.address || "Address unknown"}`,
    work.returned ? work.returned.reason : work.handoff ? "Not returned. Pending handoff." : "Not returned",
    work.returned ? work.returned.sender : sent,
    work.owner,
    work.handoff ? work.handoff.proposed_receiver : "No handoff proposed",
    work.handoff ? work.handoff.chase_owner : "No handoff recorded",
    work.handoff ? work.handoff.resident_update_owner : "No handoff recorded"
  ];
};
const programmeHeadings = ["Home", "Return reason", "Sender", "Current owner",
  "Proposed receiver (not a confirmed owner)", "Chase owner (chases the receiver)",
  "Resident-update owner (updates the resident)"];
function programmeQueue(items, total) {
  const holder = h("div", {});
  const status = h("p", { role: "status", id: "programme-filter-status" });
  const select = h("select", { id: "programme-scope", name: "scope" },
    programmeScopes.map(([value, text]) => h("option", { value }, text)));
  const apply = (scope) => {
    const rows = items.filter((row) => programmeIn(row, scope));
    status.textContent = `${rows.length} of ${items.length} records on this page shown. Scope: ${programmeScopes.find(([v]) => v === scope)[1]}. Filtering changes the view only; no record is changed.`;
    holder.replaceChildren(screenTable("Shared queue: returned and handed-off work", programmeHeadings, rows.map(programmeRow)));
  };
  if (select.value !== undefined) select.value = "default";
  apply("default");
  return h("div", {},
    h("p", {}, `${items.length} records on this page of ${total} permitted cases. Not a portfolio total.`),
    h("form", { class: "row", "aria-label": "Scope filter",
      onsubmit: (event) => { event?.preventDefault?.(); apply(select.value || "default"); } },
      h("label", { for: "programme-scope" }, "Scope"), select,
      h("button", { class: "btn", type: "submit" }, "Apply filter"),
      h("button", { class: "btn alt", type: "button",
        onclick: () => { select.value = "default"; apply("default"); } }, "Reset to default view")),
    status, holder);
}
const programmeFunnel = (report) => {
  const rows = report?.funnel;
  if (!Array.isArray(rows)) return h("p", { class: "empty" }, "Lifecycle and funnel counts are Unknown. No record was supplied.");
  return h("div", {},
    h("p", {}, `Recorded as of ${screenValue(report.as_of)}. Audit integrity: ${screenValue(report.audit_integrity)}. Conversion is Unknown; counts are stage history only.`),
    screenTable("Lifecycle and funnel by stage",
      ["Stage", "Entries", "Exits", "Returns", "Reopens", "Cases in scope"],
      rows.map((r) => [r.stage, r.entries, r.exits, r.returns, r.reopens, r.denominator])));
};
const programmeGate = (blockers, pattern) => blockers.filter((b) => pattern.test(b.step));
const programmeGateRow = (name, blocked, clear, unknown) => {
  if (blocked.length) return [name, "Blocked",
    blocked.map((b) => b.reason).join(" "), blocked[0].owner, blocked[0].next_action];
  if (unknown) return [name, "Blocked: evidence missing", unknown, "Unknown", "Record the missing evidence through the permitted review"];
  return [name, "No recorded blocker", `${clear} This is not a pass; a named person decides readiness.`, "Unknown", "Unknown"];
};
function programmeGates(c) {
  const blockers = c.work?.blockers || [];
  const booked = (c.appointments || []).find((a) => a.outcome === "Booked");
  const quality = c.quality || [];
  const returnedQuality = quality.filter((r) => r.state === "Returned");
  const budget = c.finance?.budget;
  return [
    programmeGateRow("Technical", programmeGate(blockers, /technical|Stock review/i),
      "No technical blocker is recorded.", c.technical ? null : "No technical record is supplied."),
    programmeGateRow("Resident", programmeGate(blockers, /resident/i),
      "No resident decision blocker is recorded.", null),
    programmeGateRow("Delivery", programmeGate(blockers, /Safety review|Shared building/i),
      booked ? `Visit booked for ${screenValue(booked.date)}.` : "", booked ? null : "No booked visit is recorded."),
    returnedQuality.length
      ? ["Quality", "Blocked", returnedQuality.map((r) => `${r.measure} returned for remediation.`).join(" "), "Unknown", "Record remediation evidence"]
      : programmeGateRow("Quality", [], quality.length ? "Quality checks are recorded." : "",
        quality.length ? null : "No quality check is recorded."),
    programmeGateRow("Finance", programmeGate(blockers, /funding/i),
      budget ? `Budget status: ${screenValue(budget.status)}.` : "",
      budget || c.funding_ok ? null : "No confirmed funding or budget is visible to your role.")
  ];
}
registerRoleScreen({
  id: "programme-queue",
  title: "Programme queue and connected home view",
  roles: [...screenManagers, "Retrofit Coordinator"],
  async overview(signal) {
    const page = await api("/api/cases?view=all&limit=50&offset=0", undefined, signal);
    const report = await api("/api/coordinator", undefined, signal).catch(() => null);
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only view of recorded work. Chase and update responsibility are shown separately. Nothing here sends, assigns or changes a record. Source: desk research, not observed behaviour; validation remains open.")),
      screenPanel("Shared queue", programmeQueue(page.items || [], page.total)),
      screenPanel("Lifecycle and funnel", programmeFunnel(report)));
  },
  render(c) {
    const rows = programmeGates(c);
    const blocked = rows.filter((r) => r[1].startsWith("Blocked"));
    return screenPanel(`Connected view for ${c.id}`,
      h("p", {}, "Technical, resident, delivery, quality and finance states are shown independently. One clear state never clears another."),
      blocked.length ? screenUnknown(`${blocked.length} of 5 gates are blocked: ${blocked.map((r) => r[0]).join(", ")}.`,
        blocked[0][3], blocked[0][4]) : h("p", {}, "No blocker is recorded, which does not confirm readiness."),
      screenTable("Same-home gate states", ["Gate", "State", "Meaning", "Owner", "Next action"], rows));
  }
});
