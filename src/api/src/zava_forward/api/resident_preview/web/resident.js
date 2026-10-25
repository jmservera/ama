"use strict";
(function () {
  var statusEl = document.getElementById("status");
  var errorEl = document.getElementById("error");
  var errorTitle = document.getElementById("error-title");
  var errorText = document.getElementById("error-text");
  var content = document.getElementById("content");

  function el(tag, text, cls) {
    var node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    if (cls) node.className = cls;
    return node;
  }

  function card(title, cls) {
    var section = el("section", null, "card" + (cls ? " " + cls : ""));
    var heading = el("h2", title);
    heading.id = "h-" + title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    section.setAttribute("aria-labelledby", heading.id);
    section.appendChild(heading);
    return section;
  }

  function formatDate(iso) {
    var parts = String(iso).split("-");
    var d = new Date(Date.UTC(+parts[0], +parts[1] - 1, +parts[2]));
    if (isNaN(d.getTime())) return String(iso);
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  }

  function appointmentCard(group, cls, tagText, tagCls) {
    var section = card(group.heading, cls);
    section.appendChild(el("span", tagText, "tag " + tagCls));
    section.appendChild(el("p", group.note));
    if (group.items.length) {
      var list = el("ul");
      group.items.forEach(function (item) {
        var text = formatDate(item.date) + (item.period ? ", " + item.period.toLowerCase() : "");
        list.appendChild(el("li", text));
      });
      section.appendChild(list);
    } else {
      section.appendChild(el("p", group.empty));
    }
    return section;
  }

  function render(view) {
    content.textContent = "";
    if (view.authority_note) {
      var note = card("Who this is for");
      note.appendChild(el("p", view.authority_note));
      if (view.tasks_not_shown && view.tasks_not_shown.length) {
        var nl = el("ul");
        view.tasks_not_shown.forEach(function (t) { nl.appendChild(el("li", t)); });
        note.appendChild(nl);
      }
      content.appendChild(note);
    }
    if (view.home) {
      var home = card("Your home");
      home.appendChild(el("p", [view.home.address, view.home.town, view.home.postcode].filter(Boolean).join(", ")));
      content.appendChild(home);
    }
    if (view.measures && view.measures.length) {
      var measures = card("Planned improvements");
      var ml = el("ul");
      view.measures.forEach(function (m) { ml.appendChild(el("li", m)); });
      measures.appendChild(ml);
      content.appendChild(measures);
    }
    if (view.progress) {
      var progress = card("Where things are");
      progress.appendChild(el("p", view.progress));
      if (view.closed) progress.appendChild(el("p", view.closed));
      content.appendChild(progress);
    }
    if (view.next_step) {
      var next = card("What happens next");
      next.appendChild(el("p", view.next_step));
      content.appendChild(next);
    }
    if (view.appointments) {
      content.appendChild(appointmentCard(view.appointments.offers, "offered", "Offer - not confirmed", "offer"));
      content.appendChild(appointmentCard(view.appointments.confirmed, "confirmed", "Confirmed", "ok"));
      if (view.appointments.unknown.count) {
        var unknown = card("Appointments we cannot show");
        unknown.appendChild(el("p", view.appointments.unknown.note));
        content.appendChild(unknown);
      }
    }
    var help = card("Help and other ways to reach us");
    help.appendChild(el("p", view.help.summary));
    var hl = el("ul");
    view.help.routes.forEach(function (r) { hl.appendChild(el("li", r)); });
    help.appendChild(hl);
    help.appendChild(el("p", view.help.note));
    content.appendChild(help);

    var unavailable = card("Not available in this preview");
    var ul = el("ul", null, "unavail");
    view.unavailable.forEach(function (u) {
      var li = el("li");
      var b = el("button", u.feature);
      b.type = "button";
      b.disabled = true;
      b.setAttribute("aria-disabled", "true");
      li.appendChild(b);
      li.appendChild(el("span", u.reason, "why"));
      ul.appendChild(li);
    });
    unavailable.appendChild(ul);
    content.appendChild(unavailable);

    errorEl.hidden = true;
    content.hidden = false;
    statusEl.textContent = "";
  }

  function fail(message) {
    content.hidden = true;
    statusEl.textContent = "";
    errorText.textContent = message;
    errorEl.hidden = false;
    errorTitle.focus();
  }

  function load() {
    errorEl.hidden = true;
    statusEl.textContent = "Loading your progress...";
    fetch("/resident/view", { headers: { Accept: "application/json" }, cache: "no-store" })
      .then(function (r) {
        return r.json().then(function (body) { return { ok: r.ok, status: r.status, body: body }; });
      })
      .then(function (res) {
        if (res.ok) render(res.body);
        else fail(res.body.error || "Something went wrong.");
      })
      .catch(function () {
        fail("We could not reach this preview. Check that it is still running, then try again.");
      });
  }

  document.getElementById("retry").addEventListener("click", load);
  load();
})();
