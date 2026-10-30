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
    if (typeof window.ChatWidget?.create !== "function") {
      var unavailable = node("p", "Chat could not load. Reload this page to try again, or contact your housing officer using your usual contact details. The manual callback form is still available.");
      unavailable.setAttribute("role", "alert");
      content.appendChild(unavailable);
      return { setSession: function () {} };
    }
    var ui = window.ChatWidget.create({
      id: "resident-chat", title: "Help with your case",
      questionLabel: "Your question", skillLabel: "Assistant", maxLength: 500
    });
    var launcher = ui.launcher, panel = ui.root, title = ui.heading;
    launcher.id = "chat-launcher";
    title.id = "assistant-title";
    panel.setAttribute("aria-labelledby", title.id);
    var notice = node("p", "Advisory only. Chat cannot submit forms, give consent or make decisions. Callback booking needs your separate confirmation.");
    notice.id = "assistant-notice";
    ui.intro.appendChild(notice);
    ui.intro.appendChild(node("p", "AI may help explain your case. Each answer says whether AI or rules were used. AI cannot decide eligibility or give legal, safety or financial advice. This chat does not send messages to staff."));
    var anonymous = node("p", "Sign in to ask about your own record. You can ask a person for help without using chat.");
    panel.insertBefore(anonymous, ui.log);
    var form = ui.form;
    var consent = checkbox(ui.beforeInput, "assistant-consent", "Use my question and limited own-case details for this chat, including AI when enabled. This is not consent to works.");
    consent.setAttribute("aria-describedby", "resident-chat-error assistant-status");
    var select = ui.select;
    var option = node("option", "Resident assistant");
    option.value = "resident";
    select.appendChild(option);
    var question = ui.input;
    question.id = "assistant-question";
    question.setAttribute("aria-describedby", "assistant-notice resident-chat-error");
    ui.intro.appendChild(node("p", "Ask about your case, documents, forms, planned improvements or a repair concern. Do not enter sensitive or contact details. With your permission, your question and limited own-case details may be sent to AI. Chat is not kept as model conversation memory."));
    ui.status.id = "assistant-status";
    var result = ui.log;
    result.id = "assistant-result";
    var callbacks = node("button", "Use the manual callback form");
    callbacks.type = "button";
    callbacks.className = "secondary";
    ui.intro.appendChild(callbacks);
    ui.intro.appendChild(node("p", "A person can help instead. Phone your housing officer using your usual number, or write to or visit your local office."));
    ui.intro.appendChild(node("p", "For immediate danger, call 999. Report safety concerns directly to a person or emergency repairs service. Chat has not alerted anyone."));

    function hide(returnFocus) {
      ui.hide(returnFocus);
    }
    callbacks.addEventListener("click", function () {
      hide(false);
      var target = ["callback-title", "email", "retry"].map(function (id) {
        return document.getElementById(id);
      }).find(function (item) { return item && item.getClientRects().length; });
      (target || launcher).focus();
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (busy || !signedIn) return;
      ui.clearError();
      if (!consent.checked) {
        consent.setAttribute("aria-invalid", "true");
        ui.fail("Agree to use your own record for this question first.");
        consent.focus();
        return;
      }
      var draft = question.value;
      var text = draft.trim();
      if (!text) { ui.fail("Type a question first."); question.focus(); return; }
      var current = generation;
      busy = true;
      ui.busy(true);
      ui.setStatus("Getting your advice\u2026");
      ui.message("user", text);
      var body = { question: text, use_record: true };
      api("/demo/assistant", { method: "POST", body: JSON.stringify(body) })
        .then(function (response) {
          if (current !== generation || !signedIn) return;
          if (response.status === 401) { sessionExpired("Please sign in again."); return; }
          ui.setStatus("");
          if (!response.ok) {
            ui.fail(response.body.error || "The assistant is not available. Try again or ask your housing officer.");
            return;
          }
          var entry = ui.message("assistant", response.body.answer, {
            label: response.body.label, sources: response.body.sources,
            detail: [
              response.body.label.startsWith("AI") ? "Not approved. AI-generated content may be incorrect. Check the sources." : "",
              response.body.notice, response.body.help
            ].filter(Boolean).join(" ")
          });
          if (question.value === draft) question.value = "";
          if (response.body.action === "appointments") {
            var search = node("button", "Find callback times in the manual form");
            search.type = "button";
            search.addEventListener("click", function () {
              if (current !== generation || !signedIn || !consent.checked) return;
              hide(false);
              searchCallbacks(response.body.callback_search);
            });
            entry.appendChild(search);
          }
        })
        .catch(function () {
          if (current === generation && signedIn) ui.fail("We could not reach the assistant. Check your connection, then try again or ask your housing officer.");
        })
        .then(function () {
          if (current !== generation) return;
          busy = false;
          ui.busy(false);
        });
    });
    consent.addEventListener("change", function () {
      consent.removeAttribute("aria-invalid");
      generation += 1;
      busy = false;
      ui.busy(false);
      ui.clearError();
      result.textContent = "";
      question.value = "";
      ui.setStatus(consent.checked ? "" : "Record use stopped. Previous answers cleared.");
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
        ui.setStatus("");
        ui.busy(false);
        ui.clearError();
        hide(false);
      }
    };
  };
})();
