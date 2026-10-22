import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import climate_paired_bounds as cpb  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "docs/reference/research/climate-paired-sample-178"
REPORT = ROOT / "docs/reference/research/climate-paired-bounds-178.json"
OM_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=54.768"
PW_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point?x=1"


def om_payload(n=6):
    temp = [5.0, 6.0, 7.5, 3.2, -1.0, 4.4][:n]
    dew = [3.0, 4.5, 6.0, 1.0, -3.0, 4.0][:n]
    rh = [round(cpb.magnus_rh(t, d)) for t, d in zip(temp, dew)]
    return {
        "latitude": 54.75, "longitude": -1.5, "elevation": 98.0,
        "utc_offset_seconds": 0,
        "hourly_units": {"time": "iso8601", "temperature_2m": "°C",
                         "relative_humidity_2m": "%", "dew_point_2m": "°C"},
        "hourly": {"time": [f"2023-01-01T{h:02d}:00" for h in range(n)],
                   "temperature_2m": temp, "relative_humidity_2m": rh,
                   "dew_point_2m": dew},
    }


def power_payload(n=6, shift=0):
    keys = [f"20230101{h + shift:02d}" for h in range(n)]
    return {
        "header": {"time_standard": "UTC", "fill_value": -999.0},
        "geometry": {"coordinates": [-1.585, 54.768, 144.05]},
        "parameters": {"T2M": {"units": "C"}, "RH2M": {"units": "%"}},
        "properties": {"parameter": {
            "T2M": dict(zip(keys, [4.0, 5.0, 6.5, 2.0, -2.0, 3.0][:n])),
            "RH2M": dict(zip(keys, [90.0, 88.0, 85.0, 95.0, 97.0, 92.0][:n])),
        }},
    }


def encode(payload):
    raw = json.dumps(payload).encode()
    return raw, hashlib.sha256(raw).hexdigest()


def parse_om(payload, **override):
    raw, digest = encode(payload)
    kwargs = {"source_url": OM_URL, "retrieved_on": "2026-10-22",
              "expected_sha256": digest}
    kwargs.update(override)
    return cpb.parse_open_meteo(raw, **kwargs)


def parse_pw(payload, **override):
    raw, digest = encode(payload)
    kwargs = {"source_url": PW_URL, "retrieved_on": "2026-10-22",
              "expected_sha256": digest}
    kwargs.update(override)
    return cpb.parse_power(raw, **kwargs)


class OpenMeteoRejectionTests(unittest.TestCase):
    def mutate(self, edit):
        payload = copy.deepcopy(om_payload())
        edit(payload)
        return payload

    def assertRejected(self, payload, text, **override):
        with self.assertRaisesRegex(ValueError, text):
            parse_om(payload, **override)

    def test_accepts_consistent_series(self):
        series = parse_om(om_payload())
        self.assertEqual(len(series["times"]), 6)
        self.assertLessEqual(series["max_rh_residual"], cpb.RH_TOLERANCE)

    def test_hash_mismatch_and_url_and_date(self):
        self.assertRejected(om_payload(), "SHA-256 mismatch", expected_sha256="0" * 64)
        self.assertRejected(om_payload(), "HTTPS", source_url="http://example.org/x")
        self.assertRejected(om_payload(), "YYYY-MM-DD", retrieved_on="22/10/2026")

    def test_null_or_non_numeric_values(self):
        for key in ("temperature_2m", "relative_humidity_2m", "dew_point_2m"):
            payload = self.mutate(lambda p: p["hourly"][key].__setitem__(2, None))
            self.assertRejected(payload, "Missing or non-numeric")
        payload = self.mutate(lambda p: p["hourly"]["temperature_2m"].__setitem__(1, "6"))
        self.assertRejected(payload, "non-numeric")

    def test_short_series_each_variable(self):
        for key in ("time", "temperature_2m", "relative_humidity_2m", "dew_point_2m"):
            payload = self.mutate(lambda p: p["hourly"][key].pop())
            self.assertRejected(payload, "differ in length")

    def test_timestamp_defects(self):
        skipped = self.mutate(lambda p: p["hourly"]["time"].__setitem__(3, "2023-01-01T04:00"))
        self.assertRejected(skipped, "gap or non-hourly")
        duplicate = self.mutate(lambda p: p["hourly"]["time"].__setitem__(2, "2023-01-01T01:00"))
        self.assertRejected(duplicate, "not strictly increasing")
        reversed_ = self.mutate(lambda p: p["hourly"]["time"].reverse())
        self.assertRejected(reversed_, "not strictly increasing")
        bad = self.mutate(lambda p: p["hourly"]["time"].__setitem__(0, "yesterday"))
        self.assertRejected(bad, "Unparseable timestamp")

    def test_unit_and_timezone_mismatch(self):
        units = self.mutate(lambda p: p["hourly_units"].__setitem__("temperature_2m", "°F"))
        self.assertRejected(units, "Unexpected unit")
        zone = self.mutate(lambda p: p.__setitem__("utc_offset_seconds", 3600))
        self.assertRejected(zone, "not UTC")

    def test_humidity_range_and_dew_point(self):
        high = self.mutate(lambda p: p["hourly"]["relative_humidity_2m"].__setitem__(0, 101))
        self.assertRejected(high, "outside 0..100")
        low = self.mutate(lambda p: p["hourly"]["relative_humidity_2m"].__setitem__(0, -1))
        self.assertRejected(low, "outside 0..100")
        dew = self.mutate(lambda p: p["hourly"]["dew_point_2m"].__setitem__(0, 9.0))
        self.assertRejected(dew, "Dew point above temperature")

    def test_fabricated_humidity_rejected_at_tolerance_boundary(self):
        base = om_payload()
        exact = cpb.magnus_rh(base["hourly"]["temperature_2m"][0],
                              base["hourly"]["dew_point_2m"][0])
        inside = copy.deepcopy(base)
        inside["hourly"]["relative_humidity_2m"][0] = exact + cpb.RH_TOLERANCE - 0.01
        parse_om(inside)
        outside = copy.deepcopy(base)
        outside["hourly"]["relative_humidity_2m"][0] = exact + cpb.RH_TOLERANCE + 0.01
        self.assertRejected(outside, "inconsistent with temperature and dew point")
        constant = copy.deepcopy(base)
        constant["hourly"]["relative_humidity_2m"] = [70] * 6
        self.assertRejected(constant, "inconsistent")


class PowerRejectionTests(unittest.TestCase):
    def test_accepts_and_parses(self):
        series = parse_pw(power_payload())
        self.assertEqual(series["rh"][0], 90.0)
        self.assertEqual(series["times"][1].hour, 1)

    def test_fill_value_rejected_not_filled(self):
        payload = power_payload()
        payload["properties"]["parameter"]["RH2M"]["2023010102"] = -999.0
        with self.assertRaisesRegex(ValueError, "Fill value in relative humidity"):
            parse_pw(payload)

    def test_misaligned_humidity_keys_rejected(self):
        payload = power_payload()
        rh = payload["properties"]["parameter"]["RH2M"]
        rh["2023010106"] = rh.pop("2023010105")
        with self.assertRaisesRegex(ValueError, "timestamps differ"):
            parse_pw(payload)

    def test_units_timezone_and_gaps(self):
        payload = power_payload()
        payload["parameters"]["RH2M"]["units"] = "fraction"
        with self.assertRaisesRegex(ValueError, "units"):
            parse_pw(payload)
        payload = power_payload()
        payload["header"]["time_standard"] = "LST"
        with self.assertRaisesRegex(ValueError, "not UTC"):
            parse_pw(payload)
        payload = power_payload()
        for name in ("T2M", "RH2M"):
            payload["properties"]["parameter"][name].pop("2023010103")
        with self.assertRaisesRegex(ValueError, "gap or non-hourly"):
            parse_pw(payload)

    def test_missing_series_and_humidity_range(self):
        payload = power_payload()
        del payload["properties"]["parameter"]["RH2M"]
        with self.assertRaisesRegex(ValueError, "Missing T2M or RH2M"):
            parse_pw(payload)
        payload = power_payload()
        payload["properties"]["parameter"]["RH2M"]["2023010101"] = 120.0
        with self.assertRaisesRegex(ValueError, "outside 0..100"):
            parse_pw(payload)


class DerivationTests(unittest.TestCase):
    def test_percentile_interpolation_and_ties(self):
        values = [10.0, 20.0, 30.0, 40.0, 50.0]
        self.assertEqual(cpb.percentile(values, 0), 10.0)
        self.assertEqual(cpb.percentile(values, 100), 50.0)
        self.assertEqual(cpb.percentile(values, 50), 30.0)
        self.assertAlmostEqual(cpb.percentile(values, 10), 14.0)
        self.assertAlmostEqual(cpb.percentile(values, 99), 49.6)
        self.assertEqual(cpb.percentile([7.0], 99), 7.0)

    def test_derive_hand_computed_extremes_with_pairing(self):
        series = parse_om(om_payload())
        derived = cpb.derive(series)
        temp = derived["temperature"]
        self.assertEqual(temp["minimum"]["value"], -1.0)
        self.assertEqual(temp["minimum"]["occurrences"][0]["time"], "2023-01-01T04:00Z")
        self.assertEqual(temp["minimum"]["occurrences"][0]["paired_rh"],
                         series["rh"][4])
        self.assertEqual(temp["maximum"]["value"], 7.5)
        self.assertAlmostEqual(temp["mean"], round(sum(series["temperature"]) / 6, 3))
        self.assertEqual(temp["monthly"], {"2023-01": {"minimum": -1.0, "maximum": 7.5}})
        rh = derived["relative_humidity"]
        self.assertEqual(rh["maximum"]["value"], max(series["rh"]))

    def test_tied_extremum_lists_every_hour(self):
        payload = om_payload()
        payload["hourly"]["temperature_2m"][5] = 7.5
        payload["hourly"]["dew_point_2m"][5] = 6.0
        payload["hourly"]["relative_humidity_2m"][5] = round(cpb.magnus_rh(7.5, 6.0))
        times = [o["time"] for o in cpb.derive(parse_om(payload))
                 ["temperature"]["maximum"]["occurrences"]]
        self.assertEqual(times, ["2023-01-01T02:00Z", "2023-01-01T05:00Z"])


class CrossSourceTests(unittest.TestCase):
    def test_compare_by_timestamp(self):
        result = cpb.compare(parse_om(om_payload()), parse_pw(power_payload()))
        self.assertEqual(result["common_hour_count"], 6)
        self.assertEqual(result["start"], "2023-01-01T00:00Z")
        self.assertEqual(result["end"], "2023-01-01T05:00Z")
        # (25.1 - 18.5) / 6 hand-computed from the two constructed series
        self.assertAlmostEqual(result["temperature_degC"]["mean_difference"], 1.1, places=3)
        self.assertAlmostEqual(
            result["temperature_degC"]["mean_absolute_difference"], 1.1, places=3)

    def test_one_hour_shift_rejected(self):
        with self.assertRaisesRegex(ValueError, "exact same UTC hour set"):
            cpb.compare(parse_om(om_payload()), parse_pw(power_payload(shift=1)))

    def test_different_length_rejected(self):
        with self.assertRaisesRegex(ValueError, "exact same UTC hour set"):
            cpb.compare(parse_om(om_payload()), parse_pw(power_payload(n=5)))


class CommittedSampleTests(unittest.TestCase):
    OM_FILE = SAMPLE / "open-meteo-era5-durham-2023-raw.json"
    PW_FILE = SAMPLE / "nasa-power-merra2-durham-2023-raw.json"
    OM_SHA = "96e707ea5f7bd35af3ebdf896c7f9a41a055d220a0a0e832aa5ad008b7484a26"
    PW_SHA = "cba9cf308878e9a4b2f2847cbbc4e66f06d14a1b734d4da48be0133fef9c6db1"

    def build(self):
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        sources = report["sources"]
        primary = cpb.parse_open_meteo(
            self.OM_FILE.read_bytes(),
            source_url=sources["open_meteo_era5"]["request_url"],
            retrieved_on="2026-10-22", expected_sha256=self.OM_SHA)
        secondary = cpb.parse_power(
            self.PW_FILE.read_bytes(),
            source_url=sources["nasa_power_merra2"]["request_url"],
            retrieved_on="2026-10-22", expected_sha256=self.PW_SHA)
        return report, primary, secondary

    def test_committed_report_regenerates_from_raw_fixtures(self):
        report, primary, secondary = self.build()
        request = report["sources"]["open_meteo_era5"]["requested_location"]
        rebuilt = json.loads(json.dumps(
            cpb.build_report(primary, secondary, request), ensure_ascii=False))
        self.assertEqual(rebuilt, report)

    def test_fixture_properties_and_labels(self):
        report, primary, secondary = self.build()
        self.assertEqual(report["cross_source_check"]["common_hour_count"], 8760)
        self.assertEqual(len(primary["times"]), 8760)
        self.assertEqual(report["bounds"]["temperature"]["minimum"]["value"],
                         min(primary["temperature"]))
        self.assertEqual(report["bounds"]["relative_humidity"]["maximum"]["value"],
                         max(primary["rh"]))
        self.assertLess(report["validation"]["open_meteo_max_rh_residual_rh_points"],
                        cpb.RH_TOLERANCE)
        self.assertIs(report["observed"], False)
        self.assertEqual(report["owner_reuse_approval"], "UNMET")
        self.assertEqual(report["production_status"], "pending")
        self.assertIs(report["licence_and_attribution"]["open_meteo"]
                      ["underlying_c3s_reuse_verified"], False)

    def test_durham_temperature_only_evidence_kept_separate(self):
        durham = json.loads((ROOT / "docs/reference/research/"
                             "climate-source-evidence-178.json").read_text())
        self.assertEqual(durham["humidity"]["status"], "unavailable")
        self.assertEqual(durham["source"]["station"], "Durham")


if __name__ == "__main__":
    unittest.main()
