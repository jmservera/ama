"use strict";

registerRoleScreen({
  id: "engagement",
  title: "Housing and resident engagement",
  roles: ["Resident Liaison Officer", "Retrofit Coordinator", ...screenManagers],
  render(c) {
    const update = c.resident_update;
    return [
      screenPanel("Resident choice for each measure",
        h("p", {}, "A call, visit, access arrangement or representative contact is not agreement to works. Paused and Withdrawn choices stay separate. The resident can use phone, letter, a visit or assisted service without using a portal."),
        screenTable("Measure-specific choices", ["Measure", "Current scope", "Design version", "Resident answer", "Readiness", "Answer versions"],
          (c.measure_decisions || []).map((m) => [
            m.measure,
            m.context ? `${m.context.scope}; revision ${m.context.revision}` : "Unknown",
            m.context?.design_version, m.status, m.readiness,
            (m.versions || []).map((answer) => `v${answer.version}: ${answer.status}; scope revision ${screenValue(answer.context_revision)}; source ${screenValue(answer.source)}; recorded by ${screenValue(answer.recorded_by)}`).join("; ") || "Not recorded"
          ]))),
      screenPanel("Linked update commitment",
        h("p", {}, "An update commitment is not a sent message or evidence of receipt. Handoffs do not transfer it automatically."),
        update ? screenFields([
          ["Purpose or linked issue", update.purpose], ["Update owner", screenPerson(update.owner_identity)],
          ["Status", update.status], ["Version", update.version], ["Due", screenStamp(update.due_at)],
          ["Date basis", update.basis], ["Safe route reference", update.safe_contact_ref],
          ["Recorded at", screenStamp(update.at)]
        ]) : screenUnknown("No update commitment is supplied.", "Resident Liaison Officer", "Confirm the purpose, named owner, due-date basis and resident-confirmed safe route in the existing case workspace.")),
      screenPanel("Accessible service issues and remedy",
        screenTable("Service requests", ["Reference and route", "Requested outcome", "Contact adjustment", "Response and owner", "Remedy and owner", "Next update"],
          (c.service_requests || []).map((request) => [
            `${request.id}: ${request.route}`, request.desired_outcome,
            (request.accessibility || []).join(", ") || "Unknown",
            `${screenValue(request.status)}; ${screenPerson(request.status_owner)}`,
            `${screenValue(request.remedy?.status)}; ${screenPerson(request.remedy?.owner)}`,
            request.next_update
          ])),
        h("p", {}, "Response closure does not complete a remedy or change a works choice. Ask the named officer for an accessible explanation, independent human review or the formal complaints route. Urgent safety concerns go directly to the existing hazard and repairs service; this screen does not send a referral.")),
      screenUnknown("This read-only view cannot confirm contact safety, representative authority or current consent.", "Resident Liaison Officer", "Check the current source and measure revision with the resident before using the existing recording workflow.")
    ];
  }
});
