"""Read-only views over the case data: filters, statistics, map, visits, handover suggestions."""
from collections import Counter, defaultdict

STAGE_ORDER = ["Home identified", "Checking lease", "Rescheduled", "Contacting resident", "Contact paused",
               "Survey being booked", "Survey booked", "Survey write-up", "Design starting", "Design in progress",
               "Design awaiting approval", "Design being corrected", "Waiting on other works",
               "Waiting for resident decision", "Resident paused works", "Funding check",
               "Final checks before ordering", "Waiting for block programme", "With contractor", "Install booked",
               "Works under way", "Handover to arrange", "Quality check", "Closing down", "Aftercare issue"]
LONG_WAIT = 60

RESIDENT_STAGES = {"Home identified", "Checking lease", "Rescheduled", "Contacting resident", "Contact paused",
                   "Survey being booked", "Survey booked", "Waiting for resident decision", "Resident paused works",
                   "Handover to arrange", "Aftercare issue"}
ROLE_BY_STAGE = {"Funding check": "Grants and Evidence Officer", "Final checks before ordering": "Grants and Evidence Officer",
                 "Quality check": "Quality Inspector", "Closing down": "Quality Inspector"}
SORTS = {
    "urgent": "Most urgent first",
    "waiting": "Waiting longest",
    "contact": "Longest since last contact",
    "name": "Resident A to Z",
    "visit": "Next visit soonest",
}


def has_hazard(c):
    return any(not h["released"] for h in c["hazards"])


def preferred_role(c):
    if has_hazard(c):
        return "Building Safety Liaison"
    if c["stage"] in ROLE_BY_STAGE:
        return ROLE_BY_STAGE[c["stage"]]
    if c["stage"] in RESIDENT_STAGES:
        return "Resident Liaison Officer"
    return "Retrofit Coordinator"


def matches(c, f):
    if f.get("stage") and c["stage"] != f["stage"]:
        return False
    if f.get("area") and c["home"]["area"] != f["area"]:
        return False
    if f.get("wave") and c["wave"] != f["wave"]:
        return False
    if f.get("owner") and c["owner_code"] != f["owner"]:
        return False
    if f.get("contractor") and c["contractor"]["name"] != f["contractor"]:
        return False
    flag = f.get("flag")
    if flag == "hazard" and not has_hazard(c):
        return False
    if flag == "support" and not (c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None"):
        return False
    if flag == "long" and c["days_in_stage"] < LONG_WAIT:
        return False
    if flag == "nodecision" and c["decision"]["status"] in ("Accepted", "Declined"):
        return False
    if flag == "fundingprog" and c["funding"]["status"] in ("To prepare", "Draft ready", "Approved", "Submitted"):
        return True
    if flag == "fundingprog":
        return False
    if flag == "funding" and c["funding"]["status"] == "Confirmed":
        return False
    return True


def sort_key(sort):
    def nxt(s):
        return s["next_visit"] or "9999"
    keys = {
        "urgent": lambda s: s["rank"],
        "waiting": lambda s: -s["days"],
        "contact": lambda s: s["last_contact"] or "0000",
        "name": lambda s: s["resident"].split(" ")[-1].lower(),
        "visit": nxt,
    }
    return keys.get(sort, keys["urgent"])


def facets(cases):
    open_ = [c for c in cases if not c["closed"]]
    stages = Counter(c["stage"] for c in open_)
    return dict(
        stages=sorted(stages, key=lambda s: STAGE_ORDER.index(s) if s in STAGE_ORDER else 99),
        areas=sorted({c["home"]["area"] for c in open_}),
        waves=sorted({c["wave"] for c in open_}),
        contractors=sorted({c["contractor"]["name"] for c in open_}),
        sorts=SORTS)


def stats(cases, staff):
    open_ = [c for c in cases if not c["closed"]]
    by_stage = Counter(c["stage"] for c in open_)
    ages = Counter()
    for c in open_:
        d = c["days_in_stage"]
        ages["0 to 30 days" if d <= 30 else "31 to 60 days" if d <= 60 else "61 to 90 days" if d <= 90 else "Over 90 days"] += 1
    load = Counter(c["owner_code"] for c in open_)
    contractors = defaultdict(lambda: dict(open=0, booked=0, long=0))
    for c in open_:
        k = contractors[c["contractor"]["name"]]
        k["open"] += 1
        k["booked"] += c["stage"] in ("Install booked", "Works under way")
        k["long"] += c["stage"] in ("With contractor", "Install booked") and c["days_in_stage"] >= LONG_WAIT
    return dict(
        kpis=dict(open=len(open_), completed=len(cases) - len(open_), hazards=sum(has_hazard(c) for c in open_),
                  long=sum(c["days_in_stage"] >= LONG_WAIT for c in open_),
                  nodecision=sum(c["decision"]["status"] in ("Not yet asked", "Waiting") for c in open_),
                  funding=sum(c["funding"]["status"] in ("To prepare", "Draft ready", "Approved", "Submitted") for c in open_),
                  support=sum(c["resident"]["priority_support"] for c in open_)),
        stages=[dict(label=s, n=by_stage[s]) for s in sorted(by_stage, key=lambda s: STAGE_ORDER.index(s) if s in STAGE_ORDER else 99)],
        areas=[dict(label=k, n=v) for k, v in Counter(c["home"]["area"] for c in open_).most_common()],
        waves=[dict(label=k, n=v) for k, v in sorted(Counter(c["wave"] for c in open_).items())],
        ages=[dict(label=k, n=ages[k]) for k in ("0 to 30 days", "31 to 60 days", "61 to 90 days", "Over 90 days")],
        funding=[dict(label=k, n=v) for k, v in Counter(c["funding"]["status"] for c in open_).most_common()],
        contractors=[dict(name=k, **v) for k, v in sorted(contractors.items())],
        team=[dict(code=s["code"], name=s["name"], role=s["role"], open=load[s["code"]],
                   hazards=sum(1 for c in open_ if c["owner_code"] == s["code"] and has_hazard(c))) for s in staff])


def map_points(cases, f):
    out = []
    for c in cases:
        if c["closed"] or not matches(c, f):
            continue
        out.append(dict(id=c["id"], lat=c["home"]["lat"], lon=c["home"]["lon"], name=c["resident"]["name"],
                        address=f"{c['home']['address']}, {c['home']['postcode']}", stage=c["stage"],
                        kind="hazard" if has_hazard(c) else "long" if c["days_in_stage"] >= LONG_WAIT else "normal"))
    return out


MAP_CAP = 500


def map_view(cases, f, bbox=None, zoom=None, cap=MAP_CAP):
    """Points when few enough, otherwise grid clusters. bbox is (south, west, north, east)."""
    pts = []
    for c in cases:
        if c["closed"] or not matches(c, f):
            continue
        lat, lon = c["home"]["lat"], c["home"]["lon"]
        if bbox and not (bbox[0] <= lat <= bbox[2] and bbox[1] <= lon <= bbox[3]):
            continue
        pts.append((c, lat, lon))
    total = len(pts)
    bounds = [min(p[1] for p in pts), min(p[2] for p in pts), max(p[1] for p in pts), max(p[2] for p in pts)] if pts else None
    if total <= cap:
        items = [dict(id=c["id"], lat=lat, lon=lon, name=c["resident"]["name"],
                      address=f"{c['home']['address']}, {c['home']['postcode']}", stage=c["stage"],
                      kind="hazard" if has_hazard(c) else "long" if c["days_in_stage"] >= LONG_WAIT else "normal")
                 for c, lat, lon in sorted(pts, key=lambda p: p[0]["id"])]
        return dict(mode="points", total=total, shown=len(items), cap=cap, bounds=bounds, items=items)
    z = 8 if zoom is None else max(0, min(20, int(zoom)))
    cell = 360.0 / (2 ** z) / 4
    while True:
        cells = {}
        for c, lat, lon in pts:
            k = (int(lat // cell), int(lon // cell))
            g = cells.setdefault(k, [0, 0.0, 0.0, 0, 0])
            g[0] += 1
            g[1] += lat
            g[2] += lon
            g[3] += has_hazard(c)
            g[4] += c["days_in_stage"] >= LONG_WAIT
        if len(cells) <= cap:
            break
        cell *= 2
    items = [dict(lat=g[1] / g[0], lon=g[2] / g[0], count=g[0], hazards=g[3], long=g[4], key=f"{k[0]}:{k[1]}")
             for k, g in sorted(cells.items())]
    return dict(mode="clusters", total=total, shown=len(items), cap=cap, bounds=bounds, items=items)


def visits(cases, owner=None):
    out = []
    for c in cases:
        if c["closed"] or (owner and c["owner_code"] != owner):
            continue
        for a in c["appointments"]:
            if a["outcome"] == "Booked":
                out.append(dict(id=c["id"], date=a["date"], slot=a["slot"], type=a["type"], resident=c["resident"]["name"],
                                address=f"{c['home']['address']}, {c['home']['town']} {c['home']['postcode']}",
                                who=a["who"], person=a["person"], support=c["resident"]["adjustment"] != "None",
                                phone=c["resident"]["phone"], owner=c["owner"]))
    return sorted(out, key=lambda v: (v["date"], v["slot"]))


def recommend_handover(c, cases, staff):
    """Rank colleagues with plain reasons: role fit, current workload, who already knows the resident."""
    want = preferred_role(c)
    load = Counter(x["owner_code"] for x in cases if not x["closed"])
    avg = sum(load.values()) / max(1, len(staff))
    known = {k["by"] for k in c["contacts"]}
    out = []
    for s in staff:
        if s["code"] == c["owner_code"]:
            continue
        score, why = 0, []
        if s["role"] == want:
            score += 50
            why.append(f"{s['role']}: the usual role for '{c['stage'].lower()}'")
        elif s["role"] in ("Retrofit Programme Manager", "Programme Support Officer"):
            score += 10
            why.append("Can pick up anything when needed")
        if s["name"] in known:
            score += 20
            why.append("Has already spoken to this resident")
        n = load[s["code"]]
        score += max(-20, min(30, round((avg - n) * 1.5)))
        why.append(f"{n} open cases (team average {avg:.0f})")
        if has_hazard(c) and s["role"] == "Building Safety Liaison":
            score += 20
            why.append("Owns open safety issues")
        out.append(dict(email=s["email"], name=s["name"], role=s["role"], score=score, reasons=why))
    return sorted(out, key=lambda x: -x["score"])[:3]
