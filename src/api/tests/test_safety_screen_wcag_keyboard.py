"""Safety lead and hazard triage screens give state meaning in text and are keyboard reachable."""

import importlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from test_safety_screens import SAFE, SCRIPT, WEB, find_all, hazard, run, string_leaves
else:
    _tests_dir = str(Path(__file__).resolve().parent)
    if _tests_dir not in sys.path:
        sys.path.insert(0, _tests_dir)
    _ss = importlib.import_module("test_safety_screens")
    SAFE = _ss.SAFE
    SCRIPT = _ss.SCRIPT
    WEB = _ss.WEB
    find_all = _ss.find_all
    hazard = _ss.hazard
    run = _ss.run
    string_leaves = _ss.string_leaves

CSS = (Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/style.css").read_text()


class SafetyScreenWcagKeyboard(unittest.TestCase):
    def test_every_state_cue_is_plain_language_text(self) -> None:
        past = "2020-01-01T00:00:00+00:00"
        decided = {
            "scope": "Home",
            "case_id": "C-1",
            "status": "Released",
            "decision": {
                "at": "2026-10-31T09:00:00+00:00",
                "actor": SAFE,
                "reason": "Repair verified",
                "evidence": "External job J-9 sign-off",
            },
        }
        items = [
            hazard(response_due_at=past),
            hazard(response_due_at="2999-01-01T00:00:00+00:00"),
            hazard(
                responded_at=past, hold={"scope": "Home", "case_id": "C-1", "status": "Released"}
            ),
            hazard(
                state="Accepted",
                received_at=past,
                accepted_at=past,
                accepted_by=SAFE,
                responded_at=past,
                hold=decided,
            ),
            hazard(state="Escalated", destination=SAFE),
        ]
        for screen in run(items).values():
            text = " ".join(string_leaves(screen["tree"]))
            for phrase in (
                "Every referral, clock, and stop-work state is written as words first",
                "Action needed: Stop-work indicator: retrofit work is paused",
                "Action needed: Stop-work indicator: released",
                "Confirmed: Stop-work indicator: released",
                "Action needed: Overdue service response",
                "Waiting: Awaiting service response",
                "Confirmed: Service responded",
                "Unknown: Service response clock: no due time recorded",
                "Action needed: Escalation state: Escalated",
                "Confirmed: Escalation state: Accepted",
                "urgency: Urgent",
                "State: Recorded",
                "State: Not recorded",
            ):
                self.assertIn(phrase, text)
            summary = " ".join(string_leaves(screen["summary"]))
            for summary_phrase in (
                "Every referral, clock, and stop-work state is written as words first",
                "Action needed: Escalation state: Sent",
                "Confirmed: Escalation state: Accepted",
                "Action needed: Stop-work indicator: Active (retrofit work paused)",
                (
                    "Confirmed: Stop-work indicator: Released "
                    "(decision recorded; open the home to inspect)"
                ),
                (
                    "Action needed: Stop-work indicator: Released. "
                    "Release decision evidence: open the home"
                ),
                "Unknown: Unavailable. Open the home to check.",
                "Unknown: Unknown. Hazard list not supplied. Open the home to check.",
                (
                    "Action needed: Mismatch. The list flags a hazard "
                    "but the case returns none. Open the home to check."
                ),
            ):
                self.assertIn(summary_phrase, summary)

    def test_unreadable_stamps_and_prototype_keys_render_unknown_text(self) -> None:
        tricky = hazard(
            state="toString",
            sent_at="not-a-date",
            responded_at="bad-stamp",
            response_due_at=None,
            clock_text="",
            escalation_clock="",
            hold={"scope": "Home", "case_id": "C-1", "status": "constructor"},
        )
        bad_due = hazard(responded_at=None, response_due_at="bad-due")
        for screen in run([tricky, bad_due]).values():
            text = " ".join(string_leaves(screen["tree"]))
            self.assertNotIn("function ", text)
            for phrase in (
                "Unknown: Escalation state: toString",
                "Unknown: Stop-work indicator: pause status constructor",
                "Unknown: Timestamp not readable (not-a-date)",
                "Unknown: Service responded (bad-stamp; timestamp not readable)",
                "Unknown: Service response clock: due time not readable (bad-due)",
                "Unknown: Clock not supplied",
            ):
                self.assertIn(phrase, text)
            summary = " ".join(string_leaves(screen["summary"]))
            self.assertIn("Unknown: Stop-work indicator: constructor", summary)

    def test_sections_are_headed_landmarks_with_keyboard_jump_links(self) -> None:
        for screen in run([hazard()]).values():
            for view, expected_count in ((screen["tree"], 4), (screen["summary"], 1)):
                (nav,) = find_all(view, "nav")
                self.assertEqual(nav["attrs"]["aria-label"], "Sections on this screen")
                self.assertEqual(nav["attrs"]["class"], "screen-links")
                links = find_all(nav, "a")
                self.assertEqual(len(links), expected_count)
                sections = find_all(view, "section")
                self.assertEqual(len(sections), expected_count)
                heading_ids: list[str] = []
                for section in sections:
                    (heading,) = [k for k in section["kids"] if k.get("tag") == "h2"]
                    heading_id = str(heading["attrs"]["id"])
                    heading_ids.append(heading_id)
                    self.assertTrue(section["attrs"]["id"])
                    self.assertEqual(section["attrs"]["aria-labelledby"], heading_id)
                    self.assertEqual(heading["attrs"]["tabindex"], -1)
                for link, heading_id in zip(links, heading_ids, strict=True):
                    self.assertNotIn("onclick", link["attrs"])
                    self.assertEqual(link["attrs"]["href"], f"#{heading_id}")
                    self.assertEqual(link["attrs"]["data-jump"], heading_id)
                    self.assertEqual(link["attrs"]["data-jump-target"], heading_id)
                self.assertEqual(find_all(view, "button"), [])

    def test_focus_indicator_is_visible_and_skip_link_exists(self) -> None:
        self.assertRegex(CSS, r"(?m)^:focus-visible\{outline:")
        self.assertNotRegex(CSS, r":focus(-visible)?\s*\{[^}]*outline:\s*(none|0)\b")
        index = (
            Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/index.html"
        ).read_text()
        self.assertTrue(re.search(r'class="skip-link" href="#app"', index))

    def test_css_enforces_link_underlines_target_height_and_flag_borders(self) -> None:
        link_match = re.search(r"(?m)^\.screen-links a\s*\{([^}]*)\}", CSS)
        assert link_match is not None
        link_rule = link_match.group(1)
        self.assertIn("min-height: 2.5rem", link_rule)
        self.assertIn("text-decoration: underline", link_rule)
        self.assertNotIn("font-weight", link_rule)
        current_match = re.search(
            r'(?m)^\.screen-links a\[aria-current="page"\]\s*\{([^}]*)\}', CSS
        )
        assert current_match is not None
        self.assertIn("font-weight: 600", current_match.group(1))
        self.assertIn("text-decoration-thickness: .2em", current_match.group(1))
        flag_match = re.search(r"(?m)^\.flag\{([^}]*)\}", CSS)
        danger_match = re.search(r"(?m)^\.flag\.danger\{([^}]*)\}", CSS)
        assert flag_match is not None and danger_match is not None
        self.assertIn("border:1px solid var(--soft-line)", flag_match.group(1))
        self.assertIn("border-color:var(--warn)", danger_match.group(1))

    def test_status_is_not_colour_only(self) -> None:
        payload = json.dumps(run([hazard()])["safety-lead"]["tree"])
        self.assertNotRegex(payload, r"\"style\"|\"color\"")


if __name__ == "__main__":
    unittest.main()


TOP_LEVEL = re.compile(
    r"^(?:async\s+)?(?:const|let|var|function\*?|class)\s+([A-Za-z_$][\w$]*)", re.M
)

JUMP_SCRIPT = (
    "let clickListener = null;\n"
    "const target = {focused: 0, scrolled: 0, focus() { this.focused++; },\n"
    '  scrollIntoView(o) { this.scrolled += o.block === "start" ? 1 : 0; }};\n'
    + SCRIPT.split("(async () => {")[0].replace(
        "api: async () => ({}),",
        """document: {
    addEventListener(type, fn) { if (type === "click") clickListener = fn; },
    getElementById: (id) => id === "hazard-queue-heading" ? target : null
  },
  api: async () => ({}),""",
    )
    + r"""
const find = (n, tag, out = []) => {
  if (n && n.tag === tag) out.push(n);
  for (const k of (n && n.kids) || []) find(k, tag, out);
  return out;
};
(async () => {
  const tree = await context.__r.get("hazard-triage").render({id: "C-1", hazards: []});
  const links = find(tree, "a");
  let prevented = 0;
  const fire = (link) => clickListener({
    target: {
      closest: (sel) => sel === "a[data-jump]" ? {getAttribute: (k) => link.attrs[k]} : null
    },
    preventDefault() { prevented++; }
  });
  fire(links[1]);
  context.document.getElementById = () => null;
  fire(links[0]);
  context.document.getElementById = () => ({});
  fire(links[2]);
  clickListener({target: {closest: () => null}, preventDefault() { prevented++; }});
  console.log(JSON.stringify({prevented, focused: target.focused, scrolled: target.scrolled}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""
)

ALIAS_SCRIPT = r"""
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const web = process.argv[1];
const appSrc = fs.readFileSync(path.join(web, "app.js"), "utf8");
const start = appSrc.indexOf("function missingWorkspaceScripts");
const end = appSrc.indexOf("async function requireWorkspaceScripts");
const loaderSlice = appSrc.slice(start, end);

function checkLoader(role, hash) {
  const ctx = {
    me: {user: {role}},
    AsyncAction: {handler() {}, run() {}, feedback() {}},
    employeeChat: {},
    chatCasePanel() {}
  };
  vm.runInNewContext(loaderSlice, ctx);
  return ctx.missingWorkspaceScripts(hash, false);
}

async function runAlias(role, hash) {
  const rendered = [];
  const h = (tag, attrs = {}, ...kids) => ({
    tag, attrs,
    kids: kids.flat(Infinity).filter((k) => k !== null && k !== undefined && k !== false)
  });
  const ctx = vm.createContext({
    URLSearchParams, Intl, AbortController, Object, Promise, Date, Array, Number, Boolean,
    Math, JSON, encodeURIComponent,
    location: {hash},
    me: {user: {role}},
    routeController: new AbortController(),
    document: {addEventListener() {}, getElementById: () => null},
    workspaceStatus: {},
    h,
    show: (...nodes) => rendered.push(nodes),
    api: async (url) => url.startsWith("/api/cases?")
      ? {items: [{id: "C-1", address: "1 North St", stage: "Survey", hazard: true}], total: 1}
      : {
          id: "C-1",
          hazards: [{
            category: "Damp", priority: "Urgent", state: "Sent",
            sent_at: "2026-10-30T10:00:00+00:00"
          }]
        }
  });
  vm.runInContext(fs.readFileSync(path.join(web, "role-screens.js"), "utf8"), ctx);
  await ctx.roleScreensView();
  return JSON.stringify(rendered);
}

(async () => {
  const out = {
    loaderSafety: checkLoader("Building Safety Liaison", "#/role/building_safety_lead"),
    loaderRepairs: checkLoader("Contractor", "#/role/repairs"),
    safetyAllowed: await runAlias("Building Safety Liaison", "#/role/building_safety_lead"),
    safetyBlocked: await runAlias("Contractor", "#/role/building_safety_lead"),
    repairsAllowed: await runAlias("Retrofit Coordinator", "#/role/repairs"),
    repairsBlocked: await runAlias("Building Safety Liaison", "#/role/repairs")
  };
  console.log(JSON.stringify(out));
})().catch((e) => { console.error(e); process.exitCode = 1; });
"""


class RoleScreensGlobalScope(unittest.TestCase):
    def test_no_top_level_identifier_collides_with_app_js(self) -> None:
        names = {
            f: set(TOP_LEVEL.findall((WEB / f).read_text())) for f in ("role-screens.js", "app.js")
        }
        self.assertEqual(names["role-screens.js"] & names["app.js"], set())

    def test_jump_button_moves_focus_and_tolerates_missing_target(self) -> None:
        result = subprocess.run(
            ["node", "-e", JUMP_SCRIPT, str(WEB), "[]"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"prevented": 3, "focused": 1, "scrolled": 1})

    def test_role_hash_aliases_load_scripts_render_views_and_block_unauthorised_roles(self) -> None:
        result = subprocess.run(
            ["node", "-e", ALIAS_SCRIPT, str(WEB)], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads(result.stdout)
        self.assertEqual(out["loaderSafety"], ["/role-screens.js"])
        self.assertEqual(out["loaderRepairs"], ["/role-screens.js"])
        self.assertIn("Building safety referral queue", out["safetyAllowed"])
        self.assertEqual(out["safetyAllowed"].count('"id":"hazard-page-summary-heading"'), 1)
        self.assertIn('"aria-current":"page"', out["safetyAllowed"])
        self.assertIn("screen=safety-lead&case=C-1", out["safetyAllowed"])
        self.assertIn("Screen unavailable", out["safetyBlocked"])
        self.assertIn("Repairs and hazard triage", out["repairsAllowed"])
        self.assertIn("screen=hazard-triage&case=C-1", out["repairsAllowed"])
        self.assertIn("Screen unavailable", out["repairsBlocked"])
