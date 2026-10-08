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
  return listView(location.hash === "#/all" ? "all" : "mine");
}

async function listView(view, q = "") {
  const isMgr = ["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
  const rows = await api(`/api/cases?view=${view}&q=${encodeURIComponent(q)}`);
  const hz = rows.filter((r) => r.hazard).length;
  const search = h("input", { type: "search", "aria-label": "Find a resident, address or postcode", placeholder: "Find a resident, address or postcode", value: q });
  const go = () => listView(view, search.value);
  search.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
  const items = rows.slice(0, 100).map((r) => h("li", {},
    h("a", { class: "item", href: `#/case/${encodeURIComponent(r.id)}` },
      h("div", {}, h("span", { class: "name" }, r.resident),
        r.hazard && h("span", { class: "flag danger" }, "Safety issue open"),
        r.support && h("span", { class: "flag" }, "Needs extra support"),
        h("div", {}, `${r.address}, ${r.town} ${r.postcode}`),
        h("div", { class: "status" }, r.status)),
      h("div", { class: "meta" }, h("div", {}, r.stage), h("div", {}, `Last contact: ${ago(r.last_contact)}`),
        r.next_visit && h("div", {}, `Visit: ${fmtDate(r.next_visit)}`)))));
  show(
    h("div", { class: "row between" },
      h("h1", {}, view === "mine" ? "My cases today" : "All open cases"),
      h("div", { class: "row" },
        isMgr && h("a", { class: "btn alt", href: view === "mine" ? "#/all" : "#/" }, view === "mine" ? "See everyone's cases" : "See my cases"),
        h("a", { class: "btn alt", href: "#/import" }, "Check a spreadsheet"),
        h("a", { class: "btn alt", href: `/api/cases.csv?view=${view}&q=${encodeURIComponent(q)}`, download: "cases.csv" }, "Download for Excel"))),
    h("p", { class: "muted" }, `${rows.length} cases${hz ? `, ${hz} with a safety issue open (shown first)` : ""}`),
    h("div", { class: "row" }, search, h("button", { onclick: go }, "Find")),
    h("ul", { class: "list" }, items.length ? items : h("li", { class: "card" }, "Nothing here. You are all caught up.")),
    rows.length > 100 && h("p", { class: "muted" }, "Showing the first 100. Use Find to narrow the list."));
}

async function caseView(id) {
  const c = await api(`/api/cases/${encodeURIComponent(id)}`);
  const r = c.resident, hm = c.home;
  const openHaz = c.hazards.filter((x) => !x.released);
  const msg = h("div", { role: "status" });
  const refresh = async (fn) => {
    try { await fn(); await caseView(id); } catch (e) {
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
    c.can_advance && h("section", { class: "card" }, h("h2", {}, "Final checks"),
      c.gate.length ? [h("p", {}, "This case cannot move on yet:"), h("ul", {}, c.gate.map((x) => h("li", {}, x)))] : h("p", {}, "Everything is in place."),
      h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/advance`, {})) }, "Ready to book the installation")),
    h("section", { class: "card" }, h("h2", {}, "Write to the resident"),
      h("div", { class: "row" }, h("button", { class: "alt", onclick: () => kind("visit") }, "Draft a visit request"),
        h("button", { class: "alt", onclick: () => kind("update") }, "Draft an update")), draftBox),
    msg,
    h("section", { class: "card" }, h("h2", {}, "History"),
      c.contacts.length ? h("ul", { class: "tl" }, c.contacts.slice(0, 15).map((k) => h("li", {},
        h("strong", {}, `${fmtDate(k.at)} ${k.channel}: ${k.outcome}`), h("div", { class: "muted" }, `${k.by}${k.note ? `. ${k.note}` : ""}`)))) : h("p", {}, "No contact recorded yet.")));
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

document.getElementById("signout").addEventListener("click", async () => { await api("/api/logout", {}); me = null; login(); });
window.addEventListener("hashchange", () => me && route());
start().catch(() => login());
