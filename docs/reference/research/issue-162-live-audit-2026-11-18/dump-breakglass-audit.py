"""Drive the real server break-glass route on synthetic data and print the stored audit rows."""
import json, os, sys, unittest
sys.path.insert(0, "tests")
import test_chat_isolation as t

class Dump(t.ChatIsolationTests):
    def test_zz_dump(self):
        self.test_break_glass_is_default_deny_audited_and_metadata_only()
        for e in self.store.audit_entries():
            if e["action"].startswith("chat.breakglass"):
                print(e["action"], e["detail"])

if __name__ == "__main__":
    s = unittest.TestSuite([Dump("test_zz_dump")])
    unittest.TextTestRunner(verbosity=0).run(s)
