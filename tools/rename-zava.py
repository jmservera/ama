#!/usr/bin/env python3
"""One-off local branding migration; dry-run by default, never deletes Azure resources."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
import hashlib
from io import BytesIO
import json
import logging
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

LOG = logging.getLogger("rename_zava")
REPLACEMENTS = (
    ("Proper North Homes", "Zava North Homes"),
    ("PROPER NORTH HOMES", "ZAVA NORTH HOMES"),
    ("proper-north-homes", "zava-north-homes"),
    ("proper_north_homes", "zava_north_homes"),
    ("propernorthhomes", "zavanorthhomes"),
    ("Proper Warm", "Zava Forward"),
    ("PROPER WARM", "ZAVA FORWARD"),
    ("ProperWarm", "ZavaForward"),
    ("proper-warm", "zava-forward"),
    ("proper_warm", "zava_forward"),
    ("properwarm", "zavaforward"),
    ("PW_", "ZF_"),
    ("pw_", "zf_"),
    ("X-PW-", "X-ZF-"),
    ("PW-", "ZF-"),
    ("pw-", "zf-"),
    ("Pw-", "Zf-"),
    ("warm-test", "forward-test"),
    ("warm-dev", "forward-dev"),
)
TEXT_SUFFIXES = {
    ".md", ".py", ".json", ".yaml", ".yml", ".html", ".css", ".js", ".mjs",
    ".bicep", ".bicepparam", ".sh", ".ps1", ".sql", ".svg", ".excalidraw",
    ".txt", ".in", ".csv", ".geojson",
}
HISTORICAL = (
    "docs/reference/regulatory/", "docs/reference/log.md",
    "docs/reference/memory.md", "docs/case_study_48_original.md",
)
URL = re.compile(r"https?://[^\s<>\"')\]]+")
SCRIPT_PREFIX = "tools/rename-zava"
HISTORY_MANIFEST = ".copilot-tracking/renames/zava-forward-history.json"


def replace_names(text: str) -> str:
    """Replace known branding forms, preserving external URLs as historical links."""
    def replace_part(part: str) -> str:
        for old, new in REPLACEMENTS:
            part = part.replace(old, new)
        return re.sub(r"\bPW\b", "ZF", part)

    result, start = [], 0
    for match in URL.finditer(text):
        result.extend((replace_part(text[start:match.start()]), match.group()))
        start = match.end()
    result.append(replace_part(text[start:]))
    return "".join(result)


def preserved(path: str) -> bool:
    """Keep historical records, migration tooling and recorded assertions unchanged."""
    if path.startswith((*HISTORICAL, SCRIPT_PREFIX)):
        return True
    if path.startswith(".copilot-tracking/"):
        return not (
            path.endswith(".pptx")
            or ("/ppt/" in path and "/content/" in path)
        )
    return False


def tracked_files(root: Path) -> list[str]:
    """Inventory Git-tracked files without touching untracked secrets or Git history."""
    raw = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True, capture_output=True,
    ).stdout
    return sorted(p.decode("utf-8") for p in raw.split(b"\0") if p)


def destination(path: str) -> str:
    """Rename active paths, keeping historical artifact paths intact."""
    return path if preserved(path) else replace_names(path)


def update_text(text: str, path: str, path_map: dict[str, str]) -> str:
    """Update active identifiers and references to paths which will actually move."""
    # References into preserved snapshots must not be changed by the generic mapping.
    references = set()
    for old, new in path_map.items():
        if old == new and replace_names(old) != old:
            references.add(old)
            relative = Path(os.path.relpath(old, Path(path).parent)).as_posix()
            references.add(relative)
            if not relative.startswith("."):
                references.add("./" + relative)
    protected = {old: f"\x00HISTORY_{i}\x00" for i, old in enumerate(sorted(references))}
    for old, marker in sorted(protected.items(), key=lambda item: -len(item[0])):
        text = text.replace(old, marker)
    text = replace_names(text)
    for old, marker in protected.items():
        text = text.replace(marker, old)
    if path.startswith("infra/"):
        text = re.sub(r"(?<![A-Za-z])warm(?=[-'])", "forward", text)
    if path == "mvp/web/index.html":
        text = re.sub(
            r'<span class="logo" aria-hidden="true">(?:PW|ZF)</span>',
            '<img class="zava-logo" src="/zava-logo.png" alt="Zava North Homes">', text,
        )
    if path == ".github/extensions/program-workbench/assets/index.html":
        text = re.sub(
            r'<span class="brand-mark" aria-hidden="true">(?:PW|ZF)</span>',
            '<img class="zava-logo" src="./zava-logo.png" alt="Zava North Homes">', text,
        )
        if ".zava-logo{" not in text:
            text = text.replace("</head>",
                                "<style>.zava-logo{width:114px;height:40px;object-fit:contain;background:#fff;padding:4px}</style></head>")
    if path == "mvp/web/style.css" and ".zava-logo{" not in text:
        text += "\n.zava-logo{width:114px;height:40px;object-fit:contain;flex-shrink:0;background:#fff;border-radius:4px;padding:4px}\n"
    return text


def replace_runs(runs: Iterable[object]) -> bool:
    """Replace names spanning runs without collapsing unaffected run formatting."""
    runs = list(runs)
    original = "".join(run.text for run in runs)
    if replace_names(original) == original:
        return False
    # Process longest known forms first and right-to-left to retain run offsets.
    for old, new in (*REPLACEMENTS, ("PW", "ZF")):
        text = "".join(run.text for run in runs)
        url_spans = [m.span() for m in URL.finditer(text)]
        pattern = r"\bPW\b" if old == "PW" else re.escape(old)
        for match in reversed(list(re.finditer(pattern, text))):
            left, right = match.span()
            if any(a <= left < b for a, b in url_spans):
                continue
            offset, segments = 0, []
            for run in runs:
                segments.append((run, offset, offset + len(run.text)))
                offset += len(run.text)
            first = True
            for run, start, end in segments:
                if end <= left or start >= right:
                    continue
                a, b = max(0, left - start), min(len(run.text), right - start)
                run.text = run.text[:a] + (new if first else "") + run.text[b:]
                first = False
    return True


def shape_paragraphs(shapes: Iterable[object]) -> Iterable[object]:
    """Visit normal text, grouped shapes and table cells."""
    for shape in shapes:
        if shape.shape_type == 6:
            yield from shape_paragraphs(shape.shapes)
        if shape.has_text_frame:
            yield from shape.text_frame.paragraphs
        if shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    yield from cell.text_frame.paragraphs


def migrate_pptx(raw: bytes, logo: bytes | None) -> bytes:
    """Update editable text, notes, metadata and add a logo to each slide."""
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.util import Inches

    presentation = Presentation(BytesIO(raw))
    collections = [slide.shapes for slide in presentation.slides]
    collections += [master.shapes for master in presentation.slide_masters]
    collections += [layout.shapes for layout in presentation.slide_layouts]
    for shapes in collections:
        for paragraph in shape_paragraphs(shapes):
            replace_runs(paragraph.runs)
    for slide in presentation.slides:
        if slide.has_notes_slide:
            for paragraph in shape_paragraphs(slide.notes_slide.shapes):
                replace_runs(paragraph.runs)
        if logo and not any(s.name == "Zava branding logo" for s in slide.shapes):
            width = Inches(1.05)
            left = presentation.slide_width - width - Inches(.2)
            top = Inches(.12)
            backing = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, left, top, width, int(width * png_ratio(logo)),
            )
            backing.name = "Zava logo contrast backing"
            backing.fill.solid()
            backing.fill.fore_color.rgb = RGBColor(255, 255, 255)
            backing.line.fill.background()
            picture = slide.shapes.add_picture(
                BytesIO(logo), left, top, width=width,
            )
            picture.name = "Zava branding logo"
    for name in ("title", "subject", "author", "keywords", "comments", "category"):
        setattr(presentation.core_properties, name,
                replace_names(getattr(presentation.core_properties, name)))
    output = BytesIO()
    presentation.save(output)
    return output.getvalue()


def png_ratio(logo: bytes) -> float:
    """Validate the PNG dimensions used by slide source and binary placement."""
    if len(logo) < 24 or not logo.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Logo is not a PNG with an IHDR dimension header.")
    width, height = struct.unpack(">II", logo[16:24])
    if not 0 < width <= 10000 or not 0 < height <= 10000:
        raise ValueError("Logo dimensions must be between 1 and 10000 pixels.")
    return height / width


def add_yaml_logo(text: str, path: Path, *, logo: bytes, apply: bool) -> str:
    """Keep the slide authoring source in sync with binary logo insertion."""
    import yaml

    try:
        document = yaml.safe_load(text)
        style_path = path.parent.parent / "global/style.yaml"
        style = yaml.safe_load(style_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid slide/style YAML: {error}") from error
    if not isinstance(document, dict) or not isinstance(document.get("elements"), list):
        raise ValueError("Slide YAML must have an elements list.")
    if any(element.get("name") == "Zava branding logo" for element in document["elements"]):
        return text
    if not isinstance(style, dict) or not isinstance(style.get("dimensions"), dict):
        raise ValueError("Slide style YAML must define dimensions.width_inches.")
    width = float(style["dimensions"]["width_inches"])
    left, height = round(width - 1.25, 4), round(1.05 * png_ratio(logo), 4)
    document["elements"].append({
        "type": "shape", "name": "Zava logo contrast backing", "shape": "rectangle",
        "left": left, "top": .12, "width": 1.05, "height": height,
        "fill": "#FFFFFF", "line_color": "#FFFFFF",
    })
    document["elements"].append({
        "type": "image", "name": "Zava branding logo", "path": "images/zava-logo.png",
        "left": left, "top": .12, "width": 1.05, "height": height,
    })
    if apply:
        atomic_write(path.parent / "images/zava-logo.png", logo)
    return yaml.safe_dump(document, allow_unicode=True, sort_keys=False)


def pptx_branding(raw: bytes) -> bool:
    """Inspect text across XML runs without a PowerPoint dependency in dry-run."""
    with zipfile.ZipFile(BytesIO(raw)) as archive:
        for name in archive.namelist():
            if not name.endswith(".xml"):
                continue
            xml = ET.fromstring(archive.read(name))
            text = "".join(node.text or "" for node in xml.iter())
            if replace_names(text) != text:
                return True
    return False


def atomic_write(path: Path, data: bytes) -> None:
    """Replace one file atomically, retaining its executable permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode if path.exists() else None
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(data)
    try:
        if mode is not None:
            temporary.chmod(mode)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def migrate(root: Path, *, apply: bool, logo: bytes | None) -> dict:
    """Plan or apply local changes, returning explicit per-file and remaining work."""
    paths = tracked_files(root)
    history_manifest = root / HISTORY_MANIFEST
    existing_history = set(json.loads(history_manifest.read_text()).get("snapshots", [])) if history_manifest.exists() else set()
    path_map = {p: p if p in existing_history else destination(p) for p in paths}
    historical_snapshots: dict[str, bytes] = {}
    for name in paths:
        if not preserved(name) or Path(name).suffix != ".md":
            continue
        text = (root / name).read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^\s)]+)\)", text):
            if ":" in link or link.startswith("#"):
                continue
            link = link.split("#", 1)[0]
            candidate = ((root / name).parent / link).resolve()
            if not candidate.is_relative_to(root):
                continue
            old = candidate.relative_to(root).as_posix()
            if old in path_map and path_map[old] != old:
                historical_snapshots[old] = candidate.read_bytes()
    pending_moves: list[tuple[Path, Path]] = []
    slide_logos: set[Path] = set()
    report = {
        "mode": "apply" if apply else "dry-run", "company": "Zava North Homes",
        "project": "Zava Forward", "changes": [], "preserved": [], "failures": [],
        "historical_snapshots": sorted(historical_snapshots),
        "manual_follow_up": [
            "Render every changed PPTX: check text overflow, logo overlap and contrast.",
            "Re-export PDFs, screenshots and slide previews; raster text is not replaced.",
            "Validate/rebuild changed slide YAML sources with the shared deck pipeline.",
            "Review anchors, local links, old live URLs and embedded/chart/SmartArt text.",
            "Run renamed MVP/prototype tests; regenerate synthetic data (443 open cases).",
            "Inventory ama resources, Entra app roles/redirects, SQL grants, secrets and M365 dependencies.",
            "Confirm exact destructive Azure reset inventory before deleting anything.",
            "Redeploy with workload=forward, real image, Entra client ID and map tile configuration.",
            "Verify Entra login, My cases, All cases, 443 open cases, map tiles/points and logo.",
        ],
    }
    targets = list(path_map.values())
    if len(set(targets)) != len(targets):
        raise ValueError("Rename collision: multiple tracked paths map to one destination.")
    for old, new in path_map.items():
        target = root / new
        if new != old and target.exists():
            raise ValueError(f"Rename destination already exists: {new}")
        if (root / old).is_symlink() or any(p.is_symlink() for p in target.parents if p != root):
            raise ValueError(f"Refusing symlink path: {old}")
    for old, new in path_map.items():
        path = root / old
        if preserved(old) or old in existing_history:
            report["preserved"].append(old)
            continue
        try:
            raw = path.read_bytes()
            is_pptx = path.suffix.lower() == ".pptx"
            if is_pptx:
                changed = pptx_branding(raw) or logo is not None
                output = migrate_pptx(raw, logo) if apply and changed else raw
            elif path.suffix.lower() in TEXT_SUFFIXES or path.name in ("Dockerfile", ".gitignore"):
                output = update_text(raw.decode("utf-8"), old, path_map).encode("utf-8")
                if old.startswith("mvp/policies/") and path.suffix == ".json" and output != raw:
                    policy = json.loads(output)
                    if "content_hash" not in policy:
                        raise ValueError("Ranking policy is missing its required content_hash.")
                    body = {key: value for key, value in policy.items() if key != "content_hash"}
                    policy["content_hash"] = hashlib.sha256(json.dumps(
                        body, sort_keys=True, separators=(",", ":"),
                    ).encode("utf-8")).hexdigest()
                    output = (json.dumps(policy, indent=2) + "\n").encode("utf-8")
                if logo and old.endswith("/content.yaml") and "/ppt/" in old:
                    output = add_yaml_logo(
                        output.decode("utf-8"), path, logo=logo, apply=False,
                    ).encode("utf-8")
                    slide_logos.add((root / new).parent / "images/zava-logo.png")
                changed = output != raw
            else:
                if path.suffix.lower() in (".pdf", ".png", ".jpg", ".jpeg"):
                    report["manual_follow_up"].append(f"Inspect/re-export binary asset: {new}")
                output, changed = raw, False
            if changed or old != new:
                report["changes"].append({"from": old, "to": new, "content": changed})
                if apply:
                    if changed:
                        atomic_write(path, output)
                    if old != new:
                        pending_moves.append((path, root / new))
        except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError,
                ET.ParseError, zipfile.BadZipFile, ImportError) as error:
            LOG.error("Cannot migrate %s: %s", old, error)
            report["failures"].append({"path": old, "reason": str(error)})
    # Keep every source dependency (including global slide style) at its old
    # path until all files have been read and transformed.
    for source, target in pending_moves:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
        except OSError as error:
            LOG.error("Cannot rename %s: %s", source.relative_to(root), error)
            report["failures"].append({"path": source.relative_to(root).as_posix(),
                                       "reason": str(error)})
    if apply and historical_snapshots:
        for name, raw in historical_snapshots.items():
            atomic_write(root / name, raw)
        snapshots = sorted(existing_history | historical_snapshots.keys())
        atomic_write(history_manifest, (json.dumps({"snapshots": snapshots}, indent=2) + "\n").encode())
    if apply and logo:
        for path in slide_logos:
            atomic_write(path, logo)
        atomic_write(root / "mvp/web/zava-logo.png", logo)
        if (root / ".github/extensions/program-workbench/assets").is_dir():
            atomic_write(root / ".github/extensions/program-workbench/assets/zava-logo.png", logo)
    report["status"] = "partial" if report["failures"] else (
        "local-changes-applied-review-required" if apply else "planned"
    )
    return report


def main() -> int:
    """Run the explicitly scoped local migration and write a required JSON report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--logo", type=Path, help="Locally downloaded, reviewed PNG; no automatic fetch.")
    parser.add_argument("--report", type=Path, required=True, help="JSON report outside the repository.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    root = args.root.resolve()
    if args.report.resolve().is_relative_to(root):
        parser.error("--report must be outside the repository (may contain historical names).")
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True).stdout.strip()
        if Path(top).resolve() != root:
            parser.error("--root must be the Git worktree root.")
        if args.apply:
            branch = subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                                    check=True, capture_output=True, text=True).stdout.strip()
            status = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                                    check=True, capture_output=True, text=True).stdout
            if not branch or branch in ("main", "master") or status:
                parser.error("--apply requires a clean topic branch; untracked files are not ignored.")
            if args.logo is None:
                parser.error("--apply requires --logo to avoid silently incomplete branding.")
        logo = args.logo.read_bytes() if args.logo else None
        if logo and (len(logo) > 5_000_000 or not logo.startswith(b"\x89PNG\r\n\x1a\n")):
            parser.error("--logo must be a PNG under 5 MB.")
        if logo:
            png_ratio(logo)
        report = migrate(root, apply=args.apply, logo=logo)
        atomic_write(args.report.resolve(), (json.dumps(report, indent=2) + "\n").encode())
        LOG.info("%s: %d changes, %d failures; report %s",
                 report["status"], len(report["changes"]), len(report["failures"]), args.report)
        return 1 if report["failures"] else 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        LOG.error("Migration stopped: %s", error)
        return 2


if __name__ == "__main__":
    sys.exit(main())
