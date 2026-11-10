"use strict";
// Synthetic staff-assisted aftercare screens (issue 133). Stage A builders and submission are
// unchanged; the workspace route at the end connects them to the signed-in session.
// Shares h and api with app.js. Every function renders a returned contract or posts to it; nothing
// here reads browser storage, calls a model or decides anything on the server's behalf.
const AFTERCARE_API = "/api/aftercare";

const AFTERCARE_LABELS = {
  household: "Someone who lives in the home",
  representative: "A person acting for the household",
  discomfort: "Too cold, too warm or damp",
  higher_bill: "Energy bill higher than expected",
  control_use: "Not sure how to use the controls",
  other: "Something else",
  not_assessed: "Not assessed yet",
  open: "Open",
  in_progress: "In progress",
  completed: "Completed",
  not_needed: "Not needed",
  received: "Received",
  under_investigation: "Under investigation",
  outcome_recorded: "Outcome recorded",
  no_outcome_yet: "No outcome yet",
  remedy_needed: "Remedy needed",
  no_remedy_needed: "No remedy needed",
  advice_given: "Advice given",
  cannot_determine: "Cannot determine",
  handover: "Handover",
  financial: "Payment",
};

function acLabel(value) {
  return AFTERCARE_LABELS[value] || String(value ?? "Unknown");
}

function acText(value) {
  return value === null || value === undefined || value === "" ? "Unknown" : String(value);
}

function acNumber(value, digits = 1) {
  return typeof value === "number" && Number.isFinite(value)
    ? new Intl.NumberFormat("en-GB", { maximumFractionDigits: digits }).format(value)
    : "Unknown";
}

const AC_TABLE_CAPTION = "Observed baseline and late means, with concerns by home";

function acFraction(value) {
  const ok = (n) => typeof n === "number" && Number.isInteger(n) && n >= 0;
  if (!value || typeof value !== "object" || !ok(value.count) || !ok(value.denominator) || value.count > value.denominator) {
    return "Unresolved concerns: Unknown";
  }
  const base = `${value.count} of ${value.denominator} concerns unresolved.`;
  return value.denominator === 0 ? `${base} No proportion is stated.` : base;
}

function acOwner(owner) {
  if (!owner || owner.status === "unknown") return "Unknown. No owner is named yet.";
  return `${acText(owner.label)}`;
}

function acNotice(form) {
  return h("p", { class: "notice" }, acText(form.synthetic_notice));
}

function acField(spec, value, error) {
  const id = `ac-${spec.name}`;
  const errId = `${id}-error`;
  const common = {
    id,
    name: spec.name,
    autocomplete: "off",
    spellcheck: "false",
    "aria-describedby": error ? errId : undefined,
    "aria-invalid": error ? "true" : undefined,
  };
  let control;
  if (spec.options) {
    control = h("select", { ...common, required: spec.required ? "" : undefined },
      h("option", { value: "" }, "Choose one…"),
      ...spec.options.map((o) => h("option", { value: o.value, selected: o.value === value ? "" : undefined }, o.label)));
  } else if (spec.name === "statement" || spec.name === "representative_basis") {
    control = h("textarea", { ...common, rows: "4" }, value || "");
  } else if (spec.name === "next_update") {
    control = h("input", { ...common, type: "date", value: value || "" });
  } else {
    control = h("input", { ...common, type: "text", value: value || "" });
  }
  return h("div", { class: "field" },
    h("label", { for: id }, spec.required ? `${spec.label} (required)` : spec.label),
    control,
    error ? h("p", { id: errId, class: "field-error" }, `Problem: ${error}`) : false);
}

function aftercareFormView(form, state = {}) {
  const errors = state.errors || {};
  const values = state.values || {};
  const specs = [...(form.fields || []), ...(form.staff_fields || [])]
    .filter((s) => s.name !== "representative_basis" || values.raised_by === "representative");
  const entries = Object.entries(errors);
  const summary = entries.length
    ? h("div", { id: "ac-error-summary", role: "alert", tabindex: "-1", class: "error-summary" },
      h("h2", {}, "Some details need fixing"),
      h("ul", {}, ...entries.map(([name, text]) => h("li", {}, h("a", { href: `#ac-${name}` }, text)))))
    : false;
  return h("section", { "aria-labelledby": "ac-title" },
    h("h1", { id: "ac-title", tabindex: "-1" }, acText(form.title)),
    acNotice(form),
    h("p", {}, acText(form.intro)),
    h("p", {}, acText(form.owner_note)),
    summary,
    h("form", { id: "ac-form", novalidate: "", "data-request-id": state.requestId || "" },
      ...specs.map((s) => acField(s, values[s.name], errors[s.name])),
      h("button", { type: "submit" }, state.sending ? "Saving…" : "Record concern")),
    h("p", { role: "status", id: "ac-status" }, state.message || ""),
    h("p", {}, acText(form.manual_route)),
    h("p", {}, acText(form.protection)));
}

function aftercareReceiptView(receipt, replay = false) {
  const owner = receipt.owner || {};
  const rows = [
    ["Receipt", acText(receipt.receipt_id)],
    ["Concern", acText(receipt.concern_id)],
    ["Received", acText(receipt.received_at)],
    ["Recorded by", `${acText(receipt.recorded_by && receipt.recorded_by.name)} (${acText(receipt.recorded_by && receipt.recorded_by.role)})`],
    ["How it was raised", acLabel(receipt.channel)],
    ["Raised by", acLabel(receipt.raised_by)],
    ["Home reference", acText(receipt.home_ref)],
    ["Topic", acLabel(receipt.kind)],
    ["Original statement", acText(receipt.original && receipt.original.statement)],
    ["Authority given", acText(receipt.original && receipt.original.representative_basis)],
    ["Owner", owner.status === "unknown" ? acOwner(owner) : `${acText(owner.label)}`],
    ["Next update", acText(receipt.next_update)],
  ];
  return h("section", { "aria-labelledby": "ac-receipt-title" },
    h("h1", { id: "ac-receipt-title", tabindex: "-1" }, replay ? "Concern already recorded" : "Concern recorded"),
    h("p", { role: "status" }, replay
      ? "This request was already saved. No second record was made."
      : "Saved. Keep this receipt reference."),
    h("dl", {}, rows.flatMap(([term, text]) => [h("dt", {}, term), h("dd", {}, text)])),
    h("p", {}, acText(receipt.what_happens_next)),
    h("p", {}, acText(receipt.accessible_route)),
    h("p", {}, acText(receipt.protection)),
    h("p", {}, acText(receipt.synthetic_notice)));
}

function aftercareConcernView(c) {
  const remedy = c.remedy || {};
  const outcome = c.outcome || null;
  const closures = c.closures || [];
  return h("section", { "aria-labelledby": `ac-${c.id}-title` },
    h("h2", { id: `ac-${c.id}-title` }, `${acText(c.id)}: ${acLabel(c.kind)}`),
    h("dl", {},
      h("dt", {}, "Status"),
      h("dd", {}, `${c.unresolved ? "Unresolved" : "Resolved"}${c.overdue ? ", update overdue" : ""}`),
      h("dt", {}, "Owner"), h("dd", {}, acOwner(c.owner)),
      h("dt", {}, "Investigation"), h("dd", {}, acLabel(c.investigation)),
      h("dt", {}, "Outcome"), h("dd", {}, outcome ? acLabel(outcome.outcome) : "No outcome yet"),
      h("dt", {}, "Remedy"), h("dd", {}, acLabel(remedy.status)),
      h("dt", {}, "Next update"), h("dd", {}, acText(c.next_update)),
      h("dt", {}, "Original statement"), h("dd", {}, acText(c.statement)),
      h("dt", {}, "Raised by"), h("dd", {}, `${acLabel(c.raised_by)} via ${acLabel(c.channel)}`)),
    closures.length
      ? h("p", {}, `Related handover or payment records (${closures.length}) are shown for context. ${acText(closures[0].note)}`)
      : false,
    h("p", {}, acText(c.sensor_note)));
}

function aftercareEvaluatorView(v) {
  const totals = v.totals || {};
  const usable = totals.homes_with_usable_comparison || {};
  const rows = (v.rows || []).map((row) => {
    const cmp = row.comparison || {};
    const ok = cmp.status === "sufficient";
    return h("tr", {},
      h("th", { scope: "row" }, acText(row.home_ref)),
      h("td", {}, ok ? "Comparison available" : "Unknown"),
      h("td", {}, ok ? `${acNumber(cmp.baseline.temperature_c)} °C` : "Unknown"),
      h("td", {}, ok ? `${acNumber(cmp.late.temperature_c)} °C` : "Unknown"),
      h("td", {}, String((row.concerns || []).length)),
      h("td", {}, String(row.unresolved_count ?? "Unknown")));
  });
  return h("section", { "aria-labelledby": "ac-eval-title" },
    h("h1", { id: "ac-eval-title", tabindex: "-1" }, "Aftercare view for a synthetic cohort"),
    h("p", {}, acText(v.synthetic_notice)),
    h("p", {}, acText(v.notice)),
    h("p", {}, `${acText(usable.count)} of ${acText(usable.denominator)} homes have a usable comparison. Concerns raised: ${acText(totals.concerns_raised)}.`),
    h("p", {}, acFraction(totals.concerns_unresolved)),
    rows.length
      ? h("div", { class: "table-scroll", role: "region", tabindex: "0", "aria-label": AC_TABLE_CAPTION },
        h("table", {},
        h("caption", {}, AC_TABLE_CAPTION),
        h("thead", {}, h("tr", {},
          ...["Home", "Comparison", "Baseline mean", "Late mean", "Concerns", "Unresolved"].map((t) => h("th", { scope: "col" }, t)))),
        h("tbody", {}, ...rows)))
      : h("p", {}, "No homes are in the synthetic cohort."),
    h("h2", {}, "What is not known"),
    h("ul", {}, ...(v.unknowns || []).map((u) => h("li", {}, acText(u)))),
    h("p", {}, acText(v.sensor_note)));
}

const AC_UNCONFIRMED = "Saving could not be confirmed. The concern may or may not have been saved. Do not start another record or use the paper route yet. Send again with the same details, which is safe because the same request reference is kept, or ask a colleague to check. Check the concerns list for a receipt first.";
const AC_EARLIER = "An earlier attempt may have been saved. Send the original details again without changes, or check the concerns list for a receipt, before starting another record or using the paper route.";

function acRefusal(error, unresolved) {
  const own = error.status === 403
    ? "Your role cannot do this. Ask a colleague who can, or use the paper route."
    : (error.message || "Some details need fixing.");
  return unresolved ? `${own} ${AC_EARLIER}` : own;
}

function acValidReceipt(receipt, requestId) {
  return Boolean(receipt) && typeof receipt === "object" && !Array.isArray(receipt)
    && typeof receipt.receipt_id === "string" && typeof receipt.concern_id === "string"
    && receipt.request_id === requestId;
}

function acUnconfirmed(outcome, message = AC_UNCONFIRMED) {
  return { ok: false, outcome, message, errors: {}, retainRequestId: true, unresolved: true };
}

// The shared api() copies data.errors onto the thrown error. The caller owns requestId and keeps it across retries; opts.unresolved says an earlier attempt is still unconfirmed.
async function aftercareSubmit(api, values, requestId, signal, opts = {}) {
  const earlier = Boolean(opts.unresolved);
  const body = { ...values, request_id: requestId };
  try {
    const reply = await api(`${AFTERCARE_API}/concerns`, body, signal);
    if (!reply || !acValidReceipt(reply.receipt, requestId)) return acUnconfirmed("unconfirmed");
    const replay = Boolean(reply.replayed);
    return { ok: true, outcome: replay ? "replayed" : "saved", receipt: reply.receipt, replay, unresolved: false };
  } catch (error) {
    if (error && error.name === "AbortError") throw error;
    const status = error && error.status;
    if (status === 400 || status === 403) {
      return {
        ok: false, outcome: "refused", message: acRefusal(error, earlier),
        errors: (error.errors && typeof error.errors === "object") ? error.errors : {},
        retainRequestId: earlier, unresolved: earlier,
      };
    }
    if (status === 401) return acUnconfirmed("unconfirmed", `Your session has ended. Sign in again. ${AC_UNCONFIRMED}`);
    if (status === 409) return acUnconfirmed("conflict");
    return acUnconfirmed("unconfirmed");
  }
}

// Draft and request reference live only in memory: they survive validation errors, failed saves,
// route changes and an ended session, and are dropped on sign-out or when another person signs in.
let acDraftState = null;

function acActor() {
  const user = typeof me === "object" && me && me.user;
  return user ? String(user.email || user.name || "") : "";
}

function acDraft() {
  const actor = acActor();
  if (!acDraftState || acDraftState.actor !== actor) {
    acDraftState = { actor, requestId: null, values: {}, unresolved: false, message: "" };
  }
  return acDraftState;
}

function acNewRequestId() {
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  return "req-" + Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

function acReadValues(form) {
  const values = {};
  for (const el of form.elements) if (el.name && typeof el.value === "string") values[el.name] = el.value;
  return values;
}

function acHomeChoices(form) {
  if (!Array.isArray(form.homes)) return form;
  const options = form.homes.map((home) => ({ value: home, label: home }));
  const fields = (form.fields || []).map((f) => (f.name === "home_ref" ? { ...f, options } : f));
  return { ...form, fields };
}

function acSecondaryHeading(section) {
  const first = section.querySelector("h1");
  if (first) {
    const heading = h("h2", { id: first.id, tabindex: "-1" }, first.textContent);
    first.replaceWith(heading);
  }
  return section;
}

function acFocus(node) {
  if (!node) return;
  node.tabIndex = -1;
  node.focus();
}

async function aftercareWorkspaceView() {
  const read = (path) => api(`${AFTERCARE_API}/${path}`);
  const [formResult, concerns, evaluator] = await Promise.all([
    read("form").catch((error) => (error.status === 403 ? null : Promise.reject(error))),
    read("concerns"),
    read("evaluator"),
  ]);
  const form = formResult && acHomeChoices(formResult);
  const draft = acDraft();
  let sending = false;
  const page = (extra = {}) => {
    const state = {
      values: draft.values, requestId: draft.requestId || "", sending, errors: extra.errors || {},
      message: extra.message || draft.message,
    };
    const parts = [];
    if (form) parts.push(aftercareFormView(form, state));
    else {
      parts.push(h("h1", { id: "ac-title", tabindex: "-1" }, "Aftercare concerns"),
        h("p", { class: "notice" }, acText(concerns.synthetic_notice)),
        h("p", { role: "status" }, "Your role can read these concerns but cannot record one. Ask a colleague who can."));
    }
    parts.push(h("section", { "aria-labelledby": "ac-list-title" },
      h("h2", { id: "ac-list-title" }, `Recorded concerns (${acText(concerns.count)})`),
      concerns.items.length
        ? concerns.items.map((c) => aftercareConcernView(c))
        : h("p", {}, "No concerns have been recorded yet.")));
    parts.push(acSecondaryHeading(aftercareEvaluatorView(evaluator)));
    show(...parts);
    wire();
    return state;
  };
  const showReceipt = (receipt, replay) => {
    const view = aftercareReceiptView(receipt, replay);
    show(view, h("p", {}, h("button", { type: "button", onclick: () => aftercareWorkspaceView() }, "Back to aftercare concerns")));
    acFocus(document.getElementById("ac-receipt-title"));
  };
  const wire = () => {
    const el = document.getElementById("ac-form");
    if (!el) return;
    el.addEventListener("input", () => { draft.values = acReadValues(el); });
    const raised = document.getElementById("ac-raised_by");
    if (raised) raised.addEventListener("change", () => { draft.values = acReadValues(el); page(); acFocus(document.getElementById("ac-raised_by")); });
    el.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (sending) return;
      draft.values = acReadValues(el);
      if (!draft.requestId) draft.requestId = acNewRequestId();
      sending = true;
      el.querySelector("button[type=submit]").disabled = true;
      let result;
      try {
        result = await aftercareSubmit(api, draft.values, draft.requestId, undefined, { unresolved: draft.unresolved });
      } catch (error) {
        if (error && error.name === "AbortError") { draft.unresolved = true; draft.message = AC_EARLIER; return; }
        throw error;
      } finally { sending = false; }
      draft.unresolved = Boolean(result.unresolved);
      if (result.ok) {
        acDraftState = null;
        return showReceipt(result.receipt, result.replay);
      }
      draft.message = result.message;
      page({ errors: result.errors, message: result.message });
      acFocus(Object.keys(result.errors).length ? document.getElementById("ac-error-summary") : document.getElementById("ac-status"));
    });
  };
  if (draft.unresolved && !draft.message) draft.message = AC_EARLIER;
  page();
  acFocus(document.getElementById("ac-title"));
}

globalThis.aftercareScreens = {
  formView: aftercareFormView,
  receiptView: aftercareReceiptView,
  concernView: aftercareConcernView,
  evaluatorView: aftercareEvaluatorView,
  submit: aftercareSubmit,
  workspaceView: aftercareWorkspaceView,
  reset: () => { acDraftState = null; },
};
globalThis.aftercareWorkspaceView = aftercareWorkspaceView;
