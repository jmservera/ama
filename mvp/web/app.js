"use strict";
const app = document.getElementById("app");
let me = null;

function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) {
    if (kid == null || kid === false) continue;
    el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return el;
}

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && path !== "/api/login") { me = null; return login(); }
  if (!res.ok) { const e = new Error(data.error || "Something went wrong."); e.reasons = data.reasons; throw e; }
  return data;
}

const fmtDate = (s) => {
  if (!s) return "None";
  const d = new Date(s);
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
};
const ago = (s) => {
  if (!s) return "No contact yet";
  const days = Math.floor((Date.now() - new Date(s)) / 864e5);
  return days <= 0 ? "Today" : days === 1 ? "Yesterday" : `${days} days ago`;
};
const show = (...nodes) => { app.replaceChildren(...nodes.filter((n) => n && n.nodeType)); app.focus(); };

function login(msg) {
  document.getElementById("nav").hidden = true;
  const email = h("input", { id: "email", type: "email", autocomplete: "username", required: true });
  const pass = h("input", { id: "pw", type: "password", autocomplete: "current-password", required: true });
  const err = h("p", { class: "err", role: "alert" }, msg || "");
  const form = h("form", { class: "card login", onsubmit: async (e) => {
    e.preventDefault();
    try { await api("/api/login", { email: email.value, password: pass.value }); await start(); }
    catch (x) { err.textContent = x.message; }
  } },
    h("h1", {}, "Sign in"),
    h("label", { for: "email" }, "Work email"), email,
    h("label", { for: "pw" }, "Password"), pass, err,
    h("button", { type: "submit" }, "Sign in"));
  show(form);
}

async function start() {
  me = await api("/api/me");
  document.getElementById("who").textContent = `${me.user.name}, ${me.user.role}`;
  document.getElementById("nav").hidden = false;
  route();
}

function route() {
  const m = location.hash.match(/^#\/case\/(.+)$/);
  if (m) return caseView(decodeURIComponent(m[1]));
  if (location.hash === "#/import") return importView();
  if (location.hash === "#/overview") return overviewView();
  if (location.hash === "#/visits") return visitsView();
  if (location.hash === "#/funding") return fundingView();
  return listView(location.hash === "#/all" ? "all" : "mine");
}

const listState = { q: "", stage: "", area: "", flag: "", sort: "urgent", wave: "", owner: "" };
const qs = (o) => Object.entries(o).filter(([, v]) => v).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join("&");
const isManager = () => ["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
const FLAGS = [["hazard", "Safety issue open"], ["support", "Needs extra support"], ["long", "Waiting 60+ days"], ["nodecision", "No resident decision yet"], ["funding", "Funding not confirmed"]];

function aiBox() {
  const box = h("section", { class: "card ai" }, h("h2", {}, "Today's briefing"), h("p", { class: "muted" }, "Reading your cases..."));
  api("/api/briefing").then((b) => box.replaceChildren(h("h2", {}, "Today's briefing"), h("p", {}, b.text), h("p", { class: "muted" }, `${b.label}. Suggestions only. Refreshed when your cases change.`)))
    .catch(() => box.remove());
  return box;
}

function priorityPanel() {
  const box = h("section", { class: "card ai", "aria-label": "AI priority suggestion" });
  const rowsOf = (items, withReason) => h("ol", {}, items.map((i) => h("li", {},
    h("a", { href: `#/case/${encodeURIComponent(i.case_id)}` }, `${i.resident}, ${i.address}`), ` (rank ${i.rank})`,
    withReason && i.reason ? h("div", { class: "muted" }, i.reason) : null)));
  const paint = (rec, msg) => {
    const kids = [h("h2", {}, "Which cases first? A second opinion"),
      h("p", { class: "muted" }, "The rule-based order below is the list order. The AI suggestion is advice only: it never changes the ranking, owners, stages or queues.")];
    if (msg) kids.push(h("p", { role: "alert" }, msg));
    if (!rec) {
      kids.push(h("p", {}, h("button", { class: "alt", onclick: ask }, "Suggest my top 5")));
    } else {
      kids.push(h("div", { class: "grid" },
        h("div", {}, h("h3", {}, `Rule-based order (policy ${rec.policy_version})`), rowsOf(rec.deterministic, false)),
        h("div", {}, h("h3", {}, `Suggestion: ${rec.label}`), rowsOf(rec.items, true),
          h("p", { class: "muted" }, `${rec.source === "ai" ? "Written by AI" : "Written by rules, AI not available"}. ${rec.overlap} of ${rec.items.length} match the rule-based top ${rec.n}.`))));
      if (rec.status === "Proposed") {
        const why = h("input", { id: "pri-why", type: "text", placeholder: "Reason (needed to edit or reject)", maxlength: 300 });
        const keep = rec.items.map((i) => h("input", { type: "checkbox", checked: true, "aria-label": `Keep ${i.resident}` }));
        const act = (action) => async () => {
          const items = rec.items.filter((_, n) => keep[n].checked).map((i) => ({ case_id: i.case_id, reason: i.reason }));
          try { paint(await api(`/api/ai/priority/${rec.id}/${action}`, { reason: why.value, items })); } catch (e) { paint(rec, e.message); }
        };
        kids.push(h("div", { class: "row" }, h("label", { for: "pri-why" }, "Your reason"), why),
          h("div", { class: "row" }, h("span", { class: "muted" }, "To edit, untick cases to drop:"), rec.items.map((i, n) => h("label", {}, keep[n], ` ${i.resident}`))),
          h("div", { class: "row" }, h("button", { onclick: act("accept") }, "Accept"), h("button", { class: "alt", onclick: act("edit") }, "Edit"),
            h("button", { class: "alt", onclick: act("reject") }, "Reject")));
      } else {
        kids.push(h("p", {}, `${rec.status}${rec.reason ? `: ${rec.reason}` : ""}. Recorded in the audit log.`),
          h("p", {}, h("button", { class: "alt", onclick: ask }, "Suggest again")));
      }
    }
    box.replaceChildren(...kids);
  };
  const ask = async () => { box.setAttribute("aria-busy", "true"); try { paint(await api("/api/ai/priority", { n: 5 })); } catch (e) { paint(null, e.message); } box.removeAttribute("aria-busy"); };
  api("/api/ai/priority").then((d) => paint(d.recommendation && d.recommendation.status === "Proposed" ? d.recommendation : null)).catch(() => paint(null));
  return box;
}

let briefingBox = null;
async function listView(view) {
  const fx = await api("/api/facets");
  if (!briefingBox) briefingBox = aiBox();
  const results = h("div", { "aria-live": "polite" });
  const title = h("h1", {}, view === "mine" ? "My cases today" : "All open cases");
  const csv = h("a", { class: "btn alt", download: "cases.csv" }, "Download for Excel");
  let timer = 0, seq = 0;
  let rows = [], total = 0, policy = "";
  const PAGE = 50;
  const render = () => {
    results.replaceChildren(...[
      h("p", { class: "muted" }, `${total} ${total === 1 ? "case" : "cases"}${listState.sort === "urgent" ? `. Ranked by policy version ${policy}, a fixed rule order (safety first). The order is the same every time.` : ""}`),
      h("ul", { class: "list" }, rows.length ? rows.map((r) => h("li", {},
        h("a", { class: "item", href: `#/case/${encodeURIComponent(r.id)}` },
          h("div", {}, h("span", { class: "name" }, r.resident),
            r.hazard && h("span", { class: "flag danger" }, "Safety issue open"),
            r.support && h("span", { class: "flag" }, "Needs extra support"),
            h("div", {}, `${r.address}, ${r.town} ${r.postcode}`),
            h("div", { class: "status" }, r.status),
            h("div", { class: "muted" }, `Rank ${r.rank}: ${r.reasons.slice(0, 3).join("; ")}`),
            view === "all" && h("div", { class: "muted" }, `Owner: ${r.owner}`),
            r.focus && h("dl", { class: "focus" }, r.focus.flatMap(([k, v]) => [h("dt", {}, k), h("dd", {}, /^\d{4}-\d\d-\d\d$/.test(v) ? fmtDate(v) : v)]))),
          h("div", { class: "meta" }, h("div", {}, r.stage), h("div", {}, `${r.days} days in this stage`), h("div", {}, `Last contact: ${ago(r.last_contact)}`),
            r.next_visit && h("div", {}, `Visit: ${fmtDate(r.next_visit)}`))))) : h("li", { class: "card" }, "Nothing matches. Try clearing a filter.")),
      rows.length < total ? h("p", {}, h("button", { class: "alt", onclick: () => load(true) }, `Show more (${rows.length} of ${total} shown)`)) : null].filter(Boolean));
  };
  const load = async (more) => {
    const my = ++seq;
    const d = await api(`/api/cases?view=${view}&${qs(listState)}&limit=${PAGE}&offset=${more ? rows.length : 0}`);
    if (my !== seq) return;
    csv.href = `/api/cases.csv?view=${view}&${qs(listState)}`;
    rows = more ? rows.concat(d.items) : d.items;
    total = d.total;
    policy = d.policy_version;
    render();
  };
  const field = (label, key, opts) => {
    const el = h("select", { id: `f-${key}` }, h("option", { value: "" }, "Any"), opts.map(([v, t]) => h("option", { value: v }, t)));
    el.value = listState[key];
    el.addEventListener("change", () => { listState[key] = el.value; load(); });
    return [h("label", { for: `f-${key}` }, label), el];
  };
  const search = h("input", { id: "f-q", type: "search", placeholder: "Name, address or postcode" });
  search.value = listState.q;
  search.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(() => { listState.q = search.value; load(); }, 250); });
  const sort = h("select", { id: "f-sort" }, Object.entries(fx.sorts).map(([k, t]) => h("option", { value: k }, t)));
  sort.value = listState.sort;
  sort.addEventListener("change", () => { listState.sort = sort.value; load(); });
  const side = h("aside", { class: "side", "aria-label": "Filters" }, h("h2", {}, "Filter"),
    h("label", { for: "f-q" }, "Find"), search,
    field("Stage", "stage", fx.stages.map((x) => [x, x])),
    field("Local authority", "area", fx.areas.map((x) => [x, x])),
    field("Wave", "wave", fx.waves.map((x) => [x, x])),
    view === "all" && field("Owner", "owner", me.staff.map((x) => [x.code, x.name])),
    field("Show only", "flag", FLAGS),
    h("label", { for: "f-sort" }, "Sort by"), sort,
    h("p", {}, h("button", { class: "alt", onclick: () => { Object.assign(listState, { q: "", stage: "", area: "", flag: "", wave: "", owner: "" }); listView(view); } }, "Clear filters")));
  show(h("div", { class: "layout" }, side, h("div", { class: "main" },
    briefingBox,
    view === "mine" && priorityPanel(),
    h("div", { class: "row between" }, title, h("div", { class: "row" },
      h("a", { class: "btn alt", href: view === "mine" ? "#/all" : "#/" }, view === "mine" ? "See all cases" : "See my cases"),
      h("a", { class: "btn alt", href: "#/import" }, "Check a spreadsheet"), csv)),
    results)));
  load();
}

async function caseView(id) {
  const c = await api(`/api/cases/${encodeURIComponent(id)}`);
  const r = c.resident, hm = c.home;
  const openHaz = c.hazards.filter((x) => !x.released);
  const msg = h("div", { role: "status" });
  const refresh = async (fn) => {
    try { await fn(); briefingBox = null; await caseView(id); } catch (e) {
      msg.replaceChildren(h("p", { class: "err" }, e.message), ...(e.reasons || []).map((x) => h("p", {}, x)));
    }
  };
  const outcome = h("input", { id: "outcome", placeholder: "For example: spoke to resident, visit agreed" });
  const note = h("textarea", { id: "note", "aria-label": "Notes" });
  const channel = h("select", { "aria-label": "How you spoke" }, ["Phone", "Text message", "Email", "Visit"].map((x) => h("option", {}, x)));
  const decision = h("select", { id: "dec" }, ["Not yet asked", "Waiting", "Accepted", "Declined"].map((x) => h("option", { selected: x === c.decision.status }, x)));
  const to = h("select", { id: "to" }, me.staff.map((s) => h("option", { value: s.email }, `${s.name} (${s.role})`)));
  const draftBox = h("div", {});
  const kind = async (k) => {
    const d = await api(`/api/cases/${encodeURIComponent(id)}/draft`, { kind: k });
    draftBox.replaceChildren(h("p", { class: "muted" }, d.note), h("textarea", { "aria-label": "Draft message" }, d.text));
    draftBox.querySelector("textarea").value = d.text;
  };
  const aiRun = async (task) => {
    draftBox.replaceChildren(h("p", { class: "muted" }, "Working on it..."));
    try {
      const d = await api(`/api/cases/${encodeURIComponent(id)}/ai`, { task });
      const ta = h("textarea", { "aria-label": "Draft", rows: 9 });
      ta.value = d.text;
      draftBox.replaceChildren(h("p", { class: "muted" }, `${d.label}. Nothing is sent. Change it as you like.`), ta);
    } catch (e) { draftBox.replaceChildren(h("p", { class: "err" }, e.message)); }
  };
  const sugg = h("section", { class: "card" }, h("h2", {}, "Who could take this on"),
    h("p", { class: "muted" }, "Suggested by role and workload rules. You decide."),
    h("ul", { class: "list" }, c.suggestions.map((x) => h("li", {},
      h("strong", {}, `${x.name}, ${x.role}`), h("div", { class: "muted" }, x.reasons.join(". ")),
      h("button", { class: "alt", onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/handover`, { to: x.email })) }, `Hand over to ${x.name.split(" ")[0]}`)))));
  show(
    h("a", { class: "back", href: "#/" }, "Back to the list"),
    h("div", { class: "row between" },
      h("h1", {}, r.name, c.hazards.some((x) => !x.released) && h("span", { class: "flag danger" }, "Safety issue open")),
      h("span", { class: "muted" }, `Reference ${c.id}`)),
    h("div", { class: `status-line${openHaz.length ? " danger" : ""}`, role: "status" }, c.status),
    h("div", { class: "grid" },
      h("section", { class: "card" }, h("h2", {}, "Contact"),
        h("div", { class: "big" }, h("a", { href: `tel:${r.phone.replace(/\s/g, "")}` }, r.phone)),
        r.email && h("div", {}, r.email),
        h("dl", {},
          h("dt", {}, "Address"), h("dd", {}, `${hm.address}, ${hm.town} ${hm.postcode}`),
          h("dt", {}, "Prefers"), h("dd", {}, r.preferred),
          h("dt", {}, "Not available"), h("dd", {}, r.unavailable || "No restrictions recorded"),
          h("dt", {}, "Support needs"), h("dd", {}, r.adjustment === "None" ? "None recorded" : r.adjustment),
          r.priority_support && [h("dt", {}, "Flag"), h("dd", {}, "Needs extra support")],
          r.representative && [h("dt", {}, "Acts for them"), h("dd", {}, `${r.representative.name} (${r.representative.relationship}), ${r.representative.phone}`)],
          h("dt", {}, "Last contact"), h("dd", {}, ago(c.contacts[0] && c.contacts[0].at)),
          h("dt", {}, "Next visit"), h("dd", {}, fmtDate((c.appointments.find((a) => a.outcome === "Booked") || {}).date)))),
      h("section", { class: "card" }, h("h2", {}, "Where it is up to"),
        h("dl", {},
          h("dt", {}, "Stage"), h("dd", {}, c.stage),
          h("dt", {}, "In this stage"), h("dd", {}, `${c.days_in_stage} days`),
          h("dt", {}, "Case owner"), h("dd", {}, `${c.owner}, ${c.owner_role}`),
          h("dt", {}, "Works"), h("dd", {}, c.measures),
          h("dt", {}, "Contractor"), h("dd", {}, `${c.contractor.name}, ${c.contractor.contact}, ${c.contractor.phone}`),
          h("dt", {}, "Home"), h("dd", {}, `${hm.type}, built ${hm.built}, EPC ${hm.epc}, ${hm.tenure}`),
          h("dt", {}, "Resident decision"), h("dd", {}, `${c.decision.status}${c.decision.by ? ` (recorded by ${c.decision.by})` : ""}`)))),
    openHaz.length > 0 && h("section", { class: "card" }, h("h2", {}, "Safety issues"),
      h("ul", { class: "list" }, openHaz.map((x) => h("li", {},
        `${x.category}, noticed ${fmtDate(x.noticed)} (${Math.max(0, Math.floor((Date.now() - new Date(x.noticed)) / 864e5))} days open). Owner: ${x.owner}. ${x.referred ? `Passed to repairs ${fmtDate(x.referred)}.` : "Not yet passed to repairs."}`)))),
    h("section", { class: "card" }, h("h2", {}, "Log a call"),
      h("label", { for: "outcome" }, "What happened"), outcome,
      h("label", {}, "How you spoke"), channel,
      h("label", { for: "note" }, "Notes"), note,
      h("p", {}, h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/call`, { outcome: outcome.value, note: note.value, channel: channel.value })) }, "Save"))),
    h("div", { class: "grid" },
      h("section", { class: "card" }, h("h2", {}, "What the resident has told us"),
        h("p", { class: "muted" }, "Record their answer in their words. It is never worked out for them."),
        h("label", { for: "dec" }, "Do they want the works?"), decision,
        h("p", {}, h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/decision`, { status: decision.value })) }, "Save answer"))),
      h("section", { class: "card" }, h("h2", {}, "Hand this case to someone"),
        h("label", { for: "to" }, "Who is taking it"), to,
        h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/handover`, { to: to.value })) }, "Hand over")))),
    sugg,
    c.can_advance && h("section", { class: "card" }, h("h2", {}, "Final checks"),
      c.gate.length ? [h("p", {}, "This case cannot move on yet:"), h("ul", {}, c.gate.map((x) => h("li", {}, x)))] : h("p", {}, "Everything is in place."),
      h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/advance`, {})) }, "Ready to book the installation")),
    h("section", { class: "card" }, h("h2", {}, "Write to the resident"),
      h("div", { class: "row" }, h("button", { onclick: () => aiRun("message") }, "Draft with AI"),
        h("button", { class: "alt", onclick: () => aiRun("summary") }, "Catch me up on this case"),
        h("button", { class: "alt", onclick: () => kind("visit") }, "Plain visit template"),
        h("button", { class: "alt", onclick: () => kind("update") }, "Plain update template")), draftBox),
    documentsPanel(c, id, refresh),
    fundingPanel(c, id, refresh),
    msg,
    h("section", { class: "card" }, h("h2", {}, "History"),
      c.contacts.length ? h("ul", { class: "tl" }, c.contacts.slice(0, 15).map((k) => h("li", {},
        h("strong", {}, `${fmtDate(k.at)} ${k.channel}: ${k.outcome}`), h("div", { class: "muted" }, `${k.by}${k.note ? `. ${k.note}` : ""}`)))) : h("p", {}, "No contact recorded yet.")));
}

function documentsPanel(c, id, refresh) {
  const kinds = ["EPC", "Survey", "Design", "Consent", "Funding evidence", "Photo", "Other"];
  const kind = h("select", { "aria-label": "Type of document" }, kinds.map((k) => h("option", {}, k)));
  const file = h("input", { type: "file", "aria-label": "Choose a file", accept: ".pdf,.png,.jpg,.jpeg,.docx,.xlsx,.csv,.txt" });
  const out = h("div", { role: "status" });
  const upload = () => {
    const f = file.files[0];
    if (!f) { out.replaceChildren(h("p", { class: "err" }, "Choose a file first.")); return; }
    const rd = new FileReader();
    rd.onload = () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/upload`, { name: f.name, kind: kind.value, data: String(rd.result).split(",")[1] }));
    rd.readAsDataURL(f);
  };
  const read = async (d) => {
    out.replaceChildren(h("p", { class: "muted" }, "Reading..."));
    try {
      const r = await api(`/api/cases/${encodeURIComponent(id)}/read-doc`, { id: d.id });
      out.replaceChildren(h("p", { class: "muted" }, r.source === "ai" ? "AI-read, please check:" : "Note:"), h("p", { class: "pre" }, r.text));
    } catch (e) { out.replaceChildren(h("p", { class: "err" }, e.message)); }
  };
  return h("section", { class: "card" }, h("h2", {}, "Documents"),
    h("p", {}, c.checklist.map((x) => h("span", { class: `flag${x.present ? "" : " danger"}` }, `${x.present ? "Have" : "Need"}: ${x.kind}`))),
    c.documents.length ? h("ul", { class: "list" }, c.documents.map((d) => h("li", { class: "row between" },
      h("span", {}, h("a", { href: `/api/docs/${encodeURIComponent(id)}/${d.id}` }, d.name), ` ${d.kind}, ${fmtDate(d.at)}, ${d.by}`),
      !d.generated && h("button", { class: "alt", onclick: () => read(d) }, "Read with AI")))) : h("p", {}, "No documents yet."),
    h("div", { class: "row" }, kind, file, h("button", { onclick: upload }, "Add document")), out);
}

function fundingPanel(c, id, refresh) {
  const f = c.funding;
  const canAct = ["Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
  const ta = h("textarea", { "aria-label": "Funding application draft", rows: 10 });
  ta.value = f.draft || "";
  const ref = h("input", { "aria-label": "Reference from the funder", placeholder: "Reference from the funder" });
  const step = (action, text) => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/funding`, { action, text }));
  if (f.status === "Confirmed") {
    return h("section", { class: "card" }, h("h2", {}, "Funding"), h("p", {}, `Confirmed. Route: ${f.route}${f.reference ? `, reference ${f.reference}` : ""}.`));
  }
  const need = c.checklist.filter((x) => !x.present).map((x) => x.kind);
  return h("section", { class: "card" }, h("h2", {}, "Funding application"),
    h("p", {}, `Route: ${f.route}. Status: ${f.status}.${need.length ? ` Still needed: ${need.join(", ")}.` : " All evidence is in."}`),
    h("p", { class: "muted" }, "AI drafts the wording. A person approves it and submits it to the funder. The system never submits."),
    h("div", { class: "row" }, h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/funding-draft`, {})) }, "Draft application with AI")),
    ta,
    canAct ? h("div", { class: "row" },
      h("button", { class: "alt", onclick: () => step("save_draft", ta.value) }, "Save my changes"),
      f.status === "Draft ready" && h("button", { onclick: () => step("approve") }, `Approve as ${me.user.name}`),
      f.status === "Approved" && [ref, h("button", { onclick: () => step("submit", ref.value) }, "Record that I submitted it")],
      f.status === "Submitted" && h("button", { onclick: () => step("confirm") }, "Funder confirmed the award"))
      : h("p", { class: "muted" }, "The Grants and Evidence Officer or a manager approves and submits."),
    f.approved_by && h("p", { class: "muted" }, `Approved by ${f.approved_by}.`));
}

function importView() {
  const out = h("div", {});
  const file = h("input", { type: "file", accept: ".csv,text/csv", id: "f" });
  file.addEventListener("change", async () => {
    const text = await file.files[0].text();
    try {
      const r = await api("/api/import-check", { text });
      out.replaceChildren(
        h("p", { class: "notice" }, r.message),
        h("p", {}, `${r.ready} rows are ready to bring in. ${r.matched_existing} match a home we already hold.`),
        h("p", {}, "We found these columns: ", Object.entries(r.columns).map(([k, v]) => `${k}: ${v || "not found"}`).join("; ")),
        r.to_fix.length ? h("div", {}, h("h2", {}, "Rows to fix"), h("ul", {}, r.to_fix.map((x) => h("li", {}, `Row ${x.row}: ${x.problem}`)))) : h("p", {}, "No rows need fixing."));
    } catch (e) { out.replaceChildren(h("p", { class: "err" }, e.message)); }
  });
  show(h("a", { class: "back", href: "#/" }, "Back to the list"), h("h1", {}, "Check a spreadsheet"),
    h("p", {}, "Choose any spreadsheet saved as CSV. We match the columns for you and list anything to fix. Your file is never changed."),
    h("label", { for: "f" }, "Spreadsheet (CSV)"), file, out);
}

document.getElementById("signout").addEventListener("click", async () => { await api("/api/logout", {}); me = null; briefingBox = null; login(); });
window.addEventListener("hashchange", () => me && route());
start().catch(() => login());

// ---- Overview, Visits, Funding screens
const NS = "http://www.w3.org/2000/svg";
const svg = (tag, attrs, ...kids) => {
  const el = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) el.setAttribute(k, v);
  kids.flat().forEach((k) => k && el.append(k.nodeType ? k : document.createTextNode(k)));
  return el;
};

function bars(title, data, link) {
  const max = Math.max(1, ...data.map((d) => d.n));
  const rowH = 24;
  const g = svg("svg", { viewBox: `0 0 480 ${data.length * rowH + 4}`, class: "chart", role: "img", "aria-label": title },
    data.map((d, i) => {
      const bar = svg("g", {}, svg("text", { x: 0, y: i * rowH + 16, class: "lbl" }, d.label),
        svg("rect", { x: 190, y: i * rowH + 4, width: Math.max(2, (d.n / max) * 240), height: 16, class: "bar" }),
        svg("text", { x: 190 + (d.n / max) * 240 + 6, y: i * rowH + 16, class: "lbl" }, String(d.n)));
      return bar;
    }));
  return h("section", { class: "card" }, h("h2", {}, title), g, link);
}

const OV_TILES = [["", "Open cases"], ["hazard", "Safety issues open"], ["long", "Waiting 60+ days"], ["nodecision", "Awaiting resident decision"], ["fundingprog", "Funding in progress"], ["support", "Residents needing extra support"]];
const ovState = { flag: "", area: "" };

function mapPanel() {
  const el = h("div", { id: "leaflet", class: "leafmap", role: "region", "aria-label": "Map of open cases. Zoom with the buttons, mouse wheel or pinch." });
  const info = h("p", { class: "muted", role: "status" });
  const open = h("a", { href: "#/all" }, "Show these as a list");
  let map = null, layer = null;
  const KIND = { normal: "#0b5d6b", long: "#d98a00", hazard: "#b42318" };
  let fitting = false, seq = 0;
  const draw = async (fit) => {
    const my = ++seq;
    open.onclick = () => { Object.assign(listState, { flag: ovState.flag === "fundingprog" ? "funding" : ovState.flag, area: ovState.area }); };
    if (!map) {
      map = L.map(el, { scrollWheelZoom: true }).setView([54.9, -1.6], 9);
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, referrerPolicy: "strict-origin-when-cross-origin",
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
      layer = L.layerGroup().addTo(map);
      map.on("moveend", () => { if (!fitting) draw(false); });
    }
    const b = map.getBounds();
    const view = fit ? "" : `&bbox=${[b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].join(",")}`;
    const d = await api(`/api/map?${qs(ovState)}&zoom=${map.getZoom()}${view}`);
    if (my !== seq) return;
    info.textContent = d.mode === "clusters"
      ? `${d.total} homes in this view, grouped into ${d.shown} areas. Zoom in to see each home.`
      : `${d.total} ${d.total === 1 ? "home" : "homes"} shown`;
    layer.clearLayers();
    d.items.forEach((p) => {
      if (d.mode === "clusters") {
        const m = L.marker([p.lat, p.lon], { icon: L.divIcon({ className: "", html: `<div class="cluster${p.hazards ? " hazard" : ""}">${p.count}</div>`, iconSize: [34, 34] }),
          keyboard: false, title: `${p.count} homes${p.hazards ? `, ${p.hazards} with a safety issue open` : ""}` });
        m.on("click", () => map.setView([p.lat, p.lon], Math.min(map.getZoom() + 2, 18)));
        m.addTo(layer);
        return;
      }
      const m = L.circleMarker([p.lat, p.lon], { radius: p.kind === "hazard" ? 8 : 6, color: "#fff", weight: 1.5, fillColor: KIND[p.kind], fillOpacity: 0.9 });
      m.bindTooltip(`${p.name}`, { direction: "top" });
      m.on("click", () => { location.hash = `#/case/${encodeURIComponent(p.id)}`; });
      m.addTo(layer);
    });
    if (fit && d.bounds) {
      fitting = true;
      map.fitBounds([[d.bounds[0], d.bounds[1]], [d.bounds[2], d.bounds[3]]], { padding: [30, 30], maxZoom: 15, animate: false });
      fitting = false;
      draw(false);
    }
  };
  const box = h("section", { class: "card" }, h("h2", {}, "Map of open cases"),
    h("p", {}, h("span", { class: "key normal" }, "Normal"), h("span", { class: "key long" }, "Waiting 60+ days"), h("span", { class: "key hazard" }, "Safety issue open")),
    el, h("div", { class: "row between" }, info, open));
  return { box, draw, size: () => map && map.invalidateSize() };
}

async function overviewView() {
  const st = await api("/api/stats");
  const k = st.kpis;
  const counts = { "": k.open, hazard: k.hazards, long: k.long, nodecision: k.nodecision, fundingprog: k.funding, support: k.support };
  const mp = mapPanel();
  const tiles = h("div", { class: "tiles", role: "group", "aria-label": "Choose what the map shows" });
  const paint = () => tiles.replaceChildren(...OV_TILES.map(([f, label]) => h("button", { class: `tile${f === "hazard" ? " danger" : ""}`, "aria-pressed": String(ovState.flag === f),
    onclick: () => { ovState.flag = f; paint(); mp.draw(true); } }, h("strong", {}, String(counts[f])), h("span", {}, label))),
    h("div", { class: "tile static" }, h("strong", {}, String(k.completed)), h("span", {}, "Completed")));
  paint();
  const area = h("select", { id: "mapArea", onchange: (e) => { ovState.area = e.target.value; mp.draw(true); } },
    h("option", { value: "" }, "All areas"), st.areas.map((a) => h("option", { value: a.label }, a.label)));
  area.value = ovState.area;
  show(
    h("h1", {}, "Overview"), tiles,
    h("div", { class: "row" }, h("label", { for: "mapArea" }, "Show map for"), area), mp.box,
    h("div", { class: "grid" }, bars("Cases by stage", st.stages), bars("Cases by local authority", st.areas)),
    h("div", { class: "grid" }, bars("How long cases have waited", st.ages), bars("Cases by wave", st.waves)),
    h("div", { class: "grid" }, bars("Funding status", st.funding),
      h("section", { class: "card" }, h("h2", {}, "Contractors"), h("table", {}, h("thead", {}, h("tr", {}, ["Contractor", "Open", "On site or booked", "Stuck 60+ days"].map((x) => h("th", {}, x)))),
        h("tbody", {}, st.contractors.map((c) => h("tr", {}, h("td", {}, c.name), h("td", {}, c.open), h("td", {}, c.booked), h("td", {}, c.long))))))),
    h("section", { class: "card" }, h("h2", {}, "Team workload"), h("table", {}, h("thead", {}, h("tr", {}, ["Name", "Role", "Open cases", "With a safety issue"].map((x) => h("th", {}, x)))),
      h("tbody", {}, st.team.map((t) => h("tr", {}, h("td", {}, t.name), h("td", {}, t.role), h("td", {}, t.open), h("td", {}, t.hazards)))))));
  mp.size();
  await mp.draw(true);
}

async function visitsView() {
  const isMgr = ["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
  const rows = await api("/api/visits?view=" + (isMgr ? "all" : "mine"));
  const days = {};
  rows.forEach((v) => (days[v.date] = days[v.date] || []).push(v));
  show(h("div", { class: "row between" }, h("h1", {}, "Visits coming up"),
    h("span", { class: "muted" }, isMgr ? "Everyone's visits" : "Your visits")),
    rows.length ? Object.entries(days).map(([d, vs]) => h("section", { class: "card" }, h("h2", {}, fmtDate(d)),
      h("ul", { class: "list" }, vs.map((v) => h("li", {}, h("a", { href: `#/case/${encodeURIComponent(v.id)}` }, `${v.slot} ${v.resident}`),
        ` ${v.type}. ${v.address}. ${v.who}: ${v.person}.`, v.support && h("span", { class: "flag" }, "Extra support"), ` Call ${v.phone}`))))) : h("p", {}, "No booked visits."));
}

async function fundingView() {
  const rows = await api("/api/funding");
  show(h("h1", {}, "Funding applications"),
    h("p", { class: "muted" }, "Homes where funding is not yet confirmed. Open one to draft the application with AI, add evidence, and have it approved."),
    h("table", {}, h("thead", {}, h("tr", {}, ["Resident", "Area", "Route", "Status", "Evidence", "Owner"].map((x) => h("th", {}, x)))),
      h("tbody", {}, rows.slice(0, 150).map((r) => h("tr", {}, h("td", {}, h("a", { href: `#/case/${encodeURIComponent(r.id)}` }, r.resident)),
        h("td", {}, r.area), h("td", {}, r.route), h("td", {}, r.status), h("td", {}, `${r.have} of ${r.need}`), h("td", {}, r.owner))))));
}
