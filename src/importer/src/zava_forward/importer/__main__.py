import argparse
import sys
from pathlib import Path

from zava_forward.importer.mapping import STRUCTURES, preview_file
from zava_forward.importer.version import __version__
from zava_forward.importer.xlsx import WorkbookError


def main(argv: list[str]) -> int:
    if not argv:
        print(f"zava-forward-import {__version__}")
        return 0
    parser = argparse.ArgumentParser(prog="zava_forward.importer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser(
        "preview", help="show mapping, conflicts and a row-level preview; changes nothing"
    )
    p.add_argument("file", type=Path)
    p.add_argument("--structure", default="case-list", choices=sorted(STRUCTURES))
    args = parser.parse_args(argv)
    try:
        prev, _ = preview_file(args.file, STRUCTURES[args.structure])
    except (WorkbookError, OSError) as exc:
        print(f"Cannot import: {exc}", file=sys.stderr)
        return 2
    print(
        f"{prev.message} source={prev.source_name} sha256={prev.source_sha256} sheet={prev.sheet}"
    )
    for c in prev.columns:
        print(f"  {c.field}: {c.header or '-'} ({c.how})")
    for text in prev.conflicts:
        print(f"  CONFLICT: {text}")
    print(f"  ready={prev.ready} to_fix={len(prev.to_fix)}")
    for r in prev.rows:
        print(f"  row {r.row}: {'OK' if not r.problems else '; '.join(r.problems)}")
    return 1 if prev.blocking else 0


sys.exit(main(sys.argv[1:]))
