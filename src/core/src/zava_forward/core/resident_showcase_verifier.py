"""Owner-side password policy and verifier builder for the synthetic resident showcase.

The owner chooses and keeps the shared demo password. This module never generates, stores or
prints a password. It only checks that a candidate is not trivially weak, without echoing it, and
builds the scrypt verifier the showcase already verifies. The rules reject predictable patterns;
they are not proof of strength, so a password-manager random value is the recommended choice.
"""

from . import resident_showcase as _rs

MIN_LENGTH = 20
MAX_LENGTH = 128
MIN_DISTINCT = 10
MAX_PERIOD = 8
COMMON_PARTS = (
    "password",
    "passw0rd",
    "qwerty",
    "123456",
    "abcdef",
    "letmein",
    "welcome",
    "admin",
    "zava",
    "demo",
    "example",
    "showcase",
)


def check_strength(password: str) -> str | None:
    """Return a generic reason the candidate is rejected, or None. Never includes the value."""
    if not MIN_LENGTH <= len(password) <= MAX_LENGTH:
        return f"Use between {MIN_LENGTH} and {MAX_LENGTH} characters."
    if password != password.strip() or any(ord(c) < 32 or ord(c) == 127 for c in password):
        return "Do not start or end with a space and avoid control characters."
    classes = (
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    )
    if sum(classes) < 3:
        return "Mix at least three of lower case, upper case, digits and symbols."
    if len(set(password)) < MIN_DISTINCT:
        return "Use more different characters."
    if any(
        all(password[i] == password[i % period] for i in range(len(password)))
        for period in range(1, MAX_PERIOD + 1)
    ):
        return "Avoid repeating a short pattern."
    if any(len(set(password[i : i + 4])) == 1 for i in range(len(password) - 3)):
        return "Avoid runs of the same character."
    lowered = password.casefold()
    if any(part in lowered for part in COMMON_PARTS):
        return "Avoid common words and names related to this demo."
    return None


def build_verifier(password: str) -> str:
    """Strength-check then build the verifier. Raises ValueError with a generic reason."""
    reason = check_strength(password)
    if reason is not None:
        raise ValueError(reason)
    return _rs.make_verifier(password)
