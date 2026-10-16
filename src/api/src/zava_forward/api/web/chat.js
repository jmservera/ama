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
  const log = h("ol", { class: "chat-log", role: "log", "aria-live": "polite", "aria-label": "Conversation" });
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
    log,
    h("form", { onsubmit: ask }, h("label", { for: "chat-question" }, "Your question"), input, send),
    proposals, status, regulatoryChatPanel(id));
}

function regulatoryChatPanel(caseId) {
  const root = h("details", { hidden: true },
    h("summary", {}, "Cited regulatory lookup (synthetic-demo)"));
  const status = h("p", { role: "status" });
  const log = h("ol", { role: "log", "aria-live": "polite", "aria-label": "Cited regulatory turns" });
  const input = h("textarea", { id: "regulatory-question", maxlength: "1000", rows: "3" });
  const button = h("button", { type: "submit" }, "Look up cited sources");
  let tid = null;
  const show = (answer, thread) => {
    const item = h("li", {}, h("pre", {}, answer.reply));
    const citations = h("ul", { "aria-label": "Provision and fact citations" });
    for (const source of answer.citations) {
      citations.append(h("li", {},
        source.link ? h("a", { href: source.link, target: "_blank", rel: "noopener" }, source.id) : h("code", {}, source.id),
        ` | ${source.status} | effective: ${source.effective || "unknown"} | retrieved/observed: ${source.retrieved}`));
    }
    for (const card of answer.cards) {
      const freshness = card.source_freshness;
      citations.append(h("li", {},
        h("a", { href: card.link, target: "_blank", rel: "noopener" }, card.id),
        ` | ${freshness?.label || "Historical source monitoring cadence unknown."} | as of: ${freshness?.as_of || "unknown"}`));
    }
    const doubt = h("button", { type: "button", class: "alt", onclick: async () => {
      doubt.disabled = true;
      try {
        const receipt = await api(`/api/chat/regulatory/threads/${encodeURIComponent(thread)}/doubt`, { turn: answer.turn });
        status.textContent = `${receipt.label}: sent to ${receipt.owner}'s exercise inbox. No legal approval or resident message.`;
      } catch (e) {
        status.textContent = `Doubt route failed: ${e.message}`;
        doubt.disabled = false;
      }
    } }, "In doubt: send this turn to Juan Manuel Servera");
    item.append(citations, doubt);
    log.append(item);
  };
  root.append(h("p", {}, "synthetic-demo only. Exact source excerpts and recorded facts, not legal interpretation. Ask about hazard sources or automated decisions. Safety routes and deterministic alerts remain independent."),
    log, h("form", { onsubmit: async (event) => {
      event.preventDefault();
      if (!input.value.trim()) { status.textContent = "Enter a source question."; return; }
      button.disabled = true;
      try {
        if (!tid) tid = (await api("/api/chat/regulatory/threads", { case_id: caseId })).id;
        const answer = await api(`/api/chat/regulatory/threads/${encodeURIComponent(tid)}/ask`, { content: input.value });
        show(answer, tid);
        status.textContent = `${answer.kind}: synthetic-demo turn stored with its sources.`;
        input.value = "";
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
            h("p", {}, thread.messages[0].content), h("pre", {}, answer.reply)));
        }
        status.textContent = `${here.length} synthetic-demo referrals for this home. No decision recorded.`;
      } catch (e) { status.textContent = `Exercise inbox unavailable: ${e.message}`; }
    } }, "Open my exercise doubt inbox (named owner only)"), status);
  api("/api/chat/regulatory/status").then(async () => {
    root.hidden = false;
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
  }).catch(() => {});
  return root;
}
