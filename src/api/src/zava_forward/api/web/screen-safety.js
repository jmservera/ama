"use strict";

registerRoleScreen({
  id: "safety",
  title: "Safety referrals and response evidence",
  roles: ["Building Safety Liaison", ...screenManagers],
  render(c) {
    return [
      screenPanel("Independent hazard and safeguarding route",
        h("p", {}, "Use the existing hazard, repairs or safeguarding service immediately for urgent concerns. This view cannot classify a hazard, set a clock, close a hazard or authorise work. Retrofit restrictions must not delay that independent response."),
        h("p", {}, "Every reported safety item for this selected home stays visible, including historical items. A sent referral is not receipt, receipt is not acceptance, and repair is not a restart decision.")),
      ...(c.hazards || []).map((item, index) => {
        const decision = item.hold?.decision;
        return screenPanel(`Safety item ${index + 1}: ${screenValue(item.category)}`,
          h("p", { class: item.released ? "status-line" : "status-line danger" },
            item.released ? "Recorded restart state; check the independent decision evidence." : "Safety issue open; retrofit work stopped."),
          screenFields([
            ["Evidence class", item.classification], ["Reported urgency, not service classification", item.priority],
            ["Awareness time", screenStamp(item.aware_at)], ["Awareness source", item.source],
            ["Destination", screenPerson(item.destination)], ["External case reference", item.job],
            ["Sent", screenStamp(item.sent_at)], ["Sending evidence", item.sent_evidence],
            ["Received", screenStamp(item.received_at)], ["Receipt evidence", item.receipt_evidence],
            ["Accepted", screenStamp(item.accepted_at)], ["Acceptance evidence", item.acceptance_evidence],
            ["Named follow-up owner", screenPerson(item.follow_up)],
            ["External response due", screenStamp(item.response_due_at)],
            ["External resident update due", screenStamp(item.resident_update_due_at)],
            ["Stopped retrofit scope", item.hold?.case_id], ["Accountable role", item.hold?.accountable_role],
            ["Repair evidence", item.repair_evidence],
            ["Human restart decision by", screenPerson(decision?.actor)],
            ["Decision evidence", decision?.evidence], ["Decision reason", decision?.reason]
          ]),
          !item.received_at && screenUnknown(
            "Receipt is not evidenced. Sending has not transferred responsibility.",
            screenPerson(item.follow_up) === "Unknown" ? "Building Safety Liaison" : screenPerson(item.follow_up),
            "Chase receipt through the existing hazard service and record the supplied evidence separately."),
          item.released && !decision?.evidence && screenUnknown(
            "The recorded restart state has no supplied independent human decision evidence.",
            "Building Safety Liaison", "Verify the authoritative decision before treating any affected retrofit work as released."));
      }),
      !(c.hazards || []).length && screenUnknown("No safety reports are supplied; absence of a record is not proof of safety.", "Building Safety Liaison", "Check the independent service and use its urgent reporting route when needed.")
    ];
  }
});
