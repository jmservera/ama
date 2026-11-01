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

const technicalRoles = ["Retrofit Coordinator", "Quality Inspector", "Building Safety Liaison", ...screenManagers];
const qualityRoles = ["Quality Inspector", ...screenManagers];
// Competent role per sign-off, mirroring core signoffs.SIGNOFFS (a proposal for the programme to confirm).
const signoffTypes = [
  ["assessment", "Retrofit assessment", "Quality Inspector"],
  ["design", "Design", "Retrofit Coordinator"],
  ["building", "Building and safety dependency", "Building Safety Liaison"],
  ["coordination", "Coordination", "Retrofit Programme Manager or Programme Support Officer"]
];
function signoffState(s, current) {
  if (!s) return { text: "Not given", ok: false };
  if (s.status === "Signed off") {
    return Number(s.version) === Number(current)
      ? { text: `Signed off on design version ${s.version}`, ok: true }
      : { text: `Stale: signed off on design version ${screenValue(s.version)}, current is ${current}`, ok: false };
  }
  return { text: s.status === "Returned" ? "Returned" : s.status === "Needs reassessment" ? "Needs reassessment" : screenValue(s.status), ok: false };
}
registerRoleScreen({
  id: "technical-queue",
  title: "Technical queue",
  roles: technicalRoles,
  render(c) {
    const t = c.technical;
    const queries = c.stock_reconciliation || [];
    const missing = Array.isArray(c.technical_missing) ? c.technical_missing : null;
    const states = signoffTypes.map(([key, label, role]) => ({ key, label, role, s: t?.signoffs?.[key], ...signoffState(t?.signoffs?.[key], t?.design_version) }));
    const reasons = [];
    if (!t) reasons.push("No design is recorded.");
    if (!queries.length) reasons.push("No source comparison is recorded, so source facts are Unknown.");
    if (missing === null) reasons.push("Missing references are not supplied.");
    for (const m of missing || []) reasons.push(`${m.item}. Owner: ${m.assigned_to}.`);
    for (const x of states) if (t && !x.ok && !(missing || []).some((m) => m.item.startsWith(x.label))) reasons.push(`${x.label}: ${x.text}.`);
    const returned = states.filter((x) => x.s?.status === "Returned" || x.s?.status === "Needs reassessment");
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view. It gives no sign-off and changes no record. Sign-offs are named human professional decisions; role membership alone does not attest competence. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Technical readiness",
        reasons.length
          ? screenUnknown(reasons.join(" "), "See the owner named against each item", "Complete and record each item, then reload this screen")
          : h("p", { class: "ok", role: "status" }, "Recorded evidence is complete: every sign-off is on the current design version and nothing is missing. This screen does not approve the stage.")),
      screenPanel("Source facts",
        screenTable("Source facts and conflicts", ["Query", "Field", "First source (value, ID, version, age)", "Compared source (value, ID, version, age)", "Status", "Owner"],
          queries.map((q) => [q.id, q.field,
            `${q.left.value}, ${q.left.source_id} v${q.left.version}, ${assetAgeDays(q.left.date)}, ${q.left.validation_state}`,
            `${q.right.value}, ${q.right.source_id} v${q.right.version}, ${assetAgeDays(q.right.date)}, ${q.right.validation_state}`,
            assetStatus(c, q), screenPerson(q.query_owner)]))),
      screenPanel("Design version",
        t ? screenFields([["Current design version", t.design_version], ["Recorded by", t.design_name], ["Recorded at", screenStamp(t.design_at)],
          ["Latest change note", t.versions?.at(-1)?.note]])
          : screenUnknown("No design is recorded for this home.", "Retrofit Coordinator", "Record the design")),
      screenPanel("Separate sign-offs",
        screenTable("Sign-offs against the current design version", ["Sign-off", "Competent role", "State", "By", "Note or reason"],
          states.map((x) => [x.label, x.role, x.text, x.s?.by || "Nobody yet", x.s?.reason || x.s?.note]))),
      screenPanel("Returns and routing",
        returned.length ? screenTable("Returned or reassessment sign-offs", ["Sign-off", "Route to", "Why", "Returned by"],
          returned.map((x) => {
            const last = (x.s.history || []).at(-1);
            return [x.label, `${x.role} (competent reviewer for this sign-off, not a generic approval)`, x.s.reason, last?.by];
          }))
          : h("p", { class: "empty" }, "No returned sign-offs recorded. This does not establish readiness.")),
      screenPanel("Missing references",
        missing === null ? screenUnknown("Missing references are not supplied for this home.", "Grants and Evidence Officer", "Reload; do not treat as complete")
          : screenTable("Missing references", ["Missing item", "Owner"], missing.map((m) => [m.item, m.assigned_to]))));
  }
});

function qualityMeasures(c) {
  const m = c.measures;
  return (Array.isArray(m) ? m : String(m ?? "").split(",")).map((x) => String(x).trim()).filter(Boolean);
}
function qualityNext(r) {
  if (r.state === "Returned") return `Defect owner ${screenValue(r.defect?.owner)} to correct, then record the fix`;
  if (r.state === "Fixed, awaiting reinspection") return "Independent reinspection by a Quality Inspector not involved in the work or fix";
  if (r.state === "Submitted") return "Independent inspector to accept or return";
  if (r.state === "Accepted") return "Handover to be recorded by a person";
  return "None recorded";
}
registerRoleScreen({
  id: "quality-queue",
  title: "Quality queue",
  roles: qualityRoles,
  render(c) {
    const records = (c.quality || []).filter((r) => r.state !== "Superseded");
    const measures = qualityMeasures(c);
    const blockers = measures.flatMap((measure) => {
      const rs = records.filter((r) => r.measure === measure);
      if (!rs.length) return [`${measure}: no quality evidence recorded.`];
      return rs.filter((r) => r.state !== "Accepted" && r.state !== "Handed over").map((r) => `${measure}: ${r.state}.`)
        .concat(rs.filter((r) => (r.items || []).some((i) => !String(i.evidence || "").trim())).map(() => `${measure}: a check has no evidence note.`));
    });
    if (!measures.length) blockers.push("No measures are recorded for this home.");
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view. It accepts, returns and hands over nothing. Acceptance is by a named person independent of the work. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Handover readiness",
        blockers.length ? screenUnknown(blockers.join(" "), "Quality Inspector or defect owner named per measure", "Record the missing evidence, fix or reinspection; handover stays blocked until then")
          : h("p", { class: "ok", role: "status" }, "Every measure has accepted evidence and no open defect. This screen does not record the handover.")),
      ...(records.length ? records.map((r) => screenPanel(`${r.measure}: ${r.state}`,
        screenFields([["Checklist", `${screenValue(r.checklist)} ${screenValue(r.checklist_version)}`], ["Evidence version", r.evidence_version],
          ["Evidence source", r.source], ["Submitted by", r.submitted_by], ["Accepted by", r.accepted_by || "Nobody yet"], ["Next action", qualityNext(r)]]),
        screenTable(`Per-check evidence for ${r.measure}`, ["Check", "Evidence seen", "State"],
          (r.items || []).map((i) => [i.label, i.evidence, String(i.evidence || "").trim() ? "Evidence noted" : "No evidence"])),
        r.defect ? screenFields([["Defect", r.defect.description], ["Why returned", r.defect.reason], ["Defect owner", r.defect.owner],
          ["Raised by", r.defect.raised_by], ["Fixed by", r.defect.fixed_by || "Not yet fixed"], ["Remediation evidence", r.defect.remediation_evidence || "Not supplied"],
          ["Reinspection", r.state === "Fixed, awaiting reinspection" ? "Awaiting independent reinspection" : r.state === "Accepted" ? "Passed" : "Not yet possible"]])
          : h("p", { class: "empty" }, "No defect recorded."),
        r.handover ? screenFields([["Handed over by", r.handover.by], ["Handed over at", screenStamp(r.handover.at)]]) : null))
        : [screenPanel("Quality evidence", h("p", { class: "empty" }, "No quality records supplied. This does not establish readiness."))]));
  }
});
