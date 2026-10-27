"use strict";

registerRoleScreen({
  id: "technical",
  title: "Technical and independent quality evidence",
  roles: ["Retrofit Coordinator", "Quality Inspector", ...screenManagers],
  render(c) {
    const technical = c.technical;
    const reviews = [["assessment", "Assessment"], ["design", "Design"],
      ["building", "Building and safety dependency"], ["coordination", "Coordination"]];
    return [
      screenPanel("Sourced home facts and design version",
        screenFields([["Home", c.id], ["Recorded EPC, not verified here", c.home?.epc],
          ["Home type", c.home?.type], ["Tenure", c.home?.tenure],
          ["Design version", technical?.design_version], ["Design recorded by", technical?.design_name]]),
        screenTable("Source document references", ["Reference", "Kind", "Version", "Recorded date", "Scan state, not professional acceptance"],
          (c.documents || []).map((item) => [item.id, item.kind, item.version, item.at, item.scan?.status]))),
      screenPanel("Separate professional sign-offs",
        h("p", {}, "A recorded sign-off is not a generic approval. Confirm the exact design version, professional competence and appointment. Missing or stale evidence cannot establish readiness."),
        screenTable("Independent technical reviews", ["Review", "State", "Design version", "Reviewer", "Current-version evidence"],
          reviews.map(([key, title]) => {
            const review = technical?.signoffs?.[key];
            return [title, review?.status, review?.version, review?.by,
              review?.status === "Signed off" && review.version === technical?.design_version
                ? "Version matches; verify professional evidence"
                : "Missing or stale version; cannot establish readiness"];
          })),
        screenTable("Missing references and named review routing", ["Missing item", "Required competent reviewer role", "Proposed named reviewer, not appointed"],
          (c.technical_missing || []).map((item) => [
            item.item, item.assigned_to,
            (c.suggestions || []).filter((person) => person.role === item.assigned_to)
              .map((person) => person.name).join("; ") || "Unknown; the required professional role must nominate a competent reviewer"
          ]))),
      screenPanel("Per-measure quality, defects and reinspection",
        h("p", {}, "Positive evidence is required for each measure. Provider submission, independent acceptance, defect correction, reinspection and resident handover are separate. No evidence is accepted or handed over here."),
        ...(c.quality || []).map((record) => h("section", { class: "screen-record" },
          h("h3", {}, `${record.measure}: ${record.state}`),
          screenFields([["Evidence version", record.evidence_version], ["Checklist version", record.checklist_version],
            ["Submitted by", record.submitted_by], ["Evidence source", record.source],
            ["Independent accepted-by record", record.accepted_by],
            ["Defect", record.defect?.description], ["Defect owner", record.defect?.owner],
            ["Return reason", record.defect?.reason], ["Correction evidence", record.defect?.remediation_evidence],
            ["Reinspection state", record.state === "Fixed, awaiting reinspection" ? record.state : "Not established by this state"],
            ["Resident handover evidence", record.handover?.note]]),
          screenTable(`Positive evidence for ${record.measure}`, ["Check", "Supplied evidence reference"],
            (record.items || []).map((item) => [item.label, item.evidence])))),
        !(c.quality || []).length && h("p", { class: "empty" }, "No per-measure quality evidence supplied."),
        screenUnknown("Incomplete, returned, replaced or stale evidence blocks handover; a recorded state alone does not clear it.", "Independent Quality Inspector", "Check every current measure and return defects to the named owner for correction and independent reinspection."))
    ];
  }
});
