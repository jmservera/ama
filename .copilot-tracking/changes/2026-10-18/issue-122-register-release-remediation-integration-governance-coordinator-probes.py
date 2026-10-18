"""Independent constructed-fixture verification; no implementation writes."""

import contextlib
import copy
import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import test_continuity_epoch_export as fixture
from zava_forward.core import continuity


@contextlib.contextmanager
def opened(kind):
    case = kind("runTest")
    case.setUp()
    try:
        yield case
    finally:
        case.tearDown()
        case.doCleanups()


def reseal(bundle):
    bundle["complete"] = True
    bundle["incomplete_reasons"] = []
    bundle["digest"] = continuity.sha({k: v for k, v in bundle.items() if k != "digest"})
    return json.loads(json.dumps(bundle))


class IndependentControls(unittest.TestCase):
    def test_oversized_json_numbers_and_valid_controls_at_both_boundaries(self):
        with opened(fixture.OfflineTests) as f:
            part = f.service.export()
            original = f.store.continuity_export(f.pm, part)
            head = copy.deepcopy(original["ledger"]["head"])
            self.assertTrue(continuity.verify_export(original, head)["valid"])
            values = (
                (10**309, False),
                (-(10**309), False),
                (10**500, False),
                (-(10**500), False),
                (10**300, True),
                (-12.5, True),
                (0, True),
                (True, False),
                ("1", False),
            )
            for boundary in ("producer", "verifier"):
                for value, valid in values:
                    with self.subTest(boundary=boundary, value=value):
                        source = copy.deepcopy(part if boundary == "producer" else original)
                        source["task_releases"]["records"][0]["events"][0]["at"] = value
                        source = json.loads(json.dumps(source))
                        if boundary == "producer":
                            bundle = f.store.continuity_export(f.pm, source)
                            expected = copy.deepcopy(bundle["ledger"]["head"])
                            self.assertEqual(bundle["complete"], valid)
                        else:
                            bundle, expected = reseal(source), head
                        result = continuity.verify_export(bundle, expected)
                        self.assertEqual(result["valid"], valid, result)
                        self.assertEqual(result["complete"], valid, result)
                        self.assertEqual(bundle["ledger"]["head"], expected)
                        self.assertFalse(
                            any("digest mismatch" in p or "externally held" in p
                                for p in result["problems"]),
                            result,
                        )
                        if not valid:
                            self.assertIn("invalid task-release event envelope", result["problems"])

    def test_unreferenced_releases_cannot_hide_missing_or_misbound_lifecycle(self):
        with opened(fixture.OfflineTests) as f:
            part = f.service.export()
            self.assertEqual(part["proposals"], [])
            original = f.store.continuity_export(f.pm, part)
            self.assertTrue(continuity.verify_export(original, original["ledger"]["head"])["valid"])
            for defect in ("missing", "wrong-release", "truncated", "wrong-status"):
                with self.subTest(defect=defect):
                    bad = copy.deepcopy(original)
                    row = bad["task_releases"]["records"][-1]
                    if defect == "missing":
                        row["events"] = []
                    elif defect == "wrong-release":
                        row["events"][0]["release_id"] = "SYNTHETIC-OTHER-RELEASE"
                    elif defect == "truncated":
                        row["truncated"] = True
                    else:
                        row["current_status"] = "revoked"
                    result = continuity.verify_export(reseal(bad), original["ledger"]["head"])
                    self.assertFalse(result["valid"], result)
                    self.assertFalse(result["complete"], result)
                    self.assertFalse(
                        any("digest mismatch" in p or "externally held" in p
                            for p in result["problems"]),
                        result,
                    )

    def test_real_http_register_projection_tracks_recorded_need_without_mutation(self):
        with opened(fixture.HttpTests) as f:
            marker = "SYNTHETIC-INDEPENDENT-122-REGISTER"
            f.store.suspend(f.pm, dict(fixture.SUSPEND, reason=marker, containment=marker))
            before = copy.deepcopy(f.store._cont())
            for allowed in (False, True, False):
                roles = "Programme Support Officer,Quality Inspector" if allowed else ""
                with patch.dict(os.environ, {"ZF_REASON_ROLES": roles}):
                    for role in ("Programme Support Officer", "Quality Inspector"):
                        f.user = f.people[role]
                        status, result = f.request("/api/continuity")
                        self.assertEqual(status, 200, result)
                        self.assertEqual(marker in json.dumps(result), allowed)
                        self.assertEqual(result["suspensions"][0]["status"], "Suspended")
                        self.assertFalse(result["suspensions"][0]["communication"]["sent"])
                        self.assertEqual(f.store._cont(), before)


if __name__ == "__main__":
    source = Path(continuity.__file__)
    print("HEAD", subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip())
    print("CONTINUITY", source, hashlib.sha256(source.read_bytes()).hexdigest(), flush=True)
    unittest.main(verbosity=2)
