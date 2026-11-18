"""Stable module name for #215 role alert owner, clock and safe-action matrix tests."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_epic215_role_alert_owner_clock_safe_action_matrix import (  # noqa: E402, F401
    RenderedAlertContractTests,
    RoleAlertDataTests,
)

if __name__ == "__main__":
    import unittest

    unittest.main()
