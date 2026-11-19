"""Stable module name for #215 doubt-route and held-state WCAG parity tests."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_epic215_doubt_route_held_state_wcag_parity import (  # noqa: E402, F401
    DoubtRouteRoleParityTests,
    StaticHeldStateContractTests,
)

if __name__ == "__main__":
    import unittest

    unittest.main()
