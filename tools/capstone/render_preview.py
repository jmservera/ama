#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
"""Render a local deck with LibreOffice, preserving its fixed PDF slide jumps."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

import pymupdf

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


@dataclass(frozen=True)
class SlideJump:
    source: int
    target: int
    box: tuple[float, float, float, float]


def resolve_part(part: str, target: str) -> str:
    """Resolve an OOXML member URI, not an operating-system file path."""
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
    if resolved.startswith(("../", "/")):
        raise ValueError("Slide relationship escapes the package")
    return resolved


def read_slide_jumps(deck: Path) -> tuple[int, list[SlideJump]]:
    with zipfile.ZipFile(deck) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        parts = {
            entry.attrib["Id"]: resolve_part(
                "ppt/presentation.xml", entry.attrib["Target"]
            )
            for entry in relationships
            if entry.get("TargetMode") != "External"
        }
        slide_ids = presentation.findall("p:sldIdLst/p:sldId", NS)
        slides = [parts[entry.attrib[f"{{{NS['r']}}}id"]] for entry in slide_ids]
        if not slides or len(set(slides)) != len(slides):
            raise ValueError("Presentation slide order is empty or duplicated")
        targets = {part: number for number, part in enumerate(slides)}
        size = presentation.find("p:sldSz", NS)
        if size is None:
            raise ValueError("Presentation dimensions are missing")
        width, height = int(size.attrib["cx"]), int(size.attrib["cy"])
        if width <= 0 or height <= 0:
            raise ValueError("Presentation dimensions must be positive")
        jumps: list[SlideJump] = []
        for number, part in enumerate(slides):
            document = ET.fromstring(archive.read(part))
            actions = document.findall(".//a:hlinkClick", NS)
            if not actions:
                continue
            parent_part = Path(part)
            rel_part = (
                parent_part.parent / "_rels" / f"{parent_part.name}.rels"
            ).as_posix()
            relationships = ET.fromstring(archive.read(rel_part))
            slide_rels = {
                entry.attrib["Id"]: resolve_part(part, entry.attrib["Target"])
                for entry in relationships
                if entry.get("TargetMode") != "External"
                and entry.attrib["Type"].endswith("/slide")
            }
            parents = {child: parent for parent in document.iter() for child in parent}
            owners: set[ET.Element] = set()
            for action in actions:
                if action.get("action") != "ppaction://hlinksldjump":
                    raise ValueError(
                        f"Unsupported navigation action on slide {number + 1}"
                    )
                target_part = slide_rels.get(action.get(f"{{{NS['r']}}}id", ""))
                if target_part not in targets:
                    raise ValueError(
                        f"Missing slide-jump destination on slide {number + 1}"
                    )
                owner = action
                while owner.tag not in {
                    f"{{{NS['p']}}}sp",
                    f"{{{NS['p']}}}pic",
                    f"{{{NS['p']}}}graphicFrame",
                }:
                    if owner not in parents:
                        raise ValueError("Slide jump has no shape owner")
                    owner = parents[owner]
                if owner in owners:
                    raise ValueError(
                        "Multiple run-level links need separate PDF hit regions"
                    )
                owners.add(owner)
                ancestor = owner
                while ancestor in parents:
                    ancestor = parents[ancestor]
                    if ancestor.tag == f"{{{NS['p']}}}grpSp":
                        raise ValueError(
                            "Grouped navigation requires an explicit group transform"
                        )
                transform = owner.find("p:spPr/a:xfrm", NS)
                if transform is None:
                    transform = owner.find("p:xfrm", NS)
                if transform is None or any(
                    int(transform.get(key, "0")) for key in ("rot", "flipH", "flipV")
                ):
                    raise ValueError("Missing or unsupported navigation transform")
                offset, extent = (
                    transform.find("a:off", NS),
                    transform.find("a:ext", NS),
                )
                if offset is None or extent is None:
                    raise ValueError("Navigation shape bounds are missing")
                x, y = int(offset.attrib["x"]), int(offset.attrib["y"])
                w, h = int(extent.attrib["cx"]), int(extent.attrib["cy"])
                if min(x, y) < 0 or min(w, h) <= 0 or x + w > width or y + h > height:
                    raise ValueError("Navigation shape is outside the slide")
                jumps.append(
                    SlideJump(
                        number,
                        targets[target_part],
                        (x / width, y / height, w / width, h / height),
                    )
                )
    return len(slides), jumps


def jump_key(source: int, target: int, rectangle: pymupdf.Rect) -> tuple:
    return source, target, *(round(value, 2) for value in rectangle)


def add_hit_region(
    regions: dict[int, list[tuple[int, pymupdf.Rect]]],
    source: int,
    target: int,
    rectangle: pymupdf.Rect,
) -> None:
    page_regions = regions.setdefault(source, [])
    if any(
        existing_target != target and (rectangle & region).get_area() > 0.1
        for existing_target, region in page_regions
    ):
        raise ValueError(f"Overlapping slide-jump hit regions on slide {source + 1}")
    page_regions.append((target, rectangle))


def restore_slide_links(deck: Path, rendered: Path, output: Path) -> dict:
    count, jumps = read_slide_jumps(deck)
    if output.exists():
        raise ValueError("PDF destination already exists; choose a fresh output")
    expected: Counter = Counter()
    hit_regions: dict[int, list[tuple[int, pymupdf.Rect]]] = {}
    with pymupdf.open(rendered) as document:
        if len(document) != count:
            raise ValueError("Rendered PDF and presentation slide counts differ")
        for page in document:
            for link in page.get_links():
                if link["kind"] == pymupdf.LINK_GOTO:
                    page.delete_link(link)
        for jump in jumps:
            page = document[jump.source]
            x, y, w, h = jump.box
            bounds = page.rect
            rectangle = pymupdf.Rect(
                x * bounds.width,
                y * bounds.height,
                (x + w) * bounds.width,
                (y + h) * bounds.height,
            )
            add_hit_region(hit_regions, jump.source, jump.target, rectangle)
            page.insert_link(
                {
                    "kind": pymupdf.LINK_GOTO,
                    "from": rectangle,
                    "page": jump.target,
                    "to": pymupdf.Point(0, 0),
                }
            )
            expected[jump_key(jump.source, jump.target, rectangle)] += 1
        document.save(output, garbage=4, deflate=True)
    actual: Counter = Counter()
    saved_regions: dict[int, list[tuple[int, pymupdf.Rect]]] = {}
    with pymupdf.open(output) as document:
        for number, page in enumerate(document):
            for link in page.get_links():
                if link["kind"] == pymupdf.LINK_GOTO:
                    add_hit_region(saved_regions, number, link["page"], link["from"])
                    actual[jump_key(number, link["page"], link["from"])] += 1
    if actual != expected:
        raise ValueError("PDF slide-jump readback differs from the presentation")
    return {
        "slides": count,
        "fixed_slide_jumps": len(jumps),
        "all_destinations_and_hit_regions_verified": True,
        "unambiguous_hit_regions": True,
    }


def render_preview(deck: Path, output: Path) -> dict:
    office = shutil.which("libreoffice")
    if office is None:
        raise ValueError("LibreOffice is required for a Linux preview")
    repository = Path(__file__).resolve().parents[2]
    output = output.resolve()
    if output.is_relative_to(repository):
        raise ValueError("Preview output must be outside the repository")
    if not deck.is_file():
        raise ValueError("Input presentation does not exist")
    output.mkdir(parents=True, exist_ok=False)
    raw = output / "libreoffice"
    raw.mkdir()
    version = subprocess.run(
        [office, "--version"], check=True, capture_output=True, text=True, timeout=30
    ).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="capstone-office-") as profile:
        subprocess.run(
            [
                office,
                f"-env:UserInstallation={Path(profile).as_uri()}",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(raw),
                str(deck.resolve()),
            ],
            check=True,
            timeout=180,
        )
    pdf = output / f"{deck.stem}.pdf"
    navigation = restore_slide_links(deck, raw / pdf.name, pdf)
    images = output / "slides"
    images.mkdir()
    with pymupdf.open(pdf) as document:
        for number, page in enumerate(document, start=1):
            scale = 1600 / page.rect.width
            page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False).save(
                images / f"slide-{number:03}.png"
            )
    report = {
        "renderer": version,
        "native_powerpoint_validation": False,
        "source_sha256": hashlib.sha256(deck.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "navigation": navigation,
        "rendered_images": navigation["slides"],
        "text_bound_metrics": "Not native PowerPoint metrics; inspect rendered images and measure source frames separately.",
        "human_acceptance": False,
    }
    (output / "preview-validation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, required=True, help="Verified candidate PPTX"
    )
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="New external preview directory"
    )
    return parser


def main() -> int:
    parser = create_parser()
    arguments = parser.parse_args()
    try:
        report = render_preview(arguments.input, arguments.output_dir)
    except (
        OSError,
        ValueError,
        zipfile.BadZipFile,
        ET.ParseError,
        subprocess.SubprocessError,
    ) as error:
        parser.exit(1, f"Preview failed: {error}\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
