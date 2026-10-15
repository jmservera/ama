"""Allowlisted synthetic stock inputs for backfill, never real monitoring consent."""

import csv
import hashlib
import json
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from zava_forward.core.synthetic import stock_fabric

VERSION = "stock-sensor-v1"
INPUT_FIELDS = (
    "synthetic_home_id",
    "building_form_osm",
    "locality_theme",
    "is_synthetic",
    "monitoring_consent",
)
CONSTRUCTION_LOSS = {
    "Solid brick": 1.15,
    "Stone": 1.20,
    "Cavity brick": 1.0,
    "Non-traditional (precast concrete)": 1.10,
    "Timber frame": 0.90,
    "Cavity brick, partial fill": 0.85,
    "Cavity brick, full fill": 0.75,
}
DWELLING = {value: key for key, value in stock_fabric.FORM_TO_DWELLING.items()}
FABRIC_FIELDS = [*stock_fabric.FIELDS, "monitoring_consent"]


@dataclass(frozen=True)
class Selection:
    register_homes: int
    input_sha256: str
    rows: tuple[dict[str, str], ...]

    def coverage(self) -> dict[str, object]:
        choices = Counter(row["monitoring_consent"] for row in self.rows)
        return dict(
            register_homes=self.register_homes,
            selected_homes=len(self.rows),
            unselected_homes=self.register_homes - len(self.rows),
            monitored_homes=choices["granted"],
            declined_homes=choices["declined"],
            unknown_homes=choices["unknown"],
            selected_home_ids=[row["synthetic_home_id"] for row in self.rows],
            excluded=[
                dict(home_id=row["synthetic_home_id"], reason=row["monitoring_consent"])
                for row in self.rows
                if row["monitoring_consent"] != "granted"
            ],
            scope="Synthetic register anchors only; not verified dwelling or resident consent.",
        )

    def fabric_rows(self) -> list[dict[str, object]]:
        return [
            {**stock_fabric.fabric(row), "monitoring_consent": row["monitoring_consent"]}
            for row in self.rows
        ]

    def sensors(self, seed: int) -> list[dict[str, object]]:
        sensors: list[dict[str, object]] = []
        for row in self.rows:
            if row["monitoring_consent"] != "granted":
                continue
            fabric = stock_fabric.fabric(row)
            home_id = row["synthetic_home_id"]
            rng = random.Random(f"{seed}-sensor-{home_id}")
            year = fabric["build_year"]
            age = (
                "pre-1919"
                if year < 1919
                else "1919-1944"
                if year < 1945
                else "1945-1979"
                if year < 1980
                else "1980-2002"
                if year < 2003
                else "2003+"
            )
            sensors.append(
                dict(
                    sensor_id="SENS-SYN-" + hashlib.sha256(home_id.encode()).hexdigest(),
                    home_id=home_id,
                    dwelling_type=DWELLING[fabric["dwelling_type"]],
                    age_band=age,
                    retrofitted=False,
                    heating_pattern=rng.choice(["morning_evening", "all_day", "low"]),
                    fault_profile=rng.choices(
                        ["none", "outlier", "stuck", "dropout"], [70, 12, 6, 12]
                    )[0],
                    source_type="SYNTHETIC",
                    construction_loss=CONSTRUCTION_LOSS[fabric["construction"]],
                )
            )
        return sensors


def select(register: Sequence[Mapping[str, str]], homes: int | None) -> Selection:
    if homes is None or homes <= 0:
        raise ValueError("Register mode requires an explicit positive homes subset")
    if homes > len(register):
        raise ValueError("homes exceeds the supplied register size")
    clean: list[dict[str, str]] = []
    ids: set[str] = set()
    for row in register:
        home_id = row.get("synthetic_home_id", "")
        if (
            not home_id
            or home_id != home_id.strip()
            or len(home_id.encode("utf-16-le")) // 2 > 128
            or any(ord(char) < 32 or ord(char) == 127 for char in home_id)
            or home_id in ids
        ):
            raise ValueError(
                "Stock home IDs must be unique, nonblank, unpadded and <=128 UTF-16 units"
            )
        if row.get("is_synthetic", "").lower() != "true":
            raise ValueError("Register mode requires is_synthetic=true on every home")
        choice = row.get("monitoring_consent", "") or "unknown"
        if choice not in {"granted", "declined", "unknown"}:
            raise ValueError("monitoring_consent must be granted, declined or unknown")
        ids.add(home_id)
        clean.append(
            dict(
                synthetic_home_id=home_id,
                building_form_osm=row.get("building_form_osm", ""),
                locality_theme=row.get("locality_theme", ""),
                is_synthetic="true",
                monitoring_consent=choice,
            )
        )
    clean.sort(key=lambda row: row["synthetic_home_id"])
    digest = hashlib.sha256(
        json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return Selection(len(clean), digest, tuple(clean[:homes]))


def read_register(path: Path, homes: int | None) -> Selection:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Register requires unique CSV column names")
        if not {"synthetic_home_id", "is_synthetic"} <= set(reader.fieldnames):
            raise ValueError("Register requires synthetic_home_id and is_synthetic columns")
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("Register rows must match the CSV header")
            rows.append({key: row[key] for key in INPUT_FIELDS if key in row})
    return select(rows, homes)
