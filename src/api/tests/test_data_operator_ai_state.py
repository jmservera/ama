"""The data-operator browser check's AI-state fixture renders the distinctions it asserts (#229).

Builds the register with the real core mixin and renders the real role-screens.js in Node.
Constructed synthetic text only: this proves neither a serving model nor browser behaviour.
"""

import json
import subprocess
import threading
import unittest
from pathlib import Path
from typing import Any

from checks import data_operator_ai_state as ai
from zava_forward.core.exception_register import ExceptionRegisterMixin

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const data = JSON.parse(process.argv[2]);
const h = (tag, attrs, ...kids) => {
  return {tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)};
};
const controller = new AbortController();
const context = vm.createContext({URLSearchParams, Intl, AbortController, Date,
  location: {hash: "#/screens?screen=data-operator&exceptions=1"}, routeController: controller,
  me: {user: {role: "Retrofit Programme Manager"}}, api: async () => data, h});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
context.__s.overview(controller.signal, [], null).then(out => console.log(JSON.stringify(out)));
"""


class Register(ExceptionRegisterMixin):  # type: ignore[misc]
    def __init__(self, records: list[dict[str, Any]]) -> None:
        self.cases: dict[str, Any] = {}
        self.data = {"recommendations": records}
        self.lock = threading.RLock()
        self.audits: list[tuple[Any, ...]] = []

    def audit(self, *args: Any) -> None:
        self.audits.append(args)


def rendered() -> tuple[dict[str, Any], str, list[str]]:
    user = {"email": ai.OPERATOR_EMAIL, "role": "Retrofit Programme Manager"}
    staff = {ai.OPERATOR_EMAIL: ("data_steward", "digital_operator")}
    contract = Register(ai.ai_records()).exception_register(user, staff)
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(contract)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    tree = json.loads(result.stdout)
    rows: list[str] = []

    def walk(node: Any) -> str:
        if isinstance(node, str):
            return node
        text = " ".join(walk(kid) for kid in node.get("kids", []))
        if node.get("tag") == "tr":
            rows.append(text)
        return text

    return contract, walk(tree), rows


class DataOperatorAiState(unittest.TestCase):
    contract: dict[str, Any]
    page: str
    rows: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.page, cls.rows = rendered()

    def row(self, record_id: str) -> str:
        found = [row for row in self.rows if record_id in row]
        self.assertEqual(len(found), 1, record_id)
        return found[0]

    def test_quarantined_and_fallback_are_distinct_rows(self) -> None:
        quarantined, fallback = self.row(ai.QUARANTINED_ID), self.row(ai.FALLBACK_ID)
        self.assertIn(ai.QUARANTINED_TEXT, quarantined)
        self.assertNotIn("Fell back", quarantined)
        self.assertIn(ai.FALLBACK_TEXT, fallback)
        self.assertNotIn("Quarantined.", fallback)

    def test_workflow_only_is_not_listed_and_is_explained(self) -> None:
        self.assertNotIn(ai.WORKFLOW_ID, self.page)
        self.assertEqual(len(self.contract["items"]), 2)

    def test_every_expected_phrase_shows_and_no_forbidden_claim_does(self) -> None:
        for phrase in ai.REGISTER_EXPECTED:
            self.assertIn(phrase, self.page, phrase)
        for phrase in ai.REGISTER_FORBIDDEN:
            self.assertNotIn(phrase, self.page, phrase)
        self.assertEqual(self.contract["banner"]["state"], "unknown")


if __name__ == "__main__":
    unittest.main()
