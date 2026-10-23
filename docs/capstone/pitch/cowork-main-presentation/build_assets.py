#!/usr/bin/env python3
"""Build portable slide notes and 16:9 Excalidraw/SVG assets from the brief."""

import base64
import hashlib
import html
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1600, 900
INK, GREEN, BLUE, PURPLE = "#173f35", "#e8f1ed", "#e8f2fb", "#f0ebfa"
AMBER, PAPER, MUTED = "#fff1d6", "#faf9f6", "#50655e"


class Drawing:
    def __init__(self, name, title, subtitle):
        self.name = name
        self.elements = []
        self.files = {}
        self.svg = []
        self.count = 0
        self.rect(0, 0, WIDTH, HEIGHT, PAPER, PAPER, locked=True)
        self.text(64, 42, title, 37, width=1472)
        self.text(64, 102, subtitle, 21, MUTED, width=1472)

    def element(self, kind, x, y, w, h, **extra):
        self.count += 1
        ident = f"{self.name}-{self.count:03}"
        element = {
            "id": ident, "type": kind, "x": x, "y": y, "width": w,
            "height": h, "angle": 0, "strokeColor": INK,
            "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0,
            "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": self.count * 7919, "version": 1,
            "versionNonce": self.count * 3571, "isDeleted": False,
            "boundElements": None, "updated": 1792710000000,
            "link": None, "locked": False,
        }
        element.update(extra)
        self.elements.append(element)
        return ident

    def rect(self, x, y, w, h, fill, stroke=INK, dashed=False, locked=False):
        self.element("rectangle", x, y, w, h, backgroundColor=fill,
                     strokeColor=stroke, strokeStyle="dashed" if dashed else "solid",
                     locked=locked, roundness={"type": 3})
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        self.svg.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')

    def text(self, x, y, value, size=24, color=INK, width=1450):
        lines = value.splitlines()
        self.element("text", x, y, width, len(lines) * size * 1.25,
                     strokeColor=color, text=value, originalText=value,
                     fontSize=size, fontFamily=2, textAlign="left",
                     verticalAlign="top", containerId=None, lineHeight=1.25,
                     autoResize=False)
        spans = "".join(
            f'<tspan x="{x}" dy="{0 if i == 0 else size * 1.25}">'
            f'{html.escape(line)}</tspan>' for i, line in enumerate(lines))
        self.svg.append(
            f'<text x="{x}" y="{y + size}" font-family="Arial, sans-serif" '
            f'font-size="{size}" fill="{color}">{spans}</text>')

    def icon(self, x, y, name, size=46):
        raw = (ROOT / "assets" / "azure" / f"{name}.svg").read_bytes()
        viewbox = ET.fromstring(raw).get("viewBox", "0 0 18 18").split()
        natural_w, natural_h = map(float, viewbox[2:])
        width = size * min(1, natural_w / natural_h)
        height = size * min(1, natural_h / natural_w)
        file_id = hashlib.sha256(raw).hexdigest()
        uri = "data:image/svg+xml;base64," + base64.b64encode(raw).decode()
        self.files[file_id] = {
            "id": file_id, "mimeType": "image/svg+xml", "dataURL": uri,
            "created": 1792710000000, "lastRetrieved": 1792710000000,
        }
        self.element("image", x, y, width, height, fileId=file_id,
                     status="saved", scale=[1, 1], crop=None)
        self.svg.append(
            f'<image x="{x}" y="{y}" width="{width}" height="{height}" '
            f'preserveAspectRatio="xMidYMid meet" href="{uri}"/>')

    def card(self, x, y, w, h, title, body, icon=None, fill=GREEN, dashed=False):
        first = len(self.elements)
        self.rect(x, y, w, h, fill, dashed=dashed)
        if icon:
            self.icon(x + 20, y + 22, icon)
        self.text(x + (80 if icon else 22), y + 24, title, 26,
                  width=w - (100 if icon else 44))
        self.text(x + 22, y + 84, body, 23, width=w - 44)
        group = f"{self.name}-group-{first}"
        for item in self.elements[first:]:
            item["groupIds"] = [group]

    def arrow(self, x, y, dx, dy=0, dashed=False):
        self.element(
            "arrow", min(x, x + dx), min(y, y + dy), abs(dx), abs(dy),
            points=[[max(0, -dx), max(0, -dy)], [max(0, dx), max(0, dy)]],
            lastCommittedPoint=None, startBinding=None, endBinding=None,
            startArrowhead=None, endArrowhead="arrow",
            strokeStyle="dashed" if dashed else "solid", elbowed=False)
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        self.svg.append(
            f'<path d="M{x},{y} l{dx},{dy}" fill="none" stroke="{INK}" '
            f'stroke-width="3" marker-end="url(#arrow)"{dash}/>')

    def footer(self, text):
        self.text(64, 817, text, 20, MUTED, width=1472)
        self.text(64, 852, "SOURCE-BASED EXERCISE VIEW | 23 OCT 2026 | NOT LIVE INVENTORY", 17, MUTED)

    def save(self):
        out = ROOT / "diagrams"
        out.mkdir(exist_ok=True)
        data = {
            "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
            "elements": self.elements, "files": self.files,
            "appState": {"viewBackgroundColor": PAPER, "gridSize": None},
        }
        (out / f"{self.name}.excalidraw").write_text(json.dumps(data, indent=2) + "\n")
        defs = ('<defs><marker id="arrow" markerWidth="10" markerHeight="10" '
                'refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
                f'<path d="M0,0 L0,6 L9,3 z" fill="{INK}"/></marker></defs>')
        (out / f"{self.name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
            f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">'
            + defs + "".join(self.svg) + "</svg>\n")


def diagrams():
    d = Drawing("01-the-idea", "One programme. One evidence trail. People decide.",
                "Start here: this is an operating-model view, not a network boundary.")
    d.card(64, 240, 340, 310, "People", "Residents choose.\nStaff own the case.\nProfessionals approve.")
    d.arrow(410, 390, 70)
    d.card(490, 240, 555, 310, "Controlled workbench", "Workflow keeps the commitments.\nRules enforce the boundaries.\nAI prepares source-bound help.", "aca")
    d.arrow(1055, 390, 70)
    d.card(1136, 240, 400, 310, "Retained evidence", "Azure SQL: case + audit\nBlob: evidence files\nUnknown stays unknown.", "sql", BLUE)
    d.card(490, 610, 1046, 145, "Bounded AI, never delegated accountability",
           "Generative drafts and typed decisions enter a review queue, not an approval.", "openai", PURPLE)
    d.footer("Solid = logical workflow | AI output is unreviewed | Value remains a measured hypothesis")
    d.save()

    d = Drawing("02-ai-placement", "Choose the smallest tool that earns its place.",
                "Task routing is application policy. Decision 1 is not the deterministic workflow engine.")
    for x, title, body, icon, fill in [
        (64, "Rules / no AI", "Known policy + arithmetic\nEligibility and freshness\nConsent / release gates", "aca", GREEN),
        (566, "Decision model", "Supplied candidate scoring\nForm / support screening\nAbstain when uncertain", None, BLUE),
        (1068, "Generative AI", "Explain permitted evidence\nDraft a cited narrative\nHuman verifies meaning", "openai", PURPLE),
    ]:
        d.card(x, 220, 468, 320, title, body, icon, fill)
    for x in (298, 800, 1302):
        d.arrow(x, 553, 0, 65)
    d.card(64, 635, 1472, 135, "One shared boundary: a proposal is not permission",
           "Review current evidence and authority. Retain a manual route. Count review effort, latency and full cost.")
    d.footer("Decision-model cost/latency advantage is a hypothesis until paired tests pass | Sources: E04, E05")
    d.save()

    d = Drawing("03-runtime", "One API coordinates the work; models do not own state.",
                "Current source contracts; historical deployment proof is not current end-to-end acceptance.")
    d.card(64, 198, 390, 195, "Staff browser", "Resident-assisted routes\nNo mandatory resident portal")
    d.arrow(464, 285, 66)
    d.card(540, 198, 520, 195, "Container Apps API", "Permissions + workflow\nFive bounded assistants", "aca")
    d.arrow(1070, 285, 65)
    d.card(1145, 198, 391, 195, "SQL state", "Cases, proposals, audit\nVersion-bound review", "sql", BLUE)
    d.card(64, 480, 390, 235, "Entra sign-in", "EasyAuth identity\nAPI rechecks role + scope\nIdentity is not delegation.", "entra", BLUE)
    d.arrow(454, 565, 86, -180, dashed=True)
    d.card(540, 480, 520, 235, "Scoped model call", "Azure OpenAI: draft + usage\nDecision 1: gated candidate path\nValidate before storing proposal", "foundry", PURPLE)
    d.arrow(800, 405, 0, 62, dashed=True)
    d.card(1145, 480, 391, 235, "Evidence files", "Azure Blob bytes\nSQL references + hashes\nRestore proof is separate.", "blob", BLUE)
    d.arrow(1065, 405, 70, 65, dashed=True)
    d.footer("Solid = application/state relationship | Dashed = configured or gated path, not fresh deployment proof")
    d.save()

    d = Drawing("04-controlled-ai-flow", "The model prepares. The system checks. A person decides.",
                "A guarded request/response flow, not an autonomous agent-to-agent conversation.")
    cards = [
        (64, "1. Capture", "Role + case scope\nPermitted evidence\nSource/version IDs", GREEN),
        (440, "2. Call", "Bounded task\nModel + usage\nNo database lock", PURPLE),
        (816, "3. Validate", "Schema + citations\nStale/error = stop\nStore as unreviewed", BLUE),
        (1192, "4. Review", "Human checks source\nCurrent permissions\nSeparate domain action", GREEN),
    ]
    for x, title, body, fill in cards:
        d.card(x, 245, 344, 300, title, body, fill=fill)
    for x in (410, 786, 1162):
        d.arrow(x, 385, 20)
    d.card(64, 628, 1472, 135, "Failure does not become approval",
           "Unknown, stale, disabled, exhausted allowance or unavailable model -> owned manual work; hazards bypass AI.", fill=AMBER)
    d.footer("Citation presence is not semantic truth | Proposal review never substitutes for consent, QA or Finance")
    d.save()

    d = Drawing("05-operations", "Design for failure before asking for operational trust.",
                "Configured/source architecture. No claim of tested whole-system recovery or production readiness.")
    d.card(64, 200, 460, 245, "Access + secrets", "Entra and managed identities\nKey Vault secret references\nPrivate backing services", "vault", BLUE)
    d.card(570, 200, 460, 245, "Runtime + releases", "Container Apps / pinned images\nRegistry and CI checks\nControlled rollout + rollback", "aca", GREEN)
    d.card(1076, 200, 460, 245, "Observe + budget", "Monitor / Log Analytics\nScoped allowance + usage\nBudget alert is not a stop.", "monitor", BLUE)
    d.card(64, 520, 1472, 250, "Evidence required before expansion",
           "Genuine staff sign-in + role denial | Azure SQL persistence | Bounded real-model result\nRestore and recovery drill | Human task/comprehension checks | Current cost + processing terms\nKeep manual and safety routes independent; do not relax private controls to rescue a demo.", fill=AMBER)
    d.footer("Detailed network settings belong in the runbook | No live endpoints, credentials or private roster in this pack")
    d.save()

    d = Drawing("06-sensor-target", "Sensors raise a review signal, never a safety verdict.",
                "Accepted design direction, not a completed live telemetry path. Every dashed step needs its own evidence.")
    for x, title, body, icon in [
        (64, "Device / simulator", "Distinct identity\nLabel synthetic input\nStable reading ID", None),
        (440, "Azure IoT Hub", "Basic for exercise\nDevice-to-cloud only\nCredential owner needed", "iot"),
        (816, "API + SQL", "Validate mapping/time\nIdempotent append\nOwned DQ exceptions", "sql"),
        (1192, "Human review", "Deterministic signal\nNo diagnosis / repriority\nMissing = insufficient", None),
    ]:
        d.card(x, 250, 344, 310, title, body, icon, AMBER, dashed=True)
    for x in (410, 786, 1162):
        d.arrow(x, 405, 20, dashed=True)
    d.card(64, 635, 1472, 130, "Independent safety route",
           "A resident report goes directly to human hazard handling. Telemetry and AI never delay or suppress it.")
    d.footer("Local offline consumer evidence != live Hub/SQL/Azure acceptance | Dashed = target, not live transport")
    d.save()

    d = Drawing("07-tokenomics", "Count accepted outcomes above a quality floor.",
                "Tokenomics: measured usage is one input. No price or accepted-outcome unit cost is established.")
    d.card(64, 215, 460, 305, "Observe", "6,884 tokens / five runs\nHistorical operator exercise\nNo human acceptance", "openai", PURPLE)
    d.arrow(535, 365, 25)
    d.card(570, 215, 460, 305, "Account for total cost", "Inference + hosting allocation\nHuman review + correction\nAssurance + support", "cost", BLUE)
    d.arrow(1040, 365, 25)
    d.card(1076, 215, 460, 305, "Divide by accepted work", "Agreed quality floor\nAccepted-proposal count\nCurrent unit cost: unknown", fill=AMBER)
    d.card(64, 610, 712, 155, "Existing bounded path",
           "Finite calls / tokens / expiry\nPartial usage capture; not a money cap.", fill=GREEN)
    d.card(808, 610, 728, 155, "Proposed, not tested",
           "Complete metering + currency/task budgets\nPer-request call and depth limits.", fill=AMBER, dashed=True)
    d.footer("No savings, payback or currency/unit claim | Keep or revert one measured lever | Source: E19")
    d.save()


def write_notes(data):
    lines = [
        "---", "title: Zava Forward Main Presentation Script",
        "description: Timed executive script and interruption cues generated from slides.json",
        "ms.date: 2026-10-23", "ms.topic: reference", "---", "",
        "## Timing contract", "",
        "24 minutes planned narration + 6 minutes discussion = 30 minutes presentation. "
        "The separate demo is 10 minutes. S18 is the short close after the demo; "
        "its 30 seconds are already in the presentation allocation. Backup slides are not extra scheduled content.",
        "", "This is a rehearsal script, not an observed delivery or verified timing result.", "",
    ]
    clock = 0
    for slide in data["main"]:
        end = clock + slide["seconds"]
        lines += [
            f'## {slide["id"]}: {slide["title"]}', "",
            f'Planned narration {clock // 60:02}:{clock % 60:02} to '
            f'{end // 60:02}:{end % 60:02}; {slide["seconds"]} seconds. '
            "Discussion stops the narration clock but consumes the six-minute reserve.", "",
            f'### On-slide copy', "", *[f'* {x}' for x in slide["on_slide"]], "",
            "### Say", "", slide["notes"], "",
            "### Show and deliver", "", slide["visual"], "",
            "### Interruption and return", "", slide["interrupt"], "",
            "Return: " + slide["return"], "",
            "Evidence: " + ", ".join(slide["sources"]), "",
        ]
        clock = end
    assert clock == 1440, f"Expected 24-minute script, got {clock}"
    (ROOT / "speaker-script.md").write_text("\n".join(lines))
    lines = [
        "---", "title: CXO Backup Slides and Questions",
        "description: Ready-to-build question-led appendix with direct answers, limits and return routes",
        "ms.date: 2026-10-23", "ms.topic: reference", "---", "",
        "## How to use", "",
        "Show only the requested answer. State the answer first, then its strongest evidence "
        "and limitation. Return to the named main slide. These are anticipated questions, "
        "not a transcript of a customer meeting.", "",
    ]
    for slide in data["backup"]:
        lines += [
            f'## {slide["id"]}: {slide["question"]}', "",
            "Audience: " + slide["audience"] + ". Return to " + slide["return"] + ".", "",
            "### On-slide copy", "", *[f'* {x}' for x in slide["on_slide"]], "",
            "### Answer", "", slide["answer"], "",
            "### Visual", "", slide["visual"], "",
            "Evidence: " + ", ".join(slide["sources"]), "",
        ]
    (ROOT / "backup-slides.md").write_text("\n".join(lines))


def project_view():
    snapshot = json.loads((ROOT / "evidence" / "project-snapshot.json").read_text())
    items = snapshot["items"]
    types = Counter(
        next((label for label in ("epic", "feature", "story")
              if label in (item.get("labels") or [])), "unclassified")
        for item in items)
    statuses = Counter(item.get("status", "Unknown") for item in items)
    columns = []
    for status in ("Todo", "In Progress", "Done"):
        selected = [item for item in items if item.get("status") == status]
        cards = []
        for item in selected[:4]:
            kind = next((label for label in ("epic", "feature", "story")
                         if label in (item.get("labels") or [])), "other")
            cards.append(
                f'<article><small>#{item["number"]} / {kind}</small>'
                f'<p>{html.escape(item["title"])}</p></article>')
        columns.append(
            f'<section><h2>{status} <span>{statuses[status]}</span></h2>'
            + "".join(cards)
            + f'<p class="more">Showing 4 of {len(selected)} items</p></section>')
    page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>AMA Plan: API-derived board snapshot</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;padding:44px 60px;
background:{PAPER};color:{INK};font-family:Arial,sans-serif}}
.eyebrow{{font-size:17px;letter-spacing:2px}}h1{{font-size:42px;margin:12px 0}}
.sub{{font-size:21px;margin:12px 0}}.metrics{{display:flex;gap:54px;margin:26px 0}}
.metrics b{{font-size:43px;display:block}}.metrics span{{font-size:19px}}
main{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
section{{background:#eef2ef;padding:18px;border:1px solid #c4d1cb;border-radius:12px}}
h2{{font-size:24px;margin:0 0 12px}}h2 span{{float:right}}
article{{height:86px;background:white;border:1px solid #d6dfda;border-radius:8px;
padding:10px 14px;margin:10px 0}}small{{font-size:15px;color:{MUTED}}}
article p{{font-size:18px;line-height:1.1;margin:6px 0 0}}
.more,.foot{{font-size:17px;color:{MUTED}}}.foot{{line-height:1.4;margin-top:20px}}
</style>
<div class="eyebrow">AMA PLAN / PRIVATE GITHUB PROJECT 7 / API-DERIVED VISUAL</div>
<h1>From requirements to a reviewable delivery backlog.</h1>
<p class="sub">BRD + PRD + ADRs -> epics, features and user stories -> bounded implementation and review</p>
<div class="metrics"><div><b>{len(items)}</b><span>current board items</span></div>
<div><b>{types['epic']}</b><span>epic-labelled</span></div>
<div><b>{types['feature']}</b><span>feature-labelled</span></div>
<div><b>{types['story']}</b><span>story-labelled</span></div>
<div><b>{types['unclassified']}</b><span>other / unclassified</span></div></div>
<main>{''.join(columns)}</main>
<p class="foot">Retrieved {html.escape(snapshot['retrieved_at'])}.
Board originated 15 Oct 2026; excludes agentic-workflows at generation, includes open and closed issues.<br>
Current status is not accepted delivery. This is a rendered API projection, NOT a screenshot of GitHub's website.
Historical &quot;around 180&quot; is an approximate owner recollection, not an exact creation count.</p>
</html>
"""
    (ROOT / "evidence" / "project-snapshot.html").write_text(page)


def check(data):
    assert len({s["id"] for s in data["main"] + data["backup"]}) == (
        len(data["main"]) + len(data["backup"]))
    known = set(json.loads((ROOT / "evidence" / "sources.json").read_text()))
    for slide in data["main"] + data["backup"]:
        assert set(slide["sources"]) <= known, slide["id"]
    for path in sorted((ROOT / "diagrams").glob("*.excalidraw")):
        drawing = json.loads(path.read_text())
        ids = {e["id"] for e in drawing["elements"]}
        assert len(ids) == len(drawing["elements"])
        for e in drawing["elements"]:
            assert e["width"] >= 0 and e["height"] >= 0
            assert 0 <= e["x"] <= WIDTH - e["width"], (path.name, e["id"], "x")
            assert 0 <= e["y"] <= HEIGHT - e["height"], (path.name, e["id"], "y")
            if e["type"] == "image":
                assert e["fileId"] in drawing["files"]
            if e["type"] == "text":
                assert e["fontSize"] >= 17
        assert len(drawing["files"]) >= 1 or path.stem == "04-controlled-ai-flow" or path.stem == "06-sensor-target"
    print(f'Checked {len(data["main"])} main slides, {len(data["backup"])} backups, '
          "24-minute narration and seven 1600x900 diagrams.")


if __name__ == "__main__":
    content = json.loads((ROOT / "slides.json").read_text())
    diagrams()
    write_notes(content)
    project_view()
    check(content)
