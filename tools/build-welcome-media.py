#!/usr/bin/env python3
"""Rebuild the public welcome page's pictures from the retained capstone deck media.

Before sign-in the platform serves only a short list of paths, so welcome.py inlines the
page's pictures. This tool derives the packaged files it reads (web-sized WebP photographs
and one SVG sprite of the deck's pictograms) from docs/capstone/source/assets/media. Every
source must still match the hash pinned in the capstone asset catalog.

    python3 -m pip install -r tools/build-welcome-media-requirements.txt
    python3 tools/build-welcome-media.py            # write the files
    python3 tools/build-welcome-media.py --check    # compare with the files on disk
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("docs/capstone/source/assets")
WEB = Path("src/api/src/zava_forward/api/web")
# Output file: (deck media file, output width in pixels, WebP quality).
PHOTOS = {
    "welcome-street.webp": ("image1.jpeg", 1280, 58),
    "welcome-estate.webp": ("image2.jpeg", 560, 58),
    "welcome-dusk.webp": ("image34.jpeg", 1280, 54),
    "welcome-shield.webp": ("image33.jpeg", 440, 60),
}
# Sprite symbol id: deck pictogram.
ICONS = {
    "house": "image9.png",
    "survey": "image11.png",
    "assessment": "image6.png",
    "funding": "image12.png",
    "resident": "image13.png",
    "contractor": "image14.png",
    "quality": "image15.png",
    "ai": "image16.png",
    "safety": "image24.png",
    "idea": "image10.png",
}
ICON_PIXELS = 112
ICON_COLOURS = 32
SPRITE = "welcome-icons.svg"


def pinned_hashes(root: Path) -> dict[str, str]:
    catalog = json.loads((root / MEDIA / "catalog.json").read_text())
    return {Path(item["path"]).name: item["sha256"] for item in catalog["media"]}


def source(root: Path, hashes: dict[str, str], name: str) -> Image.Image:
    data = (root / MEDIA / "media" / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != hashes.get(name):
        raise SystemExit(f"{name} no longer matches the hash pinned in the asset catalog.")
    return Image.open(io.BytesIO(data))


def photo(image: Image.Image, width: int, quality: int) -> bytes:
    image = image.convert("RGB")
    image = image.resize(
        (width, round(image.height * width / image.width)), Image.Resampling.LANCZOS
    )
    out = io.BytesIO()
    image.save(out, "WEBP", quality=quality, method=6)
    return out.getvalue()


def icon(image: Image.Image) -> bytes:
    image = image.convert("RGBA").resize((ICON_PIXELS, ICON_PIXELS), Image.Resampling.LANCZOS)
    image = image.quantize(
        colors=ICON_COLOURS, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE
    )
    out = io.BytesIO()
    image.save(out, "PNG", optimize=True)
    return out.getvalue()


def build(root: Path) -> dict[str, bytes]:
    hashes = pinned_hashes(root)
    files = {
        target: photo(source(root, hashes, name), width, quality)
        for target, (name, width, quality) in PHOTOS.items()
    }
    symbols = []
    for symbol, name in ICONS.items():
        uri = base64.b64encode(icon(source(root, hashes, name))).decode()
        size = f'width="{ICON_PIXELS}" height="{ICON_PIXELS}"'
        symbols.append(
            f'<symbol id="ic-{symbol}" viewBox="0 0 {ICON_PIXELS} {ICON_PIXELS}">'
            f'<image {size} href="data:image/png;base64,{uri}"/></symbol>'
        )
    sprite = '<svg xmlns="http://www.w3.org/2000/svg">' + "".join(symbols) + "</svg>\n"
    files[SPRITE] = sprite.encode()
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    parser.add_argument("--check", action="store_true", help="compare instead of writing")
    args = parser.parse_args(argv)
    stale = []
    for target, data in build(args.root).items():
        path = args.root / WEB / target
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                stale.append(target)
        else:
            path.write_bytes(data)
            print(f"{target}: {len(data) / 1024:.1f} KB")
    if stale:
        print("Out of date: " + ", ".join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
