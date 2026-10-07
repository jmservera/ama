'use strict';

(() => {
  const param = new URLSearchParams(window.location.search).get('scoutTheme');
  const theme =
    param || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
})();

(() => {
  const $ = (id) => document.getElementById(id);
  const state = {
    config: null, role: 'viewer', workflow: '', query: '', cases: [],
    portfolio: null, asOf: null, scope: null, selectedId: null, detail: null,
    drill: null, pending: null, writing: false, assistantBusy: false,
    assistant: null, assistantCaseId: null, listRequest: 0, detailRequest: 0,
  };
  const fieldHelp = {
    reason: 'Required human exercise rationale. Explain why this decision or observation is being recorded.',
    source: 'Required constructed source identifier, e.g. exercise:survey-900. No URL is fetched and no file is uploaded.',
    evidenceId: 'Constructed evidence identifier. Use new evidence for reinspection; an assistant draft is not approval evidence.',
    designVersion: 'Current design version from case facts, not the case record version shown above.',
    packageVersion: 'Current package version from case facts. Capacity and release must reference the same package.',
    slots: 'Positive whole number of committed exercise capacity slots.',
    amount: 'Nonnegative synthetic amount. Claimed is simulated submitted value, not acceptance or payment.',
    dueAt: 'ISO timestamp, e.g. 2026-10-08T16:00:00Z. Resident-update ownership remains separate from handoff ownership.',
    destination: 'Receiving role. Sending or receiving does not transfer the current owner; acceptance does.',
    handoffId: 'Exact active handoff ID shown in the handoff panel. Only its destination can receive, accept or return it.',
    referralId: 'Exact linked referral identifier. Acknowledgement records receipt only; it never clears the hazard hold.',
    appointmentId: 'Unique identifier per case. Recording the same appointment twice is rejected.',
    confirmed: 'Only a confirmed AND verified resident_no_access contributes to the exercise no-access count.',
    verified: 'Verify the appointment outcome. Provider no-show, cancellation and rescheduling never count as resident no-access.',
    outcome: 'Select the observed exercise outcome. A returned quality result requires new reinspection evidence.',
    decision: 'Resident choice for this home only. Contact or access is never consent; withdrawal remains recordable after scheduling.',
    measure: 'Exact single-home measure identifier from case facts. Shared buildings do not share resident consent.',
    target: 'Explicit recovery stage. Coordinator returns to assessed; quality reviewer returns to installed.',
    value: 'Sourced resolution of the conflicting stock fact. Unknown values never satisfy a gate.',
    matched: 'Synthetic invoice-match observation only. This does not issue a payment.',
    state: 'Ordered exercise grant state. This application does not submit a claim or move money.',
    budgetApproved: 'Finance exercise decision only; not an operational investment approval.',
    fundingConfirmed: 'Finance exercise confirmation only; not a real grant award.',
    contractApproved: 'Finance exercise decision only; no instruction is sent to a supplier.',
  };

  function node(tag, className, text) {
    const item = document.createElement(tag);
    if (className) item.className = className;
    if (text !== undefined && text !== null) item.textContent = String(text);
    return item;
  }
  function clear(element) { element.replaceChildren(); return element; }
  function human(value) { return String(value ?? 'Not recorded').replaceAll('_', ' ').replace(/([a-z])([A-Z])/g, '$1 $2'); }
  function display(value) {
    if (value === null || value === undefined || value === '') return 'Not recorded';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    return String(value);
  }
  function workflowLabel(id) { return state.config?.workflows.find((item) => item.id === id)?.label ?? human(id); }
  function announce(message) { $('status').textContent = message; }
  function structured(value, depth = 0) {
    if (depth > 7) return node('pre', '', JSON.stringify(value, null, 2));
    if (Array.isArray(value)) {
      if (!value.length) return node('span', 'empty-inline', 'None recorded');
      const list = node('ul', 'data-array');
      value.forEach((entry) => { const li = node('li'); li.append(structured(entry, depth + 1)); list.append(li); });
      return list;
    }
    if (value && typeof value === 'object') {
      const entries = Object.entries(value);
      if (!entries.length) return node('span', 'empty-inline', 'No fields recorded');
      const grid = node('dl', 'data-grid');
      entries.forEach(([key, entry]) => {
        grid.append(node('dt', '', human(key)));
        const dd = node('dd');
        dd.append(structured(entry, depth + 1));
        grid.append(dd);
      });
      return grid;
    }
    return node('span', '', display(value));
  }
  function errorInfo(error) {
    return error.data?.error ?? {
      code: error.code ?? 'TRANSPORT_UNCERTAIN',
      message: error.message || 'The local API did not return a usable response.',
      owner: 'Local demo operator',
    };
  }
  function showError(error, recovery) {
    const info = errorInfo(error);
    const panel = clear($('error-panel'));
    panel.hidden = false;
    panel.append(node('h2', '', `${info.code}: ${info.message}`));
    panel.append(node('p', '', `Recovery owner: ${display(info.owner)}.`));
    panel.append(node('p', '', recovery ?? 'Review the case facts and blockers with the named owner. Correct the sourced payload or switch the local simulated role, then submit a new intent against the current version.'));
    if (info.details) panel.append(structured(info.details));
    if (error.data?.requestId) panel.append(node('p', 'mono', `Request ID: ${error.data.requestId}`));
    const refresh = node('button', 'button secondary', state.config ? 'Refresh current evidence' : 'Retry connection');
    refresh.type = 'button';
    refresh.addEventListener('click', () => state.config ? refreshAll() : initialise());
    panel.append(refresh);
    announce(`${info.code}. Owner: ${display(info.owner)}. ${recovery ?? 'Review visible recovery instructions.'}`);
  }
  function clearError() { $('error-panel').hidden = true; clear($('error-panel')); }

  async function api(path, { method = 'GET', body, role = state.role } = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(path, {
        method, headers: { 'x-demo-role': role, ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}) },
        body: body === undefined ? undefined : typeof body === 'string' ? body : JSON.stringify(body),
        signal: controller.signal, cache: 'no-store',
      });
      let data;
      try { data = await response.json(); }
      catch {
        const error = new Error('The API response was not readable JSON. A write may already have committed.');
        error.ambiguous = true;
        throw error;
      }
      if (!response.ok) {
        const error = new Error(data.error?.message ?? `API returned HTTP ${response.status}`);
        error.data = data;
        error.status = response.status;
        error.ambiguous = response.status >= 500;
        throw error;
      }
      return data;
    } catch (error) {
      if (!error.status) error.ambiguous = true;
      throw error;
    } finally { clearTimeout(timer); }
  }
  function filterParams() {
    const params = new URLSearchParams();
    if (state.workflow) params.set('workflow', state.workflow);
    if (state.query) params.set('q', state.query);
    return params.size ? `?${params}` : '';
  }

  function renderNavigation() {
    const nav = clear($('workflow-nav'));
    [{ id: '', label: 'All workflows' }, ...state.config.workflows].forEach((workflow, index) => {
      const button = node('button', 'workflow-button');
      button.type = 'button';
      button.setAttribute('aria-current', state.workflow === workflow.id ? 'page' : 'false');
      button.append(node('span', 'workflow-number', String(index).padStart(2, '0')), node('span', '', workflow.label));
      button.addEventListener('click', () => {
        state.workflow = workflow.id;
        state.drill = null;
        renderNavigation();
        loadCases();
      });
      nav.append(button);
    });
  }
  function metricFallback() {
    const total = state.cases.length;
    const count = (id, label, predicate) => {
      const ids = state.cases.filter(predicate).map((item) => item.id);
      return { id, label, numerator: ids.length, denominator: total, value: ids.length, caseIds: ids };
    };
    return [
      count('homes', 'Homes in scope', () => true),
      count('blocked', 'With recorded blockers', (item) => item.blockers?.length > 0),
      count('handoff', 'With a handoff record', (item) => Boolean(item.handoff)),
      count('complete', 'At handed over stage', (item) => item.stage === 'handed_over'),
    ];
  }
  function renderMetrics() {
    const apiMetrics = state.portfolio?.metrics;
    const supplied = Array.isArray(apiMetrics) && apiMetrics.length > 0;
    const metrics = supplied ? apiMetrics : metricFallback();
    const cards = clear($('metric-cards'));
    metrics.forEach((metric, index) => {
      const id = String(metric.id ?? index);
      const label = metric.label ?? human(id);
      const button = node('button', 'metric-card');
      button.type = 'button';
      const canDrill = Array.isArray(metric.caseIds);
      button.disabled = !canDrill;
      button.setAttribute('aria-pressed', String(state.drill?.id === id));
      button.setAttribute('aria-label', `${label}: ${display(metric.value ?? metric.numerator)}. ${canDrill ? 'Inspect contributing homes.' : 'No contributing case IDs supplied.'}`);
      button.append(
        node('span', 'metric-label', label),
        node('span', 'metric-value', display(metric.value ?? metric.numerator)),
        node('span', 'metric-denominator', `Numerator ${display(metric.numerator)} / denominator ${display(metric.denominator)}`),
      );
      button.addEventListener('click', () => {
        state.drill = state.drill?.id === id ? null : { id, label, ids: new Set(metric.caseIds) };
        renderMetrics();
        renderCases();
        announce(state.drill ? `${label}: displaying its exact contributing cohort within the current search and workflow.` : 'Metric drilldown cleared.');
      });
      cards.append(button);
    });
    $('as-of').textContent = `AS OF ${display(state.portfolio?.asOf ?? state.asOf)}`;
    $('metric-note').textContent = `${supplied ? 'API-reported metrics' : 'UI-derived case counts'} for exactly the active workflow/search set (${state.cases.length} synthetic homes). Numerators and denominators are explicit; metric selection narrows only the home register, not the base denominator. No throughput, savings or operational performance is inferred.`;
    const details = $('portfolio-details');
    details.hidden = false;
    const output = clear($('portfolio-data'));
    output.append(structured(state.portfolio ?? { scope: state.scope, asOf: state.asOf, synthetic: true, note: 'Portfolio unavailable; displayed counts derived only from fetched cases.' }));
  }
  function renderCases() {
    const items = state.drill ? state.cases.filter((item) => state.drill.ids.has(item.id)) : state.cases;
    $('case-count').textContent = `${items.length} / ${state.cases.length}`;
    $('queue-title').textContent = state.workflow ? workflowLabel(state.workflow) : 'Home register';
    $('filter-summary').textContent = `${state.workflow ? workflowLabel(state.workflow) : 'All workflows'}${state.query ? ` / "${state.query}"` : ''}`;
    $('drilldown').hidden = !state.drill;
    $('drilldown-label').textContent = state.drill ? `Cohort: ${state.drill.label}` : '';
    const list = clear($('case-list'));
    if (!items.length) {
      list.append(node('p', 'empty-state', 'No homes match this cohort. Reset filters or clear the metric to widen the view.'));
      return;
    }
    items.forEach((item) => {
      const button = node('button', 'case-row');
      button.type = 'button';
      button.setAttribute('aria-pressed', String(state.selectedId === item.id));
      button.setAttribute('aria-label', `${item.homeId}, ${human(item.stage)}, owner ${human(item.owner)}, version ${item.version}. Open case.`);
      const heading = node('span', 'row-heading');
      heading.append(node('span', '', item.homeId), node('span', 'chip', `v${item.version}`));
      button.append(heading, node('span', 'row-meta', `${item.buildingId} / ${workflowLabel(item.workflow)}`));
      button.append(node('span', 'chip stage', human(item.stage)));
      if (item.blockers?.length) button.append(node('span', 'chip blocked', `${item.blockers.length} blocker${item.blockers.length === 1 ? '' : 's'}`));
      button.append(node('span', 'row-meta', `Owner: ${human(item.owner)}`));
      if (item.blockers?.[0]) button.append(node('span', 'row-blocker', `${item.blockers[0].message} / ${human(item.blockers[0].owner)}`));
      button.addEventListener('click', () => selectCase(item.id, true));
      list.append(button);
    });
  }

  async function loadCases() {
    if (!state.config) return;
    const token = ++state.listRequest;
    const role = state.role;
    const params = filterParams();
    $('case-list').setAttribute('aria-busy', 'true');
    announce('Loading the filtered synthetic cohort...');
    const [casesResult, portfolioResult] = await Promise.allSettled([
      api(`/api/cases${params}`, { role }), api(`/api/portfolio${params}`, { role }),
    ]);
    if (token !== state.listRequest) return;
    $('case-list').setAttribute('aria-busy', 'false');
    if (casesResult.status === 'rejected') {
      state.cases = [];
      state.portfolio = null;
      clear($('metric-cards'));
      $('as-of').textContent = 'Snapshot unavailable';
      $('portfolio-details').hidden = true;
      $('metric-note').textContent = 'No usable case snapshot. No metrics inferred from stale data.';
      state.asOf = null;
      state.scope = null;
      state.drill = null;
      renderCases();
      showError(casesResult.reason, 'The cohort could not be loaded. Check the local API, then refresh. No case was changed.');
      return;
    }
    const data = casesResult.value;
    if (!Array.isArray(data.cases)) {
      showError(new Error('Case list contract mismatch: expected {cases,scope,asOf}.'));
      return;
    }
    state.cases = data.cases;
    state.scope = data.scope;
    state.asOf = data.asOf;
    state.portfolio = portfolioResult.status === 'fulfilled' ? portfolioResult.value : null;
    state.drill = null;
    renderMetrics();
    renderCases();
    announce(`Loaded ${state.cases.length} synthetic homes. ${portfolioResult.status === 'rejected' ? 'Portfolio unavailable; counts are derived from these homes only.' : 'Metrics share the same filters.'}`);
    if (portfolioResult.status === 'rejected') showError(portfolioResult.reason, 'Portfolio metrics could not be loaded. Case-count fallback uses only the fetched cohort. Refresh to retry the portfolio API.');
    if (!state.selectedId && state.cases.length) await selectCase(state.cases[0].id);
  }

  function panel(title, value, full = false) {
    const section = node('section', `detail-panel${full ? ' full' : ''}`);
    section.append(node('h3', '', title), structured(value));
    return section;
  }
  function recordPanel(title, records, emptyText, full = false) {
    const section = node('section', `detail-panel${full ? ' full' : ''}`);
    section.append(node('h3', '', title));
    if (!Array.isArray(records) || !records.length) section.append(node('p', 'empty-inline', emptyText));
    else {
      const list = node('ul', 'record-list');
      records.forEach((record) => { const li = node('li'); li.append(structured(record)); list.append(li); });
      section.append(list);
    }
    return section;
  }
  function renderDetail(focus = false) {
    const item = state.detail;
    if (!item) return;
    const root = clear($('case-detail'));
    const header = node('header', 'detail-header');
    header.append(node('span', 'eyebrow', '03 / HOME CASE FILE'));
    const titleRow = node('div', 'detail-title-row');
    const title = node('h2', '', item.homeId);
    title.id = 'detail-heading';
    title.tabIndex = -1;
    titleRow.append(title, node('span', 'version mono', `CASE VERSION ${item.version}`));
    header.append(titleRow, node('p', 'detail-identifiers mono', `Case ${item.id} / Building ${item.buildingId} / Scheme ${item.schemeId}`));
    header.append(node('p', 'help', 'Selected case detail is independent of the home-register filters.'));
    root.append(header);
    const owner = node('div', 'owner-strip');
    owner.append(node('strong', '', `Current owner: ${human(item.owner)}`), node('span', '', workflowLabel(item.workflow)));
    root.append(owner);
    const body = node('div', 'detail-body');
    body.append(node('h3', '', 'Lifecycle / controlled progression'));
    body.append(node('p', 'help', 'Stage reflects the current record, not proof that every future gate is satisfied. Historical observations are retained after a return.'));
    const lifecycle = node('ol', 'lifecycle');
    lifecycle.setAttribute('aria-label', 'Current lifecycle stage');
    const current = state.config.lifecycle.indexOf(item.stage);
    state.config.lifecycle.forEach((stage, index) => {
      const step = node('li', index === current ? 'current' : index < current ? 'passed' : '');
      if (index === current) step.setAttribute('aria-current', 'step');
      step.append(node('span', '', String(index + 1).padStart(2, '0')), node('div', '', `${human(stage)}${index === current ? ' (current)' : ''}`));
      lifecycle.append(step);
    });
    body.append(lifecycle);
    const grid = node('div', 'detail-grid');
    const blockers = node('section', 'detail-panel full');
    blockers.append(node('h3', '', 'What blocks this home'));
    if (item.blockers?.length) {
      const list = node('ul', 'blocker-list');
      item.blockers.forEach((blocker) => {
        const li = node('li');
        li.append(node('code', '', blocker.code), node('p', '', blocker.message), node('p', 'help', `Recovery owner: ${human(blocker.owner)}`));
        list.append(li);
      });
      blockers.append(list);
    } else blockers.append(node('p', 'empty-inline', 'No blockers currently reported. Server predicates still apply to every command.'));
    grid.append(blockers, panel('Resident-update commitment', item.residentUpdate), panel('Handoff / ownership continuity', item.handoff));
    const handoffNote = node('p', 'help', 'Sent, received and accepted are distinct. The case owner transfers only on acceptance; the resident-update owner does not transfer.');
    grid.lastChild.append(handoffNote);
    grid.append(recordPanel('Versioned evidence', item.evidence, 'No evidence recorded.', true));
    grid.append(panel('Current facts / gate inputs', item.facts, true));
    grid.append(recordPanel('Owned manual tasks', item.tasks, 'No manual tasks recorded.'), recordPanel('Appointment observations', item.appointments, 'No appointment observations recorded.'));
    body.append(grid);
    body.append(commandSection(item), assistantSection(item), auditSection(item));
    root.append(body);
    if (focus) title.focus();
  }

  async function selectCase(id, focus = false) {
    const token = ++state.detailRequest;
    const role = state.role;
    state.selectedId = id;
    state.detail = null;
    renderCases();
    const root = clear($('case-detail'));
    root.setAttribute('aria-busy', 'true');
    const loading = node('div', 'detail-placeholder');
    const title = node('h2', '', 'Loading case evidence...');
    title.id = 'detail-heading';
    loading.append(title);
    root.append(loading);
    try {
      const item = await api(`/api/cases/${encodeURIComponent(id)}`, { role });
      if (token !== state.detailRequest) return;
      if (item.id !== id || !Array.isArray(item.allowedActions)) throw new Error('Case detail contract mismatch: expected a direct case object with allowedActions.');
      state.detail = item;
      renderDetail(focus);
      announce(`Home ${item.homeId}, version ${item.version}. Current owner: ${human(item.owner)}.`);
    } catch (error) {
      if (token !== state.detailRequest) return;
      const placeholder = clear(root);
      const empty = node('div', 'detail-placeholder');
      const title = node('h2', '', 'Case unavailable');
      title.id = 'detail-heading';
      empty.append(title, node('p', '', 'Refresh to retrieve current evidence. No action is available without a current case snapshot.'));
      placeholder.append(empty);
      showError(error, 'Case evidence could not be loaded. Refresh before attempting a command; no speculative case state is displayed.');
    } finally {
      if (token === state.detailRequest) root.setAttribute('aria-busy', 'false');
    }
  }

  function commandSection(item) {
    const section = node('section', 'command-section');
    section.append(node('h3', '', 'Record a sourced exercise action'));
    section.append(node('p', 'section-caption', 'Role authority makes an action available, not safe to advance. The server checks continuing consent, safety, evidence and stage predicates. Rejections stay visible with an owner and recovery.'));
    const allowed = state.config.commands.filter((command) => item.allowedActions.includes(command.action));
    if (!allowed.length) {
      section.append(node('p', 'empty-inline', `No commands for the simulated ${human(state.role)} role. Switch the local role selector to explore other exercise authorities.`));
      return section;
    }
    const form = node('form', 'command-form');
    form.id = 'command-form';
    const fieldset = node('fieldset', 'command-fieldset');
    fieldset.disabled = Boolean(state.pending || state.writing || state.assistantBusy);
    const label = node('label', '', 'Exercise action');
    label.htmlFor = 'command-action';
    const select = node('select');
    select.id = 'command-action';
    allowed.forEach((command) => {
      const option = node('option', '', command.label);
      option.value = command.action;
      select.append(option);
    });
    fieldset.append(label, select);
    const fields = node('div', 'command-fields');
    fieldset.append(fields);
    const footer = node('div', 'command-footer');
    footer.append(node('span', 'mono', `Expected case version: ${item.version}`));
    const submit = node('button', 'button', 'Submit exercise command');
    submit.type = 'submit';
    footer.append(submit);
    fieldset.append(footer);
    form.append(fieldset);
    function selectedCommand() { return allowed.find((command) => command.action === select.value); }
    function formFields() {
      const descriptors = [...(selectedCommand()?.fields ?? [])];
      ['reason', 'source'].forEach((key) => {
        if (!descriptors.some((descriptor) => descriptor.key === key)) descriptors.push({ key, type: 'string' });
      });
      return descriptors;
    }
    function renderFields() {
      clear(fields);
      formFields().forEach((field) => fields.append(commandField(field, item)));
    }
    select.addEventListener('change', renderFields);
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (state.pending || state.writing || state.assistantBusy) return;
      const payload = {};
      for (const field of formFields()) {
        const input = form.elements.namedItem(field.key);
        if (field.type === 'boolean') payload[field.key] = input.checked;
        else if (['number', 'integer'].includes(field.type)) payload[field.key] = Number(input.value);
        else payload[field.key] = input.value.trim();
      }
      const request = { action: select.value, expectedVersion: item.version, idempotencyKey: crypto.randomUUID(), payload };
      state.pending = { caseId: item.id, role: state.role, request, body: JSON.stringify(request), uncertain: false };
      runPendingCommand();
    });
    renderFields();
    section.append(form);
    return section;
  }
  function commandField(field, item) {
    const key = field.key;
    const wide = ['reason', 'source'].includes(key);
    const group = node('div', `field-group${wide ? ' wide' : ''}`);
    const label = node('label', '', human(key).replace(/^./, (character) => character.toUpperCase()));
    const id = `payload-${key}`;
    label.htmlFor = id;
    label.append(node('code', '', `payload.${key} / ${field.type}`));
    let input;
    if (field.type === 'boolean') {
      input = node('input');
      input.type = 'checkbox';
      input.checked = field.default === true;
      label.className = 'boolean-label';
      label.prepend(input);
      group.append(label);
    } else {
      if (Array.isArray(field.options)) {
        input = node('select');
        field.options.forEach((entry) => {
          const value = typeof entry === 'object' ? entry.value : entry;
          const option = node('option', '', typeof entry === 'object' ? entry.label ?? human(value) : human(value));
          option.value = value;
          input.append(option);
        });
      } else if (key === 'reason') {
        input = node('textarea');
        input.rows = 3;
      } else {
        input = node('input');
        input.type = ['number', 'integer'].includes(field.type) ? 'number' : 'text';
        if (input.type === 'number') {
          input.step = field.type === 'integer' ? '1' : 'any';
          input.min = ['designVersion', 'packageVersion', 'slots'].includes(key) ? '1' : '0';
        }
      }
      input.required = true;
      if (field.default !== undefined && field.default !== null) input.value = String(field.default);
      if (key === 'handoffId' && item.handoff?.id) input.value = item.handoff.id;
      if (key === 'designVersion' && item.facts?.design?.version) input.value = String(item.facts.design.version);
      if (key === 'packageVersion' && item.facts?.package?.version) input.value = String(item.facts.package.version);
      if (key === 'source') input.placeholder = 'exercise:source-reference';
      if (key === 'dueAt') input.placeholder = '2026-10-08T16:00:00Z';
      group.append(label, input);
    }
    input.id = id;
    input.name = key;
    const help = node('small', 'help', fieldHelp[key] ?? 'Required action-specific value. Inspect the current case facts and supply a sourced synthetic observation.');
    help.id = `${id}-help`;
    input.setAttribute('aria-describedby', help.id);
    group.append(help);
    return group;
  }

  function updateWriteLocks() {
    const locked = Boolean(state.pending || state.writing || state.assistantBusy);
    $('demo-role').disabled = !state.config || locked;
    const form = $('command-form');
    if (form) form.querySelector('fieldset').disabled = locked;
    const assistant = $('assistant-submit');
    if (assistant) assistant.disabled = locked;
  }
  function renderPending() {
    const root = clear($('pending-panel'));
    const pending = state.pending;
    root.hidden = !pending;
    if (!pending) return;
    root.append(node('h2', '', pending.uncertain ? 'Outcome unknown / preserve the original intent' : 'Awaiting server commit'));
    root.append(node('p', '', `Case ${pending.caseId}. Simulated actor: ${human(pending.role)}. Expected version: ${pending.request.expectedVersion}.`));
    root.append(node('p', 'mono', `Idempotency key: ${pending.request.idempotencyKey}`));
    root.append(node('p', '', 'This exact request, role and key are retained in this tab. Do not close or reload before reconciliation. No success is inferred, and no new key is silently generated.'));
    const details = node('details');
    details.append(node('summary', '', 'Inspect retained request'), node('pre', '', pending.body));
    root.append(details);
    if (pending.uncertain) {
      const retry = node('button', 'button', 'Retry exact retained request');
      retry.type = 'button';
      retry.disabled = state.writing;
      retry.addEventListener('click', runPendingCommand);
      root.append(retry);
    }
  }
  async function runPendingCommand() {
    const pending = state.pending;
    if (!pending || state.writing) return;
    state.writing = true;
    clearError();
    renderPending();
    updateWriteLocks();
    announce('Submitting retained intent. Waiting for a committed API response...');
    let outcome = null;
    try {
      const response = await api(`/api/cases/${encodeURIComponent(pending.caseId)}/commands`, { method: 'POST', body: pending.body, role: pending.role });
      if (!response.case || typeof response.replayed !== 'boolean') {
        const error = new Error('Command response contract mismatch. Its commit status cannot be confirmed.');
        error.ambiguous = true;
        throw error;
      }
      outcome = response;
      state.pending = null;
    } catch (error) {
      if (error.ambiguous) {
        pending.uncertain = true;
        showError(error, 'Do not submit a new intent. Retry the exact retained request with its original role, version and idempotency key. The server will replay a committed intent; current detail is fetched afterwards.');
      } else {
        state.pending = null;
        showError(error, error.status === 409 ? 'The intent was rejected. Refresh current evidence, inspect version or idempotency conflict details, and correct the intent before a new submission. There is no automatic version override.' : undefined);
      }
    } finally {
      state.writing = false;
      renderPending();
      updateWriteLocks();
    }
    if (!state.pending) {
      state.assistant = null;
      await selectCase(pending.caseId, true);
      await loadCases();
      if (outcome) announce(`${outcome.replayed ? 'Original committed intent replayed' : 'Exercise command committed'}. Current detail refetched; displayed version ${state.detail?.version ?? 'unavailable'}. No operational approval or external action is implied.`);
    }
  }

  function assistantSection(item) {
    const section = node('section', 'assistant-section');
    section.append(node('h3', '', 'Evidence desk / bounded draft assistant'));
    section.append(node('p', 'section-caption', 'Offline deterministic simulator, not an evaluated model. Cited drafts are not approvals, consent, submissions or supplier instructions. It cannot execute a case command or clear a hazard.'));
    const form = node('form', 'assistant-controls');
    const field = node('div');
    const label = node('label', '', 'Simulator mode');
    label.htmlFor = 'assistant-mode';
    const mode = node('select');
    mode.id = 'assistant-mode';
    [
      ['draft', 'Cited draft / no execution'],
      ['disabled', 'Disabled / owned manual fallback'],
      ['failure', 'Failure / owned manual fallback'],
    ].forEach(([value, text]) => { const option = node('option', '', text); option.value = value; mode.append(option); });
    field.append(label, mode);
    const submit = node('button', 'button secondary', 'Run simulator');
    submit.id = 'assistant-submit';
    submit.type = 'submit';
    submit.disabled = Boolean(state.pending || state.writing || state.assistantBusy);
    form.append(field, submit);
    form.addEventListener('submit', (event) => { event.preventDefault(); runAssistant(item.id, mode.value); });
    section.append(form);
    const output = node('div', 'assistant-output');
    if (state.assistant && state.assistantCaseId === item.id) {
      output.append(node('h3', '', `${display(state.assistant.mode)} / ${display(state.assistant.status)}`));
      if (state.assistant.error) output.append(panel('Explicit simulator error', state.assistant.error));
      if (state.assistant.draft) {
        output.append(node('h3', '', 'Draft only / human review required'), node('p', 'draft-text', state.assistant.draft));
      }
      ['citations', 'findings', 'prohibitedActions'].forEach((key) => {
        output.append(node('h3', '', human(key)), structured(state.assistant[key]));
      });
      Object.entries(state.assistant).filter(([key]) => !['mode', 'status', 'draft', 'error', 'citations', 'findings', 'prohibitedActions'].includes(key)).forEach(([key, value]) => {
        output.append(node('h3', '', human(key)), structured(value));
      });
    } else output.append(node('p', 'empty-inline', 'No draft generated. Failure and disabled modes must report an explicit owned fallback, not fabricated completion.'));
    section.append(output);
    return section;
  }
  async function runAssistant(id, mode) {
    if (state.assistantBusy || state.pending || state.writing) return;
    state.assistantBusy = true;
    state.assistant = null;
    clearError();
    updateWriteLocks();
    announce(`Running ${mode} mode. Simulator output is never an approval.`);
    let result;
    let failure;
    try {
      result = await api(`/api/cases/${encodeURIComponent(id)}/assistant`, { method: 'POST', body: { mode } });
      state.assistant = result;
      state.assistantCaseId = id;
    } catch (error) {
      failure = error;
    } finally {
      state.assistantBusy = false;
      updateWriteLocks();
    }
    await selectCase(id);
    await loadCases();
    if (failure) showError(failure, 'Simulator did not return a draft. Inspect the refreshed owned manual tasks and audit; no approval or progression is claimed. If the transport failed, check history before running it again.');
    else if (result.error || ['error', 'failed', 'failure', 'disabled'].includes(result.status)) {
      showError({ data: { error: result.error ?? { code: 'SIMULATOR_UNAVAILABLE', message: `Simulator status: ${result.status}.`, owner: result.owner ?? state.detail?.owner ?? 'Local demo operator' } } }, 'No draft completion is claimed. Continue through the owned manual-review task visible in the current case.');
    } else announce('Cited simulator draft available for human review only. No case approval or external action performed.');
  }
  function auditSection(item) {
    const section = node('section', 'audit-section');
    section.append(node('h3', '', 'Audit / committed history'));
    section.append(node('p', 'section-caption', 'Persistent local exercise events, not production-grade immutable evidence. Export retains the API evidence and versions.'));
    if (!item.events?.length) {
      section.append(node('p', 'empty-inline', 'No events recorded.'));
      return section;
    }
    const list = node('ol', 'audit-list');
    [...item.events].reverse().forEach((event) => {
      const li = node('li');
      li.append(node('p', 'event-heading', human(event.action ?? 'Event')), structured(event));
      list.append(li);
    });
    section.append(list);
    return section;
  }

  async function refreshAll() {
    if (!state.config) return initialise();
    if (state.selectedId) await selectCase(state.selectedId);
    await loadCases();
  }
  async function exportJSON() {
    const button = $('export-button');
    button.disabled = true;
    try {
      const data = await api('/api/export');
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = node('a');
      link.href = url;
      link.download = `proper-warm-synthetic-audit-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      announce('Synthetic audit JSON downloaded. Local versions, evidence and events preserved; no production immutability or privacy guarantee.');
    } catch (error) { showError(error, 'Export failed. Refresh the local API and retry; no file content was fabricated.'); }
    finally { button.disabled = !state.config; }
  }
  async function initialise() {
    clearError();
    announce('Connecting to the local API configuration...');
    try {
      const config = await api('/api/config');
      if (!Array.isArray(config.roles) || !Array.isArray(config.workflows) || !Array.isArray(config.lifecycle) || !Array.isArray(config.commands)) {
        throw new Error('Configuration contract mismatch. Expected roles, workflows, lifecycle and command field schemas.');
      }
      state.config = config;
      const roleSelect = clear($('demo-role'));
      config.roles.forEach((role) => { const option = node('option', '', human(role)); option.value = role; roleSelect.append(option); });
      if (!config.roles.includes(state.role)) state.role = config.roles[0];
      roleSelect.value = state.role;
      roleSelect.disabled = false;
      $('simulation-banner').textContent = `${typeof config.banner === 'string' ? config.banner : JSON.stringify(config.banner)} Local role selection is simulation, not authentication. Synthetic reads/export are intentionally unrestricted, not field-level privacy. No external action or operational approval.`;
      $('export-button').disabled = false;
      renderNavigation();
      await loadCases();
    } catch (error) {
      showError(error, 'Start or inspect the local demonstrator API, then retry connection. No remote fallback, invented metrics or speculative actions are shown.');
    }
  }
  $('search-form').addEventListener('submit', (event) => {
    event.preventDefault();
    state.query = $('search').value.trim();
    state.drill = null;
    loadCases();
  });
  $('reset-button').addEventListener('click', () => {
    state.query = '';
    state.workflow = '';
    state.drill = null;
    $('search').value = '';
    if (state.config) renderNavigation();
    loadCases();
  });
  $('clear-drilldown').addEventListener('click', () => {
    state.drill = null;
    renderMetrics();
    renderCases();
    announce('Metric drilldown cleared. Workflow and search filters retained.');
  });
  $('demo-role').addEventListener('change', async (event) => {
    if (state.pending || state.writing || state.assistantBusy) return;
    state.role = event.target.value;
    state.assistant = null;
    clearError();
    await refreshAll();
    announce(`Local ${human(state.role)} role simulation, not authentication. Current case authority refreshed from the server.`);
  });
  $('export-button').addEventListener('click', exportJSON);
  window.addEventListener('beforeunload', (event) => {
    if (state.pending) { event.preventDefault(); event.returnValue = ''; }
  });
  initialise();
})();
