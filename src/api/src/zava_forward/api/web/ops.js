"use strict";
// Quality checks, defects, capacity and work orders. Shares h, api, post, me, show and isManager with app.js.
const QUALITY_ROLES = ["Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer"];
const QUALITY_SOURCES = ["Installer", "Contractor", "Provider submission", "Our own inspection"];
const WO_OUTCOMES = ["Booked", "Declined by provider", "Resident not available", "No access", "Rebooking needed"];
const QUALITY_WORDS = { "Submitted": "Waiting for an independent check", "Returned": "Returned: defect to put right", "Fixed, awaiting reinspection": "Fixed, waiting to be checked again",
  "Accepted": "Accepted, ready to hand over to the resident", "Handed over": "Handed over to the resident" };

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

function qualityPanel(c, id, refresh) {
  const box = h("section", { class: "card", id: "quality" }, h("h2", {}, "Quality checks and defects"));
  const canCheck = QUALITY_ROLES.includes(me.user.role);
  const measures = (Array.isArray(c.measures) ? c.measures : String(c.measures).split(",")).map((x) => x.trim()).filter(Boolean);
  const records = (c.quality || []).map((r, i) => {
    const note = h("input", { type: "text", maxlength: 300, "aria-label": `Note for ${r.measure}` });
    const defect = h("input", { type: "text", maxlength: 300, "aria-label": `What is wrong with ${r.measure}` });
    const owner = h("input", { type: "text", maxlength: 80, "aria-label": `Who will put it right for ${r.measure}` });
    const fixer = h("input", { type: "text", maxlength: 80, "aria-label": `Who fixed ${r.measure}` });
    const told = h("input", { type: "checkbox", id: `told-${i}` });
    const act = (name, body) => refresh(() => post(id, name, Object.assign({ index: i }, body)));
    return h("li", {},
      h("strong", {}, r.measure), ` ${QUALITY_WORDS[r.state] || r.state}. Checked against ${r.checklist_version}. Evidence from ${r.source}: ${r.submitted_by}.`,
      h("ul", {}, r.items.map((x) => h("li", {}, `${x.label}: ${x.evidence}`))),
      r.defect && r.state !== "Accepted" && r.state !== "Handed over" && h("p", { class: "err" }, `Defect: ${r.defect.description}. Reason: ${r.defect.reason}. Owner: ${r.defect.owner}.`),
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
      r.state === "Returned" && h("div", { class: "row" }, fixer, note,
        h("button", { class: "alt", onclick: () => act("quality-fix", { fixed_by: fixer.value, note: note.value }) }, "Record that it has been put right")),
      r.state === "Accepted" && h("div", { class: "row" }, note, told, h("label", { for: `told-${i}` }, "The resident has been told"),
        h("button", { onclick: () => act("quality-handover", { note: note.value, resident_told: told.checked }) }, "Record handover (guarantees, how to use it)")),
      r.state === "Handed over" && h("div", { class: "row" }, note,
        h("button", { class: "alt", onclick: () => act("quality-aftercare", { note: note.value }) }, "Add an aftercare note")));
  });
  box.append(records.length ? h("ul", { class: "list" }, records) : h("p", {}, "No quality checks recorded yet."));
  if (!c.closed) {
    const form = h("div", {}, h("h3", {}, "Record the evidence for a measure"),
      h("p", { class: "muted" }, "Evidence from an installer or contractor is kept as evidence only. It is checked by someone else before it counts."));
    const measure = h("select", { id: "q-measure", "aria-label": "Measure" }, measures.map((m) => h("option", {}, m)));
    const by = h("input", { id: "q-by", type: "text", maxlength: 80 });
    const src = h("select", { id: "q-src" }, QUALITY_SOURCES.map((x) => h("option", {}, x)));
    const checks = h("div", {});
    let lists = null;
    const paint = () => {
      const m = measures.find((x) => x === measure.value) || "";
      const key = [["loft", "Loft insulation"], ["wall", "Wall insulation"], ["heat pump", "Heat pump"], ["solar", "Solar panels"]].find(([w]) => m.toLowerCase().includes(w));
      const list = lists[key ? key[1] : "General"];
      checks.replaceChildren(h("p", { class: "muted" }, `Checklist ${list.version}. Say what was seen for every check.`),
        ...list.items.map((lab, n) => h("div", {}, h("label", { for: `q-i${n}` }, lab), h("input", { id: `q-i${n}`, type: "text", maxlength: 200, "data-label": lab }))));
    };
    measure.addEventListener("change", () => lists && paint());
    api("/api/checklists").then((l) => { lists = l; if (measures.length) paint(); });
    const revision = h("input", { id: "q-revision", type: "number", min: 1 });
    form.append(h("label", { for: "q-measure" }, "Which measure"), measure,
      h("label", { for: "q-revision" }, "Scope revision the evidence covers (see the resident decision panel)"), revision,
      h("label", { for: "q-by" }, "Who did the work or sent the evidence"), by,
      h("label", { for: "q-src" }, "Where the evidence came from"), src, checks,
      h("p", {}, h("button", { class: "alt", onclick: () => refresh(() => post(id, "quality-submit", { measure: measure.value, context_revision: Number(revision.value), submitted_by: by.value, source: src.value,
        items: Object.fromEntries([...checks.querySelectorAll("input")].map((i) => [i.dataset.label, i.value])) })) }, "Save evidence")));
    box.append(form);
  }
  return box;
}

function workOrdersCard(rows, mine) {
  return h("section", { class: "card" }, h("h2", {}, mine ? "Your work orders" : "Work orders"),
    rows.length ? h("ul", { class: "list" }, rows.map((w) => h("li", {},
      h("strong", {}, `${w.id}, version ${w.version}`), ` ${w.state}. ${w.address}, ${w.postcode}. Works: ${w.measures}. `,
      w.needs_notice ? h("span", { class: "flag" }, "Needs notice") : "No extra notice needed", `. Named contact: ${w.named_contact}.`,
      h("div", { class: "muted" }, w.scope), w.appointments.length > 0 && h("div", { class: "muted" }, "Visits: " + w.appointments.map((a) => `${a.outcome}${a.date ? ` ${a.date}` : ""}`).join("; "))))) : h("p", {}, "No work orders yet."));
}

async function contractorOrders() {
  return workOrdersCard(await api("/api/workorders"), true);
}

async function capacityView() {
  if (!isManager()) return show(h("p", {}, "Only a manager sees capacity and work orders."));
  const msg = h("div", { role: "status" });
  const go = async (fn) => { try { await fn(); await capacityView(); } catch (e) { msg.replaceChildren(h("p", { class: "err" }, e.message)); } };
  const [pkgs, orders] = await Promise.all([api("/api/packages"), api("/api/workorders")]);
  const inp = (label, attrs) => [h("label", {}, label), h("input", Object.assign({ type: "text" }, attrs))];
  const name = inp("Package name", { maxlength: 80 }), from = inp("Starts (2026-04-01)", {}), to = inp("Ends (2027-03-31)", {});
  const scope = inp("What it covers", { maxlength: 400 }), ref = inp("Contract or call-off reference", { maxlength: 60 });
  const create = h("section", { class: "card" }, h("h2", {}, "New package"), ...[name, from, to, scope, ref].flat(),
    h("p", {}, h("button", { onclick: () => go(() => api("/api/packages", { name: name[1].value, period_from: from[1].value, period_to: to[1].value, scope: scope[1].value, contract_ref: ref[1].value })) }, "Create package")));
  const cards = pkgs.map((p) => {
    const con = inp("Contractor", { maxlength: 80 }), off = inp("Offered (homes)", { inputmode: "numeric" }), com = inp("Committed with evidence (homes)", { inputmode: "numeric" });
    const evi = inp("Evidence for the commitment", { maxlength: 300 });
    const cid = inp("Case reference to issue a work order for", {}), wsc = inp("Work order wording (leave blank to use the package scope)", { maxlength: 400 });
    const bindings = inp("Affected measures and scope revisions: Measure|revision; Measure|revision", { maxlength: 1000 });
    return h("section", { class: "card" }, h("h2", {}, `${p.name} (${p.id})`),
      h("p", {}, `${p.period_from} to ${p.period_to}. Reference ${p.contract_ref}. Scope version ${p.scope_version}: ${p.scope}`),
      h("table", {}, h("caption", { class: "muted" }, "Offered is what a contractor says it can do. Only evidenced commitment can be used for work orders."),
        h("thead", {}, h("tr", {}, ["Contractor", "Offered", "Committed with evidence", "In use", "Room left", "Evidence"].map((x) => h("th", {}, x)))),
        h("tbody", {}, p.capacity.map((k) => h("tr", {}, h("td", {}, k.contractor), h("td", {}, k.offered), h("td", {}, k.committed), h("td", {}, k.in_use), h("td", {}, k.headroom), h("td", {}, k.evidence || "None"))))),
      h("h3", {}, "Record capacity"), ...[con, off, com, evi].flat(),
      h("p", {}, h("button", { class: "alt", onclick: () => go(() => api(`/api/packages/${p.id}/capacity`, { contractor: con[1].value, offered: off[1].value, committed: com[1].value, evidence: evi[1].value })) }, "Save capacity")),
      h("h3", {}, "Issue a work order"), ...[cid, wsc, bindings].flat(),
      h("p", {}, h("button", { onclick: () => go(() => api("/api/workorders", { package: p.id, case_id: cid[1].value, scope: wsc[1].value, resident_bindings: residentBindings(bindings[1].value) })) }, "Issue work order")));
  });
  const actions = orders.map((w) => {
    const note = h("input", { type: "text", maxlength: 300, "aria-label": `Note or date for ${w.id}` });
    const out = h("select", { "aria-label": `Appointment outcome for ${w.id}` }, WO_OUTCOMES.map((x) => h("option", {}, x)));
    const call = (a, body) => go(() => api(`/api/workorders/${w.id}/${a}`, body));
    const open = w.state === "Issued" || w.state === "Appointed";
    const bindings = h("input", { type: "text", maxlength: 1000, "aria-label": `Affected Measure|revision bindings for new version of ${w.id}` });
    return h("li", {}, h("strong", {}, `${w.id}, version ${w.version}`), ` ${w.state}. ${w.contractor}. ${w.address}. Issued by ${w.issued_by}.`,
      h("div", { class: "muted" }, w.scope),
      w.state !== "Withdrawn" && h("div", { class: "row" }, note, bindings,
        open && [out, h("button", { class: "alt", onclick: () => call("appointment", { outcome: out.value, date: note.value }) }, "Record appointment (date for Booked)"),
          h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/reissue`, { scope: note.value, reason: "Changed", resident_bindings: residentBindings(bindings.value) })) }, "New version"),
          h("button", { class: "alt", onclick: () => call("complete", { note: note.value }) }, "Record completion"),
          h("button", { class: "alt", onclick: () => call("withdraw", { reason: note.value }) }, "Withdraw (add the reason)")],
        w.state === "Completed" && h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/correct`, { reason: note.value, resident_bindings: residentBindings(bindings.value) })) }, "Record a correction (add the reason)")));
  });
  show(h("h1", {}, "Capacity and work orders"),
    h("p", { class: "muted" }, "Work orders are controlled: every change is a new version with who issued it, and nothing is issued beyond a contractor's evidenced commitment."),
    msg, create, ...cards, h("section", { class: "card" }, h("h2", {}, "Work orders"), orders.length ? h("ul", { class: "list" }, actions) : h("p", {}, "No work orders yet.")));
}
