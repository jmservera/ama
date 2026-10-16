"use strict";
const app = document.getElementById("app");
let me = null;
const microsoftSignIn = document.body.dataset.authProvider === "trusted-proxy";
let photoUrl = null;
let routeController = new AbortController();
let searchTimer = 0;
let queueOrigin = "mine";
let resetFocus = false;
const workspaceStatus = document.getElementById("workspace-status");

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

async function api(path, body, signal) {
  signal = signal || routeController.signal;
  const res = await fetch(path, body === undefined ? { signal } : {
    method: "POST", headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" }, body: JSON.stringify(body), signal,
  });
  const data = await res.json().catch(() => ({}));
  signal.throwIfAborted();
  if (res.status === 401 && path !== "/api/login") { me = null; login("Your session has ended. Sign in again."); throw new Error("Your session has ended. Sign in again."); }
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
const show = (...nodes) => { app.replaceChildren(...nodes.flat().filter((n) => n && n.nodeType)); app.focus(); };

function login(msg) {
  workspaceStatus.textContent = "";
  document.getElementById("nav").hidden = true;
  document.getElementById("account").hidden = true;
  clearPhoto();
  if (microsoftSignIn) {
    show(h("section", { class: "card login" }, h("h1", {}, "Sign in to Zava Forward"),
      h("p", { class: "err", role: "alert" }, msg || "Use your authorised Microsoft work account."),
      h("a", { class: "btn", href: "/sign-in" }, "Sign in with Microsoft"),
      h("p", {}, h("a", { href: "/" }, "Back to welcome"))));
    return;
  }
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
  Object.assign(listState, defaultListState());
  queueOrigin = "mine";
  briefingBox = null;
  document.getElementById("who").textContent = `${me.user.name}, ${me.user.role}`;
  showAccount();
  const nav = document.getElementById("nav");
  nav.replaceChildren(...me.navigation.map((item) => h("a", { href: item.href }, item.label)));
  nav.hidden = false;
  route();
}

function clearPhoto() {
  if (photoUrl) URL.revokeObjectURL(photoUrl);
  photoUrl = null;
  const picture = document.getElementById("account-photo");
  picture.hidden = true;
  picture.removeAttribute("src");
  document.getElementById("account-initials").hidden = false;
}

function showAccount() {
  clearPhoto();
  const account = me.account || { name: me.user.name, email: "" };
  document.getElementById("account-name").textContent = account.name;
  document.getElementById("account-short").textContent = account.name.split(/\s+/)[0] || "Account";
  document.getElementById("account-email").textContent = account.email;
  document.getElementById("who").textContent = me.user.role;
  document.getElementById("account-initials").textContent = account.name.trim().split(/\s+/).slice(0, 2).map((n) => n[0]).join("").toUpperCase();
  document.getElementById("switch-account").hidden = !microsoftSignIn;
  document.getElementById("account-error").textContent = "";
  document.getElementById("account").hidden = false;
  const status = document.getElementById("photo-status");
  status.textContent = microsoftSignIn ? "Loading Microsoft profile photo..." : "Local development account";
  if (microsoftSignIn) loadPhoto(account);
}

async function loadPhoto(account) {
  const status = document.getElementById("photo-status");
  try {
    let res = await fetch("/api/account/photo");
    if (res.status === 401) {
      const refresh = await fetch("/.auth/refresh");
      if (!refresh.ok) throw new Error("Microsoft photo access has expired. Sign in again.");
      res = await fetch("/api/account/photo");
    }
    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.error || "Microsoft profile photo is unavailable.");
    }
    const blob = await res.blob();
    if (!me || me.account !== account) return;
    photoUrl = URL.createObjectURL(blob);
    const picture = document.getElementById("account-photo");
    picture.src = photoUrl;
    picture.hidden = false;
    document.getElementById("account-initials").hidden = true;
    status.textContent = "Microsoft profile photo";
  } catch (e) {
    if (me && me.account === account) status.textContent = e.message;
  }
}

async function route() {
  routeController.abort();
  routeController = new AbortController();
  clearTimeout(searchTimer);
  const signal = routeController.signal;
  const hash = location.hash || "#/";
  const m = location.hash.match(/^#\/case\/(.+)$/);
  const active = m ? (queueOrigin === "all" ? "#/all" : "#/") : hash;
  document.querySelectorAll("#nav a").forEach((link) => {
    if (link.getAttribute("href") === active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  const destination = me.navigation.find((item) => item.href === active);
  workspaceStatus.textContent = `${me.user.role}. ${destination?.scope || "Case workspace"}.`;
  try {
  if (me.user.role === "Contractor") return await (m ? contractorCaseView(decodeURIComponent(m[1])) : contractorListView());
  if (m) return await caseView(decodeURIComponent(m[1]));
  const building = location.hash.match(/^#\/building\/(.+)$/);
  if (building) return await buildingView(decodeURIComponent(building[1]));
  if (hash === "#/assistants") return await assistantQueueView();
  if (hash === "#/time") return await timeView();
  if (hash === "#/closed") return await closedView();
  if (hash === "#/capacity") return await capacityView();
  if (hash === "#/import") return await importView();
  if (hash === "#/overview") return await overviewView();
  if (hash === "#/visits") return await visitsView();
  if (hash === "#/funding") return await fundingView();
  if (hash === "#/finance") return await financeQueueView();
  return await listView(hash === "#/all" ? "all" : "mine");
  } catch (error) {
    if (signal.aborted || !me) return;
    workspaceStatus.textContent = `Workspace unavailable: ${error.message}`;
    show(h("h1", {}, "Workspace unavailable"), h("p", { class: "err", role: "alert" }, error.message),
      h("button", { onclick: route }, "Try again"));
  }
}

const defaultListState = () => {
  const { view, ...filters } = me.work_queues?.default || {};
  return filters;
};
const listState = {};
const queueHref = () => queueOrigin === "all" ? "#/all" : "#/";
const qs = (o) => Object.entries(o).filter(([, v]) => v).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join("&");
const isManager = () => ["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
const FLAGS = [["hazard", "Safety issue open"], ["support", "Needs extra support"], ["long", "Waiting 60+ days"], ["nodecision", "No resident decision yet"], ["funding", "Funding not confirmed"]];

// Workflow-only mode: the person can choose rules and templates instead of AI. It is recorded with each output.
const aiMode = { workflow: false };
const modeBody = (o) => (aiMode.workflow ? { ...o, mode: "workflow" } : o);

// Sources, approval state and the review buttons shown beside every AI-drafted output.
function aiNotes(d, onDone, getText) {
  if (!d) return null;
  const kids = [];
  if (d.reason) kids.push(h("p", { class: "muted", role: "status" }, d.reason));
  if (d.verified === false || d.validated === false) kids.push(h("p", { class: "flag danger", role: "status" }, "Unverified: its sources do not match the case record. Check it before use."));
  const cites = d.citations || [];
  if (cites.length) kids.push(h("p", { class: "muted" }, "Sources: " + cites.join("; ")));
  if (d.dropped_uncited) kids.push(h("p", { class: "muted" }, `${d.dropped_uncited} uncited statement(s) removed.`));
  kids.push(h("p", { class: "muted" }, d.approval === "Not reviewed" ? "AI suggestion, not approved. Not reviewed by a person yet." : `${d.approval} as a draft by a person. This is not an approval, consent or safety decision.`));
  if (d.record_id && d.approval === "Not reviewed") {
    const why = h("input", { type: "text", maxlength: 300, placeholder: "Reason (needed to edit or reject)", "aria-label": "Reason for your review" });
    const go = (action) => async () => {
      try { await api(`/api/ai/review/${d.record_id}/${action}`, { reason: why.value, text: action === "edit" ? getText && getText() : undefined }); d.approval = REVIEWED[action]; onDone ? onDone() : box.replaceChildren(h("p", { class: "muted" }, `${d.approval} as a draft. This is not an approval, consent or safety decision. Recorded in the audit log.`)); }
      catch (e) { why.setCustomValidity(e.message); why.reportValidity(); }
    };
    const box = h("div", { class: "row" }, why, h("button", { class: "alt", onclick: go("accept") }, "Accept as is"),
      h("button", { class: "alt", onclick: go("edit") }, "I changed it"), h("button", { class: "alt", onclick: go("reject") }, "Reject"));
    kids.push(box);
  }
  return h("div", { class: "aimeta" }, kids);
}
const REVIEWED = { accept: "Accepted", edit: "Edited", reject: "Rejected" };

function aiBox() {
  const box = h("section", { class: "card ai" }, h("h2", {}, "Today's briefing"), h("p", { class: "muted" }, "Reading your cases..."));
  const toggle = h("input", { type: "checkbox", id: "wf-mode", checked: aiMode.workflow, onchange: () => { aiMode.workflow = toggle.checked; load(); } });
  const load = () => {
    const signal = routeController.signal;
    const cancel = () => { if (briefingBox === box) briefingBox = null; };
    signal.addEventListener("abort", cancel, { once: true });
    return api(`/api/briefing${aiMode.workflow ? "?mode=workflow" : ""}`, undefined, signal).then((b) => box.replaceChildren(h("h2", {}, "Today's briefing"), h("p", {}, b.text),
      h("p", { class: "muted" }, `${b.label}. Suggestions only. Refreshed when your cases change.`), aiNotes(b),
      h("p", {}, toggle, h("label", { for: "wf-mode" }, " Workflow only (no AI) for my AI requests"))))
      .catch((error) => {
        if (signal.aborted) { box.remove(); return; }
        box.replaceChildren(h("h2", {}, "Today's briefing"),
          h("p", { class: "err", role: "alert" }, `Briefing unavailable: ${error.message}`),
          h("button", { onclick: load }, "Try loading briefing again"));
      })
      .finally(() => signal.removeEventListener("abort", cancel));
  };
  load();
  return box;
}

function priorityPanel() {
  const box = h("section", { class: "card ai", "aria-label": "AI priority suggestion" });
  const rowsOf = (items, withReason) => h("ol", {}, items.map((i) => h("li", {},
    h("a", { href: `#/case/${encodeURIComponent(i.case_id)}` }, `${i.resident}, ${i.address}`), ` (rank ${i.rank})`,
    withReason && i.reason ? h("div", { class: "muted" }, i.reason, i.cites && i.cites.length ? ` Sources: ${i.cites.join("; ")}.` : "") : null)));
  const paint = (rec, msg) => {
    const kids = [h("h2", {}, "Which cases first? A second opinion"),
      h("p", { class: "muted" }, "The rule-based order below is the list order. The AI suggestion, not approved, is advice only: it never changes the ranking, owners, stages or queues.")];
    if (msg) kids.push(h("p", { role: "alert" }, msg));
    if (rec && rec.release_denied) kids.push(h("p", { role: "status" }, "This suggestion's release is no longer valid. Use the ordinary case controls or request a new suggestion. The release owner must review the missing evidence."));
    if (!rec) {
      kids.push(h("p", {}, h("button", { class: "alt", onclick: ask }, "Suggest my top 5")));
    } else {
      kids.push(h("div", { class: "grid" },
        h("div", {}, h("h3", {}, `Rule-based order (policy ${rec.policy_version})`), rowsOf(rec.deterministic, false)),
        h("div", {}, h("h3", {}, `Suggestion: ${rec.label}`), rowsOf(rec.items, true),
          h("p", { class: "muted" }, `${rec.source === "ai" ? "Written by AI" : `Written by rules: ${rec.fallback_reason || "AI not available"}`}. ${rec.validated === false ? "Unverified. " : ""}${rec.overlap} of ${rec.items.length} match the rule-based top ${rec.n}.`))));
      if (rec.status === "Proposed") {
        const why = h("input", { id: "pri-why", type: "text", placeholder: "Reason (needed to edit or reject)", maxlength: 300 });
        const keep = rec.items.map((i) => h("input", { type: "checkbox", checked: true, "aria-label": `Keep ${i.resident}` }));
        const act = (action) => async () => {
          const items = rec.items.filter((_, n) => keep[n].checked).map((i) => ({ case_id: i.case_id, reason: i.reason }));
          try { paint(await api(`/api/ai/priority/${rec.id}/${action}`, { reason: why.value, items })); } catch (e) { paint(rec, e.message); }
        };
        kids.push(h("div", { class: "row" }, h("label", { for: "pri-why" }, "Your reason"), why),
          h("div", { class: "row" }, h("span", { class: "muted" }, "To edit, untick cases to drop:"), rec.items.map((i, n) => h("label", {}, keep[n], ` ${i.resident}`))),
          h("div", { class: "row" }, h("button", { disabled: rec.actionable === false, onclick: act("accept") }, "Accept"), h("button", { class: "alt", disabled: rec.actionable === false, onclick: act("edit") }, "Edit"),
            h("button", { class: "alt", onclick: act("reject") }, "Reject")));
      } else {
        kids.push(h("p", {}, `${rec.status}${rec.reason ? `: ${rec.reason}` : ""}. Recorded in the audit log.`),
          h("p", {}, h("button", { class: "alt", onclick: ask }, "Suggest again")));
      }
    }
    box.replaceChildren(...kids);
  };
  const ask = async () => { box.setAttribute("aria-busy", "true"); try { paint(await api("/api/ai/priority", modeBody({ n: 5 }))); } catch (e) { paint(null, e.message); } box.removeAttribute("aria-busy"); };
  api("/api/ai/priority").then((d) => paint(d.recommendation && d.recommendation.status === "Proposed" ? d.recommendation : null)).catch(() => paint(null));
  return box;
}

function pendingHandoffs() {
  const box = h("section", { class: "card", "aria-label": "Handoffs waiting for you", hidden: true });
  api("/api/handoffs").then((rows) => {
    if (!rows.length) return;
    box.hidden = false;
    box.replaceChildren(h("h2", {}, "Handoffs waiting for you"), h("ul", { class: "list" }, rows.map((x) => h("li", {},
      h("a", { href: `#/case/${encodeURIComponent(x.case_id)}` }, `${x.resident}, ${x.address}`),
      h("div", { class: "muted" }, `${x.status}. Current owner: ${x.accountable_owner}; proposed receiver: ${x.proposed_receiver || "Unassigned"}; confirmed receiver: ${x.confirmed_receiver || "Unconfirmed"}; destination: ${x.destination || "Unknown"}; chase: ${x.chase_owner || "Unassigned"}.`),
      h("div", { class: "muted" }, `Urgency: ${x.urgency || "Unknown"}; due: ${x.due_at || "Unknown"}; next action: ${x.next_action || "Unknown"}. Resident update: ${x.resident_update_owner || "Unassigned"}, ${x.resident_update_due_at || "Unknown"}.`),
      h("div", {}, x.to_code === me.user.code ? "Open to record receipt, accept or decline." : "Open to chase, escalate or withdraw.")))));
  }).catch((e) => { box.hidden = false; box.replaceChildren(h("p", { role: "alert" }, `Could not load handoffs: ${e.message}`)); });
  return box;
}

let briefingBox = null;
function workSummary(work) {
  return h("div", { class: "work-context" },
    h("p", {}, `Current owner: ${work.owner}. Reason: ${work.reason}.`),
    h("p", { class: "next-action" }, `Next action: ${work.next_action}`),
    h("p", { class: "muted" }, `Source: ${work.source}; evidence: ${work.evidence}; version: ${work.version}; recorded: ${work.recorded_at}; snapshot: ${work.as_of}.`),
    work.handoff && h("p", {}, `Destination: ${work.handoff.destination}; proposed receiver: ${work.handoff.proposed_receiver}; confirmed receiver: ${work.handoff.confirmed_receiver}; chase owner: ${work.handoff.chase_owner}; resident-update owner: ${work.handoff.resident_update_owner}.`),
    work.hazard_clocks.map((clock) => h("p", { class: "safety-clock" },
      `Safety clock at snapshot: ${clock.elapsed_hours === null ? "Unknown" : `${clock.elapsed_hours} elapsed hours`}; awareness: ${clock.aware_at}; named follow-up owner: ${clock.owner}; service response due: ${clock.response_due_at}; resident update due: ${clock.resident_update_due_at}. ${clock.authority} owns timing.`)));
}

function workSteps(work) {
  return h("section", { class: "card", "aria-label": "Recorded task context" },
    h("h2", {}, "Recorded task context"), workSummary(work),
    work.blockers.length ? h("details", {}, h("summary", {}, "Blocked steps and prerequisites"),
      h("ul", {}, work.blockers.map((step) => h("li", {},
        `${step.step} (${step.current_stop ? "current stop" : "final-check prerequisite"}): ${step.reason} Named owner: ${step.owner}. Responsible role: ${step.responsible_role}. Next action: ${step.next_action}`,
        h("p", { class: "muted" }, `Source: ${step.source}; version: ${step.version}.`))))) : h("p", {}, "No recorded blockers."),
    work.overdue.length > 0 && h("ul", {}, work.overdue.map((task) => h("li", {},
      `${task.task}: due ${task.due_at}; owner: ${task.owner}; completion: ${task.completion}.`))),
    h("details", {}, h("summary", {}, "Task sources"),
      h("p", {}, `Case ${work.case_id}; definition ${work.definition_version}; snapshot ${work.as_of}. Missing evidence stays Unknown; freshness does not establish validity.`),
      h("ul", {}, work.evidence_freshness.map((item) => h("li", {},
        `${item.kind}: ${item.status}; record date: ${item.recorded_at}; evidence: ${item.evidence}; source: ${item.source}; version: ${item.version}.`)))));
}

async function listView(view) {
  queueOrigin = view;
  const signal = routeController.signal;
  const fx = await api("/api/facets");
  if (!briefingBox) briefingBox = aiBox();
  const results = h("div", { "aria-live": "polite" });
  const title = h("h1", {}, view === "mine" ? "My cases today" : "All open cases");
  const csv = h("a", { class: "btn alt", download: "cases.csv" }, "Download for Excel");
  let seq = 0;
  let rows = [], total = 0, policy = "", cursor = null;
  const PAGE = 50;
  const render = () => {
    workspaceStatus.textContent = `${me.user.role}. ${view === "mine" ? "My assigned cases" : "All permitted open cases"}. ${total} ${total === 1 ? "case" : "cases"}. Search: ${listState.q || "none"}. Stage: ${listState.stage || "any"}. Area: ${listState.area || "any"}. Wave: ${listState.wave || "any"}. Owner: ${listState.owner || "any"}. Show only: ${listState.flag || "any"}. Work queue: ${listState.queue || "any"}. Order: ${fx.sorts[listState.sort]}. Default: ${me.work_queues.version}; selection: none.`;
    results.replaceChildren(...[
      h("p", { class: "muted" }, `${total} ${total === 1 ? "case" : "cases"}${listState.sort === "urgent" ? `. Ranked by policy version ${policy}, a fixed rule order (safety first). The order is the same every time.` : ""}`),
      h("ul", { class: "list" }, rows.length ? rows.map((r) => h("li", {},
        h("a", { class: "item", href: `#/case/${encodeURIComponent(r.id)}` },
          h("div", {}, h("span", { class: "name" }, r.resident),
            r.hazard && h("span", { class: "flag danger" }, "Safety issue open"),
            r.support && h("span", { class: "flag" }, "Needs extra support"),
            h("div", {}, `${r.address}, ${r.town} ${r.postcode}`),
            h("div", { class: "status" }, r.status),
            workSummary(r.work),
            h("div", { class: "muted" }, `Queue reasons: ${r.work.queues.map((key) => me.work_queues.definitions.find((d) => d.id === key).label).join(", ") || "None under these definitions"}`),
            h("div", { class: "muted" }, `Rank ${r.rank}: ${r.reasons.slice(0, 3).join("; ")}`),
            view === "all" && h("div", { class: "muted" }, `Owner: ${r.owner}`),
            r.focus && h("dl", { class: "focus" }, r.focus.flatMap(([k, v]) => [h("dt", {}, k), h("dd", {}, /^\d{4}-\d\d-\d\d$/.test(v) ? fmtDate(v) : v)]))),
          h("div", { class: "meta" }, h("div", {}, r.stage), h("div", {}, `${r.days} days in this stage`), h("div", {}, `Last contact: ${ago(r.last_contact)}`),
            r.next_visit && h("div", {}, `Visit: ${fmtDate(r.next_visit)}`))))) : h("li", { class: "empty" }, Object.entries(listState).some(([key, value]) => key !== "sort" && value) ? "No cases match these filters. Reset my queue to try again." : view === "mine" ? "No open cases are assigned to you. This does not mean the programme has no work." : "No permitted open cases are available.")),
      rows.length < total ? h("p", {}, h("button", { class: "alt", onclick: () => load(true) }, `Show more (${rows.length} of ${total} shown)`)) : null].filter(Boolean));
  };
  const load = async (more) => {
    const my = ++seq;
    const paging = more && cursor ? `after=${encodeURIComponent(cursor)}` : `offset=${more ? rows.length : 0}`;
    let d;
    try { d = await api(`/api/cases?view=${view}&${qs(listState)}&limit=${PAGE}&${paging}`, undefined, signal); }
    catch (error) {
      if (signal.aborted || my !== seq || !me) return;
      workspaceStatus.textContent = `Cases unavailable: ${error.message}`;
      results.replaceChildren(h("p", { class: "err", role: "alert" }, error.message),
        h("button", { onclick: () => load(false) }, "Try loading cases again"));
      return;
    }
    if (signal.aborted || my !== seq) return;
    cursor = d.next_cursor || null;
    csv.href = `/api/cases.csv?view=${view}&${qs(listState)}`;
    rows = more ? rows.concat(d.items) : d.items;
    total = d.total;
    policy = d.policy_version;
    render();
    if (resetFocus) { resetFocus = false; document.getElementById("reset-queue").focus(); }
  };
  const field = (label, key, opts) => {
    const el = h("select", { id: `f-${key}` }, h("option", { value: "" }, "Any"), opts.map(([v, t]) => h("option", { value: v }, t)));
    el.value = listState[key];
    el.addEventListener("change", () => { listState[key] = el.value; load(); });
    return [h("label", { for: `f-${key}` }, label), el];
  };
  const search = h("input", { id: "f-q", type: "search", placeholder: "Name, address or postcode" });
  search.value = listState.q;
  search.addEventListener("input", () => { listState.q = search.value; clearTimeout(searchTimer); searchTimer = setTimeout(() => load(), 250); });
  const sort = h("select", { id: "f-sort" }, Object.entries(fx.sorts).map(([k, t]) => h("option", { value: k }, t)));
  sort.value = listState.sort;
  sort.addEventListener("change", () => { listState.sort = sort.value; load(); });
  const side = h("aside", { class: "side", "aria-label": "Filters" }, h("h2", {}, "Filter"),
    h("label", { for: "f-q" }, "Find"), search,
    field("Stage", "stage", fx.stages.map((x) => [x, x])),
    field("Local authority", "area", fx.areas.map((x) => [x, x])),
    field("Wave", "wave", fx.waves.map((x) => [x, x])),
    view === "all" && field("Owner", "owner", me.staff.map((x) => [x.code, x.name])),
    field("Work queue", "queue", me.work_queues.definitions.map((d) => [d.id, d.label])),
    field("Show only", "flag", FLAGS),
    h("label", { for: "f-sort" }, "Sort by"), sort,
    h("p", {}, h("button", { id: "reset-queue", class: "alt", onclick: () => {
      clearTimeout(searchTimer);
      Object.assign(listState, defaultListState());
      resetFocus = true;
      if (location.hash && location.hash !== "#/") location.hash = "#/";
      else route();
    } }, "Reset my queue")),
    h("p", { class: "muted" }, `Default ${me.work_queues.version}: returns to your assigned cases, ${fx.sorts[me.work_queues.default.sort]}, first page and no case selection. No records change.`),
    h("details", {}, h("summary", {}, "Queue definitions"),
      h("p", {}, me.work_queues.status), h("p", {}, me.work_queues.clock),
      h("p", {}, "Your authenticated role determines access. Work queue, search and other filters narrow the chosen own/all scope together; they never change your role."),
      h("dl", {}, me.work_queues.definitions.flatMap((d) => [
        h("dt", {}, d.label), h("dd", {}, d.definition, d.limitation ? ` Unavailable: ${d.limitation}` : "")
      ]))));
  show(h("div", { class: "layout" }, side, h("div", { class: "main" },
    briefingBox,
    view === "mine" && pendingHandoffs(),
    view === "mine" && priorityPanel(),
    h("div", { class: "row between" }, title, h("div", { class: "row" },
      h("a", { class: "btn alt", href: view === "mine" ? "#/all" : "#/" }, view === "mine" ? "See all cases" : "See my cases"),
      h("a", { class: "btn alt", href: "#/import" }, "Check a spreadsheet"), csv)),
    results)));
  await load();
}

async function caseView(id) {
  const c = await api(`/api/cases/${encodeURIComponent(id)}`);
  const assistantPanel = assistantCasePanel(id);
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
  const draftBox = h("div", {});
  const kind = async (k) => {
    const d = await api(`/api/cases/${encodeURIComponent(id)}/draft`, { kind: k });
    draftBox.replaceChildren(h("p", { class: "muted" }, d.note), h("textarea", { "aria-label": "Draft message" }, d.text));
    draftBox.querySelector("textarea").value = d.text;
  };
  const aiRun = async (task) => {
    draftBox.replaceChildren(h("p", { class: "muted" }, "Working on it..."));
    try {
      const d = await api(`/api/cases/${encodeURIComponent(id)}/ai`, modeBody({ task }));
      const ta = h("textarea", { "aria-label": "Draft", rows: 9 });
      ta.value = d.text;
      draftBox.replaceChildren(h("p", { class: "muted" }, `${d.label}. Nothing is sent. Change it as you like.`), ta, aiNotes(d, null, () => ta.value));
    } catch (e) { draftBox.replaceChildren(h("p", { class: "err" }, e.message)); }
  };
  const canOffer = !c.closed && (c.owner_code === me.user.code || isManager()) &&
    (!c.handoff || !["Offered", "Received", "Escalated", "Accepted"].includes(c.handoff.state));
  const sugg = h("section", { class: "card" }, h("h2", {}, "Who could take this on"),
    h("p", { class: "muted" }, "Suggested by role and workload rules. You decide."),
    workSummary(c.work),
    h("p", {}, "These are proposed reviewers, not confirmed receiving owners. Review the recorded blocked steps and prerequisites above."),
    h("ul", { class: "list" }, c.suggestions.map((x) => h("li", {},
      h("strong", {}, `${x.name}, ${x.role}`), h("div", { class: "muted" }, x.reasons.join(". ")),
      canOffer && h("button", { class: "alt", onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/handover`, { to: x.email })) }, `Offer to ${x.name.split(" ")[0]}`)))));
  show(
    h("a", { class: "back", href: queueHref() }, "Back to the list"),
    c.building_id ? h("a", { class: "back", href: `#/building/${encodeURIComponent(c.building_id)}` }, `Shared building context: ${c.building_id}`) :
      h("p", { class: "muted" }, "Building link not recorded; shared context is unknown."),
    c.cost_allocation && h("section", { class: "card" }, h("h2", {}, "This home's cost allocation"),
      h("p", {}, "Recorded allocations only, not additional building costs or payment approval."),
      h("ul", {}, c.cost_allocation.map((x) => h("li", {}, `${x.shared_cost_id}: GBP ${x.amount_gbp}. Source: ${x.source}`)))),
    h("div", { class: "row between" },
      h("h1", {}, r.name, c.hazards.some((x) => !x.released) && h("span", { class: "flag danger" }, "Safety issue open")),
      h("span", { class: "muted" }, `Reference ${c.id}`)),
    h("div", { class: `status-line${openHaz.length ? " danger" : ""}`, role: "status" }, c.status),
    workSteps(c.work),
    safetyPanel(c, id, refresh),
    regulatoryAlertsPanel(id),
    h("div", { class: "grid" },
      h("section", { class: "card" }, h("h2", {}, "Contact"),
        h("div", { class: "big" }, h("a", { href: `tel:${r.phone.replace(/\s/g, "")}` }, r.phone)),
        r.email && h("div", {}, r.email),
        h("dl", {},
          h("dt", {}, "Address"), h("dd", {}, `${hm.address}, ${hm.town} ${hm.postcode}`),
          h("dt", {}, "Prefers"), h("dd", {}, r.preferred),
          h("dt", {}, "Not available"), h("dd", {}, r.unavailable || "No restrictions recorded"),
          h("dt", {}, "Support needs"), h("dd", {}, c.support_status === "Unknown" ? "Unknown" : r.adjustment === "None" ? "None recorded" : r.adjustment),
          h("dt", {}, "Support flag coverage"), h("dd", {}, c.support_coverage),
          r.priority_support === true && [h("dt", {}, "Flag"), h("dd", {}, "Needs extra support")],
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
          h("dt", {}, "Historical case-wide answer (not scope consent)"), h("dd", {}, `${c.decision.status}${c.decision.by ? ` (recorded by ${c.decision.by})` : ""}`)))),
    returnPanel(c, id, refresh),
    handoffPanel(c, id, refresh),
    qualityPanel(c, id, refresh),
    stockPanel(c),
    h("section", { class: "card" }, h("h2", {}, "Log a call"),
      h("label", { for: "outcome" }, "What happened"), outcome,
      h("label", {}, "How you spoke"), channel,
      h("label", { for: "note" }, "Notes"), note,
      h("p", {}, h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/call`, { outcome: outcome.value, note: note.value, channel: channel.value })) }, "Save"))),
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
    assistantPanel,
    chatCasePanel(id),
    financePanel(c, id, refresh), grantPanel(c, id, refresh), technicalPanel(c, id, refresh), residentPanel(c, id, refresh),
    msg,
    h("section", { class: "card" }, h("h2", {}, "History"),
      h("p", {}, "Current task context below; event-time owners and reasons in the history remain unchanged."),
      workSummary(c.work),
      c.contacts.length ? h("ul", { class: "tl" }, c.contacts.slice(0, 15).map((k) => h("li", {},
        h("strong", {}, `${fmtDate(k.at)} ${k.channel}: ${k.outcome}`), h("div", { class: "muted" }, `${k.by}${k.note ? `. ${k.note}` : ""}`)))) : h("p", {}, "No contact recorded yet.")));
}

async function buildingView(id) {
  try {
    const b = await api(`/api/buildings/${encodeURIComponent(id)}`);
    const category = (key, title) => h("section", { class: "card" }, h("h2", {}, title),
      b[key] == null ? h("p", {}, "Unknown: no source-backed records supplied.") :
        b[key].length === 0 ? h("p", {}, "Source records explicitly list none.") :
          h("ul", {}, b[key].map((x) => h("li", {},
            h("strong", {}, `${x.id}: ${x.label}`),
            x.status && h("p", {}, `Recorded status: ${x.status}. Owner: ${x.owner}`),
            x.case_ids !== undefined && h("p", {}, `Affected homes: ${x.case_ids === null ? "Unknown" : x.case_ids.join(", ") || "None"}. Packages: ${x.package_ids === null ? "Unknown" : x.package_ids.join(", ") || "None"}.`),
            h("p", { class: "muted" }, `Source: ${x.source}`)))));
    show(h("a", { class: "back", href: "#/" }, "Back to the list"),
      h("h1", {}, `${b.name} (${b.id})`),
      h("p", {}, `Version ${b.version}. Source: ${b.source}`),
      h("p", { role: "status" }, b.notice),
      category("systems", "Shared systems"), category("dependencies", "Dependencies"),
      category("holds", "Work stopped pending review"), category("works", "Shared works"),
      h("section", { class: "card" }, h("h2", {}, "Shared building costs"),
        b.costs_restricted ? h("p", {}, "Restricted to authorised Finance roles.") :
          b.costs === null ? h("p", {}, "Unknown: costs have not been supplied.") :
            b.costs.length === 0 ? h("p", {}, "No shared costs recorded.") :
              h("ul", {}, b.costs.map((x) => h("li", {}, `${x.id}: GBP ${x.amount_gbp}, shared work ${x.work_id}. Source: ${x.source}`))),
        h("p", {}, "Home allocations are retained on each home, not added to these shared costs. These are recorded costs, not spending or payment approval.")),
      h("section", { class: "card" }, h("h2", {}, "Linked home cases"),
        h("p", {}, "A link does not prove shared-work applicability or transfer an approval."),
        b.homes.length ? h("ul", {}, b.homes.map((c) => h("li", {},
          h("a", { href: `#/case/${encodeURIComponent(c.id)}` }, c.id),
          `: ${c.stage}; ${c.closed ? "closed" : "open"}. Review this home's own checks.`))) :
          h("p", {}, "No home links recorded.")));
  } catch (e) {
    if (e.name === "AbortError" || !me) return;
    show(h("a", { class: "back", href: "#/" }, "Back to the list"),
      h("h1", {}, "Shared building context unavailable"),
      h("p", { class: "err", role: "alert" }, e.message));
  }
}

const STAGES_ORDER = ["Home identified", "Checking lease", "Rescheduled", "Contacting resident", "Contact paused", "Survey being booked", "Survey booked", "Survey write-up", "Design starting", "Design in progress", "Design awaiting approval", "Design being corrected", "Waiting on other works", "Waiting for resident decision", "Resident paused works", "Funding check", "Final checks before ordering", "Waiting for block programme", "With contractor", "Install booked", "Works under way", "Handover to arrange", "Quality check", "Closing down", "Aftercare issue"];
const SAFETY_ROLES = ["Building Safety Liaison", "Retrofit Programme Manager", "Programme Support Officer"];
const HAZ_CATEGORIES = ["Damp and mould", "Structural", "Electrical", "Other"];
const HAZ_PRIORITIES = ["Emergency", "Significant", "Routine"];
const post = (id, act, body) => api(`/api/cases/${encodeURIComponent(id)}/${act}`, body);

function returnPanel(c, id, refresh) {
  const why = h("input", { id: "ret-why", type: "text", maxlength: 300, required: true });
  const source = h("input", { id: "ret-source", type: "text", maxlength: 300, required: true });
  const next = h("input", { id: "ret-next", type: "text", maxlength: 300, required: true });
  const metadata = () => ({ reason: why.value, source: source.value, next_action: next.value });
  const fields = () => [h("label", { for: "ret-source" }, "Source reference (human-recorded, not verified automatically)"), source,
    h("label", { for: "ret-next" }, "Next action"), next,
    h("p", { class: "muted" }, `Receiving owner: ${c.owner}. Return or reopen does not transfer ownership. Use a handoff for another colleague.`)];
  const history = c.returns && c.returns.length ? h("ul", { class: "tl" }, c.returns.slice(-5).reverse().map((x) => h("li", {},
    h("strong", {}, `${fmtDate(x.at)} ${x.reopened ? "Reopened" : "Returned"}: ${x.from_stage} to ${x.to_stage}`),
    h("div", { class: "muted" }, `${x.by}. ${x.reason}. Source: ${x.source || "Unknown"}; authority: ${x.initiating_authority?.role || "Unknown"}; receiving owner: ${x.receiving_owner?.name || "Unknown"}; next action: ${x.next_action || "Unknown"}.`)))) : null;
  if (c.closed) {
    if (!isManager()) return h("section", { class: "card" }, h("h2", {}, "Closed case"), h("p", {}, "This case is closed. A manager can reopen it."), history);
    return h("section", { class: "card" }, h("h2", {}, "Reopen this case"),
      h("p", { class: "muted" }, "Only a manager can reopen a closed case. Your reason is kept in the audit log."),
      h("label", { for: "ret-why" }, "Why it is being reopened"), why,
      ...fields(),
      h("p", {}, h("button", { onclick: () => refresh(() => post(id, "reopen", metadata())) }, "Reopen case")), history);
  }
  const earlier = STAGES_ORDER.slice(0, Math.max(0, STAGES_ORDER.indexOf(c.stage)));
  if (!earlier.length) return history ? h("section", { class: "card" }, h("h2", {}, "Return and reopen history"), history) : null;
  const to = h("select", { id: "ret-to" }, earlier.map((x) => h("option", { value: x, selected: x === earlier[earlier.length - 1] }, x)));
  return h("section", { class: "card" }, h("h2", {}, "Send this case back"),
    h("p", { class: "muted" }, "Use this when something earlier needs redoing. A case can only go back to an earlier stage, and the reason is kept in the audit log."),
    h("label", { for: "ret-to" }, "Back to which stage"), to,
    h("label", { for: "ret-why" }, "Why it is going back"), why,
    ...fields(),
    h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "return", { ...metadata(), to_stage: to.value })) }, "Send back")), history);
}

function handoffPanel(c, id, refresh) {
  const hd = c.handoff;
  const open = hd && ["Offered", "Received", "Escalated"].includes(hd.state);
  const kids = [h("h2", {}, "Handoff to a colleague")];
  if (hd) kids.push(
    h("p", { role: "status" }, `${hd.status}. Current accountable owner: ${hd.accountable_owner}. Destination: ${hd.destination || "Unknown"}. Proposed receiver: ${hd.proposed_receiver || "Unassigned"}. Confirmed receiver: ${hd.confirmed_receiver || "Unconfirmed"}. Chase owner: ${hd.chase_owner || "Unassigned"}.`),
    h("p", {}, `Urgency: ${hd.urgency || "Unknown"}. Due: ${hd.due_at || "Unknown"}. Next action: ${hd.next_action || "Unknown"}.`),
    h("p", {}, `Resident update owner: ${hd.resident_update_owner || "Unassigned"}; commitment: ${hd.resident_update_due_at || "Unknown"}. No message is sent automatically.`),
    hd.state === "Escalated" && h("p", {}, `Escalated to ${hd.escalation_owner}. ${hd.answer_note}`));
  if (open) {
    kids.push(h("p", { role: "status" }, `Offered to ${hd.to_name} by ${hd.offered_by} on ${fmtDate(hd.offered_at)}. Waiting for an answer. The case stays with ${hd.from_name} until it is accepted.`),
      hd.note && h("p", { class: "muted" }, hd.note));
    const why = h("input", { id: "ho-why", type: "text", maxlength: 300 });
    if (hd.to_code === me.user.code) {
      if (hd.state === "Offered") kids.push(h("button", { class: "alt", onclick: () => refresh(() => post(id, "receive-handoff", {})) }, "Record receipt (not acceptance)"));
      kids.push(h("div", { class: "row" }, h("button", { onclick: () => refresh(() => post(id, "accept-handoff", {})) }, "Accept this case")),
        h("div", { class: "row" }, h("label", { for: "ho-why" }, "Reason if you cannot take it"), why,
          h("button", { class: "alt", onclick: () => refresh(() => post(id, "decline-handoff", { reason: why.value })) }, "Decline")));
    }
    if (hd.from_code === me.user.code || isManager()) {
      kids.push(h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "withdraw-handoff", {})) }, "Withdraw the offer")));
      if (hd.state !== "Escalated") {
        const manager = h("select", { id: "ho-escalate-to" }, me.staff.filter((s) => ["Retrofit Programme Manager", "Programme Support Officer"].includes(s.role)).map((s) => h("option", { value: s.email }, s.name)));
        const reason = h("input", { id: "ho-escalate-why", maxlength: 300 });
        kids.push(h("label", { for: "ho-escalate-to" }, "Escalate to manager"), manager,
          h("label", { for: "ho-escalate-why" }, "Escalation reason"), reason,
          h("button", { class: "alt", onclick: () => refresh(() => post(id, "escalate-handoff", { to: manager.value, reason: reason.value })) }, "Record manual escalation"));
      }
    }
  } else {
    if (hd) kids.push(h("p", { class: "muted" }, `Last handoff to ${hd.to_name}: ${hd.state}${hd.answer_note ? `. ${hd.answer_note}` : ""}.`));
    if (hd && hd.state === "Accepted" && hd.to_code === me.user.code && c.owner_code === me.user.code) {
      const done = h("input", { id: "ho-done", maxlength: 300 });
      kids.push(h("label", { for: "ho-done" }, "Completed action"), done,
        h("button", { onclick: () => refresh(() => post(id, "complete-handoff", { note: done.value })) }, "Complete handoff"));
    }
    if (!c.closed && (!hd || hd.state !== "Accepted") && (c.owner_code === me.user.code || isManager())) {
      const to = h("select", { id: "ho-to" }, me.staff.filter((s) => s.code !== c.owner_code && s.role !== "Contractor").map((s) => h("option", { value: s.email }, `${s.name} (${s.role})`)));
      const note = h("input", { id: "ho-note", type: "text", maxlength: 300 });
      const next = h("input", { id: "ho-next", maxlength: 300 });
      const urgency = h("select", { id: "ho-urgency" }, ["", "Routine", "Urgent"].map((x) => h("option", { value: x }, x || "Unknown")));
      const due = h("input", { id: "ho-due", type: "datetime-local" });
      const updateTo = h("select", { id: "ho-update-to" }, h("option", { value: "" }, "Unassigned"), me.staff.filter((s) => s.role !== "Contractor").map((s) => h("option", { value: s.email }, s.name)));
      const updateDue = h("input", { id: "ho-update-due", type: "datetime-local" });
      const iso = (value) => value ? new Date(value).toISOString() : null;
      kids.push(h("p", { class: "muted" }, "Offer the case. It only moves when the other person accepts."),
        h("label", { for: "ho-to" }, "Offer to"), to, h("label", { for: "ho-note" }, "Note for them (optional)"), note,
        h("label", { for: "ho-next" }, "Next action"), next, h("label", { for: "ho-urgency" }, "Urgency"), urgency,
        h("label", { for: "ho-due" }, "Human-selected due date (not an approved SLA)"), due,
        c.resident_update ? h("p", {}, "The existing resident-update commitment is preserved.") : h("div", {},
          h("label", { for: "ho-update-to" }, "Resident-update owner"), updateTo,
          h("label", { for: "ho-update-due" }, "Resident-update commitment"), updateDue),
        h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "offer-handoff", {
          to: to.value, note: note.value, next_action: next.value, urgency: urgency.value, due_at: iso(due.value),
          resident_update_to: updateTo.value, resident_update_due_at: iso(updateDue.value)
        })) }, "Offer the case")));
    }
  }
  const history = c.handoff_history || c.handoff_log;
  if (history && history.length) {
    kids.push(h("ul", { class: "tl" }, history.slice(-8).reverse().map((x) => h("li", {}, `${fmtDate(x.at || x.answered_at)}: ${x.from_name} to ${x.to_name}, ${x.status || x.state}; current owner at event: ${x.accountable_owner || "Unknown"}; chase: ${x.chase_owner || "Unknown"}`))));
  }
  return h("section", { class: "card" }, ...kids);
}

function hazardState(x) {
  if (x.released) return "Retrofit work restriction lifted";
  if (x.repaired) return "Repair evidenced; retrofit work still stopped";
  return x.state || "Legacy evidence needed";
}

function safetyPanel(c, id, refresh) {
  const canRelease = SAFETY_ROLES.includes(me.user.role);
  const safeStaff = me.staff.filter((s) => SAFETY_ROLES.includes(s.role));
  const iso = (v) => v ? new Date(v).toISOString() : "";
  const timingLabels = {
    response_due_at: "Service response due", responded_at: "Service responded",
    resident_update_due_at: "Service resident update due", resident_updated_at: "Service resident updated"
  };
  const items = c.hazards.map((x, i) => {
    const st = hazardState(x);
    const job = h("input", { type: "text", maxlength: 40, "aria-label": `External service case reference for ${x.category}` });
    const to = h("select", { "aria-label": `Refer ${x.category} to` }, safeStaff.map((s) => h("option", { value: s.email }, `${s.name} (${s.role})`)));
    const evidence = h("input", { type: "text", maxlength: 300, "aria-label": `External evidence reference for ${x.category}` });
    const note = h("input", { type: "text", maxlength: 300, "aria-label": `Reason to restart retrofit work for ${x.category}` });
    const receiver = x.destination && x.destination.code === me.user.code && canRelease;
    const action = (name) => refresh(() => post(id, name, { index: i, evidence: evidence.value, note: note.value }));
    const times = Object.entries(timingLabels).filter(([key]) => !x[key]).map(([key, label]) => [
      key, h("input", { type: "datetime-local", "aria-label": `${label} for ${x.category}` })
    ]);
    return h("li", {},
      h("strong", {}, `Reported: ${x.category}, ${x.priority || "urgency unknown"}`), ` ${st}.`,
      h("p", {}, `Source: ${x.source || "Unknown (legacy)"}. Awareness: ${x.aware_at || "Unknown (legacy)"}.`),
      h("p", {}, `Stopped work scope: home ${x.hold.case_id}. Accountable role: ${x.hold.accountable_role || "Unknown (legacy)"}. Follow-up: ${x.follow_up ? x.follow_up.name : "Unknown (legacy)"}.`),
      h("p", {}, `Destination: ${x.destination ? `${x.destination.name} (${x.destination.role})` : "Not bound"}. External case: ${x.job || "Unknown"}.`),
      h("p", {}, `Sent: ${x.sent_at || "Unknown"}; receipt: ${x.received_at || "Not evidenced"}; acceptance: ${x.accepted_at || "Not evidenced"}.`),
      h("p", {}, `Sending evidence: ${x.sent_evidence || "Unknown"}; receipt evidence: ${x.receipt_evidence || "Unknown"}; acceptance evidence: ${x.acceptance_evidence || "Unknown"}.`),
      h("p", {}, `Repair evidence: ${x.repair_evidence || "Unknown"}. Restart decision: ${x.hold.decision ? `${x.hold.decision.actor.name} (${x.hold.decision.actor.role}): ${x.hold.decision.reason}; ${x.hold.decision.evidence}` : "Not recorded"}.`),
      h("ul", {}, Object.entries(timingLabels).map(([key, label]) => h("li", {}, `${label}: ${x[key] || "Unknown (external service owns timing)"}`))),
      (!x.released || (receiver && x.accepted_at && times.length > 0)) && h("div", {}, h("label", {}, "External evidence reference", evidence)),
      !x.released && !x.referral_version && h("div", { class: "row" }, to, job, h("button", { class: "alt", onclick: () => refresh(() => post(id, "hazard-refer", { index: i, to: to.value, job: job.value, evidence: evidence.value })) }, x.referred ? "Bind legacy referral prospectively" : "Record referral sent")),
      receiver && !x.received_at && h("button", { class: "alt", onclick: () => action("hazard-receive") }, "Record separate receipt evidence"),
      receiver && x.received_at && !x.accepted_at && h("button", { class: "alt", onclick: () => action("hazard-accept") }, "Record separate acceptance evidence"),
      receiver && x.accepted_at && h("div", {},
        times.map(([key, input]) => h("label", {}, timingLabels[key], input)),
        times.length > 0 && h("button", { class: "alt", onclick: () => refresh(() => post(id, "hazard-times", {
          index: i, evidence: evidence.value, ...Object.fromEntries(times.map(([key, input]) => [key, iso(input.value)]))
        })) }, "Record externally supplied times"),
        !x.repaired && !x.released && h("button", { class: "alt", onclick: () => action("hazard-repaired") }, "Record external repair evidence")),
      x.repaired && !x.released && canRelease && h("div", { class: "row" }, note,
        h("button", { onclick: () => action("hazard-release") }, "Allow home retrofit work to restart (independent reviewer)")));
  });
  const cat = h("select", { id: "hz-cat" }, HAZ_CATEGORIES.map((x) => h("option", {}, x)));
  const pri = h("select", { id: "hz-pri" }, HAZ_PRIORITIES.map((x) => h("option", {}, x)));
  const note = h("input", { id: "hz-note", type: "text", maxlength: 300 });
  const source = h("input", { id: "hz-source", type: "text", maxlength: 300 });
  const aware = h("input", { id: "hz-aware", type: "datetime-local" });
  return h("section", { class: "card" }, h("h2", {}, "Safety referrals and stopped retrofit work"),
    h("p", { class: "muted" }, "The existing hazard and repairs service owns categorisation, clocks, resident updates and closure. These are unverified reports and human-recorded external evidence, not service commands or verified transport. No message is sent here. Use the existing hazard service immediately for urgent concerns; AI and stopped retrofit work must not delay it."),
    items.length ? h("ul", { class: "list" }, items) : h("p", {}, "No safety issues recorded."),
    h("div", {}, h("h3", {}, "Raise a safety observation (also available after retrofit closure)"),
      h("label", { for: "hz-cat" }, "Reported observation (not service classification)"), cat,
      h("label", { for: "hz-pri" }, "Reported urgency (not service priority)"), pri,
      h("label", { for: "hz-note" }, "What you saw"), note,
      h("label", { for: "hz-source" }, "Source and channel reference"), source,
      h("label", { for: "hz-aware" }, "When the landlord first became aware (local time)"), aware,
      h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "hazard-raise", {
        category: cat.value, priority: pri.value, note: note.value, source: source.value, aware_at: iso(aware.value)
      })) }, "Raise safety issue"))));
}

async function closedView() {
  if (!isManager()) return show(h("p", {}, "Only a manager sees closed cases."));
  const d = await api("/api/cases?view=closed&limit=100");
  show(h("h1", {}, "Closed cases"), h("p", { class: "muted" }, `${d.total} closed. Open one to reopen it with a reason.`),
    h("ul", { class: "list" }, d.items.length ? d.items.map((r) => h("li", {}, h("a", { class: "item", href: `#/case/${encodeURIComponent(r.id)}` },
      h("div", {}, h("span", { class: "name" }, r.resident), h("div", {}, `${r.address}, ${r.town} ${r.postcode}`)), h("div", { class: "meta" }, r.stage)))) : h("li", { class: "card" }, "No closed cases.")));
}

async function contractorListView() {
  const PAGE = 50;
  let rows = [], total = 0;
  const out = h("div", { "aria-live": "polite" });
  const render = () => out.replaceChildren(
    h("p", { class: "muted" }, `${total} ${total === 1 ? "job" : "jobs"}`),
    h("ul", { class: "list" }, rows.length ? rows.map((r) => h("li", {}, h("a", { class: "item", href: `#/case/${encodeURIComponent(r.id)}` },
      h("div", {}, h("span", { class: "name" }, `${r.address}, ${r.town} ${r.postcode}`), h("div", { class: "status" }, r.status),
        r.needs_notice ? h("span", { class: "flag" }, "Needs notice") : h("span", { class: "muted" }, "No extra notice needed"),
        h("div", {}, `Named contact: ${r.named_contact}`)),
      h("div", { class: "meta" }, h("div", {}, r.stage), r.next_visit && h("div", {}, `Visit: ${fmtDate(r.next_visit)}`))))) : h("li", { class: "card" }, "No jobs assigned to you.")),
    rows.length < total ? h("p", {}, h("button", { class: "alt", onclick: () => load(true) }, `Show more (${rows.length} of ${total} shown)`)) : null);
  const load = async (more) => {
    const d = await api(`/api/cases?limit=${PAGE}&offset=${more ? rows.length : 0}`);
    rows = more ? rows.concat(d.items) : d.items;
    total = d.total;
    render();
  };
  show(h("h1", {}, "Your jobs"), h("p", { class: "muted" }, "You see the address, the works and a named contact. Where a resident needs notice before a visit it says so; the reason is not shared with contractors."), out);
  await load();
  out.after(await contractorOrders());
}

async function contractorCaseView(id) {
  let c;
  try { c = await api(`/api/cases/${encodeURIComponent(id)}`); } catch (e) { if (e.name === "AbortError" || !me) return; return show(h("a", { class: "back", href: "#/" }, "Back to your jobs"), h("p", { class: "err" }, e.message)); }
  show(h("a", { class: "back", href: "#/" }, "Back to your jobs"),
    h("h1", {}, `${c.home.address}, ${c.home.town} ${c.home.postcode}`),
    h("div", { class: "status-line", role: "status" }, c.status),
    h("section", { class: "card regulatory", id: "regulatory-supplier" }, h("h2", {}, "Requirements and doubt route"),
      h("p", {}, "Suppliers: follow the agreed contract and scheme requirements, not a chat interpretation of law. Contract and TrustMark terms are not held here. Obtain them from your named contact or contracts manager before relying on a requirement."),
      h("p", {}, `In doubt, contact ${c.named_contact}. For a possible emergency or hazard use the existing human emergency or hazard service immediately; do not wait for this application. No consent, safety approval or financial commitment is inferred.`),
      h("p", {}, "Share only necessary resident information. This view grants no access to staff regulatory chat or alerts.")),
    h("section", { class: `card${c.needs_notice ? " ai" : ""}` }, h("h2", {}, "Before you visit"),
      h("p", { class: "big" }, c.needs_notice ? "Needs notice" : "No extra notice needed"),
      h("p", {}, `Named contact: ${c.named_contact}`)),
    h("section", { class: "card" }, h("h2", {}, "The job"),
      h("dl", {}, h("dt", {}, "Works"), h("dd", {}, c.measures), h("dt", {}, "Stage"), h("dd", {}, c.stage),
        h("dt", {}, "Home"), h("dd", {}, c.home.type), h("dt", {}, "Your contact"), h("dd", {}, `${c.contractor.name}, ${c.contractor.contact}`))),
    h("section", { class: "card" }, h("h2", {}, "Visits"),
      c.appointments.length ? h("ul", { class: "list" }, c.appointments.map((a) => h("li", {}, `${fmtDate(a.date)} ${a.slot}: ${a.type} (${a.outcome})`))) : h("p", {}, "No visits booked.")));
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
      const r = await api(`/api/cases/${encodeURIComponent(id)}/read-doc`, modeBody({ id: d.id }));
      out.replaceChildren(h("p", { class: "muted" }, r.source === "ai" ? "AI-read, please check:" : "Note:"), h("p", { class: "pre" }, r.text), aiNotes(r));
    } catch (e) { out.replaceChildren(h("p", { class: "err" }, e.message)); }
  };
  return h("section", { class: "card" }, h("h2", {}, "Documents"),
    h("p", {}, c.checklist.map((x) => h("span", { class: `flag${x.present ? "" : " danger"}` }, `${x.present ? "Have" : "Need"}: ${x.kind}`))),
    c.documents.length ? h("ul", { class: "list" }, c.documents.map((d) => h("li", { class: "row between" },
      h("span", {}, h("a", { href: `/api/docs/${encodeURIComponent(id)}/${d.id}` }, d.name), ` ${d.kind}, ${fmtDate(d.at)}, ${d.by}`),
      !d.generated && h("button", { class: "alt", onclick: () => read(d) }, "Read with AI")))) : h("p", {}, "No documents yet."),
    h("div", { class: "row" }, kind, file, h("button", { onclick: upload }, "Add document")), out);
}

const fundingAi = {};
function fundingPanel(c, id, refresh) {
  const f = c.funding;
  const canAct = ["Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
  const ta = h("textarea", { "aria-label": "Funding application draft", rows: 10 });
  ta.value = f.draft || "";
  const fundNote = h("div", {}, fundingAi[id] ? [h("p", { class: "muted" }, fundingAi[id].label), aiNotes(fundingAi[id])] : null);
  const ref = h("input", { "aria-label": "Reference from the funder", placeholder: "Reference from the funder" });
  const step = (action, text) => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/funding`, { action, text }));
  if (f.status === "Confirmed") {
    return h("section", { class: "card" }, h("h2", {}, "Funding"), h("p", {}, `Confirmed. Route: ${f.route}${f.reference ? `, reference ${f.reference}` : ""}.`));
  }
  const need = c.checklist.filter((x) => !x.present).map((x) => x.kind);
  return h("section", { class: "card" }, h("h2", {}, "Funding application"),
    h("p", {}, `Route: ${f.route}. Status: ${f.status}.${need.length ? ` Still needed: ${need.join(", ")}.` : " All evidence is in."}`),
    h("p", { class: "muted" }, "AI drafts the wording. A person approves it and submits it to the funder. The system never submits."),
    h("div", { class: "row" }, h("button", { onclick: () => refresh(async () => { fundingAi[id] = (await api(`/api/cases/${encodeURIComponent(id)}/funding-draft`, modeBody({}))).ai; }) }, "Draft application with AI")),
    fundNote,
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
        h("p", {}, `${r.ready} rows are ready to bring in. ${r.matched_existing} match a home we already have a record for.`),
        h("p", {}, "We found these columns: ", Object.entries(r.columns).map(([k, v]) => `${k}: ${v || "not found"}`).join("; ")),
        r.to_fix.length ? h("div", {}, h("h2", {}, "Rows to fix"), h("ul", {}, r.to_fix.map((x) => h("li", {}, `Row ${x.row}: ${x.problem}`)))) : h("p", {}, "No rows need fixing."));
    } catch (e) { out.replaceChildren(h("p", { class: "err" }, e.message)); }
  });
  show(h("a", { class: "back", href: "#/" }, "Back to the list"), h("h1", {}, "Check a spreadsheet"),
    h("p", {}, "Choose any spreadsheet saved as CSV. We match the columns for you and list anything to fix. Your file is never changed."),
    h("label", { for: "f" }, "Spreadsheet (CSV)"), file, out);
}

async function signOut(switchAccount) {
  try {
    const r = await api("/api/logout", { switchAccount });
    me = null; briefingBox = null; clearPhoto();
    if (r && r.redirect) { location.href = r.redirect; return; }
    location.href = "/";
  } catch (e) { document.getElementById("account-error").textContent = e.message; }
}
document.getElementById("signout").addEventListener("click", () => signOut(false));
document.getElementById("switch-account").addEventListener("click", () => signOut(true));
document.querySelector(".skip-link").addEventListener("click", (event) => { event.preventDefault(); app.focus(); });
document.addEventListener("keydown", (e) => {
  const menu = document.getElementById("account");
  if (e.key === "Escape" && menu.open) { menu.open = false; menu.querySelector("summary").focus(); }
});
document.addEventListener("click", (e) => {
  const menu = document.getElementById("account");
  if (!menu.contains(e.target)) menu.open = false;
});
window.addEventListener("hashchange", () => me && route());
start().catch((e) => login(e.message));

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
  const table = h("details", { class: "chart-data" }, h("summary", {}, "Show this chart as a table"),
    h("table", {}, h("caption", { class: "sr-only" }, title), h("thead", {}, h("tr", {}, h("th", { scope: "col" }, "Group"), h("th", { scope: "col" }, "Cases"))),
      h("tbody", {}, data.map((d) => h("tr", {}, h("th", { scope: "row" }, d.label), h("td", {}, String(d.n)))))));
  return h("section", { class: "card" }, h("h2", {}, title), g, table, link);
}

const OV_TILES = [["", "Open cases"], ["hazard", "Safety issues open"], ["long", "Waiting 60+ days"], ["nodecision", "Awaiting resident decision"], ["fundingprog", "Funding in progress"], ["support", "Residents needing extra support"]];
const ovState = { flag: "", area: "" };
const MAP_SIGNALS = {
  normal: { label: "Normal", code: "O" },
  long: { label: "Waiting 60+ days", code: "W" },
  hazard: { label: "Safety issue open", code: "!" },
};

function mapSymbol(kind) {
  const shape = kind === "hazard" ? svg("path", { d: "M14 2 L26 26 H2 Z" })
    : kind === "long" ? svg("rect", { x: 2, y: 2, width: 24, height: 24 })
      : svg("circle", { cx: 14, cy: 14, r: 12 });
  return h("span", { class: `map-symbol ${kind}`, "aria-hidden": "true" },
    svg("svg", { viewBox: "0 0 28 28", focusable: "false" }, shape),
    h("span", { class: "marker-code" }, MAP_SIGNALS[kind].code));
}

function mapAction(marker, action) {
  // Leaflet forwards keys but does not activate custom markers without a popup.
  marker.on("click", action);
  marker.on("keydown", (event) => {
    if (event.originalEvent.key === "Enter" || event.originalEvent.key === " ") {
      event.originalEvent.preventDefault();
      action();
    }
  });
}

function mapPanel() {
  const signal = routeController.signal;
  const el = h("div", { id: "leaflet", class: "leafmap", role: "region", "aria-label": "Map of open cases. Zoom with the buttons, mouse wheel or pinch." });
  const info = h("p", { class: "muted", role: "status", "aria-live": "polite" });
  const open = h("a", { href: "#/all" }, "Show these as a list");
  let map = null, layer = null;
  const listHead = h("summary", { id: "maplist-h" }, "Show the map areas as a list (keyboard and screen reader friendly)");
  const listUl = h("ul", { "aria-labelledby": "maplist-h", class: "plainlist" });
  const listBox = h("details", { class: "maplist" }, listHead, listUl);
  const renderList = (d) => {
    listUl.replaceChildren(...d.items.map((p) => {
      if (d.mode === "clusters") {
        const label = `${p.count} homes, ${p.hazards} with a safety issue open`;
        return h("li", {}, h("button", { type: "button", class: "linkbtn", "aria-label": `${label}. Zoom in to this area`,
          onclick: () => { map.setView([p.lat, p.lon], Math.min(map.getZoom() + 2, 18)); listHead.focus(); } }, label));
      }
      return h("li", {}, h("a", { href: `#/case/${encodeURIComponent(p.id)}` }, `${p.name}, ${MAP_SIGNALS[p.kind].label}`));
    }));
  };
  let fitting = false, seq = 0;
  const draw = async (fit) => {
    if (signal.aborted) return;
    const my = ++seq;
    open.onclick = () => { Object.assign(listState, { flag: ovState.flag === "fundingprog" ? "funding" : ovState.flag, area: ovState.area }); };
    if (!map) {
      map = L.map(el, { scrollWheelZoom: true }).setView([54.9, -1.6], 9);
      if (me.map && me.map.tiles) {
        L.tileLayer(me.map.tiles, { maxZoom: 19, referrerPolicy: "strict-origin-when-cross-origin", attribution: me.map.attribution || "" }).addTo(map);
      }
      layer = L.layerGroup().addTo(map);
      map.on("moveend", () => { if (!fitting) draw(false); });
    }
    const b = map.getBounds();
    const view = fit ? "" : `&bbox=${[b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].join(",")}`;
    let d;
    try { d = await api(`/api/map?${qs(ovState)}&zoom=${map.getZoom()}${view}`, undefined, signal); }
    catch (error) {
      if (signal.aborted || my !== seq || !me) return;
      layer.clearLayers();
      listUl.replaceChildren();
      info.setAttribute("role", "alert");
      info.textContent = `Map unavailable: ${error.message}. Use the case list or try changing the map filter.`;
      return;
    }
    if (signal.aborted || my !== seq) return;
    info.setAttribute("role", "status");
    info.textContent = d.mode === "clusters"
      ? `${d.total} homes in this view, grouped into ${d.shown} areas. Zoom in to see each home.`
      : `${d.total} ${d.total === 1 ? "home" : "homes"} shown`;
    renderList(d);
    layer.clearLayers();
    d.items.forEach((p) => {
      if (d.mode === "clusters") {
        const label = `${p.count} homes, ${p.hazards} with a safety issue open. Zoom in to this area`;
        const icon = h("div", { class: `cluster${p.hazards ? " hazard" : ""}`, "aria-hidden": "true" },
          h("span", {}, `${p.count} homes`),
          h("span", { class: "cluster-safety" }, `Safety: ${p.hazards}`));
        const m = L.marker([p.lat, p.lon], { icon: L.divIcon({ className: "map-cluster", html: icon, iconSize: [104, 50] }),
          keyboard: true, title: label, alt: label });
        mapAction(m, () => map.setView([p.lat, p.lon], Math.min(map.getZoom() + 2, 18)));
        m.addTo(layer);
        return;
      }
      const label = `${p.name}, ${MAP_SIGNALS[p.kind].label}`;
      const m = L.marker([p.lat, p.lon], { icon: L.divIcon({ className: "map-marker", html: mapSymbol(p.kind), iconSize: [28, 28] }),
        keyboard: true, title: label, alt: label });
      m.bindTooltip(h("span", {}, label), { direction: "top" });
      mapAction(m, () => { location.hash = `#/case/${encodeURIComponent(p.id)}`; });
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
    h("p", {}, Object.entries(MAP_SIGNALS).map(([kind, signal]) => h("span", { class: `key ${kind}` }, mapSymbol(kind), signal.label))),
    el, listBox, h("div", { class: "row between" }, info, open));
  return { box, draw, size: () => map && map.invalidateSize() };
}

async function overviewView() {
  const st = await api("/api/stats");
  const k = st.kpis;
  const counts = { "": k.open, hazard: k.hazards, long: k.long, nodecision: k.nodecision, fundingprog: k.funding, support: k.support };
  const mp = mapPanel();
  const tiles = h("div", { class: "tiles", role: "group", "aria-label": "Choose what the map shows" });
  const paint = () => tiles.replaceChildren(...OV_TILES.map(([f, label]) => h("button", { class: `tile${f === "hazard" ? " danger" : ""}`, "aria-pressed": String(ovState.flag === f),
    onclick: () => { ovState.flag = f; paint(); mp.draw(true); } }, h("strong", {}, String(counts[f])), h("span", {}, label),
    h("span", { class: "tile-selection" }, ovState.flag === f ? "Selected" : "Select filter"))),
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
      h("section", { class: "card" }, h("h2", {}, "Contractors"),
        h("div", { class: "table-scroll", tabindex: "0", role: "region", "aria-label": "Contractors table" },
          h("table", {}, h("thead", {}, h("tr", {}, ["Contractor", "Open", "On site or booked", "Stuck 60+ days"].map((x) => h("th", { scope: "col" }, x)))),
            h("tbody", {}, st.contractors.map((c) => h("tr", {}, h("td", {}, c.name), h("td", {}, c.open), h("td", {}, c.booked), h("td", {}, c.long)))))))),
    h("section", { class: "card" }, h("h2", {}, "Team workload"),
      h("div", { class: "table-scroll", tabindex: "0", role: "region", "aria-label": "Team workload table" },
        h("table", {}, h("thead", {}, h("tr", {}, ["Name", "Role", "Open cases", "With a safety issue"].map((x) => h("th", { scope: "col" }, x)))),
          h("tbody", {}, st.team.map((t) => h("tr", {}, h("td", {}, t.name), h("td", {}, t.role), h("td", {}, t.open), h("td", {}, t.hazards))))))));
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
