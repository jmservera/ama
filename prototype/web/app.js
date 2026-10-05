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
  view: "programme",
  agents: null,
  agentStatus: "loading",
  agentBusy: null,
  agentErrors: {},
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const perspectives = {
  programme: {
    title: "Programme delivery",
    description: "Scan the synthetic portfolio, see active episodes and holds, and inspect bounded case-review proposals before a human makes any programme decision.",
    task: "Focus: portfolio, stage and hand-off",
    filter: "",
    predicate: () => true,
  },
  frontline: {
    title: "Frontline coordination",
    description: "Work active synthetic episodes: record appointment outcomes, confirm whether appointments were verified, progress eligible stages and close or reopen episodes.",
    task: "Focus: active cases and appointment history",
    filter: "active",
    predicate: (item) => item.active,
  },
  assurance: {
    title: "Assurance & review",
    description: "Prioritise safety holds, human investigations, evidence gates, audit history and agent proposals awaiting an explicit human decision.",
    task: "Focus: holds, reviews and recorded evidence",
    filter: "",
    predicate: (item) => Boolean(item.safety_hold_active || item.review_required || item.pending_agent_reviews),
  },
  operator: {
    title: "Operator & intake",
    description: "Preview and validate synthetic workbook rows, review configuration and inspect the case record. Intake never overwrites existing cases.",
    task: "Focus: synthetic intake and configuration",
    filter: "",
    predicate: () => true,
  },
};

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
  try {
    appState.agents = await api("/api/agents");
    appState.agentStatus = "ready";
  } catch (error) {
    appState.agents = null;
    appState.agentStatus = "unavailable";
    appState.agentErrors.configuration = `Agent configuration could not be loaded: ${error.message}`;
  }
  const visibleCases = casesForPerspective();
  if (!keepSelection || !appState.selectedId || !visibleCases.some((item) => item.candidate_id === appState.selectedId)) {
    appState.selectedId = visibleCases[0]?.candidate_id || null;
  }
  appState.selectedCase = appState.selectedId
    ? await api(`/api/cases/${encodeURIComponent(appState.selectedId)}`)
    : null;
  render();
}

function render() {
  renderHeader();
  renderPerspective();
  renderMetrics();
  renderCaseList();
  positionImportSection();
  renderCaseDetail();
}

function casesForPerspective() {
  const perspective = perspectives[appState.view] || perspectives.programme;
  return appState.cases.filter(perspective.predicate);
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
  document.body.dataset.view = appState.view;
}

function renderPerspective() {
  const perspective = perspectives[appState.view] || perspectives.programme;
  for (const button of $$(".perspective-button")) {
    const selected = button.dataset.view === appState.view;
    button.classList.toggle("is-selected", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
  const summary = $("#perspective-summary");
  summary.replaceChildren(
    node("p", "", perspective.description),
    node("p", "perspective-task", perspective.task),
  );
  const queueTitle = appState.view === "frontline"
    ? "Active coordination queue"
    : appState.view === "assurance"
      ? "Cases needing assurance"
      : appState.view === "operator"
        ? "Intake and case lookup"
        : "Programme case portfolio";
  $(".panel-heading h2").textContent = queueTitle;
  $(".rail-footnote").textContent = appState.view === "assurance"
    ? "Safety holds and investigation flags remain human-owned; selecting a case does not clear either."
    : appState.view === "frontline"
      ? "Record synthetic appointment outcomes and use the existing human-controlled stage and episode actions."
      : appState.view === "operator"
        ? "Search the synthetic case set; use the intake panel below to preview workbook rows before committing."
        : "Review the synthetic portfolio and select a case to see its current gates, history and agent hand-offs.";
}

function positionImportSection() {
  const page = $(".page-shell");
  const section = $("#import-section");
  const footer = $(".page-footer");
  if (appState.view === "operator") page.insertBefore(section, $("#case-detail").closest(".workbench"));
  else page.insertBefore(section, footer);
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
  const cases = casesForPerspective();
  $("#case-count").textContent = cases.length;
  if (!cases.length) {
    list.append(node("p", "empty-note", appState.view === "assurance"
      ? "No active safety holds, pending investigations or agent proposals awaiting review in this synthetic result set."
      : "No synthetic cases match this view."));
    return;
  }
  const fragment = document.createDocumentFragment();
  for (const item of cases) {
    const button = node("button", `case-item${item.candidate_id === appState.selectedId ? " is-selected" : ""}`);
    button.type = "button";
    button.dataset.id = item.candidate_id;
    button.setAttribute("aria-pressed", String(item.candidate_id === appState.selectedId));
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

function registerEvidenceAliases(targets, targetId, values) {
  for (const value of values) {
    if (value !== undefined && value !== null && String(value).trim()) {
      targets.set(String(value), targetId);
    }
  }
}

function evidenceReference(id, targets) {
  const wrapper = node("span", "evidence-links");
  const targetId = targets.get(String(id));
  if (targetId) {
    const link = node("a", "evidence-link", `Open source ${id}`);
    link.href = `#${targetId}`;
    wrapper.append(link);
  } else {
    wrapper.append(node("span", "evidence-missing", `Source not present in this case response: ${id}`));
  }
  return wrapper;
}

function runMeta(run) {
  const usage = run.usage || {};
  const wrapper = node("div", "agent-run-meta");
  const values = [
    `Run ${run.run_id || "Not recorded"}`,
    `Candidate ${run.candidate_id || "Not recorded"}`,
    `Deployment ${run.model || "Not recorded"} · Resolved model ${run.resolved_model || "Not reported"}`,
    `Prompt ${run.prompt_version || "Not recorded"}`,
    `Prompt SHA-256 ${run.prompt_sha256 || "Not recorded"}`,
    `Duration ${Number.isFinite(run.duration_ms) ? `${run.duration_ms} ms` : "Not reported"}`,
    `Tokens ${Number.isFinite(usage.prompt_tokens) ? usage.prompt_tokens : "?"} prompt / ${Number.isFinite(usage.completion_tokens) ? usage.completion_tokens : "?"} completion`,
    `Created ${fmtDate(run.created_at)}`,
  ];
  if (run.reviewed_at || run.reviewed_by) {
    values.push(`Human disposition ${run.reviewed_by || "Actor not recorded"} · ${fmtDate(run.reviewed_at)}`);
  }
  for (const value of values) wrapper.append(node("span", "", value));
  return wrapper;
}

function agentRunCard(run, item, targets) {
  const card = node("article", "agent-run");
  const runTargets = new Map(targets);
  const snapshot = run.source_snapshot;
  if (snapshot) {
    const sourceId = `agent-source-${run.run_id}`;
    registerEvidenceAliases(runTargets, sourceId, [
      `case:${snapshot.candidate_id}:row:${snapshot.source_row}`,
      "control:safety_hold", "control:active_episode", "control:stage_mapping",
      "control:transition_gates", "rule:006",
    ]);
    const source = node("details", "agent-source");
    source.id = sourceId;
    source.append(node("summary", "", "Captured synthetic evidence snapshot"));
    source.append(node("p", "microcopy", "Evidence used by this run, not a claim that the case is still unchanged."));
    source.append(node("pre", "", JSON.stringify(snapshot, null, 2)));
    card.append(source);
  }
  const heading = node("div", "agent-run-head");
  const title = node("h4", "", "Case Review Agent proposal");
  const status = node("span", `status-tag${run.state === "failed" ? " is-alert" : ""}`, run.state || "Unknown state");
  heading.append(title, status);
  card.append(heading, runMeta(run));
  if (run.proposal) {
    const proposal = node("div", "agent-proposal");
    proposal.append(node("p", "", run.proposal.summary || "No summary was recorded."));
    if (run.proposal.recommended_owner) {
      proposal.append(node("p", "", `Suggested owner: ${run.proposal.recommended_owner}`));
    }
    const findings = node("ul", "agent-findings");
    for (const finding of run.proposal.findings || []) {
      const row = node("li", "agent-finding");
      row.append(node("strong", "", String(finding.kind || "Finding")));
      row.append(node("p", "", finding.next_action || "No next action was recorded."));
      const references = finding.evidence_ids || [];
      if (references.length) {
        row.append(node("p", "", "Evidence references"));
        for (const evidenceId of references) {
          const reference = evidenceReference(evidenceId, runTargets);
          reference.querySelector("a")?.addEventListener("click", () => {
            const source = card.querySelector(".agent-source");
            if (source) source.open = true;
          });
          row.append(reference);
        }
      } else {
        row.append(node("span", "evidence-missing", "No evidence references supplied."));
      }
      findings.append(row);
    }
    if (!findings.childElementCount) findings.append(node("li", "empty-note", "No findings were recorded."));
    proposal.append(findings);
    card.append(proposal);
  } else if (run.state === "failed") {
    card.append(node("p", "agent-intro agent-error-text", run.error || "The agent run failed without an error description."));
  } else {
    card.append(node("p", "agent-intro", "This run contains no proposal."));
  }
  const trace = node("details", "agent-trace");
  trace.append(node("summary", "", `Tool and state trace (${(run.trace || []).length} steps)`));
  const steps = node("ol");
  for (const entry of run.trace || []) {
    const step = node("li");
    step.append(node("strong", "", `${entry.state || "state"}: `), document.createTextNode(entry.detail || "No detail recorded."));
    steps.append(step);
  }
  if (!steps.childElementCount) steps.append(node("li", "", "No trace entries recorded."));
  trace.append(steps);
  card.append(trace);

  if (run.state === "awaiting_review") {
    const actions = node("div", "agent-review-actions");
    for (const [decision, label, className] of [
      ["accepted", "Accept suggestion", "button button-primary button-small"],
      ["rejected", "Reject suggestion", "button button-quiet button-small"],
    ]) {
      const button = node("button", className, label);
      button.type = "button";
      button.disabled = appState.agentBusy === item.candidate_id;
      button.addEventListener("click", () => reviewAgentRun(item, run, decision));
      actions.append(button);
    }
    actions.append(node("span", "agent-review-state", "Records a human disposition only. It does not approve evidence, satisfy a gate or change case stage."));
    card.append(actions);
  } else if (run.state === "accepted" || run.state === "rejected") {
    card.append(node("p", "agent-review-state", `Human ${run.state} disposition recorded. This is not evidence approval or a workflow transition.`));
  }
  return card;
}

function renderAgentPanel(item, targets) {
  const panel = node("section", "detail-card is-agent");
  panel.dataset.workspaces = "programme assurance";
  const config = appState.agents;
  const heading = node("div", "agent-heading");
  const title = node("div");
  title.append(node("p", "card-kicker", "Bounded synthetic case review"));
  title.append(node("h3", "", "Case Review Agent · proposal and human hand-off"));
  heading.append(title);
  let statusText = "Configuration loading";
  let statusClass = "status-tag";
  if (appState.agentStatus === "unavailable") {
    statusText = "Configuration unavailable";
    statusClass += " is-alert";
  } else if (config?.configured) {
    statusText = "Configured";
  } else if (config && !config.configured) {
    statusText = "Disabled / not configured";
    statusClass += " is-alert";
  }
  heading.append(node("span", `${statusClass} agent-status`, statusText));
  panel.append(heading);
  panel.append(node("p", "agent-intro", config?.configured
    ? `Model: ${config.model || "Not reported"} · Prompt: ${config.prompt_version || "Not reported"}`
    : "This prototype surface is for the bounded Case Review Agent. No model-generated proposal is shown unless a configured run returns one."));
  const reason = appState.agentStatus === "unavailable"
    ? appState.agentErrors.configuration
    : config?.configured
      ? ""
      : config?.reason || "No inference endpoint or model configuration is available.";
  if (reason) panel.append(node("p", "agent-error", `Run unavailable: ${reason}`));
  panel.append(node("p", "agent-boundary", "The agent may propose a case summary, evidence-linked findings and a suggested owner. It cannot write evidence, record appointments, change gates, mark an investigation complete, close a case or advance a stage. A human disposition is not an operational approval."));
  const controls = node("div", "agent-controls");
  const runButton = node("button", "button button-primary button-small", appState.agentBusy === item.candidate_id ? "Run in progress…" : "Request case review");
  runButton.type = "button";
  runButton.disabled = !config?.configured || appState.agentStatus !== "ready" || appState.agentBusy === item.candidate_id;
  runButton.addEventListener("click", () => requestAgentRun(item));
  controls.append(runButton);
  controls.append(node("span", "microcopy", `Actor label sent with request: ${actor()}. This label is not authenticated identity.`));
  panel.append(controls);
  if (appState.agentErrors[item.candidate_id]) {
    panel.append(node("p", "agent-error", appState.agentErrors[item.candidate_id]));
  }
  const runs = Array.isArray(item.agent_runs) ? [...item.agent_runs] : [];
  runs.sort((left, right) => new Date(right.created_at || 0) - new Date(left.created_at || 0));
  const runList = node("div", "agent-runs");
  if (!runs.length) {
    runList.append(node("p", "empty-note", config?.configured
      ? "No review runs for this synthetic case yet."
      : "No generated output is available because agent inference is not configured."));
  } else {
    for (const run of runs) runList.append(agentRunCard(run, item, targets));
  }
  panel.append(runList);
  return panel;
}

async function requestAgentRun(item) {
  if (appState.agentBusy === item.candidate_id || !appState.agents?.configured) return;
  appState.agentBusy = item.candidate_id;
  delete appState.agentErrors[item.candidate_id];
  renderCaseDetail();
  let result;
  try {
    result = await api(`/api/cases/${encodeURIComponent(item.candidate_id)}/agent-run`, {
      method: "POST",
      body: JSON.stringify({ actor: actor() }),
    });
  } catch (error) {
    appState.agentErrors[item.candidate_id] = `Agent run failed: ${error.message}`;
    try {
      await refresh();
    } catch (refreshError) {
      appState.agentErrors[item.candidate_id] += ` Case refresh also failed: ${refreshError.message}`;
    }
    announce(appState.agentErrors[item.candidate_id], "error");
    appState.agentBusy = null;
    renderCaseDetail();
    return;
  }
  try {
    await refresh();
    if (result?.state === "failed") {
      announce(`Agent run failed: ${result.error || "No error description was returned."}`, "error");
    } else {
      announce("Case Review Agent run recorded. Review its evidence and trace before deciding what to do.", "success");
    }
  } catch (error) {
    appState.agentErrors[item.candidate_id] = `Agent run request succeeded, but case refresh failed: ${error.message}`;
    announce(appState.agentErrors[item.candidate_id], "error");
  } finally {
    appState.agentBusy = null;
    renderCaseDetail();
  }
}

async function reviewAgentRun(item, run, decision) {
  if (appState.agentBusy === item.candidate_id || run.state !== "awaiting_review") return;
  appState.agentBusy = item.candidate_id;
  delete appState.agentErrors[item.candidate_id];
  renderCaseDetail();
  try {
    await api(`/api/cases/${encodeURIComponent(item.candidate_id)}/agent-review`, {
      method: "POST",
      body: JSON.stringify({ run_id: run.run_id, decision, actor: actor() }),
    });
  } catch (error) {
    appState.agentErrors[item.candidate_id] = `Could not record human proposal disposition: ${error.message}`;
    try {
      await refresh();
    } catch (refreshError) {
      appState.agentErrors[item.candidate_id] += ` Case refresh also failed: ${refreshError.message}`;
    }
    announce(appState.agentErrors[item.candidate_id], "error");
    appState.agentBusy = null;
    renderCaseDetail();
    return;
  }
  try {
    await refresh();
    announce(`Human ${decision} disposition recorded for the proposal only; case gates and stage are unchanged.`, "success");
  } catch (error) {
    appState.agentErrors[item.candidate_id] = `Human disposition request succeeded, but case refresh failed: ${error.message}`;
    announce(appState.agentErrors[item.candidate_id], "error");
  } finally {
    appState.agentBusy = null;
    renderCaseDetail();
  }
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
  const evidenceTargets = new Map();
  registerEvidenceAliases(evidenceTargets, "case-record", [item.candidate_id, `case:${item.candidate_id}`, `row:${item.source_row}`]);
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
  overview.id = "case-record";
  overview.dataset.workspaces = "programme frontline assurance operator";
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
  rule.dataset.workspaces = "programme frontline assurance";
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
  gateCard.id = "case-gates";
  gateCard.dataset.workspaces = "assurance";
  gateCard.append(node("p", "card-kicker", "Human-controlled release"), node("h3", "", "Evidence gates"));
  const gateForm = node("form", "gate-form");
  const gates = node("div", "gate-grid");
  for (const [key, label] of Object.entries(appState.settings.gates)) {
    const wrapper = node("label", "gate-option");
    wrapper.id = `gate-source-${key}`;
    registerEvidenceAliases(evidenceTargets, wrapper.id, [key, `gate:${key}`]);
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
  actionsCard.dataset.workspaces = "frontline assurance";
  actionsCard.append(node("p", "card-kicker", "Scenario actions"), node("h3", "", "Record what happened"));
  const actions = node("div", "scenario-actions");
  const appointmentForm = node("form", "action-row");
  appointmentForm.dataset.workspaces = "frontline";
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
    review.dataset.workspaces = "assurance";
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
  stageForm.dataset.workspaces = "programme frontline";
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
  closureForm.dataset.workspaces = "programme frontline";
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

  const thresholdCard = node("section", "detail-card");
  thresholdCard.dataset.workspaces = "operator";
  thresholdCard.append(node("p", "card-kicker", "Operator configuration"), node("h3", "", "Synthetic test threshold"));
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
  thresholdCard.append(thresholdForm);
  const thresholdNote = node("p", "microcopy", "Demonstration setting only. Changes do not establish a company-approved operational rule.");
  thresholdCard.append(thresholdNote);
  grid.append(thresholdCard);
  grid.append(actionsCard);

  const activity = node("section", "detail-card activity-card");
  activity.id = "case-history";
  activity.dataset.workspaces = "programme frontline assurance";
  activity.append(node("p", "card-kicker", "Audit trail"), node("h3", "", "Recorded evidence"));
  const events = node("ul", "event-list");
  for (const [index, event] of [...item.appointment_events].reverse().entries()) {
    const row = node("li", "event-item");
    row.id = `appointment-source-${index}`;
    registerEvidenceAliases(evidenceTargets, row.id, [
      event.id, event.event_id, event.evidence_id, event.source_id,
      `event:${event.id}`, `event:${event.event_id}`, `appointment:${event.id}`,
    ]);
    row.append(node("span", "event-time", fmtDate(event.occurred_at)));
    const description = node("span");
    const outcome = appState.settings.outcomes[event.outcome] || event.outcome.replaceAll("_", " ");
    description.append(node("strong", "", outcome));
    description.append(node("small", "", `${event.appointment_confirmed ? "Confirmed appointment" : "Confirmation not recorded"} · ${event.actor_label}`));
    row.append(description);
    row.append(node("span", "status-tag", event.source_file || "Scenario"));
    events.append(row);
  }
  for (const [index, entry] of item.audit.entries()) {
    const row = node("li", "event-item");
    row.id = `audit-source-${index}`;
    registerEvidenceAliases(evidenceTargets, row.id, [
      entry.id, entry.audit_id, entry.event_id, entry.evidence_id, entry.source_id,
      `audit:${entry.id}`, `audit:${entry.audit_id}`,
    ]);
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
  grid.append(renderAgentPanel(item, evidenceTargets));
  shell.append(grid);
  root.append(shell);
  for (const card of $$("[data-workspaces]", grid)) {
    card.hidden = !card.dataset.workspaces.split(/\s+/).includes(appState.view);
  }
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
  for (const button of $$(".perspective-button")) {
    button.addEventListener("click", async () => {
      const nextView = button.dataset.view;
      if (!perspectives[nextView] || nextView === appState.view) return;
      appState.view = nextView;
      appState.filter = perspectives[nextView].filter;
      for (const filterButton of $$(".filter-button")) {
        const selected = (filterButton.dataset.filter || "") === appState.filter;
        filterButton.classList.toggle("is-active", selected);
        filterButton.setAttribute("aria-pressed", String(selected));
      }
      render();
      try {
        await refresh();
      } catch (error) {
        announce(`Could not load this perspective: ${error.message}`, "error");
      }
    });
  }
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
      $$(".filter-button").forEach((item) => {
        const selected = item === button;
        item.classList.toggle("is-active", selected);
        item.setAttribute("aria-pressed", String(selected));
      });
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
