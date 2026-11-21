"""Container hardening guard on Azure Container Apps (#144): CapInh drop and private scratch."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.container_hardening import (
    ContainerHardeningError,
    HardeningReport,
    _drop_inheritable_capabilities,
    enforce_container_hardening,
    prepare_private_scratch,
)

STATUS = (
    "NoNewPrivs:\t1\nCapInh:\t{inh}\nCapPrm:\t{prm}\nCapEff:\t0000000000000000\n"
    "CapBnd:\t00000000a80425fb\nCapAmb:\t0000000000000000\n"
)
ZERO = "0000000000000000"
INHERITED = "00000000a80425fb"


class GuardFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.ro = self.base / "ro"
        self.rw = self.base / "rw"
        self.ro.mkdir()
        self.rw.mkdir()
        self.rw.chmod(0o700)
        self.ro.chmod(0o555)
        self.addCleanup(self.ro.chmod, 0o700)
        self.status = self.base / "status"

    def run_guard(
        self, drop: object, *, inh: str, prm: str = ZERO, scratch: Path | None = None
    ) -> HardeningReport:
        self.status.write_text(STATUS.format(inh=inh, prm=prm), encoding="utf-8")
        return enforce_container_hardening(
            uid_getter=lambda: 10001,
            euid_getter=lambda: 10001,
            gid_getter=lambda: 10001,
            egid_getter=lambda: 10001,
            umask_fn=lambda _: 0o022,
            dont_write_bytecode=True,
            platform="linux",
            prctl_fn=lambda: 0,
            drop_inheritable_fn=drop,  # type: ignore[arg-type]
            proc_status_path=self.status,
            immutable_paths=(self.ro,),
            writable_paths=(scratch or self.rw,),
        )


class InheritableCapabilityTests(GuardFixture):
    def test_inherited_mask_that_is_dropped_passes(self) -> None:
        self.status.write_text(STATUS.format(inh=INHERITED, prm=ZERO), encoding="utf-8")

        def drop() -> int:
            self.status.write_text(STATUS.format(inh=ZERO, prm=ZERO), encoding="utf-8")
            return 0

        report = enforce_container_hardening(
            uid_getter=lambda: 10001,
            euid_getter=lambda: 10001,
            gid_getter=lambda: 10001,
            egid_getter=lambda: 10001,
            umask_fn=lambda _: 0o022,
            dont_write_bytecode=True,
            platform="linux",
            prctl_fn=lambda: 0,
            drop_inheritable_fn=drop,
            proc_status_path=self.status,
            immutable_paths=(self.ro,),
            writable_paths=(self.rw,),
        )
        self.assertTrue(report.enforced)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux capset")
    def test_real_capset_succeeds_without_privileges(self) -> None:
        self.assertEqual(_drop_inheritable_capabilities(), 0)

    def test_failed_drop_leaving_mask_refuses(self) -> None:
        with self.assertRaisesRegex(ContainerHardeningError, "CapInh must be zero"):
            self.run_guard(lambda: -1, inh=INHERITED)

    def test_drop_reporting_success_but_mask_remaining_refuses(self) -> None:
        with self.assertRaisesRegex(ContainerHardeningError, "CapInh must be zero"):
            self.run_guard(lambda: 0, inh=INHERITED)

    def test_non_zero_permitted_set_still_refuses(self) -> None:
        with self.assertRaisesRegex(ContainerHardeningError, "CapPrm must be zero"):
            self.run_guard(lambda: 0, inh=ZERO, prm=INHERITED)


class ScratchDirectoryTests(GuardFixture):
    def test_world_writable_without_sticky_is_refused_and_private_subdirectory_accepted(
        self,
    ) -> None:
        mount = self.base / "emptydir"
        mount.mkdir()
        mount.chmod(0o777)
        with self.assertRaisesRegex(ContainerHardeningError, "without sticky bit"):
            self.run_guard(lambda: 0, inh=ZERO, scratch=mount)

        env = {
            "ZF_CONTAINER_HARDENING": "enforced",
            "TMPDIR": str(mount),
            "ZF_STATE": str(mount),
        }
        prepare_private_scratch(env, tmp_base=mount, state_base=mount)
        private = mount / "zf"
        self.assertEqual(env["TMPDIR"], str(private))
        self.assertEqual(env["ZF_STATE"], str(private))
        self.assertEqual(private.stat().st_mode & 0o777, 0o700)
        self.assertEqual(private.stat().st_uid, os.getuid())
        self.assertTrue(self.run_guard(lambda: 0, inh=ZERO, scratch=private).enforced)

    def test_helper_is_idempotent_and_skips_unset_state_and_non_enforced_mode(self) -> None:
        env = {"ZF_CONTAINER_HARDENING": "enforced"}
        for _ in range(2):
            prepare_private_scratch(env, tmp_base=self.rw, state_base=self.rw / "unused")
        self.assertEqual(env["TMPDIR"], str(self.rw / "zf"))
        self.assertNotIn("ZF_STATE", env)
        self.assertFalse((self.rw / "unused").exists())

        off: dict[str, str] = {"TMPDIR": "/tmp"}
        prepare_private_scratch(off, tmp_base=self.rw / "other")
        self.assertEqual(off, {"TMPDIR": "/tmp"})
        self.assertFalse((self.rw / "other").exists())

    def test_foreign_or_unusable_private_directory_is_refused(self) -> None:
        blocked = self.base / "blocked"
        blocked.write_text("not a directory", encoding="utf-8")
        with self.assertRaisesRegex(ContainerHardeningError, "Unable to prepare"):
            prepare_private_scratch(
                {"ZF_CONTAINER_HARDENING": "enforced"}, tmp_base=blocked, state_base=blocked
            )


if __name__ == "__main__":
    unittest.main()
