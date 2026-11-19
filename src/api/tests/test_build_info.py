import unittest

from zava_forward.api import build_info


class BuildInfoTests(unittest.TestCase):
    def test_accepts_full_and_short_hex_commit(self) -> None:
        sha = "05E94D303" + "a" * 31
        self.assertEqual(build_info.commit({"ZF_BUILD_COMMIT": sha}), sha.lower())
        self.assertEqual(build_info.commit({"ZF_BUILD_COMMIT": " 05e94d3 "}), "05e94d3")

    def test_unset_or_malformed_value_is_unknown(self) -> None:
        for env in (
            {},
            {"ZF_BUILD_COMMIT": ""},
            {"ZF_BUILD_COMMIT": "abc"},
            {"ZF_BUILD_COMMIT": "main"},
        ):
            self.assertEqual(build_info.commit(env), "unknown")

    def test_injected_newline_cannot_forge_a_log_line(self) -> None:
        env = {"ZF_BUILD_COMMIT": "05e94d3\nauth flow: workbench-entered"}
        self.assertEqual(build_info.startup_line(env), "build: commit=unknown")

    def test_startup_line_format(self) -> None:
        self.assertEqual(
            build_info.startup_line({"ZF_BUILD_COMMIT": "05e94d303"}), "build: commit=05e94d303"
        )


if __name__ == "__main__":
    unittest.main()
