"""Generate the approved 22-slide capstone content, exclusively in this directory."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
from pathlib import Path

import yaml
from pptx import Presentation

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
HANDOVER = REPO / ".copilot-tracking/reviews/plans/2026-10-14/capstone-native-rebuild-plan-critique.md"
CONTENT = ROOT / "content"
FOREST = "#173F35"
INK = "#183A31"
CREAM = "#F7F2E7"
MOSS = "#D5E2D4"
WARM = "#E5B96A"
MUTED = "#446056"
FONT = "Liberation Sans"
LOGGER = logging.getLogger(__name__)
SOURCE_IDS = {
    1: [1, 2, 3, 9, 10], 2: [1, 2], 3: [2, 4], 4: [2, 4],
    5: [2, 7, 12], 6: [2, 5, 6, 7], 7: [6, 7], 8: [2, 6, 7, 10],
    9: [2, 7, 11], 10: [7, 11, 12], 11: [7, 8, 10, 11],
    12: [8, 9, 10, 11], 13: [2, 7, 9, 11, 15], 14: [3, 6, 9],
    15: [6, 7, 10, 12], 16: [2, 5, 7, 10], 17: [7, 9, 10, 11],
    18: [2, 3, 7, 10], 19: [7, 8, 11, 12, 13], 20: [2, 3, 5, 7, 9, 10, 11, 12],
    21: list(range(1, 16)), 22: [2, 3, 7, 12],
}
TIMES = [35, 25, 35, 35, 30, 35, 65, 40, 35, 30, 45, 110, 60, 50, 35, 50, 45, 35]
TOPICS = [
    "request/mission", "five asks", "research reversal", "prerequisite examples",
    "shared foundation", "work contract", "connected journey", "dignity/capacity",
    "decision trace", "system context", "control flow", "task fit and technical proof",
    "map", "fictional cash", "supported change", "two comparisons", "gates",
    "decision", "technical limits", "council challenge", "provenance", "options",
]


def textbox(name: str, text: str, x: float, y: float, w: float, h: float,
            *, size: float = 20, color: str = INK, bold: bool = False,
            pad: float = 0.02) -> dict:
    """Return a named, fixed-size, explicitly top-anchored native text box."""
    return dict(type="textbox", name=name, text=text, left=x, top=y, width=w, height=h,
                font=FONT, font_size=size, font_color=color, font_bold=bold,
                vertical_anchor="top", auto_size="none", word_wrap=True,
                margin_left=pad, margin_right=pad, margin_top=pad, margin_bottom=pad,
                line_spacing=1.08, space_before=0, space_after=5)


def box(name: str, x: float, y: float, w: float, h: float,
        *, fill: str = MOSS) -> dict:
    """Return a separately editable native card background without hidden text."""
    return dict(type="shape", shape="rounded_rectangle", name=name,
                left=x, top=y, width=w, height=h, fill=fill,
                line_color=fill, line_width=0)


def arrow(name: str, x1: float, y1: float, x2: float, y2: float,
          *, color: str = MUTED) -> dict:
    """Return a native directional connector."""
    return dict(type="connector", name=name, connector_type="straight",
                begin_x=x1, begin_y=y1, end_x=x2, end_y=y2,
                line_color=color, line_width=1.8, head_end="none", tail_end="triangle")


def ribbon(elements: list[dict], text: str, *, y: float = 6.2,
           fill: str = WARM, size: int = 20, h: float = 0.60) -> None:
    """Append an independent, readable statement band."""
    elements.extend([box("boundary-background", .55, y, 12.23, h, fill=fill),
                     textbox("boundary-text", text, .73, y+.10, 11.87, h-.14,
                             size=size, bold=True)])


def cards(elements: list[dict], entries: list[tuple[str, str]], *,
          y: float = 2.02, h: float = 3.72, title_h: float = .94,
          title_size: int = 24, body_size: int = 22, fill: str = MOSS,
          prefix: str = "peer") -> None:
    """Create peer cards with shared title regions, padding and body baselines."""
    gap = .22
    w = (12.23 - gap * (len(entries)-1)) / len(entries)
    for i, (title, body) in enumerate(entries, 1):
        x = .55+(i-1)*(w+gap)
        elements.extend([
            box(f"{prefix}-{i}-background", x, y, w, h, fill=fill),
            textbox(f"{prefix}-{i}-title", title, x+.18, y+.20, w-.36, title_h,
                    size=title_size, bold=True),
            textbox(f"{prefix}-{i}-body", body, x+.18, y+.20+title_h+.17,
                    w-.36, h-title_h-.57, size=body_size),
        ])


def clean_markdown(text: str) -> str:
    """Retain approved words while removing presentation markdown syntax."""
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", text).replace("“", '"').replace("”", '"')


def parse_handover() -> tuple[dict[int, dict], dict[int, str], str]:
    """Read all approved slide notes and expand the handover source register."""
    text = HANDOVER.read_text(encoding="utf-8")
    source_rows = re.findall(r"^\| S(\d+) \| (.*?) \| (.*?) \|$", text, re.MULTILINE)
    sources = {int(i): f"S{int(i):02d}: {path}. Status: {status}."
               for i, path, status in source_rows}
    matches = list(re.finditer(r"^### Slide (\d+) — (.+)$", text, re.MULTILINE))
    slides = {}
    for index, match in enumerate(matches):
        end = matches[index+1].start() if index+1 < len(matches) else text.index("### Retained-content")
        section = text[match.end():end]
        notes = section.split("* **Notes", 1)[1]
        notes = notes[notes.index(":**")+3:]
        notes = notes.split("* **Sources /", 1)[0].strip()
        message = re.search(r"\* \*\*Message:\*\* (.*)", section).group(1)
        slides[int(match.group(1))] = {
            "title": match.group(2), "notes": clean_markdown(notes), "message": message,
        }
    oracle = text.split("**Exact current-proof oracle (parent verifies final source claims):**", 1)[1]
    oracle = oracle.split("No new legal date", 1)[0]
    return slides, sources, oracle.strip()


def make_base(number: int, title: str, source_ids: list[int]) -> list[dict]:
    """Create consistent branding, reserved title block and correct page counter."""
    dark = number in (1, 5, 18)
    fg = CREAM if dark else INK
    section = "OPTIONAL REFERENCE" if number >= 19 else "EXECUTIVE PROPOSAL"
    return [
        textbox("deck-eyebrow", f"ZAVA NORTH HOMES  /  ZAVA FORWARD  /  {section}",
                .55, .25, 10.8, .25, size=11, color=fg, bold=True),
        box("brand-logo-backing", 11.90, .22, .88, .32, fill="#FFFFFF"),
        dict(type="image", name="Zava branding logo — only branding",
             path="images/zava-logo.png", left=11.92, top=.23, width=.84, height=.293),
        textbox("slide-title", title, .55, .79, 12.23, .98,
                size=32, color=fg, bold=True),
        textbox("source-footer", "14 OCT 2026  •  " +
                " / ".join(f"S{s:02d}" for s in source_ids) + "  •  Sources + status in notes",
                .55, 7.12, 11.4, .20, size=10, color=fg),
        textbox("page-counter", f"{number:02d} / 22", 12.00, 7.10, .78, .23,
                size=11, color=fg, bold=True),
    ]


def map_elements(elements: list[dict]) -> None:
    """Create the five-column map with native names and shared row geometry."""
    # The .98-inch title region of the rest of the deck becomes .5 on the dense map.
    title = next(e for e in elements if e["name"] == "slide-title")
    title.update(top=.65, height=.50, font_size=30)
    elements.append(textbox("map-status", "Workflow controls progression. People retain decisions.  |  Design + implemented contracts; proactive OFF.",
                            .55, 1.19, 12.23, .30, size=16, bold=True))
    stages = ["Choose homes", "Assess & design", "Prepare funding", "Coordinate works", "Verify & hand over"]
    owners = [
        "Assets: policy;\ndata owners: verify",
        "Assessor/coordinator:\nindependent sign-off",
        "Finance: validate,\napprove, submit",
        "Resident: choice;\nProgramme: release",
        "Independent quality\nauthority: accept",
    ]
    titles = ["Stock\nPrioritisation", "Assessment\nPreparation", "Grant & Funding\nEvidence",
              "Works & Resident\nCoordination", "Quality Evidence\nReview"]
    requests = ["Explain facts;\nquery conflicts", "Prepare sourced\nsurvey/design pack",
                "Draft source-linked\nevidence pack", "Draft update;\nsuggest crew slots",
                "Assemble evidence;\nraise gaps"]
    triggers = ["Missing/conflicting\nstock facts", "Missing/changed\nsurvey or design",
                "Missing inputs or\nchanged terms", "Unaccepted handoff;\noverdue update",
                "Missing/conflicting\nquality evidence"]
    gap = .13
    w = (12.23-4*gap)/5
    for i in range(5):
        x = .55+i*(w+gap)
        p = f"map-peer-{i+1}"
        elements.extend([
            box(p+"-stage-background", x, 1.63, w, .54, fill=FOREST),
            textbox(p+"-stage", stages[i], x+.05, 1.70, w-.10, .41,
                    size=17, color=CREAM, bold=True),
            textbox(p+"-owner", owners[i], x+.05, 2.26, w-.10, .69, size=16),
            box(p+"-capability-background", x, 3.01, w, 2.84),
            textbox(p+"-title", titles[i], x+.10, 3.10, w-.20, .74,
                    size=17, bold=True),
            textbox(p+"-request-label", "On request", x+.10, 3.91, w-.20, .29,
                    size=16, bold=True),
            textbox(p+"-request-body", requests[i], x+.10, 4.23, w-.20, .57, size=16),
            textbox(p+"-proactive-label", "Trigger • OFF", x+.10, 4.86, w-.20, .29,
                    size=16, bold=True),
            textbox(p+"-proactive-body", triggers[i], x+.10, 5.19, w-.20, .59, size=16),
        ])
        if i < 4:
            elements.append(arrow(p+"-stage-arrow", x+w+.01, 1.90,
                                  x+w+gap-.01, 1.90))
    elements.extend([
        box("map-core-background", .55, 5.99, 12.23, .45, fill=FOREST),
        textbox("map-core", "Workflow core: rights • versions • gates • human approvals • audit • retries • manual recovery",
                .69, 6.08, 11.95, .31, size=16, color=CREAM, bold=True),
        textbox("map-funding-boundary", "Checks OFF now; future eligibility → named human queue. Funding: application ≠ award ≠ claim ≠ cash.",
                .55, 6.54, 12.23, .28, size=16),
        textbox("map-hazard-boundary", "Hazard → human service now, never wait for AI. Value remains a hypothesis.",
                .55, 6.86, 12.23, .27, size=16),
    ])
    # Dense map uses an explicitly smaller citation line, not smaller process copy.
    footer = next(e for e in elements if e["name"] == "source-footer")
    footer.update(top=7.25, font_size=9, height=.17)
    next(e for e in elements if e["name"] == "page-counter").update(top=7.23, height=.20)


def slide_elements(number: int, elements: list[dict]) -> None:
    """Add each approved slide's individual narrative layout and editable copy."""
    if number == 1:
        elements.extend([
            textbox("resident-scale", "60,000 homes.", .55, 2.12, 7.2, .65, size=38, color=CREAM, bold=True),
            textbox("resident-outcome", "Safe, resident-accepted\nhandovers.", .55, 2.99, 7.0, 1.40,
                    size=34, color=CREAM),
            textbox("opening-evidence", "Real service proof now.\nHuman and value gates next.", .55, 5.12, 7.1, 1.0,
                    size=24, color=CREAM),
            box("decision-background", 8.30, 2.12, 4.48, 3.89, fill=WARM),
            textbox("decision-title", "TODAY’S DECISION", 8.55, 2.39, 3.98, .70, size=21, bold=True),
            textbox("decision-body", "Endorse the next\nacceptance-and-value\nproposal.", 8.55, 3.32, 3.98, 1.80,
                    size=25, bold=True),
        ])
        ribbon(elements, "Proposal only — no new spending or production authority.", size=19)
    elif number == 2:
        cards(elements, [("Choose\nhomes", "Prioritisation"), ("Assess &\ndesign", "Assessment"),
                         ("Prepare\nfunding", "Evidence"),
                         ("Coordinate\nworks", "Delivery"),
                         ("Verify &\nhand over", "Quality")],
              title_size=23, body_size=18, h=2.80, title_h=1.05)
        elements.append(textbox("outcome", "Safe + resident-accepted + evidence-complete", .75, 5.21, 11.8, .65,
                                 size=29, bold=True))
        ribbon(elements, "Measure accepted outcomes, not messages or drafts.")
    elif number == 3:
        cards(elements, [("Rules", "Gates, clocks,\neligibility, versions."),
                         ("People", "Policy, consent,\nprofessional and\nfinancial decisions."),
                         ("Bounded AI", "Reconcile, prepare,\ndraft, flag.")])
        ribbon(elements, "Eight role-agent research instruments — not employee interviews.", size=19)
    elif number == 4:
        cards(elements, [("Rank homes", "Approved policy\n+\nsourced facts."),
                         ("Offer a slot", "Committed capacity\n+\nresident choice."),
                         ("Draft funding", "Accepted evidence\n+\nseparate ledger states.")], title_size=25, body_size=24)
        ribbon(elements, "A slot is not consent. A form is not funding.")
    elif number == 5:
        cards(elements, [("KEEP", "Teams, suppliers,\nuseful systems."),
                         ("ADD", "One case, owned transitions,\nevidence, bounded assistance.")],
              title_size=28, body_size=27, fill=CREAM)
        ribbon(elements, "Excel becomes reporting after a controlled transition.", size=22)
    elif number == 6:
        cells = [
            ("Owner + receiver", "Sender chases until accepted."),
            ("State", "What is actually true now?"),
            ("Entry, exit, pause", "Explicit conditions and holds."),
            ("Blocker + next action", "Named action and update owner."),
            ("Evidence version", "Reopen dependent reviews."),
            ("Decision + reason", "Authority, rationale, history."),
        ]
        for row in range(2):
            cards(elements, cells[row*3:row*3+3], y=2.01+row*1.97, h=1.78,
                  title_h=.55, title_size=22, body_size=19, prefix=f"row-{row+1}-peer")
        ribbon(elements, "Sent ≠ accepted. Completed ≠ handed over.", y=6.20)
    elif number == 7:
        cards(elements, [
            ("1  Resolve", "Conflicting evidence.\nNamed resolver."),
            ("2  Agree", "Scope, resident choice,\nfunding, capacity."),
            ("3  Deliver", "Inspect work.\nReturn defects."),
            ("4  Accept", "Resident handover.\nFinance closes separately."),
        ], h=3.30, title_h=.63, title_size=25, body_size=22)
        for i in range(3):
            right_edge = .55+(i+1)*(12.23-.66)/4+i*.22
            elements.append(arrow(f"journey-arrow-{i+1}", right_edge+.02, 3.10,
                                  right_edge+.20, 3.10))
        elements.extend([
            box("journey-hold-return-background", .55, 5.51, 12.23, .43, fill=WARM),
            textbox("journey-hold-return", "Hold / return → named, competent human owner", .73, 5.58, 11.87, .31,
                    size=18, bold=True),
        ])
        ribbon(elements, "Illustrative exercise journey — not an executed end-to-end customer outcome.",
               y=6.10, size=18, h=.70)
    elif number == 8:
        cards(elements, [
            ("Resident", "Clear options.\nSafe phone, letter or assisted route.\nMeasure-specific choice."),
            ("Delivery", "Committed crew, competence,\nmaterials and named liaison."),
        ], body_size=24)
        ribbon(elements, "Preferences ≠ consent. Silence/no-access ≠ refusal.", y=5.94, size=19)
        elements.append(textbox("human-hazard-route", "Human hazard route — never wait for AI.", .70, 6.67, 11.9, .34,
                                 size=19, bold=True))
    elif number == 9:
        cards(elements, [("Know", "Source + evidence\nversion + unknowns."),
                         ("Decide", "Rule + result +\nreviewer + reason."),
                         ("Change", "Authority + dependent\nre-review + preserved\nhistory.")], body_size=24)
        ribbon(elements, "New source ≠ approved new policy.")
    elif number == 10:
        cards(elements, [
            ("Existing sources", "Housing / repairs\nDocuments / spreadsheets\nSource owners retain authority."),
            ("Shared case", "Validated intake\nVersions + owned work\nNo uncontrolled write-back."),
            ("People + channels", "Role queues\nSupported resident routes\nScoped supplier exchange."),
        ], body_size=21, title_size=24)
        elements.extend([
            arrow("context-proposed-intake", 4.50, 4.9, 4.76, 4.9),
            arrow("context-proposed-exchange", 8.65, 4.9, 8.91, 4.9),
        ])
        ribbon(elements, "Target context — links proposed, not all delivered. Excel reports.", size=19)
    elif number == 11:
        elements.append(textbox("proposal-lane-label", "PROPOSAL PATH  /  observed operator integration; staff acceptance open",
                                 .55, 1.93, 12.2, .35, size=17, bold=True))
        cards(elements, [("Request → API", "Permitted task."),
                         ("Snapshot → model", "Bounded proposal."),
                         ("Human review", "Verify sources first.")],
              y=2.43, h=1.75, title_h=.48, title_size=23, body_size=21, prefix="proposal-peer")
        elements.append(textbox("domain-lane-label", "SEPARATE CONTROLLED PATH  /  authority remains with people and rules",
                                 .55, 4.45, 12.2, .35, size=17, bold=True))
        cards(elements, [("Authorized action", "Effective authority."),
                         ("Deterministic gates", "Holds + evidence."),
                         ("SQL + audit", "Controlled write.")],
              y=4.94, h=1.35, title_h=.36, title_size=21, body_size=18,
              prefix="domain-peer")
        ribbon(elements, "Model cannot approve, send, book, pay or clear a hold.", y=6.42, size=20, h=.48)
    elif number == 12:
        cards(elements, [
            ("OBSERVED", "5 distinct ready proposals\n5 real calls · 6,884 tokens\n15 ledger events\n\nControlled state unchanged;\nproposal contents survived restart."),
            ("STILL TO PROVE", "Staff browser/API + roles\nHuman source verification\nSemantic correctness + value\n\nCurrent authority absent.\nProactive OFF; gates OPEN."),
        ], y=1.97, h=4.10, title_h=.55, title_size=25, body_size=22)
        elements.append(textbox("proof-provenance", "Recorded operator-service proof · 14 October · image05 / e0254cb3 · revision12",
                                 .68, 6.24, 12.0, .35, size=17, bold=True))
        elements.append(textbox("proof-synthetic-context", "Synthetic baseline: 980 cases / 38 visits / 11 private staff bindings. No identity details.",
                                 .68, 6.67, 12.0, .30, size=16))
    elif number == 13:
        map_elements(elements)
    elif number == 14:
        elements.extend([
            textbox("fictional-label", "FICTIONAL EXA-010/015  /  not a workbench price or award",
                    .55, 1.93, 12.2, .35, size=18, bold=True),
            box("gross-background", .55, 2.51, 12.23, 1.13, fill=FOREST),
            textbox("gross-title", "BEFORE GRANT RECEIPT", .80, 2.72, 5.6, .40, size=21, color=CREAM, bold=True),
            textbox("gross-value", "£20,000 gross base cash", 6.57, 2.72, 5.96, .60,
                    size=29, color=CREAM, bold=True),
        ])
        cards(elements, [
            ("IF RECEIVED", "£7,500 fictional grant\n→ £12,500 provider base."),
            ("IF CONTINGENCY SPENT", "£22,000 gross exposure\n£14,500 provider exposure."),
        ], y=3.98, h=1.95, title_h=.43, title_size=21, body_size=23)
        ribbon(elements, "Application ≠ award ≠ claim ≠ cash.", y=6.23, size=23)
    elif number == 15:
        cards(elements, [
            ("Co-design\ntasks", "Programme +\nworkbook owners."),
            ("Shadow\none-way import", "Data owners:\nreconcile + quarantine."),
            ("Supported task\nwalkthroughs", "Team leads:\nhelp + observe."),
            ("Controlled switch\nand rollback", "Digital + work owners:\nexit tests first."),
        ], title_size=22, body_size=22, title_h=1.05)
        ribbon(elements, "Proposed owners. No permanent dual entry. No compulsory portal.", size=19)
    elif number == 16:
        cards(elements, [
            ("Programme comparison", "Matched existing teams.\nFrozen cohort; same events.\nAccepted handovers +\nwhole-chain cost."),
            ("Paired task comparison", "Same inputs: manual/rules\nversus assistance.\nQuality, net human effort,\nlatency and cost."),
        ], title_size=24, body_size=24)
        ribbon(elements, "Include unfinished/withdrawn homes. Protect safety, choice, quality, equity + cash.", size=18)
    elif number == 17:
        cards(elements, [
            ("1  Confirm", "Requirements,\nowners, authority."),
            ("2  Accept", "Real staff/session,\nsource review, roles,\naccessibility."),
            ("3  Compare", "Semantics, net effort,\ncost, recovery."),
            ("4  Decide", "Continue,\nsimplify or stop."),
        ], title_h=.73, title_size=24, body_size=23)
        ribbon(elements, "Recorded operator proof is an input — not production approval.", size=20)
    elif number == 18:
        cards(elements, [
            ("CEO / Assets", "Sponsor +\naccountable owners."),
            ("CIO / Programme", "Human, permission\nand recovery evidence."),
            ("CFO", "Whole-life affordability\n+ scoped authority review."),
        ], title_size=24, body_size=24, fill=CREAM)
        ribbon(elements, "Agree the return date and stop tests.", size=24)
        elements.append(textbox("closing-boundary", "No new procurement, spending, rollout or production authority.",
                                 .72, 6.80, 11.9, .27, size=16, color=CREAM))
    elif number == 19:
        cards(elements, [
            ("State", "Versions, fenced attempts,\nreservations.\nContent restart observed."),
            ("Trust", "Permitted sources,\ncurrent role checks,\nindependent review.\nReal-session assurance open."),
            ("Operate", "Owned manual path.\nPerformance, restore,\nquality and unit cost open."),
        ], title_size=26, body_size=22)
        ribbon(elements, "Decision 1 is separate from the five new GPT proposal calls.", size=20)
    elif number == 20:
        entries = [
            ("Why not improve Excel?", "Test equal scope and controls."),
            ("Why not launch now?", "Human, semantic and value gates open."),
            ("What budget?", "No new commitment; whole-life appraisal."),
            ("What if AI fails?", "Manual workflow remains; simplify."),
        ]
        for row in range(2):
            cards(elements, entries[row*2:row*2+2], y=2.01+row*2.03, h=1.90,
                  title_h=.57, title_size=23, body_size=22, prefix=f"qa-row-{row+1}-peer")
        ribbon(elements, "Unknown answers get an owner and evidence route, not a confident guess.", size=19)
    elif number == 21:
        cards(elements, [
            ("Request + research", "Request ≠ result.\nResearch instruments\n≠ residents."),
            ("Exercise fixtures", "Fixtures ≠ company\nperformance or budgets."),
            ("Observed proof", "Operator proof ≠ human,\nsemantic or value\nacceptance."),
        ], title_size=24, body_size=23)
        ribbon(elements, "As at 14 October. Legal currentness not refreshed.", y=6.03, size=20)
        elements.append(textbox("assessment-open", "Live pitch, rehearsal and thought-leadership evidence still required.",
                                 .71, 6.76, 11.9, .32, size=18, bold=True))
    elif number == 22:
        # Native text cells instead of a paragraph-heavy screenshot/table image.
        x_positions = [3.45, 6.62, 9.79]
        options = ["Improve current\nworkflow", "Greenfield\nbusiness platform", "Azure-led\nhybrid"]
        for i, (x, title) in enumerate(zip(x_positions, options), 1):
            elements.extend([
                box(f"option-{i}-header-background", x, 1.98, 2.99, 1.05, fill=FOREST),
                textbox(f"option-peer-{i}-title", title, x+.13, 2.14, 2.73, .76,
                        size=21, color=CREAM, bold=True),
            ])
        rows = [("Mandatory controls", "To verify"), ("Transition + access", "To test"),
                ("Support + recovery", "To test"), ("Whole-life cost", "To price")]
        for r, (label, cell) in enumerate(rows):
            y = 3.18+r*.64
            elements.append(textbox(f"option-row-{r+1}-label", label, .55, y+.12, 2.75, .42,
                                     size=19, bold=True))
            for i, x in enumerate(x_positions, 1):
                elements.extend([
                    box(f"option-{i}-row-{r+1}-background", x, y, 2.99, .57),
                    textbox(f"option-row-{r+1}-peer-{i}-body", cell, x+.13, y+.12, 2.73, .40, size=19),
                ])
        ribbon(elements, "Equivalent-scope evidence still needed — no winner scored.", y=6.21, size=21)


def write_yaml(path: Path, content: dict) -> None:
    """Write reproducible UTF-8 YAML within the bounded output tree."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(content, sort_keys=False, allow_unicode=True, width=100),
                    encoding="utf-8")


def main() -> None:
    """Generate all editable content and source provenance."""
    slides, sources, oracle = parse_handover()
    assert len(slides) == 22
    source = ROOT / "source/canonical-22-slides.pptx"
    prs = Presentation(source)
    style = yaml.safe_load((ROOT / "source/extracted/global/style.yaml").read_text())
    style["dimensions"] = dict(width_inches=prs.slide_width/914400,
                               height_inches=prs.slide_height/914400, format="16:9")
    style["typography"].update(body_font=FONT, heading_size=32, body_size=22)
    style["metadata"]["title"] = "Zava Forward — Back the evidence. Keep the resident promise."
    style["metadata"]["subject"] = "14 October 2026; bounded next acceptance-and-value proposal"
    write_yaml(CONTENT / "global/style.yaml", style)
    map_spec = HANDOVER.read_text().split("## Native Map Implementation Specification — Slide 13", 1)[1]
    map_spec = map_spec.split("**Builder-generated checks", 1)[0]
    registry_excerpt = (REPO / "mvp/zavaforward_mvp/assistants.py").read_text().split("REGISTRY = {", 1)[1]
    registry_excerpt = "REGISTRY = {" + registry_excerpt.split("OUTPUT_SCHEMA", 1)[0]
    contracts = {
        "RC": "Retrofit Coordinator",
        "PM": "Programme Manager",
    }
    for short, full in contracts.items():
        registry_excerpt = re.sub(rf"\b{short}\b", f'"{full}"', registry_excerpt)
    for number, approved in slides.items():
        slide_dir = CONTENT / f"slide-{number:03d}"
        (slide_dir / "images").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "source/extracted/slide-001/images/image-01.png",
                        slide_dir / "images/zava-logo.png")
        elements = make_base(number, approved["title"], SOURCE_IDS[number])
        slide_elements(number, elements)
        notes = (
            f"SLIDE {number:02d} — {approved['title']}\n"
            f"Topic sentinel: {TOPICS[number-1]}\n"
            f"Message: {approved['message']}\n"
            f"Status: strategist-recommended proposal; refreshed 14 October 2026.\n\n"
            f"{approved['notes']}\n\n"
            "Sources — workspace-relative paths, section and evidence status; as read 14 October 2026:\n"
            + "\n".join(sources[i] for i in SOURCE_IDS[number])
        )
        if number <= 18:
            notes += f"\n\nPlanned allocation: {TIMES[number-1]} seconds; not rehearsed."
        else:
            notes += "\n\nOptional appendix, outside the planned 795-second main route."
        if number in (12, 19, 21):
            notes += "\n\nExact current claim-status oracle:\n" + clean_markdown(oracle)
        if number == 13:
            notes += (
                "\n\nFULL MAP TEXT EQUIVALENT — five capabilities, owners, requests and OFF triggers:\n"
                + clean_markdown(map_spec)
                + "\n\nCanonical capability identifiers, permitted source categories, registry purposes and synthetic predicates:\n"
                + registry_excerpt
                + "\n\nProposal review is separate from domain approval. Programme release additionally requires "
                "current technical evidence, resident measure choice, funding/budget and committed competent "
                "capacity. Only contract authority instructs suppliers. Failed, stale or expired assistance "
                "leaves controlled state unchanged, with an owned manual path. Actual sources include permitted "
                "metadata and hashes, not arbitrary document/photo analysis. OFF triggers are not paid scans. "
                "The workflow core is deterministic infrastructure, never a sixth supervisor agent."
            )
        content = dict(slide=number, title=approved["title"],
                       section="Main" if number <= 18 else "Optional appendix",
                       layout="Blank", background=dict(fill=FOREST if number in (1, 5, 18) else CREAM),
                       elements=elements, speaker_notes=notes)
        write_yaml(slide_dir / "content.yaml", content)
    provenance = {
        "canonical_source": "docs/capstone/deck/zava-forward-executive-draft.pptx",
        "source_copy": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "handover_sha256": hashlib.sha256(HANDOVER.read_bytes()).hexdigest(),
        "source_slides": len(prs.slides),
        "source_dimensions_emu": [prs.slide_width, prs.slide_height],
        "documentation_context": "cabe05c",
        "runtime_source": "cd14b3b379026a87ebfa3e9058ac10c0df7888eb",
        "font": FONT,
        "font_rationale": "Explicit installed sans-serif; avoids uninspectable Aptos fallback in local LibreOffice. Original masters/themes retained.",
        "planned_main_seconds": sum(TIMES),
        "planned_discussion_contingency_seconds": 105,
        "rehearsed": False,
        "notes_topics": TOPICS,
        "source_ids": SOURCE_IDS,
    }
    (ROOT / "reports/provenance.json").write_text(json.dumps(provenance, indent=2)+"\n")
    LOGGER.info("Created all %d slides; main route %d seconds", len(slides), sum(TIMES))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
