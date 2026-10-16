"use strict";

const chatLabel = "AI suggestion, not approved";
const chatProposalNames = {
  "stock-prioritisation": "Stock facts and prioritisation",
  "assessment-preparation": "Assessment preparation",
  "funding-evidence": "Funding evidence",
  "works-resident-coordination": "Works and resident coordination",
  "quality-evidence": "Quality evidence",
};

function chatMessageItem(role, text, answer) {
  const item = h("li", { class: `chat-msg chat-${role}` },
    h("strong", {}, role === "user" ? "You" : "Assistant"), " ", h("span", {}, text));
  if (answer) {
    item.append(h("p", { class: "muted" }, answer.label || chatLabel));
    if (answer.citations && answer.citations.length) {
      item.append(h("ul", { "aria-label": "Sources cited" },
        answer.citations.map((c) => h("li", {}, h("code", {}, c.id), c.text ? `: ${c.text}` : ""))));
    } else if (answer.kind === "abstain") {
      item.append(h("p", { class: "muted" }, "No permitted source answers this question."));
    } else if (answer.kind === "refused") {
      item.append(h("p", { class: "muted" }, "Outside the chat scope: use the workflow route in the reply."));
    }
  }
  return item;
}

function chatCasePanel(id) {
  let threadId = null;
  const log = h("ol", { class: "chat-log", "aria-label": "Conversation" });
  const liveLog = h("div", { role: "log", "aria-live": "polite", "aria-label": "Conversation updates" }, log);
  const status = h("p", { role: "status" }, "");
  const input = h("textarea", { id: "chat-question", maxlength: "1000", rows: "3" });
  const send = h("button", { type: "submit" }, "Ask");
  const proposals = h("div", { class: "row" });
  const say = (text) => { status.textContent = text; };
  const ensureThread = async () => {
    if (threadId) return threadId;
    threadId = (await api("/api/chat/threads", { case_id: id })).id;
    return threadId;
  };
  const ask = async (event) => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) { say("Type a question first."); return; }
    send.disabled = true;
    say("Asking the assistant. The ordinary case controls stay available.");
    log.append(chatMessageItem("user", question));
    input.value = "";
    try {
      const tid = await ensureThread();
      const answer = await api(`/api/chat/threads/${encodeURIComponent(tid)}/ask`, { content: question });
      log.append(chatMessageItem("assistant", answer.reply, answer));
      say(answer.workflow_only ? "The assistant is not available. Continue with the ordinary workflow." : "New answer added.");
    } catch (e) {
      say(`Chat unavailable: ${e.message} Continue with the ordinary case workflow.`);
    } finally { send.disabled = false; input.focus(); }
  };
  const requestProposal = async (capability) => {
    say("Requesting a proposal for independent review.");
    try {
      const tid = await ensureThread();
      await api(`/api/chat/threads/${encodeURIComponent(tid)}/proposals`, { capability });
      log.append(chatMessageItem("assistant", "Proposal requested. It needs a separate source check and role review before anything changes."));
      say("Proposal requested. Find it in the proposals panel and the review queue.");
    } catch (e) { say(`Proposal not requested: ${e.message}`); }
  };
  api("/api/assistants").then((registry) => {
    for (const a of registry.assistants || []) {
      proposals.append(h("button", { type: "button", class: "alt", onclick: () => requestProposal(a.id) },
        `Request proposal: ${chatProposalNames[a.id] || a.id}`));
    }
  }).catch(() => {});
  return h("details", { class: "card", id: "chat-panel" },
    h("summary", {}, "Ask the assistant about this case (optional)"),
    h("p", { class: "muted" }, `${chatLabel}. Answers cite only sources your role may see. The assistant cannot change a record, approve, send or book anything; it can only request a proposal that someone else reviews. Do not type personal details about residents.`),
    liveLog,
    h("form", { onsubmit: ask }, h("label", { for: "chat-question" }, "Your question"), input, send),
    proposals, status, regulatoryChatPanel(id));
}

const regulatoryRoleHelp = {
  "Resident Liaison Officer": "Repairs and intake: recognise a possible hazard and use the human hazard service immediately. Record the reported awareness time without guessing. Do not wait for chat or a check.",
  "Building Safety Liaison": "Building Safety: review hazard categorisation, recorded clocks and independent evidence. Completion is not safety assurance; only an authorised human can decide a hold.",
  "Retrofit Coordinator": "Assessment and coordination: check appointed roles, risk path and independent evidence. Only a PAS 2035 overview is held; licensed text and contract incorporation are unverified.",
  "Quality Inspector": "Assessment and quality: check independent evidence and the appointed coordinator's review. Completion is not assurance. Licensed PAS 2035 text and contract incorporation are unverified.",
  "Retrofit Programme Manager": "Programme: distinguish policy targets from duties in force. Check source status and dependencies before planning; a target or allocation is not an approved commitment or award.",
  "Programme Support Officer": "Programme support: check the current step, evidence and named owner. Do not treat a policy target as an active duty, or a completed task as assurance.",
  "Grants and Evidence Officer": "Finance and grants: obtain the actual award letter and grant agreement. An allocation annex is not authority to claim. No commitment, signature or submission is made by chat.",
};

function regulatoryGuidance(role) {
  return h("div", { class: "regulatory-guidance" },
    h("p", {}, regulatoryRoleHelp[role] || "Recognise the trigger, preserve evidence and ask the named human owner. This guidance grants no additional permissions."),
    h("p", {}, "For everyone handling data: use only the necessary resident information. Health and vulnerability information needs special care. Consent is not the same as another lawful basis. Significant decisions need meaningful human involvement; ask the DPO owner if unsure."),
    h("p", {}, "In doubt: Juan Manuel Servera is the exercise Legal, Compliance and DPO owner, for synthetic-demo review only. Real safety, consent, finance and legal decisions remain with the relevant authorised humans. No operational approval is claimed."));
}

function regulatoryPlainMode(root, id) {
  const input = h("input", { type: "checkbox", id, checked: true });
  root.classList.add("regulatory", "plain-language");
  input.addEventListener("change", () => root.classList.toggle("plain-language", input.checked));
  return h("label", { class: "regulatory-mode", for: id }, input, " Plain-language explanations");
}

function regulatorySources(citations) {
  const list = h("ul", { "aria-label": "Provision and fact citations" });
  if (!citations?.length) list.append(h("li", {}, "No source held for this answer. Do not infer a duty or terms; ask the named human owner."));
  for (const source of citations || []) {
    const link = `/api/law/provisions/${encodeURIComponent(source.id)}`;
    list.append(h("li", {},
      source.source_id || source.link?.startsWith("/api/law/provisions/") ? h("a", { href: link, target: "_blank", rel: "noopener" }, `${source.id} (source record, opens new tab)`) : h("code", {}, source.id),
      ` | Status: ${source.status || "unknown"} | Effective: ${source.effective || "unknown"} | Retrieved/observed: ${source.retrieved || "unknown"}`,
      source.review_status ? ` | Review: ${source.review_status}` : "",
      source.completeness ? ` | Completeness: ${source.completeness}` : "",
      source.currentness ? ` | ${source.currentness}` : "",
      source.excerpt_truncated ? " | Short excerpt; open source record for the full provision." : ""));
  }
  return list;
}

function regulatoryAlertsPanel(caseId) {
  const root = h("section", { class: "card", id: "regulatory-alerts", "aria-labelledby": "regulatory-alerts-title" });
  const status = h("p", { role: "status", "aria-atomic": "true" }, "Loading role-scoped alerts. Coverage is unknown.");
  const list = h("div", { class: "regulatory-alert-list" });
  const meanings = {
    "breach risk": "A recorded check needs urgent human review. This is not a legal finding.",
    attention: "A recorded trigger needs human attention.",
    unknown: "Evidence is missing or cannot be relied on. Do not treat this as clear.",
    clear: "This bounded check is clear; it does not establish compliance.",
    "not applicable": "This check did not apply to the recorded evidence; it is not a legal decision.",
  };
  const refresh = h("button", { type: "button", class: "alt", onclick: load }, "Refresh alerts");
  async function load() {
    refresh.disabled = true;
    status.textContent = "Loading role-scoped alerts. Coverage is unknown.";
    try {
      const data = await api(`/api/law/alerts?case=${encodeURIComponent(caseId)}`);
      const alerts = (data.homes || []).flatMap((home) => home.alerts);
      list.replaceChildren(...alerts.map((alert) => h("article", { class: "regulatory-alert" },
        h("h3", {}, `Status: ${alert.result}`),
        h("p", { class: "plain-explanation" }, meanings[alert.result] || meanings.unknown),
        alert.exercise && h("p", {}, "synthetic-demo: fictional exercise control, not law or operational approval."),
        h("dl", {},
          h("dt", {}, "What was noticed"), h("dd", {}, alert.noticed || "Unknown"),
          h("dt", {}, "Safe action"), h("dd", {}, alert.safe_action || "Use the human owner route; do not infer an action."),
          h("dt", {}, "Decision owner"), h("dd", {}, `${alert.decision_owner || "Unassigned"}; route: ${alert.escalation_role || "unknown"}`),
          h("dt", {}, "Clock"), h("dd", {}, `${alert.clock || "No approved clock held"}; due: ${alert.due_at || "unknown, not calculated here"}`),
          h("dt", {}, "Check snapshot"), h("dd", {}, `${alert.at || "unknown"}; step: ${alert.step || "unknown"}; card: ${alert.card_id}@${alert.card_version}`),
          h("dt", {}, "Current control"), h("dd", {}, alert.active_control ? "Active bounded control" : "Not active or source uncertain; retained risk still needs human review"),
          h("dt", {}, "Latest check"), h("dd", {}, `${alert.latest_result || "unknown"} at ${alert.latest_evaluated_at || "unknown"}`)),
        h("h4", {}, "Source and status"), regulatorySources(alert.citations),
        h("p", {}, `Owner acknowledgement: ${alert.requires_acknowledgement ? "required" : "not outstanding"}. Owner outcome: ${alert.requires_outcome ? "required" : "not outstanding"}. This panel cannot acknowledge, decide compliance or release a hold.`))));
      status.textContent = `${alerts.length} visible alerts. Coverage: ${data.coverage_status || "unknown"}. ${alerts.length ? "Only alerts permitted for your role are shown." : "No visible alerts does not mean no risk, complete coverage or compliance."}`;
    } catch (e) {
      list.replaceChildren();
      status.textContent = `Alert coverage unknown: ${e.message} Use the existing human emergency or hazard service; do not wait for checks.`;
    } finally { refresh.disabled = false; }
  }
  root.append(h("h2", { id: "regulatory-alerts-title" }, "Regulatory alerts for this home"),
    h("p", { class: "notice" }, "Possible emergency or hazard? Use the existing human emergency or hazard service now. Do not wait for alerts, chat or this application. No resident message is sent."),
    regulatoryPlainMode(root, "alerts-plain-mode"),
    regulatoryGuidance(me.user.role), status, list, refresh);
  load();
  return root;
}

function regulatoryChatPanel(caseId) {
  const root = h("details", { id: "regulatory-chat" },
    h("summary", {}, "Cited regulatory lookup (synthetic-demo)"));
  const status = h("p", { role: "status" });
  const privacy = h("p", { id: "regulatory-privacy", class: "muted" },
    "Synthetic data only. Do not enter resident personal or special-category details. DPIA and retention review remain incomplete.");
  const log = h("ol", { "aria-label": "Cited regulatory turns" });
  const liveLog = h("div", { role: "log", "aria-live": "polite", "aria-label": "Cited regulatory updates" }, log);
  const input = h("textarea", { id: "regulatory-question", maxlength: "1000", rows: "3", "aria-describedby": "regulatory-privacy" });
  const button = h("button", { type: "submit" }, "Look up cited sources");
  let tid = null;
  const show = (answer, thread) => {
    const sections = answer.sections;
    const item = h("li", { class: "regulatory-turn" },
      h("h3", {}, `Lookup status: ${answer.kind}`),
      h("p", {}, answer.label || "synthetic-demo: not legal advice or approval"));
    if (sections) {
      item.append(h("h4", {}, "What the sources say"),
        h("p", { class: "plain-explanation" }, "These are exact excerpts, not a decision about which duty applies. Check the source status and dates."),
        ...sections.what_sources_say.map((source) => h("blockquote", {}, `[${source.citation}] ${source.quote}`)),
        h("h4", {}, "Recorded home facts"),
        ...sections.recorded_home_facts.map((fact) => h("p", {}, `[${fact.id}] ${fact.text}`)),
        h("h4", {}, "Unknown or missing"),
        h("ul", {}, sections.unknown_or_missing.map((text) => h("li", {}, text))),
        h("h4", {}, "Safe next action"), h("p", {}, sections.safe_next_action),
        h("h4", {}, "Who decides"), h("p", {}, sections.who_decides));
    } else item.append(h("p", {}, answer.reply));
    const citations = regulatorySources(answer.citations);
    for (const card of answer.cards || []) {
      const freshness = card.source_freshness;
      citations.append(h("li", {},
        h("a", { href: card.link, target: "_blank", rel: "noopener" }, card.id),
        ` | ${freshness?.label || "Historical source monitoring cadence unknown."} | as of: ${freshness?.as_of || "unknown"}`));
    }
    const doubt = h("button", { type: "button", class: "alt", onclick: async () => {
      if (doubt.getAttribute("aria-disabled") === "true") return;
      doubt.setAttribute("aria-disabled", "true");
      try {
        const receipt = await api(`/api/chat/regulatory/threads/${encodeURIComponent(thread)}/doubt`, { turn: answer.turn });
        status.textContent = `${receipt.label}: sent to ${receipt.owner}'s exercise inbox. No legal approval or resident message.`;
        doubt.textContent = "Sent to exercise owner; awaiting human review";
      } catch (e) {
        status.textContent = `Doubt route failed: ${e.message}`;
        doubt.removeAttribute("aria-disabled");
      }
    } }, "In doubt: send this turn to Juan Manuel Servera");
    item.append(citations, doubt);
    log.append(item);
  };
  root.append(h("p", {}, "synthetic-demo only. Exact source excerpts and recorded facts, not legal interpretation. Ask about hazard sources or automated decisions. Safety routes and deterministic alerts remain independent."),
    privacy,
    regulatoryPlainMode(root, "chat-plain-mode"),
    h("p", { class: "plain-explanation" }, "Use short questions to find sources. Missing, conflicting, stale or future sources are not proof of a duty. For lease, grant or contract terms, obtain the actual document and ask the named human owner."),
    regulatoryGuidance(me.user.role),
    liveLog, h("form", { onsubmit: async (event) => {
      event.preventDefault();
      const question = input.value.trim();
      if (!question) { status.textContent = "Enter a source question."; return; }
      button.disabled = true;
      status.textContent = "Looking up cited sources. Human safety routes remain available.";
      try {
        if (!tid) tid = (await api("/api/chat/regulatory/threads", { case_id: caseId })).id;
        const answer = await api(`/api/chat/regulatory/threads/${encodeURIComponent(tid)}/ask`, { content: question });
        log.append(h("li", {}, h("strong", {}, "You"), " ", question));
        show(answer, tid);
        status.textContent = `${answer.kind}: synthetic-demo turn stored with its sources.`;
        if (input.value.trim() === question) input.value = "";
      } catch (e) { status.textContent = `Cited lookup unavailable: ${e.message} Use the ordinary human route.`; }
      finally { button.disabled = false; input.focus(); }
    } }, h("label", { for: "regulatory-question" }, "Cited source question"), input, button),
    h("button", { type: "button", class: "alt", onclick: async () => {
      try {
        const inbox = await api("/api/chat/regulatory/inbox");
        const here = inbox.threads.filter((thread) => thread.case_id === caseId);
        for (const thread of here) {
          const turn = thread.messages[1];
          const answer = JSON.parse(turn.content);
          log.append(h("li", {}, h("strong", {}, "Exercise doubt inbox"),
            h("p", {}, thread.messages[0].content), h("p", { class: "regulatory-excerpt" }, answer.reply)));
        }
        status.textContent = `${here.length} synthetic-demo referrals for this home. No decision recorded.`;
      } catch (e) { status.textContent = `Exercise inbox unavailable: ${e.message}`; }
    } }, "Open my exercise doubt inbox (named owner only)"), status);
  api("/api/chat/regulatory/status").then(async (admission) => {
    status.textContent = "Synthetic source lookup available. No legal approval is implied.";
    const schedule = admission.privacy.chat;
    privacy.textContent = `${admission.warning} DPIA: draft for DPO review. Retention: ${schedule.status === "simulated" ? `${schedule.days} days (simulated only)` : "unknown, DPO period not set"}. No automatic deletion or operational approval.`;
    try {
      const threads = await api("/api/chat/threads");
      const latest = threads.find((thread) => thread.case_id === caseId &&
        thread.title === "regulatory-home-chat: synthetic-demo");
      if (!latest) return;
      const history = await api(`/api/chat/regulatory/threads/${encodeURIComponent(latest.id)}`);
      tid = history.id;
      for (const turn of history.messages) {
        if (turn.role === "user") log.append(h("li", {}, h("strong", {}, "You"), " ", turn.content));
        else {
          const answer = JSON.parse(turn.content);
          if (answer.schema === "regulatory-chat-v1") show({ ...answer, turn: turn.seq }, tid);
        }
      }
      status.textContent = "Stored synthetic-demo excerpts restored. Dates are historical snapshots; ask again for a fresh lookup.";
    } catch (e) { status.textContent = `Stored regulatory chat unavailable: ${e.message}`; }
  }).catch((e) => {
    input.disabled = true;
    button.disabled = true;
    status.textContent = `Cited lookup unavailable: ${e.message} Continue with the human owner route; safety and alerts do not depend on chat.`;
  });
  return root;
}
