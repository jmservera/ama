"use strict";

const ProgressViews = (() => {
  const number = value => new Intl.NumberFormat(navigator.language || "en-GB", { maximumFractionDigits: 1 }).format(value);
  const dateLabel = value => value ? new Intl.DateTimeFormat(navigator.language || "en-GB", {
    day: "numeric", month: "short", year: "numeric", timeZone: "UTC",
  }).format(new Date(`${value}T00:00:00Z`)) : "Unknown";
  const query = () => new URLSearchParams(location.hash.split("?")[1] || "");
  const href = (path, values) => `${path}${values.size ? `?${values}` : ""}`;
  const navigate = (path, values) => {
    const target = href(path, values);
    if (location.hash === target) route();
    else location.hash = target;
  };
  function field(name, label, value, type = "text") {
    const input = h("input", { id: `progress-${name}`, name, type, value,
      autocomplete: "off", ...(name === "q" ? { maxlength: 200 } : {}) });
    return h("div", {}, h("label", { for: input.id }, label), input);
  }
  function select(name, label, value, options) {
    const choices = [...new Set([value, ...options].filter(Boolean))];
    const control = h("select", { id: `progress-${name}`, name, autocomplete: "off" },
      h("option", { value: "" }, "All"),
      choices.map(item => h("option", { value: item, selected: value === item }, item)));
    return h("div", {}, h("label", { for: control.id }, label), control);
  }
  function filters(path, values, fields) {
    return h("form", { class: "progress-filters card", onsubmit: event => {
      event.preventDefault();
      const next = new URLSearchParams();
      for (const [key, value] of new FormData(event.currentTarget)) {
        if (String(value)) next.set(key, String(value));
      }
      if (values.has("limit")) next.set("limit", values.get("limit"));
      navigate(path, next);
    } }, fields, h("button", { type: "submit" }, "Apply filters"),
    h("a", { href: path }, "Reset filters"));
  }
  function table(title, columns, rows) {
    return h("div", { class: "table-scroll", role: "region", tabindex: 0, "aria-label": `${title} table` },
      h("table", {}, h("caption", {}, title),
        h("thead", {}, h("tr", {}, columns.map(label => h("th", { scope: "col" }, label)))),
        h("tbody", {}, rows.length ? rows.map(row => h("tr", {},
          row.map((cell, index) => h(index ? "td" : "th", index ? {} : { scope: "row" }, cell))))
          : h("tr", {}, h("td", { colspan: columns.length }, "No recorded data for this view.")))));
  }
  function chart(title, columns, rows) {
    const max = Math.max(1, ...rows.flatMap(row => row.slice(1)));
    return h("section", { class: "card progress-chart" }, h("h2", {}, title),
      h("div", { class: "progress-bars", "aria-hidden": "true" }, rows.length ? rows.map(row =>
        h("div", { class: "progress-bar-row" }, h("span", { class: "progress-bar-label" }, row[0]),
          h("div", {}, row.slice(1).map((count, index) => {
            const bar = h("meter", { min: 0, max, value: count, tabindex: -1 });
            return h("div", { class: "progress-bar-value" },
              h("span", {}, `${columns[index + 1]}: ${number(count)}`), bar);
          })))) : h("p", {}, "No recorded data for this view.")),
      h("details", {}, h("summary", {}, `Show ${title.toLowerCase()} as a table`),
        table(title, columns, rows.map(row => [row[0], ...row.slice(1).map(number)]))));
  }
  function pending(title) {
    show(h("div", { class: "progress-page" }, h("h1", {}, title),
      h("p", { role: "status" }, "Loading demonstration data\u2026")));
  }
  async function load(path, values, title, controls) {
    const signal = routeController.signal;
    pending(title);
    try {
      return await api(`${path}?${values}`, undefined, signal);
    } catch (error) {
      if (signal.aborted || !me) return null;
      const invalidFields = error.status === 400 && Array.isArray(error.reasons?.fields)
        ? ["start", "end"].filter(name => error.reasons.fields.includes(name))
          .map(name => controls.querySelector(`[name=${name}]`)).filter(Boolean)
        : [];
      for (const input of invalidFields) {
        const message = h("p", { id: `${input.id}-error`, class: "field-error", role: "status" }, error.message);
        input.setAttribute("aria-invalid", "true");
        input.setAttribute("aria-describedby", message.id);
        input.after(message);
      }
      show(h("div", { class: "progress-page" }, h("h1", {}, title),
        h("p", { class: "flag" }, "Demonstration data"),
        controls, !invalidFields.length && [
          h("p", { class: "err", role: "alert" }, error.message),
          h("p", {}, "Change the filters or try again. A failed read is not an empty result."),
          h("button", { type: "button", onclick: route }, "Try again")]));
      invalidFields[0]?.focus();
      return null;
    }
  }
  async function dashboard() {
    const values = query();
    const controls = filters("#/progress", values, [
      field("start", "Start date (UTC)", values.get("start") || "", "date"),
      field("end", "End date (UTC)", values.get("end") || "", "date"),
    ]);
    const data = await load("/api/progress", values, "Progress dashboard", controls);
    if (!data) return;
    controls.querySelector("[name=start]").value = data.start;
    controls.querySelector("[name=end]").value = data.end;
    const periodRows = rows => rows.map(row =>
      [dateLabel(row.date), row.opened, row.closed, row.reopened]);
    const stats = data.time_to_close;
    const duration = value => value == null ? "Unknown" : `${number(value)} days`;
    const facts = [
      ["Median time to close", duration(stats.median_days)],
      ["90th percentile time to close", duration(stats.p90_days)],
      ["Cases open now", number(data.current.open)],
      ["Stalled cases now (60+ days in stage)", number(data.current.stalled)],
      ["Cases with recorded overdue tasks now", number(data.current.overdue)],
    ];
    const cohort = h("section", { class: "card" }, h("h2", {}, "What these figures mean"),
      h("p", {}, `${number(data.coverage.synthetic_cases)} explicitly synthetic cases. ` +
        `${number(data.coverage.excluded_unmarked)} unmarked cases excluded. ` +
        `${number(data.coverage.known_lifecycle)} cases have usable lifecycle dates; ` +
        `${number(data.coverage.unknown_lifecycle)} have unknown or contradictory dates and are excluded from trends and time to close.`),
      h("p", {}, "Opened includes first openings and reopened episodes. Reopened is also shown separately. " +
        "Backlog is the number of cases with usable lifecycle dates still open at the end of each UTC day. " +
        "Weeks start on Monday; first and last weeks include only selected dates."),
      h("p", {}, `Time to close uses ${number(stats.samples)} closure episodes in the selected dates, ` +
        "in calendar days from that episode's opening. The 90th percentile uses the nearest ranked sample. " +
        "Unknown does not mean zero."),
      h("p", {}, `Journey, workload, stalled and overdue counts use the current recorded view (dataset date ${dateLabel(data.as_of)}), ` +
        "not historical ownership or workflow reconstruction. Teams are recorded owner roles. " +
        "Stalled is a review signal, not a legal deadline. Overdue uses recorded task clocks, not a compliance decision."),
      h("p", {}, data.ai.basis, " Accepted, Changed and Rejected describe draft review, not approval, consent or a safety decision. " +
        "Unmarked activity never counts. " +
        `${number(data.ai.eligible_records)} eligible briefing records; ` +
        `${number(data.ai.unknown_review_date)} with unknown review date; ` +
        `${number(data.ai.unreviewed_or_unavailable)} unreviewed or unavailable; ` +
        `${number(data.ai.rules_or_templates)} rules/template records excluded from AI outcomes.`));
    show(h("div", { class: "progress-page" }, h("h1", {}, "Progress dashboard"),
      h("p", { class: "flag" }, "Demonstration data - fictional cases, not company performance."),
      controls, h("p", { role: "status" }, `Showing ${dateLabel(data.start)} to ${dateLabel(data.end)}.`),
      h("section", { class: "card" }, h("h2", {}, "Progress summary"),
        h("dl", { class: "progress-facts" }, facts.map(([label, value]) =>
          h("div", {}, h("dt", {}, label), h("dd", {}, value))))),
      cohort,
      chart("Cases opened and closed per day", ["Day", "Opened", "Closed", "Reopened"], periodRows(data.daily)),
      chart("Cases opened and closed per week", ["Week starting", "Opened", "Closed", "Reopened"], periodRows(data.weekly)),
      chart("Backlog trend", ["Day", "Open cases"], data.daily.map(row => [dateLabel(row.date), row.backlog])),
      chart("Cases by journey step now", ["Journey step", "Open cases"], data.current.journey.map(row => [row.label, row.count])),
      chart("Workload by team now", ["Team (owner role)", "Open cases"], data.current.teams.map(row => [row.label, row.count])),
      !data.ai.eligible_records && h("p", { class: "empty" }, "No recorded synthetic AI briefing usage. No usage has been inferred."),
      chart("AI briefing review outcomes", ["Draft review", "Reviews"], data.ai.outcomes.map(row => [row.label, row.count]))));
  }
  async function closed() {
    if (!isManager()) return show(h("h1", {}, "Closed cases"), h("p", {}, "Only a manager sees closed cases."));
    const values = query();
    const makeFilters = (facets = { statuses: [], teams: [] }) => filters("#/closed", values, [
      select("status", "Recorded case status (stage)", values.get("status"), facets.statuses),
      field("start", "Closed on or after (UTC)", values.get("start") || "", "date"),
      field("end", "Closed on or before (UTC)", values.get("end") || "", "date"),
      select("team", "Team (owner role)", values.get("team"), facets.teams),
      field("q", "Search reference, resident or address", values.get("q") || ""),
    ]);
    const data = await load("/api/closed-cases", values, "Closed cases", makeFilters());
    if (!data) return;
    if (values.has("page") && values.get("page") !== String(data.page)) {
      values.set("page", String(data.page));
      history.replaceState(null, "", href("#/closed", values));
      displayedHash = location.hash;
    }
    const controls = makeFilters(data.facets);
    const pageLink = (page, label, enabled) => {
      const next = new URLSearchParams(values);
      next.set("page", String(page));
      return enabled ? h("a", { class: "btn alt", href: href("#/closed", next) }, label)
        : h("span", { class: "progress-unavailable" }, `${label} (unavailable)`);
    };
    show(h("div", { class: "progress-page" }, h("h1", {}, "Closed cases"),
      h("p", { class: "flag" }, "Demonstration data - fictional cases."),
      h("p", {}, "Closed does not necessarily mean works completed. Filter the recorded case status. " +
        "Open a case to review it; only a manager can reopen it with a reason."),
      controls,
      h("p", {}, `Closure date means the latest observed closure after any reopening. ` +
        `${number(data.unknown_closure_dates)} closed cases have unknown closure dates. ` +
        "They appear without date filters and are excluded when either date is set."),
      h("p", { role: "status", id: "closed-results" },
        `${number(data.total)} matching closed cases. Page ${number(data.page)} of ${number(data.pages)}.`),
      table("Matching closed cases", ["Case", "Recorded case status", "Closed on", "Team"],
        data.items.map(row => [
          h("span", {}, h("a", { href: `#/case/${encodeURIComponent(row.id)}` }, `${row.id}: ${row.resident}`),
            h("span", { class: "progress-address" }, `${row.address}, ${row.town} ${row.postcode}`),
            row.hazard && h("span", { class: "flag danger" }, "Safety issue open")),
          row.status, dateLabel(row.closed_on), row.team,
        ])),
      h("nav", { class: "progress-pagination", "aria-label": "Closed case pages" },
        pageLink(data.page - 1, "Previous page", data.page > 1),
        pageLink(data.page + 1, "Next page", data.page < data.pages))));
  }
  return { dashboard, closed };
})();
