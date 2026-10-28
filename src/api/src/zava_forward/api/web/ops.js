"use strict";
// Quality checks, defects, capacity and work orders. Shares h, api, post, me, show and isManager with app.js.
const QUALITY_ROLES = ["Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer"];
const QUALITY_SOURCES = ["Installer", "Contractor", "Provider submission", "Our own inspection"];
const WO_OUTCOMES = ["Booked", "Declined by provider", "Resident not available", "No access", "Rebooking needed"];
const QUALITY_WORDS = { "Submitted": "Waiting for an independent check", "Returned": "Returned: defect to put right", "Fixed, awaiting reinspection": "Fixed, waiting to be checked again",
  "Accepted": "Accepted, ready to hand over to the resident", "Handed over": "Handed over to the resident",
  "Superseded": "Replaced evidence: previous acceptance and handover no longer apply" };

function residentBindings(text) {
  if (!text.trim()) throw new Error("Enter each affected measure and current scope revision.");
  return text.split(";").map((line) => {
    const parts = line.split("|");
    if (parts.length !== 2 || !parts[0].trim() || !/^[1-9][0-9]*$/.test(parts[1].trim())) {
      throw new Error("Use Measure|revision, separated by semicolons. Check current revisions on the case.");
    }
    return { measure: parts[0].trim(), context_revision: Number(parts[1].trim()) };
  });
}

function qualityPanel(c, id, refresh, savedFields = [], session = caseSession) {
  const box = h("section", { class: "card", id: "quality" }, h("h2", {}, "Quality checks and defects"));
  const canCheck = QUALITY_ROLES.includes(me.user.role);
  const measures = (Array.isArray(c.measures) ? c.measures : String(c.measures).split(",")).map((x) => x.trim()).filter(Boolean);
  const records = (c.quality || []).map((r, i) => {
    const noteLabel = r.state === "Returned" ? `Remediation evidence for ${r.measure}` : `Note for ${r.measure}`;
    const note = h("input", { type: "text", name: `quality-note-${i}`, autocomplete: "off", maxlength: 300, "aria-label": noteLabel });
    const defect = h("input", { type: "text", maxlength: 300, "aria-label": `What is wrong with ${r.measure}` });
    const owner = h("input", { type: "text", maxlength: 80, "aria-label": `Who will put it right for ${r.measure}` });
    const fixer = h("input", { type: "text", name: `quality-fixer-${i}`, autocomplete: "off", maxlength: 80, "aria-label": `Who fixed ${r.measure}` });
    const told = h("input", { type: "checkbox", id: `told-${i}` });
    const message = h("div", { role: "status", "aria-live": "polite", tabindex: -1 });
    const act = async (name, body) => {
      const button = document.activeElement;
      if (button instanceof HTMLButtonElement) { button.disabled = true; button.setAttribute("aria-busy", "true"); }
      try {
        await refresh(async () => {
          try { await post(id, name, Object.assign({ index: i }, body)); }
          catch (error) {
            message.textContent = error.message;
            message.className = "err";
            if (name === "quality-fix" && !note.value.trim()) { note.setAttribute("aria-invalid", "true"); note.focus(); }
            else message.focus();
            throw error;
          }
        }, name === "quality-return" ? [note, defect, owner]
          : name === "quality-fix" ? [note, fixer]
          : name === "quality-handover" ? [note, told] : [note]);
      } finally {
        if (button instanceof HTMLButtonElement) { button.disabled = false; button.removeAttribute("aria-busy"); }
      }
    };
    return h("li", {},
      h("strong", {}, r.measure), ` ${QUALITY_WORDS[r.state] || r.state}. Evidence version ${r.evidence_version || 1}. Checked against ${r.checklist_version}. Evidence from ${r.source}: ${r.submitted_by}.`,
      h("ul", {}, r.items.map((x) => h("li", {}, `${x.label}: ${x.evidence}`))),
      r.defect && !["Accepted", "Handed over", "Superseded"].includes(r.state) && h("p", { class: "err" }, `Defect: ${r.defect.description}. Reason: ${r.defect.reason}. Owner: ${r.defect.owner}.`),
      r.defect?.remediation_evidence && h("p", {}, `Remediation evidence: ${r.defect.remediation_evidence}`),
      r.state === "Superseded" && h("p", { class: "muted" }, `Historical record only. Use evidence record ${r.superseded_by + 1} for current decisions.`,
        r.prior_acceptance?.accepted_by ? ` Previously accepted by ${r.prior_acceptance.accepted_by}.` : "",
        r.prior_acceptance?.handover ? ` Previous handover: ${r.prior_acceptance.handover.note}` : ""),
      r.accepted_by && h("p", {}, `Accepted by ${r.accepted_by}.`),
      r.handover && h("p", {}, `Handed over by ${r.handover.by}: ${r.handover.note}`),
      r.aftercare.length > 0 && h("ul", {}, r.aftercare.map((a) => h("li", {}, `${fmtDate(a.at)} ${a.by}: ${a.note}`))),
      (r.state === "Submitted" || r.state === "Fixed, awaiting reinspection") && (canCheck
        ? h("div", {}, h("p", { class: "muted" }, "You cannot accept work you submitted, recorded or fixed. Nothing is accepted automatically."),
          h("div", { class: "row" }, note,
            h("button", { onclick: () => act(r.state === "Submitted" ? "quality-accept" : "quality-reinspect", { result: "pass", note: note.value }) }, "Accept this work"),
            r.state === "Fixed, awaiting reinspection" && h("button", { class: "alt", onclick: () => act("quality-reinspect", { result: "fail", note: note.value }) }, "Still not right")),
          r.state === "Submitted" && h("div", { class: "row" }, defect, owner,
            h("button", { class: "alt", onclick: () => act("quality-return", { reason: note.value, defect: defect.value, owner: owner.value }) }, "Return with a defect (add the reason above)")))
        : h("p", { class: "muted" }, "A Quality Inspector or a manager checks this work.")),
      r.state === "Returned" && h("div", {}, h("p", {}, "Record what was corrected and the photo, document or inspection reference. A different person must check it again."),
        h("div", { class: "row" }, fixer, note,
          h("button", { class: "alt", onclick: () => act("quality-fix", { fixed_by: fixer.value, note: note.value }) }, "Record that it has been put right"))),
      r.state === "Accepted" && h("div", { class: "row" }, note, told, h("label", { for: `told-${i}` }, "The resident has been told"),
        h("button", { onclick: () => act("quality-handover", { note: note.value, resident_told: told.checked }) }, "Record handover (guarantees, how to use it)")),
      r.state === "Handed over" && h("div", { class: "row" }, note,
        h("button", { class: "alt", onclick: () => act("quality-aftercare", { note: note.value }) }, "Add an aftercare note")), message);
  });
  box.append(records.length ? h("ul", { class: "list" }, records) : h("p", {}, "No quality checks recorded yet."));
  if (!c.closed) {
    const form = h("div", {}, h("h3", {}, "Record the evidence for a measure"),
      h("p", { class: "muted" }, "Evidence from an installer or contractor is kept as evidence only. It is checked by someone else before it counts. Replacing accepted evidence cancels its previous acceptance and handover. A new independent check and resident handover are needed."));
    const measure = h("select", { id: "q-measure", "aria-label": "Measure" }, measures.map((m) => h("option", {}, m)));
    const by = h("input", { id: "q-by", type: "text", maxlength: 80 });
    const src = h("select", { id: "q-src" }, QUALITY_SOURCES.map((x) => h("option", {}, x)));
    const checks = h("div", {});
    let lists = null;
    const paint = () => {
      if (box.isConnected) savedFields = rememberCaseFields(session);
      const m = measures.find((x) => x === measure.value) || "";
      const key = [["loft", "Loft insulation"], ["wall", "Wall insulation"], ["heat pump", "Heat pump"], ["solar", "Solar panels"]].find(([w]) => m.toLowerCase().includes(w));
      const list = lists[key ? key[1] : "General"];
      checks.replaceChildren(h("p", { class: "muted" }, `Checklist ${list.version}. Say what was seen for every check.`),
        ...list.items.map((lab, n) => {
          const input = h("input", { id: `q-i${n}`, name: "checklist-evidence", autocomplete: "off", type: "text", maxlength: 200, "data-label": lab,
            "data-case-field-key": JSON.stringify(["checklist", m, list.version, lab]) });
          input.caseBinding = { kind: "checklist", id: `${m}, checklist ${list.version}` };
          return h("div", {}, h("label", { for: input.id }, lab), input);
        }));
      restoreBoundFields(savedFields, form, "checklist", session);
    };
    measure.addEventListener("change", () => lists && paint());
    api("/api/checklists").then((l) => {
      lists = l;
      if (measures.length) paint();
    }).catch(error => checks.replaceChildren(h("p", { class: "err", role: "alert" }, `Could not load checklists: ${error.message}. Refresh this case to try again.`)));
    const revision = h("input", { id: "q-revision", type: "number", min: 1 });
    form.append(h("label", { for: "q-measure" }, "Which measure"), measure,
      h("label", { for: "q-revision" }, "Scope revision the evidence covers (see the resident decision panel)"), revision,
      h("label", { for: "q-by" }, "Who did the work or sent the evidence"), by,
      h("label", { for: "q-src" }, "Where the evidence came from"), src, checks,
      h("p", {}, h("button", { class: "alt", onclick: () => {
        const replaces = (c.quality || []).some((r) => r.measure === measure.value && ["Accepted", "Handed over"].includes(r.state));
        if (replaces && !window.confirm("Replace this measure's evidence? Its previous acceptance and resident handover will no longer apply. The history will be kept.")) return;
        refresh(() => post(id, "quality-submit", { measure: measure.value, context_revision: Number(revision.value), submitted_by: by.value, source: src.value,
          items: Object.fromEntries([...checks.querySelectorAll("input")].map((i) => [i.dataset.label, i.value])) }), [measure, revision, by, src, ...checks.querySelectorAll("input")]);
      } }, "Save evidence")));
    box.append(form);
  }
  return box;
}

function appointmentSlot(state) {
  const offer = state.offer || state;
  const ended = state.status === "Ended" || offer.ended;
  return h("div", {},
    h("p", {}, offer.date
      ? `${ended ? "Historical visit (ended)" : "Selected visit"}: ${fmtDate(offer.date)}. Period: ${offer.period || "Unknown"}.`
      : "Selected visit: Unknown. No verified offer."),
    h("p", {}, `Necessary instructions: ${offer.instructions || "Unknown"}`));
}

function workOrdersCard(rows, mine) {
  return h("section", { class: "card" }, h("h2", {}, mine ? "Your work orders" : "Work orders"),
    rows.length ? h("ul", { class: "list" }, rows.map((w) => h("li", {},
      h("strong", {}, `${w.id}, version ${w.version}`), ` ${w.state}. ${w.address}, ${w.postcode}. Works: ${w.measures}. `,
      w.needs_notice ? h("span", { class: "flag" }, "Needs notice") : "No extra notice needed", `. Named contact: ${w.named_contact}.`,
      h("p", {}, `Appointment: ${w.appointment_control.status}.${w.appointment_control.missing.length ? ` ${w.appointment_control.missing.join("; ")}.` : ""}`),
      appointmentSlot(w.appointment_control),
      h("div", { class: "muted" }, w.scope), w.appointments.length > 0 && h("div", { class: "muted" }, "Visits: " + w.appointments.map((a) => `${a.outcome}${a.date ? ` ${a.date}` : ""}`).join("; "))))) : h("p", {}, "No work orders yet."));
}

async function contractorOrders() {
  return workOrdersCard(await api("/api/workorders"), true);
}

function appointmentDrafts() {
  return [...document.querySelectorAll('form[data-appointment-form][data-unsaved="true"]')].map((form) => ({
    key: form.dataset.appointmentForm,
    context: form.appointmentContext,
    open: form.parentElement.open,
    values: [...form.elements].filter((el) => el.name).map((el) => ({ name: el.name, value: el.value, checked: el.checked }))
  }));
}

async function capacityView() {
  if (!isManager()) return show(h("p", {}, "Only a manager sees capacity and work orders."));
  const signal = routeController.signal;
  const msg = h("div", { role: "status", "aria-live": "polite", tabindex: -1 });
  const go = async (fn = async () => {}, savedForm) => {
    const button = document.activeElement;
    if (button instanceof HTMLButtonElement) { button.disabled = true; button.setAttribute("aria-busy", "true"); }
    try {
      await fn();
      if (savedForm) delete savedForm.dataset.unsaved;
      signal.throwIfAborted();
      await capacityView();
    }
    catch (e) {
      if (signal.aborted || !me) return;
      msg.replaceChildren(h("p", { class: "err" }, e.message));
      if (e.capacityLoadFailure) msg.append(h("button", { type: "button", onclick: () => go() }, "Try again"));
      msg.focus();
    }
    finally { if (button instanceof HTMLButtonElement) { button.disabled = false; button.removeAttribute("aria-busy"); } }
  };
  const load = async (path, label) => {
    try { return await api(path, undefined, signal); }
    catch (error) {
      if (signal.aborted || !me) throw error;
      const detail = error instanceof TypeError || error.message === "Something went wrong." ? "" : ` ${error.message}`;
      error.message = `We could not load ${label}. Try again. If this continues, contact application support.${detail}`;
      error.capacityLoadFailure = true;
      throw error;
    }
  };
  const [pkgs, orders] = await Promise.all([load("/api/packages", "packages"), load("/api/workorders", "work orders")]);
  signal.throwIfAborted();
  if (!me) return;
  let field = 0;
  const inp = (label, attrs) => {
    const id = `capacity-field-${++field}`;
    return [h("label", { for: id }, label), h("input", Object.assign({ id, name: label.toLowerCase().replace(/[^a-z0-9]+/g, "-"), autocomplete: "off", type: "text" }, attrs))];
  };
  const name = inp("Package name", { maxlength: 80 }), from = inp("Starts", { type: "date" }), to = inp("Ends", { type: "date" });
  const scope = inp("What it covers", { maxlength: 400 }), ref = inp("Contract or call-off reference", { maxlength: 60 });
  const contractVersion = inp("Contract or call-off version", { maxlength: 80, spellcheck: false, required: true });
  const versionError = h("p", { id: "capacity-version-error", class: "err", role: "status", "aria-live": "polite" });
  contractVersion[1].setAttribute("aria-describedby", "capacity-version-error");
  contractVersion[1].addEventListener("input", () => {
    contractVersion[1].removeAttribute("aria-invalid");
    versionError.textContent = "";
  });
  const createPackage = () => {
    if (!contractVersion[1].value.trim()) {
      contractVersion[1].setAttribute("aria-invalid", "true");
      versionError.textContent = "Enter the contract or call-off version before creating the package.";
      contractVersion[1].focus();
      return;
    }
    return go(() => api("/api/packages", { name: name[1].value, period_from: from[1].value, period_to: to[1].value, scope: scope[1].value, contract_ref: ref[1].value, contract_version: contractVersion[1].value }));
  };
  const create = h("section", { class: "card" }, h("h2", {}, "New package"), ...[name, from, to, scope, ref].flat(),
    ...contractVersion, versionError,
    h("p", {}, "A package is a draft, not an instruction. Creating it grants no contract authority."),
    h("p", {}, h("button", { onclick: createPackage }, "Create package")));
  const cards = pkgs.map((p) => {
    const con = inp("Contractor", { maxlength: 80 }), off = inp("Offered (home orders)", { type: "number", min: 0, max: 100000, step: 1, inputmode: "numeric" }), com = inp("Committed with evidence (home orders)", { type: "number", min: 0, max: 100000, step: 1, inputmode: "numeric" });
    const evi = inp("Evidence for the commitment", { maxlength: 300 });
    const sourceCase = inp("Case holding the commitment document", { maxlength: 64, spellcheck: false });
    const document = inp("Commitment document ID", { maxlength: 64, spellcheck: false });
    const sourceVersion = inp("Commitment document version", { maxlength: 80, spellcheck: false });
    const sourceDate = inp("Commitment source date", { type: "date" }), reviewed = inp("Manager reviewed on", { type: "date" });
    const validFrom = inp("Capacity delivery starts", { type: "date" }), validTo = inp("Capacity delivery ends", { type: "date" });
    const covered = inp("Covered case references, separated by semicolons", { maxlength: 2000, spellcheck: false });
    const cid = inp("Case reference to issue a work order for", {}), wsc = inp("Work order wording (leave blank to use the package scope)", { maxlength: 400 });
    const bindings = inp("Affected measures and scope revisions: Measure|revision; Measure|revision", { maxlength: 1000 });
    return h("section", { class: "card" }, h("h2", {}, `${p.name} (${p.id})`),
      h("p", {}, `${fmtDate(p.period_from)} to ${fmtDate(p.period_to)}. Reference ${p.contract_ref}, version ${p.contract_version || "Unknown"}. Scope version ${p.scope_version}: ${p.scope}`),
      h("div", { class: "table-scroll", role: "region", "aria-label": `Capacity for ${p.id}`, tabindex: 0 },
        h("table", {}, h("caption", { class: "muted" }, "One unit is one home work order for this package period, not a crew or weekly slot. Only evidenced commitment can confirm work."),
          h("thead", {}, h("tr", {}, ["Contractor", "Offered", "Committed", "In use", "Room left", "Evidence"].map((x) => h("th", { scope: "col" }, x)))),
          h("tbody", {}, p.capacity.map((k) => h("tr", {}, h("td", {}, k.contractor), h("td", {}, k.offered), h("td", {}, k.committed), h("td", {}, k.in_use), h("td", {}, k.headroom),
            h("td", {}, `${k.evidence || "None"}. ${k.evidence_status}.`, k.details && h("div", {}, `Source ${k.details.document_id}, version ${k.details.source_version}. Reviewed ${fmtDate(k.details.reviewed_on)}. Capacity version ${k.version}.`))))))),
      h("h3", {}, "Record capacity"), ...[con, off, com, evi, sourceCase, document, sourceVersion, sourceDate, reviewed, validFrom, validTo, covered].flat(),
      h("p", { class: "muted" }, "Only a named manager with recorded contract authority can accept this commitment. Check the original document, current scope and covered homes. A review is current for 7 days. Record 0 if capacity is lost; existing orders will show a deficit."),
      h("p", {}, h("button", { class: "alt", onclick: () => go(() => api(`/api/packages/${p.id}/capacity`, {
        contractor: con[1].value, offered: off[1].value, committed: com[1].value, evidence: evi[1].value,
        details: { source_case_id: sourceCase[1].value, document_id: document[1].value, source_version: sourceVersion[1].value,
          source_date: sourceDate[1].value, reviewed_on: reviewed[1].value, valid_from: validFrom[1].value, valid_to: validTo[1].value,
          unit: "home-work-order", status: "Committed", case_ids: covered[1].value.split(";").map((x) => x.trim()).filter(Boolean) }
      })) }, "Save capacity")),
      h("h3", {}, "Issue a work order"), ...[cid, wsc, bindings].flat(),
      h("p", {}, h("button", { onclick: () => go(() => api("/api/workorders", { package: p.id, case_id: cid[1].value, scope: wsc[1].value, resident_bindings: residentBindings(bindings[1].value) })) }, "Issue work order")));
  });
  const actions = orders.map((w) => {
    const note = h("input", { type: "text", name: `order-note-${w.id}`, autocomplete: "off", maxlength: 300, "aria-label": `Note or date for ${w.id}` });
    const out = h("select", { name: `legacy-outcome-${w.id}`, "aria-label": `Appointment outcome for ${w.id}` }, WO_OUTCOMES.map((x) => h("option", {}, x)));
    const call = (a, body, savedForm) => go(() => api(`/api/workorders/${w.id}/${a}`, body), savedForm);
    const open = w.state === "Issued" || w.state === "Appointed";
    const bindings = h("input", { type: "text", maxlength: 1000, "aria-label": `Affected Measure|revision bindings for new version of ${w.id}` });
    return h("li", {}, h("strong", {}, `${w.id}, version ${w.version}`), ` ${w.state}. ${w.contractor}. ${w.address}. Issued by ${w.issued_by}.`,
      h("div", { class: "muted" }, w.scope),
      appointmentControls(w, (body, form) => call("appointment-control", body, form)),
      w.state !== "Withdrawn" && h("div", { class: "row" }, note, bindings,
        open && [out, h("button", { class: "alt", onclick: () => call("appointment", { outcome: out.value, date: note.value }) }, "Record appointment (date for Booked)"),
          h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/reissue`, { scope: note.value, reason: "Changed", resident_bindings: residentBindings(bindings.value) })) }, "New version"),
          h("button", { class: "alt", onclick: () => call("complete", { note: note.value }) }, "Record completion"),
          h("button", { class: "alt", onclick: () => call("withdraw", { reason: note.value }) }, "Withdraw (add the reason)")],
        w.state === "Completed" && h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/correct`, { reason: note.value, resident_bindings: residentBindings(bindings.value) })) }, "Record a correction (add the reason)")));
  });
  const drafts = appointmentDrafts();
  show(h("h1", {}, "Capacity and work orders"),
    h("p", { class: "muted" }, "Work orders are controlled: every change is a new version with who issued it, and nothing is issued beyond a contractor's evidenced commitment."),
    msg, create, ...(cards.length ? cards : [h("p", {}, "No packages yet.")]),
    h("section", { class: "card" }, h("h2", {}, "Work orders"), orders.length ? h("ul", { class: "list" }, actions) : h("p", {}, "No work orders yet.")));
  for (const draft of drafts) {
    const form = [...document.querySelectorAll("form[data-appointment-form]")].find((el) => el.dataset.appointmentForm === draft.key);
    if (!form) continue;
    for (const saved of draft.values) {
      const control = form.elements.namedItem(saved.name);
      if (control) { control.value = saved.value; if (control.type === "checkbox") control.checked = saved.checked; }
    }
    form.appointmentContext = draft.context;
    form.dataset.unsaved = "true";
    form.parentElement.open = draft.open;
  }
}

function appointmentControls(w, submit) {
  const state = w.appointment_control;
  if (!state.current_binding) return h("section", { "aria-label": `Appointment controls for ${w.id}` },
    h("h3", {}, `Appointment: ${state.status}`), appointmentSlot(state),
    h("p", {}, "Appointment evidence is held for roles with a recorded need. Ask the resident-service owner to review the next step."));
  const offer = state.offer;
  let field = 0;
  const input = (label, type = "text", value = "", required = true) => {
    const id = `${w.id}-appointment-${++field}`;
    const error = h("span", { id: `${id}-error`, role: "status", "aria-live": "polite", class: "err" });
    const control = h("input", { id, name: id, autocomplete: "off", type, maxlength: 500, value,
      required: required && type !== "checkbox", "aria-describedby": `${id}-error`,
      oninvalid: () => { error.textContent = control.validationMessage; control.setAttribute("aria-invalid", "true"); },
      oninput: () => { error.textContent = ""; control.removeAttribute("aria-invalid"); }
    });
    return [h("label", { for: id }, `${label} (${w.id})`), control, error];
  };
  const check = (label) => {
    const pair = input(label, "checkbox");
    pair[1].removeAttribute("aria-describedby");
    return [h("label", {}, pair[1], ` ${label} (${w.id})`), pair[1]];
  };
  const select = (label, choices) => {
    const id = `${w.id}-appointment-${++field}`;
    const control = h("select", { id, name: id }, choices.map((x) => h("option", {}, x)));
    return [h("label", { for: id }, `${label} (${w.id})`), control];
  };
  const section = (title, fields, action, body) => {
    const event = input(`${title} event reference`, "text", crypto.randomUUID());
    const form = h("form", {
      "data-appointment-form": `${w.id}-${action}`,
      oninput: () => { form.dataset.unsaved = "true"; },
      onchange: () => { form.dataset.unsaved = "true"; },
      onreset: (e) => {
        if (form.dataset.unsaved === "true" && !window.confirm("Discard only this unsaved draft?")) { e.preventDefault(); return; }
        delete form.dataset.unsaved; form.appointmentContext = { ...initialContext };
      },
      onsubmit: (e) => {
      e.preventDefault();
      if (action === "close_case" && !window.confirm(`Record the supplied human closure of underlying home case ${state.case_id}? This resets its active no-access count, not its history. Outstanding resident updates and remedies remain. This is not investigation task disposition or technical, legal or financial approval.`)) return;
      submit(Object.assign({ action, event_ref: event[1].value }, body(), form.appointmentContext), form);
    } }, ...event, ...fields, h("button", { type: "submit", class: "alt" }, title),
    h("button", { type: "reset", class: "alt" }, "Discard this draft"));
    const initialContext = action === "offer" ? { expected_offer_id: offer ? offer.id : null }
      : ["confirm", "authority", "outcome"].includes(action) ? { offer_id: offer && offer.id }
      : action === "close_case" ? { case_id: state.case_id, expected_case_version: state.case_version } : {};
    form.appointmentContext = { ...initialContext };
    return h("details", {}, h("summary", {}, `${title} for ${w.id}`), form);
  };
  const date = input("Offer date", "date"), period = input("Visit period");
  const options = input("Options offered, separated by semicolons");
  const constraints = input("Household constraints or Unknown");
  const instructions = input("Necessary provider instructions only, no diagnoses");
  const paused = check("Household paused"), deferred = check("Household deferred");
  const bundle = check("Bundle requested"), agreed = check("Resident agreed to bundle");
  const competence = input("Scoped competence source for bundle", "text", "", false);
  const proposal = section("Record appointment offer",
    [...date, ...period, ...options, ...constraints, ...instructions, paused[0], deferred[0],
      bundle[0], agreed[0], ...competence], "offer", () => ({
      date: date[1].value, period: period[1].value,
      expected_offer_id: offer ? offer.id : null,
      options: options[1].value.split(";").map((s) => s.trim()).filter(Boolean),
      constraints: constraints[1].value, instructions: instructions[1].value,
      paused: paused[1].checked, deferred: deferred[1].checked,
      bundle: bundle[1].checked, bundle_agreed: agreed[1].checked,
      competence: { source: competence[1].value, scope: state.current_binding }
    }));
  const kind = select("Confirmation kind", ["resident", "staff", "capacity"]);
  const person = input("Confirming person"), source = input("Confirmation source");
  const channel = input("Confirmation channel, including phone or in person");
  const representative = input("Appointment representative reference, if applicable", "text", "", false);
  const confirmation = section("Record separate confirmation",
    [...kind, ...person, ...source, ...channel, ...representative], "confirm", () => ({
      offer_id: offer && offer.id, kind: kind[1].value, person: person[1].value,
      source: source[1].value, channel: channel[1].value,
      representative_ref: representative[1].value || null
    }));
  const rep = input("Appointment authority reference"), repPerson = input("Authorized representative");
  const repSource = input("Appointment-specific authority source");
  const start = input("Authority starts", "date"), end = input("Authority ends", "date");
  const revoked = check("Appointment authority revoked");
  const authority = section("Record appointment authority",
    [...rep, ...repPerson, ...repSource, ...start, ...end, revoked[0]], "authority", () => ({
      representative_ref: rep[1].value, person: repPerson[1].value, source: repSource[1].value,
      offer_id: offer && offer.id,
      valid_from: start[1].value, valid_to: end[1].value, revoked: revoked[1].checked
    }));
  const cause = select("Visit cause", ["Unknown", "Resident", "Provider", "Cancelled", "Rescheduled"]);
  const owner = input("Cause owner or Unknown"), verification = input("Verification source or Unknown");
  const verified = check("Evidence verified"), noAccess = check("Resident no-access fact");
  const breach = check("Preference breach fact"), abortive = check("Abortive visit fact");
  const outcome = section("Record evidenced visit outcome",
    [...cause, ...owner, ...verification, verified[0], noAccess[0], breach[0], abortive[0]], "outcome", () => ({
      offer_id: offer && offer.id, cause: cause[1].value, owner: owner[1].value,
      source: verification[1].value, verified: verified[1].checked, no_access: noAccess[1].checked,
      preference_breach: breach[1].checked, abortive: abortive[1].checked
    }));
  const threshold = input("Provisional no-access threshold", "number", "5");
  threshold[1].min = "0"; threshold[1].step = "1";
  const basis = input("Threshold configuration evidence");
  const configure = section("Record provisional threshold", [...threshold, ...basis], "configure", () => ({
    threshold: Number(threshold[1].value), basis: basis[1].value
  }));
  const checks = Object.fromEntries(["confirmation", "notice", "attendance", "adjustments", "contact", "circumstances"]
    .map((key) => [key, input(`Human ${key} check evidence or Unknown`)]));
  const corrective = input("Corrective action"), update = input("Next resident update");
  const disposition = input("Investigation task disposition, not case closure");
  const investigation = state.investigation && section("Record human investigation",
    [...Object.values(checks).flat(), ...corrective, ...update, ...disposition], "investigation", () => ({
      checks: Object.fromEntries(Object.entries(checks).map(([key, pair]) => [key, pair[1].value])),
      corrective_action: corrective[1].value, next_update: update[1].value, disposition: disposition[1].value
    }));
  const closureSource = input("Human home-case closure decision source");
  const closureVersion = input("Human closure source version");
  const closureReason = input("Human underlying home-case closure reason");
  const closureConfirmed = check("I am recording the supplied human underlying home-case closure, not investigation task disposition");
  closureConfirmed[1].required = true;
  const closure = state.case_closed === false && section("Record human underlying home-case closure",
    [h("p", {}, `Underlying home case ${state.case_id}. Record only a supplied human decision. This does not approve handover, legal or financial closure or clear resident updates or remedies.`),
      ...closureSource, ...closureVersion, ...closureReason, closureConfirmed[0]], "close_case", () => ({
      case_id: state.case_id, expected_case_version: state.case_version,
      source: closureSource[1].value, source_version: closureVersion[1].value,
      reason: closureReason[1].value, confirmed: closureConfirmed[1].checked
    }));
  return h("section", { "aria-label": `Appointment controls for ${w.id}` },
    h("h3", {}, `Appointment: ${state.status}`),
    appointmentSlot(state),
    h("p", {}, state.missing.length ? state.missing.join("; ") : "Resident, staff and current contractor capacity confirmations recorded."),
    h("p", {}, "An offer is not an agreement. Works consent remains separate. Nothing is sent. Urgent safety response does not wait for a bundle or investigation."),
    h("a", { href: `#/case/${encodeURIComponent(w.case_id)}` }, "Record or review the named resident-update commitment and safe contact"),
    offer && h("p", {}, `Options: ${offer.options.join("; ")}. Constraints: ${offer.constraints}. Paused: ${offer.paused ? "Yes" : "No"}. Deferred: ${offer.deferred ? "Yes" : "No"}. Update owner: ${state.current_update_owner ? state.current_update_owner.name : "Unknown"}.`),
    h("p", {}, `Eligible resident no-access: ${state.eligible_no_access}. Reporting threshold: ${state.reporting_threshold}. ${state.case_reset}.`),
    h("p", {}, `Underlying home case ${state.case_id}: ${state.case_closed === true ? "Closed" : state.case_closed === false ? "Active" : "Unknown"}. Recorded human closures: ${state.closure_history.length}. History is retained.`),
    h("p", {}, `Preference breaches by cause / owner: ${JSON.stringify(state.counts.preference_breach)}. Abortive visits by cause / owner: ${JSON.stringify(state.counts.abortive)}.`),
    proposal, confirmation, authority, outcome, configure, investigation, closure);
}
