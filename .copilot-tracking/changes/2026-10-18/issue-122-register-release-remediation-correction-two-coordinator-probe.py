"""Independent SQL-unavailable export reproduction with constructed records."""

import copy
import json
import subprocess
import unittest
from unittest.mock import patch

from test_continuity_epoch_export import OfflineTests
from zava_forward.core import continuity
from zava_forward.core.assistants import Assistants


class UnavailableSource(unittest.TestCase):
    def test_migration_failure_cannot_certify_retained_sql_evidence_absent(self):
        f = OfflineTests("runTest")
        f.setUp()
        try:
            retained = f.store.db.execute("SELECT COUNT(*) FROM assistant_releases").fetchone()[0]
            self.assertGreater(retained, 0)
            with patch.object(Assistants, "migrate", side_effect=RuntimeError("SYN migration unavailable")):
                unavailable = Assistants(f.store, {})
            try:
                self.assertFalse(unavailable.sql)
                self.assertIsNotNone(unavailable.schema_error)
                part = unavailable.export()
                bundle = f.store.continuity_export(f.pm, part)
                external_head = copy.deepcopy(bundle["ledger"]["head"])
                verified = continuity.verify_export(bundle, external_head)
                print(json.dumps(dict(
                    retained_release_count=retained,
                    source=part,
                    complete=bundle["complete"],
                    reasons=bundle["incomplete_reasons"],
                    verified=verified,
                )), flush=True)
                self.assertFalse(bundle["complete"], "Unavailable SQL was falsely certified complete")
                self.assertFalse(verified["valid"])
            finally:
                unavailable.stop()
        finally:
            f.tearDown()
            f.doCleanups()


if __name__ == "__main__":
    print("HEAD", subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(), flush=True)
    unittest.main(verbosity=2)
