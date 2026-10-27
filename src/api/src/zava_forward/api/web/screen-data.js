"use strict";

registerRoleScreen({
  id: "data",
  title: "Data conflicts and recovery context",
  roles: screenManagers,
  render(c) {
    const source = (item) => `${screenValue(item?.value)}; source ${screenValue(item?.source_id)}; version ${screenValue(item?.version)}; date ${screenValue(item?.date)}; ${screenValue(item?.validation_state)}`;
    return [
      screenPanel("Conflict and return queue",
        h("p", {}, "Both original values remain visible. A query disposition does not select a winning source or make eligibility known. This view cannot correct, replay or overwrite a source."),
        screenTable("Conflicting source records", ["Query and field", "First source", "Compared source", "Owner", "Query state", "Eligibility"],
          (c.stock_reconciliation || []).map((item) => [
            `${item.id}: ${item.field}`, source(item.left), source(item.right),
            screenPerson(item.query_owner), item.status, item.eligibility
          ])),
        screenTable("Returned source work", ["Return source", "Sender", "Receiving owner", "Reason", "Next action"],
          (c.returns || []).map((item) => [
            item.source, item.by, screenPerson(item.receiving_owner), item.reason, item.next_action
          ]))),
      screenPanel("Recorded event metadata",
        h("p", {}, "These supplied record events are not an operational audit trail or proof of complete history. Narrative case history is not substituted for independently verified audit evidence."),
        screenTable("Stock query events", ["Event", "Query", "State", "Recorded by", "Recorded at", "Evidence"],
          (c.stock_reconciliation_events || []).map((item) => [
            item.id, item.query_id, item.status, screenPerson(item.recorded_by),
            screenStamp(item.at), item.evidence
          ])),
        screenTable("Return event context", ["Schema and event type", "Source/version", "Actor", "Recorded at"],
          (c.returns || []).map((item) => [
            `${screenValue(item.schema)}; ${screenValue(item.event_type)}`,
            `${screenValue(item.source)}; ${screenValue(item.source_version)}`,
            screenPerson(item.actor) === "Unknown" ? item.by : screenPerson(item.actor),
            screenStamp(item.at)
          ]))),
      screenPanel("Exception and recovery context",
        screenFields([["Failed operation and attempt", "Unknown; no runtime failure receipt supplied"],
          ["Acknowledged or uncertain outcome", "Unknown"], ["Corrective-test evidence", "Unknown"],
          ["Recovery owner", "Programme Support Officer; confirm the named operator"],
          ["Original sources", "Preserved above; no automatic replay or silent correction"]]),
        screenUnknown("No verified recovery receipt or restart authority is supplied.", "Programme Support Officer", "Use the existing controlled runbook, reconcile uncertain outcomes and obtain the required human decision before any separate recovery operation."))
    ];
  }
});
