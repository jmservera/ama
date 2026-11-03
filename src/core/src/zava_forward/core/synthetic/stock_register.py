"""SYNTHETIC DATA ONLY. Seeded fictional stock register, the input the fabric and EPC tools read.

This is not the original private register: it uses invented identifiers, made-up locality
themes and fictional building forms, and no map data. It exists so a register can be rebuilt
byte for byte from a seed and an as-of date. Output refuses a non-empty folder, so an existing
exercise snapshot is never replaced.

    python3 -m zava_forward.core.synthetic.stock_register --out DIR [--homes N] [--seed N]
"""

import argparse
import csv
import json
import random
from pathlib import Path

from zava_forward.core.synthetic import output_dir, provenance

VERSION = "1.0.0"
SEED = 4820260930
AS_OF = "2026-09-30"
HOMES = 60000
FILE_NAME = "stock-register.csv"
FIELDS = ["synthetic_home_id", "locality_theme", "building_form_osm"]
LOCALITIES = ("Locality A", "Locality B", "Locality C")
# Empty means no form is recorded, so the fabric tool draws a dwelling type itself.
FORMS = ("apartments", "bungalow", "terrace", "semidetached_house", "detached", "")
FORM_WEIGHTS = (0.15, 0.08, 0.30, 0.30, 0.12, 0.05)
LABEL = (
    "Wholly fictional stock register; not the private 60,000-home register, "
    "with no real addresses, map anchors or residents."
)


def rows(n: int = HOMES, seed: int = SEED) -> list[dict[str, str]]:
    rng = random.Random(f"{seed}-{VERSION}-register")
    return [
        {
            "synthetic_home_id": f"SYN-{i:05d}",
            "locality_theme": rng.choice(LOCALITIES),
            "building_form_osm": rng.choices(FORMS, FORM_WEIGHTS)[0],
        }
        for i in range(n)
    ]


def write(
    out: str | Path, n: int = HOMES, seed: int = SEED, *, as_of: str = AS_OF
) -> dict[str, object]:
    provenance.parse_as_of(as_of)
    if n <= 0:
        raise ValueError("homes must be positive")
    revision = provenance.source_revision(
        (Path(__file__), Path(provenance.__file__), Path(__file__).with_name("__init__.py"))
    )
    path = provenance.prepare_output(out)
    with (path / FILE_NAME).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows(n, seed))
    manifest: dict[str, object] = {
        "version": VERSION,
        "seed": seed,
        "as_of": as_of,
        "generator_revision": revision,
        "homes": n,
        "file_sha256": provenance.file_hashes([path / FILE_NAME]),
        "source_type": "SYNTHETIC",
        "synthetic_label": LABEL,
    }
    (path / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    parser.add_argument("--out", default=str(output_dir("stock-register")))
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--as-of", default=AS_OF, help="YYYY-MM-DD snapshot label")
    parser.add_argument("--homes", type=int, default=HOMES)
    args = parser.parse_args(argv)
    print(json.dumps(write(args.out, n=args.homes, seed=args.seed, as_of=args.as_of), indent=2))


if __name__ == "__main__":
    main()
