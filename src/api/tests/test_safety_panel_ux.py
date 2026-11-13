# ruff: noqa: E501
"""Issue 1530: case safety panel labels, per-action forms, next-step guidance and legacy rows."""

import subprocess
import unittest

from test_case_journey import DOM, WEB, shipped_helpers

PRELUDE = r"""
Node.prototype.setCustomValidity = function (message) { this.message = message; };
Node.prototype.reportValidity = function () { return !(this.hasAttribute("required") && this.message); };
const source = require("node:fs").readFileSync(WEB_APP, "utf8");
const start = source.indexOf("const SAFETY_ROLES");
const mid = source.indexOf("const HAZ_PRIORITIES");
eval(source.slice(start, source.indexOf("\n", mid)).replaceAll("const ", "var "));
eval(source.slice(source.indexOf("function hazardState"), source.indexOf("async function contractorListView"))
  .replace(/^function (\w+)/gm, "globalThis.$1 = function $1"));
let me;
const posts = [];
const refreshed = [];
globalThis.post = async (id, name, body) => { posts.push([id, name, body]); };
const BEA = {code: "BS-1", email: "bea@example.test", name: "Bea Safe", role: "Building Safety Liaison"};
const BO = {code: "BS-2", email: "bo@example.test", name: "Bo Safe", role: "Building Safety Liaison"};
const PM = {code: "PM-1", email: "pm@example.test", name: "Pat Manager", role: "Retrofit Programme Manager"};
const RC = {code: "RC-1", email: "rex@example.test", name: "Rex Coordinator", role: "Retrofit Coordinator"};
const hold = (extra = {}) => ({scope: "Home", case_id: "ZF-1", status: "Active",
  accountable_role: "Building Safety Liaison", decision: null, ...extra});
const base = (extra = {}) => ({category: "Damp and mould", priority: "Significant", released: false,
  source: "Phone call", aware_at: "2026-01-01T10:00:00Z", job: "RJ-700047", hold: hold(), ...extra});
const legacy = (extra = {}) => base({referred: "2026-01-02", repaired: "2026-02-01", repair_evidence: null,
  hold: hold({accountable_role: null, legacy: true}), ...extra});
const referred = (extra = {}) => base({referral_version: 1, destination: {...BEA}, sent_at: "2026-01-03T09:00:00Z",
  hold: hold(), ...extra});
const repaired = (extra = {}) => referred({received_at: "2026-01-04", accepted_at: "2026-01-05",
  repaired: "2026-01-06", repair_evidence: "Cert DM-9921", raised_identity: {...RC},
  repaired_identity: {...BEA}, ...extra});
function build(user, hazards) {
  me = {user, staff: [BO, PM, BEA, RC]};
  return safetyPanel({hazards}, "ZF-1", async (fn, fields) => { refreshed.push(fields); await fn(); });
}
const text = (node) => node.textContent;
const controls = (root) => root.querySelectorAll("input, select, textarea");
const byId = (root, id) => root.querySelector("#" + id);
const labelFor = (root, id) => root.querySelectorAll("label").find((l) => l.getAttribute("for") === id);
const submit = (form) => form.events.submit({preventDefault() {}});
const formWith = (root, id) => root.querySelectorAll("form").find((f) => controls(f).some((c) => c.id === id));
const cards = (root) => root.querySelectorAll("li").filter((li) => li.className === "safety-item");
"""


def run(body: str) -> None:
    script = (
        DOM
        + f"const WEB_APP = {str(WEB / 'app.js')!r};\n"
        + shipped_helpers()
        + PRELUDE
        + "(async () => {\n"
        + body
        + "\n})().catch((e) => { console.error(e); process.exitCode = 1; });\n"
    )
    result = subprocess.run(["node", "-e", script], text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stderr


class SafetyPanelUx(unittest.TestCase):
    def test_every_control_has_visible_label_unique_id_and_hint(self) -> None:
        run(r"""
const panel = build(BEA, [legacy(), base(), referred(), repaired(), repaired({released: true, accepted_at: "x"})]);
const ids = new Set();
const all = controls(panel);
assert.ok(all.length >= 12);
for (const control of all) {
  assert.ok(control.id, "id");
  assert.ok(!ids.has(control.id), "unique " + control.id);
  ids.add(control.id);
  assert.ok(labelFor(panel, control.id), "label for " + control.id);
  assert.equal(control.getAttribute("aria-label"), null, control.id);
  const hint = byId(panel, control.getAttribute("aria-describedby"));
  assert.ok(hint, "hint for " + control.id);
  assert.ok(String(hint.className).includes("field-hint"), control.id);
}
for (const id of ["hz-cat", "hz-pri", "hz-note", "hz-source", "hz-aware"]) assert.ok(ids.has(id), id);
assert.ok(ids.has("hz-0-refer-job") && ids.has("hz-1-refer-to"));
""")

    def test_each_action_has_its_own_form_fieldset_and_evidence_field(self) -> None:
        run(r"""
const panel = build(BEA, [referred(), referred({received_at: "r"}), referred({received_at: "r", accepted_at: "a"}),
  repaired({raised_identity: {...RC}, repaired_identity: {...RC}, destination: {...BEA}}), legacy()]);
me.user = BO;
const second = build(BO, [repaired({repaired_identity: {...RC}, raised_identity: {...RC}})]);
for (const root of [panel, second]) {
  assert.ok(root.querySelectorAll("form").length >= 1);
  for (const form of root.querySelectorAll("form")) {
    assert.equal(form.querySelectorAll("fieldset").length, 1);
    assert.equal(form.querySelectorAll("legend").length, 1);
  }
}
assert.ok(!text(panel).includes("External evidence reference External"), "no shared field");
const evidenceCounts = panel.querySelectorAll("form").filter((f) => !controls(f).some((c) => c.id === "hz-cat"))
  .map((f) => controls(f).filter((c) => /evidence$/.test(c.id)).length);
assert.ok(evidenceCounts.length >= 4);
assert.ok(evidenceCounts.every((n) => n === 1), JSON.stringify(evidenceCounts));
for (const id of ["hz-0-receive-evidence", "hz-1-accept-evidence", "hz-2-repair-evidence", "hz-4-refer-evidence"]) {
  assert.ok(byId(panel, id), id);
  assert.ok(text(labelFor(panel, id)).startsWith("External evidence reference"), id);
}
assert.ok(byId(second, "hz-0-release-evidence") && byId(second, "hz-0-release-note"));
// Submitting one form posts only its own evidence value.
byId(panel, "hz-0-receive-evidence").value = "ACK-1";
byId(panel, "hz-1-accept-evidence").value = "Accepted";
await submit(formWith(panel, "hz-0-receive-evidence"));
assert.deepEqual(posts.pop(), ["ZF-1", "hazard-receive", {index: 0, evidence: "ACK-1"}]);
assert.deepEqual(refreshed.pop().map((f) => f.id), ["hz-0-receive-evidence"]);
await submit(formWith(panel, "hz-1-accept-evidence"));
assert.deepEqual(posts.pop(), ["ZF-1", "hazard-accept", {index: 1, evidence: "Accepted"}]);
// An empty required field blocks submission.
byId(panel, "hz-2-repair-evidence").value = "   ";
const before = posts.length;
await submit(formWith(panel, "hz-2-repair-evidence"));
assert.equal(posts.length, before);
assert.equal(byId(panel, "hz-2-repair-evidence").message, "Enter this detail.");
byId(panel, "hz-2-repair-evidence").events.input();
assert.equal(byId(panel, "hz-2-repair-evidence").message, "");
""")

    def test_next_step_callout_names_who_acts_and_explains_waiting(self) -> None:
        run(r"""
const waiting = build(RC, [referred(), referred({received_at: "r"}), referred({received_at: "r", accepted_at: "a"}), legacy(), base()]);
const notes = cards(waiting).map((card) => text(card.querySelector(".safety-next")));
assert.equal(notes.length, 5);
assert.ok(notes.every((n) => n.startsWith("What humans need to do next")));
assert.ok(notes[0].includes("Waiting on Bea Safe (Building Safety Liaison)"));
assert.ok(notes[1].includes("Waiting on Bea Safe") && notes[1].includes("accepted responsibility"));
assert.ok(notes[2].includes("Waiting on Bea Safe") && notes[2].includes("repair"));
assert.ok(notes[3].includes("older tracker") && notes[3].includes("RJ-700047"));
assert.equal(waiting.querySelectorAll("form").filter((f) => !byId(f, "hz-cat") && !byId(f, "hz-source")).length, 2);
const mine = build(BEA, [referred()]);
assert.ok(text(cards(mine)[0].querySelector(".safety-next")).includes("You are the assigned safety coordinator"));
const done = build(BEA, [repaired({released: true, hold: hold({status: "Released", decision: {actor: BO, reason: "Fixed", evidence: "Cert"}})})]);
assert.equal(cards(done)[0].querySelector(".safety-next"), undefined);
assert.ok(text(cards(done)[0]).includes("Restarted by Bo Safe"));
""")

    def test_legacy_row_is_truthful_prefilled_and_has_no_restart_trap(self) -> None:
        run(r"""
const panel = build(RC, [legacy({hold: hold({case_id: "ZF-2025-0122", accountable_role: null, legacy: true})})]);
const all = text(panel);
for (const old of ["Bind legacy referral prospectively", "Destination: Not bound", "Repair evidenced"])
  assert.ok(!all.includes(old), old);
assert.ok(!all.includes("Repair evidence: Unknown"));
assert.ok(all.includes("Assign a Zava coordinator to track this older referral"));
assert.ok(all.includes("Assign coordinator and record referral"));
assert.ok(all.includes("Older tracker shows a repair, but verification evidence is not recorded here yet"));
assert.ok(all.includes("Why retrofit work cannot restart yet"));
assert.equal(byId(panel, "hz-0-refer-job").value, "RJ-700047");
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
assert.ok(!all.includes("Allow home retrofit work to restart"));
const options = byId(panel, "hz-0-refer-to").querySelectorAll("option").map((o) => o.getAttribute("value"));
assert.equal(options[0], "bo@example.test");
assert.equal(options[options.length - 1], "pm@example.test");
const facts = panel.querySelector(".safety-facts");
assert.equal(facts.querySelectorAll("dt").length, 4);
assert.ok(text(facts).includes("Not assigned yet"));
assert.ok(!text(facts).includes("Unknown"));
byId(panel, "hz-0-refer-to").value = "bea@example.test";
byId(panel, "hz-0-refer-evidence").value = "Portal check";
await submit(formWith(panel, "hz-0-refer-job"));
assert.deepEqual(posts.pop(), ["ZF-1", "hazard-refer", {index: 0, to: "bea@example.test", job: "RJ-700047", evidence: "Portal check"}]);
""")

    def test_audit_fields_and_timings_sit_in_collapsed_details(self) -> None:
        run(r"""
const panel = build(BEA, [referred({received_at: "r", accepted_at: "a"})]);
const card = cards(panel)[0];
const details = card.querySelector(".safety-details");
assert.ok(text(details).includes("Unknown (external service owns timing)"));
assert.ok(!text(card.querySelector(".safety-facts")).includes("Unknown"));
assert.equal(details.hasAttribute("open"), false);
const optional = card.querySelector(".safety-optional");
assert.ok(text(optional.querySelector("summary")).includes("(4 unrecorded)"));
assert.ok(controls(optional).some((c) => c.id === "hz-0-time-responded_at"));
assert.ok(card.querySelector(".safety-step") !== optional.querySelector(".safety-step"));
byId(panel, "hz-0-times-evidence").value = "SLA screen";
await submit(formWith(panel, "hz-0-times-evidence"));
const [, action, body] = posts.pop();
assert.equal(action, "hazard-times");
assert.equal(body.evidence, "SLA screen");
assert.equal(body.index, 0);
""")

    def test_restart_form_needs_independent_reviewer_with_the_accountable_role(self) -> None:
        run(r"""
const ready = () => repaired();
let panel = build(BO, [ready()]);
assert.ok(byId(panel, "hz-0-release-evidence"));
assert.ok(panel.querySelector(".primary-step"));
byId(panel, "hz-0-release-evidence").value = "DM-9921";
byId(panel, "hz-0-release-note").value = "Dry";
await submit(formWith(panel, "hz-0-release-note"));
assert.deepEqual(posts.pop(), ["ZF-1", "hazard-release", {index: 0, evidence: "DM-9921", note: "Dry"}]);
// The person who recorded the repair cannot restart; neither can one who only appears in history.
panel = build(BEA, [ready()]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
assert.ok(text(panel).includes("You cannot approve the restart yourself"));
panel = build(BO, [repaired({raised_identity: null, history: [{action: "safety_raised", actor: {...BO}}]})]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
panel = build(BO, [repaired({repaired_identity: null, repaired_by_email: "BO@example.test"})]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
// Name only matches when no identifier is recorded.
panel = build(BO, [repaired({raised_identity: {name: "Bo Safe"}, raised_by_email: null})]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
// Wrong role for the recorded accountable role or not a safety role.
panel = build(PM, [ready()]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
assert.ok(text(panel).includes("waiting for an independent safety review"));
assert.ok(text(panel).includes("Building Safety Liaison"));
panel = build(RC, [ready()]);
assert.equal(byId(panel, "hz-0-release-evidence"), undefined);
// A manager can restart a legacy-hold record that names no accountable role.
panel = build(PM, [repaired({hold: hold({accountable_role: null, legacy: true})})]);
assert.ok(byId(panel, "hz-0-release-evidence"));
""")

    def test_raise_form_explains_when_to_use_and_defaults_to_significant(self) -> None:
        run(r"""
const panel = build(RC, []);
assert.ok(text(panel).includes("No safety issues recorded."));
assert.ok(text(panel).includes("also available after retrofit closure"));
assert.ok(text(byId(panel, "hz-raise-intro")).includes("contact the hazard and repairs service immediately"));
assert.equal(byId(panel, "hz-pri").value, "Significant");
assert.ok(text(labelFor(panel, "hz-note")).includes("(optional)"));
for (const id of ["hz-cat", "hz-pri", "hz-source", "hz-aware"]) assert.ok(text(labelFor(panel, id)).includes("(required"), id);
for (const id of ["hz-note", "hz-source", "hz-aware"]) assert.ok(text(byId(panel, id + "-hint")).length > 60, id);
assert.ok(text(byId(panel, "hz-note-hint")).includes("Example:"));
assert.ok(text(byId(panel, "hz-source-hint")).includes("Example:"));
assert.ok(text(byId(panel, "hz-aware-hint")).includes("Example:"));
assert.ok(byId(panel, "hz-source").hasAttribute("required") && byId(panel, "hz-aware").hasAttribute("required"));
const form = formWith(panel, "hz-source");
await submit(form);
assert.equal(posts.length, 0, "blank source blocked");
byId(panel, "hz-source").events.input();
assert.equal(byId(panel, "hz-source").message, "");
byId(panel, "hz-source").value = "Resident call";
byId(panel, "hz-aware").value = "2026-01-01T10:00";
await submit(form);
const [, action, body] = posts.pop();
assert.equal(action, "hazard-raise");
assert.equal(body.priority, "Significant");
assert.equal(body.source, "Resident call");
""")


if __name__ == "__main__":
    unittest.main()
