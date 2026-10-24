"""Read-only issue 441 document checks; writes only the explicitly requested report."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import unicodedata
from urllib.parse import unquote
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = "140d8f494482c78e84d15f3d46b9223d3c487af0"
BRD = "docs/brds/agentic-retrofit-programme-brd.md"
PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
CANONICAL_DOCS = frozenset({
    BRD, PRD, "docs/architecture/README.md", "docs/capstone/README.md",
    "docs/case_study_48_addendum.md", "docs/reference/README.md", "docs/reference/log.md",
    "docs/reference/research/company/agent-request-challenge.md",
    "docs/reference/research/company/agent-what-if-study.md",
    "docs/reference/research/ux/content-standard.md",
    "docs/reference/research/ux/customer-journeys/customer-journey-atlas.md",
    "docs/reference/research/ux/customer-journeys/frontline.md",
    "docs/reference/research/ux/customer-journeys/residents.md",
    "docs/reference/research/ux/design-system.md",
    "docs/reference/research/ux/wcag-conformance-baseline.md",
    "docs/reference/research/ux/zava-forward-prototype-profile-review.md",
})
TASK = "resident-portal-requirements-441"
TRACKING = re.compile(
    r"\.copilot-tracking/(?:research|plans|details|changes|reviews/plans|reviews/logs|rpi-sessions)"
    r"/\d{4}-\d{2}-\d{2}/" + TASK + r"(?:-[a-z0-9][a-z0-9-]*)?\.(?:md|json)"
)
PACKAGE = HERE.relative_to(ROOT).as_posix() + "/"


def git_bytes(path, *, allow_missing=False):
    if allow_missing and not subprocess.check_output(
        ["git", "ls-tree", "-z", BASE, "--", path], cwd=ROOT
    ):
        return b""
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def canonical_changes(changed):
    rejected = []
    for path in changed:
        parts = path.split("/")
        normalized = not any(part in ("", ".", "..", "node_modules", "__pycache__") for part in parts)
        package_file = path.startswith(PACKAGE) and Path(path).suffix in {
            ".md", ".json", ".yaml", ".py", ".patch", ".excalidraw", ".svg", ".png",
        }
        allowed = path in CANONICAL_DOCS or path == ".github/rubric/scores/latest.json"
        if not normalized or not (allowed or TRACKING.fullmatch(path) or package_file):
            rejected.append(path)
    if rejected:
        raise ValueError(f"Paths outside issue 441 scope: {sorted(rejected)}")
    return sorted(set(changed) & CANONICAL_DOCS)


def branch_changes():
    scope_base = subprocess.check_output(
        ["git", "merge-base", "HEAD", "origin/main"], cwd=ROOT
    ).decode().strip()
    tracked = subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-only", "-z", scope_base], cwd=ROOT
    )
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"], cwd=ROOT
    )
    changed = sorted(set((tracked + untracked).decode().strip("\0").split("\0")) - {""})
    return scope_base, canonical_changes(changed)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cells(line):
    return [cell.strip() for cell in line.split("|")[1:-1]]


def reconstruct(base, patch):
    original = base.decode().splitlines(keepends=True)
    lines = patch.decode().splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.startswith("@@ ")]
    result, cursor = [], 0
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", lines[start])
        assert match
        pos = int(match[1]) - 1
        body = lines[start + 1:end]
        old = [line[1:] for line in body if line[0] in " -"]
        new = [line[1:] for line in body if line[0] in " +"]
        assert pos >= cursor and original[pos:pos + len(old)] == old
        result.extend(original[cursor:pos])
        assert len(result) == int(match[2]) - 1
        result.extend(new)
        cursor = pos + len(old)
    result.extend(original[cursor:])
    return "".join(result).encode()


def prd_definitions(text, prefix):
    found = []
    for line in text.splitlines():
        row = cells(line)
        if row and re.fullmatch(prefix + r"-\d{3}", row[0]):
            if prefix in ("FR", "NFR") and len(row) == 5 and "shall" in row[1]:
                found.append((row[0], line))
            elif prefix == "AC" and len(row) >= 2 and row[1].startswith("Given "):
                found.append((row[0], line))
            elif prefix == "GOAL" and len(row) == 5:
                found.append((row[0], line))
            elif prefix in ("CON", "OQ") and len(row) >= 4:
                found.append((row[0], line))
        if prefix == "NFR":
            match = re.match(r"\* (?:\*\*)?(NFR-\d{3})\b", line)
            if match:
                found.append((match[1], line))
        if prefix == "DD":
            match = re.match(r"\| (DD-\d{3}):", line)
            if match:
                found.append((match[1], line))
    assert all(n == 1 for n in Counter(k for k, _ in found).values()), prefix
    return dict(found)


def anchors(text):
    counts, result = Counter(), set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6} (.+?)(?: +#+)?$", line)
        if not match:
            continue
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", match[1]).lower()
        slug = "".join(c for c in heading if c in "-_ " or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        suffix = f"-{counts[slug]}" if counts[slug] else ""
        counts[slug] += 1
        result.add(slug + suffix)
    result.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    return result


def broken_links(path, text, baseline=False):
    broken = set()
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
    for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        file, _, fragment = unquote(target).partition("#")
        resolved = (path.parent / file).resolve() if file else path
        if not resolved.exists():
            broken.add(target)
        elif fragment and resolved.suffix == ".md":
            relative = resolved.relative_to(ROOT).as_posix()
            data = git_bytes(relative, allow_missing=True).decode() if baseline else resolved.read_text()
            if fragment not in anchors(data):
                broken.add(target)
    return broken


def lint(data, cli):
    result = subprocess.run(
        ["node", str(cli), "--stdin", "--config", str(HERE / "markdownlint.json")],
        input=data, capture_output=True, cwd=ROOT, check=False,
    )
    output = (result.stderr + result.stdout).decode().strip().splitlines()
    diagnostics = output and all(re.fullmatch(
        r"stdin:[1-9]\d*(?::[1-9]\d*)? MD\d{3}(?:/[A-Za-z0-9_-]+)* \S.*", line
    ) for line in output)
    if not ((result.returncode == 0 and not output)
            or (result.returncode == 1 and diagnostics and not result.stdout)):
        raise RuntimeError(
            f"markdownlint failed: {cli} (exit {result.returncode})\n"
            + "\n".join(output)
        )
    normalized = Counter(re.sub(r"^stdin:\d+(?::\d+)? ", "", line) for line in output)
    return result.returncode, output, normalized


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdownlint-cli", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    custody = json.loads((ROOT / ".copilot-tracking/research/2026-10-23/"
                          "resident-portal-requirements-441-input-custody.json").read_text())
    candidates = {}
    for name, record in custody["candidates"].items():
        base = git_bytes(record["target"])
        patch = (HERE / "source-evidence" / name / "amendment.patch").read_bytes()
        assert sha(base) == record["base_sha256"] and sha(patch) == record["patch_sha256"]
        candidates[name] = reconstruct(base, patch)
        assert sha(candidates[name]) == record["candidate_sha256"]
    for source in (HERE / "source-evidence").glob("*/*"):
        if source.is_file():
            key = source.relative_to(HERE / "source-evidence").as_posix()
            assert sha(source.read_bytes()) == custody["files"][key]["sha256"], key
    for name in ("resident-service-boundary.excalidraw", "resident-service-boundary.svg",
                 "resident-service-boundary.png"):
        assert sha((HERE / name).read_bytes()) == custody["files"]["adr/" + name]["sha256"]
    diagram = json.loads((HERE / "resident-service-boundary.excalidraw").read_text())
    assert diagram["type"] == "excalidraw" and len(diagram["elements"]) == 47
    ET.fromstring((HERE / "resident-service-boundary.svg").read_bytes())
    png = (HERE / "resident-service-boundary.png").read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", png[16:24]) == (1800, 1160)
    brd, prd = (ROOT / BRD).read_text(), (ROOT / PRD).read_text()
    old_brd, old_prd = git_bytes(BRD).decode(), git_bytes(PRD).decode()
    rows = {}
    old_rows = {}
    for data, dest in ((brd, rows), (old_brd, old_rows)):
        for line in data.splitlines():
            row = cells(line)
            if len(row) == 7 and re.fullmatch(r"(?:FR|NFR|RULE)-\d{3}", row[0]):
                assert row[0] not in dest
                dest[row[0]] = row
    assert len([x for x in rows if x.startswith("FR-")]) == 62
    assert len([x for x in rows if x.startswith("NFR-")]) == 14
    assert len([x for x in rows if x.startswith("RULE-")]) == 28
    old_acs = {ac for row in old_rows.values() for ac in re.findall(r"AC-\d{3}:", row[5])}
    new_acs = [ac for row in rows.values() for ac in re.findall(r"AC-\d{3}:", row[5])]
    assert len(new_acs) == len(set(new_acs)) == 126 and old_acs <= set(new_acs)
    allowed_changes = {"FR-044", "RULE-018", "RULE-022", "RULE-025"}
    for key, row in old_rows.items():
        assert key in rows and (rows[key] == row or key in allowed_changes), key
    matrix = brd.split("### FR-to-AC and FR-to-BG Coverage", 1)[1].split(
        "### Business Rule Enforcement", 1)[0]
    for line in matrix.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(r"FR-\d{3}", row[0]):
            assert set(re.findall(r"AC-\d{3}", row[2])) == set(
                x[:-1] for x in re.findall(r"AC-\d{3}:", rows[row[0]][5])), row[0]
    for line in old_brd.splitlines():
        if line.startswith("| FR-033 | BR-041 | AC-051 |") or line.startswith("| BG-013 | FR-049"):
            assert line in brd, "Unrelated inherited goal repair introduced"
    expected = {"FR": 71, "AC": 123, "NFR": 21, "CON": 9, "GOAL": 5, "DD": 9, "OQ": 31}
    definitions = {p: prd_definitions(prd, p) for p in expected}
    for prefix, count in expected.items():
        assert len(definitions[prefix]) == count, prefix
        old = prd_definitions(old_prd, prefix)
        assert old.keys() <= definitions[prefix].keys()
        changes = {"FR": {"FR-027"}, "OQ": {"OQ-023"}, "AC": set()}
        for key, row in old.items():
            assert definitions[prefix][key] == row or key in changes.get(prefix, set()), key
    for i in range(111, 141):
        assert definitions["AC"][f"AC-{i:03}"].endswith("| Not run |")
    prd_matrix = prd.split("### FR-to-AC coverage", 1)[1].split(
        "### FR-to-goal alignment", 1)[0]
    matrix_rows = {}
    for line in prd_matrix.splitlines():
        row = cells(line)
        if len(row) == 3 and row[0] in definitions["FR"]:
            matrix_rows[row[0]] = re.findall(r"AC-\d{3}", row[1])
    assert set(matrix_rows) == set(definitions["FR"])
    for key, line in definitions["FR"].items():
        assert matrix_rows[key] == re.findall(r"AC-\d{3}", cells(line)[3])
        assert set(matrix_rows[key]) <= definitions["AC"].keys()
    goal_matrix = prd.split("### FR-to-goal alignment", 1)[1].split(
        "### RAI draft identifier reconciliation", 1)[0]
    goal_links = {}
    for line in goal_matrix.splitlines():
        row = cells(line)
        if len(row) != 2:
            continue
        goals = set(re.findall(r"GOAL-\d{3}", row[1]))
        for first, last in re.findall(r"FR-(\d{3})(?: to FR-(\d{3}))?", row[0]):
            for number in range(int(first), int(last or first) + 1):
                goal_links.setdefault(f"FR-{number:03}", set()).update(goals)
    differences = {}
    for key, line in definitions["FR"].items():
        declared = set(re.findall(r"GOAL-\d{3}", cells(line)[4]))
        assert declared and declared <= definitions["GOAL"].keys()
        if declared != goal_links[key]:
            differences[key] = {"declared": sorted(declared), "matrix": sorted(goal_links[key])}
    assert differences == {"FR-059": {"declared": ["GOAL-004"],
                                     "matrix": ["GOAL-002", "GOAL-004"]}}
    trace = prd.split("### Resident upstream trace", 1)[1].split("## Functional Requirements", 1)[0]
    seen = set()
    for line in trace.splitlines():
        row = cells(line)
        if len(row) == 3:
            for group in re.findall(r"AC-\d{3}(?:/\d{3})*", row[2]):
                seen.update(int(n) for n in re.findall(r"\d{3}", group))
    assert set(range(104, 127)) <= seen
    assert old_prd.split("### Historical v0.12.0 Approval Checklist", 1)[1].split(
        "### Current v0.17.0 Candidate Handoff", 1)[0] in prd
    handoff = json.loads((HERE / "source-evidence/brd/draft-prd-handoff.json").read_text())
    assumptions = list(handoff["business_case"]["assumptions"].values())
    results = {}
    for i, name in enumerate(("low", "base", "high")):
        A, D, C, Tc, E, Te, U, V, R, Tr, Q, S, To = [v[i] for v in assumptions]
        W = A * D
        B = W * (C * Tc + E * Te) / 60
        G, H, J, O, I = B * U * V, W * U * R * Tr / 60, W * Q / 60, A * U * To / 60, W * U * To / 60
        F = G - H - J - S - O
        assert abs(F - (-1.594, 14.74, 94.3333333333333)[i]) < 1e-8
        results[name] = dict(W=W, B=B, G=G, H=H, J=J, O=O, F=F, I=I)
    for formula in ("W = A × D", "B = W × (C × Tc + E × Te) / 60",
                    "H = W × U × R × Tr / 60", "O = A × U × To / 60"):
        assert formula in brd, formula
    source_brd = candidates["brd"].decode()
    for start, end in (("| Assumption and denominator |", "Calls and email"),
                       ("| Derived measure |", "Onboarding assumes")):
        source_table = source_brd.split(start, 1)[1].split(end, 1)[0]
        assert source_table == brd.split(start, 1)[1].split(end, 1)[0]
    for value in ("720 WIP", "84 baseline", "14.74 net", "-1.594", "94.333"):
        assert value in prd, value
    for path in ("docs/case_study_48_original.md", "docs/reference/memory.md"):
        assert (ROOT / path).read_bytes() == git_bytes(path), path
    assert (ROOT / "docs/reference/log.md").read_bytes().startswith(git_bytes("docs/reference/log.md"))
    old_exa = next(line for line in git_bytes("docs/case_study_48_addendum.md").decode().splitlines()
                   if line.startswith("| EXA-004 "))
    assert old_exa in (ROOT / "docs/case_study_48_addendum.md").read_text()
    proposal = HERE / "resident-service-unregistered-proposal.md"
    text = proposal.read_text()
    assert "id: null\n" in text and "registration_status: unregistered\n" in text
    rationale = ("Reuse existing case authority to avoid duplicate platforms; deliver the "
                 "portal/workflow first and independently gate the bounded resident-answer task.")
    assert rationale in text
    assert ("five concurrent fictional sessions\n  (three residents on separate scopes and two staff), "
            "and a 30-minute run.") in prd
    assert "case/status/receipt API completion at or below 2 seconds" in prd
    scope_base, changed = branch_changes()
    paths = [ROOT / path for path in changed]
    paths += [proposal, HERE / "source-evidence/README.md"]
    lint_report, link_report, hashes = {}, {}, {}
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        hashes[relative] = sha(data)
        assert not re.search(rb"\]\([^)]*(?:/home/|session-state|file://)", data), relative
        base_data = git_bytes(relative, allow_missing=True)
        base_lint = lint(base_data, args.markdownlint_cli)
        current_lint = lint(data, args.markdownlint_cli)
        introduced = current_lint[2] - base_lint[2]
        assert not introduced, (relative, introduced)
        lint_report[relative] = {"base_exit": base_lint[0], "integrated_exit": current_lint[0],
                                 "diagnostics": current_lint[1], "introduced": list(introduced)}
        previous = broken_links(path, base_data.decode(), True) if base_data else set()
        current = broken_links(path, data.decode())
        assert not current - previous, (relative, sorted(current - previous))
        link_report[relative] = {"inherited_unresolved": sorted(current & previous), "introduced": []}
    for path in (HERE / "resident-service-boundary.excalidraw",
                 HERE / "resident-service-boundary.svg", HERE / "resident-service-boundary.png",
                 Path(__file__).resolve()):
        hashes[path.relative_to(ROOT).as_posix()] = sha(path.read_bytes())
    report = {
        "status": "PASS_FOCUSED_STATIC_NOT_APPROVAL",
        "base": BASE, "source_custody": "PASS", "asset_identity": "PASS",
        "scope_base": scope_base,
        "brd": {"FR": 62, "AC": 126, "NFR": 14, "RULE": 28},
        "prd": expected, "all_new_ACs": "Not run", "new_upstream_trace": "23/23",
        "formula_scenarios": results, "protected_history": "PASS",
        "inherited_goal_discrepancy": differences,
        "markdownlint": lint_report, "links_and_anchors": link_report, "sha256": hashes,
        "limits": ["Not requirements approval, application acceptance or WCAG conformance",
                   "Historical archived source links/diagnostics intentionally not rewritten",
                   "Full publication gate and independent Review separate",
                   "ADR registration UNMET; OD-52-55 and live approvals open"],
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(hashes)} exact artifact hashes; report written")


if __name__ == "__main__":
    main()
