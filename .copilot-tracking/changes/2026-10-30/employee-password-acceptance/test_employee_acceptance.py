"""Constructed-only offline checks; never read credentials or launch a browser."""

import unittest
from unittest.mock import Mock, patch

from employee_acceptance import (
    APP,
    USERNAME,
    allowed_origin,
    authenticate,
    choose_action,
    parse_password,
    sanitize,
)


class SafetyTests(unittest.TestCase):
    def test_password_formats(self):
        for raw in (
            " \tSentinel!:= \r\nignored metadata\n",
            "password: Sentinel!:=\n",
            "PASSWORD= Sentinel!:=\n",
            '{"password": " Sentinel!:= "}',
            '{"Password": "Sentinel!:="}',
        ):
            self.assertEqual(parse_password(raw), "Sentinel!:=")

    def test_invalid_formats(self):
        for raw in (
            "",
            "  ",
            '{"password":',
            '{"password": 42}',
            '{"other": "x"}',
            '{"password":"x", "Password":"y"}',
            '{"password":"x", "password":"y"}',
            "password: ",
            USERNAME,
            "[not a supported format]",
        ):
            with (
                self.subTest(category="constructed-invalid"),
                self.assertRaises(ValueError),
            ):
                parse_password(raw)

    def test_password_punctuation(self):
        self.assertEqual(parse_password("  Sentinel@!:=\r\nmetadata"), "Sentinel@!:=")

    def test_origins(self):
        self.assertTrue(allowed_origin(APP + "/app", app=True))
        self.assertTrue(allowed_origin("https://login.microsoft.com/"))
        self.assertTrue(allowed_origin("https://login.microsoftonline.com/"))
        for url in (
            "http://login.microsoft.com",
            "https://login.microsoft.com.evil.test",
            "https://login.microsoft.com:444",
            "https://user@login.microsoft.com",
            APP + ".evil.test",
            "https://login.microsoftonline.com:bad",
        ):
            self.assertFalse(allowed_origin(url))
            self.assertFalse(allowed_origin(url, app=True))

    def test_redaction(self):
        text = (
            "Use your password instead\nSentinel!:=\nSentinel%21%3A%3D\n"
            + USERNAME
            + "\nAadiK%40DIAx90853289.OnMicrosoft.com\n"
            "https://login.microsoft.com/?token=private\nsomeone@example.test"
        )
        clean = sanitize(text, "Sentinel!:=")
        self.assertTrue(clean.startswith("Use your password instead\n"))
        for forbidden in ("Sentinel", "AadiK", "token=private", "someone@example"):
            self.assertNotIn(forbidden, clean)

    def test_finite_alternatives(self):
        used = set()
        names = ["Back", "Sign-in options", "Use your password instead", "GitHub"]
        actions = []
        while action := choose_action(names, used):
            used.add(action)
            actions.append(action[0])
        self.assertEqual(actions, ["password", "options", "back"])
        self.assertIsNone(choose_action(["GitHub", "Forgot password?"], used))

    def test_terminal_no_route_and_cycle(self):
        page = Mock(url="https://login.microsoft.com/")
        page.locator.return_value.count.return_value = 0
        for controls in (["GitHub"], ["Sign-in options"]):
            with (
                patch(
                    "employee_acceptance.public_state",
                    return_value={"controls": controls},
                ),
                patch("employee_acceptance.click_named") as click,
            ):
                record = {}
                outcome = authenticate(page, "constructed", record)
                self.assertEqual(outcome, "password_route_not_offered")
                self.assertNotIn("password_submitted", record)
                self.assertLessEqual(click.call_count, 1)

    def test_authenticated_callback(self):
        page = Mock(url=APP + "/app")
        with patch(
            "employee_acceptance.binding_probe", return_value={"authenticated": True}
        ):
            self.assertEqual(
                authenticate(page, "constructed", {}), "authenticated_callback"
            )
        page.locator.assert_not_called()

    def test_deadline_no_live_action_after_navigation(self):
        page = Mock(url="https://login.microsoft.com/")
        with patch("employee_acceptance.time.monotonic", side_effect=[0, 181]):
            self.assertEqual(
                authenticate(page, "constructed", {}), "authentication_deadline"
            )
        page.locator.assert_not_called()

    def test_only_one_password_submission(self):
        page = Mock(url="https://login.microsoft.com/")
        email, secret, submit, heading = Mock(), Mock(), Mock(), Mock()
        email.count.return_value = 1
        secret.count.return_value = 1
        submit.count.return_value = 1
        submit.get_attribute.side_effect = ["Next", "Sign in", "Sign in"]
        heading.count.return_value = 1
        heading.first.is_visible.return_value = True
        page.get_by_role.return_value = heading

        def locate(selector):
            if 'type="email"' in selector:
                return email
            if 'type="password"' in selector:
                return secret
            return submit

        page.locator.side_effect = locate
        with patch(
            "employee_acceptance.public_state",
            side_effect=[
                {"controls": [], "step": "username"},
                {"controls": [], "step": "password"},
                {"controls": [], "step": "password"},
            ],
        ):
            record = {}
            self.assertEqual(
                authenticate(page, "constructed", record),
                "password_rejected_or_challenge_repeated",
            )
        self.assertTrue(record["password_submitted"])
        email.fill.assert_called_once()
        secret.fill.assert_called_once_with("constructed")
        self.assertEqual(submit.press.call_count, 2)

    def test_password_decoy_on_username_page_is_not_filled(self):
        page = Mock(url="https://login.microsoft.com/")
        email, secret, submit, heading = Mock(), Mock(), Mock(), Mock()
        email.count.return_value = 1
        secret.count.return_value = 1
        submit.count.return_value = 1
        submit.get_attribute.return_value = "Next"
        heading.count.return_value = 0
        page.get_by_role.return_value = heading

        def locate(selector):
            if 'type="email"' in selector:
                return email
            if 'type="password"' in selector:
                return secret
            return submit

        page.locator.side_effect = locate
        with patch("employee_acceptance.public_state", return_value={"controls": []}):
            record = {}
            self.assertEqual(
                authenticate(page, "constructed", record), "password_route_not_offered"
            )
        email.fill.assert_called_once()
        secret.fill.assert_not_called()
        self.assertNotIn("password_submitted", record)


if __name__ == "__main__":
    unittest.main()
