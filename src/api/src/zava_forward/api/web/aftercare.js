"use strict";
// Synthetic staff-assisted aftercare screens (issue 133, Stage A). Not wired into any route yet.
// Shares h and api with app.js. Every function renders a returned contract or posts to it; nothing
// here reads storage, calls a model or decides anything on the server's behalf.
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
    h("p", {}, `${acText(usable.count)} of ${acText(usable.denominator)} homes have a usable comparison. Concerns raised: ${acText(totals.concerns_raised)}. Unresolved: ${acText(totals.concerns_unresolved)}.`),
    rows.length
      ? h("table", {},
        h("caption", {}, "Observed baseline and late means, with concerns by home"),
        h("thead", {}, h("tr", {},
          ...["Home", "Comparison", "Baseline mean", "Late mean", "Concerns", "Unresolved"].map((t) => h("th", { scope: "col" }, t)))),
        h("tbody", {}, ...rows))
      : h("p", {}, "No homes are in the synthetic cohort."),
    h("h2", {}, "What is not known"),
    h("ul", {}, ...(v.unknowns || []).map((u) => h("li", {}, acText(u)))),
    h("p", {}, acText(v.sensor_note)));
}

function aftercareErrorMessage(error) {
  if (error && error.status === 401) return "Your session has ended. Sign in again.";
  if (error && error.status === 403) return "Your role cannot do this. Ask a colleague who can, or use the paper route.";
  if (error && error.status === 409) return error.message || "This request conflicts with an earlier one.";
  if (error && error.status === 503) return "The record could not be saved or read. Nothing was saved. Use the paper route.";
  if (error && error.status === 400) return error.message || "Some details need fixing.";
  return "The service could not be reached. Nothing was saved. Keep this page open and try again, or use the paper route.";
}

// The shared api() must copy data.errors onto the thrown error (hook item). The caller owns requestId and keeps it across retries so a repeated send is recognised.
async function aftercareSubmit(api, values, requestId, signal) {
  const body = { ...values, request_id: requestId };
  try {
    const reply = await api(`${AFTERCARE_API}/concerns`, body, signal);
    if (!reply || !reply.receipt) return { ok: false, message: aftercareErrorMessage(null), errors: {}, retainRequestId: true };
    return { ok: true, receipt: reply.receipt, replay: Boolean(reply.replayed) };
  } catch (error) {
    if (error && error.name === "AbortError") throw error;
    const errors = (error && error.errors) || {};
    const definite = error && [400, 403, 409].includes(error.status);
    return { ok: false, message: aftercareErrorMessage(error), errors, retainRequestId: !definite };
  }
}

globalThis.aftercareScreens = {
  formView: aftercareFormView,
  receiptView: aftercareReceiptView,
  concernView: aftercareConcernView,
  evaluatorView: aftercareEvaluatorView,
  submit: aftercareSubmit,
};
