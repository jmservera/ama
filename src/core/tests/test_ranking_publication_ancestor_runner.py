"""Runner-level ancestor sync tests for the ranking archive (Refs #1258).

Mocked syscall order only; this is not proof of real crash or filesystem durability.
"""

import errno
import os
import stat
import unittest
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

from test_ranking_publication_runner import TODAY, RunnerBase

ANCESTORS = ("root", "a", "b")


class RunnerAncestorSyncTests(RunnerBase):
    def setUp(self) -> None:
        super().setUp()
        self.base = self.root / "mount"
        self.base.mkdir()
        self.nested = self.base / "a" / "b" / "archive"
        self.dirs = {
            "root": self.base,
            "a": self.base / "a",
            "b": self.base / "a" / "b",
            "archive": self.nested,
        }

    def label(self, fd: int) -> str:
        st = os.fstat(fd)
        if not stat.S_ISDIR(st.st_mode):
            return "file"
        for name, path in self.dirs.items():
            try:
                if os.path.samestat(st, os.stat(path)):
                    return name
            except OSError:
                continue
        return "other"

    def recording(self, fault: str | None, events: list[str]) -> Callable[[int], None]:
        real = os.fsync

        def sync(fd: int) -> None:
            name = self.label(fd)
            events.append(name)
            if name == fault:
                raise OSError(errno.EIO, "sync failed")
            real(fd)

        return sync

    def publish(self) -> tuple[int, dict[str, object]]:
        cases = self.cases_file()
        with self.registry_patched():
            return self.cli(
                "publish", "--archive", str(self.nested), "--today", TODAY, "--cases", str(cases)
            )

    def test_new_ancestors_are_synced_deepest_first_before_the_run_is_confirmed(self) -> None:
        events: list[str] = []
        with patch.object(os, "fsync", self.recording(None, events)):
            code, res = self.publish()
        self.assertEqual(code, 0)
        self.assertEqual(res["status"], "published")
        known = [e for e in events if e != "other"]
        self.assertEqual(known, ["file", "archive", "b", "a", "root"])

    def test_each_new_ancestor_sync_failure_is_unconfirmed_path_free_and_keeps_the_record(
        self,
    ) -> None:
        for fault in ANCESTORS:
            with self.subTest(fault=fault):
                self.setUp()
                events: list[str] = []
                with patch.object(os, "fsync", self.recording(fault, events)):
                    code, res = self.publish()
                self.assertEqual((code, res["status"]), (2, "committed_unconfirmed"))
                uncertainty = res["uncertainty"]
                assert isinstance(uncertainty, dict)
                self.assertNotIn(str(self.base), str(uncertainty["message"]))
                self.assertNotIn("/", str(uncertainty["message"]))
                records: list[Path] = list(self.nested.iterdir())
                self.assertEqual(len(records), 1)
                self.assertIn(fault, events)


if __name__ == "__main__":
    unittest.main()
