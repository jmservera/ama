"""The Finance queue shows the investment limit pause signal from the shipped panels.js (#99)."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const src = fs.readFileSync(process.argv[1] + "/panels.js", "utf8");
const start = src.indexOf("function exposureNotice");
const end = src.indexOf("\n}\n", src.indexOf("async function financeQueueView")) + 3;
const data = JSON.parse(process.argv[2]);
const text = (n) => n === null || n === undefined || n === false ? "" :
  typeof n === "string" ? n : [n.tag, ...n.kids.map(text)].join(" ");
let shown;
const me = {user: {role: "Grants and Evidence Officer"}};
const api = async (path) => {
  if (path === "/api/finance") return [];
  if (data.exposure === null) throw new Error("503");
  return data.exposure;
};
const h = (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity)});
const show = (...nodes) => { shown = nodes; };
const money = (x) => String(x);
eval(src.slice(start, end) + "\nfinanceQueueView().then(() =>\n" +
  "console.log(JSON.stringify(shown.map(text))));");
"""


def render(exposure: Any) -> str:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(dict(exposure=exposure))],
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return " | ".join(json.loads(result.stdout))


class FinanceExposureScreen(unittest.TestCase):
    def test_breach_is_a_pause_for_a_person(self) -> None:
        out = render(
            dict(
                status="Breach",
                signal="Pause for human decision",
                reason="Over approved limit: envelope.",
                findings=[
                    dict(limit="envelope", state="Breach", observed=100, maximum=50, unit="GBP")
                ],
                action="Escalate to the Board; restart needs their recorded approval.",
                notice="Signal for a human decision only.",
            )
        )
        self.assertIn("Pause for human decision. Breach.", out)
        self.assertIn("envelope: Breach, 100 of 50 GBP", out)
        self.assertIn("restart needs their recorded approval", out)

    def test_held_without_approved_limits_is_not_shown_as_within(self) -> None:
        out = render(
            dict(status="Held", signal="Pause for human decision", reason="No limits.", findings=[])
        )
        self.assertIn("Pause for human decision. Held.", out)
        self.assertNotIn("Within", out)

    def test_unavailable_signal_falls_back_to_a_manual_check(self) -> None:
        out = render(None)
        self.assertIn("Limit check unavailable", out)
        self.assertIn("by hand", out)
        self.assertIn("Nothing is paid from here", out)


if __name__ == "__main__":
    unittest.main()
