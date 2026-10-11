#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""Read and edit the per-slide content YAML of a powerpoint-skill deck.

Import it from an edit script for round-trip-safe helpers, or run it as a CLI:

    python deck_yaml.py text --content-dir <deck>/content
    python deck_yaml.py insert --content-dir <deck>/content --at 10

``text`` prints every slide's element text and speaker-note word counts, with
separate totals for main slides and appendix slides (title starts with
"Appendix"). ``insert`` shifts slide-NNN folders from ``--at`` upwards by one so
a new slide can be saved at that position.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2
WORDS_PER_MINUTE = 140


class LiteralDumper(yaml.SafeDumper):
    """YAML dumper that writes multiline strings as literal blocks."""


def _str_representer(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


LiteralDumper.add_representer(str, _str_representer)


def slide_dir(content_dir: Path, number: int) -> Path:
    return content_dir / f"slide-{number:03d}"


def load_slide(content_dir: Path, number: int) -> dict[str, Any]:
    path = slide_dir(content_dir, number) / "content.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_slide(content_dir: Path, number: int, data: dict[str, Any]) -> None:
    folder = slide_dir(content_dir, number)
    folder.mkdir(parents=True, exist_ok=True)
    data["slide"] = number
    text = yaml.dump(data, Dumper=LiteralDumper, sort_keys=False, allow_unicode=True, width=100)
    (folder / "content.yaml").write_text(text, encoding="utf-8")


def element(data: dict[str, Any], name: str) -> dict[str, Any]:
    for item in data.get("elements", []):
        if item.get("name") == name:
            return item
    raise KeyError(f"No element named {name!r} on slide {data.get('slide')}")


def set_paragraph(data: dict[str, Any], name: str, index: int, text: str) -> None:
    element(data, name)["paragraphs"][index]["text"] = text


def slide_numbers(content_dir: Path) -> list[int]:
    numbers = []
    for folder in content_dir.glob("slide-[0-9][0-9][0-9]"):
        if (folder / "content.yaml").is_file():
            numbers.append(int(folder.name.split("-")[1]))
    return sorted(numbers)


def element_text(item: dict[str, Any]) -> str:
    parts = []
    if isinstance(item.get("text"), str) and item["text"].strip():
        parts.append(item["text"])
    for paragraph in item.get("paragraphs") or []:
        if paragraph.get("text"):
            parts.append(paragraph["text"])
    for row in item.get("rows") or []:
        cells = [cell.get("text", "") for cell in row.get("cells", [])]
        parts.append(" | ".join(cells))
    return " / ".join(part.replace("\n", " / ") for part in parts)


def title_of(data: dict[str, Any]) -> str:
    try:
        return element(data, "Title").get("text", "") or ""
    except KeyError:
        return data.get("title", "") or ""


def spoken_notes(notes: str) -> str:
    """Return the spoken script, excluding the evidence/source register."""
    return re.split(r"\n\s*Evidence:\s*\n", notes, maxsplit=1, flags=re.IGNORECASE)[0]


def insert_slot(content_dir: Path, position: int) -> None:
    """Shift slides at or after ``position`` up by one, highest first."""
    for number in reversed(slide_numbers(content_dir)):
        if number < position:
            break
        source = slide_dir(content_dir, number)
        target = slide_dir(content_dir, number + 1)
        if target.exists():
            raise FileExistsError(f"{target} already exists")
        source.rename(target)
        data = load_slide(content_dir, number + 1)
        save_slide(content_dir, number + 1, data)


def print_text(content_dir: Path) -> None:
    main_words = 0
    appendix_words = 0
    all_notes_words = 0
    for number in slide_numbers(content_dir):
        data = load_slide(content_dir, number)
        notes = data.get("speaker_notes") or ""
        words = len(spoken_notes(notes).split())
        total_words = len(notes.split())
        title = title_of(data).replace("\n", " ")
        section = str(data.get("section", "")).strip().lower()
        is_appendix = section.startswith("appendix") or title.lower().startswith("appendix")
        if is_appendix:
            appendix_words += words
        else:
            main_words += words
        all_notes_words += total_words
        print(f"===== slide-{number:03d} ({'appendix' if is_appendix else 'main'}) {title}")
        for item in data.get("elements", []):
            text = element_text(item)
            if text and item.get("name") != "Title":
                print(f"  [{item.get('name')}] {text}")
        print(f"  NOTES ({words} spoken words; {total_words} total incl. evidence): {notes.strip()}")
    minutes = main_words / WORDS_PER_MINUTE
    print(f"\nMain spoken script: {main_words} words, about {minutes:.1f} minutes at {WORDS_PER_MINUTE} wpm")
    print(f"Appendix spoken script: {appendix_words} words")
    print(f"All speaker notes: {all_notes_words} words, including evidence citations")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    text = sub.add_parser("text", help="Print slide text and speaker-note word counts")
    text.add_argument("--content-dir", type=Path, required=True)
    insert = sub.add_parser("insert", help="Open an empty slot at a slide position")
    insert.add_argument("--content-dir", type=Path, required=True)
    insert.add_argument("--at", type=int, required=True)
    return parser


def run(args: argparse.Namespace) -> int:
    if not args.content_dir.is_dir():
        print(f"Content directory not found: {args.content_dir}", file=sys.stderr)
        return EXIT_ERROR
    if args.command == "text":
        print_text(args.content_dir)
    elif args.command == "insert":
        insert_slot(args.content_dir, args.at)
        print(f"Opened slide-{args.at:03d}; later slides shifted by one")
    return EXIT_SUCCESS


def main() -> int:
    try:
        return run(create_parser().parse_args())
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - report any failure as a CLI error
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
