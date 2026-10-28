"use strict";
(function () {
  function node(tag, text) {
    var item = document.createElement(tag);
    if (text) item.textContent = text;
    return item;
  }

  function checkbox(parent, id, text) {
    var label = node("label");
    label.className = "check";
    var input = node("input");
    input.id = id;
    input.name = id;
    input.type = "checkbox";
    label.appendChild(input);
    label.appendChild(node("span", text));
    parent.appendChild(label);
    return input;
  }

  var dates = new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium", timeStyle: "short", timeZone: "Europe/London"
  });
  function when(slot) {
    return dates.format(new Date(slot.start)) + " to " +
      dates.format(new Date(slot.end)) + " (UK time)";
  }

  window.mountResidentAppointments = function (parent, api, expired) {
    var active = true;
    var busy = false;
    var generation = 0;
    var title = node("h2", "Synthetic callbacks");
    title.id = "callback-title";
    title.tabIndex = -1;
    parent.appendChild(title);
    var notice = "Synthetic callback only. Nobody will call you. This is not a works booking or consent to works.";
    parent.appendChild(node("p", notice));
    parent.appendChild(node("p", "Use this manual form without chat or AI. Choose dates and times that suit you. Ask a person about access needs or adjustments."));
    parent.appendChild(node("p", "To book or cancel with a person, phone your housing officer using your usual number, or write to or visit your local office. Quote the callback reference if you have one."));
    var consent = checkbox(parent, "callback-consent", "Use my own record to find, check or change my synthetic callbacks.");
    consent.setAttribute("aria-describedby", "callback-status");
    var form = node("form");
    var dateLabel = node("label", "Earliest callback date (UK time)");
    dateLabel.htmlFor = "callback-date";
    var date = node("input");
    date.id = "callback-date";
    date.name = "earliest";
    date.type = "date";
    date.required = true;
    date.autocomplete = "off";
    form.appendChild(dateLabel);
    form.appendChild(date);
    var periodLabel = node("label", "Preferred time (UK time)");
    periodLabel.htmlFor = "callback-period";
    var period = node("select");
    period.id = "callback-period";
    period.name = "period";
    [["any", "Any time"], ["morning", "Morning, before 12 noon"], ["afternoon", "Afternoon, from 12 noon"]].forEach(function (item) {
      var option = node("option", item[1]);
      option.value = item[0];
      period.appendChild(option);
    });
    form.appendChild(periodLabel);
    form.appendChild(period);
    var find = node("button", "Find callback times");
    find.type = "submit";
    form.appendChild(find);
    var list = node("button", "Check my callbacks");
    list.type = "button";
    list.className = "secondary";
    form.appendChild(list);
    parent.appendChild(form);
    var status = node("p");
    status.id = "callback-status";
    status.setAttribute("role", "status");
    parent.appendChild(status);
    var proposals = node("div");
    proposals.id = "callback-proposals";
    parent.appendChild(proposals);
    var bookings = node("div");
    bookings.id = "callback-bookings";
    parent.appendChild(bookings);

    function valid() { return active && parent.isConnected && !document.getElementById("content").hidden; }
    function request(body, done) {
      if (busy) return;
      if (!consent.checked) {
        consent.setAttribute("aria-invalid", "true");
        status.textContent = "Agree to use your own record for callbacks first.";
        consent.focus();
        return;
      }
      var current = generation;
      busy = true;
      parent.setAttribute("aria-busy", "true");
      status.textContent = "Checking the local agenda\u2026";
      body.use_record = true;
      api("/demo/agenda", { method: "POST", body: JSON.stringify(body) }).then(function (response) {
        if (!valid() || current !== generation) return;
        if (response.status === 401) { expired("Please sign in again."); return; }
        if (!response.ok) {
          status.textContent = response.body.error || "The callback result is unknown. Check your callbacks or ask your housing officer.";
          return;
        }
        status.textContent = response.body.notice;
        renderBookings(response.body.bookings);
        done(response.body);
      }).catch(function () {
        if (valid() && current === generation) status.textContent = "We could not confirm the callback result. Check your connection, then check your callbacks before trying again.";
      }).then(function () {
        busy = false;
        parent.removeAttribute("aria-busy");
      });
    }

    function renderBookings(items) {
      bookings.textContent = "";
      bookings.appendChild(node("h3", "Your synthetic callbacks"));
      if (!items.length) bookings.appendChild(node("p", "You have no reserved synthetic callbacks."));
      items.forEach(function (item, index) {
        var group = node("div");
        group.className = "callback-item";
        group.appendChild(node("p", "Reserved synthetic callback: " + when(item)));
        group.appendChild(node("p", notice + " Reference: " + item.reference));
        var confirm = checkbox(group, "cancel-callback-" + index, "I want to cancel this synthetic callback.");
        var cancel = node("button", "Cancel this callback");
        cancel.type = "button";
        cancel.addEventListener("click", function () {
          if (!confirm.checked) { status.textContent = "Confirm which callback you want to cancel."; confirm.focus(); return; }
          request({ action: "cancel", reference: item.reference, confirmed: true }, function () {
            status.textContent = "Synthetic callback cancelled. No live service was contacted.";
            list.focus();
          });
        });
        group.appendChild(cancel);
        bookings.appendChild(group);
      });
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      request({ action: "find", earliest: date.value, period: period.value }, function (body) {
        proposals.textContent = "";
        proposals.appendChild(node("h3", "Proposed synthetic callbacks"));
        proposals.appendChild(node("p", notice + " Times stay free until you confirm. Proposals expire after 10 minutes."));
        if (!body.proposals.length) proposals.appendChild(node("p", "No matching free times. Try another date or time, or ask your housing officer."));
        body.proposals.forEach(function (slot, index) {
          var group = node("div");
          group.className = "callback-item";
          group.appendChild(node("p", when(slot)));
          var confirm = checkbox(group, "book-callback-" + index, "I confirm this specific synthetic callback time.");
          var book = node("button", "Book this callback");
          book.type = "button";
          book.addEventListener("click", function () {
            if (!confirm.checked) { status.textContent = "Confirm the specific callback time before booking."; confirm.focus(); return; }
            request({ action: "book", proposal: slot.proposal, confirmed: true }, function () {
              proposals.textContent = "";
              status.textContent = "Synthetic callback reserved. " + notice;
              list.focus();
            });
          });
          group.appendChild(book);
          proposals.appendChild(group);
        });
      });
    });
    list.addEventListener("click", function () { request({ action: "list" }, function () {}); });
    consent.addEventListener("change", function () {
      consent.removeAttribute("aria-invalid");
      generation += 1;
      proposals.textContent = "";
      bookings.textContent = "";
      status.textContent = consent.checked ? "" : "Record use stopped. Any callback already reserved stays reserved; check or ask a person to cancel it.";
    });
    return {
      dispose: function () { active = false; generation += 1; },
      searchFromChat: function (search) {
        consent.checked = true;
        date.value = search.earliest;
        period.value = search.period;
        title.focus();
        form.requestSubmit();
      }
    };
  };

  window.mountResidentAssistant = function (content, api, sessionExpired, searchCallbacks) {
    var generation = 0;
    var signedIn = false;
    var busy = false;
    var launcher = node("button", "Chat");
    launcher.id = "chat-launcher";
    launcher.className = "chat-launcher";
    launcher.type = "button";
    launcher.setAttribute("aria-controls", "resident-chat");
    launcher.setAttribute("aria-expanded", "false");
    launcher.insertAdjacentHTML("afterbegin", '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><path d="M4 3h16v13H9l-5 5V3zm4 5h8M8 12h6" fill="none" stroke="currentColor" stroke-width="2"/></svg>');
    var panel = node("section");
    panel.id = "resident-chat";
    panel.className = "assistant chat-window";
    panel.hidden = true;
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-labelledby", "assistant-title");
    var title = node("h2", "Help with your case");
    title.id = "assistant-title";
    title.tabIndex = -1;
    panel.appendChild(title);
    var close = node("button", "Close chat");
    close.type = "button";
    close.className = "secondary";
    panel.appendChild(close);
    var notice = node("p", "Advisory only. Chat cannot submit forms, give consent or make decisions. Callback booking needs your separate confirmation.");
    notice.id = "assistant-notice";
    panel.appendChild(notice);
    panel.appendChild(node("p", "AI may help explain your case. Each answer says whether AI or rules were used. AI cannot decide eligibility or give legal, safety or financial advice. This chat does not send messages to staff."));
    var anonymous = node("p", "Sign in to ask about your own record. You can ask a person for help without using chat.");
    panel.appendChild(anonymous);
    var form = node("form");
    var consent = checkbox(form, "assistant-consent", "Use my own record to answer this question or find synthetic callback times. AI may use the bounded case answer if enabled. No works consent is given.");
    consent.setAttribute("aria-describedby", "assistant-status");
    var label = node("label", "Your question");
    label.htmlFor = "assistant-topic";
    form.appendChild(label);
    var select = node("select");
    select.id = "assistant-topic";
    select.name = "topic";
    select.autocomplete = "off";
    select.setAttribute("aria-describedby", "assistant-notice");
    [
      ["status", "Where is my case now?"], ["documents", "Which documents should I send?"],
      ["forms", "How can I fill in a form?"], ["home", "What is recorded about my home?"],
      ["consents", "What about my works consent?"], ["appointments", "Help with appointments"],
      ["regulations", "Which repair rules are held?"], ["safety", "I need safety help"]
    ].forEach(function (item) {
      var option = node("option", item[1]);
      option.value = item[0];
      select.appendChild(option);
    });
    form.appendChild(select);
    var questionLabel = node("label", "Or type a question (optional)");
    questionLabel.htmlFor = "assistant-question";
    form.appendChild(questionLabel);
    var question = node("input");
    question.id = "assistant-question";
    question.name = "question";
    question.type = "text";
    question.maxLength = 500;
    question.autocomplete = "off";
    form.appendChild(question);
    form.appendChild(node("p", "Supported topics only. Do not enter sensitive details. Typed messages are not sent to AI or kept as conversation memory."));
    var button = node("button", "Get advice");
    button.type = "submit";
    form.appendChild(button);
    panel.appendChild(form);
    var status = node("p");
    status.className = "status";
    status.id = "assistant-status";
    status.setAttribute("role", "status");
    panel.appendChild(status);
    var result = node("div");
    result.id = "assistant-result";
    result.setAttribute("role", "log");
    result.setAttribute("aria-label", "Chat answers");
    result.setAttribute("aria-live", "polite");
    result.setAttribute("aria-relevant", "additions");
    panel.appendChild(result);
    var callbacks = node("button", "Use the manual callback form");
    callbacks.type = "button";
    callbacks.className = "secondary";
    panel.appendChild(callbacks);
    panel.appendChild(node("p", "A person can help instead. Phone your housing officer using your usual number, or write to or visit your local office."));
    panel.appendChild(node("p", "For immediate danger, call 999. Report safety concerns directly to a person or emergency repairs service. Chat has not alerted anyone."));
    content.appendChild(launcher);
    content.appendChild(panel);

    function hide(returnFocus) {
      panel.hidden = true;
      launcher.setAttribute("aria-expanded", "false");
      if (returnFocus) launcher.focus();
    }
    launcher.addEventListener("click", function () {
      if (!panel.hidden) { hide(true); return; }
      panel.hidden = false;
      launcher.setAttribute("aria-expanded", "true");
      title.focus();
    });
    close.addEventListener("click", function () { hide(true); });
    panel.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { event.preventDefault(); hide(true); }
    });
    document.addEventListener("focusin", function (event) {
      if (!panel.hidden && !panel.contains(event.target) && event.target !== launcher) hide(false);
    });
    callbacks.addEventListener("click", function () {
      hide(false);
      var target = ["callback-title", "email", "retry"].map(function (id) {
        return document.getElementById(id);
      }).find(function (item) { return item && item.getClientRects().length; });
      (target || launcher).focus();
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (busy) return;
      if (!consent.checked) {
        consent.setAttribute("aria-invalid", "true");
        status.textContent = "Agree to use your own record for this question first.";
        consent.focus();
        return;
      }
      var current = generation;
      busy = true;
      button.setAttribute("aria-disabled", "true");
      select.disabled = true;
      status.textContent = "Getting your advice\u2026";
      var draft = question.value;
      var text = draft.trim();
      var body = text ? { question: text, use_record: true } : { topic: select.value, use_record: true };
      api("/demo/assistant", { method: "POST", body: JSON.stringify(body) })
        .then(function (response) {
          if (current !== generation || !signedIn) return;
          if (response.status === 401) { sessionExpired("Please sign in again."); return; }
          status.textContent = "";
          if (!response.ok) {
            status.textContent = response.body.error || "The assistant is not available. Try again or ask your housing officer.";
            return;
          }
          var entry = node("div");
          entry.appendChild(node("p", "You: " + (text || select.options[select.selectedIndex].textContent)));
          entry.appendChild(node("p", response.body.label));
          entry.appendChild(node("p", response.body.answer));
          entry.appendChild(node("h3", "Sources"));
          var sources = node("ul");
          response.body.sources.forEach(function (source) { sources.appendChild(node("li", source)); });
          entry.appendChild(sources);
          result.appendChild(entry);
          while (result.childElementCount > 10) result.firstElementChild.remove();
          if (question.value === draft) question.value = "";
          if (response.body.action === "appointments" && !panel.hidden) {
            hide(false);
            searchCallbacks(response.body.callback_search);
          }
        })
        .catch(function () {
          if (current === generation && signedIn) status.textContent = "We could not reach the assistant. Check your connection, then try again or ask your housing officer.";
        })
        .then(function () {
          if (current !== generation) return;
          busy = false;
          button.removeAttribute("aria-disabled");
          select.disabled = false;
        });
    });
    consent.addEventListener("change", function () {
      consent.removeAttribute("aria-invalid");
      generation += 1;
      busy = false;
      button.removeAttribute("aria-disabled");
      select.disabled = false;
      result.textContent = "";
      question.value = "";
      status.textContent = consent.checked ? "" : "Record use stopped. Previous answers cleared.";
    });
    return {
      setSession: function (value) {
        generation += 1;
        signedIn = value;
        busy = false;
        form.hidden = !signedIn;
        anonymous.hidden = signedIn;
        consent.checked = false;
        consent.removeAttribute("aria-invalid");
        question.value = "";
        result.textContent = "";
        status.textContent = "";
        select.disabled = false;
        button.removeAttribute("aria-disabled");
        hide(false);
      }
    };
  };
})();
