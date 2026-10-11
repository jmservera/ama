"""Author the iteration-3 architecture and day-in-the-life slides, then renumber footers."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent / "content"
FOREST, SAGE, CREAM, GOLD, INK, MUTED = "#173F35", "#D5E2D4", "#F7F2E7", "#E5B96A", "#183A31", "#446056"


def tb(top, left, width, height, text, size, color=INK, bold=False, font="Aptos"):
    return {
        "type": "textbox", "left": left, "top": top, "width": width, "height": height, "text": text,
        "font": font, "font_size": size, "font_color": color, "font_bold": bold,
        "margin_left": 0, "margin_right": 0, "margin_top": 0, "margin_bottom": 0, "word_wrap": True,
    }


def card(left, top, width, height, text, fill, size=15, dark=False, mv=0.08):
    return {
        "type": "shape", "shape": "rounded_rectangle", "left": round(left, 2), "top": round(top, 2),
        "width": round(width, 2), "height": round(height, 2), "fill": fill, "text": text,
        "text_font": "Aptos", "text_size": size, "text_color": CREAM if dark else INK, "text_bold": False,
        "alignment": "left", "vertical_anchor": "middle", "margin_left": 0.2, "margin_right": 0.2,
        "margin_top": mv, "margin_bottom": mv, "auto_size": "none", "line_spacing": 1.05,
    }


def chevron(left, top):
    return {"type": "shape", "shape": "chevron", "left": left, "top": top, "width": 0.4, "height": 0.45, "fill": GOLD}


def frame(num, kicker, title, footer):
    return [
        tb(0.6, 0.65, 12, 0.3, kicker, 11, MUTED, True),
        tb(1.22, 0.65, 12, 1.0, title, 38, INK, True, "Aptos Display"),
        tb(6.7, 0.65, 12, 0.28, f"{num:02d}  /  PROPER WARM     \u2022     {footer}", 11),
    ]


def write(num, title, elements, notes):
    d = ROOT / f"slide-{num:03d}"
    d.mkdir(exist_ok=True)
    doc = {"slide": num, "title": title, "section": "Main council pitch", "layout": "blank",
           "background": {"fill": CREAM}, "elements": elements, "speaker_notes": notes}
    (d / "content.yaml").write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")


EVID_ARCH = """Evidence:
docs/prds/proper-warm-retrofit-programme-demonstrator.md - front matter; Executive Summary; CON-009/AC-057 (v0.13.0 candidate 2026-10-11)
docs/adrs/0001-azure-architecture.md - Exercise Applicability (2026-10-11); Decisions; Hybrid M365 and Excel transition (proposed)
docs/adrs/0002-pilot-readiness-architecture.md - Exercise Applicability (2026-10-11); Decisions (proposed readiness design)"""

# Slide 5: system landscape
users = ["Programme + retrofit coordinators", "Surveyors, assessors + installers", "Residents + contractors\n(controlled touchpoints)", "Finance, quality + managers"]
sources = ["Excel workbooks\n(validated one-way import)", "Housing, asset + stock data", "Surveys, photos + evidence", "Funding + grant rules"]
els = frame(5, "WHAT WE BUILD \u2022 SYSTEM LANDSCAPE \u2022 PROPOSED, NOT DEPLOYED",
            "One workbench, one shared case, every role",
            "TARGET LANDSCAPE \u2022 PROPOSED DESIGN \u2022 E07/E08/E09")
els += [tb(2.55, 0.65, 3.3, 0.25, "WHO USES IT", 11, MUTED, True), tb(2.55, 9.15, 3.3, 0.25, "WHERE THE FACTS COME FROM", 11, MUTED, True),
        tb(2.55, 4.55, 4.0, 0.25, "WHAT WE ARE BUILDING", 11, MUTED, True)]
for i, (u, s) in enumerate(zip(users, sources)):
    top = 3.1 + i * 0.8
    els.append(card(0.65, top, 3.3, 0.66, u, SAGE, 14))
    els.append(card(9.15, top, 3.3, 0.66, s, SAGE, 14))
els.append(card(4.55, 3.1, 4.0, 3.06,
                "PROPER WARM RETROFIT WORKBENCH\n\nOne case per home or work package\nOwner, next action, blocker\nEvidence, approvals, audit\nBounded AI drafts; people decide",
                FOREST, 15, True, 0.14))
els += [chevron(4.05, 4.35), chevron(8.65, 4.35)]
write(5, "One workbench, one shared case, every role", els,
      f"""This is the whole product on one page. On the left are the people who touch a retrofit: coordinators, surveyors and installers, finance and quality managers, and residents and contractors through controlled touchpoints. On the right is where the facts come from today: Excel workbooks, housing and stock data, surveys and evidence, and funding rules.
In the middle is what we build: one workbench with one linked case per home or work package. Everyone sees the same owner, next action and blocker, and the evidence behind a decision.
It sits beside existing sources and reuses their data through a validated one-way import. It does not replace every system, and it does not give residents or contractors open access. Speed and experience gains are mechanisms to test, not measured results.

{EVID_ARCH}""")

# Slide 7: layered architecture
layers = [
    ("1  EXPERIENCE", "Role queues, case view and controlled resident touchpoints", SAGE, False),
    ("2  WORKFLOW + RULES", "Deterministic ranking, routing, gates and blockers", SAGE, False),
    ("3  CONTROLLED API", "Identity, case-level access, approvals and audit", SAGE, False),
    ("4  CASE + EVIDENCE", "Azure SQL case state, versioned Blob evidence, Excel import", SAGE, False),
    ("BOUNDED AI", "Permitted inputs only; cited draft or flag; no write credentials", GOLD, False),
]
els = frame(7, "WHAT WE BUILD \u2022 LAYERED ARCHITECTURE \u2022 PROPOSED, NOT DEPLOYED",
            "Four layers keep speed, control and AI separate",
            "TARGET LAYERS \u2022 PROPOSED DESIGN, PROOF STILL REQUIRED \u2022 E08/E09/E10")
for i, (label, body, fill, _) in enumerate(layers):
    top = 2.6 + i * 0.58
    els.append(card(0.65, top, 3.0, 0.5, label, FOREST if fill == SAGE else INK, 14, True, 0.05) if fill == SAGE
               else card(0.65, top, 3.0, 0.5, label, GOLD, 14, False, 0.05))
    els.append(card(3.85, top, 8.8, 0.5, body, fill, 15, False, 0.05))
els.append(card(0.65, 5.82, 12.0, 0.5, "ACROSS ALL LAYERS: least privilege, monitoring, recovery and human approval, each still to be proven",
                FOREST, 14, True, 0.05))
write(7, "Four layers keep speed, control and AI separate", els,
      f"""Here is the same system as layers. Staff and, later, controlled resident touchpoints use role queues and one case view. Beneath that, deterministic workflow rules rank work, route tasks and hold gates, so priority is explainable rather than a model's guess.
Every action passes the controlled API, which checks identity, case-level access, evidence versions and approvals before the case store changes. Case state sits in Azure SQL, evidence in versioned Blob storage, and Excel arrives by validated one-way import.
Bounded AI sits to the side. It receives permitted inputs and returns a cited draft, a typed choice or a flag to a person. It has no write credentials, so it can make staff faster without being able to act alone.
The bottom band is what we still have to prove: least privilege, monitoring, recovery and approval. This is a target design, not a deployed topology.

{EVID_ARCH}""")

# Slide 8: day in the life
rows = [
    ("Search workbooks and inboxes for the case", "Open one linked case with owner and blocker"),
    ("Ask colleagues what happens next", "See a ranked next action in your queue"),
    ("Hunt for the latest file to prove a decision", "Evidence and approvals attached to the case"),
    ("Rewrite status updates by hand", "Cited draft for staff to check and send"),
]
els = frame(8, "WHAT CHANGES FOR USERS \u2022 EXPERIENCE AND SPEED \u2022 HYPOTHESES TO TEST",
            "Same case, fewer chases: a working day",
            "SECTOR-INFORMED HYPOTHESES \u2022 NO TIME SAVED IS YET MEASURED \u2022 E05/E09/E12")
els += [tb(2.55, 0.65, 5.2, 0.25, "TODAY: WORKBOOKS AND CHASING (HYPOTHESIS)", 11, MUTED, True),
        tb(2.55, 7.45, 5.2, 0.25, "WITH THE WORKBENCH (MECHANISM TO TEST)", 11, MUTED, True)]
for i, (a, b) in enumerate(rows):
    top = 3.1 + i * 0.8
    els.append(card(0.65, top, 5.6, 0.66, a, SAGE, 15))
    els.append(chevron(6.55, top + 0.1))
    els.append(card(7.45, top, 5.2, 0.66, b, FOREST, 15, True))
write(8, "Same case, fewer chases: a working day", els,
      """Take one working day for a coordinator. Today, in a workbook-led process, finding a case can mean searching several workbooks and inboxes. Knowing what happens next can mean asking a colleague. Proving a decision can mean hunting for the latest file, and updating a resident or contractor can mean rewriting the same status by hand. These are sector-informed hypotheses about Excel, not findings about Proper North Homes.
With the workbench, the same person opens one linked case that shows the owner and blocker, sees a ranked next action, finds evidence and approvals attached, and reviews a cited draft update before sending it.
Speed comes from fewer searches, fewer chases and fewer retyped updates. We will test it by timing find-the-case, chase counts and rework in a paired exercise against the current route. No time saving is measured yet, and residents and contractors benefit through clearer, more consistent updates that staff still approve.

Evidence:
docs/reference/research/company/agent-request-challenge.md - Purpose and Method; Summary (2026-09-26, role-agent hypotheses)
docs/case_study_48_addendum.md - Subsequent Application Exercise Builds (2026-10-11); Current Learning and Parallel Experiment (feasibility, not benefit)
docs/prds/proper-warm-retrofit-programme-demonstrator.md - Executive Summary; paired proof criteria (v0.13.0 candidate 2026-10-11)""")

# Renumber footers
for d in sorted(ROOT.glob("slide-*")):
    n = int(d.name.split("-")[1])
    f = d / "content.yaml"
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"(?m)^(\s*text: '?)\d\d(  /  PROPER WARM)", lambda m: f"{m.group(1)}{n:02d}{m.group(2)}", t)
    t = re.sub(r"(?m)^slide: \d+", f"slide: {n}", t)
    f.write_text(t, encoding="utf-8")
print("done")
