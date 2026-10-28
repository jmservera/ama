"use strict";
(function () {
  var statusEl = document.getElementById("status");
  var errorEl = document.getElementById("error");
  var errorTitle = document.getElementById("error-title");
  var errorText = document.getElementById("error-text");
  var content = document.getElementById("content");
  var signin = document.getElementById("signin");
  var form = document.getElementById("signin-form");
  var signinError = document.getElementById("signin-error");
  var signinButton = document.getElementById("signin-button");
  var account = document.getElementById("account");
  var accountEmail = document.getElementById("account-email");
  var csrf = "";
  var callbackController = null;
  var assistant = window.mountResidentAssistant(document.body, api, showSignin, function (search) {
    if (callbackController) callbackController.searchFromChat(search);
  });
  assistant.setSession(false);
  function removeAppointments() {
    if (callbackController) callbackController.dispose();
    callbackController = null;
  }

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

  var sensorMetrics = [
    { key: "temperature_c", status: "temperature_status", name: "Temperature", unit: "\u00b0C", min: -10, max: 45 },
    { key: "humidity_pct", status: "humidity_status", name: "Humidity", unit: "%", min: 0, max: 100 }
  ];
  var sensorNumber = new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 });
  var sensorDate = new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short", timeZone: "UTC" });

  function sensorValue(reading, metric) {
    return reading[metric.key] === null
      ? reading[metric.status]
      : sensorNumber.format(reading[metric.key]) + " " + metric.unit;
  }

  function sensorTime(stamp) {
    var time = el("time", sensorDate.format(new Date(stamp)) + " UTC");
    time.dateTime = stamp;
    return time;
  }

  function svgEl(tag, attrs, text) {
    var node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs || {}).forEach(function (name) { node.setAttribute(name, attrs[name]); });
    if (text) node.textContent = text;
    return node;
  }

  function sensorChart(history, metric) {
    var figure = el("figure", null, "sensor-chart");
    var id = "sensor-" + metric.key;
    figure.appendChild(el("h3", metric.name + " history (" + metric.unit + ")"));
    var svg = svgEl("svg", { viewBox: "0 0 480 180", role: "img", "aria-labelledby": id + "-title " + id + "-desc" });
    svg.appendChild(svgEl("title", { id: id + "-title" }, "Synthetic " + metric.name.toLowerCase() + " history"));
    svg.appendChild(svgEl("desc", { id: id + "-desc" }, "Recorded values over time. Gaps mean readings are missing or unavailable. The table below gives every value and status."));
    svg.appendChild(svgEl("path", { d: "M45 10V150H470", class: "sensor-axis" }));
    [metric.min, (metric.min + metric.max) / 2, metric.max].forEach(function (value) {
      var y = 150 - (value - metric.min) / (metric.max - metric.min) * 140;
      svg.appendChild(svgEl("text", { x: 38, y: y + 4, "text-anchor": "end" }, sensorNumber.format(value)));
    });
    var start = Date.parse(history[0].observed_at);
    var end = Date.parse(history[history.length - 1].observed_at);
    var points = [];
    var previous = null;
    function segment() {
      if (points.length > 1) svg.appendChild(svgEl("polyline", { points: points.join(" "), class: "sensor-line" }));
      points = [];
    }
    history.forEach(function (reading) {
      var stamp = Date.parse(reading.observed_at);
      if (reading[metric.key] === null) { segment(); previous = null; return; }
      if (previous !== null && stamp - previous > 90 * 60 * 1000) segment();
      var x = end === start ? 255 : 45 + (stamp - start) / (end - start) * 425;
      var y = 150 - (reading[metric.key] - metric.min) / (metric.max - metric.min) * 140;
      points.push(x + "," + y);
      svg.appendChild(svgEl("circle", { cx: x, cy: y, r: 3, class: "sensor-point" }));
      previous = stamp;
    });
    segment();
    figure.appendChild(svg);
    var caption = el("figcaption");
    caption.appendChild(el("span", "Time (UTC): "));
    caption.appendChild(sensorTime(history[0].observed_at));
    if (history.length > 1) {
      caption.appendChild(el("span", " to "));
      caption.appendChild(sensorTime(history[history.length - 1].observed_at));
    }
    figure.appendChild(caption);
    return figure;
  }

  function renderSensors(sensors) {
    var section = card("Your home sensors");
    section.appendChild(el("p", sensors.note));
    var history = sensors.history;
    if (!history.length) {
      section.appendChild(el("p", "No synthetic sensor readings are available for your home. You can still use the help options below."));
      return section;
    }
    var latest = history[history.length - 1];
    var recorded = el("p", "Latest stored reading: ");
    recorded.appendChild(sensorTime(latest.observed_at));
    section.appendChild(recorded);
    var gauges = el("div", null, "sensor-gauges");
    sensorMetrics.forEach(function (metric) {
      var group = el("div", null, "sensor-gauge");
      var label = el("label", metric.name + " (" + metric.unit + ")");
      var id = "gauge-" + metric.key;
      if (latest[metric.key] !== null) {
        label.htmlFor = id;
        var meter = el("meter");
        meter.id = id;
        meter.min = metric.min;
        meter.max = metric.max;
        meter.value = latest[metric.key];
        meter.textContent = sensorValue(latest, metric);
        meter.setAttribute("aria-valuetext", sensorValue(latest, metric) + ", synthetic recorded value");
        group.appendChild(label);
        group.appendChild(meter);
      } else {
        group.appendChild(el("h3", metric.name + " (" + metric.unit + ")"));
      }
      group.appendChild(el("p", sensorValue(latest, metric), "sensor-value"));
      gauges.appendChild(group);
    });
    section.appendChild(gauges);
    section.appendChild(el("p", "Demo display ranges are not safe or unsafe limits. Missing values and demo faults appear as gaps, not zero."));
    sensorMetrics.forEach(function (metric) { section.appendChild(sensorChart(history, metric)); });
    var details = el("details");
    details.appendChild(el("summary", "Show sensor history as a table"));
    var scroll = el("div", null, "sensor-table");
    scroll.tabIndex = 0;
    scroll.setAttribute("role", "region");
    scroll.setAttribute("aria-label", "Synthetic sensor history table");
    var table = el("table");
    table.appendChild(el("caption", "Synthetic stored readings for your home, oldest first"));
    var head = el("thead");
    var headings = el("tr");
    ["Recorded time (UTC)", "Temperature (\u00b0C)", "Humidity (%)"].forEach(function (text) {
      var th = el("th", text);
      th.scope = "col";
      headings.appendChild(th);
    });
    head.appendChild(headings);
    table.appendChild(head);
    var body = el("tbody");
    history.forEach(function (reading) {
      var tr = el("tr");
      var timeCell = el("th");
      timeCell.scope = "row";
      timeCell.appendChild(sensorTime(reading.observed_at));
      tr.appendChild(timeCell);
      sensorMetrics.forEach(function (metric) { tr.appendChild(el("td", sensorValue(reading, metric))); });
      body.appendChild(tr);
    });
    table.appendChild(body);
    scroll.appendChild(table);
    details.appendChild(scroll);
    section.appendChild(details);
    return section;
  }

  function render(view, announce) {
    removeAppointments();
    assistant.setSession(true);
    content.textContent = "";
    if (view.banner) {
      var note = card("About this showcase");
      note.appendChild(el("p", view.banner));
      content.appendChild(note);
    }
    if (view.home) {
      var home = card("Your home");
      home.appendChild(el("p", [view.home.address, view.home.town, view.home.postcode].filter(Boolean).join(", ")));
      content.appendChild(home);
    }
    if (view.sensors) content.appendChild(renderSensors(view.sensors));
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
    var help = card("Help and other ways to reach us");
    help.appendChild(el("p", view.help.summary));
    var hl = el("ul");
    view.help.routes.forEach(function (r) { hl.appendChild(el("li", r)); });
    help.appendChild(hl);
    help.appendChild(el("p", view.help.note));
    content.appendChild(help);
    var callbacks = el("section", null, "card callbacks");
    callbacks.setAttribute("aria-labelledby", "callback-title");
    content.appendChild(callbacks);
    callbackController = window.mountResidentAppointments(callbacks, api, showSignin);

    var unavailable = card("Not available in this showcase");
    var ul = el("ul", null, "unavail");
    view.unavailable.filter(function (u) { return u.feature !== "Automated answers"; }).forEach(function (u) {
      var li = el("li");
      var appointment = u.feature === "Replying to an appointment";
      var b = el("button", appointment ? "Operational appointments" : u.feature);
      b.type = "button";
      b.disabled = true;
      b.setAttribute("aria-disabled", "true");
      li.appendChild(b);
      li.appendChild(el("span", appointment ? "You cannot change live works appointments here. Use the form above for local synthetic callbacks only." : u.reason, "why"));
      ul.appendChild(li);
    });
    unavailable.appendChild(ul);
    content.appendChild(unavailable);

    errorEl.hidden = true;
    signin.hidden = true;
    content.hidden = false;
    accountEmail.textContent = view.account.email;
    account.hidden = false;
    statusEl.textContent = announce || "";
    if (announce) {
      var first = content.querySelector("h2");
      if (first) {
        first.setAttribute("tabindex", "-1");
        first.focus();
      }
    }
  }

  function hideAccount() {
    account.hidden = true;
    account.open = false;
    accountEmail.textContent = "";
  }

  function showSignin(message) {
    removeAppointments();
    assistant.setSession(false);
    content.textContent = "";
    content.hidden = true;
    hideAccount();
    errorEl.hidden = true;
    statusEl.textContent = "";
    signin.hidden = false;
    if (message) {
      signinError.textContent = message;
      signinError.hidden = false;
      signinError.focus();
    } else {
      signinError.hidden = true;
    }
  }

  function fail(message) {
    removeAppointments();
    assistant.setSession(false);
    content.textContent = "";
    content.hidden = true;
    signin.hidden = true;
    hideAccount();
    statusEl.textContent = "";
    errorText.textContent = message;
    errorEl.hidden = false;
    errorTitle.focus();
  }

  function api(path, options) {
    options = options || {};
    var headers = { Accept: "application/json" };
    if (options.body) headers["Content-Type"] = "application/json";
    if (options.method === "POST") headers["X-CSRF-Token"] = csrf;
    return fetch(path, { method: options.method || "GET", headers: headers, body: options.body, cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        return r.json().then(function (body) { return { ok: r.ok, status: r.status, body: body }; });
      });
  }

  function loadView(announce) {
    statusEl.textContent = "Loading your progress\u2026";
    return api("/demo/view").then(function (res) {
      if (res.ok) render(res.body, announce);
      else if (res.status === 401) showSignin("Please sign in again.");
      else fail(res.body.error || "Something went wrong.");
    });
  }

  var signedOut = false;

  function start() {
    errorEl.hidden = true;
    statusEl.textContent = "Loading\u2026";
    api("/demo/session")
      .then(function (res) {
        if (!res.ok) { fail(res.body.error || "The showcase is not available right now."); return; }
        csrf = res.body.csrf;
        if (res.body.signed_in) return loadView();
        showSignin();
        if (signedOut) {
          signedOut = false;
          statusEl.textContent = "You have signed out.";
          document.getElementById("signin-title").setAttribute("tabindex", "-1");
          document.getElementById("signin-title").focus();
        }
      })
      .catch(function () {
        fail("We could not reach the showcase. Check your connection, then try again.");
      });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    if (!email.trim() || !password) {
      signinError.textContent = "Enter your email address and the password.";
      signinError.hidden = false;
      signinError.focus();
      return;
    }
    signinButton.disabled = true;
    signinError.hidden = true;
    api("/demo/login", { method: "POST", body: JSON.stringify({ email: email, password: password }) })
      .then(function (res) {
        document.getElementById("password").value = "";
        if (res.ok) {
          csrf = res.body.csrf || csrf;
          return loadView("You are signed in. Your progress is shown below.");
        }
        if (res.status === 403) { start(); return; }
        showSignin(res.body.error || "We could not sign you in.");
      })
      .catch(function () {
        showSignin("We could not reach the showcase. Try again.");
      })
      .then(function () { signinButton.disabled = false; });
  });

  document.getElementById("signout").addEventListener("click", function () {
    removeAppointments();
    assistant.setSession(false);
    function notConfirmed() {
      fail("We could not confirm that you were signed out. Your session may still be active on this device and ends by itself within 30 minutes. Select Try again to check, then sign out again.");
    }
    fetch("/demo/logout", { method: "POST", headers: { "X-CSRF-Token": csrf, "Content-Type": "application/json" }, body: "{}", cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) { notConfirmed(); return; }
        content.textContent = "";
        hideAccount();
        csrf = "";
        signedOut = true;
        start();
      }).catch(notConfirmed);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && account.open) {
      account.open = false;
      account.querySelector("summary").focus();
    }
  });
  document.addEventListener("click", function (event) {
    if (!account.contains(event.target)) account.open = false;
  });

  document.getElementById("retry").addEventListener("click", start);
  start();
})();
