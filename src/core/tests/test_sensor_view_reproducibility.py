"""Sensor view digests depend only on retained readings and `as_of` (Refs #111 criterion 1).

Fictional exercise readings only.
"""

import random
import unittest
from typing import Any

from zava_forward.core import sensor_view


def reading(i: int) -> dict[str, Any]:
    return dict(
        sensor_id="SENS-SYN-1",
        reading_id=f"R-{i:03d}",
        observed_at=f"2024-10-01T{i:02d}:00:00Z",
        temperature_c=str(18 + i),
        humidity_pct=str(50 + i),
    )


class RowsDigest(unittest.TestCase):
    def test_order_and_repeats_do_not_change_digest(self) -> None:
        rows = [reading(i) for i in range(10)]
        shuffled = rows[:]
        random.Random(111).shuffle(shuffled)
        expected = sensor_view.rows_digest(rows)
        self.assertEqual(expected, sensor_view.rows_digest(shuffled))
        self.assertEqual(expected, sensor_view.rows_digest(rows + rows[:3]))

    def test_changed_value_or_missing_row_changes_digest(self) -> None:
        rows = [reading(i) for i in range(5)]
        base = sensor_view.rows_digest(rows)
        self.assertNotEqual(base, sensor_view.rows_digest(rows[:-1]))
        self.assertNotEqual(
            base, sensor_view.rows_digest(rows[:-1] + [dict(rows[-1], humidity_pct="99")])
        )


class Reproducibility(unittest.TestCase):
    def out(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return dict(
            home_id="ZF-1",
            state="ok",
            generated_at="2024-10-02T00:00:00Z",
            readings=rows,
            before=[],
            after=[],
            trend={},
        )

    def test_versioned_digests_ignore_row_order(self) -> None:
        rows = [reading(i) for i in range(8)]
        first = sensor_view.reproducibility(self.out(rows))
        again = sensor_view.reproducibility(self.out(list(reversed(rows))))
        self.assertEqual(first, again)
        self.assertEqual(first["analysis_version"], sensor_view.ANALYSIS_VERSION)
        self.assertEqual(first["reading_count"], 8)

    def test_as_of_changes_output_but_not_input_digest(self) -> None:
        rows = [reading(i) for i in range(3)]
        a = sensor_view.reproducibility(self.out(rows))
        b = sensor_view.reproducibility(dict(self.out(rows), generated_at="2024-10-03T00:00:00Z"))
        self.assertEqual(a["input_digest"], b["input_digest"])
        self.assertNotEqual(a["output_digest"], b["output_digest"])


if __name__ == "__main__":
    unittest.main()
