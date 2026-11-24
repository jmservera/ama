import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dataset
from zava_forward.core import continuity
from zava_forward.core.sqlstore import SqlStore


class DemoOwnerOverrideTests(unittest.TestCase):
    def test_override_needs_exact_value_and_the_demo_profile(self) -> None:
        name = continuity.DEMO_OWNER_OVERRIDE_ENV
        value = "owner-directed-2026-11-23"
        demo = {"ZF_DEPLOYMENT_PROFILE": "demo"}
        self.assertFalse(continuity.demo_owner_override({}))
        self.assertFalse(continuity.demo_owner_override({name: "1", **demo}))
        self.assertFalse(continuity.demo_owner_override({name: value}))
        self.assertFalse(continuity.demo_owner_override({name: value, "ZF_ENV": "production"}))
        # The live demo runs with ZF_ENV=production and the demo profile.
        self.assertTrue(
            continuity.demo_owner_override({name: value, "ZF_ENV": "production", **demo})
        )

    def test_sql_store_hold_is_lifted_by_the_override_and_the_record_stays_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "zavaforward.json"
            data.write_text(json.dumps(dataset.DATA))
            store = SqlStore(str(data), os.path.join(tmp, "pw.sqlite"))  # type: ignore[no-untyped-call]
            self.addCleanup(store.db.close)
            manager = next(
                p for p in dataset.DATA["staff"] if p["role"] == "Retrofit Programme Manager"
            )
            store.suspend(
                manager,
                {
                    "scope": "all",
                    "reason": "SYN override probe",
                    "incident_owner": "SYN owner",
                    "containment": "SYN containment",
                    "comms_owner": "SYN comms",
                    "comms_audience": "SYN audience",
                    "synthetic": True,
                },
            )
            name, value = continuity.DEMO_OWNER_OVERRIDE_ENV, "owner-directed-2026-11-23"
            self.assertIsNotNone(store.continuity_suspension("chat"))  # type: ignore[no-untyped-call]
            demo = {name: value, "ZF_DEPLOYMENT_PROFILE": "demo", "ZF_ENV": "production"}
            with patch.dict(os.environ, demo):
                self.assertIsNone(store.continuity_suspension("chat"))  # type: ignore[no-untyped-call]
                self.assertIsNone(store.continuity_block("chat"))  # type: ignore[no-untyped-call]
            with patch.dict(os.environ, {name: value, "ZF_ENV": "production"}):
                self.assertIsNotNone(store.continuity_suspension("chat"))  # type: ignore[no-untyped-call]
            self.assertIsNotNone(store.continuity_suspension("chat"))  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    unittest.main()
