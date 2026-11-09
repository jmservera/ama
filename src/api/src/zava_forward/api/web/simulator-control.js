"use strict";
// Administrator screen for the finite simulator run control (issue 189). Shares h, api, show and me with app.js.
// It only edits the control file through the server; it cannot see or start a simulator job.
const SIMULATOR_CONTROL_API = "/api/admin/simulator-control";

function simulatorControlState(status) {
  if (status.availability === "not_configured") {
    return ["Not configured", "No run control file is configured for this service, so this screen cannot start or stop a run. Use the manual route below."];
  }
  if (status.availability === "unavailable") {
    return ["Unavailable", "The run control file cannot be read. The simulator sends nothing while it is missing or unreadable."];
  }
  if (status.availability === "invalid") {
    return ["Not valid", "The run control file is not valid. The simulator sends nothing until a valid control is written."];
  }
  const states = {
    send: ["Permitted", "Sending is permitted until the expiry time. This screen cannot see whether a simulator job is running."],
    stopped: ["Stopped", "Nothing is sent. The cohort and expiry are kept for the record."],
    expired: ["Expired", "The expiry time has passed. Nothing is sent."],
    invalid: ["Not valid", "The expiry is beyond the 14-day maximum, so every reader refuses it. Nothing is sent."],
  };
  return states[status.state] || ["Unknown", "The state could not be read. Treat sending as blocked and use the manual route."];
}

function simulatorControlFacts(status) {
  const [label, meaning] = simulatorControlState(status);
  const rows = [["State", `${label}. ${meaning}`]];
  if (status.owner) {
    const hours = status.time_limit.remaining_seconds / 3600;
    rows.push(
      ["Owner", `${status.owner.value} (declared in the control, not identity-verified)`],
      ["Time limit", `${status.time_limit.expires_at} UTC, ${new Intl.NumberFormat("en-GB", { maximumFractionDigits: 1 }).format(hours)} hours left, at most ${status.time_limit.max_days} days`],
      ["Approval reference", `${status.approval_reference.value} (declared, not verified)`],
      ["Cohort", `${status.cohort_size} homes. Home ids stay in the control file.`],
    );
    const capacity = status.capacity || {};
    rows.push(["Quota headroom", capacity.refused
      ? `Refused by the existing quota check: ${capacity.refused}.`
      : `${new Intl.NumberFormat("en-GB").format(capacity.messages_per_day)} messages a day against a budget of ${new Intl.NumberFormat("en-GB").format(capacity.daily_budget)} on the current hub tier. This is arithmetic, not live usage.`]);
  }
  rows.push(["Budget alert", `Not recorded and not verified live. ${status.budget_alert.detail}`]);
  return h("dl", {}, rows.flatMap(([term, text]) => [h("dt", {}, term), h("dd", {}, text)]));
}

async function simulatorControlView() {
  const heading = h("h1", { tabindex: "-1" }, "Simulator run control");
  const notice = h("p", { role: "status" });
  const refreshButton = h("button", { type: "button", onclick: () => simulatorControlView() }, "Refresh Status");
  let status;
  try {
    status = await api(SIMULATOR_CONTROL_API);
  } catch (error) {
    if (error.name === "AbortError" || !me) return;
    show(heading, h("p", { role: "alert", class: "err" }, `${error.message} Nothing was changed. Use the manual route: an operator with access to the control file share can run python -m zava_forward.api.live_control status.`), refreshButton);
    return;
  }
  const act = async (path, body, label) => {
    try {
      const result = await api(path, body);
      await simulatorControlView();
      const message = document.getElementById("simulator-control-notice");
      if (message) {
        message.textContent = `${label} saved and read back. ${result.changed ? "" : "Nothing needed changing. "}${result.audit_recorded === false ? "The audit entry was not recorded; tell the programme owner." : ""} Whether a simulator job runs is not checked here.`;
      }
    } catch (error) {
      if (error.name === "AbortError" || !me) return;
      notice.textContent = `${label} failed: ${error.message} If this repeats, refresh and check the status before you try again.`;
      notice.setAttribute("role", "alert");
      notice.className = "err";
    }
  };
  notice.id = "simulator-control-notice";
  const parts = [
    heading,
    h("p", {}, "This screen edits the existing finite run control for the synthetic simulator. It does not start a job, call Azure or change any permission. The simulator re-reads the control every slot, and a stop, an expiry or an unreadable file ends sending."),
    h("section", { class: "card", "aria-labelledby": "simulator-status-heading" }, h("h2", { id: "simulator-status-heading" }, "Current status"), simulatorControlFacts(status), refreshButton),
    notice,
  ];
  const canWrite = status.writable && status.availability !== "not_configured";
  if (status.read_only) {
    parts.push(h("p", { role: "status" }, "Start and Stop are switched off because administrator access without a staff role shows every option but changes nothing. A staff role is needed to act."));
  } else if (!canWrite) {
    parts.push(h("p", { role: "status" }, status.availability === "not_configured"
      ? "Start and Stop are switched off because no control file is configured."
      : "Start and Stop are switched off because the control file location is not writable from this service."));
  } else {
    if (status.state !== "send") {
      const owner = h("input", { id: "sim-owner", name: "owner", type: "text", maxlength: 160, required: true, autocomplete: "off", spellcheck: "false" });
      const approval = h("input", { id: "sim-approval", name: "approval_reference", type: "text", maxlength: 160, required: true, autocomplete: "off", spellcheck: "false" });
      const expires = h("input", { id: "sim-expires", name: "expires_at", type: "text", required: true, autocomplete: "off", spellcheck: "false", placeholder: "2026-11-12T18:00:00Z", "aria-describedby": "sim-expires-help" });
      const homes = h("textarea", { id: "sim-homes", name: "homes", rows: 3, required: true, autocomplete: "off", spellcheck: "false", "aria-describedby": "sim-homes-help" });
      const confirm = h("input", { id: "sim-start-confirm", name: "confirm", type: "checkbox" });
      parts.push(h("form", { class: "card", "aria-labelledby": "simulator-start-heading", onsubmit: (event) => {
        event.preventDefault();
        return act(`${SIMULATOR_CONTROL_API}/start`, {
          owner: owner.value, approval_reference: approval.value, expires_at: expires.value.trim(),
          homes: homes.value.split(/[\s,]+/).filter(Boolean), expected_revision: status.revision, confirm: confirm.checked,
        }, "Start");
      } },
        h("h2", { id: "simulator-start-heading" }, "Start a finite run"),
        h("p", { id: "sim-start-help" }, "The existing limits apply: 1 to 100 homes, an expiry in the future and at most 14 days away, and the daily message budget. A start that breaks a limit is refused."),
        h("div", {}, h("label", { for: "sim-owner" }, "Named owner"), owner),
        h("div", {}, h("label", { for: "sim-approval" }, "Approval reference"), approval),
        h("div", {}, h("label", { for: "sim-expires" }, "Expiry time (UTC)"), expires, h("p", { id: "sim-expires-help", class: "muted" }, "Use the form 2026-11-12T18:00:00Z.")),
        h("div", {}, h("label", { for: "sim-homes" }, "Home ids"), homes, h("p", { id: "sim-homes-help", class: "muted" }, "Separate ids with commas, spaces or new lines.")),
        h("div", {}, confirm, h("label", { for: "sim-start-confirm" }, "I confirm this permits sending for these homes until the expiry time.")),
        h("button", { type: "submit" }, "Start Finite Run")));
    }
    if (status.state) {
      const confirm = h("input", { id: "sim-stop-confirm", name: "confirm", type: "checkbox" });
      parts.push(h("form", { class: "card", "aria-labelledby": "simulator-stop-heading", onsubmit: (event) => {
        event.preventDefault();
        return act(`${SIMULATOR_CONTROL_API}/stop`, { expected_revision: status.revision, confirm: confirm.checked }, "Stop");
      } },
        h("h2", { id: "simulator-stop-heading" }, "Stop the run"),
        h("p", {}, "A stop takes effect at the simulator's next slot check. The cohort and expiry stay in the control file. Stopping again is safe if the control is already stopped or expired."),
        h("div", {}, confirm, h("label", { for: "sim-stop-confirm" }, "I confirm I want to stop this run.")),
        h("button", { type: "submit" }, "Stop Run")));
    }
  }
  parts.push(h("section", { class: "card", "aria-labelledby": "simulator-manual-heading" }, h("h2", { id: "simulator-manual-heading" }, "Manual route"), h("p", {}, status.manual_route)));
  show(...parts);
}
