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
    proposals, status);
}
