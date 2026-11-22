"""Safeguarding clock rendering: plain text, named owner, no colour-only status.

Runs the real workSummary from app.js in Node with a stub element builder. Constructed
synthetic values only; static rendering evidence, not assistive technology evidence.
"""

import json
import subprocess
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/app.js"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1], "utf8");
const extract = (name) => {
  const start = source.indexOf("function " + name + "(");
  let depth = 0, end = 0;
  for (let j = source.indexOf(") {", start) + 2; j < source.length; j++) {
    if (source[j] === "{") depth++;
    if (source[j] === "}" && --depth === 0) { end = j + 1; break; }
  }
  return source.slice(start, end);
};
const h = (tag, props, ...kids) => ({tag, class: (props || {}).class, kids: kids.flat(Infinity)});
const context = vm.createContext({h});
vm.runInContext(extract("clockStatusText") + extract("workSummary"), context);
const text = (n) => typeof n === "string" ? n : n ? (n.kids || []).map(text).join(" ") : "";
const out = JSON.parse(process.argv[2]).map((work) => {
  const node = vm.runInContext("workSummary(" + JSON.stringify(work) + ")", context);
  return node.kids.flat(Infinity).filter((k) => k && k.class === "safeguarding-clock")
    .map((k) => ({tag: k.tag, text: text(k)}));
});
console.log(JSON.stringify(out));
"""

BASE = dict(
    owner="Task owner",
    reason="r",
    next_action="n",
    source="s",
    evidence="e",
    version=1,
    recorded_at="t",
    as_of="a",
    handoff=None,
    hazard_clocks=[],
)
CLOCK = dict(
    owner="Sam Guard",
    owner_role="Safeguarding lead",
    owner_status="Named accountable owner recorded.",
    elapsed_hours=12,
    referred_at="2026-10-15T12:00Z",
    response_due_at="2026-10-17",
    response_state="Overdue",
    authority="Safeguarding lead",
)


class SafeguardingClockRendering(unittest.TestCase):
    def render(self, *works: dict[str, object]) -> list[list[dict[str, str]]]:
        done = subprocess.run(
            ["node", "-e", SCRIPT, str(APP), json.dumps(list(works))],
            capture_output=True,
            text=True,
            check=True,
            stdin=subprocess.DEVNULL,
        )
        result: list[list[dict[str, str]]] = json.loads(done.stdout)
        return result

    def test_clock_and_owner_are_stated_as_text_in_a_paragraph(self) -> None:
        unknown = dict(
            CLOCK,
            owner="Unknown",
            owner_role="Unknown",
            elapsed_hours=None,
            owner_status="No named accountable owner is recorded.",
        )
        shown, missing = self.render(
            dict(BASE, safeguarding_clocks=[CLOCK]), dict(BASE, safeguarding_clocks=[unknown])
        )
        self.assertEqual(shown[0]["tag"], "p")
        for phrase in (
            "Safeguarding clock",
            "12 elapsed hours",
            "named accountable owner: Sam Guard",
            "Safeguarding lead",
            "Response: Overdue",
        ):
            self.assertIn(phrase, shown[0]["text"])
        self.assertIn("named accountable owner: Unknown", missing[0]["text"])
        self.assertIn("recorded view: Unknown;", missing[0]["text"])
        self.assertIn("No named accountable owner", missing[0]["text"])

    def test_absent_or_empty_clocks_render_nothing(self) -> None:
        self.assertEqual(self.render(dict(BASE), dict(BASE, safeguarding_clocks=[])), [[], []])


if __name__ == "__main__":
    unittest.main()
