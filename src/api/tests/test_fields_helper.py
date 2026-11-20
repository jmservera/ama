"""The labelled-field helper: the shipped fields.js runs in a mini DOM and its wiring is checked."""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

DOM = r"""
class Text {
  constructor(data) {this.nodeType = 3; this.data = data;}
  get textContent() {return this.data;}
}
class Element {
  constructor(tag) {
    this.nodeType = 1; this.tagName = tag.toUpperCase(); this.attrs = {}; this.children = [];
  }
  append(...kids) {
    kids.flat().forEach(kid => {this.children.push(kid); kid.parentElement = this;});
  }
  setAttribute(name, value) {this.attrs[name] = String(value);}
  getAttribute(name) {return name in this.attrs ? this.attrs[name] : null;}
  hasAttribute(name) {return name in this.attrs;}
  removeAttribute(name) {delete this.attrs[name];}
  get hidden() {return this.hasAttribute("hidden");}
  set hidden(on) {if (on) this.setAttribute("hidden", ""); else this.removeAttribute("hidden");}
  set className(value) {this.setAttribute("class", value);}
  get textContent() {return this.children.map(kid => kid.textContent).join("");}
  set textContent(value) {this.children = value === "" ? [] : [new Text(String(value))];}
  all() {return this.children.filter(k => k.nodeType === 1).flatMap(k => [k, ...k.all()]);}
  addEventListener() {}
  focus() {document.activeElement = this;}
}
const document = {
  activeElement: null,
  createElement: tag => new Element(tag),
  createTextNode: text => new Text(text),
};
const byId = (root, id) => root.all().find(el => el.attrs.id === id);
const shape = node => node.nodeType === 3 ? node.data
  : {tag: node.tagName.toLowerCase(), attrs: node.attrs, children: node.children.map(shape)};
"""

FIELD_RULES = (
    ".field{margin-block:var(--sp-3)}",
    ".field>label{margin:0 0 var(--sp-1)}",
    ".field>.field-hint{margin:0 0 var(--sp-1)}",
    ".field :is(input,select,textarea):not([type=checkbox]):not([type=radio])"
    "{display:block;width:100%;max-width:36rem}",
    ".field-row{display:flex;flex-wrap:wrap;align-items:flex-end;gap:var(--sp-3)}",
    ".field-row>.field{flex:1 1 12rem;min-width:0;margin:0}",
    ".check{display:flex;flex-wrap:wrap;align-items:flex-start;gap:var(--sp-2);margin-block:var(--sp-2)}",
    ".check>label{margin:0;font-weight:400;flex:1 1 0;min-width:0}",
    ".check>input{flex:0 0 auto;margin:0}",
    ".check>.field-hint{flex-basis:100%;margin:0}",
)


def shipped_h() -> str:
    source = (WEB / "app.js").read_text()
    match = re.search(r"^function h\(.*?^\}\n", source, re.S | re.M)
    assert match is not None, "app.js no longer defines h()"
    return match.group(0)


def run(expression: str) -> Any:
    script = (
        DOM
        + shipped_h()
        + (WEB / "fields.js").read_text()
        + f"\nconsole.log(JSON.stringify({expression}));"
    )
    result = subprocess.run(["node", "-"], input=script, text=True, capture_output=True, timeout=30)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class FieldBlock(unittest.TestCase):
    def test_label_marks_required_and_optional_and_required_wins(self) -> None:
        labels = run(
            r"""(() => {
  const label = extra => Fields.fieldBlock({id: "minutes", label: "Minutes",
    control: h("input", {}), ...extra}).block.children[0].textContent;
  return [label({}), label({required: true}), label({optional: true}),
    label({required: true, optional: true})];
})()"""
        )
        self.assertEqual(
            labels, ["Minutes", "Minutes (required)", "Minutes (optional)", "Minutes (required)"]
        )

    def test_block_holds_label_hint_control_and_a_hidden_error_in_that_order(self) -> None:
        built = run(
            r"""(() => {
  const control = h("input", {type: "text"});
  const field = Fields.fieldBlock({id: "minutes", name: "minutes", label: "Minutes",
    hint: "A whole number from 1 to 600.", required: true, control});
  return {shape: shape(field.block), same: field.control === control};
})()"""
        )
        self.assertTrue(built["same"])
        self.assertEqual(
            built["shape"],
            {
                "tag": "div",
                "attrs": {"class": "field"},
                "children": [
                    {
                        "tag": "label",
                        "attrs": {"for": "minutes"},
                        "children": ["Minutes (required)"],
                    },
                    {
                        "tag": "p",
                        "attrs": {"class": "field-hint", "id": "minutes-hint"},
                        "children": ["A whole number from 1 to 600."],
                    },
                    {
                        "tag": "input",
                        "attrs": {
                            "type": "text",
                            "id": "minutes",
                            "name": "minutes",
                            "aria-describedby": "minutes-hint",
                        },
                        "children": [],
                    },
                    {
                        "tag": "p",
                        "attrs": {"class": "field-error", "id": "minutes-error", "hidden": ""},
                        "children": [],
                    },
                ],
            },
        )

    def test_without_hint_or_name_only_the_id_is_added_to_the_control(self) -> None:
        block = run(
            r"""shape(Fields.fieldBlock({id: "minutes", label: "Minutes",
  control: h("input", {})}).block)"""
        )
        self.assertEqual([child["tag"] for child in block["children"]], ["label", "input", "p"])
        self.assertEqual(block["children"][1]["attrs"], {"id": "minutes"})

    def test_described_by_keeps_existing_ids_and_never_repeats_one(self) -> None:
        described = run(
            r"""(() => {
  const merged = existing => {
    const control = h("input", {"aria-describedby": existing});
    Fields.fieldBlock({id: "minutes", label: "Minutes", hint: "Hint.", control});
    return control.getAttribute("aria-describedby");
  };
  return [merged("helper"), merged("minutes-hint helper"), merged("helper minutes-hint")];
})()"""
        )
        self.assertEqual(
            described, ["helper minutes-hint", "minutes-hint helper", "helper minutes-hint"]
        )

    def test_control_keeps_its_own_id_and_a_field_without_id_or_label_is_refused(self) -> None:
        outcome = run(
            r"""(() => {
  const refused = options => {
    try { Fields.fieldBlock(options); return "built"; } catch (error) { return error.message; }
  };
  const own = Fields.fieldBlock({label: "Minutes", control: h("input", {id: "own"})});
  return {
    labelFor: own.block.children[0].attrs.for,
    controlId: own.control.getAttribute("id"),
    noId: refused({label: "Minutes", control: h("input", {})}),
    noLabel: refused({id: "minutes", control: h("input", {})}),
  };
})()"""
        )
        self.assertEqual(outcome["labelFor"], "own")
        self.assertEqual(outcome["controlId"], "own")
        self.assertEqual(outcome["noId"], "A field needs an id and a visible label.")
        self.assertEqual(outcome["noLabel"], "A field needs an id and a visible label.")

    def test_fail_marks_the_field_and_clear_restores_it(self) -> None:
        states = run(
            r"""(() => {
  const control = h("input", {"aria-describedby": "helper"});
  const field = Fields.fieldBlock({id: "minutes", label: "Minutes", hint: "Hint.", control});
  const error = byId(field.block, "minutes-error");
  const state = () => ({hidden: error.hidden, text: error.textContent,
    invalid: control.getAttribute("aria-invalid"),
    described: control.getAttribute("aria-describedby"),
    focused: document.activeElement === control});
  const message = "Enter the minutes. Owner: you. Next action: type them, then choose Save again.";
  const seen = {start: state()};
  field.fail(message); seen.failed = state();
  field.fail(message); seen.again = state();
  field.clear(); seen.cleared = state();
  return seen;
})()"""
        )
        message = "Enter the minutes. Owner: you. Next action: type them, then choose Save again."
        failed = {
            "hidden": False,
            "text": message,
            "invalid": "true",
            "described": "helper minutes-hint minutes-error",
            "focused": True,
        }
        self.assertEqual(
            states["start"],
            {
                "hidden": True,
                "text": "",
                "invalid": None,
                "described": "helper minutes-hint",
                "focused": False,
            },
        )
        self.assertEqual(states["failed"], failed)
        self.assertEqual(states["again"], failed)
        self.assertEqual(
            states["cleared"],
            {
                "hidden": True,
                "text": "",
                "invalid": None,
                "described": "helper minutes-hint",
                "focused": True,
            },
        )

    def test_clear_drops_the_described_by_attribute_when_the_error_was_its_only_id(self) -> None:
        described = run(
            r"""(() => {
  const control = h("input", {});
  const field = Fields.fieldBlock({id: "minutes", label: "Minutes", control});
  field.clear();
  const untouched = control.hasAttribute("aria-describedby");
  field.fail("Problem. Owner: you. Next action: fix it, then choose Save again.");
  const during = control.getAttribute("aria-describedby");
  field.clear();
  return {untouched, during, after: control.hasAttribute("aria-describedby")};
})()"""
        )
        self.assertEqual(described, {"untouched": False, "during": "minutes-error", "after": False})


class CheckRow(unittest.TestCase):
    def test_box_comes_before_its_label_and_the_hint_follows_inside_the_row(self) -> None:
        built = run(
            r"""(() => {
  const box = h("input", {type: "checkbox"});
  const row = Fields.checkRow({id: "alerts", label: "Show only homes with stale sensors",
    hint: "Zoom in until homes are shown one by one.", control: box});
  const plain = Fields.checkRow({id: "plain", label: "Plain",
    control: h("input", {type: "checkbox"})});
  return {shape: shape(row.block), same: row.control === box, plain: shape(plain.block)};
})()"""
        )
        self.assertTrue(built["same"])
        self.assertEqual(
            built["shape"],
            {
                "tag": "div",
                "attrs": {"class": "check"},
                "children": [
                    {
                        "tag": "input",
                        "attrs": {
                            "type": "checkbox",
                            "id": "alerts",
                            "aria-describedby": "alerts-hint",
                        },
                        "children": [],
                    },
                    {
                        "tag": "label",
                        "attrs": {"for": "alerts"},
                        "children": ["Show only homes with stale sensors"],
                    },
                    {
                        "tag": "p",
                        "attrs": {"class": "field-hint", "id": "alerts-hint"},
                        "children": ["Zoom in until homes are shown one by one."],
                    },
                ],
            },
        )
        self.assertEqual(
            built["plain"],
            {
                "tag": "div",
                "attrs": {"class": "check"},
                "children": [
                    {"tag": "input", "attrs": {"type": "checkbox", "id": "plain"}, "children": []},
                    {"tag": "label", "attrs": {"for": "plain"}, "children": ["Plain"]},
                ],
            },
        )


class Wiring(unittest.TestCase):
    def test_index_loads_the_helper_right_after_the_async_action_helper(self) -> None:
        scripts = re.findall(r'<script src="([^"]+)"></script>', (WEB / "index.html").read_text())
        self.assertEqual(scripts[scripts.index("/async-action.js") + 1], "/fields.js")

    def test_stylesheet_carries_the_field_and_check_rules_with_tokens_only(self) -> None:
        lines = (WEB / "style.css").read_text().splitlines()
        for rule in FIELD_RULES:
            with self.subTest(rule=rule):
                self.assertIn(rule, lines)
                self.assertNotRegex(rule, r"#[0-9a-fA-F]{3,6}\b|\d\s*px")
        # The empty error hides through the hidden attribute, and hints keep their look.
        self.assertIn("[hidden]{display:none!important}", lines)
        self.assertIn(
            ".field-hint{font-size:var(--fs-sm);margin:var(--sp-1) 0 var(--sp-2);"
            "color:var(--muted)}",
            lines,
        )


if __name__ == "__main__":
    unittest.main()
