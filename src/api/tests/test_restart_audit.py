"""Single-replica restart: audit ledger entries persist across a store restart (issue 144)."""

import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.sqlstore import SqlStore

import test_mvp


class RestartAudit(unittest.TestCase):
    def test_ledger_survives_restart_and_continues_the_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "zavaforward.json"
            seed.write_text(json.dumps(test_mvp.DATA))
            sqlite_path = str(Path(tmp) / "audit.sqlite")
            sam = test_mvp.DATA["staff"][0]
            first = SqlStore(str(seed), sqlite_path)
            for index in range(3):
                first.log_call(sam, "ZF-1", f"Call {index}", "")
            first.write_digest()
            entries, head = first.ledger_head()
            first.db.close()

            restarted = SqlStore(str(seed), sqlite_path)
            self.addCleanup(restarted.db.close)
            self.assertEqual(restarted.ledger_head(), (entries, head))
            self.assertTrue(restarted.verify_ledger()["intact"])
            restarted.log_call(sam, "ZF-1", "After restart", "")
            report = restarted.verify_ledger()
            self.assertTrue(report["intact"])
            self.assertEqual(report["entries"], entries + 1)
            self.assertEqual(report["digests_checked"], 1)


if __name__ == "__main__":
    unittest.main()
