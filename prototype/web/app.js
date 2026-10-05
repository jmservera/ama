const requestedTheme = new URLSearchParams(window.location.search).get("scoutTheme");
document.documentElement.setAttribute(
  "data-theme",
  requestedTheme || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"),
);

const appState = {
  cases: [],
  overview: null,
  settings: null,
  selectedId: null,
  selectedCase: null,
  filter: "",
  preview: null,
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined && text !== null) element.textContent = String(text);
  return element;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...options.headers },
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status}).`);
  return payload;
}

function actor() {
  return $("#actor").value || "Local reviewer";
}

function announce(message, kind = "success") {
  const notice = $("#notice");
  notice.textContent = message;
  notice.className = `notice is-${kind}`;
  notice.hidden = false;
  window.setTimeout(() => { notice.hidden = true; }, 6000);
}

function fmtDate(value) {
  if (!value) return "Not recorded";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function stageNumber(stage) {
  const match = String(stage || "").match(/^(\d{2})/);
  return match ? match[1] : "—";
}

async function refresh(keepSelection = true) {
  const [overview, casePayload, settings] = await Promise.all([
    api("/api/overview"),
    api(`/api/cases?filter=${encodeURIComponent(appState.filter)}&q=${encodeURIComponent($("#search").value.trim())}`),
    api("/api/settings"),
  ]);
  appState.overview = overview;
  appState.cases = casePayload.cases;
  appState.settings = settings;
  if (!keepSelection || !appState.selectedId || !appState.cases.some((item) => item.candidate_id === appState.selectedId)) {
    appState.selectedId = appState.cases[0]?.candidate_id || null;
  }
  appState.selectedCase = appState.selectedId
    ? await api(`/api/cases/${encodeURIComponent(appState.selectedId)}`)
    : null;
  render();
}

function render() {
  renderHeader();
  renderMetrics();
  renderCaseList();
  renderCaseDetail();
}

function renderHeader() {
  const select = $("#actor");
  const selected = select.value || "Local reviewer";
  select.replaceChildren();
  for (const label of appState.settings?.actors || ["Local reviewer"]) {
    const option = node("option", "", label);
    option.value = label;
    option.selected = label === selected;
    select.append(option);
  }
  const localOnly = appState.settings?.mode !== "internal-container";
  $("#network-mode-label").textContent = localOnly ? "Local only" : "Internal network only";
  $("#data-safety-note").replaceChildren(
    node("strong", "", "Synthetic data only."),
    document.createTextNode(
      localOnly
        ? " Do not enter real resident, staff, address or contact information. This demonstrator has no M365 connection and binds only to this computer."
        : " Do not enter real resident, staff, address or contact information. This container listener is intended only for Azure Container Apps internal ingress; never expose it publicly.",
    ),
  );
}

function renderMetrics() {
  const data = appState.overview;
  if (!data) return;
  $("#metric-total").textContent = data.total_cases;
  $("#metric-active").textContent = data.active_cases;
  $("#metric-held").textContent = data.active_safety_holds;
  $("#metric-threshold").textContent = `>${data.threshold}`;
  $("#source-label").textContent = data.source_label;
}

function renderCaseList() {
  const list = $("#case-list");
  list.replaceChildren();
  $("#case-count").textContent = appState.cases.length;
  if (!appState.cases.length) {
    list.append(node("p", "empty-note", "No cases match this view."));
    return;
  }
  const fragment = document.createDocumentFragment();
  for (const item of appState.cases) {
    const button = node("button", `case-item${item.candidate_id === appState.selectedId ? " is-selected" : ""}`);
    button.type = "button";
    button.dataset.id = item.candidate_id;
    const head = node("span", "case-item-head");
    head.append(node("strong", "", item.candidate_id));
    const status = node("span", `status-tag${item.safety_hold_active ? " is-hold" : item.review_required ? " is-alert" : ""}`,
      item.safety_hold_active ? "Safety hold" : item.review_required ? "Review" : item.active ? "Active" : "Closed");
    head.append(status);
    button.append(head, node("small", "", item.property_ref));
    const meta = node("span", "case-item-meta");
    meta.append(node("span", "", item.current_status || "Status unknown"));
    if (item.locality) meta.append(node("span", "", item.locality));
    button.append(meta);
    button.addEventListener("click", async () => {
      appState.selectedId = item.candidate_id;
      await refresh();
    });
    fragment.append(button);
  }
  list.append(fragment);
}

function dataPoint(label, value) {
  const wrapper = node("div", "data-point");
  wrapper.append(node("span", "", label), node("strong", "", value || "Not recorded"));
  return wrapper;
}

function renderCaseDetail() {
  const root = $("#case-detail");
  root.replaceChildren();
  const item = appState.selectedCase;
  if (!item) {
    const empty = node("div", "empty-state panel");
    empty.append(node("span", "empty-mark", "✳"), node("h2", "", "Choose a synthetic case"));
    empty.append(node("p", "", "Case evidence and controlled actions will appear here."));
    root.append(empty);
    return;
  }

  const shell = node("article", "case-panel panel");
  const header = node("header", "case-header");
  const titleBlock = node("div");
  titleBlock.append(node("p", "eyebrow", "Synthetic case file"));
  titleBlock.append(node("h2", "", item.candidate_id));
  titleBlock.append(node("p", "case-ref", `Property reference · ${item.property_ref}`));
  header.append(titleBlock);
  const statusBlock = node("div", "case-status");
  statusBlock.append(
    node("span", `status-tag${item.safety_hold_active ? " is-hold" : item.review_required ? " is-alert" : ""}`,
      item.safety_hold_active ? "Safety hold active" : item.review_required ? "Human investigation due" : item.active ? "Active episode" : "Closed episode"),
    node("span", "microcopy", `Source row ${item.source_row}`),
  );
  header.append(statusBlock);
  shell.append(header);

  const grid = node("div", "detail-grid");
  const overview = node("section", "detail-card");
  overview.append(node("p", "card-kicker", "Case profile"), node("h3", "", "At a glance"));
  const overviewData = node("div", "data-grid");
  overviewData.append(
    dataPoint("Locality", item.locality),
    dataPoint("Archetype", item.archetype_id),
    dataPoint("Lead supplier", item.lead_supplier),
    dataPoint("Programme owner", item.owner),
    dataPoint("RAG status", item.rag_status),
    dataPoint("Source file", item.source_file?.split("/").at(-1)),
  );
  overview.append(overviewData);
  const stage = node("div", "stage-line");
  stage.append(node("span", "stage-number", stageNumber(item.scenario_stage)));
  stage.append(node("strong", "", item.scenario_stage || item.current_status));
  overview.append(stage);
  grid.append(overview);

  const rule = node("section", `detail-card alert-card${item.review_required ? " is-required" : ""}`);
  rule.append(node("p", "card-kicker", "RULE-006 · Synthetic test only"));
  rule.append(node("h3", "", item.review_required ? "Investigation needs a human" : "Appointment threshold"));
  const count = node("div", "alert-count");
  count.append(node("strong", "", item.eligible_count), node("span", "", `eligible / > ${item.threshold}`));
  rule.append(count);
  rule.append(node("p", "", item.review_required
    ? "Record a human investigation before closing. The count is not a finding of refusal or non-cooperation."
    : "Only verified resident no-access at a confirmed appointment counts. Other outcomes stay in the event history."));
  grid.append(rule);

  const gateCard = node("section", "detail-card control-card");
  gateCard.append(node("p", "card-kicker", "Human-controlled release"), node("h3", "", "Evidence gates"));
  const gateForm = node("form", "gate-form");
  const gates = node("div", "gate-grid");
  for (const [key, label] of Object.entries(appState.settings.gates)) {
    const wrapper = node("label", "gate-option");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = key;
    checkbox.checked = Boolean(item.controls[key]);
    checkbox.disabled = !item.active;
    wrapper.append(checkbox, node("span", "", label));
    gates.append(wrapper);
  }
  gateForm.append(gates);
  const gateActions = node("div", "gate-actions");
  gateActions.append(node("span", "microcopy", "Scenario controls only · audit recorded"));
  const saveGates = node("button", "button button-quiet button-small", "Save gates");
  saveGates.type = "submit";
  saveGates.disabled = !item.active;
  gateActions.append(saveGates);
  gateForm.append(gateActions);
  gateForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const controls = Object.fromEntries($$("input[type=checkbox]", gateForm).map((input) => [input.name, input.checked]));
    await runAction(() => api(`/api/cases/${encodeURIComponent(item.candidate_id)}/controls`, {
      method: "POST",
      body: JSON.stringify({ controls, actor: actor() }),
    }), "Scenario gates saved.");
  });
  gateCard.append(gateForm);
  grid.append(gateCard);

  const actionsCard = node("section", "detail-card");
  actionsCard.append(node("p", "card-kicker", "Scenario actions"), node("h3", "", "Record what happened"));
  const actions = node("div", "scenario-actions");
  const appointmentForm = node("form", "action-row");
  const outcomeLabel = node("label");
  outcomeLabel.append(node("span", "", "Appointment outcome"));
  const outcomeSelect = document.createElement("select");
  outcomeSelect.name = "outcome";
  for (const [key, label] of Object.entries(appState.settings.outcomes)) {
    const option = node("option", "", label);
    option.value = key;
    outcomeSelect.append(option);
  }
  outcomeLabel.append(outcomeSelect);
  appointmentForm.append(outcomeLabel);
  const confirmedLabel = node("label", "checkline");
  const confirmed = document.createElement("input");
  confirmed.type = "checkbox";
  confirmedLabel.append(confirmed, node("span", "", "Appointment confirmed"));
  appointmentForm.append(confirmedLabel);
  const recordButton = node("button", "button button-primary button-small", "Record outcome");
  recordButton.type = "submit";
  recordButton.disabled = !item.active;
  appointmentForm.append(recordButton);
  appointmentForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runAction(() => api(`/api/cases/${encodeURIComponent(item.candidate_id)}/appointment`, {
      method: "POST",
      body: JSON.stringify({ outcome: outcomeSelect.value, appointment_confirmed: confirmed.checked, actor: actor() }),
    }), "Appointment outcome added to the synthetic history.");
  });
  actions.append(appointmentForm);

  if (item.review_required) {
    const review = node("form", "review-callout");
    const copy = node("p");
    copy.append(node("strong", "", "Human investigation required"), node("span", "", "Record that a reviewer examined this synthetic case. No free-text notes are stored."));
    review.append(copy);
    const reviewButton = node("button", "button button-primary button-small", "Mark investigated");
    reviewButton.type = "submit";
    review.append(reviewButton);
    review.addEventListener("submit", async (event) => {
      event.preventDefault();
      await runAction(() => api(`/api/cases/${encodeURIComponent(item.candidate_id)}/review`, {
        method: "POST",
        body: JSON.stringify({ actor: actor() }),
      }), "Human investigation recorded.");
    });
    actions.append(review);
  }

  const stageForm = node("form", "action-row");
  const stageButton = node("button", "button button-quiet button-small", "Try next stage");
  stageButton.type = "submit";
  stageButton.disabled = !item.active;
  stageForm.append(stageButton, node("span", "microcopy", "Blocked when required gates or a safety hold remain."));
  stageForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runAction(async () => {
      const result = await api(`/api/cases/${encodeURIComponent(item.candidate_id)}/advance`, {
        method: "POST",
        body: JSON.stringify({ actor: actor() }),
      });
      if (!result.advanced) throw new Error(`Stage held: ${result.missing.join(", ")}`);
      return result;
    }, "Case advanced to the next synthetic stage.");
  });
  actions.append(stageForm);

  const closureForm = node("form", "action-row");
  if (item.active) {
    const reasonLabel = node("label");
    reasonLabel.append(node("span", "", "Human closure reason"));
    const reasonSelect = document.createElement("select");
    reasonSelect.name = "reason";
    const reasonCopy = {
      human_review_completed: "Human review completed",
      scenario_complete: "Synthetic scenario complete",
      synthetic_test_reset: "Reset synthetic test case",
    };
    for (const reason of appState.settings.closure_reasons) {
      const option = node("option", "", reasonCopy[reason] || reason);
      option.value = reason;
      reasonSelect.append(option);
    }
    reasonLabel.append(reasonSelect);
    closureForm.append(reasonLabel);
    const closeButton = node("button", "button button-quiet button-small", "Close case");
    closeButton.type = "submit";
    closureForm.append(closeButton);
    closureForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await runAction(() => api(`/api/cases/${encodeURIComponent(item.candidate_id)}/close`, {
        method: "POST",
        body: JSON.stringify({ reason: reasonSelect.value, actor: actor() }),
      }), "Case closed. Its active counter resets; event history is retained.");
    });
  } else {
    const reopenButton = node("button", "button button-quiet button-small", "Reopen new episode");
    reopenButton.type = "button";
    reopenButton.addEventListener("click", async () => {
      await runAction(() => api(`/api/cases/${encodeURIComponent(item.candidate_id)}/reopen`, {
        method: "POST",
        body: JSON.stringify({ actor: actor() }),
      }), "Case reopened as a new episode. The previous history remains available.");
    });
    closureForm.append(reopenButton);
  }
  actions.append(closureForm);
  actionsCard.append(actions);

  const thresholdForm = node("form", "threshold-form");
  thresholdForm.append(node("label", "", "Synthetic test threshold"));
  const thresholdInput = document.createElement("input");
  thresholdInput.type = "number";
  thresholdInput.min = "0";
  thresholdInput.max = "100";
  thresholdInput.step = "1";
  thresholdInput.value = appState.settings.threshold;
  thresholdInput.setAttribute("aria-label", "Synthetic test threshold");
  const thresholdLabel = thresholdForm.querySelector("label");
  thresholdLabel.append(thresholdInput);
  const thresholdButton = node("button", "button button-quiet button-small", "Save threshold");
  thresholdButton.type = "submit";
  thresholdForm.append(thresholdButton);
  thresholdForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runAction(() => api("/api/settings", {
      method: "POST",
      body: JSON.stringify({ threshold: thresholdInput.value, actor: actor() }),
    }), "Threshold configuration version saved.");
  });
  actionsCard.append(thresholdForm);
  grid.append(actionsCard);

  const activity = node("section", "detail-card activity-card");
  activity.append(node("p", "card-kicker", "Audit trail"), node("h3", "", "Recorded evidence"));
  const events = node("ul", "event-list");
  for (const event of [...item.appointment_events].reverse()) {
    const row = node("li", "event-item");
    row.append(node("span", "event-time", fmtDate(event.occurred_at)));
    const description = node("span");
    const outcome = appState.settings.outcomes[event.outcome] || event.outcome.replaceAll("_", " ");
    description.append(node("strong", "", outcome));
    description.append(node("small", "", `${event.appointment_confirmed ? "Confirmed appointment" : "Confirmation not recorded"} · ${event.actor_label}`));
    row.append(description);
    row.append(node("span", "status-tag", event.source_file || "Scenario"));
    events.append(row);
  }
  for (const entry of item.audit) {
    const row = node("li", "event-item");
    row.append(node("span", "event-time", fmtDate(entry.created_at)));
    const description = node("span");
    description.append(node("strong", "", entry.event_type.replaceAll("_", " ")));
    description.append(node("small", "", `${entry.actor_label} · ${JSON.stringify(entry.details)}`));
    row.append(description, node("span", "status-tag", "Audit"));
    events.append(row);
  }
  if (!item.appointment_events.length && !item.audit.length) events.append(node("li", "empty-note", "No scenario actions recorded yet."));
  activity.append(events);
  grid.append(activity);
  shell.append(grid);
  root.append(shell);
}

async function runAction(action, successMessage) {
  try {
    await action();
    await refresh();
    announce(successMessage, "success");
  } catch (error) {
    announce(error.message, "error");
  }
}

function renderImport(preview) {
  const container = $("#import-result");
  container.replaceChildren();
  container.hidden = false;
  const summary = node("div", "import-summary");
  summary.append(
    node("span", "", `Workbook: ${preview.source_file || preview.source_name}`),
    node("span", "", `Accepted: ${preview.accepted}`),
    node("span", "", `Rejected: ${preview.rejected}`),
    node("span", "", `SHA-256: ${preview.sha256 || preview.digest}`),
  );
  if (preview.warnings?.length) {
    const warnings = node("p", "import-warnings", preview.warnings.join(" "));
    summary.append(warnings);
  }
  container.append(summary);
  const rows = preview.rows || [
    ...(preview.rejected_rows || []).map((row) => ({ ...row, disposition: "Rejected" })),
  ];
  if (rows.length) {
    const wrap = node("div", "import-table-wrap");
    const table = node("table", "import-table");
    const head = node("thead");
    const heading = node("tr");
    for (const label of ["Row", "Candidate", "Disposition", "Issues"]) heading.append(node("th", "", label));
    head.append(heading);
    const body = node("tbody");
    for (const row of rows) {
      const tr = node("tr");
      tr.append(node("td", "", row.source_row ?? "—"));
      tr.append(node("td", "", row.candidate_id || "—"));
      tr.append(node("td", "", row.disposition || "Accepted"));
      tr.append(node("td", "", (row.issues || []).join(" ")));
      body.append(tr);
    }
    table.append(head, body);
    wrap.append(table);
    container.append(wrap);
  }
  if (preview.preview_token && preview.accepted > 0) {
    const footer = node("div", "import-bottom");
    footer.append(node("span", "microcopy", "Commit rechecks candidate IDs; conflicts abort the full import."));
    const commit = node("button", "button button-primary button-small", "Commit accepted rows");
    commit.type = "button";
    commit.addEventListener("click", async () => {
      await runAction(async () => {
        const result = await api("/api/import/commit", {
          method: "POST",
          body: JSON.stringify({ preview_token: preview.preview_token, actor: actor() }),
        });
        appState.preview = null;
        $("#import-result").hidden = true;
        return result;
      }, "Workbook imported without overwriting existing cases.");
    });
    footer.append(commit);
    container.append(footer);
  }
}

function toBase64(bytes) {
  let binary = "";
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize));
  }
  return btoa(binary);
}

async function previewWorkbook() {
  const file = $("#workbook").files[0];
  if (!file) {
    announce("Choose a workbook before previewing.", "error");
    return;
  }
  if (!file.name.toLowerCase().endsWith(".xlsx")) {
    announce("Only .xlsx workbooks are supported.", "error");
    return;
  }
  try {
    const bytes = new Uint8Array(await file.arrayBuffer());
    const preview = await api("/api/import/preview", {
      method: "POST",
      body: JSON.stringify({ filename: file.name, workbook_base64: toBase64(bytes) }),
    });
    appState.preview = preview;
    renderImport(preview);
    announce("Import preview ready. Review every row before committing.", "success");
  } catch (error) {
    announce(error.message, "error");
  }
}

function bindEvents() {
  $("#preview-import").addEventListener("click", previewWorkbook);
  $("#export-link").addEventListener("click", async (event) => {
    event.preventDefault();
    try {
      const data = await api("/api/export");
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "proper-warm-synthetic-export.json";
      anchor.click();
      URL.revokeObjectURL(url);
      announce("Synthetic evidence export downloaded.", "success");
    } catch (error) {
      announce(error.message, "error");
    }
  });
  for (const button of $$(".filter-button")) {
    button.addEventListener("click", async () => {
      appState.filter = button.dataset.filter || "";
      $$(".filter-button").forEach((item) => item.classList.toggle("is-active", item === button));
      try { await refresh(false); } catch (error) { announce(error.message, "error"); }
    });
  }
  let searchTimer;
  $("#search").addEventListener("input", () => {
    window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(async () => {
      try { await refresh(false); } catch (error) { announce(error.message, "error"); }
    }, 180);
  });
  $("#actor").addEventListener("change", () => renderCaseDetail());
}

async function start() {
  bindEvents();
  try {
    await refresh(false);
  } catch (error) {
    announce(`Could not connect to the local prototype: ${error.message}`, "error");
  }
}

start();
