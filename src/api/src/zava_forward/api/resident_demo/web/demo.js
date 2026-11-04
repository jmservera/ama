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
  var lede = document.getElementById("lede");
  var emailField = document.getElementById("email");
  var passwordField = document.getElementById("password");
  var mainEl = document.getElementById("main");
  var csrf = "";
  var loading = false;
  var loadingTimer = null;
  var pendingNotice = "";
  var sessionId = "";
  var transition = 0;
  var sessionChannel = new BroadcastChannel("resident-demo-session");
  var callbackController = null;
  var assistant = window.mountResidentAssistant(document.body, api, showSignin, function (search) {
    if (callbackController) callbackController.searchFromChat(search);
  });
  assistant.setSession(false);
  function removeAppointments() {
    if (callbackController) callbackController.dispose();
    callbackController = null;
  }

  var signedInLede = lede.textContent;
  var callbackLede = " You can try synthetic callback booking below. Nobody will call you.";
  var signedOutLede = "Sign in to see how your home improvement is going. Your home and works records are read-only.";

  function clearInvalid() {
    [emailField, passwordField].forEach(function (field) {
      field.removeAttribute("aria-invalid");
      field.removeAttribute("aria-describedby");
    });
  }
  emailField.addEventListener("input", clearInvalid);
  passwordField.addEventListener("input", clearInvalid);

  var SLOW_COPY = "Still signing you in. The showcase may be waking up, which can take up to 30 seconds. Please wait.";

  function beginLoading(text) {
    endLoading();
    loading = true;
    signin.hidden = true;
    errorEl.hidden = true;
    mainEl.setAttribute("aria-busy", "true");
    statusEl.className = "status loading-card";
    statusEl.textContent = text;
    loadingTimer = setTimeout(function () {
      if (loading) statusEl.textContent = SLOW_COPY;
    }, 4000);
  }

  function endLoading() {
    loading = false;
    if (loadingTimer !== null) clearTimeout(loadingTimer);
    loadingTimer = null;
    mainEl.removeAttribute("aria-busy");
    statusEl.className = "status";
  }

  function clearPersonal() {
    transition += 1;
    sessionId = "";
    removeAppointments();
    assistant.setSession(false);
    content.textContent = "";
    content.hidden = true;
    hideAccount();
  }

  sessionChannel.addEventListener("message", function () {
    if (!sessionId) return;
    var current = transition;
    var held = sessionId;
    api("/demo/session").then(function (res) {
      if (current !== transition) return;
      if (!res.ok || res.body.session_id !== held) {
        showSignin("Your sign-in changed in another tab. Please sign in again.");
      }
    }).catch(function () {
      if (current === transition) fail("We could not check your sign-in. Select Try again.");
    });
  });

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

  var ICONS = {
    list: [["path", { d: "M7 5h9M7 10h9M7 15h9" }], ["circle", { cx: 3.5, cy: 5, r: 1 }], ["circle", { cx: 3.5, cy: 10, r: 1 }], ["circle", { cx: 3.5, cy: 15, r: 1 }]],
    sparkle: [["path", { d: "M9 2l1.7 4.8L15.5 8.5l-4.8 1.7L9 15l-1.7-4.8L2.5 8.5l4.8-1.7z" }], ["path", { d: "M16 12.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z" }]],
    check: [["circle", { cx: 10, cy: 10, r: 7.5 }], ["path", { d: "M6.5 10.5l2.2 2.2 4.8-5" }]],
    clock: [["circle", { cx: 10, cy: 10, r: 7.5 }], ["path", { d: "M10 6v4.5l3 1.5" }]],
    alert: [["path", { d: "M10 3L2 17h16L10 3z" }], ["path", { d: "M10 8v4M10 14.5v.5" }]],
    ban: [["circle", { cx: 10, cy: 10, r: 7.5 }], ["path", { d: "M4.7 4.7l10.6 10.6" }]],
    home: [["path", { d: "M3 9.5L10 3l7 6.5V17H3V9.5z" }]],
    document: [["path", { d: "M5 2.5h7l3 3v12H5z" }], ["path", { d: "M12 2.5v3h3" }]],
    info: [["circle", { cx: 10, cy: 10, r: 7.5 }], ["path", { d: "M10 9v5M10 6v.5" }]],
    phone: [["path", { d: "M5 3h3l1.5 4-2 1.2a9 9 0 004.3 4.3L13 10.5l4 1.5v3a2 2 0 01-2 2A12 12 0 013 5a2 2 0 012-2z" }]],
    summary: [["path", { d: "M4 4h12v12H4z" }], ["path", { d: "M7 8h6M7 12h4" }]],
    funding: [["circle", { cx: 10, cy: 10, r: 7.5 }], ["path", { d: "M12 7.5c-.5-.7-1.3-1-2-1-1.2 0-2 .6-2 1.5s.8 1.3 2 1.6 2 .7 2 1.6-.8 1.5-2 1.5c-.8 0-1.6-.3-2-1M10 5v10" }]],
    timeline: [["path", { d: "M3 10h14" }], ["circle", { cx: 5, cy: 10, r: 2 }], ["circle", { cx: 10, cy: 10, r: 2 }], ["circle", { cx: 15, cy: 10, r: 2 }]],
    sensors: [["path", { d: "M10 3v8.5a3 3 0 11-2 0V3a1 1 0 012 0z" }]]
  };

  function icon(name) {
    var svg = svgEl("svg", { viewBox: "0 0 20 20", width: 20, height: 20, "class": "icon", "aria-hidden": "true", focusable: "false" });
    (ICONS[name] || []).forEach(function (part) { svg.appendChild(svgEl(part[0], part[1])); });
    return svg;
  }

  function withIcon(parent, name, text) {
    parent.appendChild(icon(name));
    parent.appendChild(document.createTextNode(" " + text));
    return parent;
  }

  function badge(name, text, tone) {
    return withIcon(el("span", null, "status-badge" + (tone ? " " + tone : "")), name, text);
  }

  function sectionCard(id, title, cls, iconName) {
    var node = card(title, cls);
    node.id = id;
    if (iconName) node.querySelector("h2").insertBefore(icon(iconName), node.querySelector("h2").firstChild);
    return node;
  }

  var sensorMetrics = [
    { key: "temperature_c", status: "temperature_status", name: "Temperature", unit: "\u00b0C", min: -10, max: 45 },
    { key: "humidity_pct", status: "humidity_status", name: "Humidity", unit: "%", min: 0, max: 100 }
  ];
  var sensorNumber = new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 });
  var sensorDate = new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "short", timeZone: "Europe/London" });

  function sensorValue(reading, metric) {
    return reading[metric.key] === null
      ? reading[metric.status]
      : sensorNumber.format(reading[metric.key]) + " " + metric.unit;
  }

  function sensorTime(stamp, suffix) {
    var time = el("time", sensorDate.format(new Date(stamp)) + (suffix || ""));
    time.dateTime = stamp;
    return time;
  }

  function svgEl(tag, attrs, text) {
    var node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs || {}).forEach(function (name) { node.setAttribute(name, attrs[name]); });
    if (text) node.textContent = text;
    return node;
  }

  function sensorSummary(history, metric) {
    var values = history.filter(function (r) { return r[metric.key] !== null; });
    var gaps = history.length - values.length;
    var missing = gaps ? " " + gaps + (gaps === 1 ? " reading is" : " readings are") + " missing or unavailable." : "";
    if (!values.length) return "No usable " + metric.name.toLowerCase() + " readings in this history." + missing;
    var nums = values.map(function (r) { return r[metric.key]; });
    var low = Math.min.apply(null, nums);
    var high = Math.max.apply(null, nums);
    var first = nums[0];
    var last = nums[nums.length - 1];
    var move = Math.abs(last - first) < (metric.max - metric.min) * 0.02 ? "about the same as" : last > first ? "higher than" : "lower than";
    var fmt = function (n) { return sensorNumber.format(n) + "\u00a0" + metric.unit; };
    return "Across " + values.length + " " + (values.length === 1 ? "reading" : "readings") + ": lowest " + fmt(low) + ", highest " + fmt(high) +
      (values.length > 1 ? ". The latest value is " + move + " the first." : ".") + missing;
  }

  function forecastValues(forecast, metric) {
    return ((forecast && forecast.points) || []).filter(function (p) { return p[metric.key] !== null && p[metric.key] !== undefined; });
  }

  function forecastSummary(future, metric) {
    if (!future.length) return "";
    var nums = future.map(function (p) { return p[metric.key]; });
    var fmt = function (n) { return sensorNumber.format(n) + "\u00a0" + metric.unit; };
    return " Simple 24-hour forecast (estimate): " + fmt(Math.min.apply(null, nums)) + " to " + fmt(Math.max.apply(null, nums)) + ".";
  }

  function sensorChart(history, metric, forecast) {
    var future = forecastValues(forecast, metric);
    var figure = el("figure", null, "sensor-chart");
    var id = "sensor-" + metric.key;
    var summary = sensorSummary(history, metric) + forecastSummary(future, metric);
    figure.appendChild(el("h3", metric.name + " history" + (future.length ? " and 24-hour forecast" : "") + " (" + metric.unit + ")"));
    var svg = svgEl("svg", { viewBox: "0 0 480 180", role: "img", "aria-labelledby": id + "-title " + id + "-desc" });
    svg.appendChild(svgEl("title", { id: id + "-title" }, "Synthetic " + metric.name.toLowerCase() + " history" + (future.length ? " with a 24-hour estimate" : "")));
    svg.appendChild(svgEl("desc", { id: id + "-desc" }, summary + " Gaps mean readings are missing or unavailable. The table below gives every value and status."));
    svg.appendChild(svgEl("path", { d: "M56 10V150H470", class: "sensor-axis" }));
    [metric.min, (metric.min + metric.max) / 2, metric.max].forEach(function (value) {
      var y = 150 - (value - metric.min) / (metric.max - metric.min) * 140;
      svg.appendChild(svgEl("text", { x: 50, y: y + 6, "text-anchor": "end" }, sensorNumber.format(value)));
    });
    var start = Date.parse(history[0].observed_at);
    var latestAt = Date.parse(history[history.length - 1].observed_at);
    var end = future.length ? Date.parse(future[future.length - 1].forecast_at) : latestAt;
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
      var x = end === start ? 263 : 56 + (stamp - start) / (end - start) * 414;
      var y = 150 - (reading[metric.key] - metric.min) / (metric.max - metric.min) * 140;
      points.push(x + "," + y);
      svg.appendChild(svgEl("circle", { cx: x, cy: y, r: 3, class: "sensor-point" }));
      previous = stamp;
    });
    segment();
    if (future.length) {
      var lastValue = null;
      for (var i = history.length - 1; i >= 0 && lastValue === null; i--) if (history[i][metric.key] !== null) lastValue = history[i];
      var anchorX = 56 + (latestAt - start) / (end - start) * 414;
      svg.appendChild(svgEl("line", { x1: anchorX, y1: 10, x2: anchorX, y2: 150, class: "sensor-divider" }));
      svg.appendChild(svgEl("text", { x: anchorX - 4, y: 26, "text-anchor": "end" }, "Latest stored"));
      var line = [];
      if (lastValue && history[history.length - 1][metric.key] !== null) {
        line.push(anchorX + "," + (150 - (lastValue[metric.key] - metric.min) / (metric.max - metric.min) * 140));
      }
      future.forEach(function (point) {
        var fx = 56 + (Date.parse(point.forecast_at) - start) / (end - start) * 414;
        var fy = 150 - (point[metric.key] - metric.min) / (metric.max - metric.min) * 140;
        line.push(fx + "," + fy);
        svg.appendChild(svgEl("rect", { x: fx - 3.5, y: fy - 3.5, width: 7, height: 7, class: "sensor-forecast-point" }));
      });
      svg.appendChild(svgEl("polyline", { points: line.join(" "), class: "sensor-forecast-line" }));
    }
    figure.appendChild(svg);
    var caption = el("figcaption");
    caption.appendChild(el("p", summary, "sensor-summary"));
    caption.appendChild(el("span", "Time (UK time): "));
    caption.appendChild(sensorTime(history[0].observed_at));
    if (history.length > 1) {
      caption.appendChild(el("span", " to "));
      caption.appendChild(sensorTime(history[history.length - 1].observed_at));
    }
    if (future.length) {
      caption.appendChild(el("p", "Solid line with circles: stored readings. Dashed line with hollow squares: forecast (estimate).", "sensor-key"));
    }
    figure.appendChild(caption);
    return figure;
  }

  function renderSensors(sensors) {
    var section = sectionCard("sec-sensors", "Your home sensors and forecast", "", "sensors");
    section.appendChild(el("p", sensors.note));
    var history = sensors.history;
    if (!history.length) {
      section.appendChild(el("p", "No synthetic sensor readings are available for your home. You can still use the help options below."));
      return section;
    }
    var latest = history[history.length - 1];
    var recorded = el("p", "Latest stored reading: ");
    recorded.appendChild(sensorTime(latest.observed_at, " (UK time)"));
    section.appendChild(recorded);
    if (sensors.stale) {
      section.appendChild(el("p")).appendChild(badge("alert", "Stored history is not recent. Last reading: " + sensorDate.format(new Date(latest.observed_at)) + " (UK time).", "caution"));
    }
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
    section.appendChild(el("p", "Demo display ranges are not safe or unsafe limits. Readings that are missing or look wrong appear as gaps, not zero."));
    var forecast = sensors.forecast;
    var hasForecast = !!(forecast && forecast.points && forecast.points.length);
    if (hasForecast) {
      section.appendChild(el("h3", "Simple 24-hour synthetic forecast (estimate)", "forecast-heading"));
      section.appendChild(el("p", forecast.note + " Demo display ranges (-10 to 45\u00a0\u00b0C and 0 to 100\u00a0%) are chart limits, not safe or unsafe household limits."));
    } else if (forecast && forecast.reason) {
      section.appendChild(el("p", forecast.reason, "forecast-reason"));
    }
    sensorMetrics.forEach(function (metric) { section.appendChild(sensorChart(history, metric, forecast)); });
    var details = el("details");
    details.appendChild(el("summary", hasForecast ? "Show sensor history and forecast as a table" : "Show sensor history as a table"));
    var scroll = el("div", null, "sensor-table");
    scroll.tabIndex = 0;
    scroll.setAttribute("role", "region");
    scroll.setAttribute("aria-label", "Synthetic sensor history table");
    var table = el("table");
    table.appendChild(el("caption", hasForecast ? "Synthetic stored readings for your home, oldest first, then the forecast (estimate)" : "Synthetic stored readings for your home, oldest first"));
    var head = el("thead");
    var headings = el("tr");
    ["Recorded time (UK time)", "Temperature (\u00b0C)", "Humidity (%)"].forEach(function (text) {
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
    if (hasForecast) {
      forecast.points.forEach(function (point) {
        var tr = el("tr", null, "forecast-row");
        var timeCell = el("th");
        timeCell.scope = "row";
        timeCell.appendChild(sensorTime(point.forecast_at));
        timeCell.appendChild(el("span", " Forecast (estimate)"));
        tr.appendChild(timeCell);
        sensorMetrics.forEach(function (metric) {
          var value = point[metric.key];
          tr.appendChild(el("td", value === null || value === undefined ? "No forecast for this channel" : sensorNumber.format(value) + " " + metric.unit + " (estimate)"));
        });
        body.appendChild(tr);
      });
    }
    table.appendChild(body);
    scroll.appendChild(table);
    details.appendChild(scroll);
    section.appendChild(details);
    return section;
  }

  var NAV = [
    ["sec-summary", "Summary", "summary"], ["sec-status", "Status", "clock"], ["sec-actions", "Needed from you", "alert"],
    ["sec-timeline", "Timeline", "timeline"], ["sec-documents", "Documents", "document"], ["sec-funding", "Funding", "funding"],
    ["sec-help", "Help and callbacks", "phone"], ["sec-sensors", "Sensors", "sensors"], ["sec-unavailable", "Showcase limits", "ban"]
  ];
  var STATE_TEXT = { completed: "Completed", current: "Current stage", upcoming: "Not started", unknown: "Not shown" };
  var STATE_ICON = { completed: "check", current: "clock", upcoming: "ban", unknown: "info" };

  function sectionNav(callbacks) {
    var nav = el("nav", null, "section-nav");
    nav.id = "page-nav";
    nav.setAttribute("aria-label", "Page sections");
    var list = el("ul");
    NAV.forEach(function (item, index) {
      var li = el("li");
      var a = withIcon(el("a"), item[2], item[0] === "sec-help" && !callbacks ? "Help" : item[1]);
      a.href = "#" + item[0];
      if (index === 0) a.setAttribute("aria-current", "location");
      a.addEventListener("click", function () {
        list.querySelectorAll("a").forEach(function (other) { other.removeAttribute("aria-current"); });
        a.setAttribute("aria-current", "location");
      });
      li.appendChild(a);
      list.appendChild(li);
    });
    nav.appendChild(list);
    return nav;
  }

  function linkList(sources) {
    var ul = el("ul");
    sources.forEach(function (source) {
      var li = el("li");
      var a = el("a", source.label);
      a.href = source.href;
      li.appendChild(a);
      ul.appendChild(li);
    });
    return ul;
  }

  function summarySection(view) {
    var box = sectionCard("sec-summary", "Case summary", "summary-card", "summary");
    var rules = view.summary;
    var generation = 0;
    box.appendChild(el("p", "Based only on the recorded facts shown on this page for your home. Neither rules nor AI can make decisions, approve documents, book works, or give consent.", "scope"));
    var badgeRow = el("p");
    var body = el("p");
    var disclaimer = el("p", null, "scope");
    var sourceHead = el("p", "Sources in your record:");
    var links = linkList(rules.sources);
    var aiSources = el("div");
    var consentLabel = el("label", null, "check");
    var consent = el("input");
    consent.type = "checkbox";
    consent.id = "summary-ai-consent";
    consent.name = "summary-ai-consent";
    consent.setAttribute("aria-describedby", "summary-status");
    consentLabel.appendChild(consent);
    consentLabel.appendChild(el("span", "Use my own case record to generate an AI summary (optional). This is not consent to works."));
    var actions = el("div", null, "summary-ai-actions");
    var generate = el("button", "Generate AI summary");
    generate.type = "button";
    generate.id = "summary-ai-button";
    var back = el("button", "Show rules summary instead", "secondary");
    back.type = "button";
    back.hidden = true;
    actions.appendChild(generate);
    actions.appendChild(back);
    var status = el("p");
    status.id = "summary-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");

    function showRules(note) {
      generation += 1;
      box.className = "card summary-card";
      badgeRow.textContent = "";
      badgeRow.appendChild(badge("list", rules.label));
      body.textContent = rules.text;
      disclaimer.textContent = "";
      aiSources.textContent = "";
      back.hidden = true;
      generate.disabled = false;
      box.removeAttribute("aria-busy");
      status.textContent = note || "";
    }

    function showAi(result) {
      box.className = "card summary-card ai";
      badgeRow.textContent = "";
      badgeRow.appendChild(badge("sparkle", "AI suggestion, not approved. Not an instruction.", "caution"));
      body.textContent = result.answer;
      disclaimer.textContent = "AI-generated content may be incorrect. Check the linked sections below. AI cannot make decisions, approve documents, or change your case.";
      aiSources.textContent = "";
      if (result.sources && result.sources.length) {
        aiSources.appendChild(el("p", "Record facts the AI used:"));
        var ul = el("ul");
        result.sources.forEach(function (text) { ul.appendChild(el("li", text)); });
        aiSources.appendChild(ul);
      }
      back.hidden = false;
      status.textContent = "AI summary ready. It is a suggestion, not approved.";
    }

    function reason(label) {
      var marker = "AI unavailable: ";
      var at = label ? label.indexOf(marker) : -1;
      if (at >= 0) return label.slice(at + marker.length);
      return label && label.indexOf("not enabled") >= 0 ? "AI is not enabled" : "the assistant could not be reached";
    }

    function fallback(why) {
      showRules("AI summary is not available right now (" + why + "). Showing the rules-based summary from your recorded case facts instead.");
    }

    generate.addEventListener("click", function () {
      if (generate.disabled) return;
      if (!consent.checked) {
        consent.setAttribute("aria-invalid", "true");
        status.textContent = "Agree to use your own case record before requesting an AI summary.";
        consent.focus();
        return;
      }
      consent.removeAttribute("aria-invalid");
      var current = ++generation;
      var held = transition;
      generate.disabled = true;
      box.setAttribute("aria-busy", "true");
      status.textContent = "Generating AI case summary\u2026";
      api("/demo/assistant", { method: "POST", body: JSON.stringify({ topic: "status", use_record: true }) }).then(function (res) {
        if (current !== generation || held !== transition) return;
        if (res.status === 401) { showSignin("Please sign in again."); return; }
        if (res.ok && res.body.label && res.body.label.indexOf("AI") === 0) { generate.disabled = false; box.removeAttribute("aria-busy"); showAi(res.body); return; }
        fallback(res.ok ? reason(res.body.label) : "the assistant could not be reached");
      }).catch(function () {
        if (current === generation && held === transition) fallback("the assistant could not be reached");
      });
    });
    consent.addEventListener("change", function () {
      if (consent.checked) { consent.removeAttribute("aria-invalid"); return; }
      showRules("Record use for AI summary stopped. Showing the rules-based summary.");
    });
    back.addEventListener("click", function () {
      showRules("Showing the rules-based summary.");
      generate.focus();
    });

    box.appendChild(badgeRow);
    box.appendChild(body);
    box.appendChild(disclaimer);
    box.appendChild(sourceHead);
    box.appendChild(links);
    box.appendChild(aiSources);
    box.appendChild(consentLabel);
    box.appendChild(actions);
    box.appendChild(status);
    showRules("");
    return box;
  }

  function statusSection(view) {
    var box = sectionCard("sec-status", "Current status and next step", "", "clock");
    if (view.stage) box.appendChild(el("p")).appendChild(badge("clock", "Stage: " + view.stage));
    if (view.progress) {
      box.appendChild(el("h3", "Where things are"));
      box.appendChild(el("p", view.progress));
    }
    if (view.closed) box.appendChild(el("p")).appendChild(badge("check", view.closed, "ok"));
    if (view.next_step) {
      box.appendChild(el("h3", "What happens next"));
      box.appendChild(el("p", view.next_step));
    }
    return box;
  }

  function actionsSection(view) {
    var box = sectionCard("sec-actions", "What is needed from you", "", "alert");
    var needed = view.needed || [];
    if (!needed.length) {
      box.appendChild(el("p")).appendChild(badge("check", "No action needed", "ok"));
      box.appendChild(el("p", "Nothing is needed from you right now. Zava North Homes is working on the current step. We will contact you if we need anything."));
    } else {
      box.appendChild(el("p")).appendChild(badge("alert", needed.length + (needed.length === 1 ? " item needs" : " items need") + " your attention", "caution"));
      var ul = el("ul", null, "needed");
      needed.forEach(function (item) { withIcon(ul.appendChild(el("li")), "alert", ""); ul.lastChild.lastChild.textContent = ""; ul.lastChild.appendChild(el("span", item.text)); });
      box.appendChild(ul);
    }
    if (view.callbacks_available) {
      var optional = el("p", "Optional: ");
      var link = el("a", "Book a synthetic callback");
      link.href = "#sec-help";
      optional.appendChild(link);
      box.appendChild(optional);
    }
    return box;
  }

  function timelineSection(view) {
    var box = sectionCard("sec-timeline", "Case timeline and planned improvements", "", "timeline");
    var steps = el("ol", null, "stepper");
    (view.timeline || []).forEach(function (step, index) {
      var li = el("li", null, "step " + step.state);
      if (step.state === "current") li.setAttribute("aria-current", "step");
      li.appendChild(el("span", (index + 1) + ". " + step.name));
      withIcon(li.appendChild(el("span", null, "state")), STATE_ICON[step.state], STATE_TEXT[step.state]);
      steps.appendChild(li);
    });
    box.appendChild(steps);
    box.appendChild(el("h3", "Planned improvements"));
    if (view.measures && view.measures.length) {
      var ul = el("ul", null, "doc-list");
      view.measures.forEach(function (m) { withIcon(ul.appendChild(el("li", null, "doc-item")), "home", m); });
      box.appendChild(ul);
    } else {
      box.appendChild(el("p", "No planned improvements are recorded for your home in this view."));
    }
    return box;
  }

  function documentsSection(view) {
    var box = sectionCard("sec-documents", "Documents and checks", "", "document");
    box.appendChild(el("p", "These are recorded facts from your case file, not a decision that any document is approved. A clean file check only means the file was scanned; a person still needs to review it. Uploading or downloading files is not available in this showcase."));
    var docs = view.documents || {};
    box.appendChild(el("h3", "Requested documents"));
    if (docs.requests === null || docs.requests === undefined) {
      box.appendChild(el("p", "This view does not show which documents have been requested for your case."));
    } else if (!docs.requests.length) {
      box.appendChild(el("p", "No document requests are recorded for your case."));
    } else {
      var rl = el("ul", null, "doc-list");
      docs.requests.forEach(function (r) {
        var li = rl.appendChild(el("li", null, "doc-item"));
        li.appendChild(el("strong", r.kind + " (" + r.id + ") "));
        li.appendChild(badge(r.state === "missing" ? "alert" : r.state === "provided" ? "check" : "info", r.state_label, r.state === "missing" ? "caution" : ""));
        li.appendChild(el("p", "How to provide it: " + r.how_to_provide));
      });
      box.appendChild(rl);
    }
    box.appendChild(el("h3", "Presented documents on file"));
    if (docs.presented === null || docs.presented === undefined) {
      box.appendChild(el("p", "Presented documents and their file checks are not shown in this view."));
    } else if (!docs.presented.length) {
      box.appendChild(el("p", "No presented documents are recorded in this view."));
    } else {
      var pl = el("ul", null, "doc-list");
      docs.presented.forEach(function (d) {
        var li = pl.appendChild(el("li", null, "doc-item"));
        li.appendChild(el("strong", d.kind + " (" + d.id + ") "));
        li.appendChild(badge("document", d.status_label));
        var bad = d.scan_status === "pending" || d.scan_status === "infected" || d.scan_status === "mismatch";
        li.appendChild(el("p")).appendChild(badge(bad ? "alert" : d.scan_status === "clean" ? "check" : "info", d.scan_label, bad ? "warn" : ""));
        (d.issues || []).forEach(function (issue) { li.appendChild(el("p", issue.severity.charAt(0).toUpperCase() + issue.severity.slice(1) + ": " + issue.message)); });
      });
      box.appendChild(pl);
    }
    return box;
  }

  function fundingSection() {
    var box = sectionCard("sec-funding", "Funding and household costs", "", "funding");
    box.appendChild(el("p", "Programme funding and grant checks are handled by Zava North Homes staff. You are not asked to pay anything or approve funding on this page. If you are a leaseholder or shared owner, we will explain your reviewed lease position in writing before asking you for any decision. Speak to your housing officer if you have questions."));
    return box;
  }

  function render(view, announce) {
    removeAppointments();
    endLoading();
    assistant.setSession(true);
    content.textContent = "";
    if (view.home) {
      var strip = el("div", null, "home-strip");
      withIcon(strip.appendChild(el("span", null, "addr")), "home", [view.home.address, view.home.town, view.home.postcode].filter(Boolean).join(", "));
      strip.appendChild(badge("info", "Synthetic showcase record - read-only"));
      content.appendChild(strip);
    }
    content.appendChild(sectionNav(view.callbacks_available));
    content.appendChild(summarySection(view));
    var grid = el("div", null, "status-grid");
    grid.appendChild(statusSection(view));
    grid.appendChild(actionsSection(view));
    content.appendChild(grid);
    content.appendChild(timelineSection(view));
    content.appendChild(documentsSection(view));
    content.appendChild(fundingSection());
    var help = sectionCard("sec-help", "Help and other ways to reach us", "", "phone");
    help.appendChild(el("p", view.help.summary));
    var hl = el("ul");
    view.help.routes.forEach(function (r) { hl.appendChild(el("li", r)); });
    help.appendChild(hl);
    help.appendChild(el("p", view.help.note));
    content.appendChild(help);
    if (view.callbacks_available) {
      var callbacks = el("section", null, "card callbacks");
      callbacks.setAttribute("aria-labelledby", "callback-title");
      content.appendChild(callbacks);
      callbackController = window.mountResidentAppointments(callbacks, api, showSignin);
    } else {
      help.appendChild(el("p", "Synthetic callback booking is not connected in this showcase. Use the contact routes above."));
    }
    if (view.sensors) {
      content.appendChild(renderSensors(view.sensors));
    }

    var unavailable = sectionCard("sec-unavailable", "Not available in this showcase", "", "ban");
    if (view.banner) unavailable.appendChild(el("p", view.banner));
    var ul = el("ul", null, "unavail");
    view.unavailable.filter(function (u) { return u.feature !== "Automated answers"; }).forEach(function (u) {
      var li = el("li");
      var appointment = u.feature === "Replying to an appointment";
      var b = el("button", appointment ? "Operational appointments" : u.feature);
      b.type = "button";
      b.disabled = true;
      b.setAttribute("aria-disabled", "true");
      li.appendChild(b);
      li.appendChild(el("span", appointment ? "You cannot change live works appointments here." + (view.callbacks_available ? " Use the form above for local synthetic callbacks only." : "") : u.reason, "why"));
      ul.appendChild(li);
    });
    unavailable.appendChild(ul);
    content.appendChild(unavailable);

    errorEl.hidden = true;
    signin.hidden = true;
    lede.textContent = signedInLede + (view.callbacks_available ? callbackLede : "");
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
    clearPersonal();
    endLoading();
    signinButton.disabled = false;
    lede.textContent = signedOutLede;
    clearInvalid();
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
    clearPersonal();
    endLoading();
    signin.hidden = true;
    statusEl.textContent = "";
    errorText.textContent = message;
    errorEl.hidden = false;
    errorTitle.focus();
  }

  function api(path, options) {
    options = options || {};
    var current = transition;
    var headers = { Accept: "application/json" };
    if (options.body) headers["Content-Type"] = "application/json";
    if (options.method === "POST") headers["X-CSRF-Token"] = csrf;
    if (["/demo/view", "/demo/assistant", "/demo/agenda"].includes(path)) {
      headers["X-Resident-Session"] = sessionId;
    }
    return fetch(path, { method: options.method || "GET", headers: headers, body: options.body, cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        return r.json().then(function (body) {
          if (current === transition && body.session_changed) showSignin(body.error);
          return { ok: r.ok, status: r.status, body: body, retryAfter: Number(r.headers && r.headers.get && r.headers.get("Retry-After")) };
        });
      });
  }

  function loadView(announce, retried) {
    var current = transition;
    if (!loading) statusEl.textContent = "Loading your progress\u2026";
    return api("/demo/view").then(function (res) {
      if (current !== transition) return;
      if (res.status === 503 && !retried) {
        var wait = res.retryAfter > 0 && res.retryAfter <= 10 ? res.retryAfter : 3;
        statusEl.textContent = "The showcase is busy. Trying again in a few seconds\u2026";
        return new Promise(function (resolve) { setTimeout(resolve, wait * 1000); }).then(function () {
          if (current === transition) return loadView(announce, true);
        });
      }
      if (res.ok) render(res.body, announce);
      else if (res.status === 401) showSignin("Please sign in again.");
      else fail(res.body.error || "Something went wrong.");
    });
  }

  var signedOut = false;

  function start() {
    clearPersonal();
    var current = transition;
    signin.hidden = true;
    errorEl.hidden = true;
    statusEl.textContent = "Loading\u2026";
    var slow = setTimeout(function () {
      if (current === transition && statusEl.textContent === "Loading\u2026") {
        statusEl.textContent = "Still loading. The showcase may be waking up, which can take up to 30 seconds. Please wait.";
      }
    }, 4000);
    api("/demo/session")
      .then(function (res) {
        clearTimeout(slow);
        if (current !== transition) return;
        if (!res.ok) { fail(res.body.error || "The showcase is not available right now."); return; }
        csrf = res.body.csrf;
        if (res.body.signed_in) {
          sessionId = res.body.session_id;
          return loadView();
        }
        showSignin(pendingNotice || undefined);
        pendingNotice = "";
        if (signedOut) {
          signedOut = false;
          statusEl.textContent = "You have signed out.";
          document.getElementById("signin-title").setAttribute("tabindex", "-1");
          document.getElementById("signin-title").focus();
        }
      })
      .catch(function () {
        clearTimeout(slow);
        if (current === transition) fail("We could not reach the showcase. Check your connection, then try again.");
      });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = emailField.value;
    var password = passwordField.value;
    var noEmail = !email.trim();
    var noPassword = !password;
    clearInvalid();
    if (noEmail || noPassword) {
      [[noEmail, emailField], [noPassword, passwordField]].forEach(function (pair) {
        if (!pair[0]) return;
        pair[1].setAttribute("aria-invalid", "true");
        pair[1].setAttribute("aria-describedby", "signin-error");
      });
      signinError.textContent = noEmail && noPassword ? "Enter your email address and the password."
        : noEmail ? "Enter your email address." : "Enter the password.";
      signinError.hidden = false;
      (noEmail ? emailField : passwordField).focus();
      return;
    }
    signinButton.disabled = true;
    signinError.hidden = true;
    var current = ++transition;
    beginLoading("Signing you in and loading your home progress\u2026");
    api("/demo/login", { method: "POST", body: JSON.stringify({ email: email, password: password }) })
      .then(function (res) {
        if (current !== transition) return;
        passwordField.value = "";
        if (res.ok) {
          csrf = res.body.csrf || csrf;
          sessionId = res.body.session_id;
          sessionChannel.postMessage("changed");
          return loadView("You are signed in. Your progress is shown below.");
        }
        if (res.status === 403) {
          pendingNotice = "Your page session was refreshed. Enter the password and try signing in again.";
          start();
          return;
        }
        showSignin(res.body.error || "We could not sign you in.");
      })
      .catch(function () {
        if (current === transition) showSignin("We could not reach the showcase. Check your connection, then select Sign in to try again.");
      })
      .then(function () { if (current === transition) signinButton.disabled = false; });
  });

  document.getElementById("signout").addEventListener("click", function () {
    var held = sessionId;
    clearPersonal();
    var current = transition;
    function notConfirmed() {
      if (current === transition) fail("We could not confirm that you signed out. You may still be signed in on this device. You will be signed out by itself within 30 minutes. Select Try again to check, then sign out again.");
    }
    fetch("/demo/logout", { method: "POST", headers: { "X-CSRF-Token": csrf, "X-Resident-Session": held, "Content-Type": "application/json" }, body: "{}", cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        if (current !== transition) return;
        if (!r.ok) { notConfirmed(); return; }
        sessionChannel.postMessage("changed");
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
