"use strict";
// Quality checks, defects, capacity and work orders. Shares h, api, post, me, show and isManager with app.js.
const QUALITY_ROLES = ["Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer"];
const SENSOR_ROLES = ["Quality Inspector", "Retrofit Programme Manager"];
const QUALITY_SOURCES = ["Installer", "Contractor", "Provider submission", "Our own inspection"];
const WO_OUTCOMES = ["Booked", "Declined by provider", "Resident not available", "No access", "Rebooking needed"];
// Keeps a message that already names an owner and a next action; otherwise adds both.
const opsOwned = (message, owner, next, status) => {
  const m = String(message ?? "").trim().replace(/([^.!?])$/, "$1.");
  const o = m.indexOf("Owner:");
  if (o >= 0 && m.indexOf("Next action:") > o) return m;
  const refused = status >= 400 && status < 500;
  return `${m} Owner: ${refused ? "your team manager" : owner}. Next action: ${refused ? "follow the advice above, or ask your team manager if you cannot" : next}`;
};
const OPS_SUPPORT = "application support";
const OPS_MANUAL_NEXT = "use the manual route and tell application support if it continues";
let capacityHistoryBarrier = null;
let capacityHistoryGeneration;
const QUALITY_WORDS = { "Submitted": "Waiting for an independent check", "Returned": "Returned: defect to put right", "Fixed, awaiting reinspection": "Fixed, waiting to be checked again",
  "Accepted": "Accepted, ready to hand over to the resident", "Handed over": "Handed over to the resident",
  "Superseded": "Replaced evidence: previous acceptance and handover no longer apply" };

function residentBindings(text) {
  if (!text.trim()) throw new Error("Enter each affected measure and current scope revision.");
  return text.split(";").map((line) => {
    const parts = line.split("|");
    if (parts.length !== 2 || !parts[0].trim() || !/^[1-9][0-9]*$/.test(parts[1].trim())) {
      throw new Error("Use Measure|revision, separated by semicolons. Check current revisions on the case.");
    }
    return { measure: parts[0].trim(), context_revision: Number(parts[1].trim()) };
  });
}

// The simulation panel keeps the full layout. The Home sensors tab passes `home` for the plain layout: local time first, no IDs.
function sensorTable(title, rows, absent, labels = {}, home = null) {
  const box = h("div", {}, h(home ? home.heading : "h3", {}, title));
  if (!rows || !rows.length) return box.append(h("p", {}, absent || "No retained readings.")), box;
  const name = (home && home.name) || title;
  const varies = (key) => new Set(rows.map((r) => r[key])).size > 1;
  const head = home
    ? ["Observed (UK time)", "Temperature (degC)", "Relative humidity (%RH)", ...(varies("sensor_id") ? ["Sensor"] : []), ...(varies("provenance_class") ? ["Source"] : [])]
    : ["Reading ID", "Sensor ID", "Observed (UTC)", "Temperature (degC)", "Relative humidity (%RH)", "Source"];
  const cells = (r) => home
    ? [h("th", { scope: "row" }, sensorTimeNode(r.observed_at, home.generated)), h("td", {}, sensorValue(r.temperature_c)), h("td", {}, sensorValue(r.humidity_pct)),
      ...(varies("sensor_id") ? [h("td", {}, sensorCode(r.sensor_id))] : []), ...(varies("provenance_class") ? [h("td", {}, SENSOR_SOURCES[r.provenance_class] || "Synthetic")] : [])]
    : [h("th", { scope: "row" }, r.reading_id), h("td", {}, r.sensor_id),
      h("td", {}, h("time", { datetime: r.observed_at }, r.observed_at)), h("td", {}, r.temperature_c), h("td", {}, r.humidity_pct),
      h("td", {}, labels[r.provenance_class] || "Synthetic reading, not calibrated")];
  box.append(h("div", { class: "table-scroll", role: "region", tabindex: 0, "aria-label": `${name} table` },
    h("table", {}, h("caption", { class: "sr-only" }, name),
      h("thead", {}, h("tr", {}, head.map((t) => h("th", { scope: "col" }, t)))),
      h("tbody", {}, rows.map((r) => h("tr", {}, cells(r)))))));
  return box;
}

function sensorDraftSection(id) {
  const body = h("div", {});
  const box = h("section", { id: "sensor-drafts" }, body);
  api(`/api/cases/${encodeURIComponent(id)}/sensor-drafts`).then((v) => {
    if (v.state === "disabled") return;
    box.setAttribute("aria-labelledby", "sensor-drafts-h");
    const kids = [h("h3", { id: "sensor-drafts-h" }, "Sensor review draft")];
    if (v.state === "consent-withheld") {
      kids.push(h("p", { role: "status" }, opsOwned("Saved drafts are withheld because monitoring consent is not granted now.", "the resident's consent owner", "use the ordinary quality check, and ask the resident liaison officer whether consent can be recorded.")));
    } else if (!v.drafts.length) {
      kids.push(h("p", {}, "No review draft exists for this home yet. Owner: a Quality Inspector. Next action: use the ordinary quality check."));
    } else {
      kids.push(h("ul", {}, v.drafts.map((d) => {
        if (d.state !== "PROPOSED_UNAPPROVED") return h("li", {}, "A saved draft failed its integrity check and is withheld. Owner: application support. Next action: tell application support, and use the ordinary quality check.");
        const c = d.candidate, l = d.lineage;
        const row = (name, value) => [h("dt", {}, name), h("dd", {}, value)];
        return h("li", {},
          h("p", {}, d.label),
          h("p", {}, "Not reviewed by a person yet."),
          h("p", {}, c.summary),
          h("details", {}, h("summary", {}, "Rule and version details"), h("dl", {},
            row("Rule", sensorCode(c.rule_id)), row("Policy version", c.policy_version), row("Analysis version", c.analysis_version),
            row("Readings used", [sensorTimeNode(l.window_start), " to ", sensorTimeNode(l.window_end), " (UK time)"]),
            row("Created by", `${d.created_by.name} (${d.created_by.role})`), row("Created", [sensorTimeNode(d.created_at), " (UK time)"]),
            row("Draft reference", sensorCode(d.digest_prefix)), row("Note", d.approval_note))));
      })));
    }
    body.replaceChildren(...kids);
  }).catch(() => {
    body.replaceChildren(h("p", { class: "err", role: "alert" }, "Sensor review drafts are unavailable right now. Owner: application support. Next action: refresh this page. If it keeps happening, tell application support. Use the ordinary quality check meanwhile."));
  });
  return box;
}

function sensorPanel(id) {
  const status = h("p", { class: "status-line", role: "status" }, SENSOR_COPY.loading.words);
  const checked = h("p", { class: "muted" });
  const body = h("div", {});
  const box = h("section", { id: "sensors", "aria-busy": "true" },
    h("div", { "data-sensor-badges": "" }, status, checked),
    h("p", { class: "muted", "data-sensor-advisory": "" }, "Readings are advice for a person to check. They do not change the case."),
    body);
  const paint = (state, kids) => {
    status.className = `status-line ${state.tone}`.trim();
    status.textContent = state.words;
    body.replaceChildren(...kids.filter(Boolean));
    box.removeAttribute("aria-busy");
  };
  const stop = (key) => {
    const state = sensorState(key);
    paint(state, state.notice ? [h("p", {}, state.notice)] : []);
  };
  if (!SENSOR_ROLES.includes(me.user.role)) return stop("restricted"), box;
  api(`/api/cases/${encodeURIComponent(id)}/sensors`).then((v) => {
    const model = sensorModel(v);
    const state = sensorState(model.status);
    const kids = v.state === "ok" ? sensorBody(v, model) : [h("p", {}, state.notice)];
    if (v.state !== "unavailable") kids.push(sensorDraftSection(id));
    if (v.state === "ok") kids.push(sensorAbout(v));
    checked.append("Checked ", sensorTimeNode(v.generated_at), " (UK time)");
    paint(state, kids);
    if (model.alerts.length) box.setAttribute("data-sensor-alerts", String(model.alerts.length));
  }).catch(({ status: code, message } = {}) => stop(sensorFailure(code, message)));
  return box;
}

function sensorPointer(session) {
  return h("p", {}, "Home sensor readings and alerts are on the Home sensors tab. ",
    h("button", { class: "alt", type: "button", onclick: () => session.controller ? session.controller.select("sensors", true, true) : document.getElementById("case-panel-sensors").scrollIntoView() }, "Open Home sensors"));
}

// Both rules are copies of server rules (sensor_view.FRESH_SECONDS and sensor_map.OFFLINE_SECONDS); a test pins them.
const SENSOR_FRESH_SECONDS = 900;
const SENSOR_OFFLINE_SECONDS = 86400;
const SENSOR_FRESH_TEXT = `${SENSOR_FRESH_SECONDS / 60} minutes`;
const SENSOR_OFFLINE_TEXT = `${SENSOR_OFFLINE_SECONDS / 3600} hours`;
const SENSOR_SOURCES = { "synthetic-weather-derived": "Outdoor weather", "synthetic-modelled-indoor": "Modelled indoor", "synthetic-unclassified": "Unknown origin" };
const SENSOR_MEASURES = { dew_point_c: "dew point", mould_risk_index: "mould risk" };
// Plain wording for every state, keyed by the badge states of sensor_badges.py plus the states only this screen reaches.
// A stop or an alert is one message: reason, Owner, Next action. Status words match the map labels in sensor_map.py,
// except that the 24 hour state says "may be offline" as its alert does, because a missing reading is not proof.
// The badge state "offline" means no reading has arrived; "offline-24h" is an old reading, which the map calls offline.
const SENSOR_COPY = {
  loading: { words: "Loading home sensors" },
  restricted: { words: "Sensor readings are not shown for your role", message: "Your role does not include indoor readings. Owner: a Quality Inspector or a Retrofit Programme Manager. Next action: ask one of them for the readings you need." },
  "not-connected": { words: "Sensor readings are not connected in this setup", message: "Owner: application support. Next action: use the ordinary quality check. Tell application support if you expected readings here." },
  "not-linked": { tone: "danger", words: "Your staff account is not linked to your role", message: "Your staff account is not linked to your role, so home readings are hidden. Owner: your team manager. Next action: ask them to check that your account is on the staff list with your role, then refresh this page. Until then, use the ordinary quality check." },
  "service-down": { tone: "danger", message: "Home sensors are unavailable right now. Owner: application support. Next action: refresh this page. If it keeps happening, tell application support. Use the ordinary quality check meanwhile." },
  offline: { words: "No sensor readings recorded", message: "Use the ordinary quality check." },
  withheld: { words: "Readings withheld: monitoring consent is not granted", message: "Owner: the resident's consent owner. Next action: use the ordinary quality check. Do not ask for the readings without consent. If you think consent has been given, ask the resident liaison officer to record it." },
  unavailable: { tone: "danger", message: "Sensor readings could not be read. Owner: application support. Next action: refresh this home. If it keeps happening, tell application support. Use the ordinary quality check meanwhile." },
  unknown: { words: "Latest reading is dated in the future and is not treated as recent" },
  fresh: { tone: "ok", words: `Recent reading (within ${SENSOR_FRESH_TEXT})` },
  stale: { tone: "wait", words: `Reading out of date (older than ${SENSOR_FRESH_TEXT})`, alert: { heading: "Reading out of date", message: `The latest reading is older than ${SENSOR_FRESH_TEXT}. Last reading {age} ago. Owner: the quality team. Next action: treat the reading as out of date. Use the ordinary quality check for now.` } },
  "offline-24h": { tone: "danger", words: `Sensor may be offline (no reading for over ${SENSOR_OFFLINE_TEXT})`, alert: { heading: "Sensor may be offline", message: `No reading for over ${SENSOR_OFFLINE_TEXT}. Last reading {age} ago. Owner: the quality team. Next action: use the ordinary quality check, then ask the quality team to check the sensor.` } },
  conflict: { tone: "danger", words: "Readings disagree", alert: { heading: "Readings disagree", message: "Two retained readings disagree for the same sensor and time. Do not choose between them. Owner: the quality team. Next action: use the ordinary quality check and ask the quality team to check the sensor." } },
  fault: { tone: "danger", words: "Sensor fault", alert: { heading: "Sensor fault", message: "The latest reading is missing a value or cannot be read. Owner: the quality team. Next action: do not use this reading. Use the ordinary quality check and report the sensor fault." } },
  out_of_range: { tone: "danger", words: "Reading out of range", alert: { heading: "Reading out of range", message: "The latest reading is outside the possible range. Owner: the quality team. Next action: do not use this reading. Use the ordinary quality check and ask for a check." } },
  uncalibrated: { words: "Not calibrated" },
};

function sensorSplit(message) {
  const m = /^(.*?)\s*Owner: (.*?)\. Next action: (.*)$/s.exec(message);
  return m ? { what: m[1], owner: m[2], next: m[3] } : { what: message, owner: "", next: "" };
}

// Status words, tone and the notice under them for one state. A state whose message starts with its own words shows the rest as the notice.
function sensorState(key) {
  const entry = SENSOR_COPY[key] || SENSOR_COPY.unavailable;
  const parts = sensorSplit(entry.message || "");
  return { tone: entry.tone || "", words: entry.words || parts.what.replace(/\.$/, ""),
    notice: entry.words || !parts.owner ? entry.message || "" : `Owner: ${parts.owner}. Next action: ${parts.next}` };
}

const sensorFailure = (status, message) => status === 403 && /staff role has changed or been revoked/i.test(message) ? "not-linked"
  : status === 400 && /durable sql/i.test(message) ? "not-connected" : "service-down";

// Alerts are a reading older than 15 minutes (older than 24 hours reads as offline) and the health problems in the payload.
function sensorModel(v) {
  const kinds = {};
  for (const b of v.badges || []) kinds[b.kind] = b.state;
  const byState = { "consent-withheld": "withheld", unavailable: "unavailable", "no-readings": "offline" };
  const fresh = kinds.freshness || byState[v.state] || v.freshness || "unknown";
  const alerts = [];
  if (SENSOR_COPY[kinds.health] && SENSOR_COPY[kinds.health].alert) alerts.push(kinds.health);
  if (fresh === "stale") alerts.push(Number(v.age_seconds) > SENSOR_OFFLINE_SECONDS ? "offline-24h" : "stale");
  return { fresh, alerts, status: alerts[0] || fresh };
}

function sensorTime(iso, generated) {
  const at = new Date(iso);
  if (Number.isNaN(at.getTime())) return "Time not recorded";
  const year = (date) => new Intl.DateTimeFormat("en-GB", { year: "numeric", timeZone: "Europe/London" }).format(date);
  const same = generated && !Number.isNaN(new Date(generated).getTime()) && year(new Date(generated)) === year(at);
  return new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", ...(same ? {} : { year: "numeric" }), hour: "2-digit", minute: "2-digit", hourCycle: "h23", timeZone: "Europe/London" }).format(at);
}
const sensorTimeNode = (iso, generated) => h("time", { datetime: iso }, sensorTime(iso, generated));
const sensorCode = (text) => h("span", { translate: "no" }, text);
const sensorValue = (value, unit = "") => value === null || value === undefined || value === "" ? "Missing" : `${value}${unit ? ` ${unit}` : ""}`;

function sensorAge(seconds) {
  const minutes = Math.floor(Math.max(0, Number(seconds) || 0) / 60);
  const count = (n, unit) => `${n} ${unit}${n === 1 ? "" : "s"}`;
  if (minutes < 1) return "less than a minute";
  return minutes < 120 ? count(minutes, "minute") : minutes < 2880 ? count(Math.round(minutes / 60), "hour") : count(Math.round(minutes / 1440), "day");
}

function sensorAlertList(model, v) {
  if (!model.alerts.length) return h("p", {}, "No sensor alerts for this home.");
  const age = v.age_seconds === null || v.age_seconds === undefined ? "" : sensorAge(v.age_seconds);
  const upper = (text) => text.charAt(0).toUpperCase() + text.slice(1);
  return h("ul", { class: "sensor-alerts" }, model.alerts.map((key, index) => {
    const { alert } = SENSOR_COPY[key];
    const parts = sensorSplit(age ? alert.message.replace("{age}", age) : alert.message.replace(" Last reading {age} ago.", ""));
    // The server words the next action for its most serious state, which is the first alert unless the age rule made it offline.
    const next = index === 0 && v.next_action && key !== "offline-24h" ? v.next_action : upper(parts.next);
    return h("li", { class: `sensor-alert ${SENSOR_COPY[key].tone}`.trim(), ...(key === "conflict" ? { "data-sensor-conflict": "" } : {}) },
      h("h4", {}, alert.heading),
      h("dl", {}, h("dt", {}, "What we see"), h("dd", {}, parts.what),
        h("dt", {}, "Owner"), h("dd", {}, upper(parts.owner)),
        h("dt", {}, "Next action"), h("dd", index === 0 ? { "data-sensor-next-action": "" } : {}, next)));
  }));
}

function sensorLatest(v, model) {
  const r = v.latest;
  const aged = ["fresh", "stale"].includes(model.fresh) && v.age_seconds !== null && v.age_seconds !== undefined;
  const old = model.alerts.includes("stale") || model.alerts.includes("offline-24h");
  const unusable = model.alerts.includes("fault") || model.alerts.includes("out_of_range");
  const rows = [["Temperature", sensorValue(r.temperature_c, "degC")], ["Relative humidity", sensorValue(r.humidity_pct, "%RH")],
    ["Observed", [sensorTimeNode(r.observed_at), ` (UK time)${aged ? `, ${sensorAge(v.age_seconds)} ago` : ""}${old ? ", out of date" : ""}`]],
    ["Sensor", sensorCode(r.sensor_id)], ["Source", `${SENSOR_SOURCES[r.provenance_class] || "Synthetic"}. ${SENSOR_COPY.uncalibrated.words}.`]];
  return h("div", {}, h("h3", {}, "Latest reading"), unusable && h("p", {}, "Do not use this reading. See the alert above."),
    h("dl", {}, rows.flatMap(([name, value]) => [h("dt", {}, name), h("dd", {}, value)])));
}

// The retained rows that disagree: matched by the citation keys the server names, or by sensor and time.
function sensorClashes(v) {
  const keys = new Set(), places = new Set();
  for (const c of v.conflicting_readings || []) {
    (c.citation_keys || []).forEach((key) => keys.add(key));
    places.add(`${c.sensor_id}|${c.observed_at}`);
  }
  const rows = [...(v.readings || []), ...(v.before || []), ...(v.after || [])];
  const named = rows.filter((r) => keys.has(`sensor:${r.sensor_id}:${r.reading_id}`));
  const found = named.length ? named : rows.filter((r) => places.has(`${r.sensor_id}|${r.observed_at}`));
  return found.filter((r, i) => found.findIndex((o) => o.sensor_id === r.sensor_id && o.reading_id === r.reading_id) === i);
}

function sensorSourceNote(rows, labels) {
  const classes = [...new Set(rows.map((r) => r.provenance_class))];
  return classes.length === 1 ? `Source of every row: ${labels[classes[0]] || "Synthetic reading, not calibrated."}`
    : "Rows come from more than one source, shown in the Source column. None of them is calibrated.";
}

function sensorReferences(v) {
  const rows = [...(v.readings || []).slice().reverse(), ...(v.before || []), ...(v.after || [])]
    .filter((r, i, all) => all.findIndex((o) => o.sensor_id === r.sensor_id && o.reading_id === r.reading_id) === i);
  if (!rows.length) return null;
  return h("details", {}, h("summary", {}, "Reference numbers"),
    h("p", { class: "muted" }, "Quote a reference number when you ask the quality team about a reading."),
    h("ul", {}, rows.map((r) => h("li", {}, sensorCode(r.reading_id), `: ${sensorValue(r.temperature_c, "degC")}, ${sensorValue(r.humidity_pct, "%RH")}, observed `,
      sensorTimeNode(r.observed_at), " (sensor ", sensorCode(r.sensor_id), ")"))));
}

function sensorAnchor(v, table) {
  const at = v.anchor && v.anchor.at;
  const box = h("div", {}, h("h3", {}, "Around the first quality evidence record"));
  if (!at) return box.append(h("p", {}, "There is no quality evidence record yet, so there is nothing to compare around.")), box;
  box.append(h("p", { class: "muted" }, `Compared around ${fmtDate(at)}, the time of the first quality evidence record. This is not an installation date, and a change around it is not proof that the work caused it.`),
    table("Before", v.before, "No readings before that record.", { heading: "h4", name: "Readings before the first quality evidence record" }),
    table("From then on", v.after, "No readings from that record onward.", { heading: "h4", name: "Readings from the first quality evidence record onward" }));
  return box;
}

// Two vertical axes with their own scales: temperature on the left, relative humidity on the right.
const SENSOR_SVG = "http://www.w3.org/2000/svg";
const sensorSvg = (tag, attrs, ...kids) => {
  const el = document.createElementNS(SENSOR_SVG, tag);
  for (const [k, v] of Object.entries(attrs || {})) el.setAttribute(k, String(v));
  kids.flat().forEach((k) => k && el.append(k.nodeType ? k : document.createTextNode(k)));
  return el;
};

function sensorScale(values) {
  const lo = Math.min(...values), hi = Math.max(...values);
  const span = hi - lo || 1;
  const rough = span / 4;
  const mag = 10 ** Math.floor(Math.log10(rough));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((n) => n >= rough);
  const min = Math.floor(lo / step) * step;
  let max = Math.ceil(hi / step) * step;
  if (max === min) max = min + step;
  const ticks = [];
  for (let t = min; t <= max + step / 2; t += step) ticks.push(Math.round(t * 100) / 100);
  return { min: ticks[0], max: ticks[ticks.length - 1], ticks };
}

function sensorChart(v, model) {
  const rows = (v.readings || []).filter((r) => Number.isFinite(Number(r.temperature_c)) && Number.isFinite(Number(r.humidity_pct)) && r.temperature_c !== null && r.humidity_pct !== null)
    .map((r) => ({ at: new Date(r.observed_at), t: Number(r.temperature_c), rh: Number(r.humidity_pct), iso: r.observed_at }))
    .filter((r) => !Number.isNaN(r.at.getTime())).sort((a, b) => a.at - b.at);
  if (rows.length < 2) return null;
  const old = model.alerts.includes("stale") || model.alerts.includes("offline-24h");
  const W = 640, H = 300, L = 56, R = 56, T = 40, B = 44;
  const tScale = sensorScale(rows.map((r) => r.t)), hScale = sensorScale(rows.map((r) => r.rh));
  const x0 = rows[0].at.getTime(), x1 = rows[rows.length - 1].at.getTime();
  const x = (r) => L + (x1 === x0 ? 0 : (r.at.getTime() - x0) / (x1 - x0)) * (W - L - R);
  const y = (scale, value) => T + (1 - (value - scale.min) / (scale.max - scale.min)) * (H - T - B);
  const pts = (key, scale) => rows.map((r) => `${x(r).toFixed(1)},${y(scale, r[key]).toFixed(1)}`).join(" ");
  const first = rows[0], last = rows[rows.length - 1];
  const range = (key, unit) => {
    const values = rows.map((r) => r[key]);
    return `${Math.min(...values)} to ${Math.max(...values)} ${unit}`;
  };
  const summary = `${rows.length} readings from ${sensorTime(first.iso, v.generated_at)} to ${sensorTime(last.iso, v.generated_at)} (UK time). `
    + `Temperature ranged ${range("t", "degC")}, from ${first.t} to ${last.t} degC. `
    + `Relative humidity ranged ${range("rh", "%RH")}, from ${first.rh} to ${last.rh} %RH. `
    + "The two vertical axes have different scales, so the lines show how the values move together, not how large they are. The same readings are in the Recent readings table below.";
  const id = "sensor-chart-summary";
  const grid = tScale.ticks.map((tick) => sensorSvg("line", { x1: L, x2: W - R, y1: y(tScale, tick), y2: y(tScale, tick), class: "sensor-chart-grid" }));
  const leftTicks = tScale.ticks.map((tick) => sensorSvg("text", { x: L - 6, y: y(tScale, tick) + 4, class: "sensor-chart-tick", "text-anchor": "end" }, String(tick)));
  const rightTicks = hScale.ticks.map((tick) => sensorSvg("text", { x: W - R + 6, y: y(hScale, tick) + 4, class: "sensor-chart-tick", "text-anchor": "start" }, String(tick)));
  const figure = h("figure", { class: `sensor-chart${old ? " out-of-date" : ""}`, "data-sensor-chart": "" },
    h("h3", {}, "Temperature and humidity over time"),
    old && h("p", { class: "sensor-chart-old", role: "status" }, "Out of date: these are the last readings received, not current conditions."),
    sensorSvg("svg", { viewBox: `0 0 ${W} ${H}`, class: "sensor-chart-svg", role: "img", "aria-label": "Temperature and relative humidity line chart with two vertical axes", "aria-describedby": id, focusable: "false" },
      grid, leftTicks, rightTicks,
      sensorSvg("text", { x: 4, y: 18, class: "sensor-chart-axis" }, "Temperature (degC)"),
      sensorSvg("text", { x: W - 4, y: 18, class: "sensor-chart-axis", "text-anchor": "end" }, "Relative humidity (%RH)"),
      sensorSvg("line", { x1: L, x2: L, y1: T, y2: H - B, class: "sensor-chart-axis-line" }),
      sensorSvg("line", { x1: W - R, x2: W - R, y1: T, y2: H - B, class: "sensor-chart-axis-line" }),
      sensorSvg("line", { x1: L, x2: W - R, y1: H - B, y2: H - B, class: "sensor-chart-axis-line" }),
      sensorSvg("polyline", { points: pts("t", tScale), class: "sensor-chart-line temp", fill: "none" }),
      sensorSvg("polyline", { points: pts("rh", hScale), class: "sensor-chart-line humid", fill: "none" }),
      rows.map((r) => sensorSvg("circle", { cx: x(r).toFixed(1), cy: y(tScale, r.t).toFixed(1), r: 4, class: "sensor-chart-mark temp" })),
      rows.map((r) => sensorSvg("rect", { x: (x(r) - 4).toFixed(1), y: (y(hScale, r.rh) - 4).toFixed(1), width: 8, height: 8, class: "sensor-chart-mark humid" })),
      sensorSvg("text", { x: L, y: H - 24, class: "sensor-chart-tick", "text-anchor": "start" }, sensorTime(first.iso, v.generated_at)),
      sensorSvg("text", { x: W - R, y: H - 24, class: "sensor-chart-tick", "text-anchor": "end" }, sensorTime(last.iso, v.generated_at)),
      sensorSvg("text", { x: (L + W - R) / 2, y: H - 6, class: "sensor-chart-axis", "text-anchor": "middle" }, "Time (UK time)")),
    h("ul", { class: "sensor-chart-key" },
      h("li", {}, h("span", { class: "key-line temp", "aria-hidden": "true" }), " Temperature: solid line, circles, left axis"),
      h("li", {}, h("span", { class: "key-line humid", "aria-hidden": "true" }), " Relative humidity: dashed line, squares, right axis")),
    h("p", { id, class: "muted" }, summary));
  return figure;
}

// Everything under the status for a payload that contains readings.
function sensorBody(v, model) {
  const labels = v.provenance || {};
  const table = (title, rows, absent, extra = {}) => sensorTable(title, rows, absent, labels, { generated: v.generated_at, heading: "h3", ...extra });
  const kids = [h("h3", {}, "Alerts for this home"), sensorAlertList(model, v)];
  if (!v.latest) kids.push(h("p", {}, SENSOR_COPY.offline.message));
  if (v.latest && !(v.conflicting_readings || []).length && !v.conflict_notice) kids.push(sensorLatest(v, model));
  const clashes = sensorClashes(v);
  if (clashes.length) kids.push(table("Readings that disagree", clashes, null, { name: "Readings that disagree for the same sensor and time" }));
  kids.push(sensorChart(v, model));
  const recent = (v.readings || []).slice().reverse();
  if (recent.length) kids.push(table(`Recent readings (up to ${(v.max_readings || {}).window || recent.length})`, recent, null, { name: "Recent readings, newest first" }),
    h("p", { class: "muted" }, sensorSourceNote(recent, labels)), sensorReferences(v));
  kids.push(sensorAnchor(v, table));
  return kids;
}

function sensorAbout(v) {
  const kept = ((v.grounding && v.grounding.not_retained) || []).map((name) => SENSOR_MEASURES[name]).filter(Boolean).join(" and ");
  const are = kept.includes(" and ") ? "are" : "is";
  return h("details", {}, h("summary", {}, "About these readings"), h("ul", {},
    h("li", {}, "These readings are synthetic and not calibrated. They are not a measure of comfort or hazard."),
    h("li", {}, "Live demonstration readings come from the weather outside, not from a sensor inside the home."),
    kept ? h("li", { "data-sensor-grounding": "" }, `${kept.charAt(0).toUpperCase()}${kept.slice(1)} ${are} not kept for this home and ${are} not estimated.`) : null,
    h("li", {}, `A reading counts as recent for ${SENSOR_FRESH_TEXT}. After that it is out of date, and after ${SENSOR_OFFLINE_TEXT} the sensor may be offline.`),
    h("li", {}, `The recent readings are the newest ones observed up to the time you opened this page. The comparison readings are the ones closest to the first quality evidence record, so they can be older. Readings dated after this page are left out and never treated as recent.${v.future_dated_excluded ? " Some readings dated later than this page exist and are not shown or used." : ""}`),
    h("li", {}, "These readings are the current authorised capture for this home. A suggestion in the AI tab shows the readings it cited when it ran, which may be older."),
    v.retrofit_context ? h("li", {}, v.retrofit_context.text) : null));
}

function simulationPanel() {
  const body = h("div", {}, h("p", { role: "status" }, "Loading simulation…"));
  const box = h("section", { class: "card", id: "simulation" }, h("h2", {}, "Public synthetic simulation (not this home)"), body);
  if (!SENSOR_ROLES.includes(me.user.role)) {
    body.replaceChildren(h("p", {}, "Your role does not include this simulation. Ask the quality team. Owner: your team manager. Next action: ask the quality team for the result you need."));
    return box;
  }
  const feedback = h("p", { role: "status", "aria-live": "polite" });
  const render = (s) => {
    const kids = [h("p", { class: "muted" }, s.label)];
    if (s.status === "unavailable") {
      kids.push(h("p", { role: "status" }, opsOwned(`The simulation is unavailable (${s.reason}). ${s.manual_route}`, OPS_SUPPORT, "refresh to try again, and use the manual route if it continues")));
      return body.replaceChildren(...kids);
    }
    const v = s.view || {};
    kids.push(h("p", {}, `${v.freshness_text || ""} Fixture home: ${s.home.address}, ${s.home.town}.`));
    kids.push(sensorTable("Simulated readings stored in the separate simulation store", v.readings, "No simulated readings yet.", v.provenance || {}));
    const proposal = s.proposal;
    if (proposal) {
      kids.push(h("h3", {}, "Last model proposal (unapproved)"));
      const supplied = proposal.readings || [];
      const cited = proposal.cited || [];
      const findings = (proposal.output && proposal.output.findings) || [];
      const citedText = cited.length === 0
        ? "It cited no sensor readings."
        : `It cited ${cited.length} of them: ${cited.map((r) => r[0]).join(", ")}.`;
      kids.push(h("p", {}, `Request ${proposal.digest.slice(0, 16)}. It was given ${supplied.length} stored readings. ${citedText} Status: unapproved proposal. It is not accepted and changes no case. Use the ordinary quality check.`));
      if (supplied.length) {
        kids.push(h("details", {}, h("summary", {}, `Readings supplied with the request (${supplied.length})`),
          h("ul", {}, supplied.map((r) => h("li", {}, r[0])))));
      }
      kids.push(h("p", {}, proposal.output.summary));
      kids.push(findings.length === 0
        ? h("p", { role: "status" }, "The model gave no findings.")
        : h("ul", {}, findings.map((f) => h("li", {}, `${f.text} (${f.citations.join(", ")})`))));
    }
    body.replaceChildren(...kids, controls);
  };
  const run = async (action, label) => {
    feedback.textContent = `${label}…`;
    try {
      const r = await api(`/api/assistants/simulation/quality/${action}`, {});
      feedback.textContent = r.status === "proposal" ? "Proposal stored as unapproved." : r.status === "ready" ? `Stored ${r.added || 0} new simulated readings.` : opsOwned(`Not sent (${r.reason || r.status}). ${r.manual_route || ""}`, OPS_SUPPORT, "refresh to try again, and use the manual route if it continues");
      render(await api("/api/assistants/simulation/quality"));
    } catch (error) {
      feedback.textContent = opsOwned(`${error.message || "Simulation unavailable."} Use the manual route.`, OPS_SUPPORT, "refresh to check what was stored, then try again or use the manual route", error.status);
    }
  };
  const observe = h("button", { type: "button", class: "btn" }, "Add Simulated Readings");
  const ask = h("button", { type: "button", class: "btn" }, "Request Simulation Proposal");
  observe.addEventListener("click", () => run("observe", "Adding readings"));
  ask.addEventListener("click", () => run("request", "Requesting proposal"));
  const controls = h("div", {}, observe, " ", ask, feedback);
  api("/api/assistants/simulation/quality").then(render).catch((error) => {
    body.replaceChildren(h("p", { class: "err", role: "alert" }, opsOwned(`${error.message || "Simulation unavailable."} Use the manual route.`, OPS_SUPPORT, "refresh to try again, and use the manual route if it continues", error.status)));
  });
  return box;
}

const QUALITY_TONES = { "Submitted": "wait", "Returned": "danger", "Fixed, awaiting reinspection": "wait", "Accepted": "ok", "Handed over": "ok" };
const QUALITY_CHECKS_OPEN = ["Submitted", "Returned", "Fixed, awaiting reinspection"];
const QUALITY_RETRY = "check the recorded history before repeating this change, then tell application support if it continues";

// The one-line confirmation shown at the top of the card after a decision is recorded.
function qualityRecorded(r, action, body = {}) {
  const m = r.measure;
  if (action === "quality-accept" || (action === "quality-reinspect" && body.result === "pass")) {
    return `Recorded: ${m} was accepted. Next action: record the handover once the resident has been told.`;
  }
  if (action === "quality-return" || action === "quality-reinspect") {
    const who = String(body.owner || r.defect?.owner || "the person named on the defect").trim();
    return `Recorded: ${m} was returned to ${who}. Next action: ${who} puts the defect right, then a different person checks it again.`;
  }
  if (action === "quality-fix") return `Recorded: ${m} marked as put right. Next action: a different quality inspector checks it again.`;
  if (action === "quality-handover") return `Recorded: ${m} was handed over to the resident.`;
  return `Recorded: aftercare note added to ${m}.`;
}

// A labelled text box from the shared field helper. Names of people and companies skip spell checking.
function qualityField(id, name, label, extra = {}, { maxlength = 300, person = false } = {}) {
  const control = h("input", { type: "text", maxlength, autocomplete: "off", spellcheck: person ? "false" : null });
  return Fields.fieldBlock({ id, name, label, ...extra, control });
}

// A checkbox row with the same fail and clear calls as a field block, so one check covers both.
function qualityTick(id, label) {
  const control = h("input", { type: "checkbox" });
  const row = Fields.checkRow({ id, label, control });
  const error = h("p", { class: "field-error", id: `${id}-error`, hidden: true });
  row.block.append(error);
  return {
    block: row.block, control,
    fail(text) {
      error.textContent = text;
      error.hidden = false;
      control.setAttribute("aria-describedby", error.id);
      control.focus();
    },
    clear() {
      error.hidden = true;
      error.textContent = "";
      control.removeAttribute("aria-describedby");
    },
  };
}

// Puts one sentence beside each empty required box and focuses the first. Returns true when none is empty.
function qualityComplete(required) {
  const filled = ([field]) => field.control.type === "checkbox" ? field.control.checked : field.control.value.trim() !== "";
  required.forEach(([field]) => field.clear());
  const empty = required.filter((row) => !filled(row));
  empty.forEach(([field, sentence]) => field.fail(sentence));
  if (empty.length) empty[0][0].control.focus();
  return empty.length === 0;
}

function qualityPanel(c, id, refresh, savedFields = [], session = caseSession) {
  const box = h("section", { class: "card", id: "quality" }, h("h2", {}, "Quality checks and defects"));
  const canCheck = QUALITY_ROLES.includes(me.user.role);
  const measures = (Array.isArray(c.measures) ? c.measures : String(c.measures).split(",")).map((x) => x.trim()).filter(Boolean);
  const recorded = h("p", { class: "status-line ok", id: "quality-result", hidden: !session?.qualityResult }, session?.qualityResult?.text || "");
  const records = (c.quality || []).map((r, i) => {
    const message = h("div", { id: `quality-feedback-${i}`, class: "decision-feedback", role: "status", "aria-live": "polite", tabindex: -1 });
    // A refusal shows the server's own reasons, with the owner and next action they carry, inside this record.
    const refused = (error) => {
      const reasons = Array.isArray(error.reasons) ? error.reasons.filter((x) => typeof x === "string" && x.trim()) : [];
      const lines = reasons.length ? reasons.map((x) => opsOwned(x, OPS_SUPPORT, QUALITY_RETRY, error.status))
        : [opsOwned(error.message, OPS_SUPPORT, QUALITY_RETRY, error.status)];
      message.textContent = "";
      message.append(...lines.map((line) => h("p", { class: "err" }, line)));
      message.focus();
    };
    const decide = async (button, name, body, fields) => {
      if (session) session.qualityResult = null;
      recorded.hidden = true;
      recorded.textContent = "";
      message.textContent = "";
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
      let outcome;
      try {
        outcome = await refresh(async () => {
          try {
            await post(id, name, Object.assign({ index: i }, body));
            if (session) session.qualityResult = { index: i, text: qualityRecorded(r, name, body) };
          } catch (error) {
            refused(error);
            throw error;
          }
        }, fields);
      } finally {
        button.disabled = outcome === "check-history";
        button.removeAttribute("aria-busy");
      }
      if (outcome === true) document.getElementById(`quality-record-${i}`)?.focus();
    };
    // Editing a box clears its own message and the record's last result.
    const wire = (...fields) => fields.forEach((field) => field.control.addEventListener("input", () => {
      field.clear();
      message.textContent = "";
    }));
    const submittedArea = () => {
      const acceptNote = qualityField(`quality-accept-note-${i}`, `quality-note-${i}`, "Note", { optional: true,
        hint: "Say what you checked. For example: Checked all five items on site." });
      const reason = qualityField(`quality-return-reason-${i}`, `quality-return-reason-${i}`, "Why you are returning it", { required: true,
        hint: "For example: Flow temperature record is missing." });
      const defect = qualityField(`quality-defect-${i}`, `quality-defect-${i}`, "What the defect is", { required: true,
        hint: "For example: No commissioning sheet for the second zone." });
      const owner = qualityField(`quality-owner-${i}`, `quality-owner-${i}`, "Who will put it right", { required: true,
        hint: "Name a person or a company. For example: Northern Facade Systems Ltd." }, { maxlength: 80, person: true });
      wire(acceptNote, reason, defect, owner);
      const accept = h("button", { type: "submit", "aria-label": `Accept this work: ${r.measure}` }, "Accept this work");
      const giveBack = h("button", { type: "submit", class: "alt", "aria-label": `Return with a defect: ${r.measure}` }, "Return with a defect");
      return h("div", { class: "decision-grid" },
        h("div", { class: "decision-cell" }, h("form", { novalidate: true, onsubmit: (event) => {
          event.preventDefault();
          return decide(accept, "quality-accept", { result: "pass", note: acceptNote.control.value }, [acceptNote.control]);
        } }, h("fieldset", { class: "decision-step" }, h("legend", {}, "Accept this work"), acceptNote.block,
          h("div", { class: "decision-actions" }, accept)))),
        h("div", { class: "decision-cell" }, h("form", { novalidate: true, onsubmit: (event) => {
          event.preventDefault();
          if (!qualityComplete([[reason, "Say why you are returning it."], [defect, "Say what the defect is."], [owner, "Say who will put it right."]])) return;
          return decide(giveBack, "quality-return", { reason: reason.control.value, defect: defect.control.value, owner: owner.control.value },
            [reason.control, defect.control, owner.control]);
        } }, h("fieldset", { class: "decision-step", "aria-describedby": `quality-return-intro-${i}` }, h("legend", {}, "Return with a defect"),
          h("p", { class: "field-hint", id: `quality-return-intro-${i}` }, "Use this when the work is not good enough. All three boxes are required."),
          reason.block, defect.block, owner.block, h("div", { class: "decision-actions" }, giveBack)))));
    };
    // Two buttons share one note, so Enter in the note never submits and can never accept the work.
    const fixedArea = () => {
      const note = qualityField(`quality-recheck-note-${i}`, `quality-note-${i}`, "Note", { optional: true,
        hint: "If you choose Still not right, this note is the reason it goes back. If you leave it empty we record: Reinspection failed." });
      wire(note);
      const accept = h("button", { type: "button", "aria-label": `Accept this work: ${r.measure}`,
        onclick: () => decide(accept, "quality-reinspect", { result: "pass", note: note.control.value }, [note.control]) }, "Accept this work");
      const notRight = h("button", { type: "button", class: "alt", "aria-label": `Still not right: ${r.measure}`,
        onclick: () => decide(notRight, "quality-reinspect", { result: "fail", note: note.control.value }, [note.control]) }, "Still not right");
      return h("form", { novalidate: true, onsubmit: (event) => event.preventDefault() },
        h("fieldset", { class: "decision-step" }, h("legend", {}, "Check the fix again"), note.block,
          h("div", { class: "decision-actions" }, accept, notRight),
          h("p", { class: "field-hint" }, `If it goes back, it returns to ${r.defect?.owner || "the person named on the defect"} with the same defect.`)));
    };
    const returnedArea = () => {
      const fixer = qualityField(`quality-fixer-${i}`, `quality-fixer-${i}`, "Who fixed it", { required: true,
        hint: "Name the person or company that did the repair." }, { maxlength: 80, person: true });
      const note = qualityField(`quality-fix-note-${i}`, `quality-note-${i}`, "What was corrected, with the photo, document or inspection reference", { required: true,
        hint: "For example: Duct isolator fitted, photo SYN-PH-88, inspection INS-204." });
      wire(fixer, note);
      const fix = h("button", { type: "submit", class: "alt", "aria-label": `Record that it has been put right: ${r.measure}` }, "Record that it has been put right");
      return h("div", {}, h("p", {}, "Record what was corrected and the photo, document or inspection reference. A different person must check it again."),
        h("form", { novalidate: true, onsubmit: (event) => {
          event.preventDefault();
          if (!qualityComplete([[fixer, "Say who put the defect right."], [note, "Record what was corrected and the photo, document or inspection reference."]])) return;
          return decide(fix, "quality-fix", { fixed_by: fixer.control.value, note: note.control.value }, [note.control, fixer.control]);
        } }, h("fieldset", { class: "decision-step" }, h("legend", {}, "Record that the defect has been put right"),
          fixer.block, note.block, h("div", { class: "decision-actions" }, fix))));
    };
    const acceptedArea = () => {
      const note = qualityField(`quality-handover-note-${i}`, `quality-note-${i}`, "What the resident was given or told", { required: true,
        hint: "For example: Guarantee pack and how to use the controls." });
      const told = qualityTick(`told-${i}`, "The resident has been told (required)");
      wire(note, told);
      const handover = h("button", { type: "submit", class: "alt", "aria-label": `Record handover: ${r.measure}` }, "Record handover");
      return h("form", { novalidate: true, onsubmit: (event) => {
        event.preventDefault();
        if (!qualityComplete([[note, "Say what the resident was given or told."], [told, "Tick the box once the resident has been told."]])) return;
        return decide(handover, "quality-handover", { note: note.control.value, resident_told: told.control.checked }, [note.control, told.control]);
      } }, h("fieldset", { class: "decision-step" }, h("legend", {}, "Hand over to the resident"),
        note.block, told.block, h("div", { class: "decision-actions" }, handover)));
    };
    const handedOverArea = () => {
      const note = qualityField(`quality-aftercare-note-${i}`, `quality-note-${i}`, "Aftercare note", { required: true,
        hint: "Say what the resident reported or what was done." });
      wire(note);
      const add = h("button", { type: "submit", class: "alt", "aria-label": `Add an aftercare note: ${r.measure}` }, "Add an aftercare note");
      return h("form", { novalidate: true, onsubmit: (event) => {
        event.preventDefault();
        if (!qualityComplete([[note, "Say what the resident reported or what was done."]])) return;
        return decide(add, "quality-aftercare", { note: note.control.value }, [note.control]);
      } }, h("fieldset", { class: "decision-step" }, h("legend", {}, "Add an aftercare note"), note.block, h("div", { class: "decision-actions" }, add)));
    };
    const checker = (area) => canCheck
      ? [h("p", { class: "muted" }, "You cannot accept work you submitted, recorded or fixed. Nothing is accepted automatically. Owner: the independent checker. Next action: ask a different quality inspector to check and accept it."), area()]
      : h("p", { class: "muted" }, "A Quality Inspector or a manager checks this work. Owner: a Quality Inspector or a manager. Next action: ask one of them to check this work.");
    const superseded = r.state === "Superseded";
    const tone = QUALITY_TONES[r.state];
    const checks = r.items || [];
    const aftercare = r.aftercare || [];
    return h("li", { class: `decision-item${superseded ? " superseded" : ""}` },
      h("h3", { id: `quality-record-${i}`, tabindex: -1, "aria-describedby": session?.qualityResult?.index === i ? "quality-result" : null }, r.measure),
      h("p", { class: tone ? `status-line ${tone}` : "status-line" }, QUALITY_WORDS[r.state] || r.state),
      h("dl", { class: "decision-facts" },
        h("dt", {}, "Evidence version"), h("dd", {}, String(r.evidence_version || 1)),
        h("dt", {}, "Checklist"), h("dd", {}, r.checklist_version),
        h("dt", {}, "Evidence from"), h("dd", {}, [r.source, r.submitted_by].filter(Boolean).join(", ")),
        r.accepted_by && [h("dt", {}, "Accepted by"), h("dd", {}, r.accepted_by)],
        r.handover && [h("dt", {}, "Handed over by"), h("dd", {}, r.handover.by), h("dt", {}, "Resident given or told"), h("dd", {}, Fields.heldBack(r.handover.note, r.handover.by, "what the resident was given or told"))]),
      h("details", { class: "decision-checks", open: QUALITY_CHECKS_OPEN.includes(r.state) },
        h("summary", {}, `Checks recorded (${checks.length})`),
        h("ul", {}, checks.map((x) => h("li", {}, `${x.label}: ${x.evidence}`)))),
      r.defect && !["Accepted", "Handed over", "Superseded"].includes(r.state) && h("div", { class: "decision-defect" },
        h("h4", {}, "Defect to put right"),
        h("dl", { class: "decision-facts" },
          h("dt", {}, "What is wrong"), h("dd", {}, r.defect.description),
          h("dt", {}, "Why it was returned"), h("dd", {}, r.defect.reason),
          h("dt", {}, "Who will put it right"), h("dd", {}, r.defect.owner),
          r.defect.remediation_evidence && [h("dt", {}, "Remediation evidence"), h("dd", {}, r.defect.remediation_evidence)])),
      superseded && h("p", { class: "muted" },
        Number.isInteger(r.superseded_by) ? `Historical record only. Use evidence record ${r.superseded_by + 1} for current decisions.` : "Historical record only. Use the current record for this measure.",
        r.prior_acceptance?.accepted_by ? ` Previously accepted by ${r.prior_acceptance.accepted_by}.` : "",
        r.prior_acceptance?.handover ? ` Previous handover: ${Fields.heldBack(r.prior_acceptance.handover.note, r.prior_acceptance.handover.by, "what the resident was given or told")}` : "",
        Number.isInteger(r.superseded_by) && [" ", h("a", { href: `#quality-record-${r.superseded_by}`, onclick: (event) => {
          event.preventDefault();
          document.getElementById(`quality-record-${r.superseded_by}`)?.focus();
        } }, `Go to evidence record ${r.superseded_by + 1}`)]),
      aftercare.length > 0 && [h("h4", {}, "Aftercare notes"), h("ul", {}, aftercare.map((a) => h("li", {}, `${fmtDate(a.at)} ${a.by}: ${Fields.heldBack(a.note, a.by, "what the resident reported or what was done")}`)))],
      h("div", { class: "decision-area" },
        r.state === "Submitted" && checker(submittedArea),
        r.state === "Fixed, awaiting reinspection" && checker(fixedArea),
        r.state === "Returned" && returnedArea(),
        r.state === "Accepted" && acceptedArea(),
        r.state === "Handed over" && handedOverArea()),
      message);
  });
  box.append(recorded, records.length ? h("ul", { class: "list" }, records) : h("p", {}, "No quality checks recorded yet."));
  if (!c.closed) {
    if (session.qualitySaving === "check-history") session.qualitySaving = false;
    const set = h("fieldset", { class: "decision-step evidence-step" }, h("legend", {}, "Record the evidence for a measure"),
      h("p", { class: "muted" }, "Evidence from an installer or contractor is kept as evidence only. It is checked by someone else before it counts. Replacing accepted evidence cancels its previous acceptance and handover. A new independent check and resident handover are needed."));
    const form = h("form", { novalidate: true, onsubmit: (event) => save(event) }, set);
    const measure = h("select", { id: "q-measure", "data-case-navigation": "" }, measures.map((m) => h("option", {}, m)));
    if (measures.includes(session.qualityMeasure)) measure.value = session.qualityMeasure;
    const by = h("input", { id: "q-by", type: "text", maxlength: 80, autocomplete: "off", spellcheck: "false" });
    const src = h("select", { id: "q-src" }, QUALITY_SOURCES.map((x) => h("option", {}, x)));
    const checks = h("div", {}, h("p", { role: "status" }, "Loading checklists..."));
    let lists = null;
    const paint = () => {
      if (box.isConnected) savedFields = rememberCaseFields(session);
      const m = measures.find((x) => x === measure.value) || "";
      const key = [["loft", "Loft insulation"], ["wall", "Wall insulation"], ["heat pump", "Heat pump"], ["solar", "Solar panels"]].find(([w]) => m.toLowerCase().includes(w));
      const list = lists[key ? key[1] : "General"];
      checks.replaceChildren(
        h("fieldset", { class: "evidence-checks", "aria-describedby": "q-checks-hint" },
          h("legend", {}, `Checklist ${list.version}: say what was seen for every check`),
          h("p", { class: "field-hint", id: "q-checks-hint" }, "Every check needs a note."),
          list.items.map((lab, n) => {
            const input = h("input", { id: `q-i${n}`, name: "checklist-evidence", autocomplete: "off", type: "text", maxlength: 200, "data-label": lab,
              "data-case-field-key": JSON.stringify(["checklist", m, list.version, lab]) });
            input.caseBinding = { kind: "checklist", id: `${m}, checklist ${list.version}` };
            return Fields.fieldBlock({ id: input.id, label: lab, control: input }).block;
          })),
        h("p", {}, h("a", { class: "btn alt", href: "/api/checklists.csv", download: "checklists.csv" }, "Download for Excel"), " The file is a read-only copy; changes in it are not imported back."));
      restoreBoundFields(savedFields, form, "checklist", session);
    };
    measure.addEventListener("change", () => {
      session.qualityMeasure = measure.value;
      if (lists) paint();
    });
    api("/api/checklists").then((l) => {
      lists = l;
      if (measures.length) paint();
      else checks.replaceChildren(h("p", { class: "muted" }, "This case has no measures to check yet."));
    }).catch(error => checks.replaceChildren(h("p", { class: "err", role: "alert" }, opsOwned(`Could not load checklists: ${error.message}. Refresh this case to try again.`, OPS_SUPPORT, "refresh this case to try again, then tell application support if it continues", error.status))));
    const revision = h("input", { id: "q-revision", type: "number", min: 1, inputmode: "numeric", autocomplete: "off" });
    const save = async (event) => {
      event.preventDefault();
      if (session.qualitySaving) return;
      const replaces = (c.quality || []).some((r) => r.measure === measure.value && ["Accepted", "Handed over"].includes(r.state));
      if (replaces && !window.confirm("Replace this measure's evidence? Its previous acceptance and resident handover will no longer apply. The history will be kept.")) return;
      const busy = value => {
        session.qualitySaving = value;
        if (caseSession !== session) return;
        app.querySelectorAll("[data-quality-save]").forEach(button => {
          button.disabled = Boolean(value);
          if (value === true) button.setAttribute("aria-busy", "true");
          else button.removeAttribute("aria-busy");
        });
      };
      busy(true);
      const result = await refresh(() => post(id, "quality-submit", { measure: measure.value, context_revision: Number(revision.value), submitted_by: by.value, source: src.value,
        items: Object.fromEntries([...checks.querySelectorAll("input")].map((i) => [i.dataset.label, i.value])) }), [measure, revision, by, src, ...checks.querySelectorAll("input")]);
      busy(result === "check-history" ? result : false);
    };
    set.append(
      Fields.fieldBlock({ id: "q-measure", name: "quality-measure", label: "Which measure", required: true, control: measure }).block,
      Fields.fieldBlock({ id: "q-revision", name: "quality-scope-revision", label: "Scope revision", required: true,
        hint: "Find this number in the decision for this measure on the Resident tab. Without it the work cannot be accepted.", control: revision }).block,
      Fields.fieldBlock({ id: "q-by", name: "quality-submitted-by", label: "Who did the work or sent the evidence", required: true,
        hint: "A person or a company.", control: by }).block,
      Fields.fieldBlock({ id: "q-src", name: "quality-source", label: "Where the evidence came from", required: true, control: src }).block,
      checks,
      h("div", { class: "decision-actions" }, h("button", { type: "submit", "data-quality-save": "", disabled: Boolean(session.qualitySaving) }, "Save evidence")));
    box.append(form);
  }
  return box;
}

function appointmentSlot(state) {
  const offer = state.offer || state;
  const ended = state.status === "Ended" || offer.ended;
  return h("div", {},
    h("p", {}, offer.date
      ? `${ended ? "Historical visit (ended)" : "Selected visit"}: ${fmtDate(offer.date)}. Period: ${offer.period || "Unknown"}.`
      : "Selected visit: Unknown. No verified offer."),
    h("p", {}, `Necessary instructions: ${offer.instructions || "Unknown"}`));
}

function workOrdersCard(rows, mine) {
  const orderStateCues = { Completed: "Completed on record, not accepted", Withdrawn: "Withdrawn", Issued: "Open", Appointed: "Open", Acknowledged: "Open" };
  const orderStateBadge = (state) => {
    const cue = Object.hasOwn(orderStateCues, state) ? orderStateCues[state] : "Action needed";
    const label = `${cue}: ${state || "Unknown"}`;
    return h("span", { class: state === "Withdrawn" || cue === "Action needed" ? "flag danger" : "flag", "data-state-cue": cue }, label);
  };
  const noticeBadge = (needsNotice) => needsNotice
    ? h("span", { class: "flag danger", "data-state-cue": "Visit notice required" }, "Visit notice required: Needs notice")
    : h("span", { class: "flag", "data-state-cue": "Standard visit" }, "Standard visit: No extra notice needed");
  const sectionAttrs = mine ? { class: "card", id: "contractor-work-orders", "aria-labelledby": "contractor-work-orders-heading" } : { class: "card" };
  const headingAttrs = mine ? { id: "contractor-work-orders-heading", tabindex: "-1" } : {};
  return h("section", sectionAttrs, h("h2", headingAttrs, mine ? "Your work orders" : "Work orders"),
    rows.length ? h("ul", { class: "list" }, rows.map((w) => h("li", {},
      h("strong", {}, `${w.id}, version ${w.version}`), " ", orderStateBadge(w.state), `. ${w.address}, ${w.postcode}. Works: ${w.measures}. `,
      noticeBadge(w.needs_notice), `. Named contact: ${w.named_contact}.`,
      h("p", {}, `Appointment: ${w.appointment_control.status}.${w.appointment_control.missing.length ? ` ${w.appointment_control.missing.join("; ")}.` : ""}`),
      appointmentSlot(w.appointment_control),
      h("div", { class: "muted" }, w.scope), w.appointments.length > 0 && h("div", { class: "muted" }, "Visits: " + w.appointments.map((a) => `${a.outcome}${a.date ? ` ${a.date}` : ""}`).join("; "))))) : h("p", {}, "No work orders yet."));
}

async function contractorOrders() {
  return workOrdersCard(await api("/api/workorders"), true);
}

function appointmentDrafts() {
  return [...document.querySelectorAll('form[data-appointment-form][data-unsaved="true"]')].map((form) => ({
    key: form.dataset.appointmentForm,
    context: form.appointmentContext,
    open: form.parentElement.open,
    values: [...form.elements].filter((el) => el.name).map((el) => ({ name: el.name, value: el.value, checked: el.checked }))
  }));
}

const CAPACITY_PAGE = { packages: { size: 5, offset: 0 }, orders: { size: 20, offset: 0 } };
const RENDERED_OFFSETS = { packages: 0, orders: 0 };
let capacityPagerFocus = null;

function capacityDirty() {
  return appointmentDrafts().length > 0
    || [...document.querySelectorAll("[data-capacity-draft]")].some((el) => el.value && el.value.trim());
}
let capacityLoadSeq = 0;

function pagedPath(base, page) {
  return `${base}${base.includes("?") ? "&" : "?"}limit=${page.size}&offset=${page.offset}`;
}

function pagerControls(kind, label, page, total, count, go, busy) {
  const live = CAPACITY_PAGE[kind];
  const first = total ? page.offset + 1 : 0, last = page.offset + count;
  const pages = Math.max(1, Math.ceil(total / page.size));
  const status = h("p", { class: "muted", id: `capacity-pager-${kind}`, role: "status", "aria-live": "polite", tabindex: -1 },
    total ? `Showing ${label} ${first} to ${last} of ${total}. Page ${Math.floor(page.offset / page.size) + 1} of ${pages}.` : `No ${label}.`);
  if (capacityPagerFocus === kind) { capacityPagerFocus = null; queueMicrotask(() => status.focus()); }
  const step = (delta) => {
    if (busy()) return;
    if (capacityDirty() && !window.confirm("Changing the page discards unsaved entries in this workspace. Continue?")) return;
    live.offset = Math.max(0, page.offset + delta * page.size); capacityPagerFocus = kind; return go();
  };
  const prev = h("button", { type: "button", class: "alt", onclick: () => step(-1) }, `Previous ${label}`);
  const next = h("button", { type: "button", class: "alt", onclick: () => step(1) }, `Next ${label}`);
  prev.disabled = page.offset <= 0;
  next.disabled = last >= total;
  return h("nav", { "aria-label": `${label} pages` }, status, h("p", {}, prev, " ", next));
}

async function capacityView() {
  if (!isManager()) return show(h("p", {}, "Only a manager sees capacity and work orders."));
  const signal = routeController.signal;
  const recoveryGeneration = capacityHistoryGeneration;
  const msg = h("div", { role: "status", "aria-live": "polite", tabindex: -1 });
  let saving = false, checkHistory = false;
  const go = async (fn, savedForm) => {
    if (fn && (saving || checkHistory || capacityHistoryBarrier)) return;
    const button = document.activeElement;
    if (button instanceof HTMLButtonElement) { button.disabled = true; button.setAttribute("aria-busy", "true"); }
    let recorded = false;
    saving = true;
    try {
      if (fn) { await fn(); recorded = true; }
      if (savedForm) delete savedForm.dataset.unsaved;
      signal.throwIfAborted();
      await capacityView();
    }
    catch (e) {
      if (signal.aborted || !me) return;
      if (e.capacityLoadFailure) { CAPACITY_PAGE.packages.offset = RENDERED_OFFSETS.packages; CAPACITY_PAGE.orders.offset = RENDERED_OFFSETS.orders; }
      checkHistory ||= recorded || Boolean(fn && mutationNeedsHistory(e));
      if (checkHistory) capacityHistoryBarrier = capacityHistoryGeneration = {};
      msg.replaceChildren(h("p", { class: "err" }, checkHistory
        ? opsOwned(`Reload and check work order or package history before another action. ${e.message}`, OPS_SUPPORT, "reload and check the work order or package history before another action")
        : opsOwned(e.message, OPS_SUPPORT, "correct the entries or refresh, then try again", e.status)));
      if (e.capacityLoadFailure || checkHistory) msg.append(h("button", { type: "button", onclick: () => go() }, "Try again"));
      msg.focus();
    }
    finally { saving = false; if (button instanceof HTMLButtonElement) { button.disabled = Boolean(fn && checkHistory); button.removeAttribute("aria-busy"); } }
  };
  const load = async (path, label) => {
    try { return await api(path, undefined, signal); }
    catch (error) {
      if (signal.aborted || !me) throw error;
      const detail = error instanceof TypeError || error.generic ? "" : ` ${error.message}`;
      error.message = opsOwned(`We could not load ${label}. Try again. If this continues, contact application support.${detail}`, OPS_SUPPORT, "refresh to try again, then contact application support if it continues", error.status);
      error.capacityLoadFailure = true;
      throw error;
    }
  };
  const loadSeq = ++capacityLoadSeq;
  const shown = { packages: { ...CAPACITY_PAGE.packages }, orders: { ...CAPACITY_PAGE.orders } };
  const [pkgPage, orderPage] = await Promise.all([
    load(pagedPath("/api/packages", shown.packages), "packages"),
    load(pagedPath("/api/workorders", shown.orders), "work orders")]);
  if (loadSeq !== capacityLoadSeq) return;
  for (const [kind, result] of [["packages", pkgPage], ["orders", orderPage]]) {
    signal.throwIfAborted();
    if (!me || capacityHistoryGeneration !== recoveryGeneration) return;
    const page = shown[kind];
    if (!result.items.length && result.total && page.offset >= result.total) {
      CAPACITY_PAGE[kind].offset = Math.max(0, Math.floor((result.total - 1) / page.size) * page.size);
      return await capacityView();
    }
  }
  const pkgs = pkgPage.items, orders = orderPage.items;
  signal.throwIfAborted();
  if (!me) return;
  if (capacityHistoryGeneration !== recoveryGeneration) return;
  capacityHistoryBarrier = null;
  let field = 0;
  const inp = (label, attrs) => {
    const id = `capacity-field-${++field}`;
    return [h("label", { for: id }, label), h("input", Object.assign({ id, name: label.toLowerCase().replace(/[^a-z0-9]+/g, "-"), autocomplete: "off", type: "text", "data-capacity-draft": "true" }, attrs))];
  };
  const name = inp("Package name", { maxlength: 80 }), from = inp("Starts", { type: "date" }), to = inp("Ends", { type: "date" });
  const scope = inp("What it covers", { maxlength: 400 }), ref = inp("Contract or call-off reference", { maxlength: 60 });
  const contractVersion = inp("Contract or call-off version", { maxlength: 80, spellcheck: false, required: true });
  const versionError = h("p", { id: "capacity-version-error", class: "err", role: "status", "aria-live": "polite" });
  contractVersion[1].setAttribute("aria-describedby", "capacity-version-error");
  contractVersion[1].addEventListener("input", () => {
    contractVersion[1].removeAttribute("aria-invalid");
    versionError.textContent = "";
  });
  const createPackage = () => {
    if (!contractVersion[1].value.trim()) {
      contractVersion[1].setAttribute("aria-invalid", "true");
      versionError.textContent = "Enter the contract or call-off version before creating the package. Owner: the person creating the package. Next action: type the version, then create the package again.";
      contractVersion[1].focus();
      return;
    }
    return go(() => api("/api/packages", { name: name[1].value, period_from: from[1].value, period_to: to[1].value, scope: scope[1].value, contract_ref: ref[1].value, contract_version: contractVersion[1].value }));
  };
  const create = h("section", { class: "card" }, h("h2", {}, "New package"), ...[name, from, to, scope, ref].map((pair) => h("div", { class: "field" }, ...pair)),
    h("div", { class: "field" }, ...contractVersion, versionError),
    h("p", {}, "A package is a draft, not an instruction. Creating it grants no contract authority."),
    h("p", {}, h("button", { onclick: createPackage }, "Create package")));
  const cards = pkgs.map((p) => {
    const con = inp("Contractor", { maxlength: 80 }), off = inp("Offered (home orders)", { type: "number", min: 0, max: 100000, step: 1, inputmode: "numeric" }), com = inp("Committed with evidence (home orders)", { type: "number", min: 0, max: 100000, step: 1, inputmode: "numeric" });
    const evi = inp("Evidence for the commitment", { maxlength: 300 });
    const sourceCase = inp("Case holding the commitment document", { maxlength: 64, spellcheck: false });
    const document = inp("Commitment document ID", { maxlength: 64, spellcheck: false });
    const sourceVersion = inp("Commitment document version", { maxlength: 80, spellcheck: false });
    const sourceDate = inp("Commitment source date", { type: "date" }), reviewed = inp("Manager reviewed on", { type: "date" });
    const validFrom = inp("Capacity delivery starts", { type: "date" }), validTo = inp("Capacity delivery ends", { type: "date" });
    const covered = inp("Covered case references, separated by semicolons", { maxlength: 2000, spellcheck: false });
    const cid = inp("Case reference to issue a work order for", {}), wsc = inp("Work order wording (leave blank to use the package scope)", { maxlength: 400 });
    const bindings = inp("Affected measures and scope revisions: Measure|revision; Measure|revision", { maxlength: 1000 });
    return h("section", { class: "card" }, h("h2", {}, `${p.name} (${p.id})`),
      h("p", {}, `${fmtDate(p.period_from)} to ${fmtDate(p.period_to)}. Reference ${p.contract_ref}, version ${p.contract_version || "Unknown"}. Scope version ${p.scope_version}: ${p.scope}`),
      h("div", { class: "table-scroll", role: "region", "aria-label": `Capacity for ${p.id}`, tabindex: 0 },
        h("table", {}, h("caption", { class: "muted" }, "One unit is one home work order for this package period, not a crew or weekly slot. Only evidenced commitment can confirm work."),
          h("thead", {}, h("tr", {}, ["Contractor", "Offered", "Committed", "In use", "Room left", "Evidence"].map((x) => h("th", { scope: "col" }, x)))),
          h("tbody", {}, p.capacity.map((k) => h("tr", {}, h("th", { scope: "row" }, k.contractor), h("td", {}, k.offered), h("td", {}, k.committed), h("td", {}, k.in_use), h("td", {}, k.headroom),
            h("td", {}, `${k.evidence || "None"}. ${k.evidence_status}.`, k.details && h("div", {}, `Source ${k.details.document_id}, version ${k.details.source_version}. Reviewed ${fmtDate(k.details.reviewed_on)}. Capacity version ${k.version}.`))))))),
      h("h3", {}, "Record capacity"), ...[con, off, com, evi, sourceCase, document, sourceVersion, sourceDate, reviewed, validFrom, validTo, covered].flat(),
      h("p", { class: "muted" }, "Only a named manager with recorded contract authority can accept this commitment. Check the original document, current scope and covered homes. A review is current for 7 days. Record 0 if capacity is lost; existing orders will show a deficit."),
      h("p", {}, h("button", { class: "alt", onclick: () => go(() => api(`/api/packages/${p.id}/capacity`, {
        contractor: con[1].value, offered: off[1].value, committed: com[1].value, evidence: evi[1].value,
        details: { source_case_id: sourceCase[1].value, document_id: document[1].value, source_version: sourceVersion[1].value,
          source_date: sourceDate[1].value, reviewed_on: reviewed[1].value, valid_from: validFrom[1].value, valid_to: validTo[1].value,
          unit: "home-work-order", status: "Committed", case_ids: covered[1].value.split(";").map((x) => x.trim()).filter(Boolean) }
      })) }, "Save capacity")),
      h("h3", {}, "Issue a work order"), ...[cid, wsc, bindings].flat(),
      h("p", {}, h("button", { onclick: () => go(() => api("/api/workorders", { package: p.id, case_id: cid[1].value, scope: wsc[1].value, resident_bindings: residentBindings(bindings[1].value) })) }, "Issue work order")));
  });
  const actions = orders.map((w) => {
    const note = h("input", { type: "text", name: `order-note-${w.id}`, autocomplete: "off", maxlength: 300, "data-capacity-draft": "true" });
    const out = h("select", { name: `legacy-outcome-${w.id}` }, WO_OUTCOMES.map((x) => h("option", {}, x)));
    const call = (a, body, savedForm) => go(() => api(`/api/workorders/${w.id}/${a}`, body), savedForm);
    const open = w.state === "Issued" || w.state === "Appointed";
    const bindings = h("input", { type: "text", name: `order-bindings-${w.id}`, autocomplete: "off", spellcheck: "false", maxlength: 1000 });
    const noteField = Fields.fieldBlock({ id: `order-note-${w.id}`, label: `Note, date or reason for ${w.id}`, control: note,
      hint: "The buttons use it like this: Record appointment takes the date when the outcome is Booked; Record completion takes a note; New version takes the new scope; Withdraw takes the reason." });
    const outField = Fields.fieldBlock({ id: `order-outcome-${w.id}`, label: `Appointment outcome for ${w.id}`, control: out });
    const bindingsField = Fields.fieldBlock({ id: `order-bindings-${w.id}`, label: `Affected measures and scope revisions for ${w.id}`, control: bindings,
      hint: "Only for New version. Write Measure|revision pairs separated by semicolons, for example Loft insulation|2; Cavity wall insulation|1." });
    return h("li", {}, h("strong", {}, `${w.id}, version ${w.version}`), ` ${w.state}. ${w.contractor}. ${w.address}. Issued by ${w.issued_by}.`,
      h("div", { class: "muted" }, w.scope),
      appointmentControls(w, (body, form) => call("appointment-control", body, form)),
      w.state !== "Withdrawn" && h("div", { class: "work-order-actions" },
        h("div", { class: "field-row" }, noteField.block, bindingsField.block, open && outField.block),
        h("div", { class: "row" },
          open && [h("button", { onclick: () => call("appointment", { outcome: out.value, date: note.value }) }, "Record appointment (date for Booked)"),
            h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/reissue`, { scope: note.value, reason: "Changed", resident_bindings: residentBindings(bindings.value) })) }, "New version"),
            h("button", { class: "alt", onclick: () => call("complete", { note: note.value }) }, "Record completion"),
            h("button", { class: "alt", onclick: () => call("withdraw", { reason: note.value }) }, "Withdraw (add the reason)")],
          w.state === "Completed" && h("button", { class: "alt", onclick: () => go(() => api(`/api/workorders/${w.id}/correct`, { reason: note.value, resident_bindings: residentBindings(bindings.value) })) }, "Record a correction (add the reason)"))));
  });
  const drafts = appointmentDrafts();
  const exportLink = (path, file, label, what) => h("p", {}, h("a", { class: "btn alt", href: path, download: file }, label),
    ` The file has every ${what} you can see, not only the ones on this page. It is a read-only copy; changes in it are not imported back.`);
  show(h("h1", {}, "Capacity and work orders"),
    h("p", { class: "muted" }, "Work orders are controlled: every change is a new version with who issued it, and nothing is issued beyond a contractor's evidenced commitment."),
    msg, create, h("h2", {}, "Packages"),
    pkgPage.total ? exportLink("/api/packages.csv", "packages.csv", "Download all packages for Excel", "package") : null,
    pagerControls("packages", "packages", shown.packages, pkgPage.total, pkgs.length, () => go(), () => saving || Boolean(capacityHistoryBarrier)),
    ...(cards.length ? cards : [h("p", {}, "No packages yet.")]),
    h("section", { class: "card" }, h("h2", {}, "Work orders"),
      orderPage.total ? exportLink("/api/workorders.csv", "workorders.csv", "Download all work orders for Excel", "work order") : null,
      pagerControls("orders", "work orders", shown.orders, orderPage.total, orders.length, () => go(), () => saving || Boolean(capacityHistoryBarrier)),
      orders.length ? h("ul", { class: "list" }, actions) : h("p", {}, "No work orders yet.")));
  RENDERED_OFFSETS.packages = shown.packages.offset; RENDERED_OFFSETS.orders = shown.orders.offset;
  for (const draft of drafts) {
    const form = [...document.querySelectorAll("form[data-appointment-form]")].find((el) => el.dataset.appointmentForm === draft.key);
    if (!form) continue;
    for (const saved of draft.values) {
      const control = form.elements.namedItem(saved.name);
      if (control) { control.value = saved.value; if (control.type === "checkbox") control.checked = saved.checked; }
    }
    form.appointmentContext = draft.context;
    form.dataset.unsaved = "true";
    form.parentElement.open = draft.open;
  }
}

function appointmentControls(w, submit) {
  const state = w.appointment_control;
  if (!state.current_binding) return h("section", { "aria-label": `Appointment controls for ${w.id}` },
    h("h3", {}, `Appointment: ${state.status}`), appointmentSlot(state),
    h("p", {}, "Appointment evidence is held for roles with a recorded need. Ask the resident-service owner to review the next step."));
  const offer = state.offer;
  let field = 0;
  const input = (label, type = "text", value = "", required = true) => {
    const id = `${w.id}-appointment-${++field}`;
    const error = h("span", { id: `${id}-error`, role: "status", "aria-live": "polite", class: "err" });
    const control = h("input", { id, name: id, autocomplete: "off", type, maxlength: 500, value,
      required: required && type !== "checkbox", "aria-describedby": `${id}-error`,
      oninvalid: () => { error.textContent = opsOwned(control.validationMessage, "the person filling in this form", "correct this entry, then submit again"); control.setAttribute("aria-invalid", "true"); },
      oninput: () => { error.textContent = ""; control.removeAttribute("aria-invalid"); }
    });
    return [h("label", { for: id }, `${label} (${w.id})`), control, error];
  };
  const check = (label) => {
    const pair = input(label, "checkbox");
    pair[1].removeAttribute("aria-describedby");
    return [h("label", {}, pair[1], ` ${label} (${w.id})`), pair[1]];
  };
  const select = (label, choices) => {
    const id = `${w.id}-appointment-${++field}`;
    const control = h("select", { id, name: id }, choices.map((x) => h("option", {}, x)));
    return [h("label", { for: id }, `${label} (${w.id})`), control];
  };
  const section = (title, fields, action, body) => {
    const event = input(`${title} event reference`, "text", crypto.randomUUID());
    const form = h("form", {
      "data-appointment-form": `${w.id}-${action}`,
      oninput: () => { form.dataset.unsaved = "true"; },
      onchange: () => { form.dataset.unsaved = "true"; },
      onreset: (e) => {
        if (form.dataset.unsaved === "true" && !window.confirm("Discard only this unsaved draft?")) { e.preventDefault(); return; }
        delete form.dataset.unsaved; form.appointmentContext = { ...initialContext };
      },
      onsubmit: (e) => {
      e.preventDefault();
      if (action === "close_case" && !window.confirm(`Record the supplied human closure of underlying home case ${state.case_id}? This resets its active no-access count, not its history. Outstanding resident updates and remedies remain. This is not investigation task disposition or technical, legal or financial approval.`)) return;
      return submit(Object.assign({ action, event_ref: event[1].value }, body(), form.appointmentContext), form);
    } }, ...event, ...fields, h("button", { type: "submit", class: "alt" }, title),
    h("button", { type: "reset", class: "alt" }, "Discard this draft"));
    const initialContext = action === "offer" ? { expected_offer_id: offer ? offer.id : null }
      : ["confirm", "authority", "outcome"].includes(action) ? { offer_id: offer && offer.id }
      : action === "close_case" ? { case_id: state.case_id, expected_case_version: state.case_version } : {};
    form.appointmentContext = { ...initialContext };
    return h("details", {}, h("summary", {}, `${title} for ${w.id}`), form);
  };
  const date = input("Offer date", "date"), period = input("Visit period");
  const options = input("Options offered, separated by semicolons");
  const constraints = input("Household constraints or Unknown");
  const instructions = input("Necessary provider instructions only, no diagnoses");
  const paused = check("Household paused"), deferred = check("Household deferred");
  const bundle = check("Bundle requested"), agreed = check("Resident agreed to bundle");
  const competence = input("Scoped competence source for bundle", "text", "", false);
  const proposal = section("Record appointment offer",
    [...date, ...period, ...options, ...constraints, ...instructions, paused[0], deferred[0],
      bundle[0], agreed[0], ...competence], "offer", () => ({
      date: date[1].value, period: period[1].value,
      expected_offer_id: offer ? offer.id : null,
      options: options[1].value.split(";").map((s) => s.trim()).filter(Boolean),
      constraints: constraints[1].value, instructions: instructions[1].value,
      paused: paused[1].checked, deferred: deferred[1].checked,
      bundle: bundle[1].checked, bundle_agreed: agreed[1].checked,
      competence: { source: competence[1].value, scope: state.current_binding }
    }));
  const kind = select("Confirmation kind", ["resident", "staff", "capacity"]);
  const person = input("Confirming person"), source = input("Confirmation source");
  const channel = input("Confirmation channel, including phone or in person");
  const representative = input("Appointment representative reference, if applicable", "text", "", false);
  const confirmation = section("Record separate confirmation",
    [...kind, ...person, ...source, ...channel, ...representative], "confirm", () => ({
      offer_id: offer && offer.id, kind: kind[1].value, person: person[1].value,
      source: source[1].value, channel: channel[1].value,
      representative_ref: representative[1].value || null
    }));
  const rep = input("Appointment authority reference"), repPerson = input("Authorized representative");
  const repSource = input("Appointment-specific authority source");
  const start = input("Authority starts", "date"), end = input("Authority ends", "date");
  const revoked = check("Appointment authority revoked");
  const authority = section("Record appointment authority",
    [...rep, ...repPerson, ...repSource, ...start, ...end, revoked[0]], "authority", () => ({
      representative_ref: rep[1].value, person: repPerson[1].value, source: repSource[1].value,
      offer_id: offer && offer.id,
      valid_from: start[1].value, valid_to: end[1].value, revoked: revoked[1].checked
    }));
  const cause = select("Visit cause", ["Unknown", "Resident", "Provider", "Cancelled", "Rescheduled"]);
  const owner = input("Cause owner or Unknown"), verification = input("Verification source or Unknown");
  const verified = check("Evidence verified"), noAccess = check("Resident no-access fact");
  const breach = check("Preference breach fact"), abortive = check("Abortive visit fact");
  const outcome = section("Record evidenced visit outcome",
    [...cause, ...owner, ...verification, verified[0], noAccess[0], breach[0], abortive[0]], "outcome", () => ({
      offer_id: offer && offer.id, cause: cause[1].value, owner: owner[1].value,
      source: verification[1].value, verified: verified[1].checked, no_access: noAccess[1].checked,
      preference_breach: breach[1].checked, abortive: abortive[1].checked
    }));
  const threshold = input("Provisional no-access threshold", "number", "5");
  threshold[1].min = "0"; threshold[1].step = "1";
  const basis = input("Threshold configuration evidence");
  const configure = section("Record provisional threshold", [...threshold, ...basis], "configure", () => ({
    threshold: Number(threshold[1].value), basis: basis[1].value
  }));
  const checks = Object.fromEntries(["confirmation", "notice", "attendance", "adjustments", "contact", "circumstances"]
    .map((key) => [key, input(`Human ${key} check evidence or Unknown`)]));
  const corrective = input("Corrective action"), update = input("Next resident update");
  const disposition = input("Investigation task disposition, not case closure");
  const investigation = state.investigation && section("Record human investigation",
    [...Object.values(checks).flat(), ...corrective, ...update, ...disposition], "investigation", () => ({
      checks: Object.fromEntries(Object.entries(checks).map(([key, pair]) => [key, pair[1].value])),
      corrective_action: corrective[1].value, next_update: update[1].value, disposition: disposition[1].value
    }));
  const closureSource = input("Human home-case closure decision source");
  const closureVersion = input("Human closure source version");
  const closureReason = input("Human underlying home-case closure reason");
  const closureConfirmed = check("I am recording the supplied human underlying home-case closure, not investigation task disposition");
  closureConfirmed[1].required = true;
  const closure = state.case_closed === false && section("Record human underlying home-case closure",
    [h("p", {}, `Underlying home case ${state.case_id}. Record only a supplied human decision. This does not approve handover, legal or financial closure or clear resident updates or remedies.`),
      ...closureSource, ...closureVersion, ...closureReason, closureConfirmed[0]], "close_case", () => ({
      case_id: state.case_id, expected_case_version: state.case_version,
      source: closureSource[1].value, source_version: closureVersion[1].value,
      reason: closureReason[1].value, confirmed: closureConfirmed[1].checked
    }));
  const tally = (counts) => {
    const rows = Object.entries(counts || {});
    return rows.length ? `${rows.map(([cause, n]) => `${cause}: ${n}`).join("; ")}.` : "None recorded.";
  };
  return h("section", { "aria-label": `Appointment controls for ${w.id}` },
    h("h3", {}, `Appointment: ${state.status}`),
    appointmentSlot(state),
    h("p", {}, state.missing.length ? state.missing.join("; ") : "Resident, staff and current contractor capacity confirmations recorded."),
    h("p", {}, "An offer is not an agreement. Works consent remains separate. Nothing is sent. Urgent safety response does not wait for a bundle or investigation."),
    h("a", { href: `#/case/${encodeURIComponent(w.case_id)}` }, "Record or review the named resident-update commitment and safe contact"),
    offer && h("p", {}, `Options: ${offer.options.join("; ")}. Constraints: ${offer.constraints}. Paused: ${offer.paused ? "Yes" : "No"}. Deferred: ${offer.deferred ? "Yes" : "No"}. Update owner: ${state.current_update_owner ? state.current_update_owner.name : "Unknown"}.`),
    h("p", {}, `Eligible resident no-access: ${state.eligible_no_access}. Reporting threshold: ${state.reporting_threshold}. ${String(state.case_reset).replace(/\.$/, "")}.`),
    h("p", {}, `Underlying home case ${state.case_id}: ${state.case_closed === true ? "Closed" : state.case_closed === false ? "Active" : "Unknown"}. Recorded human closures: ${state.closure_history.length}. History is retained.`),
    h("p", {}, `Preference breaches by cause / owner: ${tally(state.counts.preference_breach)} Abortive visits by cause / owner: ${tally(state.counts.abortive)}`),
    proposal, confirmation, authority, outcome, configure, investigation, closure);
}
