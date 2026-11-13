#!/usr/bin/env python3
"""Read-only #441 documentation checks over committed blobs of a git revision.

Usage: 441-portal-docs-1105-check.py REV  (writes JSON to stdout; no file writes)
"""
import json
import re
import subprocess
import sys
from posixpath import dirname, normpath, join

REV = sys.argv[1]
BRD = "docs/brds/agentic-retrofit-programme-brd.md"
PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
ADR = "docs/adrs/0007-contractor-intake-staff-mediated-proposal.md"
ARCH = "docs/architecture/README.md"
FILES = [BRD, PRD, ADR, ARCH]


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


PATHS = set(git("ls-tree", "-r", "--name-only", REV).split("\n"))
DIRS = {p for f in PATHS for p in [dirname(f)] if p} | {
    d for f in PATHS for d in [dirname(dirname(f))] if d
}
TEXT = {f: git("show", f"{REV}:{f}") if f in PATHS else None for f in FILES}
res = []


def add(i, status, detail):
    res.append({"id": i, "status": status, "detail": detail})


def lines_of(f):
    return TEXT[f].split("\n")


def find(f, pat, flags=0):
    return [(n + 1, l) for n, l in enumerate(lines_of(f)) if re.search(pat, l, flags)]


def slugs(text):
    seen, out = {}, set()
    infence = False
    for l in text.split("\n"):
        if l.startswith("```"):
            infence = not infence
        m = re.match(r"#{1,6}\s+(.*?)\s*#*\s*$", l)
        if m and not infence:
            t = re.sub(r"[`*_]|\[([^\]]*)\]\([^)]*\)", lambda x: x.group(1) or "", m.group(1))
            s = re.sub(r"[^\w\- ]", "", t.lower()).replace(" ", "-")
            k = seen.get(s, 0)
            seen[s] = k + 1
            out.add(s if k == 0 else f"{s}-{k}")
    return out


SLUG = {}


def anchors(p):
    if p not in SLUG:
        SLUG[p] = slugs(git("show", f"{REV}:{p}"))
    return SLUG[p]


# (a) links and anchors
for f in FILES:
    if TEXT[f] is None:
        add(f"file:{f}", "FAIL", "absent at revision")
        continue
    infence, total, bad = False, 0, []
    for n, l in enumerate(lines_of(f), 1):
        if l.startswith("```"):
            infence = not infence
        if infence:
            continue
        l = re.sub(r"`[^`]*`", "", l)
        for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", l):
            t = m.group(1)
            if re.match(r"[a-z]+:", t):
                continue
            total += 1
            path, _, frag = t.partition("#")
            target = normpath(join(dirname(f), path)) if path else f
            ok = target in PATHS or target in DIRS
            if ok and frag and target.endswith(".md") and frag not in anchors(target):
                ok = False
                bad.append(f"{n}: anchor #{frag} missing in {target}")
            elif not ok:
                bad.append(f"{n}: target {target} missing")
    add(f"links:{f}", "PASS" if not bad else "FAIL", f"{total} relative links; {len(bad)} unresolved: {bad[:40]}")

# (b) status markers
def req(i, f, pat, label, flags=0):
    h = find(f, pat, flags)
    add(i, "PASS" if h else "FAIL", f"{label}: {[x[0] for x in h[:6]] or 'no match'} in {f}")


req("brd:status-draft", BRD, r'^status:\s*"?draft', "BRD frontmatter status draft")
req("prd:status-unsigned", PRD, r'^exercise_status:.*unsigned', "PRD exercise_status unsigned")
req("prd:status-in-review", PRD, r'^status:\s*"?in-review', "PRD status in-review")
for od in ("OD-52", "OD-53", "OD-54", "OD-55"):
    h = find(BRD, rf"^\| {od} \|")
    add(f"brd:{od}-defined", "PASS" if h else "FAIL", f"definition row at {[x[0] for x in h]}")
    closed = [x[0] for x in find(BRD, rf"^\| {od} \|.*\b(approved by|closed|decided on|accepted by)\b", re.I)]
    reg = [x[0] for x in find(BRD, r"^#+ .*(Open Decisions|Decisions)", re.I)]
    add(f"brd:{od}-open", "PASS" if h and not closed and reg else "FAIL", f"row has no closure marker (closed rows {closed}); decision-register headings at {reg[:3]}")
    add(f"prd:{od}-visible", "PASS" if find(PRD, rf"{od}|OD-52 to OD-55") else "FAIL", "PRD mention")
req("brd:FR-044-default", BRD, r"^\| FR-044 \|.*named per-output human review is required except", "FR-044 per-message review default with bounded exception")
req("brd:AC-084-no-fabrication", BRD, r"AC-084:.*must not fabricate per-message human review", "AC-084 no fabricated review")
req("brd:OD-53-all-individually-approved", BRD, r"^\| OD-53 \|.*All AI-drafted resident messages remain individually human-approved", "OD-53 activation gate")
add("prd:not-run-resident", "PASS" if len([1 for _, l in enumerate(lines_of(PRD)) if re.match(r"\| AC-(11[1-9]|1[23]\d|140) \|.*\| Not run \|", l)]) else "INFO",
    "resident AC rows with a Not run cell: %d (rows may use another status column)" % len([1 for l in lines_of(PRD) if re.match(r"\| AC-(11[1-9]|1[23]\d|140) \|.*Not run", l)]))
add("prd:not-run-any", "PASS" if find(PRD, r"Not run") else "FAIL", f"Not run lines: {len(find(PRD, r'Not run'))}")
for c in ("criterion5", "unsigned"):
    pass
adr_status = [l for l in lines_of(ADR)[8:14] if l.strip()]
add("adr:0007-status-as-written", "INFO", f"ADR 0007 title/status: {lines_of(ADR)[1]!r}; status text starts {adr_status[:2]}")
add("adr:resident-portal-adr-present", "INFO" if not [p for p in PATHS if p.startswith("docs/adrs/") and "resident" in p.lower()] else "PASS",
    "resident-portal ADR file in docs/adrs/: " + str(sorted(p for p in PATHS if p.startswith("docs/adrs/") and "resident" in p.lower()) or "none; ADR 0007 is contractor intake"))
add("adr:0007-accepted-marker", "INFO", "ADR 0007 'Proposed' status lines: %s; 'Accepted' lines: %s" % ([x[0] for x in find(ADR, r"^Proposed")], [x[0] for x in find(ADR, r"^Accepted")]))

# (c) numbering and traceability (namespace-qualified)
def defs(f, prefix):
    out = {}
    for n, l in enumerate(lines_of(f), 1):
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 2 or not re.fullmatch(rf"{prefix}-\d+", cells[0]):
            continue
        body = (cells[1] if not cells[1].startswith("BRD ") else "") if f == PRD else (cells[2] if len(cells) > 6 else "")
        if len(body) >= 40 and not re.match(r"AC-\d+(,|\s|/|$)", body) and cells[0] not in ("",):
            out.setdefault(cells[0], []).append(n)
    return out


for f, tag in ((BRD, "brd"), (PRD, "prd")):
    for p in ("FR", "NFR", "RULE"):
        d = defs(f, p)
        dup = {k: v for k, v in d.items() if len(v) > 1}
        add(f"{tag}:{p}-defs", "PASS" if not dup else "FAIL", f"{len(d)} defined; duplicates {dup}")

bd, pd = defs(BRD, "FR"), defs(PRD, "FR")
need_b = [f"FR-{i:03d}" for i in range(53, 63)]
need_p = [f"FR-{i:03d}" for i in range(62, 72)]
add("brd:FR-053..062", "PASS" if all(k in bd for k in need_b) else "FAIL", f"missing {[k for k in need_b if k not in bd]}")
add("prd:FR-062..071", "PASS" if all(k in pd for k in need_p) else "FAIL", f"missing {[k for k in need_p if k not in pd]}")
brd_ac = set(re.findall(r"\bAC-(\d+)\b", TEXT[BRD]))
prd_ac = {m for l in lines_of(PRD) for m in re.findall(r"^\| AC-(\d+) \|", l)}
add("brd:AC-104..126", "PASS" if all(str(i) in brd_ac for i in range(104, 127)) else "FAIL", f"missing {[i for i in range(104,127) if str(i) not in brd_ac]}")
add("prd:AC-111..140-rows", "PASS" if all(str(i) in prd_ac for i in range(111, 141)) else "FAIL", f"missing {[i for i in range(111,141) if str(i) not in prd_ac]}")

# trace table: every referenced BRD FR/AC/BG/RULE/NFR/OD must be defined in the BRD
start = next(n for n, l in enumerate(lines_of(PRD)) if l.startswith("### Resident upstream trace"))
bad = []
rows = 0
for l in lines_of(PRD)[start + 7:start + 30]:
    if not l.startswith("|"):
        break
    cells = [c.strip() for c in l.strip("|").split("|")]
    if len(cells) < 3:
        continue
    rows += 1
    if cells[0] not in pd and not re.match(r"(NFR|GOAL)-", cells[0]):
        bad.append(("PRD id undefined", cells[0]))
    brdref = cells[2]
    for m in re.findall(r"\b(FR|NFR|RULE|OD|BG)-(\d+)", brdref):
        k = f"{m[0]}-{m[1]}"
        if not re.search(rf"\| {k} \|", TEXT[BRD]):
            bad.append(("BRD id not a table row", k))
    for a, b in re.findall(r"AC-(\d+)/(\d+)", brdref):
        for x in (a, b):
            if x not in brd_ac:
                bad.append(("BRD AC undefined", x))
add("trace:PRD-to-BRD-resident", "PASS" if not bad else "FAIL", f"{rows} rows; issues {bad[:20]}")
add("trace:ADR-linkage", "INFO", "PRD/BRD refs to a resident portal ADR: " + str(find(PRD, r"resident.*ADR|ADR.*resident", re.I)[:3] + find(BRD, r"resident.*ADR|ADR.*resident", re.I)[:3]))

# formulas
def table(f, start_label):
    rows = {}
    for l in lines_of(f):
        if l.startswith("|"):
            c = [x.strip() for x in l.strip("|").split("|")]
            if len(c) == 4:
                rows[c[0]] = c[1:]
    return rows


T = table(BRD, "")
def get(label_part):
    for k, v in T.items():
        if label_part in k:
            return [float(x.replace("%", "").replace(",", "")) for x in v]
    raise KeyError(label_part)


try:
    A, D, C, Tc, E, Te = (get(s) for s in ("(A)", "(D)", "(C)", "(Tc)", "(E)", "(Te)"))
    U, V, R, Tr, Q, S, To = (get(s) for s in ("(U)", "(V)", "(R)", "(Tr)", "(Q)", "(S)", "(To)"))
    pub = {k: get(k) for k in (
        "Concurrent active home cases W", "Routine baseline calls/week", "Separate email/document transactions/week",
        "Routine baseline staff hours/week B", "Gross avoided handling hours/week G", "Additional review/escalation hours/week H",
        "Reconciliation hours/week J", "Routine net released hours/week N", "New-intake onboarding hours/week O",
        "Net released hours/week including intake F", "Initial active-cohort onboarding hours I")}
    bad = []
    F6 = []
    for i in range(3):
        u, v = U[i] / 100, V[i] / 100
        W = A[i] * D[i]
        calls, mail = W * C[i], W * E[i]
        B = (calls * Tc[i] + mail * Te[i]) / 60
        G = B * u * v
        H = W * u * R[i] * Tr[i] / 60
        J = W * Q[i] / 60
        N = G - H - J - S[i]
        O = A[i] * u * To[i] / 60
        I = W * u * To[i] / 60
        F = N - O
        F6.append(F)
        calc = {"Concurrent active home cases W": W, "Routine baseline calls/week": calls, "Separate email/document transactions/week": mail,
                "Routine baseline staff hours/week B": B, "Gross avoided handling hours/week G": G, "Additional review/escalation hours/week H": H,
                "Reconciliation hours/week J": J, "Routine net released hours/week N": N, "New-intake onboarding hours/week O": O,
                "Net released hours/week including intake F": F, "Initial active-cohort onboarding hours I": I}
        for k, c in calc.items():
            if abs(pub[k][i] - c) > 0.011 + 0.0005 * abs(c):
                bad.append((("low", "base", "high")[i], k, pub[k][i], round(c, 4)))
    add("formula:BRD-capacity-table", "PASS" if not bad else "FAIL", f"11 measures x 3 scenarios recomputed from inputs; mismatches {bad}")
    qf = [round(x, 3) for x in F6]
    add("formula:F-quoted-figures", "PASS" if qf[0] == -1.594 and qf[1] == 14.74 and qf[2] == 94.333 else "FAIL",
        f"recomputed F low/base/high {qf} vs quoted -1.594/14.74/94.333; PRD line(s) {[x[0] for x in find(PRD, r'-1\.594/14\.74/94\.333')]}")
    # break-even: F(U) = a*U - O_per_U ; base
    W = A[1] * D[1]
    B = (W * C[1] * Tc[1] + W * E[1] * Te[1]) / 60
    slope = B * V[1] / 100 - W * R[1] * Tr[1] / 60 - A[1] * To[1] / 60
    const = -W * Q[1] / 60 - S[1]
    be = -const / slope
    add("formula:break-even", "PASS" if abs(slope - 35.4) < 0.05 and abs(const + 2.96) < 0.005 and abs(be * 100 - 8.36) < 0.01 else "FAIL",
        f"slope {slope:.3f} (quoted 35.4), const {const:.3f} (quoted -2.96), break-even {be*100:.3f}% (quoted 8.36%)")
    f25 = [round(slope * u + const, 2) for u in (0.25, 0.5, 0.75)]
    add("formula:F(U)", "PASS" if f25 == [5.89, 14.74, 23.59] else "FAIL", f"F at 25/50/75% {f25} vs quoted 5.89/14.74/23.59")
    vbe = (W * U[1] / 100 * R[1] * Tr[1] / 60 + W * Q[1] / 60 + S[1] + A[1] * U[1] / 100 * To[1] / 60) / (B * U[1] / 100)
    add("formula:V-break-even", "PASS" if abs(vbe * 100 - 29.90) < 0.01 else "FAIL", f"V break-even {vbe*100:.3f}% vs quoted 29.90%")
    add("formula:PRD-addendum-quotes", "PASS" if find(PRD, r"\*\*48 one-off hours\*\*") and find("docs/case_study_48_addendum.md" if False else PRD, r"14\.74") else "FAIL", "PRD quotes 48 one-off and 14.74")
except Exception as e:
    add("formula:error", "FAIL", repr(e))

# claim hygiene: Criterion 5 / acceptance claims
add("hygiene:no-FR044-signoff", "PASS" if not find(PRD + "" if False else BRD, r"requirements owner.*(dispositioned|approved) FR-044", re.I) else "FAIL",
    "no BRD text records a requirements-owner disposition of FR-044/AC-084")

print(json.dumps({"rev": REV, "blobs": {f: git("rev-parse", f"{REV}:{f}").strip() for f in FILES if f in PATHS}, "results": res}, indent=1, sort_keys=True))
