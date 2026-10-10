"use strict";

function exerciseTable(rows, caption) {
  if (!rows.length) return h("p", {}, `${caption}: no supplied rows.`);
  const keys = Object.keys(rows[0]);
  return h("div", { class: "exercise-table", role: "region", "aria-label": caption, tabindex: "0" }, h("table", {},
    h("caption", {}, caption), h("thead", {}, h("tr", {}, keys.map((key) => h("th", { scope: "col" }, key)))),
    h("tbody", {}, rows.map((row) => h("tr", {}, keys.map((key) => h("td", {}, typeof row[key] === "object" ? JSON.stringify(row[key]) : row[key])))))));
}

function exerciseDownload(snapshot, name, label = "Download reviewed JSON (not submitted)") {
  const url = URL.createObjectURL(new Blob([JSON.stringify(snapshot, null, 2)], { type: "application/json" }));
  const link = h("a", { href: url, download: name }, label);
  link.addEventListener("click", () => setTimeout(() => URL.revokeObjectURL(url), 1000), { once: true });
  return link;
}

async function exerciseView(caseId) {
  const requestedRoute = location.hash;
  try {
    const status = await api("/api/exercise");
    const banner = h("section", { class: "card", role: "status" },
      h("h1", {}, "Proper Warm fictional exercise"),
      h("p", {}, "No live resident contact, safety judgement, submission or payment. Perspectives never change your signed-in authority."),
      h("p", {}, `${status.fixture_version}. ${status.inference} ${status.budget}`),
      h("p", {}, status.validation));
    const profiles = h("section", { class: "card" }, h("h2", {}, "Eleven perspectives"),
      h("ul", {}, status.profiles.map((profile) => h("li", {},
        `${profile.name}: ${profile.role === me.user.role ? "Matching role; actions still require independence." : "Access restricted; sign in with that role to act."} `,
        profile.script.next_action))));
    const links = h("section", { class: "card" }, h("h2", {}, "Story homes (not the forecast cohort)"),
      status.stories.map((story) => h("article", {},
        h("h3", {}, h("a", { href: `#/exercise/${story.id}` }, story.id)),
        h("p", {}, `${story.lifecycle}. Owner: ${story.owner}. Next: ${story.next_action}`),
        h("ul", {}, story.blockers.map((blocker) => h("li", {}, blocker))))));
    if (caseId) {
      const data = await api(`/api/cases/${encodeURIComponent(caseId)}/exercise`);
      const home = await exerciseHome(caseId, data);
      if (location.hash === requestedRoute) show(banner, links, home);
      return;
    }
    const workflows = h("section", { class: "card" }, h("h2", {}, "Nine connected workflows"),
      status.workflows.map((workflow) => h("article", {},
        h("h3", {}, workflow.name), h("p", {}, `Owner: ${workflow.owner}. Expected: ${workflow.expected}`),
        workflow.id === "portfolio"
          ? h("button", { class: "alt", onclick: () => { const table = document.getElementById("exercise-forecast"); table.scrollIntoView(); table.focus(); } }, "Open forecast tables")
          : h("a", { href: workflow.id === "procurement" ? "#/capacity" : "#/exercise/EX-HOME-001" }, "Open relevant work"),
        h("p", {}, `Script validation: ${workflow.status}`))));
    const forecasts = h("section", { id: "exercise-forecast", class: "card", tabindex: "-1" }, h("h2", {}, "Constructed forecast, not live outcomes"),
      Object.entries(status.forecast).map(([name, result]) => h("details", {}, h("summary", {}, `${name}: ${result.status}`),
        h("p", {}, `As of ${result.as_of}; denominator ${result.denominator}; source versions ${JSON.stringify(result.source_versions)}. Held dates unknown; independent installation and QA pools.`),
        exerciseTable(result.tables.weekly, `${name} weekly forecast`),
        h("pre", {}, JSON.stringify({ coverage: result.coverage, unknowns: result.unknowns, exclusions: result.exclusions }, null, 2)))),
      h("h3", {}, "Separate stakeholder analytical snapshot"),
      h("p", {}, JSON.stringify(status.analytical)));
    const dataPanel = await exerciseDataPanel();
    if (location.hash === requestedRoute) show(banner, profiles, links, workflows, forecasts, dataPanel);
  } catch (error) {
    if (location.hash === requestedRoute) show(h("h1", {}, "Exercise unavailable"), h("p", { role: "alert" }, error.message));
  }

  async function exerciseDataPanel() {
    const card = h("section", { class: "card" }, h("h2", {}, "Exercise data portability"),
      h("p", {}, "Read-only JSON export. Uploads change only unverified coordination notes and task due dates after an explicit preview and commit. Owners, stock, consent, safety and finance remain unchanged."));
    const output = h("div", {});
    const status = h("p", { role: "status", "aria-live": "polite", tabindex: "-1" });
    card.append(status, output);
    let snapshot;
    try {
      snapshot = await api("/api/exercise/data");
      output.append(exerciseDownload(snapshot, "exercise-permitted-data.json", "Download all permitted case and history JSON"));
    } catch (error) {
      status.textContent = error.message;
      return card;
    }
    if (!["Retrofit Programme Manager", "Programme Support Officer"].includes(me.user.role)) {
      card.append(h("p", {}, "Import and bulk changes require Programme Manager or Programme Support authority."));
      return card;
    }
    const previewOutput = h("div", {});
    const reason = h("input", { id: "exercise-data-reason", type: "text", maxlength: 300 });
    card.append(h("label", { for: reason.id }, "Reason for this coordination change"), reason);
    const preview = async (body) => {
      status.textContent = "Validating every selected row...";
      previewOutput.replaceChildren();
      try {
        const result = await api("/api/exercise/data", { ...body, reason: reason.value });
        status.textContent = result.status;
        previewOutput.append(h("pre", {}, JSON.stringify(result, null, 2)));
        if (result.token && result.rows.some((row) => row.status === "ready")) {
          const button = h("button", { onclick: async () => {
            button.disabled = true;
            try {
              const committed = await api("/api/exercise/data", {
                action: "commit", token: result.token, input_hash: result.input_hash,
                expected_fingerprints: Object.fromEntries(result.rows.map((row) => [String(row.row), row.expected_fingerprint])),
              });
              status.textContent = `${committed.committed} committed; ${committed.errors} failed. Every row outcome is below.`;
              previewOutput.replaceChildren(h("pre", {}, JSON.stringify(committed, null, 2)));
              const refreshed = await api("/api/exercise/data");
              output.replaceChildren(exerciseDownload(refreshed, "exercise-permitted-data.json", "Download refreshed all-scope JSON"));
            } catch (error) {
              status.textContent = error.message;
              status.focus();
            }
          } }, "Explicitly commit this exact preview (failed rows are not changed)");
          previewOutput.append(button);
        }
      } catch (error) {
        status.textContent = error.message;
        status.focus();
      }
    };
    const file = h("input", { id: "exercise-data-workbook", type: "file", accept: ".xlsx" });
    const importNote = h("input", { id: "exercise-import-note", type: "checkbox" });
    const importDue = h("input", { id: "exercise-import-due", type: "checkbox" });
    card.append(h("h3", {}, "Declared workbook import"),
      h("p", {}, "Sheet: Case updates. Physical row 1 headers: case_id, coordination_note, task_due_date. Maximum 500 data rows and 5 MiB. Text literals only; formulas require manual correction. Source workbook stays unchanged. Choose fields explicitly."),
      h("label", { for: file.id }, "Upload Case updates .xlsx file"), file,
      importNote, h("label", { for: importNote.id }, "Import coordination_note"),
      importDue, h("label", { for: importDue.id }, "Import task_due_date"),
      h("button", { class: "alt", onclick: async () => {
        const selected = file.files[0];
        if (!selected || selected.size > 5 * 1024 * 1024) {
          status.textContent = "Select an .xlsx workbook of at most 5 MiB.";
          return;
        }
        try {
          const bytes = new Uint8Array(await selected.arrayBuffer());
          let binary = "";
          for (let offset = 0; offset < bytes.length; offset += 8192) {
            binary += String.fromCharCode(...bytes.subarray(offset, offset + 8192));
          }
          await preview({ action: "import-preview", filename: selected.name, workbook_base64: btoa(binary),
            fields: [importNote.checked && "coordination_note", importDue.checked && "task_due_date"].filter(Boolean) });
        } catch (error) {
          status.textContent = error.message;
        }
      } }, "Preview workbook rows"));
    const selections = snapshot.cases.map((row) => {
      const check = h("input", { id: `exercise-bulk-${row.case.id}`, type: "checkbox", value: row.case.id });
      return { check, label: h("label", { for: check.id }, row.case.id) };
    });
    const note = h("textarea", { id: "exercise-bulk-note", maxlength: 300 });
    const due = h("input", { id: "exercise-bulk-due", type: "date" });
    const changeNote = h("input", { id: "exercise-bulk-change-note", type: "checkbox" });
    const changeDue = h("input", { id: "exercise-bulk-change-due", type: "checkbox" });
    card.append(h("h3", {}, "Safe bulk coordination update (at most 25 cases)"),
      h("fieldset", {}, h("legend", {}, "Select exact target case IDs"), selections.flatMap(({ check, label }) => [check, label])),
      changeNote, h("label", { for: changeNote.id }, "Change coordination note"),
      h("label", { for: note.id }, "Explicit coordination note (maximum 300 characters)"), note,
      changeDue, h("label", { for: changeDue.id }, "Change task due date"),
      h("label", { for: due.id }, "Task due date"), due,
      h("button", { class: "alt", onclick: () => preview({ action: "bulk-preview",
        case_ids: selections.filter(({ check }) => check.checked).map(({ check }) => check.value),
        changes: { ...(changeNote.checked ? { coordination_note: note.value } : {}),
          ...(changeDue.checked ? { task_due_date: due.value } : {}) } }) }, "Preview selected-case changes"),
      previewOutput);
    return card;
  }
}

async function exerciseBuildingView(id) {
  const requestedRoute = location.hash;
  try {
    const data = await api(`/api/exercise/buildings/${encodeURIComponent(id)}`);
    if (location.hash !== requestedRoute) return;
    show(h("section", { class: "card" }, h("h1", {}, `Building ${data.id}`),
      h("p", {}, `Fictional, as of ${data.as_of}. ${data.note}`),
      h("h2", {}, "Shared building context (not home approval)"),
      exerciseTable([{
        systems: data.shared_systems, works: data.shared_works,
        dependencies: data.shared_dependencies, holds: data.shared_holds, cost: data.shared_cost,
      }], "Separate shared context and explicit unknowns"),
      h("h2", {}, "Independent linked homes"),
      data.homes.map((home) => h("article", {},
        h("h3", {}, h("a", { href: `#/exercise/${home.id}` }, home.id)),
        h("p", {}, `Lifecycle ${home.lifecycle}; owner ${home.case.owner || home.case.named_contact}; package ${home.package_id}; applicability ${home.applicability}.`),
        h("ul", {}, home.blockers.map((blocker) => h("li", {}, blocker))),
        h("details", {}, h("summary", {}, `${home.id} authorized home-specific context`),
          h("pre", {}, JSON.stringify(home.case, null, 2))))),
      h("a", { href: "#/exercise" }, "Return to exercise overview")));
  } catch (error) {
    if (location.hash === requestedRoute) show(h("h1", {}, "Building context unavailable"), h("p", { role: "alert" }, error.message));
  }
}

async function exerciseHome(id, data) {
  const c = data.case;
  const section = h("section", { class: "card" }, h("h2", {}, `${id}: ${data.lifecycle}`),
    h("p", {}, `Owner: ${c.owner || c.named_contact}. Blockers are independent of AI.`),
    h("ul", {}, data.blockers.map((item) => h("li", {}, item))),
    h("a", { href: `#/case/${id}` }, "Existing resident, technical, quality, finance and handoff controls"));
  section.append(h("p", {}, exerciseDownload(data, `${id}-authorized-case-history.json`,
    "Download authorized case, events, decisions and source/version history")));
  section.append(h("a", { href: `#/exercise/building/${data.building_id}` },
    `Open building ${data.building_id} (home gates stay independent)`));
  if (me.user.role === "Contractor") {
    section.append(h("p", {}, "Read assigned scope only. Ask the Programme issuer for release; you cannot review finance or accept work."),
      h("a", { href: "#/" }, "My assigned work"));
    return section;
  }
  const status = h("p", { role: "status", "aria-live": "polite" });
  const send = async (body) => {
    status.textContent = "Saving one action...";
    try {
      await api(`/api/cases/${id}/exercise`, body);
      await exerciseView(id);
    } catch (error) {
      status.textContent = [error.message, ...(error.reasons || [])].join(" ");
      status.setAttribute("role", "alert");
      status.focus();
    }
  };
  status.setAttribute("tabindex", "-1");
  section.append(status);
  const handoff = c.handoff || {};
  section.append(h("section", {},
    h("h3", {}, "Operational handoff: receipt is not acceptance"),
    h("p", {}, `State ${handoff.phase || handoff.state || "Unknown"}; current owner ${c.owner}; destination ${handoff.destination || "Unknown"}; proposed receiver ${handoff.proposed_receiver || "Unknown"}; confirmed receiver ${handoff.confirmed_receiver || "Unknown"}; chase owner ${handoff.chase_owner || "Unknown"}.`),
    h("p", {}, `Due ${handoff.due || "Unknown"}; urgency ${handoff.urgency || "Unknown"}; next action ${handoff.next_action || "Unknown"}; reason ${handoff.answer_note || handoff.note || "Unknown"}.`),
    exerciseTable(handoff.history || [], "Separately evidenced handoff transitions")));
  section.append(h("section", {}, h("h3", {}, "Independently owned resident-update commitments"),
    h("p", {}, "Operational handoffs never clear or reassign these commitments. Sent evidence is not receipt or understanding."),
    exerciseTable(c.exercise && c.exercise.resident_updates || [], "Resident update purpose, owner, due basis and safe-route history")));
  section.append(h("section", {}, h("h3", {}, "Versioned returns and explicit re-review scopes"),
    h("p", {}, "Routing alone does not alter source facts or resident choices. Only named scopes require re-review; historical external events and cash stay recorded."),
    exerciseTable(c.exercise && c.exercise.returns || [], "Return source, initiating authority, receiving owner and next action")));
  if (data.allowed_forms.length) {
    const type = h("select", { id: "exercise-template" }, data.allowed_forms.map((kind) => h("option", { value: kind }, kind)));
    section.append(h("label", { for: "exercise-template" }, "Approved fictional form template"), type,
      h("button", { onclick: () => send({ action: "create-form", form_type: type.value }) }, "Create one draft"));
  }
  section.append(h("details", {}, h("summary", {}, "Authorized source bytes and correction history"),
    data.sources.map((source) => h("article", {}, h("h3", {}, `${source.id} version ${source.version}`),
      h("p", {}, `Authority: ${source.authority}. Media: ${source.media_type}. Source owner: ${source.by}.`),
      h("pre", {}, source.raw_text)))));
  for (const [fid, draft] of Object.entries(data.forms)) {
    const card = h("article", { class: "card" }, h("h3", {}, `${fid} ${draft.form_type} v${draft.input_version}`),
      h("p", {}, `Funding route: ${draft.funding.status}. Field review is not source correction or external approval.`));
    const validation = data.validations[fid];
    card.append(h("p", { role: "status" }, validation.ready ? "Deterministic fields are ready for independent pack review." : "Pack is not ready."),
      h("ul", {}, validation.issues.map((issue) => h("li", {}, `${issue.field_id}: ${issue.reason} (${issue.code})`))));
    const go = (body) => send({ form_id: fid, ...body });
    for (const source of Object.values(draft.sources)) {
      card.append(h("button", { class: "alt", onclick: () => go({ action: "extract", source_id: source.id }) },
        `Parse ${source.id} v${source.version}`));
    }
    for (const [field, value] of Object.entries(draft.fields)) {
      const definition = draft.schema.fields[field];
      const fieldCard = h("details", {}, h("summary", {}, `${field}: ${value.state}${value.stale ? " (needs re-review)" : ""}`),
        h("p", {}, `Reviewed value: ${JSON.stringify(value.value)}. Unit ${value.unit || "none"}; currency ${value.currency || "none"}.`));
      for (const candidate of value.candidates) {
        fieldCard.append(h("p", {}, `${candidate.raw_value}; ${candidate.source_id} v${candidate.source_version}; SHA256 ${candidate.source_hash}; locator ${JSON.stringify(candidate.locator)}${candidate.stale ? "; stale" : ""}`));
        if (!candidate.stale && !definition.protected) fieldCard.append(h("button", { class: "alt",
          onclick: () => go({ action: "select", field, candidate_id: candidate.id }) }, `Select ${field} candidate ${candidate.id.slice(0, 8)}`));
      }
      if (!definition.protected && definition.type !== "calculated_money") fieldCard.append(
        h("button", { class: "alt", onclick: () => go({ action: "select", field, candidate_id: null }) }, `No match for ${field}`),
        h("button", { class: "alt", onclick: () => go({ action: "assist", field }) }, `Optional scoring for ${field} (may be blocked)`));
      if (!definition.protected && definition.type !== "calculated_money") {
        const claim = h("input", { id: `${fid}-${field}-support`, type: "text" });
        fieldCard.append(h("label", { for: claim.id }, "Explicit claim to screen against this field's evidence"),
          claim, h("button", { class: "alt", onclick: () => go({ action: "support", field, claim: claim.value }) },
            `Optional evidence support for ${field} (never approval)`));
      }
      if (definition.type !== "calculated_money") {
        const prefix = `${fid}-${field}`;
        const entered = h("input", { id: `${prefix}-value`, type: "text" });
        const reason = h("input", { id: `${prefix}-reason`, type: "text", required: true });
        const evidence = h("select", { id: `${prefix}-evidence` }, h("option", { value: "" }, "Choose evidence"),
          Object.values(draft.sources).filter((source) => source.field_ids.includes(field)).map((source) => h("option", { value: source.id }, source.id)));
        const review = (action) => {
          let supplied = entered.value;
          try { supplied = JSON.parse(entered.value); } catch (_) { /* Text is a valid manual value. */ }
          return go({ action: definition.protected ? "human-field" : "review", field,
            review_action: action, value: supplied, unit: definition.unit, currency: definition.currency,
            evidence: evidence.value ? [evidence.value] : [], reason: reason.value });
        };
        fieldCard.append(h("label", { for: `${prefix}-value` }, definition.protected ? "Explicit human-only value (never prefilled)" : "Manual correction value (text or JSON)"), entered,
          h("label", { for: `${prefix}-reason` }, "Individual review reason"), reason,
          h("label", { for: `${prefix}-evidence` }, "Same-home evidence"), evidence,
          definition.protected ? h("button", { onclick: () => review("correct") }, `Record human statement for ${field}`) :
            h("div", {}, h("button", { onclick: () => review("accept") }, `Accept selected ${field}`),
              h("button", { onclick: () => review("correct") }, `Correct ${field}`),
              h("button", { class: "alt", onclick: () => review("reject") }, `Reject ${field}`)));
      }
      card.append(fieldCard);
    }
    const packReason = h("input", { id: `${fid}-pack-reason`, type: "text" });
    const packEvidence = h("select", { id: `${fid}-pack-evidence` },
      Object.keys(draft.sources).map((key) => h("option", { value: key }, key)));
    card.append(h("button", { onclick: () => go({ action: "calculate" }) }, "Recalculate deterministic amounts"),
      h("button", { class: "alt", onclick: () => go({ action: "narrative" }) }, "Optional source-bound narrative (not reviewed)"),
      h("label", { for: `${fid}-pack-reason` }, "Independent pack-review reason"), packReason,
      h("label", { for: `${fid}-pack-evidence` }, "Pack review evidence"), packEvidence,
      h("button", { onclick: () => go({ action: "review-pack", evidence: [packEvidence.value], reason: packReason.value }) }, "Review pack with independent identity"),
      h("button", { onclick: () => go({ action: "export" }) }, "Export reviewed pack (not submit)"));
    for (const exported of draft.exports) card.append(exerciseDownload(exported, `${id}-${fid}-${exported.id}.json`));
    section.append(card);
  }
  section.append(exerciseActionEditor(id, data, send),
    h("details", {}, h("summary", {}, "Optional assistance results and source lineage"),
      h("pre", {}, JSON.stringify({ scoring: c.exercise && c.exercise.assistance || [],
        narrative: c.exercise && c.exercise.narratives || [] }, null, 2)),
      (c.exercise && c.exercise.narratives || []).filter((result) => !result.stale && result.approval === "Not reviewed").map((result) => {
        const reason = h("input", { id: `narrative-${result.record_id}-reason`, type: "text" });
        return h("div", {}, h("label", { for: reason.id }, `Review reason for narrative ${result.record_id}`), reason,
          ["accept", "reject"].map((review_action) => h("button", { class: "alt", onclick: () => send({
            action: "review-narrative", form_id: result.form_id, record_id: result.record_id,
            review_action, reason: reason.value }) }, `${review_action} narrative (no field approval)`)));
      }),
      h("p", {}, "Disabled, failed and no-match proposals require manual handling. Not reviewed output never approves a field. Real inference acceptance remains blocked.")),
    h("details", {}, h("summary", {}, "Financial events (export is never submission)"), exerciseTable(data.events, "Separate external fictional evidence")));
  return section;
}

function exerciseActionEditor(id, data, send) {
  const action = h("select", { id: "exercise-record-action" },
    ["lifecycle", "return", "handoff", "source-correct", "versions", "funding-event", "hazard-followup", "external-hazard-reference", "milestone", "resident-update"].map((value) => h("option", { value }, value)));
  const payload = h("textarea", { id: "exercise-record-payload", rows: 8 });
  const error = h("p", { role: "alert" });
  const controls = h("div", {});
  const definitions = {
    lifecycle: [["target", "Next lifecycle step", ["Assessment", "Funding", "Ready", "Installation", "Provider completed", "Independent QA", "Handover", "Financial closure"]]],
    return: [["target", "Earlier exercise stage", ["Intake", "Assessment", "Funding", "Ready", "Installation", "Provider completed", "Independent QA", "Handover"]],
      ["receiver", "Receiving owner email"], ["reason", "Return/reopen reason"], ["evidence", "Source reference"],
      ["next_action", "Owned next action"],
      ["affected_signoffs", "Explicit sign-offs for re-review, comma-separated: assessment, design, building, coordination (blank is routing-only)"],
      ["affected_milestones", "Explicit same-home milestone references for re-review, comma-separated (blank preserves milestones)"],
      ["affected_form_fields", 'Explicit same-home form fields JSON, for example {"FORM-001":["epc_band"]} (blank preserves fields)', "textarea"]],
    handoff: [["step", "Separately evidenced handoff action", ["sent", "received", "accepted", "returned", "escalated", "completed"]],
      ["receiver", "Named receiver email (sending)"], ["reason", "Reason/purpose"], ["evidence", "Explicit action evidence"],
      ["due", "Due date YYYY-MM-DD or Unknown"], ["urgency", "Urgency", ["Routine", "Urgent", "Unknown"]],
      ["next_action", "Owned next action (sending)"], ["escalation_owner", "Escalation owner (escalating)"]],
    "source-correct": [["source_id", "Authorized source to correct", data.sources.map((source) => source.id)],
      ["raw_text", "Explicit replacement source bytes", "textarea"], ["reason", "Source-owner correction reason"]],
    versions: [["form_id", "Affected form", Object.keys(data.forms)], ["schema_version", "Explicit schema version"],
      ["rule_version", "Explicit rule version"], ["reason", "Template-owner reason; unapproved versions block export"]],
    "funding-event": [["event", "Separate external evidence state", ["application-submitted", "application-disposition", "award", "claimable", "claim-submitted", "claim-disposition", "cash"]],
      ["form_id", "Same-home reviewed form", Object.keys(data.forms)], ["export_id", "Exact reviewed export ID"],
      ["evidence", "Supplied fictional external evidence reference"], ["amount", "Explicit GBP amount, if required"],
      ["disposition", "Supplied external disposition, if required", ["Accepted", "Rejected"]],
      ["previous_event", "Optional exact preceding event ID"], ["retry_of", "Rejected disposition ID for a corrected resubmission"]],
    "external-hazard-reference": [["authority", "Supplied fictional external authority"], ["version", "External evidence version"],
      ["reference", "External case/reference"], ["evidence", "Supplied external decision evidence"],
      ["released", "Supplied released flag (not your safety judgement)", ["true", "false"]],
      ["hazard_index", "Optional referred hazard index"]],
    "hazard-followup": [["hazard_index", "Referred hazard index"], ["step", "Separately supplied external event", ["received", "accepted", "chased"]],
      ["authority", "External authority"], ["external_actor", "Supplied external actor or Unknown"],
      ["observed_at", "Supplied event ISO timestamp"], ["reference", "Separate external reference"],
      ["evidence", "Supplied external action evidence"], ["followup", "Owned follow-up; not hazard closure"]],
    milestone: [["work_order", "Same-home work order ID"], ["milestone", "Independently verified milestone", ["mobilisation", "installation", "handover"]],
      ["evidence", "Actual supplied acceptance evidence"]],
    "resident-update": [["channel", "Safe supported contact route", ["Phone", "Letter", "Email", "Text", "Officer-assisted"]],
      ["step", "Commitment action", ["create", "proposed", "sent", "reassign"]],
      ["update_id", "Existing update ID (not creation)"], ["purpose", "Purpose/linked issue"],
      ["due", "Due YYYY-MM-DD or Unknown"], ["due_basis", "Due-date basis or Unknown"],
      ["adjustment_reference", "Minimum necessary safe-route reference or Unknown"],
      ["evidence", "Recorded update evidence (not assumed understanding)"], ["next_update", "Next owned update commitment"],
      ["receiver", "Explicit new owner email (reassignment only)"], ["reason", "Action/reassignment reason"]],
  };
  let values = {};
  const paint = () => {
    values = {};
    controls.replaceChildren(...definitions[action.value].flatMap(([name, label, options]) => {
      const fieldId = `exercise-event-${action.value}-${name}`;
      const input = Array.isArray(options)
        ? h("select", { id: fieldId }, h("option", { value: "" }, "Choose explicitly"),
          options.map((option) => h("option", { value: option }, option)))
        : options === "textarea" ? h("textarea", { id: fieldId, rows: 5 })
          : h("input", { id: fieldId, type: "text" });
      values[name] = input;
      return [h("label", { for: fieldId }, label), input];
    }));
  };
  action.addEventListener("change", paint);
  paint();
  const save = () => {
    const body = Object.fromEntries(Object.entries(values).filter(([, input]) => input.value !== "").map(([key, input]) => [key, input.value]));
    error.textContent = "";
    if ("affected_signoffs" in body) body.affected_signoffs = body.affected_signoffs.split(",").map((key) => key.trim()).filter(Boolean);
    if ("affected_milestones" in body) body.affected_milestones = body.affected_milestones.split(",").map((ref) => ref.trim()).filter(Boolean);
    if ("affected_form_fields" in body) {
      try {
        body.affected_form_fields = JSON.parse(body.affected_form_fields);
      } catch (parseError) {
        error.textContent = "Affected form fields must be a JSON object mapping same-home form IDs to explicit field lists.";
        return;
      }
    }
    if ("released" in body) body.released = body.released === "true";
    if ("hazard_index" in body) body.hazard_index = Number(body.hazard_index);
    send({ ...body, action: action.value });
  };
  return h("details", {}, h("summary", {}, "Record one explicitly supplied exercise event"),
    h("p", {}, "No automatic walkthrough or protected defaults. Record one event; the server enforces current prerequisites and your actual identity."),
    h("label", { for: "exercise-record-action" }, "Event type"), action,
    controls, error, h("button", { onclick: save }, "Record one supplied event"),
    h("details", {}, h("summary", {}, "Advanced explicit JSON input"),
      h("label", { for: "exercise-record-payload" }, "Event details JSON"), payload,
      h("button", { onclick: () => { try { send({ ...JSON.parse(payload.value), action: action.value }); } catch (e) { error.textContent = "Enter a JSON object."; } } }, "Record one JSON event")),
    h("h3", {}, "Manual journey instructions"),
    h("ol", {}, [
      "Intake -> Assessment. Coordinator prepares design. QI, second Coordinator, Safety and Programme each sign independently. Upload EPC, Survey, Design and resident-choice evidence using existing controls.",
      "Parse both EPC sources; inspect D/E conflict. Source owner corrects EX-EPC-B using source-correct with source_id, raw_text and reason. Parse again and re-review only affected fields. Sibling remains separate.",
      "Finance prepares GBP 20000 budget; independent Programme approves. Finance reviews ordinary fields; Programme explicitly records protected statements; a third independent Programme/Support identity reviews the pack, then exports.",
      "Record application-submitted, application-disposition and award using event, form_id, export_id, evidence and amount where needed. Disposition requires a different identity. Nothing is submitted by this workbench.",
      "Record resident decision for exact measure, scope and design_version in the resident controls. Ready requires all independent reviews, resolved EPC, resident choice and award. Capacity board supplies a committed package; issue and book the work order.",
      "Milestone details: work_order, milestone (mobilisation/installation/handover), evidence. Reviewer differs from issuer. Provider completion is separate from quality acceptance. Return defects, record fixes and independently reinspect before resident handover.",
      "Claim form/pack follows accepted Handover. Record claimable, claim-submitted, claim-disposition and cash with exact reviewed export, evidence and explicit GBP amount. Invoices bind work-order milestone references (WO-id:milestone); Finance matches and an independent approver dispositions, then records external payment.",
      "Financial closure requires all invoices paid externally, GBP 18000 reconciliation and accepted claim matched by separately evidenced cash. Switch identity by signing out; perspectives do not impersonate anyone.",
      "External hazard reference fields: authority, version, reference, evidence, released (supplied boolean), optional hazard_index after referral. This records external evidence, not local classification or clearance.",
    ].map((text) => h("li", {}, text))),
    h("p", {}, `Current ${id} lifecycle: ${data.lifecycle}. Missing/unsafe transitions return explicit errors.`));
}
