"""Read-only portable custody and integration checks for the issue 441 refinement."""

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EVIDENCE = HERE / "refinement-evidence"
ENTRY = "8ada8109f9d4b7348fbd8ff76839d020dec04d4b"
SPEC = importlib.util.spec_from_file_location("resident_validation", HERE / "validate-integration.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def at_entry(path):
    return subprocess.check_output(["git", "show", f"{ENTRY}:{path}"], cwd=ROOT)


def reverse_patch(patch):
    lines = patch.splitlines(keepends=True)
    result = []
    for line in lines:
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+(?:,\d+)?) \+(\d+(?:,\d+)?) @@(.*)", line)
            assert match, line
            result.append(f"@@ -{match[2]} +{match[1]} @@{match[3]}\n")
        elif line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("-"):
            result.append("+" + line[1:])
        elif line.startswith("+"):
            result.append("-" + line[1:])
        else:
            result.append(line)
    return "".join(result).encode()


def integrated_bytes(record):
    path = record["integrated_path"]
    current = (ROOT / path).read_bytes()
    if v.sha(current) == record["integrated_sha256"]:
        return current
    try:
        commits = subprocess.check_output(
            ["git", "log", "--all", "--format=%H", "--", path], cwd=ROOT, text=True
        ).splitlines()
    except subprocess.CalledProcessError as error:
        raise AssertionError(path) from error
    for commit in commits:
        result = subprocess.run(
            ["git", "show", f"{commit}:{path}"], cwd=ROOT,
            capture_output=True, check=False,
        )
        if result.returncode == 0 and v.sha(result.stdout) == record["integrated_sha256"]:
            return result.stdout
    raise AssertionError(path)


def source_bytes(record):
    current = integrated_bytes(record)
    patch = record["source_to_integrated_patch"]
    source = v.reconstruct(current, reverse_patch(patch)) if patch else current
    assert v.sha(source) == record["source_sha256"] and len(source) == record["source_bytes"]
    if patch:
        assert v.reconstruct(source, patch.encode()) == current
    return source


def manifest_inventory(inventory, label):
    if not isinstance(inventory, (dict, list)) or not inventory:
        raise ValueError(f"{label}: expected a nonempty manifest dictionary or list")
    entries = inventory.items() if isinstance(inventory, dict) else (
        (entry.get("path"), entry) if isinstance(entry, dict) else (None, entry)
        for entry in inventory
    )
    indexed = {}
    for path, entry in entries:
        if (not isinstance(path, str) or not path or "\\" in path
                or Path(path).is_absolute() or ".." in Path(path).parts
                or Path(path).as_posix() != path or path == "."):
            raise ValueError(f"{label}: invalid manifest path {path!r}")
        if path in indexed:
            raise ValueError(f"{label}: duplicate manifest path {path}")
        if not isinstance(entry, dict):
            raise ValueError(f"{label}: invalid manifest entry for {path}")
        sha = entry.get("sha256")
        size = entry.get("bytes")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise ValueError(f"{label}: invalid sha256 for {path}")
        if type(size) is not int or size < 0:
            raise ValueError(f"{label}: invalid byte size for {path}")
        indexed[path] = entry
    return indexed


def verify_manifest_sources(name, manifest, field, sources, records):
    document = json.loads(sources[manifest])
    if not isinstance(document, dict) or field not in document:
        raise ValueError(f"{manifest}: missing manifest field {field}")
    inventory = manifest_inventory(document[field], manifest)
    # Self manifests cannot inventory themselves; capstone predates reconciliation.
    unlisted = {manifest.removeprefix(name + "/")}
    if name == "adr":
        unlisted.add("capstone-review-boundary.md")
    for record in records:
        if not record["source"].startswith(name + "/"):
            continue
        path = record["source"].removeprefix(name + "/")
        if path not in inventory:
            if path in unlisted:
                continue
            raise ValueError(f"{manifest}: selected source not inventoried: {path}")
        if inventory[path]["sha256"] != record["source_sha256"]:
            raise ValueError(f"{manifest}: source hash mismatch for {path}")
        if inventory[path]["bytes"] != record["source_bytes"]:
            raise ValueError(f"{manifest}: source byte size mismatch for {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdownlint-cli", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads((EVIDENCE / "source-to-integrated.json").read_text())
    records = mapping["files"]
    sources = {record["source"]: source_bytes(record) for record in records}
    integrated_prd = next(
        record for record in records
        if record["integrated_path"] == v.PRD
    )
    previous_prd = integrated_bytes(integrated_prd).decode()
    for name, manifest, field in [
        ("prd", "prd/output-manifest.json", "outputs"),
        ("adr", "adr/reconciliation-output-manifest.json", "files"),
    ]:
        verify_manifest_sources(name, manifest, field, sources, records)
    pins = {
        "prd/zava-forward-retrofit-programme-demonstrator.md": "7fb40549ba4975c2feb8d8a2a3de882e06677875c02e4a43c4b3a94ddf218343",
        "prd/output-manifest.json": "cbbcc45fde3653343115a2071793cb21dcede1c335cbf1e3800e7e41a59c46b1",
        "adr/resident-service-unregistered-proposal-reconciled.md": "8e44d6ffbfe907a5e7e8cd057d0a29e0e977e916456ed0f0d9799efe8e1a4d77",
        "adr/reconciliation-output-manifest.json": "c0b97777d015926573a320d004e38f11c45e965f0540e2e64d8e241bde4f57ce",
    }
    assert all(v.sha(sources[name]) == sha for name, sha in pins.items())
    assert v.reconstruct(at_entry(v.PRD), sources["prd/amendment.patch"]) == sources[
        "prd/zava-forward-retrofit-programme-demonstrator.md"]
    current = (ROOT / v.PRD).read_text()
    counts = {}
    additions = {
        "FR": {"FR-072", "FR-073"},
        "AC": {f"AC-{i:03}" for i in range(141, 148)},
        "DD": {"DD-010"},
    }
    changed = {
        "FR": {"FR-003", "FR-005", "FR-008", "FR-022"},
        "NFR": {"NFR-003"},
    }
    for prefix in ("FR", "AC", "NFR", "CON", "GOAL", "DD", "OQ"):
        before = v.prd_definitions(previous_prd, prefix)
        after = v.prd_definitions(current, prefix)
        assert before.keys() <= after.keys(), prefix
        assert set(after) - set(before) == additions.get(prefix, set()), prefix
        assert all(
            after[key] == row or key in changed.get(prefix, set())
            for key, row in before.items()
        ), prefix
        counts[prefix] = len(after)
    acs = v.prd_definitions(current, "AC")
    assert all(acs[f"AC-{i:03}"].endswith("| Not run |") for i in range(111, 141))
    assert all(acs[f"AC-{i:03}"].endswith("| Not run |") for i in range(141, 148))
    assert len(set(re.findall(r"PR442-S\d{2}", current))) == 20
    assert len(re.findall(r"^\| PRD::FR-\d{3} \|", current, flags=re.M)) == 73
    brd = (ROOT / v.BRD).read_text()
    brd_requirements = brd.split("## Requirements Traceability", 1)[0]
    brd_fr = set(re.findall(r"^\| (FR-\d{3}) \|", brd_requirements, flags=re.M))
    brd_ac = set(re.findall(r"\bAC[:-](\d{3}):", brd_requirements))
    assert len(brd_fr) == 64 and len(brd_ac) == 132
    assert {f"FR-{i:03}" for i in range(53, 65)} <= brd_fr
    assert {str(i) for i in range(104, 133)} <= brd_ac
    brd_trace = current.split("### Traceability to the BRD", 1)[1].split(
        "\n## ", 1
    )[0]
    trace_rows = {
        v.cells(line)[0]: v.cells(line)[1]
        for line in brd_trace.splitlines()
        if len(v.cells(line)) == 2
    }
    assert "BRD FR-063" in trace_rows["FR-072"]
    assert "BRD FR-064" in trace_rows["FR-073"]
    for name in ("docs/case_study_48_original.md", "docs/reference/memory.md"):
        assert (ROOT / name).read_bytes() == at_entry(name), name
    main_log = subprocess.check_output(
        ["git", "show", "origin/main:docs/reference/log.md"], cwd=ROOT
    )
    current_log = (ROOT / "docs/reference/log.md").read_bytes()
    assert current_log.startswith(main_log)
    merge_head = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "MERGE_HEAD"],
        cwd=ROOT, capture_output=True, check=False,
    )
    branch_parent = "HEAD" if merge_head.returncode == 0 else "HEAD^1"
    branch_log = subprocess.check_output(
        ["git", "show", f"{branch_parent}:docs/reference/log.md"], cwd=ROOT, text=True
    )
    current_log_text = current_log.decode()
    for heading in (
        "## [2026-10-23] update | Optional resident requirements and unregistered architecture proposal (#441)",
        "## [2026-10-23] update | Completed unsigned resident PRD and architecture refinement (#441)",
    ):
        def entry(text):
            lines = text.splitlines()
            start = lines.index(heading)
            end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            return "\n".join(lines[start:end]).strip()
        assert entry(branch_log) in current_log_text
    for name in ("resident-service-boundary.excalidraw", "resident-service-boundary.svg",
                 "resident-service-boundary.png"):
        relative = (HERE / name).relative_to(ROOT).as_posix()
        assert (HERE / name).read_bytes() == at_entry(relative), name
    archive = mapping["historical_archive"]
    assert v.sha((ROOT / archive["path"]).read_bytes()) == archive["sha256"]
    assert (ROOT / archive["path"]).read_bytes() == at_entry(
        (HERE / "resident-service-unregistered-proposal.md").relative_to(ROOT).as_posix())
    proposal = (HERE / "resident-service-unregistered-proposal.md").read_text()
    assert all(s in proposal for s in ("id: null\n", "registration_status: unregistered\n",
                                      "status: proposed\n", "supersedes: null\n", "superseded-by: null\n"))
    for number in ("005", "040", "006", "024", "041", "009", "039"):
        assert f"pr442-qual-{number}" in proposal
        assert f"pr442-qual-{number}" in sources["prd/review/reviewer-result-summary.md"].decode()
    assert all(s in proposal for s in ("FAIL / Validate BLOCKED / Finalize NOT_EVALUATED",
                                      "singular = 1 < 2", "Activation OFF.", "47-element"))
    # Source archives are inert; lint/link checks apply to every navigable derivative.
    lint, links, hashes = {}, {}, {}
    for record in records:
        path = ROOT / record["integrated_path"]
        hashes[record["integrated_path"]] = v.sha(path.read_bytes())
        if path.suffix != ".md" or record["transformation"] == "exact inert source archive":
            continue
        source = source_bytes(record)
        original = v.lint(source, args.markdownlint_cli)[2]
        result = v.lint(path.read_bytes(), args.markdownlint_cli)
        introduced = result[2] - original
        assert not introduced, (record["integrated_path"], introduced)
        lint[record["integrated_path"]] = {"source_diagnostics": sum(original.values()),
                                          "integrated_diagnostics": len(result[1]), "introduced": []}
        broken = v.broken_links(path, path.read_text())
        if path == ROOT / v.PRD:
            inherited = v.broken_links(path, at_entry(v.PRD).decode())
            assert not broken - inherited, broken - inherited
            links[record["integrated_path"]] = {"inherited": sorted(broken), "introduced": []}
        else:
            assert not broken, (record["integrated_path"], broken)
            links[record["integrated_path"]] = {"inherited": [], "introduced": []}
    readme = EVIDENCE / "README.md"
    assert not v.broken_links(readme, readme.read_text())
    assert v.lint(readme.read_bytes(), args.markdownlint_cli)[0] == 0
    v.branch_changes()
    report = {
        "status": "PASS_REFINEMENT_STATIC_NOT_QUALITY_APPROVAL",
        "entry": ENTRY, "four_owner_pins": pins,
        "portable_selected_mappings": len(records), "definitions_unchanged": counts,
        "source_patch_reconstructed": True, "all_30_resident_AC": "Not run",
        "local_stories": 20, "qualified_FR_trace_rows": 71,
        "current_quality": mapping["source_quality"],
        "source_map_sha256": v.sha((EVIDENCE / "source-to-integrated.json").read_bytes()),
        "markdownlint": lint, "links": links, "sha256": hashes,
        "limits": ["All seven current quality findings remain open, not waived",
                   "Raw archives retain original link context and are not navigable derivatives",
                   "No application execution, requirements approval, registration or live acceptance",
                   "Hosted A5/B6 score citations remain OPEN; no generated score edit"],
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(records)} portable custody mappings, exact definitions and bounded links/lint")


if __name__ == "__main__":
    main()
