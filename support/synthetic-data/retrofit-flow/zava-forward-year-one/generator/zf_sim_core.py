"""SYNTHETIC DATA ONLY. Discrete-event core for the Zava Forward year-one
synthetic scenario: candidates, capacity-limited servers and scheduling."""
import heapq
from dataclasses import dataclass, field
from datetime import date, timedelta

from zf_model import (P, SNAP, SHUTDOWN, RC02_LEAVE, RC03_START, HP_CONSTRAINT,
                      in_shutdown, is_wd, quarter_end, month_ends)


@dataclass
class Cand:
    cid: str
    prop: object
    hh: object
    wave: str
    identified: date
    rule: str
    score: int
    measures: str
    supplier: str
    events: list = field(default_factory=list)
    contacts: list = field(default_factory=list)
    appts: list = field(default_factory=list)
    quality: list = field(default_factory=list)
    segments: list = field(default_factory=list)
    state: str = "Not yet identified"
    cat: str = ""
    since: date = None
    token: int = 0
    closed: bool = False
    exit_type: str = ""
    exit_reason: str = ""
    flags: set = field(default_factory=set)
    n: dict = field(default_factory=lambda: {"ref": 0, "na": 0, "returns": 0, "qa_fail": 0,
                                               "ev_reject": 0, "ev_version": 0, "contact_cycles": 0})
    dates: dict = field(default_factory=dict)
    funding_route: str = ""
    hold: dict = None
    gate: dict = field(default_factory=dict)
    pm_undetected: bool = False
    owner_rlo: str = ""
    owner_rc: str = ""
    history: list = field(default_factory=list)  # (date, state) true state history


class Server:
    def __init__(self, name, cap_fn):
        self.name, self.cap_fn = name, cap_fn
        self.q, self.credit, self.seq = [], 0.0, 0
        self.log = []   # (serve_date, cid, weight, arrival)
        self.arrivals = []  # (date, cid, weight)

    def request(self, d, cand, cb, prio=1, weight=1.0, **kw):
        self.seq += 1
        self.arrivals.append((d, cand.cid, weight))
        heapq.heappush(self.q, (prio, d, self.seq, cand, cb, weight, cand.token, kw))

    def serve(self, d, sim):
        cap = self.cap_fn(d)
        if not self.q:
            self.credit = min(self.credit, 0.0)
            return
        self.credit = min(self.credit, cap) + cap
        while self.q:
            prio, arr, s, cand, cb, w, tok, kw = self.q[0]
            if cand.closed or cand.token != tok:
                heapq.heappop(self.q)
                continue
            if self.credit + 1e-9 < min(w, 3.0):
                break
            heapq.heappop(self.q)
            self.credit -= w
            self.log.append((d, cand.cid, w, arr))
            getattr(sim, cb)(cand, d, **kw)


def fte_rc(d):
    f = 1.0
    f += 0.0 if RC02_LEAVE[0] <= d <= RC02_LEAVE[1] else 1.0
    f += 0.6 if d >= RC03_START else 0.0
    return f


def cap_rc(d):
    if in_shutdown(d):
        return 0.0
    return fte_rc(d) * P["rc_reviews_per_fte_day"]


def cap_survey(d):
    if in_shutdown(d):
        return 0.0
    return 4.0 if d < date(2025, 10, 1) else 6.5


def cap_supplier(sup):
    def f(d):
        if in_shutdown(d):
            return 0.0
        if sup == "SUP-F1":
            return 3.0
        if sup == "SUP-F2":
            return 0.9 if d.month in (12, 1, 2) else 1.8
        if sup == "SUP-HP":
            return 0.3 if HP_CONSTRAINT[0] <= d <= HP_CONSTRAINT[1] else 1.1
        return 2.0
    return f


def cap_qa(d):
    return 0.0 if in_shutdown(d) else 3.0


def cap_geo(d):
    if in_shutdown(d) or date(2026, 8, 10) <= d <= date(2026, 8, 21):
        return 0.0
    qe = quarter_end(d)
    if 0 <= (qe - d).days <= 13:
        return 0.6
    return 3.0


class SimCore:
    def __init__(self, rng, cands, buildings):
        self.rng = rng
        self.cands = cands
        self.buildings = buildings
        self.heap, self.seq = [], 0
        self.today = None
        self.servers = {
            "SURVEY": Server("SURVEY", cap_survey),
            "RC": Server("RC", cap_rc),
            "QA": Server("QA", cap_qa),
            "GEO": Server("GEO", cap_geo),
        }
        for s in ("SUP-F1", "SUP-F2", "SUP-HP", "SUP-HT"):
            self.servers[s] = Server(s, cap_supplier(s))
        self.month_snaps = {}
        self.hazards = []
        self.claims = []
        self.issues = []
        self.work_orders = []   # (date, cid, supplier)
        self.install_starts = []
        self.install_completes = []

    # scheduling -------------------------------------------------------
    def at(self, d, c, fn, **kw):
        self.seq += 1
        heapq.heappush(self.heap, (d, self.seq, c, fn, c.token, kw))

    def _drain(self, d):
        while self.heap and self.heap[0][0] <= d:
            ed, _, c, fn, tok, kw = heapq.heappop(self.heap)
            if c.closed and fn not in ("h_aftercare", "h_reclose", "h_hold_release",
                                       "h_repair_complete", "h_claim_received"):
                continue
            if tok != c.token and not fn.startswith("h_hold") and fn != "h_repair_complete":
                continue
            # Hazard events can be scheduled back to the survey date; keep their true date.
            self.today = ed
            getattr(self, fn)(c, ed, **kw)

    def run(self, start):
        mes = set(month_ends())
        d = start
        while d <= SNAP:
            self._drain(d)
            if is_wd(d):
                for s in self.servers.values():
                    s.serve(d, self)
                self._drain(d)
            self.daily(d)
            if d in mes:
                self.snapshot(d)
            d += timedelta(days=1)
        for c in self.cands:
            if c.since is not None and not c.closed:
                c.segments.append((c.cat, c.since, SNAP, c.state, "open"))

    # state and records -------------------------------------------------
    def set_state(self, c, d, state, cat):
        if c.since is not None and c.state != "Not yet identified":
            c.segments.append((c.cat, c.since, d, c.state, "closed"))
        c.state, c.cat, c.since = state, cat, d
        c.history.append((d, state, cat))

    def ev(self, c, d, etype, source, actor, from_team="", to_team="", outcome="",
           reason="", notes="", evidence_version=""):
        c.events.append(dict(date=d, type=etype, source=source, actor=actor,
                             from_team=from_team, to_team=to_team, outcome=outcome,
                             reason=reason, notes=notes, evidence_version=evidence_version))

    def exit(self, c, d, kind, reason, cat="EXIT"):
        self.set_state(c, d, kind, cat)
        c.segments.append((cat, d, d, kind, "closed"))
        c.closed, c.exit_type, c.exit_reason = True, kind, reason
        c.token += 1
        self.ev(c, d, "CASE_EXITED" if kind != "Accepted handover" else "ACCEPTED_HANDOVER",
                "TRACKER", "PM-01", outcome=kind, reason=reason)

    def daily(self, d):
        pass

    def snapshot(self, d):
        self.month_snaps[d] = [(c.cid, c.state, c.cat, c.since, c.closed, dict(c.dates),
                                bool(c.hold and c.hold.get("placed") and c.hold["placed"] <= d
                                     and not (c.hold.get("released") and c.hold["released"] <= d)))
                               for c in self.cands if c.identified <= d]
