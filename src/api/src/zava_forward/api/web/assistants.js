"use strict";

const assistantNames = {
  "stock-prioritisation": "Stock facts and prioritisation",
  "assessment-preparation": "Assessment preparation",
  "funding-evidence": "Funding evidence",
  "works-resident-coordination": "Works and resident coordination",
  "quality-evidence": "Quality evidence",
};
const proposalReviewStates = new Map();

function assistantProposal(p, reload, recoverable = new Map()) {
  const reviewKey = `${p.id}:${p.revision}`;
  const previous = proposalReviewStates.get(reviewKey);
  if (previous?.state === "uncertain" && recoverable.get(reviewKey) === previous) proposalReviewStates.delete(reviewKey);
  const status = h("p", { role: "status" }, `${p.display_state}. ${p.release_denial ? p.release_denial.reason : (p.reason || "")} ${p.manual}`);
  const note = h("textarea", { id: `proposal-reason-${p.id}`, name: "review-reason", autocomplete: "off", "aria-label": "Reason", maxlength: "1000" });
  const error = h("p", { id: `proposal-error-${p.id}`, class: "field-error", role: "status" });
  const verified = h("input", { type: "checkbox", id: `verified-${p.id}` });
  const editing = h("textarea", { name: "edited-proposal", autocomplete: "off", "aria-label": "Edited evidence proposal JSON", maxlength: "16000" },
    JSON.stringify(p.output, null, 2));
  const clearError = () => {
    error.textContent = "";
    [note, editing].forEach(field => {
      field.removeAttribute("aria-invalid");
      field.removeAttribute("aria-describedby");
    });
  };
  [note, editing].forEach(field => field.addEventListener("input", clearError));
  const invalid = (field, text) => {
    clearError();
    error.textContent = text;
    field.setAttribute("aria-invalid", "true");
    field.setAttribute("aria-describedby", error.id);
    field.focus();
  };
  const setReviewState = (state, message) => {
    if (state) proposalReviewStates.set(reviewKey, { state });
    else proposalReviewStates.delete(reviewKey);
    [card, ...app.querySelectorAll("[data-proposal-id]")].forEach(node => {
      if (node.dataset.proposalId === p.id && String(node.dataset.proposalRevision) === String(p.revision)) node.updateReviewState(message);
    });
  };
  const act = async (action) => {
    if (proposalReviewStates.has(reviewKey)) return;
    clearError();
    if (["edit-accept", "reject"].includes(action) && !note.value.trim()) {
      invalid(note, "Enter a reason to edit or reject this proposal.");
      return;
    }
    const body = { action, revision: p.revision, note: note.value };
    if (action === "verify") body.source_verified = verified.checked;
    if (action === "edit-accept") {
      try { body.output = JSON.parse(editing.value); }
      catch { invalid(editing, "Enter valid JSON for the edited evidence proposal."); return; }
    }
    const sent = snapshotCaseFields([note, ...(action === "verify" ? [verified] : action === "edit-accept" ? [editing] : [])]);
    setReviewState("pending");
    status.textContent = "Recording your review...";
    let recorded = false;
    try {
      await api(`/api/assistants/proposals/${p.id}/review`, body);
      recorded = true;
      setReviewState("recorded");
      reconcileCaseSubmission(sent);
      await reload();
    } catch (e) {
      const checkHistory = mutationNeedsHistory(e);
      const message = recorded
        ? `Your review was recorded, but suggestions could not reload. Refresh before another review. ${e.message}`
        : checkHistory ? `Confirmation is unavailable. Refresh and check the review history before another action. ${e.message}` : e.message;
      setReviewState(recorded ? "recorded" : checkHistory ? "uncertain" : null, message);
    }
  };
  const ready = p.state === "ready" && !p.stale && p.actionable !== false
    && !p.release_denial && p.epoch_current !== false;
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
  } }, "Earlier changes to this suggestion");
  const editBox = h("div", { hidden: true, "data-proposal-edit": "" }, h("label", {}, "Edited evidence proposal JSON", editing),
    h("button", { disabled: !ready || !ownVerification, onclick: () => act("edit-accept") }, "Save edited proposal"));
  const card = h("article", { class: "card ai-suggestion", "data-proposal-id": p.id, "data-proposal-revision": p.revision },
    h("h3", {}, `${assistantNames[p.capability]} v${p.version}`),
    h("a", { href: `#/case/${encodeURIComponent(p.case_id)}` }, p.case_id), status,
    h("p", { class: "ai-label" }, p.review
      ? `${p.display_state} as a draft by a person. This is not an approval, consent or safety decision. Reason: ${p.review.note || "Not supplied"}.`
      : "AI suggestion, not approved. Not an instruction."),
    h("p", { class: "muted" }, "Nothing is sent, booked, paid, ranked, signed off or released. Sources show where a statement came from, not that it is true."),
    h("p", { class: "muted" }, "Confidence: not provided. Confidence is not accuracy."),
    h("p", {}, `Invocation: ${p.provenance.filter((e) => e.kind === "invocation").map((e) => e.mode).join(", ")}. Attempts: ${p.attempts}.`),
    p.output && h("div", {}, h("p", {}, p.output.summary),
      h("ul", {}, p.output.findings.map((f) => h("li", {}, `${f.text}. Sources: ${f.citations.join(", ") || "Not provided"}`))),
      h("h4", {}, "Unknowns"), h("ul", {}, p.output.unknowns.map((u) => h("li", {}, u)))),
    h("details", {}, h("summary", {}, "Permitted sources, versions and hashes"),
      h("pre", {}, JSON.stringify(p.snapshot, null, 2))),
    h("details", {}, h("summary", {}, "AI usage and changes to this suggestion"),
      history, moreHistory),
    h("fieldset", {}, h("legend", {}, "Your review"), h("label", { for: note.id }, "Reason"), note, error,
    ready && h("div", {}, h("label", { for: `verified-${p.id}` }, verified,
      " I checked the cited sources, including unknowns and discrepancies."),
    h("button", { onclick: () => act("verify") }, "Record human source verification")),
    p.verification && h("p", {}, `Sources checked by ${p.verification.by}. ${p.verification.note}`),
    (!ready || !ownVerification) && h("p", {}, "Accept unavailable: request fresh evidence and record your own source verification first."),
    h("p", {}, "Accept proposal only. This reviews a suggestion, not the case."),
    h("div", { class: "row" },
      h("button", { disabled: !ready || !ownVerification, onclick: () => act("accept") }, "Accept"),
      h("button", { class: "alt", disabled: !ready || !ownVerification, onclick: () => { editBox.hidden = false; editing.focus(); } }, "Edit"),
      h("button", { class: "alt", onclick: () => act("reject") }, "Reject")), editBox));
  const buttons = [...card.querySelector("fieldset").querySelectorAll("button")]
    .map(button => ({ button, disabled: button.disabled }));
  card.updateReviewState = message => {
    const state = proposalReviewStates.get(reviewKey)?.state;
    buttons.forEach(({ button, disabled }) => {
      button.disabled = disabled || Boolean(state);
      if (state === "pending") button.setAttribute("aria-busy", "true");
      else button.removeAttribute("aria-busy");
    });
    if (state) status.textContent = state === "pending" ? "Recording your review..."
      : "Refresh and check the review history before another action on this revision.";
    if (message) status.textContent = message;
  };
  card.updateReviewState();
  return card;
}

function assistantCasePanel(id, session) {
  const status = h("p", { role: "status" }, "Loading assistance. Ordinary case controls remain available.");
  const panel = h("section", { class: "card" }, h("h2", {}, "Retrofit assistants"), status);
  const routeHash = location.hash.split("?")[0];
  const controller = new AbortController();
  const deadline = setTimeout(() => controller.abort(), 10000);
  const current = () => panel.isConnected && location.hash.split("?")[0] === routeHash;
  const load = async () => {
    const recoverable = new Map(proposalReviewStates);
    try {
      const [registry, queue] = await Promise.all([
        api("/api/assistants", undefined, controller.signal),
        api(`/api/assistants/proposals?case_id=${encodeURIComponent(id)}`, undefined, controller.signal),
      ]);
      if (!current()) return;
      const proposals = [...queue.proposals];
      let after = queue.next_after;
      while (after) {
        const more = await api(`/api/assistants/proposals?case_id=${encodeURIComponent(id)}&after=${encodeURIComponent(after)}`, undefined, controller.signal);
        proposals.push(...more.proposals);
        after = more.next_after;
        if (!current()) return;
      }
      status.textContent = registry.disabled ||
        `Assistance available. Proactive checks ${registry.proactive ? "enabled" : "off"}.`;
      panel.dataset.assistance = registry.disabled
        ? "AI assistance unavailable. Work continues manually."
        : "Assistance available.";
      panel.dataset.waiting = String(proposals.filter(p => p.state === "ready" && p.output && !p.stale).length);
      panel.append(h("p", {}, "These are synthetic exercise rules. Continue ordinary case work manually when assistance is disabled, failed or stale."));
      for (const a of registry.assistants) {
        session.assistantRequests ||= new Map();
        const request = h("button", { class: "alt", disabled: session.assistantRequests.has(a.id), "data-assistant-request": a.id, onclick: async () => {
          if (session.assistantRequests.has(a.id) || session.historyBarrier) return;
          session.assistantRequests.set(a.id, "pending");
          request.disabled = true;
          let recorded = false;
          try {
            await api(`/api/assistants/${a.id}/invoke`, { case_id: id });
            recorded = true;
            session.assistantRequests.set(a.id, "check-history");
            requireCaseHistory(session);
            await caseView(id);
          } catch (e) {
            const checkHistory = recorded || mutationNeedsHistory(e);
            if (checkHistory) {
              session.assistantRequests.set(a.id, "check-history");
              requireCaseHistory(session);
            } else session.assistantRequests.delete(a.id);
            if (caseSession !== session) return;
            app.querySelectorAll("[data-assistant-request]").forEach(button => {
              if (button.dataset.assistantRequest === a.id) button.disabled = checkHistory;
            });
            const message = checkHistory ? `Refresh and check proposal history before requesting again. ${e.message}` : e.message;
            if (panel.isConnected) status.textContent = message;
            else workspaceStatus.textContent = message;
          }
        } }, `Request ${assistantNames[a.id]}`);
        panel.append(request);
      }
      panel.append(h("button", { class: "alt", onclick: async () => {
        try { await caseView(id); }
        catch (error) { if (current()) status.textContent = `Could not refresh proposals. ${error.message}`; }
      } }, "Refresh proposals"),
        h("a", { href: "#/assistants" }, "Shared role-owned review queue"));
      const reviewed = h("details", {}, h("summary", {}, "Reviewed or stale suggestions"));
      for (const p of proposals) {
        const card = assistantProposal(p, () => caseView(id), recoverable);
        if (p.stale || p.review) reviewed.append(card);
        else panel.append(card);
      }
      if (reviewed.childElementCount > 1) panel.append(reviewed);
      if (!proposals.length) panel.append(h("p", {}, "No AI suggestions yet. Ordinary case work is not affected."));
      restoreBoundFields([...session.pendingFields.values()], panel, "proposal", session);
    } catch (e) {
      if (current()) {
        const reason = controller.signal.aborted ? "Assistance request timed out" : e.message;
        status.textContent = `Assistance unavailable: ${reason}. Continue ordinary case work manually.`;
        panel.dataset.assistance = "AI assistance unavailable. Work continues manually.";
        panel.dataset.waiting = "0";
        restoreBoundFields([...session.pendingFields.values()], panel, "proposal", session);
      }
    } finally {
      clearTimeout(deadline);
      controller.abort();
    }
  };
  load();
  return panel;
}

async function assistantQueueView(after = "", append = false) {
  const recoverable = new Map(proposalReviewStates);
  try {
    const queue = await api(`/api/assistants/proposals${after ? `?after=${encodeURIComponent(after)}` : ""}`);
    const cards = queue.proposals.map((p) => assistantProposal(p, () => assistantQueueView(), recoverable));
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
    if (e.name === "AbortError" || !me) return;
    show(h("h1", {}, "Assistant proposals"), h("p", { role: "alert" }, e.message),
      h("a", { href: "#/" }, "Continue manual case work"));
  }
}
