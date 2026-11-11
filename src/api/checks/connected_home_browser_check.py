"""Connected same-home walk across six specialist screens on records the real Store wrote (Refs #134).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.connected_home_browser_check

The data served is a deep copy of the Store held by the delivered core journey test
(`StoreJourney.journey()`), so one fixture state carries home ZF-1 through conflict, technical
sign-off, resident decision, quality acceptance and handover, and invoice records. Constructed
fixture logins (Retrofit Programme Manager, Retrofit Coordinator, Resident Liaison Officer,
Quality Inspector, Grants and Evidence Officer) read that one state through the keyboard only
(Tab, Shift+Tab, Enter); nothing is written from the browser. Home ZF-2 is a sibling control that
holds none of those records. A required marker that is absent fails the run. Only the deferrals
printed at the end are not run. The Asset view is read through the Programme Manager login, which
is a proxy, not an Asset sign-in. The check is DOM evidence on constructed data: not user
validation, not assistive-technology output and not acceptance. It passes no criterion.
"""

from __future__ import annotations

import copy
import importlib
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, NamedTuple

from playwright.sync_api import Page, Request, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.specialist_keyboard_browser_check import (
    ENTRY,
    HANDOFF,
    HOME,
    MENU,
    RESET,
    assert_focus,
    assert_status,
    expected_status,
    login,
    tab_to,
    text_markers,
    wait_status,
)

# Append only when absent, so unittest discovery keeps its own tests directory first.
CORE_TESTS = str(ROOT / "src/core/tests")
if CORE_TESTS not in sys.path:
    sys.path.append(CORE_TESTS)

HOME_ID = "ZF-1"
SIBLING_ID = "ZF-2"
SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
# Mirrors the labels the screens render (role-screens.js signoffTypes); a test reads the source.
SIGNOFFS = (
    ("assessment", "Retrofit assessment"),
    ("design", "Design"),
    ("building", "Building and safety dependency"),
)
RECONCILED = "Reconciled (recorded by a named person)"
STAGE_LINK_SCREENS = ("technical-queue", "resident-choice", "quality-queue", "finance-invoices")


@dataclass(frozen=True)
class Visit:
    """One constructed login and the screens it reads in order, with no reset between them."""

    email: str
    screens: tuple[str, ...]
    mutate: bool = False


JOURNEY = (
    Visit("pm-1@example.test", ("asset-board", "programme-queue"), mutate=True),
    Visit("rc-1@example.test", ("technical-queue",)),
    Visit("rlo-1@example.test", ("resident-choice",)),
    Visit("qi-2@example.test", ("quality-queue",)),
    Visit("geo-1@example.test", ("finance-invoices",)),
)
LOGIN_EMAILS = tuple(visit.email for visit in JOURNEY)
DEFERRED = (
    "perspective rows 6 (Repairs and Building Safety), 7 (Procurement), 8 (Provider and "
    "contractor) and 11 (Digital operator and auditor): no step or login role in this journey",
    "entry by report or nomination, intake and aftercare stages",
    "on-screen event order and unknown intervals; eight-stage screen consistency",
    "an actual Asset sign-in (Asset is read through the Programme Manager proxy)",
    "AC-034 to AC-043 dispositions, assistive-technology output, user validation, consent, "
    "professional and human approval",
)


@dataclass(frozen=True)
class Expect:
    """One required marker, scoped to a named panel of the selected-home evidence."""

    panel: str
    row: tuple[str, ...] = ()
    field: tuple[str, ...] = ()
    text: str = ""
    links: tuple[str, ...] = ()


def journey_snapshot() -> dict[str, Any]:
    """Deep copy of the Store data the delivered journey wrote; taken before cleanup."""
    # Imported by name so this strict-typed project does not re-check the core test module.
    store_journey = importlib.import_module("test_journey_store")
    journey = store_journey.StoreJourney("test_store_journey_reaches_financial_closure_in_order")
    journey.setUp()
    try:
        journey.journey()
        data: dict[str, Any] = copy.deepcopy(journey.store.data)
        return data
    finally:
        journey.doCleanups()


def measures_of(case: Mapping[str, Any]) -> list[str]:
    return [part.strip() for part in str(case.get("measures") or "").split(",") if part.strip()]


def case_of(data: Mapping[str, Any], case_id: str) -> Mapping[str, Any]:
    found = [case for case in data.get("cases", []) if case.get("id") == case_id]
    return found[0] if found else {}


def person(value: Any) -> str:
    if isinstance(value, Mapping):
        return str(value.get("name") or "Unknown")
    return str(value) if value else "Unknown"


def decided_measures(case: Mapping[str, Any]) -> dict[str, list[Mapping[str, Any]]]:
    decisions = case.get("measure_decisions")
    if not isinstance(decisions, Mapping):
        return {}
    return {str(k): list(v) for k, v in decisions.items() if v}


def snapshot_failures(data: Mapping[str, Any]) -> list[str]:
    """Reject a snapshot that is empty, seed-only, partial or lacks a distinguishable sibling."""
    home, sibling = case_of(data, HOME_ID), case_of(data, SIBLING_ID)
    if not home or not sibling:
        return [f"snapshot lacks {HOME_ID} or {SIBLING_ID}"]
    failures: list[str] = []
    staff = {s.get("email"): s for s in data.get("staff", [])}
    failures += [f"no fixture login {e}" for e in LOGIN_EMAILS if e not in staff]
    queries = home.get("stock_reconciliation") or []
    events = home.get("stock_reconciliation_events") or []
    if not queries:
        failures.append(f"{HOME_ID} has no stock conflict")
    for query in queries:
        last = [e for e in events if e.get("query_id") == query.get("id")][-1:]
        if not last or last[0].get("status") != "Reconciled" or not query.get("query_owner"):
            failures.append(f"{HOME_ID} stock conflict {query.get('id')} is not resolved by a person")
    technical = home.get("technical") or {}
    signoffs = technical.get("signoffs") or {}
    if not technical.get("design_version") or not technical.get("design_name"):
        failures.append(f"{HOME_ID} has no recorded design version and name")
    for key, _ in SIGNOFFS:
        given = signoffs.get(key) or {}
        if given.get("status") != "Signed off" or not given.get("by") or not given.get("version"):
            failures.append(f"{HOME_ID} sign-off {key} is not a named signed-off version")
    if "coordination" in signoffs:
        failures.append(f"{HOME_ID} coordination sign-off exists; the screens would not show Not given")
    decisions = decided_measures(home)
    accepted = [v[-1] for v in decisions.values() if v[-1].get("status") == "Accepted"]
    if not accepted or not all(v.get("answered_by") and v.get("scope") for v in accepted):
        failures.append(f"{HOME_ID} has no accepted resident decision with scope and answerer")
    if not [m for m in measures_of(home) if m not in decisions]:
        failures.append(f"{HOME_ID} has no undecided measure to show as Not recorded")
    handed = [r for r in home.get("quality") or [] if r.get("state") == "Handed over"]
    if not handed or not all(
        r.get("accepted_by") and r.get("submitted_by") and (r.get("handover") or {}).get("by")
        for r in handed
    ):
        failures.append(f"{HOME_ID} has no accepted and handed over quality record with named people")
    invoices = (home.get("finance") or {}).get("invoices") or []
    if not [i for i in invoices if i.get("ref") == "INV-100" and i.get("payment_status")]:
        failures.append(f"{HOME_ID} has no invoice INV-100 with a recorded payment status")
    if not [i for i in invoices if i.get("disposition") and i.get("disposition_by")]:
        failures.append(f"{HOME_ID} invoice has no named Finance decision")
    for key in ("stock_reconciliation", "technical", "measure_decisions", "quality", "finance"):
        if sibling.get(key):
            failures.append(f"{SIBLING_ID} carries {key}; it is not a record-free sibling")
    if not measures_of(sibling) or not sibling.get("stage"):
        failures.append(f"{SIBLING_ID} has no retained measure and stage of its own")
    if not leak_markers(data):
        failures.append("no distinguishable home marker survives the sibling filter")
    return failures


def leak_markers(data: Mapping[str, Any]) -> list[str]:
    """Distinctive ZF-1 values; anything also present in ZF-2's own data is dropped as generic."""
    home, sibling = case_of(data, HOME_ID), case_of(data, SIBLING_ID)
    found: set[str] = set()
    for query in home.get("stock_reconciliation") or []:
        found |= {str(query.get("id")), str(query["left"]["source_id"]), str(query["right"]["source_id"])}
        found.add(person(query.get("query_owner")))
    for sign in ((home.get("technical") or {}).get("signoffs") or {}).values():
        found.add(str(sign.get("by")))
    for versions in decided_measures(home).values():
        found |= {str(versions[-1].get("scope")), str(versions[-1].get("answered_by"))}
    for record in home.get("quality") or []:
        found |= {
            str(record.get("submitted_by")),
            str(record.get("accepted_by")),
            str((record.get("handover") or {}).get("by")),
            f"{record.get('measure')}: {record.get('state')}",
        }
    for invoice in (home.get("finance") or {}).get("invoices") or []:
        found |= {str(invoice.get("ref")), str(invoice.get("disposition_by"))}
    found |= set(measures_of(home)) - set(measures_of(sibling))
    own = str(sibling)
    return sorted(m for m in found if m and m != "None" and m not in own)


def screen_href(screen_id: str, case_id: str) -> str:
    return f"#/screens?screen={screen_id}&case={case_id}"


def home_expectations(data: Mapping[str, Any], home_id: str = HOME_ID) -> dict[str, tuple[Expect, ...]]:
    """Required ZF-1 markers per screen, derived from the Store records, scoped to a panel."""
    case = case_of(data, home_id)
    technical = case["technical"]
    asset: list[Expect] = [Expect("Evidence boundary", text=f"Home scope: {home_id} only.")]
    events = case.get("stock_reconciliation_events") or []
    for q in case["stock_reconciliation"]:
        last = [e for e in events if e.get("query_id") == q["id"]][-1]
        status = RECONCILED if last["status"] == "Reconciled" else "Unresolved"
        asset.append(
            Expect(
                "Stock conflict comparison",
                row=(
                    str(q["id"]),
                    str(q["field"]),
                    f"{q['left']['value']}, {q['left']['source_id']} v{q['left']['version']}",
                    f"{q['right']['value']}, {q['right']['source_id']} v{q['right']['version']}",
                    status,
                    person(q.get("query_owner")),
                ),
            )
        )
    connected = f"Connected view for {home_id}"
    missing = [m for m in measures_of(case) if m not in {r.get("measure") for r in case["quality"]}]
    programme = [
        Expect(connected, row=("Technical", "Blocked", "Coordination sign-off (not given)")),
        Expect(connected, row=("Resident",)),
        Expect(connected, row=("Delivery",)),
        Expect(connected, row=("Finance",)),
        Expect(connected, links=tuple(screen_href(s, home_id) for s in STAGE_LINK_SCREENS)),
    ] + [Expect(connected, row=("Quality", "Blocked", f"{m}: no quality check recorded.")) for m in missing]
    tech = [
        Expect("Design version", field=("Current design version", str(technical["design_version"]))),
        Expect("Design version", field=("Recorded by", str(technical["design_name"]))),
        Expect("Separate sign-offs", row=("Coordination", "", "Not given", "Nobody yet")),
    ]
    for key, label in SIGNOFFS:
        sign = technical["signoffs"][key]
        tech.append(
            Expect(
                "Separate sign-offs",
                row=(label, str(sign["role"]), f"Signed off on design version {sign['version']}", str(sign["by"])),
            )
        )
    resident: list[Expect] = []
    decisions = decided_measures(case)
    for measure in measures_of(case):
        if measure in decisions:
            v = decisions[measure][-1]
            binding = f"scope {v['scope']}, revision {v['context_revision']}, design {v['design_version']}"
            latest = f"v{v['version']} {v['status']} ({binding}), answered by {v['answered_by']}"
            resident.append(Expect("Choice for each measure", row=(measure, binding, str(v["status"]), latest)))
        else:
            resident.append(
                Expect("Choice for each measure", row=(measure, "Current scope not recorded", "Not recorded", "None recorded"))
            )
    quality = [
        Expect("Handover readiness", text=f"{m}: no quality evidence recorded.") for m in missing
    ]
    for r in case["quality"]:
        title = f"{r['measure']}: {r['state']}"
        quality += [
            Expect(title, field=("Submitted by", str(r["submitted_by"]))),
            Expect(title, field=("Accepted by", str(r["accepted_by"]))),
            Expect(title, field=("Handed over by", str(r["handover"]["by"]))),
        ]
    finance: list[Expect] = []
    for inv in case["finance"]["invoices"]:
        panel = "Invoice line comparison"
        finance += [
            Expect(panel, text=f"{inv['id']}: {inv['kind']} {inv['ref']} from {inv['supplier']}"),
            Expect(
                panel,
                field=(
                    "Version and record",
                    f"{inv['id']}, work order {inv['work_order']}, match status: {inv['status']}",
                ),
            ),
            Expect(
                panel,
                field=("Finance decision", f"{inv['disposition']}, recorded by {inv['disposition_by']}"),
            ),
            Expect(
                panel,
                field=(
                    "Payment status (a note of what Finance did elsewhere)",
                    f"{inv['payment_status']}. This system never makes or releases a payment.",
                ),
            ),
        ]
    return {
        "asset-board": tuple(asset),
        "programme-queue": tuple(programme),
        "technical-queue": tuple(tech),
        "resident-choice": tuple(resident),
        "quality-queue": tuple(quality),
        "finance-invoices": tuple(finance),
    }


def sibling_expectations(data: Mapping[str, Any]) -> dict[str, tuple[Expect, ...]]:
    """What the sibling's own retained record renders on each screen: its measure, no journey data."""
    sibling = case_of(data, SIBLING_ID)
    measure = measures_of(sibling)[0]
    scope = f"Home scope: {SIBLING_ID} only."
    return {
        "asset-board": (Expect("Evidence boundary", text=scope),),
        "programme-queue": (
            Expect(
                f"Connected view for {SIBLING_ID}",
                row=("Quality", "Blocked", f"{measure}: no quality check recorded."),
            ),
        ),
        "technical-queue": (Expect("Design version", text="No design is recorded for this home."),),
        "resident-choice": (Expect("Evidence boundary", text=scope),),
        "quality-queue": (Expect("Handover readiness", text=f"{measure}: no quality evidence recorded."),),
        "finance-invoices": (Expect("Invoice line comparison", text="No invoices recorded for this home."),),
    }


def expect_failures(observed: Mapping[str, Any], expected: Sequence[Expect]) -> list[str]:
    failures: list[str] = []
    panels: Sequence[Mapping[str, Any]] = observed.get("panels") or []
    for want in expected:
        found = [p for p in panels if p.get("title") == want.panel]
        if not found:
            failures.append(f"panel {want.panel!r} not shown")
            continue
        panel = found[0]
        if want.row and not any(
            len(row) >= len(want.row) and all(part in cell for part, cell in zip(want.row, row, strict=False))
            for row in panel.get("rows") or []
        ):
            failures.append(f"panel {want.panel!r} has no row matching {want.row}")
        if want.field and not any(
            label.strip() == want.field[0] and value.strip() == want.field[1]
            for label, value in panel.get("fields") or []
        ):
            failures.append(f"panel {want.panel!r} lacks {want.field[0]!r} = {want.field[1]!r}")
        if want.text and want.text not in str(panel.get("text")):
            failures.append(f"panel {want.panel!r} lacks text {want.text!r}")
        failures += [
            f"panel {want.panel!r} lacks link {link!r}"
            for link in want.links
            if link not in (observed.get("links") or [])
        ]
    return failures


def base_failures(home_id: str, observed: Mapping[str, Any], handoff: bool) -> list[str]:
    failures: list[str] = []
    if observed.get("heading") != f"Selected home {home_id}":
        failures.append(f"evidence heading {observed.get('heading')!r} is not for {home_id}")
    carried = [h for h in observed.get("menu") or [] if f"case={home_id}" not in str(h)]
    if carried or not observed.get("menu"):
        failures.append(f"menu links that do not keep {home_id}: {carried}")
    if handoff and observed.get("handoff") != f"#/case/{home_id}":
        failures.append(f"handoff link {observed.get('handoff')!r} does not open {home_id}")
    return failures


def home_failures(screen_id: str, observed: Mapping[str, Any], expected: Mapping[str, Sequence[Expect]]) -> list[str]:
    return base_failures(HOME_ID, observed, True) + expect_failures(observed, expected[screen_id])


# Selected-home domain-record panels per screen, scanned for sibling leakage whatever the positive
# expectations name. Portfolio panels (all homes, ledger-wide, waiting queues) are deliberately absent.
RECORD_PANELS: dict[str, tuple[str, ...]] = {
    "asset-board": ("Stock conflict comparison", "Eligibility"),
    "programme-queue": (),
    "technical-queue": (
        "Technical readiness",
        "Source facts",
        "Design version",
        "Separate sign-offs",
        "Returns and routing",
        "Missing references",
    ),
    "resident-choice": (
        "Choice for each measure",
        "Paused or withdrawn by the resident",
        "Linked update commitment",
        "Service requests and access needs (separate from choice)",
    ),
    "quality-queue": ("Handover readiness", "Quality evidence"),
    "finance-invoices": ("Invoice line comparison",),
}


class Excluded(NamedTuple):
    """A panel deliberately not scanned, with the reviewed source reason it carries no home record."""

    kind: str  # portfolio-call, constant or home-id-only
    anchor: str  # exact role-screens.js text the judgement was made from
    why: str


EVIDENCE_ID_ONLY = Excluded(
    "home-id-only", "Home scope: ${c.id} only", "literals plus the home id; heading and links bind the id"
)
EVIDENCE_CONSTANT = Excluded("constant", "Read-only", "literal text only; no case field is read")
# Reviewed manifest of every other panel the six renderers emit. It is a reviewed dependency
# judgement from the source anchors, not a proof of JavaScript data flow.
EXCLUDED: dict[str, dict[str, Excluded]] = {
    "asset-board": {
        "Evidence boundary": EVIDENCE_ID_ONLY,
        "Stock conflict queue across homes (portfolio scope, not this home)": Excluded(
            "portfolio-call", "/api/asset/stock-queue", "built from the all-homes stock queue call"
        ),
        "Missing investment inputs": Excluded("constant", "assetInputs.map", "module constant rows"),
        "Benefits and phase check": Excluded("constant", "assetGates.map", "module constant rows"),
        "Portfolio scope (separate from this home)": Excluded(
            "portfolio-call", "/api/cases?view=all&limit=1", "role-scoped total of an all-homes call"
        ),
        "Ledger-wide AI cohort (all homes, not this home)": Excluded(
            "portfolio-call", "/api/ai/report", "ledger-wide AI report"
        ),
        "Ledger-wide AI usage, alerts and cost components (all homes, not this home)": Excluded(
            "portfolio-call", "/api/ai/report", "ledger-wide AI report"
        ),
    },
    "programme-queue": {
        "Evidence boundary": EVIDENCE_CONSTANT,
        "Shared queue": Excluded(
            "portfolio-call", "loadPage(0)", "paged queue of all homes the role may see"
        ),
        "Lifecycle and funnel": Excluded(
            "portfolio-call", "/api/coordinator?view=all", "all-homes coordinator report"
        ),
    },
    "technical-queue": {"Evidence boundary": EVIDENCE_ID_ONLY},
    "resident-choice": {
        "Evidence boundary": EVIDENCE_ID_ONLY,
        "Choice and update commitments across open homes (portfolio scope, not this home)": Excluded(
            "portfolio-call", "queue.items", "summary rows from the all-open-homes choice queue"
        ),
        "Choice comes before offered capacity": Excluded(
            "constant", "A recorded choice, pause or withdrawal takes precedence", "literal policy text"
        ),
    },
    "quality-queue": {"Evidence boundary": EVIDENCE_ID_ONLY},
    "finance-invoices": {
        "Evidence boundary": Excluded(
            "home-id-only", "Home scope: ${c.id} only, except the queue below", "literals plus the home id"
        ),
        "Invoices waiting for Finance (all homes your role can see)": Excluded(
            "portfolio-call", "financeQueueRows(queue)", "rows of the all-homes finance queue"
        ),
        "AI economics (ledger-wide, all homes)": Excluded(
            "portfolio-call", "financeEconomicsPanel(extra?.report)", "ledger-wide AI report and literals"
        ),
    },
}
AUDITED_OTHER: dict[str, tuple[str, ...]] = {s: tuple(m) for s, m in EXCLUDED.items()}


def is_record_panel(screen_id: str, title: str) -> bool:
    """Record panels are the inventory above, the programme Connected view, and quality record panels."""
    if title in RECORD_PANELS.get(screen_id, ()) or title.startswith("Connected view for"):
        return True
    return screen_id == "quality-queue" and ": " in title


def sibling_failures(
    screen_id: str,
    observed: Mapping[str, Any],
    own: Mapping[str, Sequence[Expect]],
    leaks: Sequence[str],
) -> list[str]:
    """The sibling view must show its own retained data and none of the ZF-1 record markers."""
    failures = base_failures(SIBLING_ID, observed, True) + expect_failures(observed, own[screen_id])
    scoped = {want.panel for want in own[screen_id]}
    for panel in observed.get("panels") or []:
        title = str(panel.get("title"))
        if title in scoped or is_record_panel(screen_id, title):
            body = f"{panel.get('title')}\n{panel.get('text')}"
            failures += [f"{HOME_ID} marker {m!r} leaked into {SIBLING_ID}" for m in leaks if m in body]
    return failures


OBSERVE = """() => {
  const ev = document.querySelector('.screen-evidence');
  if (!ev) return null;
  const text = el => (el.textContent || '').trim();
  const panels = [...ev.querySelectorAll('.screen-record')].map(p => ({
    title: text(p.querySelector(':scope > h2') || p),
    text: p.innerText,
    rows: [...p.querySelectorAll('tbody tr')].map(r => [...r.children].map(c => text(c))),
    fields: [...p.querySelectorAll('dl')].flatMap(dl => [...dl.children]
      .filter(e => e.tagName === 'DT').map(dt => [text(dt), text(dt.nextElementSibling || dt)]))
  }));
  const handoff = ev.querySelector('a[href^="#/case/"]');
  return {
    heading: text(ev.querySelector(':scope > h2') || ev), panels,
    links: [...ev.querySelectorAll('a')].map(a => a.getAttribute('href')),
    handoff: handoff ? handoff.getAttribute('href') : null,
    menu: [...document.querySelectorAll('nav[aria-label="Specialist screens"] a')]
      .map(a => a.getAttribute('href'))
  };
}"""


def observe(page: Page) -> dict[str, Any]:
    found = page.evaluate(OBSERVE)
    return dict(found) if found else {"heading": None, "panels": [], "links": [], "menu": []}


def menu_title(page: Page, screen_id: str) -> str:
    link = page.locator(f'{MENU} a[href^="#/screens?screen={screen_id}"]').first
    return link.inner_text().strip()


def reach(page: Page, selector: str, label: str, stage: str) -> None:
    keys = tab_to(page, selector) or tab_to(page, selector, back=True)
    check(f"{label}: {stage} reachable by keyboard", keys is not None)
    assert_focus(page, label, stage)


def show_home(page: Page, role: str, screen_id: str, case_id: str) -> dict[str, Any]:
    """Select the home from the queue with the keyboard, or carry it through the screen menu."""
    title = menu_title(page, screen_id)
    label = f"{role}: {title}"
    reach(page, f'a.item[href="{screen_href(screen_id, case_id)}"]', label, f"home {case_id}")
    page.keyboard.press("Enter")
    return settle(page, role, screen_id, case_id)


def carry_home(page: Page, role: str, screen_id: str, case_id: str) -> dict[str, Any]:
    """Follow the menu link to another screen with no reset; the link must keep the home."""
    title = menu_title(page, screen_id)
    reach(page, f'{MENU} a[href^="{screen_href(screen_id, case_id)}"]', f"{role}: {title}", f"carry to {screen_id}")
    page.keyboard.press("Enter")
    return settle(page, role, screen_id, case_id)


def settle(page: Page, role: str, screen_id: str, case_id: str) -> dict[str, Any]:
    title = menu_title(page, screen_id)
    wait_status(page, expected_status(role, title, case_id))
    assert_status(page, role, title, case_id, f"selected {case_id}")
    page.wait_for_function(
        "h => document.querySelector('.screen-evidence > h2')?.textContent === h",
        arg=f"Selected home {case_id}",
    )
    return observe(page)


def reload_selected(page: Page, role: str, screen_id: str, case_id: str) -> None:
    page.reload()
    page.locator(MENU).wait_for()
    settle(page, role, screen_id, case_id)


@dataclass(frozen=True)
class Mutation:
    name: str
    script: str
    arg: Any


def rejected(page: Page, mutation: Mutation, verdict: Any) -> None:
    """Apply a run-only DOM edit, read it back through the walk reader and expect failures."""
    page.evaluate(mutation.script, mutation.arg)
    failures = verdict(observe(page))
    check(f"negative control rejected by the production predicate: {mutation.name}", bool(failures))


def run_mutations(
    page: Page, role: str, screen_id: str, expected: Mapping[str, Sequence[Expect]], marker: str
) -> None:
    redact = (
        "m => { const w = document.createTreeWalker(document.querySelector('.screen-evidence'),"
        " NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.textContent.includes(m))"
        " n.textContent = n.textContent.replaceAll(m, 'REDACTED'); }"
    )
    edits = (
        Mutation("a required record marker removed", redact, marker),
        Mutation(
            "selected-home heading names the sibling",
            "() => { document.querySelector('.screen-evidence > h2').textContent = 'Selected home ZF-2'; }",
            None,
        ),
        Mutation(
            "handoff link opens the sibling",
            "() => document.querySelector('.screen-evidence a[href^=\"#/case/\"]').setAttribute('href', '#/case/ZF-2')",
            None,
        ),
        Mutation(
            "a menu link drops the selected home",
            "() => document.querySelector('nav[aria-label=\"Specialist screens\"] a[href*=\"case=\"]')"
            ".setAttribute('href', '#/screens?screen=programme-queue')",
            None,
        ),
    )
    for edit in edits:
        rejected(page, edit, lambda seen: home_failures(screen_id, seen, expected))
        reload_selected(page, role, screen_id, HOME_ID)


def run_sibling_mutations(
    page: Page,
    role: str,
    screen_id: str,
    own: Mapping[str, Sequence[Expect]],
    leaks: Sequence[str],
) -> None:
    panel = own[screen_id][0].panel
    find = "[...document.querySelectorAll('.screen-evidence .screen-record')].find(p => p.querySelector(':scope > h2')?.textContent === t)"
    edits = (
        Mutation(
            "a ZF-1 record marker leaks into the sibling evidence",
            f"([t, m]) => {{ {find}.append(m); }}",
            [panel, leaks[0]],
        ),
        Mutation(
            "the sibling's own evidence panel is removed",
            f"t => {{ {find}.remove(); }}",
            panel,
        ),
    )
    for edit in edits:
        rejected(page, edit, lambda seen: sibling_failures(screen_id, seen, own, leaks))
        reload_selected(page, role, screen_id, SIBLING_ID)


def run_record_leak(
    page: Page, role: str, screen_id: str, own: Mapping[str, Sequence[Expect]], leaks: Sequence[str]
) -> None:
    """Inject a ZF-1 marker into the sibling's actual record panel, not its evidence boundary."""
    titles = [str(p["title"]) for p in observe(page)["panels"] if is_record_panel(screen_id, str(p["title"]))]
    check(f"{role}: {screen_id} sibling shows a record panel to challenge; found={titles}", bool(titles))
    if screen_id == "technical-queue":
        for required in ("Technical readiness", "Source facts"):
            check(f"{role}: {required} is shown for the sibling and scanned", required in titles)
        titles = ["Technical readiness", "Source facts"]
    find = "[...document.querySelectorAll('.screen-evidence .screen-record')].find(p => p.querySelector(':scope > h2')?.textContent === t)"
    for title in titles[: 2 if screen_id == "technical-queue" else 1]:
        edit = Mutation(
            f"a ZF-1 marker leaks into the sibling record panel {title!r}",
            f"([t, m]) => {{ {find}.append(m); }}",
            [title, leaks[0]],
        )
        rejected(page, edit, lambda seen: sibling_failures(screen_id, seen, own, leaks))
        reload_selected(page, role, screen_id, SIBLING_ID)


def walk_visit(
    page: Page,
    visit: Visit,
    role: str,
    expected: Mapping[str, Sequence[Expect]],
    own: Mapping[str, Sequence[Expect]],
    leaks: Sequence[str],
    observations: list[dict[str, Any]],
) -> None:
    entry = tab_to(page, ENTRY)
    check(f"{role}: Specialist screens entry reachable by Tab", entry is not None)
    assert_focus(page, f"{role}: Specialist screens entry", "entry")
    page.keyboard.press("Enter")
    page.locator(MENU).wait_for()
    first = visit.screens[0]
    title = menu_title(page, first)
    reach(page, f'{MENU} a[href="#/screens?screen={first}"]', f"{role}: {title}", "screen")
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    assert_status(page, role, title, None, "unselected")
    for index, screen_id in enumerate(visit.screens):
        seen = show_home(page, role, screen_id, HOME_ID) if index == 0 else carry_home(page, role, screen_id, HOME_ID)
        failures = home_failures(screen_id, seen, expected)
        check(f"{role}: {screen_id} shows the {HOME_ID} journey records; failures={failures}", not failures)
        reach(page, HANDOFF, f"{role}: {screen_id}", "case workspace handoff link")
        observations.append(
            {
                "role": role,
                "screen": screen_id,
                "home": HOME_ID,
                "panels": [p["title"] for p in seen["panels"]],
                **text_markers(page.locator(".screen-evidence").inner_text()),
            }
        )
        if visit.mutate and index == 0:
            marker = expected[screen_id][1].row[0]
            run_mutations(page, role, screen_id, expected, marker)
    last = visit.screens[-1]
    seen = show_home(page, role, last, SIBLING_ID)
    failures = sibling_failures(last, seen, own, leaks)
    check(f"{role}: {last} sibling {SIBLING_ID} control; failures={failures}", not failures)
    observations.append({"role": role, "screen": last, "home": SIBLING_ID, "panels": [p["title"] for p in seen["panels"]]})
    run_record_leak(page, role, last, own, leaks)
    for screen_id in reversed(visit.screens[:-1]):
        seen = carry_home(page, role, screen_id, SIBLING_ID)
        failures = sibling_failures(screen_id, seen, own, leaks)
        check(f"{role}: {screen_id} sibling {SIBLING_ID} control; failures={failures}", not failures)
        observations.append({"role": role, "screen": screen_id, "home": SIBLING_ID, "panels": [p["title"] for p in seen["panels"]]})
        run_record_leak(page, role, screen_id, own, leaks)
        if visit.mutate:
            run_sibling_mutations(page, role, screen_id, own, leaks)
    title = menu_title(page, visit.screens[0])
    reach(page, RESET, f"{role}: {title}", "Reset screen view")
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    assert_status(page, role, title, None, "reset-status")
    check(f"{role}: reset clears the selected home", page.locator(".screen-evidence").count() == 0)


_SERVED: dict[str, Any] = {}


def served_snapshot() -> dict[str, Any]:
    """The factory handed to the harness: blocked, not skipped, when the snapshot is not usable."""
    data = journey_snapshot()
    failures = snapshot_failures(data)
    if failures:
        raise AssertionError(f"journey snapshot cannot be served: {failures}")
    _SERVED.clear()
    _SERVED.update(copy.deepcopy(data))
    return data


def run_browser(base: str) -> None:
    if not _SERVED:
        raise AssertionError("journey snapshot was not served to this check")
    expected, own, leaks = home_expectations(_SERVED), sibling_expectations(_SERVED), leak_markers(_SERVED)
    roles = {str(s["email"]): str(s["role"]) for s in _SERVED["staff"]}
    errors: list[str] = []
    writes: list[str] = []
    observations: list[dict[str, Any]] = []

    def record(request: Request) -> None:
        if request.method not in SAFE_METHODS:
            writes.append(f"{request.method} {request.url}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        print(f"BROWSER VERSION {browser.version}")
        try:
            for visit in JOURNEY:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                role = roles[visit.email]
                login(page, base, {"email": visit.email, "role": role})
                page.on("request", record)
                walk_visit(page, visit, role, expected, own, leaks, observations)
                context.close()
            check(f"no uncaught JavaScript errors in the connected walk ({errors})", not errors)
            check(f"the browser made no write requests after login ({writes})", not writes)
            report(observations)
        finally:
            browser.close()


def report(observations: list[dict[str, Any]]) -> None:
    print("OBSERVATIONS (DOM evidence on constructed fixtures; not authentication, not AT output)")
    print(f"One fixture state: home {HOME_ID} across {len(JOURNEY)} constructed logins; sibling {SIBLING_ID}.")
    for obs in observations:
        print("OBS", obs)
    print("Asset is read through the Programme Manager login (proxy); no real Asset sign-in.")
    print("The 'no stage clears another' and eight-stage map statements are source design text only.")
    for item in DEFERRED:
        print(f"NOT RUN (out of scope): {item}")
    print("Partial subset only; no AC and no criterion is passed by this check.")


if __name__ == "__main__":
    main(run_browser, served_snapshot)
