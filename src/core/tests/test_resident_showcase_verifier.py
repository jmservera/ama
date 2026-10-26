import io
import subprocess
import sys
import unittest
from collections.abc import Callable
from pathlib import Path

from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_verifier as rv

SCRIPT = Path(__file__).resolve().parents[3] / "infra" / "scripts" / "resident_demo_verifier.py"


def load_main() -> Callable[..., int]:
    namespace: dict[str, object] = {"__name__": "verifier_under_test", "__file__": str(SCRIPT)}
    exec(compile(SCRIPT.read_text(), str(SCRIPT), "exec"), namespace)
    main = namespace["main"]
    assert callable(main)
    return main


# Unmistakably fake fixture strings. None is a real or reusable password.
GOOD = "Fq7!rT4#kL9@wX2$mB5%vN-fixture"


class PolicyTests(unittest.TestCase):
    def test_a_strong_fixture_passes_and_the_verifier_verifies_it(self) -> None:
        self.assertIsNone(rv.check_strength(GOOD))
        verifier = rs.PasswordVerifier(rv.build_verifier(GOOD))
        self.assertTrue(verifier.verify(GOOD))
        self.assertFalse(verifier.verify(GOOD + "x"))

    def test_weak_candidates_are_rejected_without_echoing_them(self) -> None:
        weak = [
            "Short1!a",
            "a" * 30,
            "Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!",
            "abcdefghijklmnopqrstuvwxyz",
            "Fq7!rT4#kL9@wX2$mB5%vN-password",
            "Fq7!rT4#kL9@wX2$mB5%vN-ZAVA",
            " " + GOOD,
            GOOD + "\x01",
            "Fq7!rT4#kL9@wX2$mB5%vN-" + "qqqq",
            "x" * 200,
        ]
        for candidate in weak:
            reason = rv.check_strength(candidate)
            self.assertIsNotNone(reason, candidate)
            assert reason is not None
            self.assertNotIn(candidate.strip(), reason)
            with self.assertRaises(ValueError):
                rv.build_verifier(candidate)

    def test_each_verifier_has_a_fresh_salt(self) -> None:
        self.assertNotEqual(rv.build_verifier(GOOD), rv.build_verifier(GOOD))


class CliTests(unittest.TestCase):
    def run_main(
        self, argv: list[str], interactive: bool, answers: list[str]
    ) -> tuple[int, str, str, list[str]]:
        out, err, asked = io.StringIO(), io.StringIO(), []
        feed = iter(answers)

        def prompt(text: str) -> str:
            asked.append(text)
            return next(feed)

        code = load_main()(argv, interactive, out, err, prompt)
        return code, out.getvalue(), err.getvalue(), asked

    def test_success_prints_only_a_verifier_and_never_the_password(self) -> None:
        code, out, err, asked = self.run_main(["tool"], True, [GOOD, GOOD])
        self.assertEqual(code, 0)
        self.assertEqual(len(asked), 2)
        self.assertTrue(out.startswith("scrypt$") and out.count("\n") == 1)
        self.assertTrue(rs.PasswordVerifier(out.strip()).verify(GOOD))
        self.assertNotIn(GOOD, out + err)

    def test_echo_that_cannot_be_disabled_is_refused_before_input(self) -> None:
        import getpass
        import warnings

        read: list[str] = []

        def unsafe(text: str) -> str:
            warnings.warn("Can not control echo", getpass.GetPassWarning, stacklevel=2)
            read.append(text)
            return GOOD

        out, err = io.StringIO(), io.StringIO()
        code = load_main()(["tool"], True, out, err, unsafe)
        self.assertEqual((code, out.getvalue(), read), (1, "", []))
        self.assertNotIn(GOOD, err.getvalue())

    def test_arguments_and_non_interactive_input_are_refused_before_any_prompt(self) -> None:
        for argv, interactive in ((["tool", GOOD], True), (["tool"], False)):
            code, out, err, asked = self.run_main(argv, interactive, [GOOD, GOOD])
            self.assertEqual((code, out, asked), (2, "", []))
            self.assertNotIn(GOOD, err)

    def test_mismatch_weak_and_cancel_print_nothing_on_stdout(self) -> None:
        for answers in ([GOOD, GOOD + "x"], ["weak", "weak"]):
            code, out, err, _ = self.run_main(["tool"], True, answers)
            self.assertEqual((code, out), (1, ""))
            for answer in answers:
                self.assertNotIn(answer, err)

        def cancel(_: str) -> str:
            raise KeyboardInterrupt

        sink, errsink = io.StringIO(), io.StringIO()
        self.assertEqual(load_main()(["tool"], True, sink, errsink, cancel), 1)
        self.assertEqual(sink.getvalue(), "")

    def test_unexpected_failure_is_generic_with_no_traceback_or_secret(self) -> None:
        def boom(_: str) -> str:
            raise RuntimeError(GOOD)

        out, err = io.StringIO(), io.StringIO()
        self.assertEqual(load_main()(["tool"], True, out, err, boom), 1)
        self.assertEqual(out.getvalue(), "")
        self.assertNotIn(GOOD, err.getvalue())
        self.assertNotIn("Traceback", err.getvalue())

    def test_the_real_script_refuses_arguments_and_piped_input(self) -> None:
        for args, stdin in (([], GOOD + "\n" + GOOD + "\n"), ([GOOD], "")):
            done = subprocess.run(
                [sys.executable, str(SCRIPT), *args],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(done.returncode, 2)
            self.assertEqual(done.stdout, "")
            self.assertNotIn(GOOD, done.stderr)
            self.assertNotIn("Traceback", done.stderr)


if __name__ == "__main__":
    unittest.main()
