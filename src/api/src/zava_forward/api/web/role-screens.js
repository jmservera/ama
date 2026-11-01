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
function screenTable(label, headings, rows, limit = 50) {
  return h("div", {},
    rows.length > limit && h("p", { role: "status" }, `Showing the first ${limit} of ${rows.length} records. Open the case workspace to inspect the remaining evidence. This is not a complete readiness check.`),
    rows.length ? h("div", { class: "table-scroll", role: "region", "aria-label": label, tabindex: 0 },
      h("table", {}, h("caption", {}, label),
        h("thead", {}, h("tr", {}, headings.map((title) => h("th", { scope: "col" }, title)))),
        h("tbody", {}, rows.slice(0, limit).map((row) => h("tr", {}, row.map((value) => h("td", {}, screenValue(value))))))))
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
  const overview = !c && screen.summarise && data.items.length ? await screen.summarise(data.items, signal) : null;
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
    : h("div", {}, h("p", { class: "empty" }, "No home selected. Choose a home from this queue."), overview);
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
  ["Phase check evidence", "Programme manager to name the evidence for the phase check"]
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
    const queue = await api("/api/asset/stock-queue", undefined, signal).catch(() => null);
    return { portfolio, report, queue };
  },
  render(c, extra) {
    const queries = c.stock_reconciliation || [];
    const owner = queries.find((q) => assetStatus(c, q) === "Unresolved")?.query_owner;
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only reader view. It records no investment approval and changes no record. Budgets, priorities, forecasts and eligibility are Unknown unless a constructed fixture says so, and this page cannot confirm them. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Stock conflict queue across homes (portfolio scope, not this home)",
        h("p", {}, "Homes with an open stock conflict, oldest source first. The order is source age only. It is not an investment priority, and no source is chosen as correct."),
        extra?.queue
          ? screenTable("Open stock conflicts by home", ["Home", "Open conflicts", "Fields in conflict", "Oldest source date", "Resolution owners", "Investment inputs"],
            extra.queue.items.map((r) => [`${r.id}, ${r.address}, ${r.town}`, r.open_queries, (r.fields || []).join(", "), `${r.oldest_source_date}, ${assetAgeDays(r.oldest_source_date)}`,
              (r.owners || []).join(", ") || "Unassigned", "Unknown. See missing investment inputs."]), 100)
          : screenUnknown("The cross-home queue could not be loaded.", "Programme manager", "Reload, or open each home from the case queue")),
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
      screenPanel("Benefits and phase check",
        screenUnknown("No measured benefit or phase check evidence is supplied for this home.", "Programme manager to name an owner", "Supply dated evidence before any phase check is read as passed")),
      screenPanel("Portfolio scope (separate from this home)",
        screenFields([["Cases permitted to your role", extra?.portfolio?.total],
          ["Meaning", "A role-scoped count, not a stock, budget or programme total"]])),
      screenPanel("Ledger-wide AI cohort (all homes, not this home)", assetCost(extra?.report)));
  }
});

const choiceRoles = ["Resident Liaison Officer", "Retrofit Coordinator", "Retrofit Programme Manager", "Programme Support Officer"];
const choiceStop = new Set(["Paused", "Withdrawn"]);
const choiceLatest = (m) => (m.versions || []).at(-1);
const choiceBinding = (v) => `scope ${screenValue(v.scope)}, revision ${screenValue(v.context_revision)}, design ${screenValue(v.design_version)}`;
const choiceStopVersion = (m) => {
  if (m.review?.status !== "Needs human review") return null;
  const v = (m.versions || []).find((x) => x.version === m.review.decision_version);
  return v && choiceStop.has(v.status) ? v : null;
};
const choiceStopped = (m) => choiceStop.has(m.status) || choiceStopVersion(m) !== null;
function choiceMeasure(m) {
  const v = choiceLatest(m);
  const ctx = m.context ? `scope ${screenValue(m.context.scope)}, revision ${screenValue(m.context.revision)}, design ${screenValue(m.context.design_version)}` : "Current scope not recorded";
  return [m.measure, ctx, m.status,
    v ? `v${v.version} ${v.status} (${choiceBinding(v)}), answered by ${screenValue(v.answered_by)}, recorded ${screenStamp(v.at)}${v.note ? `: ${v.note}` : ""}` : "None recorded",
    screenValue(m.readiness)];
}
function choiceStoppedSummary(m) {
  const v = choiceStopVersion(m) || choiceLatest(m);
  const state = v && v.status !== m.status ? `${v.status} (current answer ${m.status})` : m.status;
  const review = m.review?.status === "Needs human review" ? ", needs human review before any restart" : "";
  return `${m.measure}: ${state}${v ? ` (v${v.version}, ${choiceBinding(v)})` : ""}${review}`;
}
function choiceQueueRow([row, c]) {
  if (!c) return [row.id, "Unavailable. Open the home to check.", "Unavailable", "Unavailable"];
  const measures = c.measure_decisions || [];
  const stopped = measures.filter(choiceStopped).map(choiceStoppedSummary);
  const u = c.resident_update;
  return [row.id,
    measures.length ? measures.map((m) => { const v = choiceLatest(m); return `${m.measure}: current ${m.status}${v ? `; latest recorded v${v.version} ${v.status} (${choiceBinding(v)})` : ""}`; }).join("; ") : "No measure choices recorded",
    stopped.length ? stopped.join("; ") : "None recorded",
    u ? `${screenValue(u.status)}: ${screenValue(u.purpose)}. Owner ${screenPerson(u.owner_identity || u.owner)}, due ${screenStamp(u.due_at)}, safe route ${screenValue(u.safe_contact_ref)}` : "No commitment recorded"];
}
registerRoleScreen({
  id: "resident-choice",
  title: "Resident choice and update queue",
  roles: choiceRoles,
  async summarise(rows, signal) {
    const entries = await Promise.all(rows.map((row) =>
      api(`/api/cases/${encodeURIComponent(row.id)}`, undefined, signal).then((c) => [row, c], (e) => {
        signal.throwIfAborted();
        return [row, null];
      })));
    return this.summary(entries);
  },
  summary(entries) {
    return screenPanel("Choice and update commitments across this page of homes",
      h("p", {}, "Read-only summary of the homes on this page, not a portfolio total. A paused or withdrawn measure is listed separately from contact and access. Open a home for the full version history."),
      screenTable("Choice and update commitments by home",
        ["Home", "Measure choices (latest version)", "Paused or withdrawn", "Update commitment"],
        entries.map(choiceQueueRow), Infinity));
  },
  render(c) {
    const measures = c.measure_decisions || [];
    const stopped = measures.filter(choiceStopped);
    const update = c.resident_update;
    const requests = c.service_requests || [];
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only view. No message, call or letter is sent and no record changes here. Record supplied answers in the case workspace. Resident-facing screens are designed separately. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Choice for each measure",
        h("p", {}, "Each answer belongs to one measure and one scope version. Not recorded means no answer is known. Contact or access is never read as a yes."),
        screenTable("Measure choices by version",
          ["Measure", "Scope version", "Current answer", "Latest recorded answer", "Readiness"],
          measures.map(choiceMeasure))),
      screenPanel("Paused or withdrawn by the resident",
        h("p", {}, "A pause or withdrawal is the resident's decision about one measure. It is not a contact attempt, a missed visit or an access need."),
        stopped.length ? screenTable("Measures paused or withdrawn",
          ["Measure", "State and scope answered", "In their words", "Restart needs"],
          stopped.map((m) => {
            const v = choiceStopVersion(m) || choiceLatest(m);
            const state = choiceStop.has(m.status) && v === choiceLatest(m) ? m.status : `${v.status} (current answer ${m.status})`;
            return [m.measure, v ? `${state}, ${choiceBinding(v)}` : state, v?.note, "Human review before any restart"];
          }))
          : h("p", { class: "empty" }, "No measure is currently paused or withdrawn in the recorded answers.")),
      screenPanel("Linked update commitment",
        update ? screenFields([
          ["Status", update.status], ["Purpose or linked issue", update.purpose],
          ["Owner", screenPerson(update.owner_identity || update.owner)], ["Due", screenStamp(update.due_at)],
          ["Basis for due date", update.basis], ["Safe route reference", update.safe_contact_ref],
          ["Version", update.version], ["Meaning", "A commitment is not a message. Nothing is sent or marked received here."]])
          : screenUnknown("No update commitment is recorded for this home.", "Case owner or resident-workflow manager", "Record a commitment in the case workspace")),
      screenPanel("Service requests and access needs (separate from choice)",
        screenTable("Service requests and contact needs",
          ["Request", "Route", "Status", "Contact needs", "Next update"],
          requests.map((r) => [r.id, r.route, r.status, (r.accessibility || ["Unknown"]).join(", "), r.next_update]))));
  }
});
const hazardTriageRoles = ["Retrofit Coordinator", "Resident Liaison Officer", "Quality Inspector"];
const hazardActor = (value) => value && (value.name || value.role)
  ? [value.name, value.role].filter(Boolean).join(", ") : "Unknown";
const hazardStep = (stamp) => stamp ? `Recorded ${screenStamp(stamp)}` : "Not recorded";
function hazardFollowUp(h) {
  if (h.accepted_at) return `${hazardActor(h.accepted_by || h.destination)} owns the accepted scope`;
  if (h.received_at) return `Pending acceptance. Follow-up owner: ${hazardActor(h.follow_up || h.sender)}`;
  if (h.sent_at) return `Pending receipt. Follow-up owner: ${hazardActor(h.sender)} chases until acceptance`;
  if (h.referred) return `Legacy referral with no recorded send time. Recorded owner (unverified): ${screenValue(h.owner)}. Retrofit Coordinator to confirm ownership and check the external service record`;
  return `No referral sent. Owner: ${screenValue(h.owner)} to send or record a manual route`;
}
function hazardHold(h) {
  const pause = h.hold || {};
  const decision = pause.decision;
  const scope = `${screenValue(pause.scope)} ${screenValue(pause.case_id)} only`;
  if (pause.status !== "Released") return `${screenValue(pause.status)}. Scope: ${scope}. Release needs an authorised human decision.`;
  return decision
    ? `Released. Scope: ${scope}. Decided by ${hazardActor(decision.actor)} at ${screenStamp(decision.at)}. Reason: ${screenValue(decision.reason)}. Evidence: ${screenValue(decision.evidence)}`
    : `Released. Scope: ${scope}. No authoritative decision evidence is recorded; do not rely on this release.`;
}
function hazardScreen(intro) {
  return (c) => {
    const items = c.hazards || [];
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, intro),
        h("p", {}, "This screen does not classify hazards, set clocks, close hazards or authorise work. Categories and priorities are the recorded report, not a service categorisation. Sent, received and accepted are separate: a sent referral is not receipt, and receipt is not ownership. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only. Every recorded hazard and safeguarding item is listed, including released ones.`)),
      screenPanel("Referral queue",
        screenTable("Hazard referrals for this home",
          ["Item", "Reported observation and urgency", "Aware at", "Source", "Destination", "Sent", "Received", "Accepted", "State", "Follow-up"],
          items.map((x, i) => [`H-${i + 1}`, `${screenValue(x.category)}, ${screenValue(x.priority)}`,
            screenStamp(x.aware_at), x.source, hazardActor(x.destination),
            hazardStep(x.sent_at), hazardStep(x.received_at), hazardStep(x.accepted_at),
            x.state, hazardFollowUp(x)]), Infinity)),
      screenPanel("Retrofit pause and release decision",
        screenTable("Scoped pause and release evidence",
          ["Item", "Pause and release evidence", "Service response due", "Service responded"],
          items.map((x, i) => [`H-${i + 1}`, hazardHold(x), hazardStep(x.response_due_at), hazardStep(x.responded_at)]), Infinity)),
      screenPanel("Where to act",
        h("p", {}, "Referral, receipt, acceptance and release are recorded in the existing case workspace by the named authorised person. Emergency concerns follow the existing human emergency procedure now, not this screen.")));
  };
}
registerRoleScreen({
  id: "safety-lead",
  title: "Building safety referral queue",
  roles: ["Building Safety Liaison", ...screenManagers],
  render: hazardScreen("Read-only view for the Building Safety lead: where each referral stands, who must follow up and what evidence supports any pause release.")
});
registerRoleScreen({
  id: "hazard-triage",
  title: "Repairs and hazard triage",
  roles: hazardTriageRoles,
  render: hazardScreen("Read-only view for repairs and hazard triage: awareness time and source, referral progress and the person who chases an unanswered referral.")
});
const operatorSide = (a) => a ? `${screenValue(a.value)}; source ${screenValue(a.source_id)} v${screenValue(a.version)}; dated ${screenValue(a.date)}; ${screenValue(a.validation_state)}` : "Unknown";
const operatorStatus = (c, q) => (c.stock_reconciliation_events || []).filter((e) => e.query_id === q.id).at(-1)?.status || "Unresolved";
registerRoleScreen({
  id: "data-operator",
  title: "Data steward and operator view",
  roles: screenManagers,
  render(c) {
    const queries = c.stock_reconciliation || [];
    const events = c.stock_reconciliation_events || [];
    const work = c.work;
    const blockers = work?.blockers || [];
    const handoff = work?.handoff;
    const returns = (c.returns || []).filter((r) => r.event_type !== "advance");
    return h("div", {},
      screenPanel("Evidence boundary",
        h("p", {}, "Read-only view for data stewards, performance analysts and digital operators. It does not replay, correct, resolve or retry anything, and it keeps the original source values. Source: desk research, not observed behaviour."),
        h("p", {}, `Home scope: ${c.id} only.`)),
      screenPanel("Conflict queue: both source values",
        screenTable("Source conflicts with both values and source details",
          ["Query", "Field", "First source (value, source, version, date, validation)", "Compared source (value, source, version, date, validation)", "State", "Resolution owner"],
          queries.map((q) => [q.id, q.field, operatorSide(q.left), operatorSide(q.right),
            operatorStatus(c, q), screenPerson(q.query_owner)]))),
      screenPanel("Eligibility and original source",
        screenFields([["Eligibility", "Unknown"],
          ["Original source values", queries.length ? "Preserved unchanged in the table above" : "None supplied"],
          ["Winning source", "Not selected. No latest-wins or silent correction is applied."]])),
      screenPanel("Returns and reopens",
        returns.length ? screenTable("Recorded returns and reopens",
          ["Recorded", "Type", "From", "To", "Reason", "Source", "Next action", "Receiving owner"],
          returns.map((r) => [screenStamp(r.at), r.reopened ? "Reopened" : "Returned", r.from_stage, r.to_stage, r.reason,
            `${screenValue(r.source)} v${screenValue(r.source_version)}`, r.next_action, screenPerson(r.receiving_owner)]))
          : screenUnknown("No return or reopen is recorded for this home.", "Programme manager to name an owner", "Confirm whether a return is expected")),
      screenPanel("Handoff and exception queue",
        handoff ? screenFields([["Handoff destination", handoff.destination], ["Proposed receiver", handoff.proposed_receiver],
          ["Confirmed receiver", handoff.confirmed_receiver], ["Chase owner", handoff.chase_owner],
          ["Handoff state", handoff.state], ["Work reason", work.reason], ["Next action", work.next_action]])
          : screenUnknown("No handoff is recorded for this home.", "Programme manager to name an owner", "Confirm whether a handoff is expected"),
        screenTable("Open exceptions and prerequisites",
          ["Step", "Reason", "Owner", "Next action", "Source and version"],
          blockers.map((b) => [b.step, b.reason, b.owner, b.next_action, `${screenValue(b.source)} v${screenValue(b.version)}`]))),
      screenPanel("Event metadata and recovery context",
        h("p", {}, "Illustrative event metadata only. These are recorded dispositions with a narrative reason. They are not an operational audit trail and cannot prove that nothing else happened."),
        screenTable("Recorded stock query events",
          ["Event", "Query", "State", "Recorded", "Recorded by", "Reason", "Evidence"],
          events.map((e) => [e.id, e.query_id, e.status, screenStamp(e.at), screenPerson(e.recorded_by), e.reason, e.evidence])),
        screenFields([["Recovery context", work ? `Next action: ${screenValue(work.next_action)}. Owner: ${screenValue(work.owner)}. Recorded as of ${screenValue(work.as_of)}.` : "Unknown. No recovery context is recorded."],
          ["Integration run and queue state", "Unknown. No interface run record is supplied to this screen."]])));
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
const financeRoles = ["Grants and Evidence Officer", ...screenManagers];
const financeCurrency = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
const financeMoney = (value) => typeof value === "number" && Number.isFinite(value) ? financeCurrency.format(value) : "Unknown";
const financeQty = (value) => typeof value === "number" && Number.isFinite(value) ? String(value) : "Unknown";
const financeChecked = (inv) => Boolean(inv.status) && inv.status !== "Received" && inv.status !== "Not checked";
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
      : !Number.isFinite(ln.quantity) || !Number.isFinite(com.quantity) ? "Unknown. Quantity not supplied or invalid."
      : ln.quantity > com.quantity ? `Above authorised (${financeQty(ln.quantity)} of ${financeQty(com.quantity)})`
        : `Within authorised (${financeQty(ln.quantity)} of ${financeQty(com.quantity)})`;
    return [`Line ${i + 1}: ${screenValue(ln.measure)}`, `Quantity ${financeQty(ln.quantity)}, line total ${financeMoney(ln.amount)}`,
      com ? `${com.id} (${screenValue(com.status)}), ${financeMoney(com.amount)}` : "Unknown. Not matched.",
      scope, quantity, budgetText,
      ln.milestone_ref ? `Supplied reference ${ln.milestone_ref} (unverified). Acceptance is Unknown.` : "Unknown. No milestone reference supplied.",
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
      ["Payment pause", inv.hold ? `Paused by ${screenValue(inv.hold.name)}: ${screenValue(inv.hold.reason)}` : "No pause recorded"],
      ["Finance decision", inv.disposition ? `${inv.disposition}, recorded by ${screenValue(inv.disposition_by)}` : "No Finance decision recorded"],
      ["Payment status (a note of what Finance did elsewhere)", `${screenValue(inv.payment_status)}. This system never makes or releases a payment.`]]),
    screenTable(`Line comparison for ${inv.id}`,
      ["Invoice line", "Quantity and line total", "Commitment", "Scope", "Quantity check", "Budget", "Supplied milestone reference", "Exception or unknown"],
      financeLineRows(f, inv)))));
}
const financeQueueRows = (queue) => queue.map((q) => [q.case_id, q.invoice, `${screenValue(q.supplier)}, ref ${screenValue(q.ref)}`,
  screenValue(q.status), financeChecked(q) ? `${q.exceptions ?? "Unknown"} exceptions` : "Unknown. Not checked yet", q.on_hold ? "Paused" : "Not paused", financeMoney(q.total)]);
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
        queue ? screenTable("Invoices with exceptions, pauses or not yet checked",
          ["Home", "Invoice", "Supplier and reference", "Status", "Exceptions", "Pause", "Invoice total"], financeQueueRows(queue))
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
    const pauses = Array.isArray(extra?.review?.decision_holds) ? extra.review.decision_holds : null;
    const readable = drafts !== null && pauses !== null;
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
            g.pending ? `${screenValue(g.pending.to)}, proposed by ${screenValue(g.pending.name)}. Evidence: ${screenValue(g.pending.source)}` : "Nothing waiting",
            (g.history || []).length ? g.history.map((x) => `${screenValue(x.state)}: ${screenValue(x.source)} (approved by ${screenValue(x.approved_by)}, ${screenValue(x.source_status)})`).join("; ") : "Unknown. No approved stage."]))
          : h("p", { class: "empty" }, "No grant recorded. This does not establish that no funding is available.")),
      drafts ? (drafts.length ? drafts.map(fundingDraftPanel)
        : screenPanel("Constructed field draft", h("p", { class: "empty" }, "No field draft recorded for this home. Template, fields and evidence are Unknown.")))
        : screenPanel("Constructed field draft", h("p", { class: "empty" }, "Unknown. The field review could not be read for your role.")),
      screenPanel("Readiness export",
        screenFields([["Claim pack readiness", !readable ? "Unknown. The field review could not be read." : drafts && drafts.some((d) => d.reviewed_ready) ? "A reviewer recorded ready on at least one draft. A person must still check and submit it outside this system." : "Not ready. No reviewed export exists."],
          ["Open decision pauses", !pauses ? "Unknown. The field review could not be read." : pauses.length ? `${pauses.length} recorded` : "None recorded"],
          ["Submission, award and payment", "Not recorded here. This screen never infers them."]])),
      screenPanel("AI economics (ledger-wide, all homes)", assetCost(extra?.report)));
  }
});
