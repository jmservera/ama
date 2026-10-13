"""SYNTHETIC DATA ONLY. Calendar, parameters and entity generation for the
Zava Forward year-one synthetic evidence pack. Nothing here is a Proper North
Homes fact."""
import math
import zlib
from dataclasses import dataclass, field
from datetime import date, timedelta

SIM_START = date(2025, 7, 1)
SNAP = date(2026, 9, 30)
BASELINE_START, BASELINE_END = date(2025, 7, 1), date(2026, 6, 30)
CODE_V2_FROM = date(2026, 2, 2)
RULE_V2_FROM = date(2026, 1, 12)

BANK_HOLIDAYS = {
    date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1),
    date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4), date(2026, 5, 25),
    date(2026, 8, 31),
}
SHUTDOWN = (date(2025, 12, 22), date(2026, 1, 2))
RC02_LEAVE = (date(2026, 1, 12), date(2026, 3, 27))
RC03_START = date(2026, 4, 13)
RLO03_LEFT = date(2026, 5, 15)
HP_CONSTRAINT = (date(2025, 10, 1), date(2025, 12, 31))

# Scenario parameters. These are the hidden levers; they are documented only
# in the answer key outside the knowledge base.
P = dict(
    rc_reviews_per_fte_day=1.75,
    design_return_base=0.20, design_return_arc06=0.34, design_return_early_bonus=0.07,
    f2_evidence_reject_first=0.45, f2_evidence_reject_later=0.20,
    other_evidence_reject_first=0.12, other_evidence_reject_later=0.08,
    na_working_hours=0.30, na_default=0.07, na_unmet_adjust_bonus=0.10,
    ref_misuse_install={"SUP-F1": 0.45, "SUP-HT": 0.45, "SUP-F2": 0.05, "SUP-HP": 0.05},
    ref_misuse_survey=0.20,
    reinstate_after_ref=0.40,
    hazard_base=0.08, hazard_per_damp_report=0.05, hazard_arc01_bonus=0.04,
    hard_to_reach=0.06, hard_to_reach_contact_p=0.08,
    zombie_share=0.55, zombie_never_released=0.25,
    pm_detect_at_design=0.62,
    stale_epc_already_c=0.25,
    void_rate=0.03, resident_pause_rate=0.03,
)

LOCALITIES = {
    "LA": "Locality A - urban core",
    "LB": "Locality B - former coalfield towns",
    "LC": "Locality C - rural and coastal",
}
LOCALITY_MIX = [("LA", 0.30), ("LB", 0.45), ("LC", 0.25)]
ARCH_BY_LOC = {
    "LA": [("ARC-03", 0.70), ("ARC-05", 0.20), ("ARC-02", 0.10)],
    "LB": [("ARC-01", 0.45), ("ARC-02", 0.35), ("ARC-06", 0.12), ("ARC-05", 0.08)],
    "LC": [("ARC-04", 0.55), ("ARC-02", 0.20), ("ARC-06", 0.15), ("ARC-05", 0.10)],
}
ARCHETYPES = {
    "ARC-01": ("Pre-1919 solid-wall terrace", (1880, 1919), "Solid brick", "Mains gas"),
    "ARC-02": ("1945-64 cavity-wall house", (1946, 1964), "Cavity brick", "Mains gas"),
    "ARC-03": ("1965-80 low-rise flat block", (1965, 1980), "Cavity brick, flat roof", "Mains gas"),
    "ARC-04": ("1960-80 off-gas bungalow", (1960, 1980), "Cavity brick", "Electric storage"),
    "ARC-05": ("1980-99 house", (1980, 1999), "Cavity brick, partial fill", "Mains gas"),
    "ARC-06": ("Non-traditional PRC house", (1946, 1958), "Precast reinforced concrete", "Mains gas"),
}
SUPPLIERS = {
    "SUP-F1": "Fabric contractor 1 (cavity, loft, internal wall insulation)",
    "SUP-F2": "Fabric contractor 2 (external wall insulation)",
    "SUP-HP": "Heat pump installer",
    "SUP-HT": "Heating contractor (boilers and controls)",
}
STAFF = {
    "PM-01": "Retrofit Programme Manager", "PS-01": "Programme Support Officer",
    "RC-01": "Retrofit Coordinator", "RC-02": "Retrofit Coordinator",
    "RC-03": "Retrofit Coordinator (framework, part time)",
    "RLO-01": "Resident Liaison Officer", "RLO-02": "Resident Liaison Officer",
    "RLO-03": "Resident Liaison Officer (left May 2026)",
    "GEO-01": "Grants and Evidence Officer", "QA-01": "Quality Inspector",
    "BSL-01": "Building Safety Liaison",
}


def is_wd(d):
    return d.weekday() < 5 and d not in BANK_HOLIDAYS


def in_shutdown(d):
    return SHUTDOWN[0] <= d <= SHUTDOWN[1]


def add_wd(d, n):
    n = max(0, int(n))
    while not is_wd(d) or in_shutdown(d):
        d += timedelta(days=1)
    while n > 0:
        d += timedelta(days=1)
        if is_wd(d) and not in_shutdown(d):
            n -= 1
    return d


def last_wd_of_month(d):
    nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    x = nxt - timedelta(days=1)
    while not is_wd(x):
        x -= timedelta(days=1)
    return x


def closure_sweep_on_or_after(d):
    """Programme closure sweep: last Thursday of each month."""
    cur = d
    for _ in range(3):
        nxt = date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
        x = nxt - timedelta(days=1)
        while x.weekday() != 3:
            x -= timedelta(days=1)
        if x >= d:
            return x
        cur = nxt
    return x


def quarter_end(d):
    m = ((d.month - 1) // 3 + 1) * 3
    return last_wd_of_month(date(d.year, m, 1))


def month_ends():
    out, d = [], SIM_START
    while d <= SNAP:
        me = date(d.year + (d.month == 12), d.month % 12 + 1, 1) - timedelta(days=1)
        out.append(min(me, SNAP))
        d = me + timedelta(days=1)
    return out


def stable_rand(*parts):
    """Deterministic pseudo-random in [0,1) from string parts."""
    return (zlib.crc32("|".join(map(str, parts)).encode()) % 1_000_003) / 1_000_003


def pick(rng, pairs):
    r, acc = rng.random(), 0.0
    for v, w in pairs:
        acc += w
        if r < acc:
            return v
    return pairs[-1][0]


def lognorm(rng, median, sigma=0.5, lo=0, hi=None):
    v = median * math.exp(rng.gauss(0, sigma))
    v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return int(round(v))


@dataclass
class Building:
    building_id: str
    locality: str
    archetype: str
    shared_system_id: str = ""
    leaseholders: int = 0
    flats: list = field(default_factory=list)
    lease_start: date = None
    lease_done: date = None
    released: bool = False
    first_ready: date = None


@dataclass
class Prop:
    property_id: str
    legacy_ref: str
    uprn: str
    building: Building
    heritage: str
    locality: str
    archetype: str
    property_type: str
    year_built: int
    tenure: str
    epc_band: str
    epc_sap: int
    epc_lodged: date
    true_sap: int
    roof_due: int
    windows_due: int
    damp_reports: int
    sold: bool
    address_legacy: str


@dataclass
class Household:
    resident_ref: str
    channel: str
    working_hours_unavailable: bool
    working_hours_recorded: bool
    adjustment: str
    adjustment_recorded: bool
    priority_support: bool
    auth_rep: bool
    hard_to_reach: bool = False


def band_from_sap(s):
    for lim, b in [(92, "A"), (81, "B"), (69, "C"), (55, "D"), (39, "E"), (21, "F")]:
        if s >= lim:
            return b
    return "G"


def make_household(rng, n):
    adj = pick(rng, [("None", 0.85), ("Large print", 0.04), ("Interpreter", 0.03),
                     ("BSL", 0.005), ("Advocate or representative", 0.035),
                     ("Communication support", 0.04)])
    wh = rng.random() < 0.24
    return Household(
        resident_ref=f"R-SYN-{n:05d}",
        channel=pick(rng, [("Phone", 0.5), ("Text message", 0.25), ("Letter", 0.15), ("Email", 0.10)]),
        working_hours_unavailable=wh,
        working_hours_recorded=wh and rng.random() < 0.55,
        adjustment=adj,
        adjustment_recorded=adj != "None" and rng.random() < 0.70,
        priority_support=rng.random() < 0.18,
        auth_rep=adj == "Advocate or representative" or rng.random() < 0.02,
        hard_to_reach=rng.random() < P["hard_to_reach"],
    )


STREETS = ["Harebell", "Linnet", "Quarry", "Colliery", "Beck", "Moorside", "Chapel",
           "Mill", "Heather", "Plover", "Sandpiper", "Tern", "Foundry", "Ashlar"]
SUFFIX = ["Walk", "Row", "Terrace", "Close", "Lane", "Grove", "View"]


def make_properties(rng, n_target):
    """Create buildings and candidate properties."""
    props, buildings = [], []
    pid = 0
    bid = 0
    hetA, hetB = 40000, 10000
    while len(props) < n_target:
        loc = pick(rng, LOCALITY_MIX)
        arc = pick(rng, ARCH_BY_LOC[loc])
        # Blocks hold many homes, so draw them less often to keep flats near a fifth of candidates.
        while arc == "ARC-03" and rng.random() > 0.03:
            arc = pick(rng, ARCH_BY_LOC[loc])
        bid += 1
        b = Building(f"SYN-BLDG-{bid:05d}", loc, arc)
        if arc == "ARC-03":
            nflats = rng.randint(6, 14)
            b.shared_system_id = f"SYS-ENV-{bid:05d}"
            b.leaseholders = 0 if rng.random() < 0.35 else rng.randint(1, 4)
        else:
            nflats = 1
        buildings.append(b)
        name, (y0, y1), constr, fuel = ARCHETYPES[arc]
        yb = rng.randint(y0, y1)
        street = f"{rng.choice(STREETS)} {rng.choice(SUFFIX)}"
        roof_base = 0.22 if (loc == "LB" and arc in ("ARC-01", "ARC-02")) else 0.06
        roof_due = rng.randint(2026, 2027) if rng.random() < roof_base else rng.randint(2029, 2045)
        win_due = rng.randint(2026, 2027) if (arc in ("ARC-03", "ARC-06") and rng.random() < 0.12) else rng.randint(2029, 2042)
        for f in range(nflats):
            pid += 1
            heritage = "Heritage A" if (loc == "LA" or (loc == "LB" and rng.random() < 0.5)) else "Heritage B"
            if heritage == "Heritage A":
                hetA += rng.randint(1, 7)
                legacy = f"HA-{hetA:06d}"
            else:
                hetB += rng.randint(1, 9)
                legacy = f"HB/{hetB:05d}"
            band = pick(rng, [("D", 0.55), ("E", 0.32), ("F", 0.10), ("G", 0.03)])
            sap = {"D": rng.randint(55, 68), "E": rng.randint(39, 54),
                   "F": rng.randint(21, 38), "G": rng.randint(8, 20)}[band]
            lodged = date(2009, 1, 1) + timedelta(days=rng.randint(0, 5800))
            true_sap = sap
            if lodged < date(2015, 10, 1) and band == "D" and rng.random() < P["stale_epc_already_c"]:
                true_sap = rng.randint(69, 74)
            elif rng.random() < 0.5:
                true_sap = max(5, sap + rng.randint(-4, 4))
            if arc == "ARC-03":
                ptype = "Low-rise flat"
                addr = f"Flat {f + 1}, Block {bid % 97}, {street}"
            else:
                ptype = {"ARC-01": rng.choice(["Mid terrace", "End terrace"]),
                         "ARC-02": rng.choice(["Semi-detached", "End terrace", "Mid terrace"]),
                         "ARC-04": "Bungalow", "ARC-05": rng.choice(["Semi-detached", "Detached", "Mid terrace"]),
                         "ARC-06": "Semi-detached"}[arc]
                addr = f"{rng.randint(1, 180)} {street}"
            tenure = pick(rng, [("Social rent", 0.84), ("Affordable rent", 0.12), ("Shared ownership", 0.04)])
            if arc == "ARC-03":
                tenure = pick(rng, [("Social rent", 0.9), ("Affordable rent", 0.1)])
            dr = min(6, int(rng.expovariate(1 / (0.9 if arc == "ARC-01" else 0.4))))
            p = Prop(
                property_id=f"SYN-PROP-{pid:06d}", legacy_ref=legacy,
                uprn=f"9990{rng.randint(10_000_000, 99_999_999)}",
                building=b, heritage=heritage, locality=loc, archetype=arc,
                property_type=ptype, year_built=yb, tenure=tenure,
                epc_band=band, epc_sap=sap, epc_lodged=lodged, true_sap=true_sap,
                roof_due=roof_due, windows_due=win_due, damp_reports=dr,
                sold=rng.random() < 0.009, address_legacy=f"{addr}, {LOCALITIES[loc].split(' - ')[0]}",
            )
            b.flats.append(p)
            props.append(p)
    return props, buildings


def measures_for(rng, arc):
    if arc == "ARC-01":
        if rng.random() < 0.6:
            return "Internal wall insulation; loft insulation; dMEV ventilation", "SUP-F1"
        return "External wall insulation; loft insulation; dMEV ventilation", "SUP-F2"
    if arc == "ARC-02":
        if rng.random() < 0.55:
            return "Cavity wall insulation; loft insulation; heating controls", "SUP-F1"
        return "Boiler replacement; heating controls; loft top-up", "SUP-HT"
    if arc == "ARC-03":
        return "External wall insulation (block); dMEV ventilation", "SUP-F2"
    if arc == "ARC-04":
        return "Air source heat pump; loft insulation; dMEV ventilation", "SUP-HP"
    if arc == "ARC-05":
        return "Boiler replacement; heating controls; loft top-up", "SUP-HT"
    return "External wall insulation; loft insulation; dMEV ventilation; structural repair", "SUP-F2"


def priority_score(p, hh, rule, rng):
    base = {"G": 40, "F": 32, "E": 24, "D": 14, "C": 5}[p.epc_band]
    damp_w = 5 if rule == "SEL-2025.1" else 10
    s = base + damp_w * min(p.damp_reports, 3) + (5 if hh.priority_support else 0)
    s += 8 if p.archetype in ("ARC-03", "ARC-06") else 0
    return int(min(99, s + rng.randint(0, 12)))
