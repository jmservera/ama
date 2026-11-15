"use strict";

// Keeps a message that already names an owner and a next action; otherwise adds both.
const assistantOwned = (message, owner, next, status) => {
  const m = String(message ?? "").trim().replace(/([^.!?])$/, "$1.");
  const o = m.indexOf("Owner:");
  if (o >= 0 && m.indexOf("Next action:") > o) return m;
  const refused = status >= 400 && status < 500;
  return `${m} Owner: ${refused ? "your team manager" : owner}. Next action: ${refused ? "follow the advice above, or ask your team manager if you cannot" : next}`;
};
const ASSISTANT_SUPPORT = "application support";

const assistantNames = {
  "stock-prioritisation": "Stock facts and prioritisation",
  "assessment-preparation": "Assessment preparation",
  "funding-evidence": "Funding evidence",
  "works-resident-coordination": "Works and resident coordination",
  "quality-evidence": "Quality evidence",
};
const proposalReviewStates = new Map();

const FLAG_TITLES = { "review-suggested": "Review suggested by the model (automatic review flag, level L4)", "manual-proposal": "Requested by a person: not an automatic flag",
  "uncited": "No retained reading cited: not a flag", "rejected": "Rejected by a person: not a flag", "reviewed": "Reviewed by a person: not a flag",
  "not-current": "No longer current: not a flag", "withheld": "Withheld: monitoring consent is not granted now" };

function reviewFlagBlock(f) {
  const model = f.model ? `${f.model.provider || "unknown"} ${f.model.deployment || ""} ${f.model.model || ""}`.trim() : "not shown";
  const kids = [h("h4", {}, FLAG_TITLES[f.status] || "Not a flag")];
  if (f.status !== "withheld") {
    const asOf = f.evidence_as_of ? `Evidence as of ${f.evidence_as_of}, ${f.freshness || "unknown"}${f.age_minutes == null ? "" : `, ${f.age_minutes} minutes old at capture`}.`
      : "Evidence as-of time unknown: do not treat these readings as live.";
    const cmp = f.cited_comparison || {};
    const extra = f.newer_reading_count ? ` ${f.newer_reading_count} additional reading${f.newer_reading_count === 1 ? "" : "s"} not cited by this finding ${f.newer_reading_count === 1 ? "is" : "are"} now in the current capture.` : "";
    const change = f.changed_since_capture == null ? "Whether the cited readings have changed since capture is unknown."
      : f.changed_since_capture ? `The current authorised capture differs from the readings this finding cited: ${(cmp.changed_ids || []).length} changed and ${(cmp.missing_ids || []).length} not in the current bounded capture (they may still be stored). Review the current readings.${extra}`
        : `The current authorised capture still includes the readings this finding cited, with the same values.${extra}`;
    kids.push(h("p", {}, `Model: ${model}. Raised ${f.source_time || "at an unknown time"} (${f.trigger}). Not approved.`),
      h("p", {}, `${asOf} ${change}`),
      h("p", {}, `Cited IDs: ${(f.cited_ids || []).join(", ") || "none"}. Readings cited: ${(f.readings || []).map((r) => `sensor ${r.sensor_id}, reading ${r.reading_id}`).join("; ") || "none"}.`),
      h("p", {}, `Reading source: ${(f.provenance_classes || []).join(", ") || "none"}. Not calibrated.`),
      h("p", { class: "muted" }, f.delivery));
  }
  kids.push(h("p", { class: "muted" }, f.effect));
  return h("div", { class: "card", role: "group", "aria-label": "Review flag status" }, ...kids);
}

function assistantProposal(p, reload, recoverable = new Map(), session = caseSession) {
  const reviewKey = `${p.id}:${p.revision}`;
  const previous = proposalReviewStates.get(reviewKey);
  if (previous?.state === "uncertain" && recoverable.get(reviewKey) === previous) proposalReviewStates.delete(reviewKey);
  const status = h("p", { role: "status" }, `${p.display_state}. ${p.release_denial ? p.release_denial.reason : (p.reason || "")} ${p.manual}`);
  const note = h("textarea", { id: `proposal-reason-${p.id}`, name: "review-reason", autocomplete: "off", "aria-label": "Reason", maxlength: "1000" });
  const error = h("p", { id: `proposal-error-${p.id}`, class: "field-error", role: "status" });
  const verified = h("input", { type: "checkbox", id: `verified-${p.id}` });
  const editing = h("textarea", { name: "edited-proposal", autocomplete: "off", "aria-label": "Edited proposal (technical JSON format)", maxlength: "16000" },
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
    const sent = snapshotCaseFields([note, ...(action === "verify" ? [verified] : action === "edit-accept" ? [editing] : [])], session);
    setReviewState("pending");
    status.textContent = "Recording your review...";
    let recorded = false;
    try {
      await api(`/api/assistants/proposals/${p.id}/review`, body);
      recorded = true;
      setReviewState("recorded");
      reconcileCaseSubmission(sent, session === me.assistantQueueDrafts ? session : caseSession);
      await reload();
    } catch (e) {
      const checkHistory = mutationNeedsHistory(e);
      const message = recorded
        ? assistantOwned(`Your review was recorded, but suggestions could not reload. Refresh before another review. ${e.message}`, ASSISTANT_SUPPORT, "refresh and check the review history before another review")
        : checkHistory ? assistantOwned(`Confirmation is unavailable. Refresh and check the review history before another action. ${e.message}`, ASSISTANT_SUPPORT, "refresh and check the review history before another action") : assistantOwned(e.message, ASSISTANT_SUPPORT, "correct the entries or refresh, then try again", e.status);
      setReviewState(recorded ? "recorded" : checkHistory ? "uncertain" : null, message);
    }
  };
  const ready = p.state === "ready" && !p.stale && p.actionable !== false
    && !p.release_denial && p.epoch_current !== false;
  const ownVerification = p.verification && p.verification.by === me.user.email;
  const history = h("pre", { tabindex: "0", "aria-label": "Changes to this suggestion, technical record" }, JSON.stringify({ envelope: p.envelope, history: p.provenance }, null, 2));
  let offset = p.history_next_offset;
  const moreHistory = h("button", { class: "alt", hidden: offset == null, onclick: async () => {
    try {
      const earlier = await api(`/api/assistants/proposals/${p.id}?history_offset=${offset}`);
      history.append(document.createTextNode("\n" + JSON.stringify(earlier.provenance, null, 2)));
      offset = earlier.history_next_offset;
      moreHistory.hidden = offset == null;
    } catch (e) { status.textContent = assistantOwned(e.message, ASSISTANT_SUPPORT, "refresh to try again, then tell application support if it continues", e.status); }
  } }, "Earlier changes to this suggestion");
  const editBox = h("div", { hidden: true, "data-proposal-edit": "" }, h("p", { class: "muted" }, "This is the full proposal in a technical format. Change the values and keep the structure. A reason is required."),
    h("label", {}, "Edited proposal (technical JSON format)", editing),
    h("button", { disabled: !ready || !ownVerification, onclick: () => act("edit-accept") }, "Save edited proposal"));
  const card = h("article", { class: "card ai-suggestion", "data-proposal-id": p.id, "data-proposal-revision": p.revision },
    h("h3", {}, `${assistantNames[p.capability]} v${p.version}`),
    h("a", { href: `#/case/${encodeURIComponent(p.case_id)}` }, p.case_id), status,
    h("p", { class: "ai-label" }, p.review
      ? `${p.display_state} as a draft by a person. This is not an approval, consent or safety decision. Reason: ${p.review.note || "Not supplied"}.`
      : "AI suggestion, not approved. Not an instruction."),
    h("p", { class: "muted" }, "Nothing is sent, booked, paid, ranked, signed off or released. Sources show where a statement came from, not that it is true."),
    h("p", { class: "muted" }, "Confidence: not provided. Confidence is not accuracy."),
    h("p", {}, "Accepting or editing this proposal records a draft review. This is not an approval, consent or safety decision."),
    h("p", {}, `Requested using: ${p.provenance.filter((e) => e.kind === "invocation").map((e) => e.mode).join(", ")}. Attempts: ${p.attempts}.`),
    p.review_flag && reviewFlagBlock(p.review_flag),
    p.output && h("div", {}, h("p", {}, p.output.summary),
      h("ul", {}, p.output.findings.map((f) => h("li", {}, `${f.text}. Sources: ${f.citations.join(", ") || "Not provided"}`))),
      h("h4", {}, "Unknowns"), h("ul", {}, p.output.unknowns.map((u) => h("li", {}, u)))),
    h("details", { "data-proposal-technical": "" }, h("summary", {}, "Suggestion details (technical, for audit and support)"),
      h("p", { class: "muted" }, "The full technical record of this suggestion is kept here unchanged. The reasons, warnings and review choices on this card do not depend on it."),
      h("h4", {}, "Permitted sources, versions and hashes"),
      h("pre", { tabindex: "0", "aria-label": "Permitted sources, versions and hashes, technical record" }, JSON.stringify(p.snapshot, null, 2)),
      h("h4", {}, "AI usage and changes to this suggestion"),
      history, moreHistory),
    h("fieldset", {}, h("legend", {}, "Your review"), h("label", { for: note.id }, "Reason"), note, error,
    ready && h("div", {}, h("label", { for: `verified-${p.id}` }, verified,
      " I checked the cited sources, including unknowns and discrepancies."),
    h("button", { onclick: () => act("verify") }, "Record human source verification")),
    p.verification && h("p", {}, `Sources checked by ${p.verification.by}. ${p.verification.note}`),
    (!ready || !ownVerification) && h("p", {}, "Accept unavailable: request fresh evidence and record your own source verification first. Owner: the reviewer. Next action: request fresh evidence, record your own source verification, then accept."),
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

const ASSISTANTS_NOT_FOR_ROLE = "AI assistance is not available for your role. Use the ordinary case controls; no one is waiting on a suggestion. Owner: your team manager. Next action: ask your team manager if you need AI assistance, and carry on with the ordinary case controls.";

function assistantCasePanel(id, session) {
  const status = h("p", { role: "status" }, "Loading assistance. Ordinary case controls remain available.");
  const panel = h("section", { class: "card" }, h("h2", {}, "Retrofit assistants"), status);
  if (me?.services?.assistants === false) {
    status.textContent = ASSISTANTS_NOT_FOR_ROLE;
    panel.dataset.assistance = "AI assistance unavailable. Work continues manually.";
    panel.dataset.waiting = "0";
    return panel;
  }
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
      panel.dataset.waiting = String(proposals.filter(p => p.state === "ready" && p.output && (!p.stale || p.review_flag?.status === "review-suggested")).length);
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
            const message = checkHistory ? assistantOwned(`Refresh and check proposal history before requesting again. ${e.message}`, ASSISTANT_SUPPORT, "refresh and check the proposal history before requesting again") : assistantOwned(e.message, ASSISTANT_SUPPORT, "refresh to try again, then tell application support if it continues", e.status);
            if (panel.isConnected) status.textContent = message;
            else workspaceStatus.textContent = message;
          }
        } }, `Request ${assistantNames[a.id]}`);
        panel.append(request);
      }
      panel.append(h("button", { class: "alt", onclick: async () => {
        try { await caseView(id); }
        catch (error) { if (current()) status.textContent = assistantOwned(`Could not refresh proposals. ${error.message}`, ASSISTANT_SUPPORT, "refresh again, then tell application support if it continues", error.status); }
      } }, "Refresh proposals"),
        h("a", { href: "#/assistants" }, "Shared role-owned review queue"));
      const reviewed = h("details", {}, h("summary", {}, "Reviewed or stale suggestions"));
      for (const p of proposals) {
        const card = assistantProposal(p, () => caseView(id), recoverable);
        if ((p.stale && p.review_flag?.status !== "review-suggested") || p.review) reviewed.append(card);
        else panel.append(card);
      }
      if (reviewed.childElementCount > 1) panel.append(reviewed);
      if (!proposals.length) panel.append(h("p", {}, "No AI suggestions yet. Ordinary case work is not affected."));
      else panel.append(h("p", {}, h("a", { class: "btn alt", href: `/api/assistants/proposals.csv?case_id=${encodeURIComponent(id)}`, download: "assistant-proposals.csv" }, "Download suggestions for Excel"), " The file is a read-only copy; changes in it are not imported back."));
      restoreBoundFields([...session.pendingFields.values()], panel, "proposal", session);
    } catch (e) {
      if (current()) {
        const reason = controller.signal.aborted ? "Assistance request timed out" : e.message;
        status.textContent = assistantOwned(`Assistance unavailable: ${reason}. Continue ordinary case work manually.`, ASSISTANT_SUPPORT, "continue ordinary case work manually, and tell application support if it continues");
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
  const owner = me;
  if (owner.services?.assistants === false) {
    show(h("div", { "data-assistant-queue": "" }, h("h1", {}, "Role-owned assistant proposals"),
      h("p", { role: "status" }, ASSISTANTS_NOT_FOR_ROLE)));
    return;
  }
  const session = owner.assistantQueueDrafts ||= { pendingFields: new Map() };
  const signal = routeController.signal;
  const recoverable = new Map(proposalReviewStates);
  try {
    const queue = await api(`/api/assistants/proposals${after ? `?after=${encodeURIComponent(after)}` : ""}`);
    if (signal.aborted || me !== owner || owner.assistantQueueDrafts !== session) return;
    const existing = app.querySelector("[data-assistant-queue]");
    if (existing) rememberCaseFields(session);
    const cards = queue.proposals.map((p) => assistantProposal(p, () => assistantQueueView(), recoverable, session));
    const more = queue.next_after && h("button", { onclick: async (e) => {
      e.currentTarget.remove();
      await assistantQueueView(queue.next_after, true);
    } }, "Show more proposals");
    if (append && existing) {
      existing.querySelectorAll('[data-case-recovery="proposal"]').forEach(node => node.remove());
      existing.append(...cards, ...(more ? [more] : []));
      restoreBoundFields([...session.pendingFields.values()], existing, "proposal", session);
      return;
    }
    const panel = h("div", { "data-assistant-queue": "" }, h("h1", {}, "Role-owned assistant proposals"),
      h("p", { role: "status" }, queue.disabled || "Unreviewed proposals require a separate source check and role review."),
      h("button", { onclick: () => assistantQueueView() }, "Refresh queue"),
      ...cards, more,
      h("p", {}, h("a", { class: "btn alt", href: "/api/assistants/proposals.csv", download: "assistant-proposals.csv" }, "Download all proposals for Excel"), " The file is a read-only copy; changes in it are not imported back."),
      !queue.proposals.length && h("p", {}, "No proposals in your current role and case scope. Use the ordinary case controls."));
    show(panel);
    restoreBoundFields([...session.pendingFields.values()], panel, "proposal", session);
  } catch (e) {
    if (e.name === "AbortError" || signal.aborted || me !== owner || owner.assistantQueueDrafts !== session) return;
    const failure = h("div", { "data-queue-error": "" }, h("p", { role: "alert" }, assistantOwned(e.message, ASSISTANT_SUPPORT, "try loading proposals again, or continue manual case work and tell application support if it continues", e.status)),
      h("button", { type: "button", onclick: () => assistantQueueView() }, "Try loading proposals again"),
      h("a", { href: "#/" }, "Continue manual case work"));
    const existing = app.querySelector("[data-assistant-queue]");
    if (existing) {
      existing.querySelector("[data-queue-error]")?.remove();
      existing.append(failure);
    } else {
      const panel = h("div", { "data-assistant-queue": "" }, h("h1", {}, "Assistant proposals"), failure);
      show(panel);
      restoreBoundFields([...session.pendingFields.values()], panel, "proposal", session);
    }
  }
}
