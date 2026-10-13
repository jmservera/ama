"use strict";

const assistantNames = {
  "stock-prioritisation": "Stock facts and prioritisation",
  "assessment-preparation": "Assessment preparation",
  "funding-evidence": "Funding evidence",
  "works-resident-coordination": "Works and resident coordination",
  "quality-evidence": "Quality evidence",
};

function assistantProposal(p, reload) {
  const status = h("p", { role: "status" }, `${p.display_state}. ${p.reason || ""} ${p.manual}`);
  const note = h("textarea", { "aria-label": "Source verification or review note", maxlength: "1000" });
  const verified = h("input", { type: "checkbox", id: `verified-${p.id}` });
  const editing = h("textarea", { "aria-label": "Edited evidence proposal JSON", maxlength: "16000" },
    JSON.stringify(p.output, null, 2));
  const act = async (action) => {
    try {
      const body = { action, revision: p.revision, note: note.value };
      if (action === "verify") body.source_verified = verified.checked;
      if (action === "edit-accept") body.output = JSON.parse(editing.value);
      await api(`/api/assistants/proposals/${p.id}/review`, body);
      await reload();
    } catch (e) { status.textContent = e.message; }
  };
  const ready = p.state === "ready" && !p.stale;
  const ownVerification = p.verification && p.verification.by === me.user.email;
  const history = h("pre", {}, JSON.stringify({ envelope: p.envelope, history: p.provenance }, null, 2));
  let offset = p.history_next_offset;
  const moreHistory = h("button", { class: "alt", hidden: offset == null, onclick: async () => {
    try {
      const earlier = await api(`/api/assistants/proposals/${p.id}?history_offset=${offset}`);
      history.append(document.createTextNode("\n" + JSON.stringify(earlier.provenance, null, 2)));
      offset = earlier.history_next_offset;
      moreHistory.hidden = offset == null;
    } catch (e) { status.textContent = e.message; }
  } }, "Earlier proposal history");
  return h("article", { class: "card" },
    h("h3", {}, `${assistantNames[p.capability]} v${p.version}`),
    h("a", { href: `#/case/${encodeURIComponent(p.case_id)}` }, p.case_id), status,
    h("p", { class: "muted" }, "Proposal only. Nothing is sent, booked, paid, ranked, signed off or released. Citations establish provenance, not truth."),
    h("p", {}, `Invocation: ${p.provenance.filter((e) => e.kind === "invocation").map((e) => e.mode).join(", ")}. Attempts: ${p.attempts}.`),
    p.output && h("div", {}, h("p", {}, p.output.summary),
      h("ul", {}, p.output.findings.map((f) => h("li", {}, `${f.text} [${f.citations.join(", ")}]`))),
      h("h4", {}, "Unknowns"), h("ul", {}, p.output.unknowns.map((u) => h("li", {}, u)))),
    h("details", {}, h("summary", {}, "Permitted sources, versions and hashes"),
      h("pre", {}, JSON.stringify(p.snapshot, null, 2))),
    h("details", {}, h("summary", {}, "Provider usage and proposal history"),
      history, moreHistory),
    h("label", {}, "Source verification/review note", note),
    ready && h("div", {}, h("label", { for: `verified-${p.id}` }, verified,
      " I checked the cited sources, including unknowns and discrepancies."),
    h("button", { onclick: () => act("verify") }, "Record human source verification")),
    p.verification && h("p", {}, `Sources checked by ${p.verification.by}. ${p.verification.note}`),
    ready && ownVerification && h("div", {},
      h("button", { onclick: () => act("accept") }, "Accept proposal only"),
      h("details", {}, h("summary", {}, "Edit and accept proposal only"), editing,
        h("button", { onclick: () => act("edit-accept") }, "Save edited proposal"))),
    h("button", { class: "alt", onclick: () => act("reject") }, "Reject proposal"));
}

async function assistantCasePanel(id) {
  const panel = h("section", { class: "card" }, h("h2", {}, "Retrofit assistants"));
  try {
    const [registry, queue] = await Promise.all([
      api("/api/assistants"), api(`/api/assistants/proposals?case_id=${encodeURIComponent(id)}`),
    ]);
    panel.append(h("p", { role: "status" }, registry.disabled ||
      `Assistance available. Proactive checks ${registry.proactive ? "enabled" : "off"}.`));
    panel.append(h("p", {}, "These are synthetic exercise rules. Continue ordinary case work manually when assistance is disabled, failed or stale."));
    for (const a of registry.assistants) {
      panel.append(h("button", { class: "alt", onclick: async () => {
        try {
          await api(`/api/assistants/${a.id}/invoke`, { case_id: id });
          await caseView(id);
        } catch (e) { panel.append(h("p", { role: "alert", class: "err" }, e.message)); }
      } }, `Request ${assistantNames[a.id]}`));
    }
    panel.append(h("button", { class: "alt", onclick: () => caseView(id) }, "Refresh proposals"),
      h("a", { href: "#/assistants" }, "Shared role-owned review queue"));
    for (const p of queue.proposals) panel.append(assistantProposal(p, () => caseView(id)));
  } catch (e) {
    panel.append(h("p", { role: "status" }, `Assistance unavailable: ${e.message}. Continue ordinary case work manually.`));
  }
  return panel;
}

async function assistantQueueView(after = "", append = false) {
  try {
    const queue = await api(`/api/assistants/proposals${after ? `?after=${encodeURIComponent(after)}` : ""}`);
    const cards = queue.proposals.map((p) => assistantProposal(p, () => assistantQueueView()));
    const more = queue.next_after && h("button", { onclick: async (e) => {
      e.currentTarget.remove();
      await assistantQueueView(queue.next_after, true);
    } }, "Show more proposals");
    if (append) { app.append(...cards, ...(more ? [more] : [])); return; }
    show(h("h1", {}, "Role-owned assistant proposals"),
      h("p", { role: "status" }, queue.disabled || "Unreviewed proposals require a separate source check and role review."),
      h("button", { onclick: () => assistantQueueView() }, "Refresh queue"),
      ...cards, more,
      !queue.proposals.length && h("p", {}, "No proposals in your current role and case scope. Use the ordinary case controls."));
  } catch (e) {
    show(h("h1", {}, "Assistant proposals"), h("p", { role: "alert" }, e.message),
      h("a", { href: "#/" }, "Continue manual case work"));
  }
}
