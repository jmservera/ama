"use strict";
const app = document.getElementById("app");
let me = null;
const microsoftSignIn = document.body.dataset.authProvider === "trusted-proxy";
let photoUrl = null;
let routeController = new AbortController();
let searchTimer = 0;
let queueOrigin = "mine";
let coordinatorOrigin = null;
let resetFocus = false;
const workspaceStatus = document.getElementById("workspace-status");
let displayedHash = location.hash || "#/";
let caseSession = null;
let disposeMapPanel = null;

function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2),
      ["onclick", "onsubmit", "onchange"].includes(k) && typeof AsyncAction !== "undefined" && AsyncAction
        && typeof AsyncAction.handler === "function"
        ? AsyncAction.handler(v) : v);
    else if (v !== false && v != null) el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) {
    if (kid == null || kid === false) continue;
    el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return el;
}

function mutationNeedsHistory(error) {
  return error.outcome === "committed" || error.outcome === "uncertain" || !error.status;
}

function requireCaseHistory(session) {
  if (session) session.historyBarrier = session.historyGeneration = {};
}

const pendingMutations = new Set();

function mutationKey(path, body) {
  return JSON.stringify([path, body.action || body.task || (path.endsWith("/draft") ? body.kind : "") || "",
    ...["id", "index", "measure", "case_id", "package", "capability", "turn"]
      .map(key => body[key] ?? null)]);
}

async function api(path, body, signal) {
  const progress = typeof AsyncAction !== "undefined"
    ? AsyncAction.feedback("Loading workspace data") : null;
  try {
  signal = signal || routeController.signal;
  const key = body === undefined ? null : mutationKey(path, body);
  if (key && pendingMutations.has(key)) {
    const error = new Error("This action is still pending. Wait for its result and check the history before trying again.");
    error.status = 409;
    throw error;
  }
  if (key) pendingMutations.add(key);
  try {
    const res = await fetch(path, body === undefined ? { signal } : {
      method: "POST", headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" }, body: JSON.stringify(body), signal,
    });
    const data = await res.json().catch(error => {
      if (key) throw error;
      return {};
    });
    signal.throwIfAborted();
    if (res.status === 401 && path !== "/api/login") {
      me = null; login("Your session has ended. Sign in again.");
      const error = new Error("Your session has ended. Sign in again."); error.status = 401; throw error;
    }
    if (!res.ok) { const e = new Error(data.error || "Something went wrong."); e.reasons = data.reasons; e.status = res.status; e.outcome = data.outcome; throw e; }
    return data;
  } finally {
    if (key) pendingMutations.delete(key);
  }
  } finally { progress?.finish(); }
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

function workspaceReady() {
  document.getElementById("startup")?.remove();
  document.dispatchEvent(new Event("workspace-ready"));
}

function login(msg) {
  disposeMapPanel?.();
  workspaceReady();
  aiMode.workflow = false;
  caseSession?.controller?.dispose();
  caseSession = null;
  for (const id of Object.keys(fundingAi)) delete fundingAi[id];
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
  caseSession?.controller?.dispose();
  caseSession = null;
  me = await api("/api/me");
  Object.assign(listState, defaultListState());
  queueOrigin = "mine";
  briefingBox = null;
  document.getElementById("who").textContent = `${me.user.name}, ${me.user.role}`;
  showAccount();
  const nav = document.getElementById("nav");
  nav.replaceChildren(...me.navigation.map((item) => h("a", { href: item.href }, item.label)));
  nav.hidden = false;
  workspaceReady();
  await route();
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

const workspaceScriptLoads = new Map();

function retryWorkspaceScript(path) {
  if (!workspaceScriptLoads.has(path)) {
    workspaceScriptLoads.set(path, (async () => {
      for (let attempt = 1; attempt <= 2; attempt++) {
        await new Promise((resolve) => setTimeout(resolve, 250 * attempt));
        const outcome = await new Promise((resolve) => {
          const script = document.createElement("script");
          const finish = (result) => {
            clearTimeout(timer);
            script.onload = script.onerror = null;
            script.remove();
            resolve(result);
          };
          const timer = setTimeout(() => finish("timeout"), 5000);
          script.onload = () => finish("load");
          script.onerror = () => finish("error");
          script.src = path;
          document.head.append(script);
        });
        // A timed-out or evaluated script may still install lexical declarations.
        if (outcome !== "error") break;
      }
    })());
  }
  return workspaceScriptLoads.get(path);
}

function missingWorkspaceScripts(hash, caseRoute) {
  const destination = hash.split("?")[0];
  const contractor = me?.user.role === "Contractor";
  const staffCase = Boolean(me) && caseRoute && !contractor;
  const staffDestination = Boolean(me) && !contractor && !caseRoute;
  return [
    ["/async-action.js", true, typeof AsyncAction !== "undefined" && AsyncAction
      && ["handler", "run", "feedback"].every(method => typeof AsyncAction[method] === "function")],
    ["/ops.js", staffCase || (staffDestination && hash === "#/capacity") || (contractor && !caseRoute && destination !== "#/screens"), typeof qualityPanel === "function"],
    ["/panels.js", staffCase || (staffDestination && hash === "#/finance"), typeof financePanel === "function"],
    ["/assistants.js", staffCase || (staffDestination && hash === "#/assistants"), typeof assistantCasePanel === "function"],
    ["/chat.js", staffCase, typeof chatCasePanel === "function"],
    ["/timecapture.js", staffDestination && hash === "#/time", typeof timeView === "function"],
    ["/role-screens.js", Boolean(me) && destination === "#/screens", typeof roleScreensView === "function"],
    ["/progress.js", staffDestination && ["#/progress", "#/closed"].includes(destination), typeof ProgressViews === "object"],
    ["/vendor/leaflet.js", staffDestination && (hash === "#/overview" || destination === "#/coordinator"), typeof L === "object"],
  ].filter(([, needed, loaded]) => needed && !loaded).map(([path]) => path);
}

async function requireWorkspaceScripts(hash, caseRoute) {
  const session = me;
  let missing = missingWorkspaceScripts(hash, caseRoute);
  if (missing.length) {
    workspaceStatus.textContent = "Loading workspace files. Please wait.";
    await Promise.all(missing.map(retryWorkspaceScript));
    if (me !== session) return;
    missing = missingWorkspaceScripts(hash, caseRoute);
  }
  if (missing.length) {
    const error = new Error(`Required workspace files did not load: ${missing.join(", ")}. Reload this page to try again. If this continues, ask application support to check these files.`);
    error.reloadWorkspace = true;
    throw error;
  }
}

function hasUnsavedChanges() {
  if (caseSession) rememberCaseFields(caseSession);
  return Boolean(document.querySelector('form[data-unsaved="true"], [data-case-dirty="true"]')
    || caseSession?.pendingFields.size);
}

async function route() {
  const session = me;
  if (!session) return;
  const nextHash = location.hash || "#/";
  if (nextHash !== displayedHash && caseSession?.controller
      && nextHash.split("?")[0] === displayedHash.split("?")[0]
      && nextHash.split("?")[0] === `#/case/${encodeURIComponent(caseSession.id)}`) {
    const before = new URLSearchParams(displayedHash.split("?")[1] || "");
    const after = new URLSearchParams(nextHash.split("?")[1] || "");
    before.delete("tab"); after.delete("tab");
    if (before.toString() === after.toString()) {
      caseSession.controller.select(new URLSearchParams(nextHash.split("?")[1] || "").get("tab"));
      displayedHash = nextHash;
      return;
    }
  }
  if (nextHash !== displayedHash && hasUnsavedChanges()) {
    if (!window.confirm("Leave this screen and discard unsaved changes?")) {
      history.replaceState(null, "", displayedHash);
      return;
    }
  }
  if (nextHash !== displayedHash) delete me.assistantQueueDrafts;
  displayedHash = nextHash;
  if (caseSession && nextHash.split("?")[0] !== `#/case/${encodeURIComponent(caseSession.id)}`) {
    caseSession.controller?.dispose();
    delete fundingAi[caseSession.id];
    caseSession = null;
  }
  routeController.abort();
  routeController = new AbortController();
  clearTimeout(searchTimer);
  const signal = routeController.signal;
  const hash = location.hash || "#/";
  const m = location.hash.match(/^#\/case\/([^?]+)(?:\?.*)?$/);
  const active = m ? (coordinatorOrigin ? "#/overview" : queueOrigin === "all" ? "#/all" : "#/") : hash.startsWith("#/coordinator") ? "#/overview" : hash.split("?")[0];
  document.querySelectorAll("#nav a").forEach((link) => {
    if (link.getAttribute("href") === active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  const destination = me.navigation.find((item) => item.href === active);
  const routeStatus = `${me.user.role}. ${destination?.scope || "Case workspace"}.`;
  workspaceStatus.textContent = routeStatus;
  try {
  await requireWorkspaceScripts(hash, Boolean(m));
  signal.throwIfAborted();
  if (me !== session) return;
  workspaceStatus.textContent = routeStatus;
  if (hash.split("?")[0] === "#/screens") return await roleScreensView();
  if (me.user.role === "Contractor") return await (m ? contractorCaseView(decodeURIComponent(m[1])) : contractorListView());
  if (m) return await caseView(decodeURIComponent(m[1]));
  const building = location.hash.match(/^#\/building\/(.+)$/);
  if (building) return await buildingView(decodeURIComponent(building[1]));
  if (hash === "#/assistants") return await assistantQueueView();
  if (hash === "#/time") return await timeView();
  if (hash.split("?")[0] === "#/closed") return await ProgressViews.closed();
  if (hash.split("?")[0] === "#/progress") return await ProgressViews.dashboard();
  if (hash === "#/capacity") return await capacityView();
  if (hash === "#/import") return await importView();
  if (hash === "#/overview") return await overviewView();
  if (hash.split("?")[0] === "#/coordinator") return await coordinatorView();
  if (hash === "#/visits") return await visitsView();
  if (hash === "#/funding") return await fundingView();
  if (hash === "#/finance") return await financeQueueView();
  return await listView(hash === "#/all" ? "all" : "mine");
  } catch (error) {
    if (signal.aborted || me !== session) return;
    workspaceStatus.textContent = `Workspace unavailable: ${error.message}`;
    show(h("h1", {}, "Workspace unavailable"), h("p", { class: "err", role: "alert" }, error.message),
      error.reloadWorkspace
        ? h("button", { type: "button", onclick: () => location.reload() }, "Reload workspace")
        : h("button", { type: "button", onclick: route }, "Try again"),
      m && h("a", { href: queueHref() }, "Back to the list"));
  }
}

const defaultListState = () => {
  const { view, ...filters } = me.work_queues?.default || {};
  return filters;
};
const listState = {};
const queueHref = () => coordinatorOrigin || (queueOrigin === "all" ? "#/all" : "#/");
const qs = (o) => Object.entries(o).filter(([, v]) => v).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join("&");
const isManager = () => ["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
const FLAGS = [
  ["hazard", "Safety issue open", "At least one recorded safety issue has not been released. The independent safety service still owns its response."],
  ["support", "Needs extra support", "The resident's recorded support status is Yes. Missing support information remains unknown, not No."],
  ["long", "Waiting 60+ days", "The case has spent at least 60 days in its current stage. This is a review signal, not a statutory deadline."],
  ["nodecision", "No resident decision yet", "The recorded resident decision is neither Accepted nor Declined. This does not imply consent or refusal."],
  ["funding", "Funding not confirmed", "The recorded funding status is not Confirmed. This signal does not approve funding or spending."],
];

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
  kids.push(h("p", { class: "muted" }, "Sources: " + (cites.join("; ") || "Not provided. Check the record before use.")));
  kids.push(h("p", { class: "muted" }, "Confidence: not provided. Confidence is not accuracy."));
  if (d.dropped_uncited) kids.push(h("p", { class: "muted" }, `${d.dropped_uncited} uncited statement(s) removed.`));
  kids.push(h("p", { class: "muted" }, d.approval === "Not reviewed"
    ? `${d.source === "ai" ? "AI suggestion, not approved" : "Template draft, not approved"}. Not an instruction. Not reviewed by a person yet.`
    : ["Accepted", "Edited", "Rejected"].includes(d.approval)
      ? `${d.approval} as a draft by a person. Not an instruction. This is not an approval, consent or safety decision.`
      : `${d.approval || "Review unavailable"}. Not reviewed by a person. Not an instruction. Request fresh evidence; ordinary case work stays available.`));
  if (d.record_id && d.approval === "Not reviewed") {
    const why = h("textarea", { id: `ai-reason-${d.record_id}`, name: "review-reason", autocomplete: "off", rows: 4, maxlength: 300 });
    const editing = !getText && typeof d.text === "string" ? h("textarea", { id: `ai-edit-${d.record_id}`, name: "edited-draft", autocomplete: "off", rows: 8 }, d.text) : null;
    const error = h("p", { id: `ai-error-${d.record_id}`, class: "field-error", role: "status" });
    const result = h("p", { role: "status" });
    const invalid = text => {
      error.textContent = text; why.setAttribute("aria-invalid", "true");
      why.setAttribute("aria-describedby", error.id);
      if (reasonBox.hidden) { error.tabIndex = -1; error.focus(); } else why.focus();
    };
    let pending = false, checkHistory = false;
    const go = (action) => async () => {
      if (pending || checkHistory || d.approval !== "Not reviewed") return;
      error.textContent = "";
      why.removeAttribute("aria-invalid");
      why.removeAttribute("aria-describedby");
      if (action !== "accept" && !why.value.trim()) { invalid("Enter a reason to edit or reject this draft."); return; }
      const reason = action === "accept" ? "" : why.value;
      const text = action === "edit" ? getText ? getText() : editing?.value : undefined;
      const sent = snapshotCaseFields([...(action === "accept" ? [] : [why]), ...(action === "edit" && editing ? [editing] : [])]);
      const buttons = [...box.querySelectorAll("button")].map(button => ({ button, disabled: button.disabled }));
      pending = true;
      meta.dataset.reviewPending = "pending";
      buttons.forEach(({ button }) => { button.disabled = true; });
      result.textContent = "Recording your review...";
      try {
        await api(`/api/ai/review/${d.record_id}/${action}`, { reason, text });
        d.approval = REVIEWED[action];
        meta.dataset.reviewState = d.approval;
        result.textContent = `${d.approval} as a draft by a person. This is not an approval, consent or safety decision. Reason: ${reason || "Not supplied"}. Recorded in the audit log.`;
        reconcileCaseSubmission(sent);
        const later = [why, editing].filter(field => field?.dataset.caseDirty);
        box.hidden = !later.length;
        if (later.length) {
          box.querySelector("legend").textContent = `Unsubmitted edits for reviewed record ${d.record_id}`;
          box.prepend(h("p", { role: "status" }, "These later edits were not submitted. Copy what you need before discarding them. This review is complete; request fresh evidence for another review."));
          reasonBox.hidden = !why.dataset.caseDirty;
          editBox.hidden = !editing?.dataset.caseDirty;
          [why, editing].filter(Boolean).forEach(field => { field.readOnly = true; });
        }
        app.dispatchEvent(new Event("ai-review-change"));
        if (onDone) onDone(action, text);
      } catch (e) {
        checkHistory = mutationNeedsHistory(e);
        if (checkHistory) meta.dataset.reviewPending = "check-history";
        if (d.approval === "Not reviewed" && !checkHistory) {
          buttons.forEach(({ button, disabled }) => { button.disabled = disabled; });
        }
        result.textContent = checkHistory
          ? `Confirmation needs checking. Reload the workspace and check the review history before another action. ${e.message}` : e.message;
      } finally {
        pending = false;
        if (!checkHistory) meta.removeAttribute("data-review-pending");
      }
    };
    const unavailable = d.stale || d.verified === false || d.validated === false;
    const editBox = h("div", { hidden: true },
      editing && h("label", { for: editing.id }, "Edited draft"), editing,
      getText && h("p", {}, "Change the draft in the text box above, then record why you changed it."));
    let selected = null, reviewChoice = null;
    const reasonBox = h("div", { hidden: true }, h("label", { for: why.id }, "Reason"), why);
    const submit = h("button", { type: "button", hidden: true, onclick: () => go(selected)() });
    const cancel = h("button", { type: "button", class: "alt", hidden: true, onclick: () => {
      selected = null; editBox.hidden = reasonBox.hidden = submit.hidden = cancel.hidden = true;
      error.textContent = ""; reviewChoice?.focus();
    } }, "Cancel review");
    const choose = (action, choice) => {
      reviewChoice = choice;
      selected = action; editBox.hidden = action !== "edit"; reasonBox.hidden = false;
      submit.hidden = cancel.hidden = false;
      submit.textContent = action === "edit" ? "Save edited draft review" : "Record rejection";
      if (action === "edit" && editing) editing.focus(); else why.focus();
    };
    const chooseEdit = h("button", { class: "alt", type: "button", disabled: unavailable || (!getText && !editing), onclick: event => choose("edit", event.currentTarget) }, "Edit this draft");
    const box = h("fieldset", {}, h("legend", {}, "Review this draft"),
      h("p", {}, "Use records only after checking them. Using a draft records your review only; it does not approve works, contact a resident or change any case."),
      error,
      unavailable && h("p", {}, "Accept unavailable: check the stale or unverified sources and request a fresh draft."),
      h("div", { class: "row review-choices" }, h("button", { class: "alt", type: "button", disabled: unavailable, onclick: go("accept") }, "Use this draft"),
        chooseEdit, h("button", { class: "alt", type: "button", onclick: event => choose("reject", event.currentTarget) }, "Do not use this draft")),
      editBox, reasonBox, h("div", { class: "row" }, submit, cancel));
    why.addEventListener("input", () => {
      why.dataset.caseDirty = "true";
      error.textContent = ""; why.removeAttribute("aria-invalid"); why.removeAttribute("aria-describedby");
    });
    editing?.addEventListener("input", () => { editing.dataset.caseDirty = "true"; });
    kids.push(box, result);
  }
  const meta = h("div", { class: "aimeta ai-suggestion", "data-record-id": d.record_id, "data-review-state": d.approval }, kids);
  return meta;
}
const REVIEWED = { accept: "Accepted", edit: "Edited", reject: "Rejected" };

function aiBox() {
  const number = new Intl.NumberFormat("en-GB");
  const box = h("section", { class: "card ai briefing" }, h("h2", {}, "Today's briefing"));
  const content = h("div", { class: "briefing-content" });
  const status = h("p", { role: "status", "aria-live": "polite" });
  const toggle = h("select", { id: "wf-mode", name: "assistance-mode", onchange: () => load() },
    h("option", { value: "ai" }, "Allow AI suggestions"),
    h("option", { value: "workflow" }, "Use rules and templates, without AI"));
  toggle.value = aiMode.workflow ? "workflow" : "ai";
  const mode = h("div", {}, h("label", { for: "wf-mode" }, "How to prepare briefings and draft requests"), toggle,
    h("p", { class: "muted" }, "This choice applies to your briefing and draft requests until you sign out or reload. Rules and templates never call AI. Ordinary case work stays available."));
  const dismiss = h("button", { type: "button", class: "alt", onclick: () => {
    const hidden = !content.hidden; content.hidden = mode.hidden = hidden;
    dismiss.textContent = hidden ? "Show briefing" : "Hide briefing";
    status.textContent = hidden ? "Briefing hidden. No review or case record changed. Choose Show briefing to undo." : "Briefing shown.";
  } }, "Hide briefing");
  const source = (cite, caseIds) => {
    const prefix = cite.split(": ")[0];
    const id = caseIds.includes(prefix) ? prefix : caseIds.length === 1 ? caseIds[0] : null;
    return id
      ? h("a", { href: `#/case/${encodeURIComponent(id)}` }, cite) : cite;
  };
  const paint = b => {
    const ai = b.source === "ai";
    const refreshed = b.generated_at ? new Date(b.generated_at) : null;
    content.replaceChildren(h("h3", {}, b.scope_label),
      h("p", { class: "muted" }, `${number.format(b.case_count)} permitted open ${b.case_count === 1 ? "case" : "cases"}. ${number.format(b.summary_count)} included in this summary (up to 8).`),
      h("p", { class: "ai-label" }, ai ? "AI suggestion, not approved. Not an instruction." : "Summary by rules. Not an instruction."),
      h("p", {}, "Why these cases: the fixed case ranking selects the first permitted open cases, with safety first. This briefing does not change that order. Check the linked records before using the text."),
      h("p", { class: "muted" }, "Prepared at: ", refreshed && !Number.isNaN(refreshed.valueOf())
        ? h("time", { datetime: b.generated_at }, new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "long" }).format(refreshed))
        : "Not provided. Refresh to request current records."),
      h("h3", {}, ai ? "Generated briefing and its sources" : "Rules-derived summary and its sources"),
      h("ol", { class: "briefing-statements" }, (b.statements || [{ text: b.text, citations: [], unresolved: [] }]).map(statement => h("li", {},
        h("p", {}, statement.text),
        h("details", {}, h("summary", {}, `Sources used (${statement.citations.length})`),
          statement.citations.length ? h("ul", {}, statement.citations.map(cite => h("li", {}, source(cite, b.source_case_ids || [])))) : h("p", {}, "No statement references were provided. Check the case record."),
          statement.unresolved?.length ? h("p", { class: "err" }, `These references do not match the record: ${statement.unresolved.join("; ")}. Do not rely on this statement.`) : null)))),
      h("p", {}, "References show what was cited, not whether the statement is correct. Correct the draft or explain why you will not use it below. Recorded reviews cannot be undone."),
      aiNotes(b), h("button", { type: "button", class: "alt", onclick: () => load() }, "Refresh briefing"));
  };
  let sequence = 0, loading = false;
  const load = async () => {
    if (loading) return;
    if (content.querySelector("[data-review-pending]")) {
      toggle.value = aiMode.workflow ? "workflow" : "ai";
      status.textContent = "Finish the pending review first. If confirmation needs checking, reload the workspace and check review history before requesting a fresh briefing.";
      return;
    }
    if (content.querySelector('[data-case-dirty="true"]')
        && !window.confirm("Replace this briefing and discard its unsubmitted review edits? Copy anything you need first.")) {
      toggle.value = aiMode.workflow ? "workflow" : "ai";
      return;
    }
    aiMode.workflow = toggle.value === "workflow";
    loading = true;
    toggle.disabled = true;
    content.inert = true;
    const own = ++sequence;
    const signal = routeController.signal;
    const cancel = () => { if (briefingBox === box) briefingBox = null; };
    signal.addEventListener("abort", cancel, { once: true });
    content.setAttribute("aria-busy", "true");
    status.textContent = "Reading case summaries...";
    try {
      const b = await api(`/api/briefing${aiMode.workflow ? "?mode=workflow" : ""}`, undefined, signal);
      if (signal.aborted || own !== sequence) return;
      paint(b); status.textContent = "Briefing ready. Check the sources, then choose how to review the draft.";
    } catch (error) {
      if (signal.aborted || own !== sequence) return;
      status.textContent = `Briefing unavailable: ${error.message}. Try loading the briefing again.`;
      if (!content.childElementCount) {
        content.replaceChildren(h("button", { type: "button", onclick: () => load() }, "Try loading briefing again"));
      }
    } finally {
      signal.removeEventListener("abort", cancel);
      if (own === sequence) {
        content.removeAttribute("aria-busy");
        content.inert = false;
        toggle.disabled = false;
        loading = false;
      }
    }
  };
  box.append(status, dismiss, mode, content);
  load();
  return box;
}

function priorityPanel() {
  const box = h("section", { class: "card ai", "aria-label": "AI priority suggestion" });
  let pending = false, checkHistory = false;
  const rowsOf = (items, withReason) => h("ol", {}, items.map((i) => h("li", {},
    h("a", { href: `#/case/${encodeURIComponent(i.case_id)}` }, `${i.resident}, ${i.address}`), ` (rank ${i.rank})`,
    withReason && i.reason ? h("div", { class: "muted" }, i.reason, i.cites && i.cites.length ? ` Sources: ${i.cites.join("; ")}.` : "") : null)));
  const paint = (rec, msg) => {
    const kids = [h("h2", {}, "Which cases first? A second opinion"),
      h("p", { class: "muted" }, "The rule-based order below is the list order. The AI suggestion, not approved, is advice only: it never changes the ranking, owners, stages or queues.")];
    if (msg) kids.push(h("p", { role: "alert" }, msg));
    if (rec && rec.release_denied) kids.push(h("p", { role: "status" }, "This suggestion's release is no longer valid. Use the ordinary case controls or request a new suggestion. The release owner must review the missing evidence."));
    if (rec?.stale) kids.push(h("p", { role: "status" }, "A supplied human correction affects this suggestion. It and any recorded draft review need a fresh review. Use ordinary case work or request a new suggestion."));
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
          if (pending || checkHistory) return;
          const items = rec.items.filter((_, n) => keep[n].checked).map((i) => ({ case_id: i.case_id, reason: i.reason }));
          pending = true;
          const buttons = [...box.querySelectorAll("button")].map(button => ({ button, disabled: button.disabled }));
          buttons.forEach(({ button }) => { button.disabled = true; });
          try { paint(await api(`/api/ai/priority/${rec.id}/${action}`, { reason: why.value, items })); }
          catch (e) {
            checkHistory = mutationNeedsHistory(e);
            if (!checkHistory) buttons.forEach(({ button, disabled }) => { button.disabled = disabled; });
            box.append(h("p", { role: "status" }, checkHistory
              ? `Reload the workspace and check priority review history before another action. ${e.message}` : e.message));
          } finally { pending = false; }
        };
        kids.push(h("div", { class: "row" }, h("label", { for: "pri-why" }, "Your reason"), why),
          h("div", { class: "row" }, h("span", { class: "muted" }, "To edit, untick cases to drop:"), rec.items.map((i, n) => h("label", {}, keep[n], ` ${i.resident}`))),
          h("div", { class: "row" }, h("button", { disabled: checkHistory || rec.actionable === false, onclick: act("accept") }, "Accept"), h("button", { class: "alt", disabled: checkHistory || rec.actionable === false, onclick: act("edit") }, "Edit"),
            h("button", { class: "alt", disabled: checkHistory, onclick: act("reject") }, "Reject")));
      } else {
        kids.push(h("p", {}, `${rec.status}${rec.reason ? `: ${rec.reason}` : ""}. Recorded in the audit log.`),
          h("p", {}, h("button", { class: "alt", onclick: ask }, "Suggest again")));
      }
    }
    box.replaceChildren(...kids);
  };
  const ask = async () => { box.setAttribute("aria-busy", "true"); try { paint(await api("/api/ai/priority", modeBody({ n: 5 }))); } catch (e) { paint(null, e.message); } box.removeAttribute("aria-busy"); };
  box.append(h("p", { role: "status" }, "Loading priority suggestions..."));
  api("/api/ai/priority").then((d) => paint(d.recommendation && d.recommendation.status === "Proposed" ? d.recommendation : null)).catch(error => {
    if (error.name !== "AbortError") paint(null, `Priority suggestions unavailable: ${error.message}. Try requesting a suggestion again.`);
  });
  return box;
}

function pendingHandoffs() {
  const box = h("section", { class: "card", "aria-label": "Handoffs waiting for you" },
    h("p", { role: "status" }, "Loading handoffs..."));
  api("/api/handoffs").then((rows) => {
    if (!rows.length) { box.hidden = true; return; }
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
    h("p", { class: "muted" }, `Source: ${work.source}; evidence: ${work.evidence}; version: ${work.version}; recorded: ${work.recorded_at}; recorded as of: ${work.as_of}.`),
    work.handoff && h("p", {}, `Destination: ${work.handoff.destination}; proposed receiver: ${work.handoff.proposed_receiver}; confirmed receiver: ${work.handoff.confirmed_receiver}; chase owner: ${work.handoff.chase_owner}; resident-update owner: ${work.handoff.resident_update_owner}.`),
    work.hazard_clocks.map((clock) => h("p", { class: "safety-clock" },
      `Safety clock in this recorded view: ${clock.elapsed_hours === null ? "Unknown" : `${clock.elapsed_hours} elapsed hours`}; awareness: ${clock.aware_at}; named follow-up owner: ${clock.owner}; service response due: ${clock.response_due_at}; resident update due: ${clock.resident_update_due_at}. ${clock.authority} owns timing.`)));
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
      h("p", {}, `Case ${work.case_id}; definition ${work.definition_version}; recorded as of ${work.as_of}. Missing evidence stays Unknown; freshness does not establish validity.`),
      h("ul", {}, work.evidence_freshness.map((item) => h("li", {},
        `${item.kind}: ${item.status}; record date: ${item.recorded_at}; evidence: ${item.evidence}; source: ${item.source}; version: ${item.version}.`)))));
}

async function listView(view) {
  coordinatorOrigin = null;
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
    workspaceStatus.textContent = `Perspective: ${me.user.role}. ${view === "mine" ? "My assigned cases" : "All permitted open cases"}. ${total} ${total === 1 ? "case" : "cases"}. Workflow stage: ${listState.stage || "any"}. Search: ${listState.q || "none"}. All-cases scope: ${view === "all" ? "on (permitted cases only)" : "off (my assigned cases)"}. Workflow stage narrows this perspective's own/all scope; it never changes your role or access. Area: ${listState.area || "any"}. Wave: ${listState.wave || "any"}. Owner: ${listState.owner || "any"}. Show only: ${listState.flag || "any"}. Work queue: ${listState.queue || "any"}. Order: ${fx.sorts[listState.sort]}. Default: ${me.work_queues.version}; selection: none.`;
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
    el.addEventListener("change", AsyncAction.handler(() => { listState[key] = el.value; return load(); }));
    return [h("label", { for: `f-${key}` }, label), el];
  };
  const search = h("input", { id: "f-q", name: "q", type: "search", autocomplete: "off", placeholder: "Name, address or postcode" });
  search.value = listState.q;
  search.addEventListener("input", () => { listState.q = search.value; clearTimeout(searchTimer); searchTimer = setTimeout(() => AsyncAction.run(null, () => load(), "Finding cases", side), 250); });
  const sort = h("select", { id: "f-sort" }, Object.entries(fx.sorts).map(([k, t]) => h("option", { value: k }, t)));
  sort.value = listState.sort;
  sort.addEventListener("change", AsyncAction.handler(() => { listState.sort = sort.value; return load(); }));
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
      const target = me.work_queues.default.view === "all" ? "#/all" : "#/";
      if (location.hash !== target) location.hash = target;
      else return route();
    } }, "Reset my queue")),
    h("p", { class: "muted" }, `Default ${me.work_queues.version}: returns to ${me.work_queues.default.view === "all" ? "all permitted open cases" : "your assigned cases"}, ${fx.sorts[me.work_queues.default.sort]}, first page and no case selection. No records change.`),
    h("details", {}, h("summary", {}, "Queue definitions"),
      h("p", {}, me.work_queues.status), h("p", {}, me.work_queues.clock),
      h("p", {}, "Your authenticated role determines access. Work queue, search and other filters narrow the chosen own/all scope together; they never change your role."),
      h("dl", {}, me.work_queues.definitions.flatMap((d) => [
        h("dt", {}, d.label), h("dd", {}, d.definition, d.limitation ? ` Unavailable: ${d.limitation}` : "")
      ])),
      h("h3", {}, "Show only signals"),
      h("dl", {}, FLAGS.flatMap(([, label, definition]) => [
        h("dt", {}, label), h("dd", {}, definition)
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
  if (!caseSession || caseSession.id !== id) caseSession = {
    id, draftBox: h("div", { id: "resident-draft-output" }),
    documentBox: h("div", { role: "status" }), pendingFields: new Map(),
  };
  const session = caseSession;
  const sameCase = app.querySelector("[data-case-workspace]")?.dataset.caseWorkspace === id;
  const firstLoad = !sameCase;
  if (firstLoad) show(h("a", { href: queueHref() }, "Back to the list"),
    h("section", { "aria-label": "Case summary", "aria-busy": "true", class: "card" }, "Loading case (loading)"));
  const recoveryGeneration = session.historyGeneration;
  const c = await api(`/api/cases/${encodeURIComponent(id)}`);
  if (caseSession !== session) return;
  if (session.historyGeneration !== recoveryGeneration) return;
  delete session.historyBarrier;
  session.assistantRequests?.forEach((state, key) => {
    if (state === "check-history") session.assistantRequests.delete(key);
  });
  session.pendingSubmissions?.forEach((state, key) => {
    if (state === "check-history") session.pendingSubmissions.delete(key);
  });
  const savedFields = sameCase ? rememberCaseFields(session) : [];
  session.controller?.dispose();
  const assistantPanel = assistantCasePanel(id, session);
  const r = c.resident, hm = c.home;
  const openHaz = c.hazards.filter((x) => !x.released);
  const msg = h("div", { role: "status" });
  const refresh = async (fn, submitted = []) => {
    const sent = snapshotCaseFields(submitted);
    const key = sent.length ? JSON.stringify(sent.map(item => item.key)) : null;
    session.pendingSubmissions ||= new Map();
    if (session.historyBarrier || (key && session.pendingSubmissions.has(key))) {
      workspaceStatus.textContent = "This action is pending or needs a history check. Refresh before another submission.";
      return "check-history";
    }
    if (key) session.pendingSubmissions.set(key, "pending");
    let recorded = false;
    let checkHistory = false;
    try {
      await fn();
      recorded = true;
      if (caseSession !== session) return;
      reconcileCaseSubmission(sent);
      briefingBox = null; await caseView(id);
      return true;
    } catch (e) {
      if (caseSession !== session) return;
      const uncertain = !recorded && mutationNeedsHistory(e);
      checkHistory = recorded || uncertain;
      if (checkHistory) requireCaseHistory(session);
      msg.replaceChildren(h("p", { class: "err" }, recorded
        ? `Your change was recorded, but the case could not reload. Refresh the case before another action. ${e.message}`
        : uncertain ? `Confirmation is unavailable. Refresh and check the history before another action. ${e.message}` : e.message),
      ...(e.reasons || []).map((x) => h("p", {}, x)));
      if (!msg.isConnected) workspaceStatus.textContent = msg.textContent;
      return recorded || uncertain ? "check-history" : false;
    } finally {
      if (key) {
        if (checkHistory) session.pendingSubmissions.set(key, "check-history");
        else session.pendingSubmissions.delete(key);
      }
    }
  };
  const outcome = h("input", { id: "outcome", placeholder: "For example: spoke to resident, visit agreed" });
  const note = h("textarea", { id: "note", "aria-label": "Notes" });
  const channel = h("select", { "aria-label": "How you spoke" }, ["Phone", "Text message", "Email", "Visit"].map((x) => h("option", {}, x)));
  const draftBox = session.draftBox;
  const kind = async (k) => {
    try {
      const d = await api(`/api/cases/${encodeURIComponent(id)}/draft`, { kind: k });
      if (!confirmCaseDraftReplacement(draftBox)) return;
      draftBox.replaceChildren(h("p", { class: "muted" }, d.note), h("textarea", { "aria-label": "Draft message", name: "resident-template", autocomplete: "off" }, d.text));
      draftBox.querySelector("textarea").value = d.text;
    } catch (error) {
      draftBox.append(h("p", { class: "err", role: "alert" }, error.message));
    }
  };
  const aiRun = async (task) => {
    if (!confirmCaseDraftReplacement(draftBox)) return;
    draftBox.replaceChildren(h("p", { class: "muted" }, "Working on it..."));
    try {
      const d = await api(`/api/cases/${encodeURIComponent(id)}/ai`, modeBody({ task }));
      const ta = h("textarea", { "aria-label": "Draft", name: "resident-ai-draft", autocomplete: "off", rows: 9 });
      ta.value = d.text;
      if (!confirmCaseDraftReplacement(draftBox)) return;
      draftBox.replaceChildren(h("p", { class: "muted" }, `${d.label}. Nothing is sent. Change it as you like.`), ta, aiNotes(d, null, () => ta.value));
      app.dispatchEvent(new Event("ai-review-change"));
    } catch (e) {
      const error = h("p", { class: "err", role: "alert" }, e.message);
      if (draftBox.querySelector('[data-case-dirty="true"]')) draftBox.append(error);
      else draftBox.replaceChildren(error);
    }
  };
  const canOffer = !c.closed && (c.owner_code === me.user.code || isManager()) &&
    (!c.handoff || !["Offered", "Received", "Escalated", "Accepted"].includes(c.handoff.state));
  const sugg = h("section", { class: "card" }, h("h2", {}, "Who could take this on"),
    h("p", { class: "muted" }, "Suggested by role and workload rules. You decide."),
    workSummary(c.work),
    h("p", {}, "These are proposed reviewers, not confirmed receiving owners. Review the recorded blocked steps and prerequisites above."),
    !c.suggestions.length && h("p", {}, "Proposed owner: Unknown. No reviewer is supplied for this case. The current owner keeps responsibility."),
    h("ul", { class: "list" }, c.suggestions.map((x) => h("li", {},
      h("strong", {}, `${x.name}, ${x.role}`), h("div", { class: "muted" }, x.reasons.join(". ")),
      canOffer && h("button", { class: "alt", onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/handover`, { to: x.email })) }, `Offer to ${x.name.split(" ")[0]}`)))));
  const challengeDrafts = captureChallengeDrafts(id);
  const cost = c.cost_allocation && h("section", { class: "card" }, h("h2", {}, "This home's cost allocation"),
      h("p", {}, "Recorded allocations only, not additional building costs or payment approval."),
      h("ul", {}, c.cost_allocation.map((x) => h("li", {}, `${x.shared_cost_id}: GBP ${x.amount_gbp}. Source: ${x.source}`))));
  const contact = h("section", { class: "card" }, h("h2", {}, "Contact"),
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
          h("dt", {}, "Last contact"), h("dd", {}, ago(c.contacts[0] && c.contacts[0].at))));
  const progress = h("section", { class: "card" }, h("h2", {}, "Where it is up to"),
        h("dl", {},
          h("dt", {}, "Stage"), h("dd", {}, c.stage),
          h("dt", {}, "In this stage"), h("dd", {}, `${c.days_in_stage} days`),
          h("dt", {}, "Case owner"), h("dd", {}, `${c.owner}, ${c.owner_role}`),
          h("dt", {}, "Works"), h("dd", {}, c.measures),
          h("dt", {}, "Home"), h("dd", {}, `${hm.type}, built ${hm.built}, EPC ${hm.epc}, ${hm.tenure}`),
          h("dt", {}, "Historical case-wide answer (not scope consent)"), h("dd", {}, `${c.decision.status}${c.decision.by ? ` (recorded by ${c.decision.by})` : ""}`)));
  const call = h("section", { class: "card" }, h("h2", {}, "Log a call"),
      h("label", { for: "outcome" }, "What happened"), outcome,
      h("label", {}, "How you spoke", channel),
      h("label", { for: "note" }, "Notes"), note,
      h("p", {}, h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/call`, { outcome: outcome.value, note: note.value, channel: channel.value }), [outcome, note, channel]) }, "Save")));
  const finalChecks = c.can_advance && h("section", { class: "card" }, h("h2", {}, "Final checks"),
      c.gate.length ? [h("p", {}, "This case cannot move on yet:"), h("ul", {}, c.gate.map((x) => h("li", {}, x)))] : h("p", {}, "Everything is in place."),
      h("button", { onclick: () => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/advance`, {})) }, "Ready to book the installation"));
  const write = h("section", { class: "card" }, h("h2", {}, "Write to the resident"),
      h("div", { class: "row" }, h("button", { onclick: () => aiRun("message") }, "Draft with AI"),
        h("button", { class: "alt", onclick: () => aiRun("summary") }, "Catch me up on this case"),
        h("button", { class: "alt", onclick: () => kind("visit") }, "Plain visit template"),
        h("button", { class: "alt", onclick: () => kind("update") }, "Plain update template")), draftBox);
  const historyPanel = h("section", { class: "card" }, h("h2", {}, "History"),
      h("p", {}, "Current task context below; event-time owners and reasons in the history remain unchanged."),
      workSummary(c.work),
      c.contacts.length ? h("ul", { class: "tl" }, c.contacts.slice(0, 15).map((k) => h("li", {},
        h("strong", {}, `${fmtDate(k.at)} ${k.channel}: ${k.outcome}`), h("div", { class: "muted" }, `${k.by}${k.note ? `. ${k.note}` : ""}`)))) : h("p", {}, "No contact recorded yet."));
  const safety = safetyPanel(c, id, refresh);
  safety.id = "case-safety";
  if (openHaz.length) safety.classList.add("blocked");
  const returned = returnPanel(c, id, refresh);
  const signals = [
    [c.work.evidence_freshness.some(item => item.status === "Stale"), "Stale evidence"],
    [c.work.owner === "Unknown" || c.work.blockers.some(item => item.owner === "Unknown")
      || (c.work.handoff && ["Offered", "Received", "Escalated"].includes(c.work.handoff.state)), "Unclear owner"],
    [c.funding.status !== "Confirmed", "Funding not confirmed"],
    [!["Accepted", "Declined"].includes(c.decision.status), "No resident decision yet"],
    [Boolean(c.returns?.length) || c.stage === "Design being corrected", "Rework recorded"],
  ].filter(([present]) => present).map(([, label]) => label);
  const chatPanel = session.chatPanel ||= chatCasePanel(id);
  const definitions = [
    ["overview", "Overview", [c.closed && returned, workSummary(c.work), progress, contact, cost, finalChecks]],
    ["blockers", `Blockers and safety (${c.work.blockers.length})`, [
      h("section", { class: "card" }, h("h2", {}, "Review signals"),
        h("p", {}, "These signals do not stop unrelated work or make an approval."),
        signals.length ? h("ul", { class: "row list" }, signals.map(label => h("li", { class: "flag" }, label))) : h("p", {}, "No recorded review signals.")),
      workSteps(c.work), openHaz.length ? h("p", {}, h("a", { href: "#case-safety", onclick: event => { event.preventDefault(); safety.querySelector("h2").tabIndex = -1; safety.querySelector("h2").focus(); } }, "Review the safety actions above the journey")) : safety,
      regulatoryAlertsPanel(id), !c.closed && returned, stockPanel(c)]],
    ["survey", "Survey and assessment", [technicalPanel(c, id, refresh), documentsPanel(c, id, refresh)]],
    ["funding", "Funding", [fundingPanel(c, id, refresh, savedFields, session), financePanel(c, id, refresh), grantPanel(c, id, refresh)]],
    ["resident", "Resident", [residentPanel(c, id, refresh), call, write, affectedChallengePanel(c, id, refresh)]],
    ["contractor", "Contractor and works", [h("section", { class: "card" }, h("h2", {}, "Contractor and appointments"),
      h("p", {}, `${c.contractor.name}, ${c.contractor.contact}, ${c.contractor.phone}`),
      h("p", {}, `Next visit: ${fmtDate((c.appointments.find(a => a.outcome === "Booked") || {}).date)}`),
      c.appointments.length ? h("ul", {}, c.appointments.map(a => h("li", {}, `${fmtDate(a.date)}: ${a.type}, ${a.slot}, ${a.who}. ${a.outcome}`))) : h("p", {}, "No appointments recorded. Ask the case owner to record the next visit."))]],
    ["quality", "Quality and handover", [qualityPanel(c, id, refresh, savedFields, session), handoffPanel(c, id, refresh), sugg]],
    ["ai", "AI assistance", [assistantPanel, chatPanel,
      h("p", {}, "Resident message and summary drafts stay with the resident record.",
        h("button", { class: "alt", onclick: () => session.controller ? session.controller.select("resident", true, true) : document.getElementById("case-panel-resident").scrollIntoView() }, "Review resident drafts")),
      h("p", {}, "Funding drafts stay with the funding record.",
        h("button", { class: "alt", onclick: () => session.controller ? session.controller.select("funding", true, true) : document.getElementById("case-panel-funding").scrollIntoView() }, "Review funding drafts"))]],
    ["history", "History", [historyPanel]],
  ].map(([tab, label, nodes]) => ({ id: tab, label,
    panel: h("section", { id: `case-panel-${tab}`, class: "case-tab-panel" }, h("h2", { class: "case-section-title" }, label), nodes) }));
  const workspace = h("div", { "data-case-workspace": id }, definitions.map(tab => tab.panel), msg);
  let top = openHaz.length ? [safety] : [];
  if (typeof CaseWorkspace !== "undefined") {
    try {
      session.controller = CaseWorkspace.enhance(c, definitions, openHaz.length ? safety : null, assistantPanel, draftBox);
      top = session.controller.top;
    } catch (error) {
      session.controller = null;
      definitions.forEach(tab => {
        tab.panel.hidden = false;
        ["role", "aria-labelledby", "tabindex"].forEach(name => tab.panel.removeAttribute(name));
      });
      top.push(h("p", { class: "err", role: "alert" }, `Tab navigation unavailable: ${error.message}. Case sections are listed below; ordinary work continues.`));
    }
  } else top.push(h("p", { role: "status" }, "Tab navigation unavailable. Case sections are listed below; ordinary work continues."));
  show(h("a", { class: "back", href: queueHref() }, "Back to the list"),
    c.building_id ? h("a", { class: "back", href: `#/building/${encodeURIComponent(c.building_id)}` }, `Shared building context: ${c.building_id}`) : h("p", { class: "muted" }, "Building link not recorded; shared context is unknown."),
    h("div", { class: "row between" }, h("h1", {}, r.name,
      openHaz.length && h("span", { class: "flag danger" }, "Safety issue open")),
    h("span", { class: "muted" }, `Reference ${c.id}`)), top, workspace);
  restoreChallengeDrafts(challengeDrafts);
  restoreCaseFields([...session.pendingFields.values()]);
  restoreBoundFields(savedFields, app, "form", session);
  session.controller?.counts();
}

function caseFieldEntries(root = app, deduplicate = true) {
  const seen = new Map();
  const entries = [...root.querySelectorAll("input, textarea, select")].filter(field =>
    !field.closest("[data-challenge-case], #resident-draft-output")).map(field => {
    if (field.preservedCaseField) return { ...field.preservedCaseField, field };
    const proposal = field.closest("[data-proposal-id]");
    const prefix = proposal ? `${proposal.dataset.proposalId}:${proposal.dataset.proposalRevision}:` : "";
    const label = prefix + (field.id || `${field.closest("[id]")?.id}:${field.name || field.getAttribute("aria-label") || field.type}`);
    const index = seen.get(label) || 0;
    seen.set(label, index + 1);
    return { field, key: field.dataset.caseFieldKey || `${label}:${index}`, binding: field.caseBinding,
      proposal: proposal && { id: proposal.dataset.proposalId, revision: proposal.dataset.proposalRevision } };
  });
  if (!deduplicate) return entries;
  const byKey = new Map();
  entries.forEach(entry => {
    if (!byKey.has(entry.key) || !entry.field.preservedCaseField) byKey.set(entry.key, entry);
  });
  return [...byKey.values()];
}
function snapshotCaseFields(fields, session = caseSession) {
  const entries = new Map(caseFieldEntries(app, false).map(item => [item.field, item]));
  return fields.map(item => item.field ? item : { field: item, key: entries.get(item)?.key,
    session, value: item.value, checked: item.checked,
    files: item.files && [...item.files] });
}
function caseFieldUnchanged({ field, value, checked, files }) {
  const recovered = field.preservedCaseField;
  const selectedFiles = recovered?.fileNode?.files || field.files;
  return (recovered?.type === "checkbox" ? recovered.value : field.value) === value
    && (recovered ? recovered.checked : field.checked) === checked
    && (!files || (selectedFiles && files.length === selectedFiles.length
      && files.every((file, i) => selectedFiles[i] === file)));
}
function reconcileCaseSubmission(sent, session = caseSession) {
  const current = caseFieldEntries(app, false);
  const forms = new Set();
  sent.forEach(item => {
    const sameSession = item.session === session;
    const cached = sameSession && item.key && item.session?.pendingFields.get(item.key);
    const consumedCache = cached && cached.value === item.value && cached.checked === item.checked
      && (!cached.fileNode || caseFieldUnchanged({ ...item, field: cached.fileNode }));
    const fields = new Set([item.field, ...(sameSession && item.key
      ? current.filter(entry => entry.key === item.key).map(entry => entry.field) : [])]);
    [...fields].filter(field => caseFieldUnchanged({ ...item, field })).forEach(field => {
      const form = field.closest("form");
      if (form) forms.add(form);
      field.removeAttribute("data-case-dirty");
      if (field.preservedCaseField) field.parentElement.remove();
      else if (field.type === "checkbox") field.checked = false;
      else if (field.tagName !== "SELECT") field.value = "";
    });
    forms.forEach(form => {
      if (!form.querySelector('[data-case-dirty="true"]')) delete form.dataset.unsaved;
    });
    if (consumedCache) {
      item.session.pendingFields.delete(item.key);
    }
  });
  app.querySelectorAll("[data-case-recovery]").forEach(node => {
    if (!node.querySelector("textarea")) node.remove();
  });
}
function captureCaseFields() {
  return caseFieldEntries().filter(({ field }) => field.dataset.caseDirty)
    .map(({ field, key, proposal, binding }) => {
      const record = field.closest("[data-record-id]");
      const label = field.getAttribute("aria-label") || field.name || field.id;
      return { key, value: field.preservedCaseField?.type === "checkbox"
        ? field.preservedCaseField.value : field.value,
        checked: field.preservedCaseField?.checked ?? field.checked, proposal, binding,
        label: field.preservedCaseField?.label || `${label}${record ? ` for record ${record.dataset.recordId}` : ""}`,
        type: field.preservedCaseField?.type || field.type,
        fileNode: field.preservedCaseField?.fileNode || (field.type === "file" ? field : undefined) };
    });
}
function rememberCaseFields(session) {
  caseFieldEntries().forEach(({ key, field }) => {
    if (!field.dataset.caseDirty) session.pendingFields.delete(key);
  });
  const saved = captureCaseFields();
  saved.forEach(item => session.pendingFields.set(item.key, item));
  return [...session.pendingFields.values()];
}
function confirmCaseDraftReplacement(root) {
  if (root.querySelector('[data-case-dirty="true"]')
      && !window.confirm("Replace this draft and discard its unsubmitted edits? Copy anything you need first.")) return false;
  caseFieldEntries(root).forEach(({ key }) => caseSession?.pendingFields.delete(key));
  return true;
}
function restoreCaseFields(saved, root = app) {
  const fields = new Map(caseFieldEntries(root).map(({ key, field }) => [key, field]));
  saved.forEach(({ key, value, checked, fileNode }) => {
    const field = fields.get(key);
    if (field) {
      if (fileNode) {
        if (field !== fileNode) field.replaceWith(fileNode);
        return;
      }
      field.value = value; field.checked = checked; field.dataset.caseDirty = "true";
      for (let parent = field.parentElement; parent && parent.getAttribute("role") !== "tabpanel"; parent = parent.parentElement) {
        if (parent.tagName === "DETAILS") parent.open = true;
        if (parent.hasAttribute("data-proposal-edit")) parent.hidden = false;
      }
    }
  });
}
function restoreBoundFields(saved, panel, kind, session) {
  saved = [...session.pendingFields.values()];
  panel.querySelectorAll(`[data-case-recovery="${kind}"]`).forEach(node => node.remove());
  restoreCaseFields(saved, panel);
  const keys = new Set(caseFieldEntries(panel).map(({ key }) => key));
  const missing = saved.filter(item => (kind === "proposal" ? item.proposal
    : kind === "form" ? !item.proposal && !item.binding : item.binding?.kind === kind) && !keys.has(item.key));
  if (!missing.length) return;
  const recovery = h("details", { "data-case-recovery": kind }, h("summary", {}, "Unsubmitted review edits from earlier evidence"),
    h("p", { role: "status" }, "The evidence identity or version changed or is no longer available. These edits were not applied to different evidence. Copy what you need and check the current sources again."));
  missing.forEach(item => {
    const copy = h("textarea", { readonly: true, name: "earlier-draft", autocomplete: "off", "aria-label": `Earlier ${item.label}`,
      "data-case-dirty": "true" });
    copy.preservedCaseField = item;
    copy.value = item.type === "checkbox" ? String(item.checked) : item.value;
    const identity = item.proposal ? `${item.proposal.id}, revision ${item.proposal.revision}` : item.binding?.id || "Earlier form";
    recovery.append(h("div", {}, h("p", {}, `${identity}: ${item.label}`), copy));
  });
  recovery.append(h("button", { type: "button", class: "alt", onclick: () => {
    missing.forEach(item => session.pendingFields.delete(item.key));
    recovery.remove();
  } }, "Discard earlier review edits"));
  panel.append(recovery);
}
app.addEventListener("input", event => {
  if ((caseSession || event.target.closest("[data-assistant-queue]"))
      && event.target.matches("input, textarea, select")
      && !event.target.hasAttribute("data-case-navigation")
      && !event.target.closest("[data-challenge-case]")) event.target.dataset.caseDirty = "true";
});

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
      h("p", {}, h("button", { onclick: () => refresh(() => post(id, "reopen", metadata()), [why, source, next]) }, "Reopen case")), history);
  }
  const earlier = STAGES_ORDER.slice(0, Math.max(0, STAGES_ORDER.indexOf(c.stage)));
  if (!earlier.length) return history ? h("section", { class: "card" }, h("h2", {}, "Return and reopen history"), history) : null;
  const to = h("select", { id: "ret-to" }, earlier.map((x) => h("option", { value: x, selected: x === earlier[earlier.length - 1] }, x)));
  return h("section", { class: "card" }, h("h2", {}, "Send this case back"),
    h("p", { class: "muted" }, "Use this when something earlier needs redoing. A case can only go back to an earlier stage, and the reason is kept in the audit log."),
    h("label", { for: "ret-to" }, "Back to which stage"), to,
    h("label", { for: "ret-why" }, "Why it is going back"), why,
    ...fields(),
    h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "return", { ...metadata(), to_stage: to.value }), [why, source, next, to]) }, "Send back")), history);
}

function recordedChangeForm(prefix, label, fields, submit) {
  const status = h("div", { role: "status", "aria-live": "polite", id: `${prefix}-status` });
  const inputs = [
    ["source", "Source reference", 200],
    ["source_version", "Source version", 100],
    ["reason", "Reason for this change", 300]
  ].map(([name, title, limit]) => {
    const input = h("input", { id: `${prefix}-${name}`, name, type: "text", required: true,
      maxlength: limit, autocomplete: "off", "aria-describedby": `${prefix}-help ${prefix}-status` });
    return { name, input, node: h("div", {}, h("label", { for: input.id }, title), input) };
  });
  const button = h("button", { type: "submit" }, label);
  const form = h("form", { oninput: () => { form.dataset.unsaved = "true"; },
    onsubmit: async (e) => {
      e.preventDefault();
      if (button.disabled) return;
      for (const { input } of inputs) {
        input.setCustomValidity(input.value.trim() ? "" : "Enter this change detail.");
        if (!input.reportValidity()) { input.focus(); return; }
      }
      button.disabled = true;
      button.textContent = "Saving...";
      status.textContent = "Saving the recorded change...";
      let checkHistory = false;
      try {
        const sent = snapshotCaseFields([...form.querySelectorAll("input, textarea, select")]);
        const outcome = await submit(Object.fromEntries(inputs.map(({ name, input }) => [name, input.value.trim()])), sent);
        checkHistory = outcome === "check-history";
        if (outcome !== false && !checkHistory && sent.every(caseFieldUnchanged)) delete form.dataset.unsaved;
      } catch (error) {
        status.replaceChildren(h("p", { class: "err" }, error.message));
        status.setAttribute("tabindex", "-1");
        status.focus();
      } finally {
        button.disabled = checkHistory;
        button.textContent = label;
      }
    } },
  ...fields,
  h("p", { id: `${prefix}-help`, class: "muted" }, "Enter the source you checked, its version and why you are making this change. These details are kept with your name and the change. They do not approve any work."),
  ...inputs.map(({ node }) => node), button, status);
  inputs.forEach(({ input }) => input.addEventListener("input", () => input.setCustomValidity("")));
  return form;
}

window.addEventListener("beforeunload", (event) => {
  if (hasUnsavedChanges()) { event.preventDefault(); event.returnValue = ""; }
});

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
      kids.push(recordedChangeForm("ho-accept", "Accept this case", [], async (metadata, submitted) => {
        await refresh(() => post(id, "accept-handoff", { ...metadata, handoff_version: (c.handoff_history || []).length }), submitted);
      }),
        h("div", { class: "row" }, h("label", { for: "ho-why" }, "Reason if you cannot take it"), why,
          h("button", { class: "alt", onclick: () => refresh(() => post(id, "decline-handoff", { reason: why.value }), [why]) }, "Decline")));
    }
    if (hd.from_code === me.user.code || isManager()) {
      kids.push(h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "withdraw-handoff", {})) }, "Withdraw the offer")));
      if (hd.state !== "Escalated") {
        const manager = h("select", { id: "ho-escalate-to" }, me.staff.filter((s) => ["Retrofit Programme Manager", "Programme Support Officer"].includes(s.role)).map((s) => h("option", { value: s.email }, s.name)));
        const reason = h("input", { id: "ho-escalate-why", maxlength: 300 });
        kids.push(h("label", { for: "ho-escalate-to" }, "Escalate to manager"), manager,
          h("label", { for: "ho-escalate-why" }, "Escalation reason"), reason,
          h("button", { class: "alt", onclick: () => refresh(() => post(id, "escalate-handoff", { to: manager.value, reason: reason.value }), [manager, reason]) }, "Record manual escalation"));
      }
    }
  } else {
    if (hd) kids.push(h("p", { class: "muted" }, `Last handoff to ${hd.to_name}: ${hd.state}${hd.answer_note ? `. ${hd.answer_note}` : ""}.`));
    if (hd && hd.state === "Accepted" && hd.to_code === me.user.code && c.owner_code === me.user.code) {
      const done = h("input", { id: "ho-done", maxlength: 300 });
      kids.push(h("label", { for: "ho-done" }, "Completed action"), done,
        h("button", { onclick: () => refresh(() => post(id, "complete-handoff", { note: done.value }), [done]) }, "Complete handoff"));
    }
    if (!c.closed && (!hd || hd.state !== "Accepted") && (c.owner_code === me.user.code || isManager())) {
      const to = h("select", { id: "ho-to", name: "to", autocomplete: "off" }, me.staff.filter((s) => s.code !== c.owner_code && s.role !== "Contractor").map((s) => h("option", { value: s.email }, `${s.name} (${s.role})`)));
      const note = h("input", { id: "ho-note", name: "note", autocomplete: "off", type: "text", maxlength: 300 });
      const next = h("input", { id: "ho-next", name: "next_action", autocomplete: "off", maxlength: 300 });
      const urgency = h("select", { id: "ho-urgency", name: "urgency", autocomplete: "off" }, ["", "Routine", "Urgent"].map((x) => h("option", { value: x }, x || "Unknown")));
      const due = h("input", { id: "ho-due", name: "due_at", autocomplete: "off", type: "datetime-local" });
      const iso = (value) => value ? new Date(value).toISOString() : null;
      kids.push(recordedChangeForm("ho-offer", "Offer the case", [
        h("p", { class: "muted" }, "Offer the case. It only moves when the other person accepts."),
        h("label", { for: "ho-to" }, "Offer to"), to, h("label", { for: "ho-note" }, "Note for them (optional)"), note,
        h("label", { for: "ho-next" }, "Next action"), next, h("label", { for: "ho-urgency" }, "Urgency"), urgency,
        h("label", { for: "ho-due" }, "Human-selected due date (not an approved SLA)"), due,
        h("p", {}, c.resident_update ? "The existing resident-update commitment is preserved." : "Record a complete resident-update commitment in the resident panel. A handoff never creates or clears it.")
        ], async (metadata, submitted) => {
          await refresh(() => post(id, "offer-handoff", {
          ...metadata, handoff_version: (c.handoff_history || []).length,
          to: to.value, note: note.value, next_action: next.value, urgency: urgency.value, due_at: iso(due.value)
          }), submitted);
        }));
    }
  }
  const history = c.handoff_history || c.handoff_log;
  if (history && history.length) {
    kids.push(h("ul", { class: "tl" }, history.slice(-8).reverse().map((x) => h("li", {},
      `${fmtDate(x.at || x.answered_at)}: ${x.from_name} to ${x.to_name}, ${x.status || x.state}; current owner at event: ${x.accountable_owner || "Unknown"}; chase: ${x.chase_owner || "Unknown"}`,
      h("p", { class: "muted" }, `Source: ${x.source || "Unknown (legacy)"}; source version: ${x.source_version || "Unknown (legacy)"}; reason: ${x.reason || "Unknown (legacy)"}. Change version: ${x.version || "Unknown"}; recorded by: ${x.actor?.name || x.by || "Unknown"}.`)))));
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
    const action = (name) => refresh(() => post(id, name, { index: i, evidence: evidence.value, note: note.value }), name === "hazard-release" ? [evidence, note] : [evidence]);
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
      !x.released && !x.referral_version && h("div", { class: "row" }, to, job, h("button", { class: "alt", onclick: () => refresh(() => post(id, "hazard-refer", { index: i, to: to.value, job: job.value, evidence: evidence.value }), [to, job, evidence]) }, x.referred ? "Bind legacy referral prospectively" : "Record referral sent")),
      receiver && !x.received_at && h("button", { class: "alt", onclick: () => action("hazard-receive") }, "Record separate receipt evidence"),
      receiver && x.received_at && !x.accepted_at && h("button", { class: "alt", onclick: () => action("hazard-accept") }, "Record separate acceptance evidence"),
      receiver && x.accepted_at && h("div", {},
        times.map(([key, input]) => h("label", {}, timingLabels[key], input)),
        times.length > 0 && h("button", { class: "alt", onclick: () => refresh(() => post(id, "hazard-times", {
          index: i, evidence: evidence.value, ...Object.fromEntries(times.map(([key, input]) => [key, iso(input.value)]))
        }), [evidence, ...times.map(([, input]) => input)]) }, "Record externally supplied times"),
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
      }), [cat, pri, note, source, aware]) }, "Raise safety issue"))));
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
  const kind = h("select", { name: "kind", "aria-label": "Type of document" }, kinds.map((k) => h("option", {}, k)));
  const file = h("input", { name: "document", type: "file", required: true, "aria-label": "Choose a file", accept: ".pdf,.png,.jpg,.jpeg,.docx,.xlsx,.csv,.txt" });
  const out = caseSession?.id === id ? caseSession.documentBox : h("div", { role: "status" });
  const upload = async (metadata, submitted) => {
    const f = submitted.find(({ field }) => field.type === "file")?.field.files[0];
    const documentKind = kind.value;
    if (!f) throw new Error("Choose a file first.");
    const data = await new Promise((resolve, reject) => {
      const rd = new FileReader();
      rd.onload = () => resolve(String(rd.result).split(",")[1]);
      rd.onerror = () => reject(new Error("The file could not be read. Choose the file again."));
      rd.readAsDataURL(f);
    });
    return refresh(() => api(`/api/cases/${encodeURIComponent(id)}/upload`, { ...metadata, name: f.name, kind: documentKind, data }), submitted);
  };
  const read = async (d) => {
    if (!confirmCaseDraftReplacement(out)) return;
    out.replaceChildren(h("p", { class: "muted" }, "Reading..."));
    app.dispatchEvent(new Event("ai-review-change"));
    try {
      const r = await api(`/api/cases/${encodeURIComponent(id)}/read-doc`, modeBody({ id: d.id }));
      const text = h("p", { class: "pre", "data-document-text": "" }, r.text);
      if (!confirmCaseDraftReplacement(out)) return;
      out.replaceChildren(h("p", { class: "muted" }, r.source === "ai" ? "AI-read, please check:" : "Note:"), text,
        aiNotes(r, (action, replacement) => {
          if (action === "edit") {
            text.textContent = replacement;
            text.setAttribute("aria-label", "Reviewed replacement document text");
          }
        }));
      app.dispatchEvent(new Event("ai-review-change"));
    } catch (e) {
      const error = h("p", { class: "err", role: "alert" }, e.message);
      if (out.querySelector('[data-case-dirty="true"]')) out.append(error);
      else out.replaceChildren(error);
    }
  };
  return h("section", { class: "card" }, h("h2", {}, "Documents"),
    h("p", {}, c.checklist.map((x) => h("span", { class: `flag${x.present ? "" : " danger"}` }, `${x.present ? "Have" : "Need"}: ${x.kind}`))),
    c.documents.length ? h("ul", { class: "list" }, c.documents.map((d) => h("li", { class: "row between" },
      h("span", {}, h("a", { href: `/api/docs/${encodeURIComponent(id)}/${d.id}` }, d.name), ` ${d.kind}, ${fmtDate(d.at)}, ${d.by}`,
        h("span", { class: "muted" }, ` Source: ${d.source || "Unknown (legacy)"}; source version: ${d.source_version || "Unknown (legacy)"}; reason: ${d.reason || "Unknown (legacy)"}.`)),
      !d.generated && h("button", { class: "alt", onclick: () => read(d) }, "Read with AI")))) : h("p", {}, "No documents yet."),
    recordedChangeForm("doc-upload", "Add document", [h("div", { class: "row" }, kind, file)], upload), out);
}

const fundingAi = {};
function fundingPanel(c, id, refresh, savedFields = [], session = caseSession) {
  const f = c.funding;
  const canAct = ["Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role);
  const ta = h("textarea", { name: "funding-draft", autocomplete: "off", "aria-label": "Funding application draft", rows: 10 });
  const identity = fundingAi[id]?.record_id || "manual";
  ta.dataset.caseFieldKey = JSON.stringify(["funding", identity]);
  ta.caseBinding = { kind: "funding", id: identity };
  ta.value = f.draft || "";
  const fundNote = h("div", {}, fundingAi[id] ? [h("p", { class: "muted" }, fundingAi[id].label), aiNotes(fundingAi[id], null, () => ta.value)] : null);
  const ref = h("input", { "aria-label": "Application event evidence reference", name: "application-evidence", autocomplete: "off", spellcheck: "false" });
  const step = (action, text) => refresh(() => api(`/api/cases/${encodeURIComponent(id)}/funding`, { action, text }), [action === "save_draft" ? ta : ref]);
  if (f.status === "Confirmed") {
    const panel = h("section", { class: "card" }, h("h2", {}, "Funding application"), h("p", {}, `Application confirmation recorded. Route: ${f.route}${f.reference ? `, reference ${f.reference}` : ""}.`),
      h("p", { class: "muted" }, "Application status is not a grant award or cash receipt. See the separate grant evidence."));
    restoreBoundFields(savedFields, panel, "funding", session);
    return panel;
  }
  const need = c.checklist.filter((x) => !x.present).map((x) => x.kind);
  const panel = h("section", { class: "card" }, h("h2", {}, "Funding application"),
    h("p", {}, `Route: ${f.route}. Status: ${f.status}.${need.length ? ` Still needed: ${need.join(", ")}.` : " All evidence is in."}`),
    h("p", { class: "muted" }, "AI drafts the wording. A person approves it and submits it to the funder. The system never submits."),
    h("div", { class: "row" }, h("button", { onclick: () => refresh(async () => { fundingAi[id] = (await api(`/api/cases/${encodeURIComponent(id)}/funding-draft`, modeBody({}))).ai; }) }, "Draft application with AI")),
    fundNote,
    ta,
    canAct ? h("div", { class: "row" },
      h("button", { class: "alt", onclick: () => step("save_draft", ta.value) }, "Save my changes"),
      ["Draft ready", "Approved", "Submitted"].includes(f.status) && h("label", {}, "Application event evidence reference", ref),
      f.status === "Draft ready" && h("button", { onclick: () => step("approve", ref.value) }, `Approve as ${me.user.name}`),
      f.status === "Approved" && h("button", { onclick: () => step("submit", ref.value) }, "Record that I submitted it"),
      f.status === "Submitted" && h("button", { onclick: () => step("confirm", ref.value) }, "Record application confirmation"))
      : h("p", { class: "muted" }, "Only a designated human financial authority can approve or record submission and confirmation."),
    f.approved_by && h("p", { class: "muted" }, `Approved by ${f.approved_by}.`));
  restoreBoundFields(savedFields, panel, "funding", session);
  return panel;
}

function importView() {
  const out = h("div", {});
  const file = h("input", { type: "file", accept: ".csv,text/csv", id: "f" });
  file.addEventListener("change", AsyncAction.handler(async () => {
    if (!file.files.length) return;
    try {
      const text = await file.files[0].text();
      const r = await api("/api/import-check", { text });
      out.replaceChildren(
        h("p", { class: "notice" }, r.message),
        h("p", {}, `${r.ready} rows are ready to bring in. ${r.matched_existing} match a home we already have a record for.`),
        h("p", {}, "We found these columns: ", Object.entries(r.columns).map(([k, v]) => `${k}: ${v || "not found"}`).join("; ")),
        r.to_fix.length ? h("div", {}, h("h2", {}, "Rows to fix"), h("ul", {}, r.to_fix.map((x) => h("li", {}, `Row ${x.row}: ${x.problem}`)))) : h("p", {}, "No rows need fixing."));
    } catch (e) { out.replaceChildren(h("p", { class: "err" }, e.message)); }
  }));
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
async function bootstrapWorkspace() {
  await requireWorkspaceScripts("", false);
  workspaceStatus.textContent = "";
  document.getElementById("signout").addEventListener("click", AsyncAction.handler(() => signOut(false)));
  document.getElementById("switch-account").addEventListener("click", AsyncAction.handler(() => signOut(true)));
  await start();
}
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
function startupFailed(error) {
  if (error.status === 401) return;
  workspaceStatus.textContent = `Workspace unavailable: ${error.message}`;
  show(h("h1", {}, "Workspace unavailable"),
    h("p", { class: "err", role: "alert" }, `Could not start the workspace: ${error.message}. Try again. If this continues, contact application support.`),
    error.reloadWorkspace
      ? h("button", { type: "button", onclick: () => location.reload() }, "Reload workspace")
      : h("button", { type: "button", onclick: () => start().catch(startupFailed) }, "Try again"));
  workspaceReady();
}
bootstrapWorkspace().catch(startupFailed);

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

function mapPanel(coordinator = null) {
  disposeMapPanel?.();
  const signal = routeController.signal;
  const el = h("div", { id: "leaflet", class: "leafmap", role: "region", tabindex: "0", "aria-label": "Map of open cases. Zoom with the buttons, mouse wheel or pinch." });
  const info = h("p", { class: "muted", role: "status", "aria-live": "polite" });
  const open = coordinator
    ? h("button", { type: "button", class: "alt", onclick: () => {
      collapse(false);
      document.getElementById("coordinator-records").focus();
    } }, "Show these as a list")
    : h("a", { href: "#/all" }, "Show these as a list");
  let map = null, layer = null;
  let selectedId = null;
  const markers = new Map();
  const title = h("h3", { id: "map-home-title", tabindex: "-1" });
  const address = h("p");
  const caseId = h("dd");
  const stage = h("dd");
  const status = h("dd");
  const navigate = h("a", { class: "btn" }, "Open home");
  const restoreMarker = (id) => {
    const target = markers.get(id)?.getElement();
    (target?.isConnected ? target : el).focus({ preventScroll: true });
  };
  const closeHome = (restore = true) => {
    if (selectedId === null) return;
    const id = selectedId;
    selectedId = null;
    homeCard.hidden = true;
    if (restore) restoreMarker(id);
  };
  const homeCard = h("section", { class: "map-home-card", hidden: true, "aria-labelledby": "map-home-title" },
    h("div", { class: "map-home-header" }, title,
      h("button", { type: "button", class: "alt map-home-close", "aria-label": "Close home summary",
        onclick: () => closeHome() }, h("span", { "aria-hidden": "true" }, "\u00d7"))),
    address, h("dl", {}, h("dt", {}, "Case"), caseId, h("dt", {}, "Current stage"), stage,
      h("dt", {}, "Map status"), status), navigate);
  const showHome = (point, focus = true) => {
    selectedId = point.id;
    title.textContent = point.name || point.id;
    address.textContent = point.address || "Address not included in this map. Open home for permitted details.";
    caseId.textContent = point.id;
    stage.textContent = point.stage || "Unknown";
    status.replaceChildren(mapSymbol(point.kind), MAP_SIGNALS[point.kind].label);
    navigate.href = `#/case/${encodeURIComponent(point.id)}`;
    homeCard.hidden = false;
    if (focus) title.focus();
  };
  const listHead = h("summary", { id: "maplist-h" }, "Show the map areas as a list (keyboard and screen reader friendly)");
  const listUl = h("ul", { "aria-labelledby": "maplist-h", class: "plainlist" });
  const listBox = h("details", { class: "maplist" }, listHead, listUl);
  const sidebar = h("aside", { class: "map-info", "aria-label": "Map information and home summary" },
    h("p", {}, "Select a home for a summary, then choose Open home. Escape closes the summary first."),
    h("p", {}, Object.entries(MAP_SIGNALS).map(([kind, signal]) => h("span", { class: `key ${kind}` }, mapSymbol(kind), signal.label))),
    info, listBox, open);
  const mapStage = h("div", { class: "map-stage" }, el, homeCard);
  const dialog = h("dialog", { class: "map-dialog", "aria-labelledby": "map-title",
    oncancel: (event) => { event.preventDefault(); collapse(); } });
  const toggle = h("button", { type: "button", class: "alt", "aria-expanded": "false",
    onclick: () => dialog.open ? collapse() : expand() }, "Expand map");
  const box = h("section", { class: "card map-panel", onkeydown: (event) => {
    if (event.key === "Escape" && selectedId !== null) {
      event.preventDefault();
      event.stopPropagation();
      closeHome();
    }
  } }, h("div", { class: "row between" }, h("h2", { id: "map-title" }, "Map of open cases"), toggle),
  h("div", { class: "map-workspace" }, sidebar, mapStage));
  const slot = h("div", { class: "map-slot" }, box);
  const resize = () => map?.invalidateSize({ pan: false, animate: false });
  function expand() {
    if (slot.inert) return;
    sidebar.prepend(homeCard);
    dialog.append(box);
    document.body.append(dialog);
    document.body.classList.add("map-expanded");
    toggle.textContent = "Exit expanded map";
    toggle.setAttribute("aria-expanded", "true");
    dialog.showModal();
    resize();
    toggle.focus({ preventScroll: true });
  }
  function collapse(restore = true) {
    if (!dialog.open) return;
    dialog.close();
    slot.append(box);
    mapStage.append(homeCard);
    dialog.remove();
    document.body.classList.remove("map-expanded");
    toggle.textContent = "Expand map";
    toggle.setAttribute("aria-expanded", "false");
    resize();
    if (restore) toggle.focus({ preventScroll: true });
  }
  const dispose = () => {
    slot.inert = true;
    toggle.disabled = true;
    collapse(false);
    seq++;
    dialog.remove();
    slot.remove();
    map?.remove();
    map = null;
    if (disposeMapPanel === dispose) disposeMapPanel = null;
    signal.removeEventListener("abort", dispose);
  };
  disposeMapPanel = dispose;
  signal.addEventListener("abort", dispose, { once: true });
  const renderList = (d) => {
    listUl.replaceChildren(...d.items.map((p) => {
      if (d.mode === "clusters") {
        const label = `${p.count} homes, ${p.hazards} with a safety issue open`;
        return h("li", {}, h("button", { type: "button", class: "linkbtn", "aria-label": `${label}. Zoom in to this area`,
          onclick: () => { map.setView([p.lat, p.lon], Math.min(map.getZoom() + 2, 18), { animate: false }); listHead.focus(); } }, label));
      }
      return h("li", {}, h("a", { href: `#/case/${encodeURIComponent(p.id)}` }, `${p.name}, ${MAP_SIGNALS[p.kind].label}`));
    }));
  };
  let fitting = false, seq = 0;
  const draw = async (fit) => {
    if (signal.aborted) return;
    const my = ++seq;
    info.setAttribute("role", "status");
    info.textContent = "Loading map records. The case list remains available.";
    el.setAttribute("aria-busy", "true");
    const progress = AsyncAction.feedback("Loading map records", null, box);
    if (!coordinator) open.onclick = () => {
      collapse(false);
      Object.assign(listState, { flag: ovState.flag === "fundingprog" ? "funding" : ovState.flag, area: ovState.area });
    };
    if (!map) {
      map = L.map(el, { scrollWheelZoom: true, keyboard: false, inertia: false,
        zoomAnimation: false, fadeAnimation: false, markerZoomAnimation: false }).setView([54.9, -1.6], 9);
      el.addEventListener("keydown", (event) => {
        if (event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey
          || event.target.closest(".leaflet-control")) return;
        const offsets = { ArrowLeft: [-80, 0], ArrowRight: [80, 0], ArrowUp: [0, -80], ArrowDown: [0, 80] };
        if (offsets[event.key]) map.panBy(offsets[event.key], { animate: false });
        else if (["+", "=", "-"].includes(event.key)) {
          map.setZoom(map.getZoom() + (event.key === "-" ? -1 : 1), { animate: false });
        } else return;
        event.preventDefault();
      });
      if (me.map && me.map.tiles) {
        L.tileLayer(me.map.tiles, { maxZoom: 19, referrerPolicy: "strict-origin-when-cross-origin", attribution: me.map.attribution || "" }).addTo(map);
      }
      layer = L.layerGroup().addTo(map);
      map.on("moveend", () => { if (!fitting) draw(false); });
      map.on("click", () => closeHome());
    }
    const b = map.getBounds();
    const view = fit ? "" : `&bbox=${[b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].join(",")}`;
    let d;
    try {
      const response = await api(coordinator
        ? `/api/coordinator?${qs(coordinator.state)}&zoom=${map.getZoom()}${view}`
        : `/api/map?${qs(ovState)}&zoom=${map.getZoom()}${view}`, undefined, signal);
      d = coordinator ? response.map : response;
    }
    catch (error) {
      if (signal.aborted || my !== seq || !me) return;
      const restore = homeCard.contains(document.activeElement) || el.contains(document.activeElement);
      markers.clear();
      layer.clearLayers();
      closeHome(false);
      if (restore) el.focus({ preventScroll: true });
      listUl.replaceChildren();
      info.setAttribute("role", "alert");
      info.textContent = `Map unavailable: ${error.message}. Use the case list or try changing the map filter.`;
      return;
    } finally {
      progress.finish();
      if (my === seq) el.removeAttribute("aria-busy");
    }
    if (signal.aborted || my !== seq) return;
    info.setAttribute("role", "status");
    info.textContent = coordinator
      ? `${d.total} permitted records in this selection; ${d.mapped} with coordinates; ${d.missing_geocode} with unknown or invalid coordinates. ${d.in_view} mapped records in this viewport, ${d.shown} ${d.mode === "clusters" ? "clusters" : "markers"}. The record list includes every selected case.`
      : d.mode === "clusters"
      ? `${d.total} homes in this view, grouped into ${d.shown} areas. Zoom in to see each home.`
      : `${d.total} ${d.total === 1 ? "home" : "homes"} shown`;
    renderList(d);
    const focusedMarker = [...markers].find(([, marker]) => marker.getElement() === document.activeElement)?.[0];
    const cardFocused = homeCard.contains(document.activeElement);
    const previousSelection = selectedId;
    markers.clear();
    layer.clearLayers();
    d.items.forEach((p) => {
      if (d.mode === "clusters") {
        const label = `${p.count} homes, ${p.hazards} with a safety issue open. Zoom in to this area`;
        const icon = h("div", { class: `cluster${p.hazards ? " hazard" : ""}`, "aria-hidden": "true" },
          h("span", {}, `${p.count} homes`),
          h("span", { class: "cluster-safety" }, `Safety: ${p.hazards}`));
        const m = L.marker([p.lat, p.lon], { icon: L.divIcon({ className: "map-cluster", html: icon, iconSize: [104, 50] }),
          keyboard: true, autoPanOnFocus: false, title: label, alt: label });
        mapAction(m, () => map.setView([p.lat, p.lon], Math.min(map.getZoom() + 2, 18), { animate: false }));
        m.addTo(layer);
        return;
      }
      const label = `${p.name}, ${MAP_SIGNALS[p.kind].label}`;
      const m = L.marker([p.lat, p.lon], { icon: L.divIcon({ className: "map-marker", html: mapSymbol(p.kind), iconSize: [28, 28] }),
        keyboard: true, autoPanOnFocus: false, bubblingMouseEvents: false, title: label, alt: label });
      mapAction(m, () => showHome(p));
      m.addTo(layer);
      markers.set(p.id, m);
    });
    const current = d.mode === "points" && d.items.find((point) => point.id === previousSelection);
    if (current) showHome(current, false);
    else closeHome(false);
    if (cardFocused && !current) el.focus({ preventScroll: true });
    else if (focusedMarker) restoreMarker(focusedMarker);
    if (fit && d.bounds) {
      fitting = true;
      map.fitBounds([[d.bounds[0], d.bounds[1]], [d.bounds[2], d.bounds[3]]], { padding: [30, 30], maxZoom: 15, animate: false });
      fitting = false;
      draw(false);
    }
  };
  return { box: slot, draw, size: resize };
}

async function coordinatorView() {
  const signal = routeController.signal;
  const supplied = Object.fromEntries(new URLSearchParams(location.hash.split("?")[1] || ""));
  const state = { view: "all", as_of: new Date().toISOString(), ...supplied };
  // Map requests own their viewport; URL selection owns only the cohort and drill.
  delete state.zoom;
  delete state.bbox;
  const href = (changes = {}) => `#/coordinator?${qs({ ...state, offset: "", ...changes })}`;
  const status = h("p", { role: "status", "aria-live": "polite" }, "Loading coordinator counts...");
  show(h("h1", {}, "Coordinator flow"), status);
  const [data, fx] = await Promise.all([
    api(`/api/coordinator?${qs(state)}`, undefined, signal), api("/api/facets", undefined, signal),
  ]);
  if (signal.aborted) return;
  coordinatorOrigin = href({ offset: state.offset });
  queueOrigin = state.view;
  const number = (n) => n === null ? "Unknown" : new Intl.NumberFormat("en-GB").format(n);
  const values = {};
  const field = (label, key, options) => {
    const input = h("select", { id: `co-${key}`, name: key, autocomplete: "off" },
      h("option", { value: "" }, "Any"), options.map(([value, text]) => h("option", { value }, text)));
    input.value = state[key] || "";
    values[key] = input;
    return h("div", {}, h("label", { for: `co-${key}` }, label), input);
  };
  const textField = (label, key, required = false) => {
    const input = h("input", { id: `co-${key}`, name: key, autocomplete: "off",
      type: key === "q" ? "search" : "text", required, spellcheck: "false" });
    input.value = state[key] || "";
    values[key] = input;
    return h("div", {}, h("label", { for: `co-${key}` }, label), input);
  };
  const error = h("p", { class: "err", role: "alert" });
  const form = h("form", { class: "card coordinator-filters", onsubmit: (event) => {
    event.preventDefault();
    const next = Object.fromEntries(Object.entries(values).map(([key, input]) => [key, input.value.trim()]));
    if (!next.view || !next.group_by) {
      error.textContent = "Choose the case scope and heatmap grouping.";
      (!next.view ? values.view : values.group_by).focus();
      return;
    }
    location.hash = `#/coordinator?${qs(next)}`;
  } },
  h("h2", {}, "Choose the current case population"),
  h("div", { class: "row" },
    field("Case scope", "view", [["mine", "My assigned open cases"], ["all", "All permitted open cases"]]),
    field("Heatmap grouping", "group_by", [["area", "Local authority"], ["building", "Recorded building"], ["archetype", "Recorded home type"]]),
    field("Current stage", "stage", fx.stages.map((x) => [x, x])),
    field("Local authority", "area", fx.areas.map((x) => [x, x])),
    field("Wave", "wave", fx.waves.map((x) => [x, x])),
    field("Owner", "owner", me.staff.map((x) => [x.code, x.name])),
    field("Contractor", "contractor", fx.contractors.map((x) => [x, x])),
    field("Work queue", "queue", me.work_queues.definitions.map((x) => [x.id, x.label])),
    field("Show only", "flag", [...FLAGS, ["fundingprog", "Funding application in progress"]]),
    textField("Find by name, address, postcode or case ID", "q"),
    textField("Event cutoff (ISO date, time and timezone)", "as_of", true),
    textField("Event period start (optional ISO timestamp)", "start")),
  h("p", {}, "Dates select recorded events only. Current case membership, stages and stopped work are not reconstructed at the cutoff."),
  h("button", { type: "submit" }, "Apply coordinator filters"),
  h("a", { class: "btn alt", href: "#/coordinator" }, "Reset coordinator filters"), error);
  values.group_by.value = state.group_by || "area";
  const link = (n, changes, label) => h("a", {
    href: href(changes), "aria-label": `${number(n)} ${label}`,
  }, number(n));
  const table = (title, headers, rows) => h("section", { class: "card" },
    h("h2", {}, title), h("div", { class: "table-scroll", tabindex: "0", role: "region", "aria-label": title },
      h("table", {}, h("caption", { class: "muted" }, title),
        h("thead", {}, h("tr", {}, headers.map((x) => h("th", { scope: "col" }, x)))),
        h("tbody", {}, rows.length ? rows : h("tr", {}, h("td", { colspan: headers.length }, "No cases match this population. Change or reset the filters."))))));
  const summary = h("section", { class: "card coordinator-summary", "aria-label": "Coordinator denominator and coverage" },
    h("h2", {}, "Denominator and coverage"),
    h("p", {}, `${number(data.cohort.selected_cases)} current cases selected from ${number(data.cohort.baseline_cases)} permitted open cases in this scope. `,
      link(data.cohort.excluded_by_filters, { metric: "filtered_out", metric_stage: "", group: "" }, "cases excluded by source filters"), " excluded by filters, not lifecycle exclusion."),
    h("p", {}, link(data.counts.stopped, { metric: "stopped", metric_stage: "", group: "" }, "currently stopped cases"), " currently cannot move on. ",
      `Priority policy ${data.priority.version}: ${data.priority.status}. `,
      data.priority.approved ? `${number(data.priority.count)} cases under approved priority.` : "Approved priority is Unknown, not zero. The current rule order is not an approval."),
    h("p", {}, `${number(data.coverage.stage_history_partial)} cases with partial observed stage evidence; `,
      link(data.coverage.stage_history_unknown, { metric: "unknown_history", metric_stage: "", group: "" }, "cases with unknown stage history"),
      " without trusted stage events in this period. Complete historical coverage: 0. ",
      link(data.coverage.missing_geocode, { metric: "missing_geocode", metric_stage: "", group: "" }, "cases with unknown or invalid coordinates"),
      " with unknown or invalid coordinates remain in the population."),
    h("p", {}, `Lifecycle exclusions: Unknown. True conversion: Unknown. Audit evidence: ${data.audit_integrity}. ${data.approval_status}.`),
    h("p", {}, `Current dataset date: ${data.current_as_of}. Event window: ${data.period_start || "all recorded history"} to ${data.as_of}, inclusive UTC.`));
  const heatmap = table("Heatmap of current cases",
    ["Recorded group", "Current stage", "Cases / denominator", "Cannot move on", "Unknown coordinates", "Unknown stage history"],
    data.heatmap.map((cell) => h("tr", {},
      h("th", { scope: "row" }, cell.group), h("td", {}, cell.stage),
      h("td", { class: `heat-count${cell.count ? " heat-present" : ""}` },
        link(cell.count, { metric: "current", metric_stage: cell.stage, group: cell.group }, `current cases in ${cell.group}, ${cell.stage}`),
        ` / ${number(cell.denominator)}`),
      h("td", {}, number(cell.stopped)), h("td", {}, number(cell.missing_geocode)), h("td", {}, number(cell.unknown_history)))));
  const metrics = [["current", "Current"], ["entries", "Observed entries"], ["exits", "Observed exits"],
    ["returns", "Observed returns"], ["reopens", "Observed reopens"], ["stopped", "Currently stopped"]];
  const funnel = table("Lifecycle funnel: current and observed cases",
    ["Stage", ...metrics.map(([, label]) => label), "Denominator", "Lifecycle exclusions", "True conversion"],
    data.funnel.map((row) => h("tr", {}, h("th", { scope: "row" }, row.stage),
      metrics.map(([key, label]) => h("td", {}, row[key] === null ? "Unknown" :
        link(row[key], { metric: key, metric_stage: row.stage, group: "" }, `${label.toLowerCase()} for ${row.stage}`))),
      h("td", {}, number(row.denominator)), h("td", {}, "Unknown"), h("td", {}, "Unknown"))));
  const records = table("Selected records", ["Case", "Current stage", "Address", "Coordinates", "Can move on"],
    data.records.items.map((row) => h("tr", {}, h("th", { scope: "row" },
      h("a", { href: `#/case/${encodeURIComponent(row.id)}` }, row.id)),
      h("td", {}, row.stage), h("td", {}, `${row.address}, ${row.postcode}`),
      h("td", {}, row.geocode), h("td", {}, row.stopped ? "Cannot move on" : "No current stop recorded"))));
  records.querySelector(".table-scroll").id = "coordinator-records";
  const paging = h("p", { class: "row" },
    Number(state.offset || 0) > 0 && h("a", { class: "btn alt", href: href({ offset: Math.max(0, data.records.offset - data.records.limit) }) }, "Previous records"),
    data.records.offset + data.records.limit < data.records.total && h("a", { class: "btn alt", href: href({ offset: data.records.offset + data.records.limit }) }, "Next records"));
  const mp = mapPanel({ state });
  workspaceStatus.textContent = `${me.user.role}. Coordinator current cohort ${data.cohort.selected_cases}; selected records ${data.records.total}. Filters do not change access.`;
  show(h("div", { class: "coordinator" },
    h("div", { class: "row between" }, h("h1", {}, "Coordinator flow"), h("a", { href: "#/overview" }, "Back to overview")),
    form, summary,
    h("details", {}, h("summary", {}, "Count definitions and limits"),
      h("dl", {}, Object.entries(data.definitions).flatMap(([key, value]) => [h("dt", {}, key.replaceAll("_", " ")), h("dd", {}, value)]))),
    heatmap, h("p", {}, "Observed counts are distinct cases, not event occurrences. A case may appear in several stages. Rows do not form an additive conversion rate. Initial entries, final exits and older history may be unknown."),
    funnel, h("section", { class: "card", role: "status" },
      h("h2", {}, "Record selection"),
      h("p", {}, `${number(data.records.total)} selected records; ${data.selection.metric.replaceAll("_", " ")}${data.selection.metric_stage ? ` for ${data.selection.metric_stage}` : ""}${data.selection.group ? ` in ${data.selection.group}` : ""}. Cohort denominator: ${number(data.cohort.selected_cases)}.`),
      h("a", { href: href({ metric: "current", metric_stage: "", group: "" }) }, "Show the full filtered population")),
    mp.box, records, paging));
  mp.size();
  await mp.draw(true);
}

async function overviewView() {
  const st = await api("/api/stats");
  const k = st.kpis;
  const counts = { "": k.open, hazard: k.hazards, long: k.long, nodecision: k.nodecision, fundingprog: k.funding, support: k.support };
  const mp = mapPanel();
  const tiles = h("div", { class: "tiles", role: "group", "aria-label": "Choose what the map shows" });
  const paint = () => tiles.replaceChildren(...OV_TILES.map(([f, label]) => h("button", { class: `tile${f === "hazard" ? " danger" : ""}`, "aria-pressed": String(ovState.flag === f),
    onclick: () => { ovState.flag = f; paint(); return mp.draw(true); } }, h("strong", {}, String(counts[f])), h("span", {}, label),
    h("span", { class: "tile-selection" }, ovState.flag === f ? "Selected" : "Select filter"))),
    h("div", { class: "tile static" }, h("strong", {}, String(k.completed)), h("span", {}, "Completed")));
  paint();
  const area = h("select", { id: "mapArea", onchange: (e) => { ovState.area = e.target.value; return mp.draw(true); } },
    h("option", { value: "" }, "All areas"), st.areas.map((a) => h("option", { value: a.label }, a.label)));
  area.value = ovState.area;
  show(
    h("h1", {}, "Overview"), h("p", {}, h("a", { class: "btn alt", href: "#/coordinator" }, "Coordinator heatmap and lifecycle funnel")), tiles,
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
