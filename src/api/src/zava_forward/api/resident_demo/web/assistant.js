"use strict";
(function () {
  function node(tag, text) {
    var item = document.createElement(tag);
    if (text) item.textContent = text;
    return item;
  }

  window.mountResidentAssistant = function (content, api, sessionExpired) {
    var panel = node("section");
    panel.className = "card assistant";
    panel.setAttribute("aria-labelledby", "assistant-title");
    var title = node("h2", "Help with your case");
    title.id = "assistant-title";
    panel.appendChild(title);
    var notice = node("p", "Advisory only. This assistant cannot submit forms, give consent, book works or make decisions.");
    notice.id = "assistant-notice";
    panel.appendChild(notice);
    panel.appendChild(node("p", "Summary by rules. No AI model is connected. Choose a question below. This panel does not store or send messages to staff."));
    var form = node("form");
    var label = node("label", "Your question");
    label.htmlFor = "assistant-topic";
    form.appendChild(label);
    var select = node("select");
    select.id = "assistant-topic";
    select.name = "topic";
    select.autocomplete = "off";
    select.setAttribute("aria-describedby", "assistant-notice");
    [
      ["status", "Where is my case now?"],
      ["documents", "Which documents should I send?"],
      ["forms", "How can I fill in a form?"]
    ].forEach(function (item) {
      var option = node("option", item[1]);
      option.value = item[0];
      select.appendChild(option);
    });
    form.appendChild(select);
    var actions = node("div");
    actions.className = "actions";
    var button = node("button", "Get advice");
    button.type = "submit";
    actions.appendChild(button);
    form.appendChild(actions);
    panel.appendChild(form);
    var status = node("p");
    status.className = "status";
    status.id = "assistant-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    panel.appendChild(status);
    var result = node("div");
    result.id = "assistant-result";
    result.setAttribute("aria-live", "polite");
    panel.appendChild(result);
    panel.appendChild(node("p", "A person can help instead. Speak to your housing officer, or write to or visit your local office."));
    content.appendChild(panel);

    var busy = false;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (busy) return;
      busy = true;
      button.setAttribute("aria-disabled", "true");
      select.disabled = true;
      result.textContent = "";
      status.textContent = "Getting your advice\u2026";
      api("/demo/assistant", { method: "POST", body: JSON.stringify({ topic: select.value }) })
        .then(function (response) {
          if (!panel.isConnected || content.hidden) return;
          if (response.status === 401) { sessionExpired("Please sign in again."); return; }
          status.textContent = "";
          if (!response.ok) {
            status.textContent = response.body.error || "The assistant is not available. Try again or ask your housing officer.";
            return;
          }
          result.appendChild(node("p", response.body.label));
          result.appendChild(node("p", response.body.answer));
          result.appendChild(node("h3", "Sources"));
          var sources = node("ul");
          response.body.sources.forEach(function (source) { sources.appendChild(node("li", source)); });
          result.appendChild(sources);
        })
        .catch(function () {
          if (panel.isConnected && !content.hidden) {
            status.textContent = "We could not reach the assistant. Check your connection, then try again or ask your housing officer.";
          }
        })
        .then(function () {
          busy = false;
          button.removeAttribute("aria-disabled");
          select.disabled = false;
        });
    });
  };
})();
