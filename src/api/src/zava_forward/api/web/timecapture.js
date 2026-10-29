"use strict";
// Staff time capture screens (PR-004): status checklist, notice, own entries, manager enabling and aggregate report. Shares h, api, show, me and isManager with app.js.
async function timeView() {
  try {
    const st = await api("/api/time/status");
    const status = h("p", { role: "status" });
    const save = async (path, body) => {
      try { await api(path, body); await timeView(); }
      catch (error) { status.textContent = error.message; }
    };
    const check = (ok, text) => h("li", {}, `${ok ? "Done" : "Missing"}: ${text}`);
    const body = [h("h1", {}, "Staff time capture"),
      h("p", { role: "status" }, st.enabled ? "Time capture is on." : st.reason), status,
      h("ul", {}, check(st.flag_on, "feature switched on"), check(st.dpia_recorded, "DPIA reference recorded"),
        check(st.consultation_recorded, "staff consultation recorded"), check(st.notice_approved, "staff notice approved"),
        check(st.requested, st.requested ? `enabling requested by ${st.requested_by} (${st.requested_role}, audited)` : "enabling request by a manager (audited)"),
        check(st.activated, st.activated ? `enabled by ${st.activated_by} (${st.activated_role}) at ${st.activated_at} (audited)` : "enabling by a manager in a different role (audited)"))];
    const ready = st.flag_on && st.dpia_recorded && st.consultation_recorded && st.notice_approved;
    if (isManager() && ready && !st.requested) {
      body.push(h("button", { onclick: () => save("/api/time/request-enable", {}) }, "Request enabling (audited)"));
    }
    if (isManager() && ready && st.requested && !st.activated) {
      body.push(h("button", { onclick: () => save("/api/time/enable", {}) }, "Enable time capture (audited)"),
        h("p", { class: "muted" }, "Refused if you made the request or hold the same role as the requester."));
    }
    if (st.enabled) {
      body.push(h("h2", {}, "Staff notice"), h("p", {}, st.notice));
      if (!st.acknowledged) body.push(h("button", { onclick: () => save("/api/time/acknowledge", {}) }, "I have read the notice"));
      else {
        const cs = h("input", { type: "text", maxlength: 40, "aria-label": "Case reference" });
        const mins = h("input", { type: "number", min: 1, max: 600, "aria-label": "Minutes" });
        const act = h("select", { "aria-label": "Activity" }, st.activities.map((a) => h("option", { value: a }, a)));
        body.push(h("h2", {}, "Record time"), h("div", { class: "row" }, cs, mins, act,
          h("button", { onclick: () => save("/api/time", { case_id: cs.value, minutes: mins.value, activity: act.value }) }, "Save")));
        const mine = await api("/api/time/mine");
        body.push(h("h2", {}, "My entries"), h("ul", {}, mine.map((e) => h("li", {}, `${e.at} ${e.case_id} ${e.minutes} min ${e.activity}`))));
      }
      if (isManager()) {
        const rep = await api("/api/time/report");
        body.push(h("h2", {}, "Totals by activity"), h("p", { class: "muted" }, `${rep.note} Minimum group: ${rep.min_group} people.`),
          h("ul", {}, rep.by_activity.map((r) => h("li", {}, `${r.activity}: ${r.minutes} min in ${r.entries} entries`))),
          h("p", {}, `${rep.suppressed_activities} activity group(s) hidden because too few people contributed.`));
      }
    }
    show(...body);
  } catch (e) {
    if (e.name === "AbortError" || !me) return;
    show(h("h1", {}, "Staff time capture"), h("p", { role: "alert" }, e.message));
  }
}
