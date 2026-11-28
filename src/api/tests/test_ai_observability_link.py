# ruff: noqa: E501
"""Staff AI observability view: server link config and rendered view (issue 2486 goal)."""

import json
import shutil
import subprocess
import unittest
from pathlib import Path

from zava_forward.api.server import ai_observability_url

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"

NODE = r"""
const fs = require("fs"), vm = require("vm");
function el(tag, attrs, kids) { return { tag, attrs: attrs || {}, kids: kids.flat().filter((k) => k !== false && k != null) }; }
const text = (n) => typeof n === "string" ? n : [n.tag, ...n.kids.map(text)].join(" ");
const find = (n, tag, out = []) => { if (typeof n === "string") return out; if (n.tag === tag) out.push(n); n.kids.forEach((k) => find(k, tag, out)); return out; };
async function run(services, api) {
  let shown = [];
  const ctx = vm.createContext({ h: (t, a, ...k) => el(t, a, k), show: (...n) => { shown = n; },
    me: null, routeController: { signal: { aborted: false } }, api });
  ctx.me = { services };
  vm.runInContext(fs.readFileSync(process.argv[1] + "/assistants.js", "utf8").replace(/^const /gm, "var "), ctx);
  await vm.runInContext("aiObservabilityView", ctx)();
  return shown;
}
(async () => {
  const metrics = { metrics: { invocation: 7, refusal: 2, withheld: 1, validation_failure: 0, fallback: 0, human_review: 3, override: 1, tokens: 900, latency_samples: 7 }, latency_seconds_total: 4.2 };
  const out = {};
  const withUrl = await run({ assistants: true, ai_observability_url: "https://portal.azure.com/x" }, async () => metrics);
  out.withUrl = { text: withUrl.map(text).join(" "), links: withUrl.flatMap((n) => find(n, "a")).map((a) => a.attrs.href), tables: withUrl.flatMap((n) => find(n, "table")).length, caption: withUrl.flatMap((n) => find(n, "caption")).length };
  const noUrl = await run({ assistants: true }, async () => metrics);
  out.noUrl = noUrl.flatMap((n) => find(n, "a")).map((a) => a.attrs.href);
  const badUrl = await run({ assistants: true, ai_observability_url: "javascript:alert(1)" }, async () => metrics);
  out.badUrl = badUrl.flatMap((n) => find(n, "a")).map((a) => a.attrs.href);
  let called = false;
  const denied = await run({ assistants: false }, async () => { called = true; return metrics; });
  out.denied = { called, text: denied.map(text).join(" ") };
  console.log(JSON.stringify(out));
})();
"""


class AiObservabilityLinkTests(unittest.TestCase):
    def test_url_helper_accepts_only_plain_https(self) -> None:
        good = "https://portal.azure.com/#view/x"
        self.assertEqual(ai_observability_url({"ZF_AI_OBSERVABILITY_URL": f" {good} "}), good)
        for bad in (
            "",
            "http://portal.azure.com",
            "javascript:alert(1)",
            "https://u:p@portal.azure.com",
            "https://",
        ):
            with self.subTest(bad=bad):
                self.assertIsNone(ai_observability_url({"ZF_AI_OBSERVABILITY_URL": bad}))
        self.assertIsNone(ai_observability_url({}))

    def test_account_link_is_a_native_hidden_until_staff_anchor(self) -> None:
        html = (WEB / "index.html").read_text()
        self.assertIn(
            '<p id="ai-observability-entry" hidden><a id="ai-observability-link" href="#/ai-observability">AI observability</a></p>',
            html,
        )

    @unittest.skipUnless(shutil.which("node"), "node is required")
    def test_view_renders_counts_and_portal_link_only_when_set(self) -> None:
        run = subprocess.run(
            ["node", "-e", NODE, str(WEB)], capture_output=True, text=True, timeout=60, check=False
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        out = json.loads(run.stdout)
        self.assertEqual(out["withUrl"]["tables"], 1)
        self.assertEqual(out["withUrl"]["caption"], 1)
        self.assertIn("Requests stopped by the safety checks", out["withUrl"]["text"])
        self.assertIn("https://portal.azure.com/x", out["withUrl"]["links"])
        self.assertNotIn("https://portal.azure.com/x", out["noUrl"])
        self.assertEqual([h for h in out["badUrl"] if not h.startswith("#")], [])
        self.assertFalse(out["denied"]["called"])
        self.assertIn("staff roles", out["denied"]["text"])


if __name__ == "__main__":
    unittest.main()
